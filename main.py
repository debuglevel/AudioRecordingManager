#!/usr/bin/python2.7

import sys
import os
import datetime

from logic.metadata import Metadata
from logger import Logger
from logic.compression import Compression
from logic.open import Open

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.2
__updated__ = '2013-02-06'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

class TextInterface:
    def __init__(self):
        None
        
    class SingleOperations:
        @staticmethod
        def printAllMetadata(name):
            timestamps = Metadata.getProjectfileTimestamps(name)
            
            print "Project creation:     \t" + str(datetime.datetime.fromtimestamp(timestamps["creation"]))
            print "Project last modified:\t" + str(datetime.datetime.fromtimestamp(timestamps["modification"]))
            
            for key, value in Metadata.getAnnotations(name).iteritems():
                print "%s:\t\t%s" % (key, value)
        
        @staticmethod
        def printMetadata(name, key):
            annotations = Metadata.getAnnotations(name)
            if annotations.has_key(key):
                print "%s: %s" % (key, annotations[key])
            else:
                print "%s: %s" % (key, "<NOT SET>")
                        
        @staticmethod
        def setMetadata(name, key, value):
            Metadata.setMetadata(name, key, value)
        
        @staticmethod
        def compress(name, verbose):
            Compression.ArchiveCompression.compress(name, verbose, False)
                  
        @staticmethod
        def decompress(name, verbose):
            Compression.ArchiveCompression.decompress(name, verbose, False)
        
        @staticmethod
        def finecompress(name, verbose):
            Compression.FineCompression.finecompress(name, verbose)
        
        @staticmethod
        def finedecompress(name, verbose):
            Compression.FineCompression.finedecompress(name, verbose)
        
        @staticmethod
        def openproject(name, verbose):
            Open.openproject(name, verbose)
            
        @staticmethod
        def fineopenproject(name, verbose):
            Open.fineopenproject(name, verbose)
        
        @staticmethod
        def test(name):
            None
            
    class BatchOperations:
        def __init__(self):
            None

        @staticmethod
        def printAllMetadata(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.printAllMetadata(name)
                
        @staticmethod
        def printMetadata(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.printMetadata(name, args.key)
                        
        @staticmethod
        def setMetadata(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.setMetadata(name, args.key, args.value)
        
        @staticmethod
        def compress(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.compress(name, args.verbose)

        @staticmethod
        def decompress(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.decompress(name, args.verbose)
                                        
        @staticmethod
        def finecompress(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.finecompress(name, args.verbose)
        
        @staticmethod
        def finedecompress(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.finedecompress(name, args.verbose)
        
        @staticmethod
        def openproject(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.openproject(name, args.verbose)

        @staticmethod
        def fineopenproject(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.fineopenproject(name, args.verbose)
                
        @staticmethod
        def test(args):
            for name in args.projects:
                Logger.log("Processing "+name)
                TextInterface.SingleOperations.test(name)


    def setupParsers(self):
        parser = ArgumentParser(description=Info.program_shortdesc, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=Info.program_version_message)
        
        subparsers = parser.add_subparsers(title='commands',
                                           description='available commands to process projects')
        
        subparser = {}
        
        metadata_subparser = subparsers.add_parser('metadata', help='manage metadata')
        metadata_subparsers = metadata_subparser.add_subparsers(title='commands',
                                                              description='available commands to manage metadata')
      
        subparser['metadata_printAll'] = metadata_subparsers.add_parser('printAll', help='print all metadata of a project')
        subparser['metadata_printAll'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['metadata_printAll'].set_defaults(func=TextInterface.BatchOperations.printAllMetadata)
        
        subparser['metadata_print'] = metadata_subparsers.add_parser('print', help='print specific metadata of a project')
        subparser['metadata_print'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['metadata_print'].add_argument(dest="key", help="key to retrieve", metavar="key")
        subparser['metadata_print'].set_defaults(func=TextInterface.BatchOperations.printMetadata)
        
        subparser['metadata_set'] = metadata_subparsers.add_parser('set', help='set specific metadata of a project')
        subparser['metadata_set'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['metadata_set'].add_argument(dest="key", help="key to store", metavar="key")
        subparser['metadata_set'].add_argument(dest="value", help="value to store in key", metavar="value")
        subparser['metadata_set'].set_defaults(func=TextInterface.BatchOperations.setMetadata)
        
        subparser['compress'] = subparsers.add_parser('compress', help='compress audio files into archive')
        subparser['compress'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['compress'].set_defaults(func=TextInterface.BatchOperations.compress)
        
        subparser['decompress'] = subparsers.add_parser('decompress', help='decompress audio files from archive')
        subparser['decompress'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['decompress'].set_defaults(func=TextInterface.BatchOperations.decompress)

        subparser['finecompress'] = subparsers.add_parser('finecompress', help='compress audio files')
        subparser['finecompress'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['finecompress'].set_defaults(func=TextInterface.BatchOperations.finecompress)
        
        subparser['finedecompress'] = subparsers.add_parser('finedecompress', help='decompress audio files')
        subparser['finedecompress'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['finedecompress'].set_defaults(func=TextInterface.BatchOperations.finedecompress)

        subparser['openproject'] = subparsers.add_parser('open', help='open audio project using audacity (from archive)')
        subparser['openproject'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['openproject'].set_defaults(func=TextInterface.BatchOperations.openproject)

        subparser['fineopenproject'] = subparsers.add_parser('fineopen', help='open audio project using audacity (fine per-file compression)')
        subparser['fineopenproject'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['fineopenproject'].set_defaults(func=TextInterface.BatchOperations.fineopenproject)

        subparser['test'] = subparsers.add_parser('test', help='test function')
        subparser['test'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['test'].set_defaults(func=TextInterface.BatchOperations.test)

        args = parser.parse_args()
        args.func(args)

    def main(self, argv=None): # IGNORE:C0111
        '''Command line options.'''
        
        if argv is None:
            argv = sys.argv
        else:
            sys.argv.extend(argv)
    
        try:
            parser = self.setupParsers()
               
            return 0
        except KeyboardInterrupt:
            ### handle keyboard interrupt ###
            return 0
        except Exception, e:
            if DEBUG or TESTRUN:
                raise(e)
            indent = len(Info.program_name) * " "
            sys.stderr.write(Info.program_name + ": " + repr(e) + "\n")
            sys.stderr.write(indent + "  for help use --help")
            return 2

class Info:
    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = "tool to process certain actions on audacity based audio projects"

if __name__ == "__main__":
    textInterface = TextInterface()
    
    if DEBUG:
        None
        #sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = '${module}_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(textInterface.main())