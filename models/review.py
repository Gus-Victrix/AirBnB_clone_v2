#!/usr/bin/python3
"""
Review module for the HBNB project
"""
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review classto store review information """
    if storage_type == "db":
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        id = Column(String(60), primary_key=True)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """Initialization of Review instance"""
        super().__init__(*args, **kwargs)
