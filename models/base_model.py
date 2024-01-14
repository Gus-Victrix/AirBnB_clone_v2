#!/usr/bin/python3
"""
BaseModel class for AirBnB clone project - part of the console.
This provides the basic functionality for all other classes.

Dependencies:
    uuid - generates unique id's for each instance
    datetime - provides date and time information
    models - module containing all classes
"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    Base Class for basic functionality for all classes.
    
    Attributes:
        id - unique id for each instance
        created_at - time instance was created
        updated_at - time instance was updated

    Methods:
        __init__ - instantiates a new model
        __str__ - returns a string representation of the instance
        save - updates updated_at with current time when instance is changed
        to_dict - converts instance into dict format
    """
    def __init__(self, *args, **kwargs):
        """
        Instantiates a new BaseModel.
        If kwargs are given, instance is set to values in kwargs.
        Otherwise, a new instance is created with new id and created_at time.
        
        Kwargs:
            id - unique id for each instance
            created_at - time instance was created
            updated_at - time instance was updated
        """
        current_time = datetime.now()  # Taking time-stamp for consistency.
        if len(kwargs) == 0:  # If no kwargs were passsed.
            from models import storage
            self.id = str(uuid4())
            self.created_at = current_time
            self.updated_at = current_time
            storage.new(self)
        else:
            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime(
                        kwargs['updated_at'],
                        '%Y-%m-%dT%H:%M:%S.%f')
            else:
                kwargs['updated_at'] = current_time

            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(
                        kwargs['created_at'],
                        '%Y-%m-%dT%H:%M:%S.%f')
            else:
                kwargs['created_at'] = current_time

            del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
