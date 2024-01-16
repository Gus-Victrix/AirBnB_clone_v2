#!/usr/bin/python3
"""
Amenity class that inherits from BaseModel
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Defines amenities that may be available at a place.
    """
    name = ""
