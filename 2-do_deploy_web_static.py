#!/usr/bin/python3

"""
Create an .tgz archive with all the statoc content of
my AirBnB static clone
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['100.25.109.76', '34.207.63.26']


def do_deploy(archive_path):
    """
    Deplay all the static files in the nginx servers
    args:
        archive_path (str): String to the path of the archive
    """
    if exists(archive_path) is False:
        return False
    try:
        fileAndExent = archive_path.split('/')[-1]
        nameFile = fileAndExent.split('.')[0]
        path = '/data/web_static/releases'
        print(nameFile)

        put(archive_path, '/tmp/{}'.format(fileAndExent))
        run('rm -rf {}/{}'.format(path, nameFile))
        run('mkdir -p {}/{}'.format(path, nameFile))
        run('tar -xzf /tmp/{} -C {}/{}/'.format(fileAndExent, path, nameFile))
        run('mv {}/{}/web_static/* {}/{}'.format(
                                path, nameFile,
                                path, nameFile))
        run('rm /tmp/{}'.format(fileAndExent))
        run('rm /data/web_static/current')
        run('ln -sf {}/{} /data/web_static/current'.format(path, nameFile))

    except Exception:
        return False
