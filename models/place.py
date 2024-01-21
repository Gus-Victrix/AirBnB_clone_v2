#!/usr/bin/python3
"""
Module dealing with Place class and its relationships.

Classes:
    Place: Representation of places in the storage.
Tables:
    place_amenity: Many to Many relationship between Place and Amenity.

Dependencies:
    MySQLdb: Database.
    SQLAlchemy: ORM.
    BaseModel: Base class for all models.
"""
from models.base_model import BaseModel, Base, storage_type
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models


if storage_type == "db":
    place_amenity = Table("place_amenity", Base.metadata,  # Many to Many
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """
    Representation of places in the storage.

    Attributes:
        city_id: City.id.
        user_id: User.id.
        name: Place name.
        description: Place description.
        number_rooms: Number of rooms.
        number_bathrooms: Number of bathrooms.
        max_guest: Maximum number of guests.
        price_by_night: Price by night.
        latitude: Latitude.
        longitude: Longitude.
        reviews: List of Review instances with place_id equals to the current
        Place.id.
        amenities: List of Amenity instances based on the attribute amenity_ids
        that contains all Amenity.id linked to the Place.

    Methods:
        __init__: Constructor.
        __str__: String representation of the Place instance.
    """
    if storage_type == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        id = Column(String(60), primary_key=True)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", cascade="all, delete",
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False, backref="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            Getter attribute in case of file storage.

            Returns:
                A list of Review objects with place_id equal to the current
                Place.id.
            """
            review_list = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """
            Getter attribute in case of file storage.

            Returns:
                A list of Amenity objects with place_id equal to the current
                Place.id.
            """
            amenity_list = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """
            Setter attribute in case of file storage.

            Args:
                obj: An Amenity object.
            """
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
