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
    const publicKeyBytes = atob(`MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyGWbPYHCppJ2rtB1FMI1
4kx0QwXAf96U5yIeNCPHmXcL7wrZ1TxejINR7Q7gsEzphWqQCpKhpvhdukofdKPA
IoUAcYUZ4AK4lTzBn7KRo/KNszcB+8fceNk17eVUiR+yM2Qw60v1hIwj6kKMWaXl
e4mvtDEVr6uZsaiMRNE8mo9Ojjf2On7gMP8FBCv7C8L7scsRHlq0CgSugdL3vtm7
aT0HYq1mhVYQXKs+TGsEtwrGSORimYnzMIR8BDxIFsL+H6DaC0SXtPfH2RBw5/mL
3U9t05k0xjDeQ0BvDuto1EdmAFFEPNExlCy7JbgkrNEMIfQtP/ytgazd+4UidQO/
EwIDAQAB`);

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
