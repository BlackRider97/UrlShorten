import logging
from ..config import Config
import os

class LoggerConfig:
    config_obj = Config()
    config = config_obj.dataMap
    
    logDirPython = config.get('pythonlogdir')
    
    if not logDirPython:
        logDirPython = Config().def_home_dir+"/logs/"
    
    if not os.path.exists(logDirPython):
        os.makedirs(logDirPython)
    
    logStatusFilePython = logDirPython + "status.txt"
    logSnapshotDirPython = logDirPython + "snapshots/"
    logFilePrefixPython = "analytics"
    logFilePython = logDirPython + logFilePrefixPython + ".log"
    logFormat = '%(asctime)s|%(message)s'
    logDateFormat = "%Y-%m-%d %H:%M%Z"
    logLevel = logging.INFO
    analyticsEngine = "mixpanel" 
    
    @staticmethod
    def getAnalyticsEngine():
        return LoggerConfig.analyticsEngine
    
    @staticmethod
    def getLogFilePrefix():
        return LoggerConfig.logFilePrefixPython
    
    @staticmethod
    def getLogStatusFile():
        return LoggerConfig.logStatusFilePython
    
    @staticmethod
    def getSnapshotDir():
        return LoggerConfig.logSnapshotDirPython
    
    @staticmethod
    def getLogDir():
        return LoggerConfig.logDirPython 
       
    @staticmethod
    def getLogFile():
        return LoggerConfig.logFilePythona
    
    @staticmethod
    def getLogFormat():
        return LoggerConfig.logFormat
    
    @staticmethod
    def getLogDateFormat():
        return LoggerConfig.logDateFormat
    
    @staticmethod
    def getLogLevel():
        return LoggerConfig.logLevel
