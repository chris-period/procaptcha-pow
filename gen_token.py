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
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyGWbPYHCppJ2rtB1FMI1
    4kx0QwXAf96U5yIeNCPHmXcL7wrZ1TxejINR7Q7gsEzphWqQCpKhpvhdukofdKPA
    IoUAcYUZ4AK4lTzBn7KRo/KNszcB+8fceNk17eVUiR+yM2Qw60v1hIwj6kKMWaXl
    e4mvtDEVr6uZsaiMRNE8mo9Ojjf2On7gMP8FBCv7C8L7scsRHlq0CgSugdL3vtm7
    aT0HYq1mhVYQXKs+TGsEtwrGSORimYnzMIR8BDxIFsL+H6DaC0SXtPfH2RBw5/mL
    3U9t05k0xjDeQ0BvDuto1EdmAFFEPNExlCy7JbgkrNEMIfQtP/ytgazd+4UidQO/
    EwIDAQAB
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