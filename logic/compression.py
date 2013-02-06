import os
import subprocess
import shutil
from logger import Logger
from logic.file import File
from logic.logicError import LogicError

class Compression:
    def __init__(self):
        None

    class FineCompression:
        @staticmethod
        def finecompress(name, verbose):
            Logger.log("FineCompress "+name)
            
            audacity_data = File.datadirectoryFromName(name)
            verbose_arg = "v" if verbose else ""
            
            Logger.log("Deleting .bz2 files with no matching .au files")
            for compressedfile in filter(lambda x: x.endswith(".bz2"), File.allFiles(audacity_data)):
                audiofile = os.path.splitext(compressedfile)[0]
        
                if not os.path.exists(audiofile):
                    Logger.log(compressedfile + " should match " + audiofile + " but does not exist anymore. Deleting.")
                    os.remove(compressedfile)
            
            Logger.log("Compressing modified audio files")
            for audiofile in filter(lambda x: x.endswith(".au"), File.allFiles(audacity_data)):     
                compressedfile=audiofile+".bz2"
                if not os.path.exists(compressedfile) or File.fileModificationTimestamp(audiofile) > File.fileModificationTimestamp(compressedfile):
                    Logger.log("Compress "+audiofile)
                    output = subprocess.check_output(["bzip2", "-zf"+verbose_arg, audiofile])
                else:
                    os.remove(audiofile)
        
        @staticmethod
        def finedecompress(name, verbose):
            Logger.log("FineDecompress "+name)
            
            audacity_data = File.datadirectoryFromName(name)
            verbose_arg = "v" if verbose else ""
            
            filelist = File.allFiles(audacity_data)
            if any(s.endswith(".au") for s in filelist):
                raise LogicError("existing .au file found during decompress")    
            
            Logger.log("Decompressing files")
            for compressedfile in filter(lambda x: x.endswith(".bz2"), filelist):
                Logger.log("Decompress "+compressedfile)
                output = subprocess.check_output(["bzip2", "-dk"+verbose_arg, compressedfile])
                
    class ArchiveCompression:
        @staticmethod
        def compress(name, verbose, overwrite = False):
            Logger.log("Compress "+name)
            
            archive = File.archiveFromName(name)
            audacity_data = File.datadirectoryFromName(name)
            verbose_arg = "v" if verbose else ""
            
            if os.path.isdir(audacity_data) == False:
                raise LogicError("audio data directory " + audacity_data + " does not exist.")
            
            if os.path.isfile(archive) and overwrite is False:
                raise LogicError("audio archive " + archive + " does already exist. Will not overwrite existing files.")
            elif os.path.isfile(archive) and overwrite is True:
                Logger.log(" Deleting old existing archive")
                os.remove(archive)
            
            Logger.log(" Compressing")
            output = subprocess.check_output(["tar", "-cj"+verbose_arg+"f", archive, audacity_data])
            Logger.log(output)
            
            Logger.log(" Deleting old data")
            shutil.rmtree(audacity_data)
        
        @staticmethod             
        def decompress(name, verbose, keep = False):
            Logger.log("Decompress "+name)
            
            archive = File.archiveFromName(name)
            audacity_data = File.datadirectoryFromName(name)
            verbose_arg = "v" if verbose else ""
            
            if os.path.isfile(archive) == False:
                raise LogicError("audio archive " + archive + " does not exist.")
            
            if os.path.isdir(audacity_data):
                raise LogicError("audio data directory " + audacity_data + " does already exist. Will not overwrite existing files.")
            
            Logger.log(" Decompressing")
            output = subprocess.check_output(["tar", "-xj"+verbose_arg+"f", archive, audacity_data])
            Logger.log(output)
            
            if keep is False:
                Logger.log(" Deleting old data")
                os.remove(archive)
    