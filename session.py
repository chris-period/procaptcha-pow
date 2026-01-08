from page_tags import computeThing
from tls_client import Session
from polka import Polka
from hashlib import sha256
from gen_token import generate_token, generate_html_hash
from gen_solution import encode_solution


requests = Session(client_identifier="chrome_120",
                   random_tls_extension_order=True)


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
    def __init__(self, page_url: str, site_key: str, user_key: str):
        self.page_url = page_url
        self.site_key = site_key
        self.user_key = user_key
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        self.base_url = "https://pronode7.prosopo.io/v1/prosopo"
        self.page_binary = None

        self.headers = {
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

    def page_contents(self):
        response = requests.get(
            self.page_url,
            headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'dnt': '1',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'referer': 'https://www.twickets.live/',
                'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',

            }
        )

        if response.status_code != 200:
            raise Exception("bad response code from \"page_contents\"")

        self.page_binary = computeThing(response.text)

    def get_session_id(self):
        head_hash = generate_html_hash(self.page_binary)

        json_data = {
            'token': generate_token(self.user_key, self.user_agent),
            'headHash': head_hash,
            'dapp': self.site_key,
            'user': self.user_key,
        }

        response = requests.post(
            url=f"{self.base_url}/provider/client/captcha/frictionless",
            headers=self.headers,
            json=json_data,
        )

        resp_body = response.json()

        if resp_body.get("captchaType") != "pow":
            raise Exception("bad captchaType received: ", resp_body)

        return resp_body.get("sessionId")

    def get_challenge(self, session_id: str):
        response = requests.post(
            url=f"{self.base_url}/provider/client/captcha/pow",
            headers=self.headers,
            json={
                "dapp": self.site_key,
                "sessionId": session_id,
                "user": self.user_key,
            },
        )

        resp_body = response.json()

        if resp_body.get("status") != "ok":
            raise Exception("bad challenge received: ", resp_body)

        return resp_body

    def submit_challenge(
        self, challenge_str: str, provider: str, signature: str, nonce: int
    ):
        response = requests.post(
            url=f"{self.base_url}/provider/client/pow/solution",
            headers=self.headers,
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

        print(response.json())

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


def main(page_url: str, site_key: str, visitor_id: str):
    signer = Polka(visitor_id)
    signer.create_account()
    signer.seed_phrase()
    signer.create_keypair()
    print(f"Your (ss58) address: {signer.address()}")

    captcha = Prosopo(
        site_key=site_key,
        user_key=signer.address(),
        page_url=page_url,
    )
    captcha.page_contents()

    session_id = captcha.get_session_id()
    challenge = captcha.get_challenge(session_id)
    print('challenge:', challenge)
    nonce = Pow.checkPrefix(challenge["challenge"], challenge["difficulty"])
    signature = signer.sign(challenge["timestamp"])

    captcha.submit_challenge(
        challenge["challenge"],
        challenge["signature"]["provider"]["challenge"],
        signature,
        nonce,
    )

    solution = captcha.create_captcha_solution(
        challenge["challenge"],
        challenge["signature"]["provider"]["challenge"],
        signature,
        challenge["timestamp"],
        nonce,
    )

    print(solution)


if __name__ == "__main__":
    site_url = 'https://www.twickets.live/app/block/640070387854481,2'
    site_key = '5EZVvsHMrKCFKp5NYNoTyDjTjetoVo1Z4UNNbTwJf1GfN6Xm'
    # visitor_id = 'visitor id'
    visitor_id = '1'*20
    main(site_url, site_key, visitor_id)
