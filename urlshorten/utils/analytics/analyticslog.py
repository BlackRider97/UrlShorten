import logging
import logging.handlers
from configuration import LoggerConfig 

'''
Class: FileLogger, which is unaware of analytics, is meant to log the required 
events<tag, map> to a back end file.
'''

class FileLogger:

    logger = None

    @staticmethod
    def initLogger():
        if FileLogger.logger == None:
            FileLogger.logger = logging.getLogger("analytics")
            FileLogger.logger.propagate = False #log messages here don't go to the parent
            FileLogger.logger.setLevel(logging.INFO)
            handler = logging.handlers.TimedRotatingFileHandler(filename=LoggerConfig.logFilePython,
                                                                interval=1,
                                                                when='h',
                                                                backupCount=24)

            formatter = logging.Formatter('%(asctime)s|%(message)s', "%Y-%m-%d %H:%M%Z")
            handler.setFormatter(formatter)
            FileLogger.logger.addHandler(handler)

            #add syslog handler
            handler = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_LOCAL1)
            handler.setFormatter(formatter)
            FileLogger.logger.addHandler(handler)

    @staticmethod    
    def info(obj_tag, obj_map):
        if FileLogger.logger == None:
            FileLogger.initLogger()

        message = obj_tag + "|" + obj_map
        FileLogger.logger.info(message)

if __name__=="__main__":
    FileLogger.info("Hello", "world")