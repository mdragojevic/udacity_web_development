import hmac
import hashlib
import random
import string
SECRET = "I'm not secret at all"

def generate_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def encode(val):
    salt = generate_salt()
    return hmac.new(SECRET, val).hexdigest()

def hash_passw(passw, salt=None):
    if not salt:
        salt = generate_salt()
    return "%s,%s" % (hashlib.sha256(passw+salt).hexdigest(), salt)

def validate(val, coded_val):
    return encode(val) == coded_val

def validate_passw(passw, coded_val):
    coded, salt = coded_val.split(",")
    return hash_passw(passw, salt) == coded_val