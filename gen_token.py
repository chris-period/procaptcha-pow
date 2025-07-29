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
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmEpX9Tqve86xUQcSCAX1
    2S2XsivOzZYLe7BwhlkyLrc9tNN7OqHg8SEQA0z7RCvJPSvB5gfd0G/VHtMzDVH/
    iNuaU3sz/4Vi4mVOG/dQ1C2R2AZYu581TCL2NFVZbNK79KhDjB9kXF6ufBsAU+W4
    Hz7myBFBWHS5FNGf1QGSBDAPL1zsSaEv9HqDggMx5BH+1ibiU06aNobUpT179uIe
    Uxf0yki3pNohIUQC8JChu4FgNYUZTBeZ1OYIV9bqzfZR3pQH7kssXlePH06d+dkb
    e4k7xwu95/R5Nal5d2uA8iLO5bczJac+2whEHs1u+mUWgxBWmJXi4t9iwUvghaSI
    KQIDAQAB
    -----END PUBLIC KEY-----
    """

    public_key = RSA.import_key(public_key_base64)

    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)

    encrypted = cipher.encrypt(plain_text.encode())

    return b64encode(encrypted).decode()


def generate_token():
    c = Ax(min(random.random() * 0.3, 1))
    return _encrypt_text(json.dumps(c))
