#!/usr/bin/python2.7

import sys
import os
import subprocess
import shutil

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__updated__ = '2013-01-23'

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

def log(msg):
    print(msg)

def compress(path, verbose):
    log("Compress "+path)
    
    archive = path+"/"+path+".tar.bz2"
    audacity_data = path+"/"+path+"_data"
    verbose_arg = "v" if verbose else ""
    
    if os.path.isdir(audacity_data) == False:
        raise CLIError("audio data directory " + audacity_data + " does not exist.")
    
    if os.path.isfile(archive):
        raise CLIError("audio archive " + archive + " does already exist. Will not overwrite existing files.")
    
    log(" Compressing")
    output = subprocess.check_output(["tar", "-cj"+verbose_arg+"f", archive, audacity_data])
    log(output)
    
    log(" Deleting old data")
    shutil.rmtree(audacity_data)

def compress_cli(args):
    for path in args.projects:
        log("Processing "+path)
        compress(path, args.verbose)

def decompress(path, verbose):
    log("Decompress "+path)
    
    archive = path+"/"+path+".tar.bz2"
    audacity_data = path+"/"+path+"_data"
    verbose_arg = "v" if verbose else ""
    
    if os.path.isfile(archive) == False:
        raise CLIError("audio archive " + archive + " does not exist.")
    
    if os.path.isdir(audacity_data):
        raise CLIError("audio data directory " + audacity_data + " does already exist. Will not overwrite existing files.")
    
    log(" Decompressing")
    output = subprocess.check_output(["tar", "-xj"+verbose_arg+"f", archive, audacity_data])
    log(output)
    
    log(" Deleting old data")
    os.remove(archive)
    
def decompress_cli(args):
    for path in args.projects:
        log("Processing "+path)
        decompress(path, args.verbose)

def isCompressed(path):
    archive = path+"/"+path+".tar.bz2"
    return os.path.exists(archive)
    
def open(path, verbose):
    audacity_project = path+"/"+path+".aup"
    
    if isCompressed(path):
        decompress(path, verbose)
    
    log(" Open")
    process = subprocess.Popen(["audacity", audacity_project])
    process.wait() # NOTE: switch to communicate() if wait() blocks the process because of a full pipe
    
    compress(path, verbose)

def open_cli(args):
    for path in args.projects:
        log("Processing "+path)
        open(path, args.verbose)

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = "tool to process certain actions on audacity based audio projects"

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_shortdesc, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        subparsers = parser.add_subparsers(title='commands',
                                           description='available commands to process projects')
        
        subparser = {}
        subparser['open_cli'] = subparsers.add_parser('open', help='open audio project using audacity')
        subparser['open_cli'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['open_cli'].set_defaults(func=open_cli)
        
        subparser['compress_cli'] = subparsers.add_parser('compress', help='compress audio files into archive')
        subparser['compress_cli'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['compress_cli'].set_defaults(func=compress_cli)
        
        subparser['decompress_cli'] = subparsers.add_parser('decompress', help='decompress audio files from archive')
        subparser['decompress_cli'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['decompress_cli'].set_defaults(func=decompress_cli)

        args = parser.parse_args()
        args.func(args)
   
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
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
        statsfile = open_cli("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())