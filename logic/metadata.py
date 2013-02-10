import json
import os
from file import File
from logger import Logger
from logic.logicError import LogicError

class Metadata:
    def __init__(self):
        None
    
    @staticmethod
    def listUsedAnnotations(rootdirectory):
        annotationlist = []
        
        projects = File.allProjects(rootdirectory)
        for project in projects:
            projectannotations = Metadata.getAnnotations(project)
            for projectannotation in projectannotations:
                if not projectannotation in annotationlist:
                    annotationlist.append(projectannotation)
        
        return annotationlist
    
    @staticmethod
    def saveAnnotations(name, dict):
        metadatafile = File.metadatafileFromName(name)
        fp = open(metadatafile, mode='w')
        json.dump(dict, fp)
        #file.flush()
    
    @staticmethod
    def getAnnotations(name):
        metadatafile = File.metadatafileFromName(name)
        if os.path.exists(metadatafile):
            json_data=open(metadatafile)
            data = json.load(json_data)
            json_data.close()
        else:
            data = {}
        
        return data
    
    @staticmethod
    def setMetadata(name, key, value):
        annotations = Metadata.getAnnotations(name)
        annotations[key] = value
        Metadata.saveAnnotations(name, annotations)
        
    @staticmethod
    def getProjectfileTimestamps(name):
        projectfile = File.projectfileFromName(name)
        
        timestamps = {}
        timestamps["creation"] = File.fileCreationTimestamp(projectfile)
        timestamps["modification"] = File.fileModificationTimestamp(projectfile)
        
        return timestamps   