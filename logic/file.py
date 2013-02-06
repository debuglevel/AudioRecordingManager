import os
from logger import Logger
from logic.logicError import LogicError

class File:
    def __init__(self):
        None
        
    @staticmethod
    def projectfileFromName(name):
        return "%s/%s.aup" %(name, name)
    
    @staticmethod
    def metadatafileFromName(name):
        return "%s/%s.json" %(name, name)
    
    @staticmethod
    def archiveFromName(name):
        return "%s/%s.tar.bz2" %(name, name)
    
    @staticmethod
    def datadirectoryFromName(name):
        return "%s/%s_data" %(name, name)
    
    @staticmethod
    def allFiles(directory):
        filelist = []
        
        for root, subFolders, files in os.walk(directory):
            files = filter(lambda x: not os.path.isdir(x), files)
            for file in files:
                filelist.append(root + "/" + file)
                
        return filelist
    
    @staticmethod
    def fileCreationTimestamp(file):
        return os.path.getctime(file)
    
    @staticmethod
    def fileModificationTimestamp(file):
        return os.path.getmtime(file)
    
    @staticmethod
    def isCompressed(name):
        archive = File.archiveFromName(name)
        return os.path.exists(archive)
    
    @staticmethod
    def newestDataTimestamp(dataDirectory):
        fileList = []
        
        for root, subFolders, files in os.walk(dataDirectory):
            files = filter(lambda x: not os.path.isdir(x), files)
            for file in files:
                fileList.append(root + "/" + file)
            
        newest = max(fileList, key=lambda x: os.stat(x).st_mtime)
            
        return os.stat(newest).st_mtime