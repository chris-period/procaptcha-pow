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
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxoLSRWT/eNMWOs9oiCnq
    Q8qQosbPpU0dwZpgBmv+kCFMbOdlyiaOcYfB9qLwTmMPXRW/C01kF8gw1AAjauZ4
    mzxSb/Q8Su1cWfO8/gVFW8N1mvduuri6Vodak3T6kejoODctiv85FU2NJKng0nNO
    WOCOLFD9qC2+sXzG3Vd6EyDtwcO9VmvdCin+jBODPg6WbBsvAfD8P1YfdrOg2L/v
    KJpOScr4wUqhz/Zu7869OzYp9AfQHFAcxSyDy6p3PnAH/ZaTZJ2fYo7IEE7qDd6A
    h/QQVcROBG0p9Lhm1NsLCmFtFIoyjGdY8EdTXwgSMrN69gdWpSrI/zcLV042t+5N
    EQIDAQAB
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
    print("token:", token)
    return _encrypt_text(token)
