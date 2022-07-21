# Packages
from vcr_unittest import VCRTestCase

# Local
from webapp.app import app


class TestEngagePages(VCRTestCase):
    def _get_vcr_kwargs(self):
        """
        This removes the authorization header
        from VCR so we don't record auth parameters
        """
        return {
            "filter_headers": ["Api-key", "Api-username"],
        }

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        return super().setUp()

    def test_engage_pages_index(self):
        """
        Given /engage page,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/engage").status_code, 200)

    def test_takeover_index(self):
        """
        Given /takeovers page,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/takeovers").status_code, 200)

    def test_robotics_whitepaper(self):
        """
        When given the engage robotics_whitepaper URL,
        we should return a 200 status code
        """

        self.assertEqual(
            self.client.get("/engage/robotics_whitepaper").status_code, 200
        )
