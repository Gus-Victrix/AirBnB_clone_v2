#!/usr/bin/python3
"""This module defines the City class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """This class represents a city"""

    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
#    state = relationship("State", back_populates="cities", foreign_keys=[state_id])

    def __init__(self, *args, **kwargs):
        """Initialize a new City instance"""
        super().__init__(*args, **kwargs)
