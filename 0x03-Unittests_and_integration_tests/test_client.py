#!/usr/bin/env python3
"""A module for testing the client module.
"""
import unittest
from typing import Dict

from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import (
    GithubOrgClient
)
from fixtures import TEST_PAYLOAD
from unittest.mock import patch, PropertyMock
import utils


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""
    @parameterized.expand([("google",), ("abc",)])
    def test_org(self, org):
        with patch.object(GithubOrgClient, "org") as GithubOrgClient_org:
            GithubOrgClient_org.return_value = {
                'message': 'mock_message',
                'documentation_url': 'https://docs.github.com/rest/orgs/orgs#get-an-organization',
                'status': '200'}

            GithubOrgClient(org).org()
            GithubOrgClient_org.assert_called_once()

    @parameterized.expand([("google",), ("abc",)])
    def test_public_repos_url(self, payload):
        with patch.object(GithubOrgClient, "_public_repos_url") as public_repos_url:
            public_repos_url.return_value = f"https://api.github.com/orgs/{payload}"\
                ""

            self.assertEqual(
                f"https://api.github.com/orgs/{payload}",
                GithubOrgClient(payload)._public_repos_url()

            )
            public_repos_url.assert_called()

    @patch('client.get_json')
    def test_public_repos(self, get_json):
        get_json.return_value = [{"name": "Google"}, {"name": "Twitter"}]

        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as public_repos_url:
            public_repos_url.return_value = " https://hello/world.com"
            client = GithubOrgClient('test')
            result = client.public_repos()

            self.assertIsNotNone(client.public_repos())
            self.assertIsInstance(client.public_repos(), list)
            public_repos_url.assert_called()
            get_json.assert_called_once()
######################################


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Class for Integration test of fixtures """

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""

        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """ Integration test: public repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """ Integration test for public repos with License """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""
        cls.get_patcher.stop()
