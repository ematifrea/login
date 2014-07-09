import hashlib
import random
from django.utils.encoding import smart_str


def get_hexdigest(salt, raw_in):
    raw_in, salt = smart_str(raw_in), smart_str(salt)
    return hashlib.md5(salt+raw_in).hexdigest()


def encrypt_input(raw_in):
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(salt, raw_in)
    return '%s$%s' % (salt, hsh)


def check_inputs(raw_in, enc_in):
    salt, hsh = enc_in.split('$')
    return hsh == get_hexdigest(salt, raw_in)