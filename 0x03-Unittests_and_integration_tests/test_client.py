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
from unittest.mock import patch, PropertyMock, Mock
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

        def test_has_license(self, repo: Dict, key: str,
                             expected: bool) -> None:
            """Tests the `has_license` method."""
            gh_org_client = GithubOrgClient("google")
            client_has_licence = gh_org_client.has_license(repo, key)
            self.assertEqual(client_has_licence, expected)
######################################


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Args:
            unittest (_type_): _description_
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Returns:
                _type_: _description_
        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """
        Test public repos
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """
        Test public repos with licence
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        teardown class
        """
        cls.get_patcher.stop()
