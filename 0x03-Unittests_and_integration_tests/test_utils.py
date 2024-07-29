#!/usr/bin/env python3
"""A module for testing the utils module."""
from utils import access_nested_map
from unittest import TestCase
from parameterized import parameterized, parameterized_class
parameterized.expand


class TestAccessNestedMap(TestCase):
    """
    A test that accesses the nested dicts contained in a nested dict .
    """
    @parameterized.expand([({"a": 1}, ("a",), 1),
                           ({"a": {"b": {"c": 1}}}, ["a", "b", "c"], 1),
                           ({"a": {"b": 2}}, ("a", "b"), 2)
                           ]
                          )
    def test_access_nested_map(self, dictionary: dict, path, result):
        """
        Test if the value of a nested dictionary matches the result of the test .

        Args:
            dictionary (dict): dictionary to be tested
            path ([type]): path of the info
            result ([type]): expected result
        """
        self.assertAlmostEqual(result, access_nested_map(dictionary, path,))

    @parameterized.expand([({}, ("a",))])
    def test_access_nested_map_exception(self, dictionary, path):
        self.assertRaises(KeyError, access_nested_map, dictionary, path,)
