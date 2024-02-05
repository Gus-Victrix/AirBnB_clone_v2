#!/usr/bin/python3

"""
Deploy all static hbnb into our 2 web servers.
"""

from fabric.api import put, run, env, local
from os.path import exists
import time

env.hosts = ['34.207.63.26', '100.25.109.76']


def do_pack():
    """
    Enpack all the static content of AirBnB clone
    """
    date = time.strftime("%Y%m%d%H%M%S")
    try:
        local('mkdir -p versions')
        local('tar -czvf versions/web_static_{}.tgz web_static'.format(date))
        return 'versions/web_static_{}.tgz'.format(date)
    except Exception:
        return None


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


def deploy():
    """
    Deploy all the web static
    Using do_pack to enpackage all the html and css static
    Using do_deploy to send and deploy file on the web site
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
