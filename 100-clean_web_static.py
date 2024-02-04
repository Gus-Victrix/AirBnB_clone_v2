#!/usr/bin/python3

"""
Clean all folder of the zip package
"""

import os
import pathlib
from fabric.api import *

env.hosts = ['34.207.63.26', '100.25.109.76']


def do_clean(number=0):
    """
    Clean files from zip package.
    Keep only n files where n is a numbers given
    in input
    Args:
        number (int): The number of file to keep
    """

    if int(number) == 0:
        number = 1
    else:
        number = int(number)

    with lcd("versions"):
        files = os.listdir("./versions")
        files.sort()
        for i in range(number):
            if len(files) == 0:
                break
            files.pop()
        for fileName in files:
            local('rm -rf ./{}'.format(fileName))

    with cd('/data/web_static/releases'):
        files = run('ls -lt').split()
        nameFiles = [nameF for nameF in files if "web_static" in nameF]
        nameFiles.sort()
        for i in range(number):
            if len(nameFiles) == 0:
                break
            nameFiles.pop()
        print(nameFiles)
        for fileName in nameFiles:
            run('rm -rf ./{}'.format(fileName))
