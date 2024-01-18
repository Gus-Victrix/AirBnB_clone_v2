#!/usr/bin/python3.8
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from os import getenv

storageType = getenv("HBNB_TYPE_STORAGE")


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        if storageType == "db":
            self.assertEqual(new.name, None)
        else:
            self.assertEqual(type(new.name), str)
