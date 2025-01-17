#!/usr/bin/python3
"""
This module creates BaseModel class for AirBnB clone project.
This provides the basic functionality for all other classes.

Dependencies:
    uuid.uuid4 - generates unique id's for each instance
    datetime - provides date and time information
    storage - stores instances of classes
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer
import uuid  # For generating unique id's
from os import getenv  # For accessing environment variables
import models
import datetime
from datetime import datetime

storage_type = getenv("HBNB_TYPE_STORAGE")

Base = object

if storage_type == "db":  # Checking current storage-type settings
    Base = declarative_base()  # Creating base class for SQLAlchemy.


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
    if storage_type == "db":  # Setting up schema for sqlalchemy
        # Seting up id column
        id = Column(String(60), nullable=False, primary_key=True)
        # Setting up creation time column and updated time column
        current_time = datetime.utcnow
        created_at = Column(DateTime, default=current_time)
        updated_at = Column(DateTime, default=current_time)

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
            self.id = str(uuid.uuid4())  # Generating unique id.
            self.created_at = current_time
            self.updated_at = current_time
            storage.new(self)
        else:
            for key, value in kwargs.items():  # Iterating through kwargs.
                if key != '__class__':  # Ignoring class name.
                    setattr(self, key, value)
            if 'id' not in kwargs.keys():
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs.keys():
                self.created_at = current_time
            else:
                self.created_at = datetime.fromisoformat(self.created_at)
            if 'updated_at' not in kwargs.keys():
                self.updated_at = current_time
            else:
                self.updated_at = datetime.fromisoformat(self.updated_at)
        return

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
        storage.new(self)
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
