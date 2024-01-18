#!/usr/bin/python3.8
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
from os import getenv

storageType = getenv("HBNB_TYPE_STORAGE")


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        if storageType == "db":
            self.assertEqual(new.state_id, None)
        else:
            self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        if storageType == "db":
            self.assertEqual(new.name, None)
        else:
            self.assertEqual(type(new.name), str)
