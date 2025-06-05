// reversing how to generate ("token") key for /frictionless endpoint\
const Ax = (a) => {
    const currTime = Date.now();
    let pie = Number(currTime.toString().slice(-3)) + a;
    pie /= 999 * Math.PI;
    pie -= Math.PI / 2
    return [currTime, Math.sin(pie) * 1000]
};

async function encryptPlainText(...e) {
    const publicKeyBytes = atob(`MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtZnLYfVDeDrxEFF/Vwon
+tOjfUotjblyWyANYz7ZlM2wtkIiBehq/vY6dbrmOCH9Sy+tU3nfOgyS1aNZ0c9G
0ECmLD1LjyIWFzSi/GyRrA85HP6C0CVWNJPwhP9uhIpuotuYLczv5aGYGgqzLshZ
BsI6W/gj45KyWxFBPmLRYjwlGMUSJ077UuC1pqzoEfngKT5pRCdw7S7AICU6jtck
2bj4UaZQHKnzfwo8n7yY2JEv+PWW4vUuPevZoTVZF/qozMoHIpOzqgZQzw679fKZ
53YepkEkRPwT4xLSBN5LvUUDE2mtnjfgMBS3qd8jBeetKu5YZ89tzYyl+BFzTtZe
XwIDAQAB`);

    const publicKey = new Uint8Array(294);

    for (let a = 0; a < 294; a++)
        publicKey[a] = publicKeyBytes.charCodeAt(a);

    const cryptoKey = await crypto.subtle.importKey('spki', publicKey, {
        'name': 'RSA-OAEP',
        'hash': 'SHA-256'
    }, true, ['encrypt']);

    const cryptoText = await crypto.subtle.encrypt(
        { name: "RSA-OAEP" },
        cryptoKey,
        new TextEncoder().encode(e[0])
    );

    return btoa(String.fromCharCode(...new Uint8Array(cryptoText)));
}

const token = await encryptPlainText(
    JSON.stringify(
        Ax(Math.min(Math.random() * 0.3, 1))
    )
);
console.log(token)
