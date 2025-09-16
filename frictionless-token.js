// reversing how to generate ("token") key for /frictionless endpoint\
const Ax = (a) => {
    const currTime = Date.now();
    let pie = Number(currTime.toString().slice(-3)) + a;
    pie /= 999 * Math.PI;
    pie -= Math.PI / 2
    return [currTime, Math.sin(pie) * 1000]
};

async function encryptPlainText(...e) {
    // new key (September 15, 2025) 
    const publicKeyBytes = atob(`MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA78KXuYmPpOLaXdU3Rbmr
P9xUZnNJ7Ykfec9fK4/i/rlJodoxkKub2ZvxkyAoESotxprTN2FhAABh3hnA6qY/
GGszpaAghtUpnhU6WTHbN305Bdsk+FzrqYE3dxc7hgGaqYodz55OmuGdaomN2Mqs
W7U3/Vk35Fa0DJpQel7DDdJU8JQKmaHJVSewOf+bxYw1RvM5a90US9pc2cqMExx/
hYl294Xn0SDDUz0oYalG8hOgFT5rnfuc5inGqb+tQzljUBnvdDyQFYRvjnwZxRMM
SLh46f2v0xvNfHVp7qXPMqLCXeqnsfU5tgBpuwxWFzI552HTfqw8NUaefY4xN9vn
VQIDAQAB`);

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
