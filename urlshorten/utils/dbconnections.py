import MySQLdb
import logging
import redis
import base64

TABLE_NAME = "urls"

INSERT_COMMAND = "insert ignore into "+TABLE_NAME+ " ( longurl ) values ( '%s' )"
SELECT_COMMAND = "select longurl from "+TABLE_NAME+ " where id = '%s' " 
 
class DbConnections():

    def __init__(self, dbhandler):
        self.dbhandler = dbhandler

    @classmethod
    def fromConfig(cls,config_obj):
        config = config_obj.dataMap
        redis_config = config['redis']
        redis_client = redis.Redis(redis_config.get('host','127.0.0.1'), redis_config.get('port',6379))
    
        mysql_config = config['mysql']
        mysql_client = MySQLdb.connect(host=mysql_config.get('host','127.0.0.1'),user=mysql_config['user'],passwd=mysql_config['passwd'],db=mysql_config['db'])
        return cls( DbHandler(redis_client,mysql_client) )
        
class DbHandler:
    def __init__(self,redis_client,mysql_client):
        self.redis_client = redis_client
        self.mysql_client = mysql_client        
        
    def set_data_in_redis(self, short_url, long_url):
        return self.redis_client.setex(short_url,long_url, 10*60)
        
    def insert_data_in_mysql(self,long_url):
        try:
            encoded_data = base64.b64encode(long_url, "-_")
            logging.debug("inserting data in mysql. url=" + str(long_url)+ " encoded="+str(encoded_data))
            mysql_cur = self.mysql_client.cursor()
            sqt_stmt = INSERT_COMMAND % (encoded_data,)
            self.mysql_client.commit() 
            mysql_cur.execute(sqt_stmt)
            return mysql_cur.lastrowid
        except Exception as e:
            logging.exception("error while inserting data in mysql for: %s  reason: %s", long_url, e.message) 
        
    def get_data_from_redis(self,short_url):
        return self.redis_client.get(short_url)
                
    def get_data_from_mysql(self, integer_value):
        try:
            logging.debug("fetching data from mysql. data=" + str(integer_value))            
            mysql_cur = self.mysql_client.cursor()
            sqt_stmt = SELECT_COMMAND % (integer_value,)
            mysql_cur.execute(sqt_stmt)
            long_url = None
            for row in mysql_cur.fetchall():
                long_url =  row[0]
            if not long_url:
                return None    
            return base64.urlsafe_b64decode(long_url)  
        except Exception as e:
                logging.exception("error fetching data from mysql for: %s  reason: %s", integer_value, e.message)    

