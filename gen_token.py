import time
import math
import random
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from base64 import b64encode


def Ax(a):
    curr_time = int(time.time() * 1000)
    pie = (curr_time % 1000 + a) / 999 * math.pi
    pie -= math.pi / 2
    return (curr_time, math.sin(pie) * 1000)


def _encrypt_text(plain_text: str):
    public_key_base64 = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtZnLYfVDeDrxEFF/Vwon
    +tOjfUotjblyWyANYz7ZlM2wtkIiBehq/vY6dbrmOCH9Sy+tU3nfOgyS1aNZ0c9G
    0ECmLD1LjyIWFzSi/GyRrA85HP6C0CVWNJPwhP9uhIpuotuYLczv5aGYGgqzLshZ
    BsI6W/gj45KyWxFBPmLRYjwlGMUSJ077UuC1pqzoEfngKT5pRCdw7S7AICU6jtck
    2bj4UaZQHKnzfwo8n7yY2JEv+PWW4vUuPevZoTVZF/qozMoHIpOzqgZQzw679fKZ
    53YepkEkRPwT4xLSBN5LvUUDE2mtnjfgMBS3qd8jBeetKu5YZ89tzYyl+BFzTtZe
    XwIDAQAB
    -----END PUBLIC KEY-----
    """

    public_key = RSA.import_key(public_key_base64)

    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)

    encrypted = cipher.encrypt(plain_text.encode())

    return b64encode(encrypted).decode()


def generate_token():
    c = Ax(min(random.random() * 0.3, 1))
    return _encrypt_text(json.dumps(c))
