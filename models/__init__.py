#!/usr/bin/python3
"""
Package initializer
"""

"""
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
"""
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':  # if storage type is database
    from models.engine.db_storage import DBStorage as Storage
else:
    from models.engine.file_storage import FileStorage as Storage

storage = Storage()  # instantiates storage object
storage.reload()
