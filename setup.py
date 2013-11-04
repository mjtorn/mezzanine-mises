# vim: fileencoding=utf-8

from setuptools import setup, find_packages

from subprocess import Popen, PIPE

import glob

import os
import sys

NAME = 'mezzamises'
AUTHOR = 'Markus Törnqvist'
AUTHOR_EMAIL = 'mjt@mises.fi'
URL = 'http://mises.fi/'

def get_virtualenv_name():
    venv_path = os.environ['VIRTUAL_ENV']
    base, venv_name = os.path.split(venv_path)

    return venv_name

def is_production():
    return get_virtualenv_name == 'production'

def get_egg_version():
    dirname = os.path.dirname(__file__)
    dir = os.path.split(dirname)[1]

    egg_dir = '%s.egg-info' % dir
    egg_path = os.path.join(dirname, egg_dir)

    pkg_info = os.path.join(egg_path, 'PKG-INFO')

    with open(pkg_info, 'r') as pkg_info_f:
        for line in pkg_info_f.readlines():
            split_line = line.split(': ')
            if split_line[0] == 'Version':
                return split_line[1].strip()

    raise ValueError('No version found')

def get_version():
    p = Popen(['git', 'ls-remote', '.'], stdout=PIPE, stderr=PIPE)
    stderr = p.stderr.read()
    stdout = p.stdout.readlines()

    if stderr:
#        print stderr
        try:
            ## Assume we are an egg
            return get_egg_version()
        except Exception, e:
            print e
            sys.exit(1)

    head = None
    tag = None
    for line in stdout:
        hash, name = line.split()
        if name == 'HEAD':
            head = hash

        if head and hash == head and '/tags' in name:
            tag = name.rsplit('/', 1)[-1]
            tag = '.'.join(tag.split('.')[:-1])

    if not tag:
        if not is_production():
            return hash

        print 'tag not found'
        #sys.exit(1)
        return hash

    return tag

setup(
    name = NAME,
    version = get_version(),
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    packages = find_packages(), # Because only modules can be excluded
    scripts = glob.glob('bin/*') or None,
#    package_data = package_data, # MANIFEST.in where available
    include_package_data = True,
    long_description = '%s.' % NAME,
)

# EOF

