#!/usr/bin/python3
"""
This module creates BaseModel class for AirBnB clone project.
This provides the basic functionality for all other classes.

Dependencies:
    uuid4 - generates unique id's for each instance
    datetime - provides date and time information
    storage - stores instances of classes
"""
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
            self.id = str(uuid4())  # Generating unique id.
            self.created_at = current_time
            self.updated_at = current_time
            storage.new(self)
        else:
            for key, value in kwargs.items():  # Iterating through kwargs.
                if key != '__class__':  # Ignoring class name.
                    # Setting anything that isn't a datetime object.
                    if key != 'created_at' and key != 'updated_at':
                        setattr(self, key, value)
                    else:  # Setting datetime objects.
                        setattr(self, key, datetime.fromisoformat(value))

    def __str__(self):
        """
        Creates an unofficial string representation of instance.
        Format:
            [<class name>] (<self.id>) <self.__dict__>

        Returns:
            Unofficial string representation of instance.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates updated_at with current time when instance is changed.
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Converts instance into dict format.
        Format: {
            '__class__': <class name>
            'created_at': <self.created_at.isoformat()>
            'updated_at': <self.updated_at.isoformat()>
            }

        Returns:
            Dictionary representation of instance.
        """
        dictionary = self.__dict__.copy()  # Copying to avoid overwriting.
        # Converting datetime objects to isoformat.
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        dictionary['__class__'] = self.__class__.__name__  # Adding class name.
        return dictionary
