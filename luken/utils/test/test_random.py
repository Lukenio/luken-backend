from django.test import TestCase

from luken.utils.random import generate_random_string


class GenerateRandomStringTestCase(TestCase):

    def test_generated_string_has_requested_length(self):
        test_length = 10
        generated_string = generate_random_string(test_length)
        self.assertEqual(len(generated_string), test_length)
