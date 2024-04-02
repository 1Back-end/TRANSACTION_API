import re
import string
import random
from random import randint, choice

ALGORITHM = "HS256"


def generate_code(length=10):
    """Generate a random string of fixed length """

    end = random.choice([True, False])

    string_length = round(length / 3)
    letters = string.ascii_lowercase
    random_string = (''.join(choice(letters) for i in range(string_length))).upper()
    range_start = 10 ** ((length - string_length) - 1)
    range_end = (10 ** (length - string_length)) - 1
    random_number = randint(range_start, range_end)
    if not end:
        final_string = f"{random_string}{random_number}"
    else:
        final_string = f"{random_number}{random_string}"
    return final_string


