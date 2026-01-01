import hashlib
import secrets
import time
import random
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from base64 import b64encode


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


def hash_user_agent(s: str) -> str:
    digest = hashlib.sha256(s.encode("utf-8")).hexdigest()
    return digest[:32]


def transform_float(f: float):
    e = 0.4294846358501722
    r = float(3)
    c = float(1)

    return e * f**2 + r * f + c


def generate_html_hash(contents: str):
    return _encrypt_text(contents)


def generate_token(user_addr: str, user_agent: str):
    rand_float = min(random.random() * 0.3, 1)
    user_agent_encrypt = hash_user_agent(user_agent)
    details = f'{user_addr}|{transform_float(rand_float)}|{user_agent_encrypt}|0|0'
    a = secrets.randbits(16) % 2001
    token = json.dumps(
        obj=[int(time.time()*1000), details, a],
        indent=None,
        separators=(",", ":")
    )
    return _encrypt_text(token)
