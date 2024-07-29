#!/usr/bin/env python3
"""A module for testing the client module.
"""
import unittest
from typing import Dict

from parameterized import parameterized, parameterized_class
from requests import HTTPError
from unittest.mock import patch, PropertyMock, Mock

from client import (
    GithubOrgClient
)
from fixtures import TEST_PAYLOAD
from unittest.mock import patch


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
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            payload = {"repos_url": "World"}
            mock.return_value = payload
            test_class = GithubOrgClient('test')
            result = test_class._public_repos_url
            self.assertEqual(result, payload["repos_url"])
