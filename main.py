#!/usr/local/bin/python2.7
# encoding: utf-8
'''
${module} -- ${shortdesc}

${module} is a ${description}

It defines ${classes_and_methods}

@author:     ${user_name}
        
@copyright:  ${year} ${organization_name}. All rights reserved.
        
@license:    ${license}

@contact:    ${user_email}
@deffield    updated: Updated
'''

import sys
import os
import subprocess
import shutil

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '${isodate}'
__updated__ = '${isodate}'

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

def compress(args):
    for path in args.projects:
        log("Processing "+path)
        archive = path+"/"+path+".tar.bz2"
        audacity_data = path+"/"+path+"_data"
        verbose_arg = "v" if args.verbose else ""
        
        if os.path.isdir(audacity_data) == False:
            raise CLIError("audio data directory " + audacity_data + " does not exist.")
        
        if os.path.isfile(archive):
            raise CLIError("audio archive " + archive + " does already exist. Will not overwrite existing files.")
        
        log(" Compressing")
        output = subprocess.check_output(["tar", "-cj"+verbose_arg+"f", archive, audacity_data])
        log(output)
        
        log(" Deleting old data")
        shutil.rmtree(audacity_data)
    
def decompress(args):
    for path in args.projects:
        log("Processing "+path)
        archive = path+"/"+path+".tar.bz2"
        audacity_data = path+"/"+path+"_data"
        verbose_arg = "v" if args.verbose else ""
        
        if os.path.isfile(archive) == False:
            raise CLIError("audio archive " + archive + " does not exist.")
        
        if os.path.isdir(audacity_data):
            raise CLIError("audio data directory " + audacity_data + " does already exist. Will not overwrite existing files.")
        
        log(" Decompressing")
        output = subprocess.check_output(["tar", "-xj"+verbose_arg+"f", archive, audacity_data])
        log(output)
        
        log(" Deleting old data")
        os.remove(archive)
    
def open(args):
    for path in args.projects:
        log("Processing "+path)
        audacity_project = path+"/"+path+".aup"
        
        log(" Open")
        subprocess.Popen(["audacity", audacity_project])

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
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by ${user_name} on %s.
  Copyright ${year} ${organization_name}. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        subparsers = parser.add_subparsers(title='commands',
                                           description='available commands to process projects')
        
        subparser = {}
        subparser['open'] = subparsers.add_parser('open', help='open audio project using audacity')
        subparser['open'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['open'].set_defaults(func=open)
        
        subparser['compress'] = subparsers.add_parser('compress', help='compress audio files into archive')
        subparser['compress'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['compress'].set_defaults(func=compress)
        
        subparser['decompress'] = subparsers.add_parser('decompress', help='decompress audio files from archive')
        subparser['decompress'].add_argument(dest="projects", help="path(s) to folder(s) with audio project [default: %(default)s]", metavar="project", nargs='+')
        subparser['decompress'].set_defaults(func=decompress)

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
        #sys.argv.append("-h")
        #sys.argv.append("-v")
#        sys.argv.append("-r")
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
    sys.exit(main())