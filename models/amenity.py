#!/usr/bin/python3
"""
Module defines the Amenity class which inherits from BaseModel and Base.

Classes:
    Amenity: Defines amenities that may be available at a place.

Dependencies:
    BaseModel: Parent class.
    Base: Instance of declarative_base.
    storage_type: The type of storage.
    Column: An instance of SQLAlchemy Column.
    String: An instance of SQLAlchemy String.
    relationship: An instance of SQLAlchemy relationship.
"""
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    Defines amenities that may be available at a place.
    Has a many to many relationship with the Place class.

    Attributes:
        name (str): The name of the amenity.
        __tablename__ (str): The name of the table in the database.
        place_amenities (Place): The relationship between the amenity and
            the place.
    """
    if storage_type == "db":  # In the case that the storage type is a database
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity",
                                       back_populates="amenities")
    else:  # In the case that the storage type is a JSON file
        name = ""
