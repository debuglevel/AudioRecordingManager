import subprocess
import shutil
from file import File
from logger import Logger
from compression import Compression
from logic.logicError import LogicError

class Open:
    def __init__(self):
        None

    @staticmethod
    def openproject(name, verbose):
        audacity_project = File.projectfileFromName(name)
        audacity_data = File.datadirectoryFromName(name)
        archive = File.archiveFromName(name)
        
        if File.isCompressed(name):
            Compression.ArchiveCompression.decompress(name, verbose, keep=True)
        
        Logger.log(" Open")
        process = subprocess.Popen(["audacity", audacity_project])
        process.wait() # NOTE: switch to communicate() if wait() blocks the process because of a full pipe
        
        if File.newestDataTimestamp(audacity_data) > File.fileModificationTimestamp(archive):
            Logger.log(" Compress changed data files")
            Compression.ArchiveCompression.compress(name, verbose, overwrite=True)
        else:
            Logger.log(" Deleting unchanged data files")
            shutil.rmtree(audacity_data)
            
    @staticmethod
    def fineopenproject(name, verbose):
        audacity_project = File.projectfileFromName(name)
        
        Compression.FineCompression.finedecompress(name, verbose)
        
        Logger.log(" Open")
        process = subprocess.Popen(["audacity", audacity_project])
        process.wait() # NOTE: switch to communicate() if wait() blocks the process because of a full pipe
        
        Compression.FineCompression.finecompress(name, verbose)