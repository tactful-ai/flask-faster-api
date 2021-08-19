# This is the unit test of the create_model function
# Author: Seif Ashraf

# Testing Methodology
# send return types example as a dict to the function to simulate the output of the annotations function
# let create_model() process input and get its output
# compare its output types with a sample model
# NOTE: typing.List needs comparing its type of fields.List with the create_model output type cuz idk why

from flask_fastx import *
from flask_fastx.model_api import create_model
import unittest
from utils import *


# the unit testing function

descriptions = dict()


class TestModel(unittest.TestCase):
    def test_one(self):
        self.assertEqual(ModelMatcher(
            create_model(input, descriptions)), model)


if __name__ == '__main__':

    unittest.main()
