import string
import random


def generate_random_string(length=30):
    """
    Generates random string of given length.

    :param length: length of generated string
    :return: random string containing ASCII letters (both uppercase and lowercase)
    and digits
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(random.SystemRandom().choice(alphabet) for _ in range(length))
