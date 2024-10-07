import uuid
import os
from base64 import urlsafe_b64encode


def base64url_encode(payload):
    if not isinstance(payload, bytes):
        payload = payload.encode("utf-8")
    encode = urlsafe_b64encode(payload)
    return encode.decode("utf-8").rstrip("=")


def get_rand_hash(length=16):
    return uuid.uuid4().hex[:length]


def get_rand_oct(size=256):
    key = os.urandom(size // 8)
    return base64url_encode(key)
