#!/usr/bin/env python3
"""A module for testing the utils module."""
from utils import access_nested_map
from unittest import TestCase
from parameterized import parameterized, parameterized_class
parameterized.expand
from utils import get_json
import unittest.mock as mock
from utils import memoize


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
            path ([list]): path of the info
            result ([any]): expected result
        """
        self.assertAlmostEqual(result, access_nested_map(dictionary, path,))

    @parameterized.expand([({}, ("a",)),
                           (({"a": 1}, ("a", "b")))])
    def test_access_nested_map_exception(
            self, dictionary: dict, path: list) -> None:
        """Raises an exception if the key is not a nested_nested_map attribute .

        Args:
            dictionary (dict): dictionary to be tested
            path ([list]): path of the info
        """
        self.assertRaises(KeyError, access_nested_map, dictionary, path,)


class TestGetJson(TestCase):

    @parameterized.expand([("http://example.com", {"payload": True}),
                          ("http://holberton.io", {"payload": False})])
    def test_get_json(self, url, payload):
        """
        Assert the access token is called on the server .

        Args:
            url ([str])
            payload ([dict])
        """
        with mock.patch("utils.get_json") as mock_class:
            get_json = mock_class.return_value = payload

        # Define the TestClass inside the test method


class TestMemoize(TestCase):
    """Memoize test class
    """

    def test_memoize(self):
        """Test memoize method to ensure that when a_property method
         called twice is correctly tested by calling a_method once
        """

        class TestClass:
            """wrapper class for memoize method
            """

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with mock.patch.object(TestClass, 'a_method') as _mock:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            _mock.assert_called_once()
