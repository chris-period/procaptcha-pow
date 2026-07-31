# pip install py-sr25519-bindings
# pip install py-bip39-bindings
# pip install mnemonic
# pip install scalecodec

import bip39
import sr25519
import mnemonic
import scalecodec
from hashlib import blake2b
from wordlist import words


class Polka:
    def __init__(self, visitor_id: str):
        self.visitor_id = visitor_id
        self.blake_digest = None
        self.mini_secret = None
        self.keypair = None
        self.pubkey = None
        self.mnemonic = mnemonic.Mnemonic(language="english", wordlist=words)

    def create_account(self):
        blake = blake2b(self.visitor_id.encode(), digest_size=16, key=bytes())
        self.blake_digest = blake.hexdigest().encode()

    def seed_phrase(self):
        seed = self.mnemonic.to_mnemonic(self.blake_digest)
        self.mini_secret = bip39.bip39_to_mini_secret(seed, "")

    def create_keypair(self):
        self.keypair = sr25519.pair_from_seed(self.mini_secret)
        self.pubkey = self.keypair[0].hex()

    def address(self):
        return scalecodec.ss58_encode(self.pubkey)

    # received from the challenge
    # ../provider/client/captcha/pow
    def sign(self, timestamp: str):
        signature = sr25519.sign(self.keypair, timestamp.encode())
        return signature.hex()
