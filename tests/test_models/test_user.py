#!/usr/bin/python3.8
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User
from os import getenv

storageType = getenv("HBNB_TYPE_STORAGE")


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        if storageType == "db":
            self.assertEqual(new.first_name, None)
        else:
            self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.value()
        if storageType == "db":
            self.assertEqual(new.last_name, None)
        else:
            self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        new = self.value()
        if storageType == "db":
            self.assertEqual(new.email, None)
        else:
            self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        new = self.value()
        if storageType == "db":
            self.assertEqual(new.password, None)
        else:
            self.assertEqual(type(new.password), str)


if __name__ == "__main__":
    unittest.main()
