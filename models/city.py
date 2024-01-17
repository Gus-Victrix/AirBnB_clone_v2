#!/usr/bin/python3
"""
Module defines City class.
City inherits from BaseModel class and Base class.

Dependencies:
    sqlalchemy
    models/base_model.py
"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """
    Representation of City where the particular entry is located.
    It's a child of State class.
    Inherits from BaseModel and Base.

    Attributes:
        __tablename__ (str): Table name in MySQL database.
        name (sqlalchemy String): City name.
        state_id (sqlalchemy String): State id.
    """
    if storage_type == "db":  # If set storage type is db
        __tablename__ = "cities"  # Table name in MySQL database
        # Setting up schema for sqlalchemy
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        id = Column(String(60), primary_key=True)
        places = relationship("Place", backref="cities", cascade="delete")
        state = relationship('State', back_populates='cities')

    else:  # If set storage type is file
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a new City instance"""
        super().__init__(*args, **kwargs)
