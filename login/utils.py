__author__ = 'blu'

import hashlib
import random

SALT = hashlib.md5(str(random.random())).hexdigest()[:5]


def hash_input(putin):
    return hashlib.md5(SALT+putin).hexdigest()


def verify_inputs(putin, input2):
    hashed_input = hash_input(putin)
    return hashed_input == input2

