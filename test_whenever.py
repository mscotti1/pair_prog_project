import unittest
import datetime
from whenever_methods import get_date_str


class Test_whenever_weather(unittest.TestCase):

    def test_get_date_str(self):
        new_date = datetime.datetime(2023, 6, 5)
        self.assertEqual(get_date_str(new_date), "2023-06-05")


# python3 -m unittest test_whenever.py
