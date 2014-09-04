Installation on Ubuntu:
=======================
1. $sudo apt-get install fabric              (install fabric )
2. $sudo apt-get install python-virtualenv   (installl virtaualenv)
3. $sudo apt-get install python-dev libmysqlclient-dev python-mysqldb (install mysql and its python client dependencies)
4. $sudo apt-get install -y redis-server (install redis)
5. $redis-server ( to run the redis server )
6. Make sure mysql is running

Mysql Commands
==============
CREATE DATABASE shorten;  
CREATE TABLE `urls` 
(
  `id` bigint(15) NOT NULL AUTO_INCREMENT,
  `longurl` varchar(10000) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8; 
 

How to run server:
=================

$ cd /path-to-this-directory/UrlShorten/  ( go to this project directory)

On localhost
-------------
Bootstrap the project ( only one time requirement )
1. fab setup_localhost

To run the server
1. source ./venv/bin/activate 
2. python urlshorten/server.py 

Also added fabfile for production and staging environment which uses supervisor as process watcher.
see supervisor conf file
$ vi ./bin/urlshorten.conf 


On production
-------------
Bootstrap the project ( only one time requirement )
1. fab production create_virtualenv

To depoy code and run the server
1. fab production all


On staging
-------------
Bootstrap the project ( only one time requirement )
1. fab staging create_virtualenv

To depoy code and run the server
1. fab staging all  

Also added fabfile for production and staging environment which uses supervisor as process watcher.
see supervisor conf file
$ vi ./conf/urlshorten.conf

 
Uses:
=====
1. curl "http://localhost:5000" -X POST  -d "http://www.google.com"
Response
{
  "pass": "true", 
  "url": "1Z"
}

2. $  curl "http://localhost:5000/1Z"  -X GET
Response
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="http://www.google.com">http://www.google.com</a>.  If not click the link.

Features:
========

1. Caching data in redis to avoid hot spoting problem which means that most accessed data in being cached for 10 minutes.
   if data is not accessed within this time it will be get deleted from cache.

2. Using a-zA-Z0-9 characters for generating short urls.

3. Added analytics log for each request access
   logs can be seen in ./logs/analytics.log 
   log file rotates after 1 hour

4. Added fabfile for production and staging environment to manage your easy deployment and server restarts
