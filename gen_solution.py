from typing import Optional


def encode_compact_int(n: int) -> bytes:
    if n < (1 << 6):
        return ((n << 2) | 0).to_bytes(1, "little")
    elif n < (1 << 14):
        return ((n << 2) | 1).to_bytes(2, "little")
    elif n < (1 << 30):
        return ((n << 2) | 2).to_bytes(4, "little")
    else:
        b = n.to_bytes((n.bit_length() + 7) // 8, "little")
        length = len(b)
        prefix = ((length - 4) << 2) | 3
        return bytes([prefix]) + b


def encode_str(s: str) -> bytes:
    s_bytes = s.encode("utf-8")
    return encode_compact_int(len(s_bytes)) + s_bytes


def encode_u32(n: int) -> bytes:
    if n < 0 or n >= (1 << 32):
        raise ValueError("Value out of range for u32")
    return n.to_bytes(4, "little")


def encode_option_str(value: Optional[str]) -> bytes:
    if value is None:
        return b"\x00"
    else:
        return b"\x01" + encode_str(value)


def encode_option_u32(value: Optional[int]) -> bytes:
    if value is None:
        return b"\x00"
    else:
        return b"\x01" + encode_u32(value)


def encode_solution(
    prosopo_url: str,
    site_key: str,
    user_key: str,
    challenge_str: str,
    provider: str,
    signature: str,
    timestamp: str,
    nonce: int,
    commitment_id: int = None,
    provider_request_hash: str = None,
    user_request_hash: str = None,
) -> str:

    encoded = b""
    encoded += encode_option_str(commitment_id)
    encoded += encode_option_str(prosopo_url)
    encoded += encode_str(site_key)
    encoded += encode_str(user_key)
    encoded += encode_option_str(challenge_str)
    encoded += encode_option_u32(nonce)
    encoded += encode_str(timestamp)

    sig_encoded = b""
    sig_encoded += encode_option_str(provider)
    sig_encoded += encode_option_str(provider_request_hash)
    sig_encoded += encode_option_str(signature)
    sig_encoded += encode_option_str(user_request_hash)

    encoded += sig_encoded

    return "0x" + encoded.hex()


if __name__ == "__main__":

    encoded_hex = encode_solution(
        prosopo_url="https://pronode11.prosopo.io",
        site_key="5EZVvsHMrKCFKp5NYNoTyDjTjetoVo1Z4UNNbTwJf1GfN6Xm",
        user_key="user key",
        challenge_str="challenge string",
        provider="provider challenge",
        signature="timestamp signature",
        timestamp="epoch",
        nonce=1,
    )

    print(encoded_hex)
