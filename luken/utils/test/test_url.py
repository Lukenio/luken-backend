from urllib import parse

from django.test import TestCase

from luken.utils.url import update_url_query_params


class UpdateURLQueryParamsTestCase(TestCase):

    def test_updates_url_with_given_url_params(self):
        url = "http://test.example.com/test/path/"
        query_params = {"test": "test-query-param-value"}

        url = update_url_query_params(url, **query_params)
        parsed = parse.urlparse(url)
        parsed_query_params = parse.parse_qs(parsed.query)

        for key, value in query_params.items():
            self.assertTrue(value in parsed_query_params[key])
