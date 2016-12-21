# -*- coding: utf-8 -*-

## \package getcmd
#  
#  Retrieves & defines paths to commands that this app uses

# MIT licensing
# See: LICENSE.txt


import os, sys
from subprocess     import PIPE
from subprocess     import Popen
from subprocess     import STDOUT


def GetCMD(cmdname):
    output, returncode = Popen((u'which', cmdname,), stdout=PIPE, stderr=STDOUT).communicate()
    
    # NOTE: Not sure why '\n' is appended from Popen command
    output = output.strip(u'\n')
    
    if sys.version_info.major < 3:
        output = unicode(output)
    
    if not returncode and os.access(output, os.X_OK):
        return output
    
    print(u'Failed to find command: {}'.format(cmdname))


def Execute(cmd):
    if isinstance(cmd, (unicode, str)):
        cmd = cmd.split(u' ')
    
    output, returncode = Popen(cmd, stdout=PIPE, stderr=STDOUT).communicate()
    
    output = output.strip(u'\n')
    
    if sys.version_info.major < 3:
        output = unicode(output)
    
    if not returncode:
        return output
    
    print(u'Error executing command: {}'.format(u' '.join(cmd)))
    return returncode
