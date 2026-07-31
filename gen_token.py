import hashlib
import math
import secrets
import time
import random
import json
import base64
from behaviorData import generate_mouse_data

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def _encrypt_text(plain_text: str):
    public_key_b64 = (
        "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6H8lw79+zANM3BGqMFgN"
        "L7ZaBpOVJAC+8UTpbmrX5+xA7fgGjiDfnO5wKfxUfxMDTA0bvO7MDI0V1l6zOGQO"
        "YDi4FDy+4FZO+UPVz7rJ85ecJTkAW3E3ZImnOFlN2ZBuOuZobAbMIRyCcXDmXRgI"
        "HGGX2nEgcx53oPKv/rQkiCbaHOjycBP1KofSZ/7JaZdBxoSGEuozQefEeE3YfiOx"
        "0M0rOXEXICOCG3xLvFy5gPlKSioPIEYhqHASF9CtU4RasrhFCUbCThaz+Bh8m+ZP"
        "LJ7LIpbK9iOZb4tzsldY0LZ+z5VW+ESKtB4fkbIb1Aemkb/Ta3uKTHsC3qgrWR1/"
        "GQIDAQAB"
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


def generate_behavior_data() -> str:
    data = generate_mouse_data(3, x_range=(500, 800), y_range=(300, 400))

    return _encrypt_text(json.dumps(data))


def generate_salt() -> str:
    def hash_hex(r, t):
        e = list(r.removeprefix("0x"))
        n, s = 2, len(e) - 1

        # Number of values
        e[:2] = f"{len(t):02x}"

        pos = []
        size = []
        used = 0

        # Write values at the end
        for x in t:
            h = f"{x:x}"
            d = s - len(h) + 1
            e[d : d + len(h)] = h
            pos.append(d)
            size.append(len(h))
            s -= len(h)
            used += len(h)

        # metadata
        for p, l in zip(pos, size):
            used += 4
            if used > len(e):
                raise ValueError("Hex data exceeds string length")
            e[n : n + 4] = f"{p:02x}{l:02x}"
            n += 4

        return "0x" + "".join(e)

    # 891 = x position where clicked on box for procaptcha
    # 616 = y position where clicked on box for procaptcha
    # window mouse down event
    return hash_hex(secrets.token_hex(14), [891, 616])


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
    details = (
        f"{user_addr}|{transform_float(rand_float)}|{user_agent_encrypt}|0|0|0000000000"
    )

    a = secrets.randbits(16) % 2001
    token = json.dumps(
        [int(time.time() * 1000), details, a],
        indent=None,
        separators=(",", ":"),
    )

    return _encrypt_text(token)
