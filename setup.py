#!/usr/bin/env python
# -*- coding: utf-8 -*-

## \package setup

# MIT licensing
# See: docs/LICENSE.txt


import codecs, os, shutil, sys
from setuptools import setup


class Path:
    def __init__(self, path, stat):
        self.Path = path
        self.UID = stat.st_uid
        self.GID = stat.st_gid
    
    def _chown_path(self, path):
        return os.chown(path, PATH_root.UID, PATH_root.GID)
    
    def ChangeOwner(self):
        # FIXME: Recursive
        if os.path.isdir(self.Path) and self.UID != PATH_root.UID:
            for ROOT, DIRS, FILES in os.walk(self.Path):
                for D in DIRS:
                    self._chown_path(os.path.join(ROOT, D))
                
                for F in FILES:
                    self._chown_path(os.path.join(ROOT, F))
        
        self._chown_path(self.Path)
        
        self.UID = PATH_root.UID
        self.GID = PATH_root.GID
        
        stat = os.stat(self.Path)
        
        return stat.st_uid == self.UID == PATH_root.UID and stat.st_gid == self.GID == PATH_root.GID


PATH_root = os.path.dirname(os.path.realpath(__file__))
PATH_root = Path(PATH_root, os.stat(PATH_root))

FILE_cfg = os.path.join(PATH_root.Path, 'getcmd.cfg')

list_types = ('scripts', 'py_modules', 'docs',)

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def Read(fname):
    FILE_BUFFER = codecs.open(os.path.join(PATH_root.Path, fname), 'r', encoding='utf-8')
    file_data = FILE_BUFFER.read().strip(' \t\n\r')
    FILE_BUFFER.close()
    
    return file_data


def ReadConfig(key, key_type='str'):
    global FILE_cfg
    
    if not os.path.isfile(FILE_cfg):
        print('Error: Cannot find configuration file: {}'.format(FILE_cfg))
        sys.exit(1)
    
    FILE_BUFFER = codecs.open(FILE_cfg, 'r', encoding='utf-8')
    cfg_data = FILE_BUFFER.read().strip(' \t\n\r')
    FILE_BUFFER.close()
    
    err_no_key = 'Error: Could not find "{}" in configuration file'.format(key)
    
    if not key in cfg_data:
        print(err_no_key)
        sys.exit(1)
    
    cfg_data = cfg_data.split('\n')
    
    for LI in cfg_data:
        if LI.replace(' ', '').startswith('{}='.format(key)):
            value = LI[LI.index('=')+1:].strip(' \t')
            
            if value.startswith('file:'):
                return Read(value[value.index(':')+1:].strip(' \t'))
            
            if key_type == 'list' or key in list_types or ',' in value:
                return tuple(value.strip(', \t').replace(' ', '').split(','))
            
            if key_type == 'str':
                return value.strip(' \t')
    
    print(err_no_key)
    sys.exit(1)


APP_name = ReadConfig('name')

# Automatically generate an install.log file
arg_install = 'install'
install_log = '{}.log'.format(arg_install)
if arg_install in sys.argv:
    arg_i_index = sys.argv.index(arg_install)
    sys.argv.insert(arg_i_index+1, '--record')
    sys.argv.insert(arg_i_index+2, install_log)

# File & directories created by setuptools
setup_objects = ['build', '{}.egg-info'.format(APP_name), install_log,]

clean = 'clean' in sys.argv
distclean = 'distclean' in sys.argv

if clean or distclean:
    if distclean:
        setup_objects.append('dist')
    
    for O in setup_objects:
        O = os.path.join(PATH_root.Path, O)
        if os.path.isfile(O):
            os.remove(O)
            continue
        
        if os.path.isdir(O):
            shutil.rmtree(O)
    
    # Avoid 'invalid command' message
    if distclean:
        sys.exit(0)


def RunSetup():
    global Read, ReadConfig, APP_name
    
    setup(
        name = APP_name,
        version = ReadConfig('version'),
        author = ReadConfig('author'),
        author_email = ReadConfig('author_email'),
        description = ReadConfig('description'),
        long_description = ReadConfig('long_description'),
        license = ReadConfig('license'),
        url = ReadConfig('url'),
        py_modules = ReadConfig('py_modules'),
        keywords = ReadConfig('keywords'),
        classifiers = [
            'License :: OSI Approved :: MIT License',
            ],
        )


# Execute setuptools.setup under a function to execute code afterwards in script
exit_value = RunSetup()

# Change permissions on files & directories so current user can easily delete
for O in setup_objects:
    O = os.path.join(PATH_root.Path, O)
    if os.path.exists(O):
        O = Path(O, os.stat(O))
        O.ChangeOwner()


sys.exit(exit_value)
