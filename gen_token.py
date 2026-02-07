import hashlib
import secrets
import time
import random
import json
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def _encrypt_text(plain_text: str):
    public_key_b64 = (
        "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtHsKhnISsZXRQiA1qyJlsEdx"
        "7fZTBUgveXzXaEMZVD0j7Q6PugbLOammnl3XqFXQCz/yaKRrg9tkq+XCGHYOKfz7TyrUNd"
        "JH84fzjMqW0rMgAGNaRcwU3BaPEnHJxUYwGu3YhybnCJOMy6V2E37ttezSDGRubC1E2Fpd"
        "LjdM1T+60+l2WyBC9Fb3zPtGO2pDTqmV7dRUuvSHrqMeS9yUzoMmBX6TZygIJ6lGtmOOGq"
        "bnzl70fxks31+32oailU3WnpbqavvrvN23DBsW6m+Cw51+NjDE5YGuHUfwTZb0ym8GnhmF"
        "3wANc73BQW6ibQiTAKVH1oaRHj2itYMX8YCbYQIDAQAB"
    )

    rsa_key = RSA.import_key(base64.b64decode(public_key_b64))

    aes_key = get_random_bytes(32)

    cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce=get_random_bytes(12))
    ciphertext, tag = cipher_aes.encrypt_and_digest(plain_text.encode("utf-8"))

    encrypted_data = ciphertext + tag

    cipher_rsa = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA256)
    encrypted_key = cipher_rsa.encrypt(aes_key)

    return json.dumps(
        {
            "key": base64.b64encode(encrypted_key).decode("ascii"),
            "data": base64.b64encode(encrypted_data).decode("ascii"),
            "iv": base64.b64encode(cipher_aes.nonce).decode("ascii"),
        }
    )


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
    details = f"{user_addr}|{transform_float(rand_float)}|{user_agent_encrypt}|0|0"
    a = secrets.randbits(16) % 2001
    token = json.dumps(
        obj=[int(time.time() * 1000), details, a], indent=None, separators=(",", ":")
    )
    print("token:", token)
    return _encrypt_text(token)
