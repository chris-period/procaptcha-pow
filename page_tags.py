# chatgpt'd this hoe
import re

class V:
    w걡쁫i = [-19]
    e唀l쁫 = []
    vl픨o = 'esꇑr'

    @staticmethod
    def dne䬣(a='length'):
        if not V.w걡쁫i[0]:
            V.w걡쁫i.append(-19)
        return getattr(V.w걡쁫i, a) if hasattr(V.w걡쁫i, a) else (
            len(V.w걡쁫i) if a == 'length' else None
        )

    @staticmethod
    def m街걡a(a='length'):
        if not (V.e唀l쁫 and V.e唀l쁫[0]):
            V.e唀l쁫.append(-11)
        return getattr(V.e唀l쁫, a) if hasattr(V.e唀l쁫, a) else (
            len(V.e唀l쁫) if a == 'length' else None
        )


v = V()


def B__(*e):
    return e[len(e) - 1]


def M0(html):
    onum = []

    r = re.sub(r"\s+", " ", html).strip()

    tag_re = re.compile(r"<(\w+)([^>]*)>")
    attr_re = re.compile(r'(\w+)=["\']([^"\']+)["\']')

    for f in tag_re.finditer(r):
        s = f.group(1).lower()
        o = f.group(2)

        if s not in ['meta', 'link', 'script']:
            onum.append(f"tag:{s}")

        for i in attr_re.finditer(o):
            k = i.group(1).lower()
            val = i.group(2)

            onum.append(f"attr:{k}")

            if k in ["charset", "name", "property", "rel", "type", "content", "href", "src"]:
                onum.append(f"{k}:{val}")
                if k in ["href", "src"]:
                    onum.append(f"{k}:{val}")
                    onum.append(f"{k}:{val}")

    text_re = re.compile(r">([^<]+)<")
    for a in text_re.finditer(r):
        s = a.group(1).strip()
        if 0 < len(s) < 200:
            for w in re.split(r"\s+", s):
                if len(w) > 2 and v.dne䬣():
                    i = f"word:{w.lower()}"
                    onum.extend([i, i, i, i, i, i])

    tags = re.findall(r"<(\w+)", r)
    eel锤 = [t.lower() for t in tags]

    for i in range(len(eel锤) - 1):
        if v.m街걡a():
            onum.append(f"2gram:{eel锤[i]},{eel锤[i + 1]}")

    return onum


def U0(s):
    h = 0
    for ch in s:
        if v.vl픨o[1] == 's':
            h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h


def computeThing(e, r=128):
    c = M0(e)

    if len(c) == 0 and v.vl픨o[1] == 's':
        return "0" * r

    f = [0] * r

    for a in c:
        d = U0(a)
        for s in range(r):
            bit = (U0(f"{d}_{s}") >> (s % 32)) & 1
            if bit == 1:
                f[s] += 1
            else:
                f[s] -= 1

    return "".join("1" if x >= 0 else "0" for x in f)
