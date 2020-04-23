import unittest

from webapp import template_utils


class TemplateUtilsTest(unittest.TestCase):
    def test_truncate_chars(self):
        value = "123456789"
        length = 5
        expected_result = "1234&hellip;"

        result = template_utils.truncate_chars(value, length)
        self.assertEqual(expected_result, result)

        value = "1234 56789"
        length = 5
        expected_result = "1234&hellip;"

        result = template_utils.truncate_chars(value, length)
        self.assertEqual(expected_result, result)

    def test_format_date(self):
        date = "2020-12-12"
        expected_result = "12 December 2020"

        result = template_utils.format_date(date)
        self.assertEqual(expected_result, result)

    def test_replace_admin(self):
        url = "https://admin.insights.ubuntu.com/test-url/123"
        expected_result = "https://jp.ubuntu.com/blog/test-url/123"

        result = template_utils.replace_admin(url)
        self.assertEqual(expected_result, result)
