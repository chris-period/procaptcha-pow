# from tls_client import Session
import asyncio
from rnet import Client, Emulation, Proxy
from polka import Polka
from hashlib import sha256
from gen_token import generate_token, generate_html_hash
from gen_solution import encode_solution


requests = Client(emulation=Emulation.Chrome143, http2_only=True, verify=False, orig_headers=[
    "content-length",
    "pragma",
    "cache-control",
    "sec-ch-ua-platform",
    "sec-ch-ua",
    "sec-ch-ua-mobile",
    "prosopo-site-key",
    "prosopo-user",
    "dnt",
    "content-type",
    "user-agent",
    "accept",
    "origin",
    "sec-fetch-site",
    "sec-fetch-mode",
    "sec-fetch-dest",
    "referer",
    "accept-encoding",
    "accept-language",
    "priority",
],)


class Pow:
    @staticmethod
    def digestToHex(c):
        return "".join([format(b, "02x") for b in c])

    @staticmethod
    def checkPrefix(challenge: str, difficulty: int) -> int:
        s = 0
        d = "0" * difficulty
        while True:
            n = (str(s) + challenge).encode("utf-8")
            if Pow.digestToHex(sha256(n).digest()).startswith(d):
                return s
            s += 1


class Prosopo:
    def __init__(self, site_key: str, user_key: str):
        self.site_key = site_key
        self.user_key = user_key
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        self.base_url = "https://pronode2.prosopo.io/v1/prosopo"

        self.default_headers = {
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'prosopo-site-key': self.site_key,
            'prosopo-user': self.user_key,
            'dnt': '1',
            'content-type': 'application/json',
            'user-agent': self.user_agent,
            'accept': '*/*',
            'origin': 'https://www.twickets.live',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.twickets.live/',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'priority': 'u=1, i',
            'accept-language': 'en-US,en;q=0.9',
        }

    async def get_session_id(self):
        response = await requests.post(
            url=f"{self.base_url}/provider/client/captcha/frictionless",
            headers=self.default_headers,
            proxy=Proxy.all(url="http://127.0.0.1:8888"),
            json={
                "token": generate_token(self.user_key, self.user_agent),
                "headHash": generate_html_hash('01011110111001111110011100110001110111001110111111100111001100010101100110100111111101110011000110111100100111001011110111001011'),
                "dapp": self.site_key,
                "user": self.user_key,
            },
        )

        resp_body = await response.json()

        if resp_body.get("captchaType") != "pow":
            raise Exception("bad captchaType received: ", resp_body)

        return resp_body.get("sessionId")

    async def get_challenge(self, session_id: str):
        response = await requests.post(
            url=f"{self.base_url}/provider/client/captcha/pow",
            json={
                "user": self.user_key,
                "dapp": self.site_key,
                "sessionId": session_id,
            },
        )

        resp_body = await response.json()

        if resp_body.get("status") != "ok":
            raise Exception("bad challenge received: ", resp_body)

        return resp_body

    async def submit_challenge(
        self, challenge_str: str, provider: str, signature: str, nonce: int
    ):
        response = await requests.post(
            url=f"{self.base_url}/provider/client/pow/solution",
            json={
                "challenge": challenge_str,
                "difficulty": 4,
                "signature": {
                    "user": {
                        "timestamp": "0x" + signature,
                    },
                    "provider": {"challenge": provider},
                },
                "user": self.user_key,
                "dapp": self.site_key,
                "nonce": nonce,
                "verifiedTimeout": 120000,
            },
        )

        print(await response.json())

    def create_captcha_solution(
        self,
        challenge_str: str,
        provider: str,
        signature: str,
        timestamp: str,
        nonce: int,
    ):

        return encode_solution(
            prosopo_url=f"https://{self.base_url.split('/')[2]}",
            site_key=self.site_key,
            user_key=self.user_key,
            challenge_str=challenge_str,
            provider=provider,
            signature=signature,
            timestamp=timestamp,
            nonce=nonce,
        )


async def main(site_key: str, visitor_id: str):
    signer = Polka(visitor_id)
    signer.create_account()
    signer.seed_phrase()
    signer.create_keypair()
    print(f"Your (ss58) address: {signer.address()}")

    captcha = Prosopo(
        site_key=site_key,
        user_key=signer.address(),
    )
    session_id = await captcha.get_session_id()
    challenge = await captcha.get_challenge(session_id)
    nonce = Pow.checkPrefix(challenge["challenge"], challenge["difficulty"])
    signature = signer.sign(challenge["timestamp"])

    await captcha.submit_challenge(
        challenge["challenge"],
        challenge["signature"]["provider"]["challenge"],
        signature,
        nonce,
    )

    solution = await captcha.create_captcha_solution(
        challenge["challenge"],
        challenge["signature"]["provider"]["challenge"],
        signature,
        challenge["timestamp"],
        nonce,
    )

    print(solution)


if __name__ == "__main__":
    asyncio.run(
        main("5EZVvsHMrKCFKp5NYNoTyDjTjetoVo1Z4UNNbTwJf1GfN6Xm", "visitor id"))
