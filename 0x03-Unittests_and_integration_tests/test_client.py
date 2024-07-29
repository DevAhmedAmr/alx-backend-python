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
        with patch.object(GithubOrgClient, "_public_repos_url") as public_repos_url:
            public_repos_url.return_value = f"https://api.github.com/orgs/{payload}"\
                ""

            self.assertEqual(
                f"https://api.github.com/orgs/{payload}",
                GithubOrgClient(payload)._public_repos_url()

            )
