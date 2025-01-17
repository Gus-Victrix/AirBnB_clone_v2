#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If cls is not None, returns a dictionary of models of type cls

        Args:
            cls (str): The name of the class type to return

        Returns:
            A dictionary of models in storage
        """
        if cls:
            instances = {}
            for key, obj in self.__objects.items():
                if isinstance(obj, cls):
                    instances[key] = obj
            return instances
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = obj.to_dict()['__class__'] + '.' + obj.id
        self.all()[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {}
            temp.update(self.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objecst dictionary if it's inside.
        Args:
            obj (obj): object to delete
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            del self.__objects[key]
        return

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects"""
        self.reload()
