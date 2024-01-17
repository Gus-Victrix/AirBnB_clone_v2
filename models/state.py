#!/usr/bin/python3
"""
State module
"""
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

class State(BaseModel, Base):
    """
    Representation of the State in which a city is located.
    Parent table of City.
    """
    if storage_type == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")
    else:
        name = ""

        @property
        def cities(self):
            """
            Getter attribute in case of file storage.
            Returns the list of City instances with state_id equals to the
            current State.id
            """
            from models import storage  # Import here to avoid circular import
            from models.city import City
            cities = []  # List of City instances
            for city in storage.all(City).values():  # Loop through all cities
                if city.state_id == self.id:  # If city.state_id == State.id
                    cities.append(city)  # Add city to list
            return cities  # Return list of City instances
