#!/usr/bin/python3

"""
Fabric script to generate a .tgz archive from the contents of the web_static.
"""

from fabric.api import local  # run commands locally
from datetime import datetime  # to get the current date and time


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static.
    format: web_static_<year><month><day><hour><minute><second>.tgz

    Returns:
        str: the archive path if the archive has been successfully generated.
        None: if the archive has not been generated.
    """
    local("mkdir -p versions")  # create the folder versions if not exists
    date = datetime.now().strftime("%Y%m%d%H%M%S")  # get current datetime
    file = "versions/web_static_{}.tgz".format(date)  # create the file name
    result = local("tar -cvzf {} web_static".format(file))  # create .tgz file
    if result.failed:  # if the creation of the archive has failed
        return None
    return file  # return the archive path
