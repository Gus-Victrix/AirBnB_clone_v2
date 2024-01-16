#!/usr/bin/python3
"""
This module defines the FileStorage class.
It manages storage of hbnb models in JSON format and handles their restoration.

It's not meant to be used directly in this project, but rather through
instances of the Storage class defined in __init__.py.

Dependencies:
    * json module
    * BaseModel class defined in models/base_model.py
    * User class defined in models/user.py
    * Place class defined in models/place.py
    * State class defined in models/state.py
    * City class defined in models/city.py
    * Amenity class defined in models/amenity.py
    * Review class defined in models/review.py
"""
import json  # For serialization/deserialization
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    Manages storage and retrieval of hbnb models in JSON format.

    Attributes:
        __file_path (str): Path to the JSON file used for storage.
        __objects (dict): Dictionary of dictionaries containing all objects.

    Methods:
        all(self): Returns the dictionary __objects.
        new(self, obj): Sets in __objects the obj with key <obj class name>.id
        save(self): Serializes __objects to the JSON file (path: __file_path)
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """
        Return all currently stored objects in a dictionary.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Add a new object to the current database session.
        Format: <obj class name>.id : <object>
        """
        key = obj.to_dict()['__class__'] + '.' + obj.id
        self.all()[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {key: obj.to_dict() for key, obj in
                    FileStorage.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj:
            key = obj.to_dict()['__class__'] + '.' + obj.id
            FileStorage.__objects.pop(key, None)
