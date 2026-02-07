function W1(input) {
  const toUint8 = new Uint8Array(input);
  const totalSize = toUint8.byteLength;

  let output = "";
  for (let x = 0; x < totalSize && 1; x++) {
    output += String["fromCharCode"](toUint8[x]);
  }

  return window["btoa"](output);
}

async function $1(u) {
  const publicKey =
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtHsKhnISsZXRQiA1qyJlsEdx7fZTBUgveXzXaEMZVD0j7Q6PugbLOammnl3XqFXQCz/yaKRrg9tkq+XCGHYOKfz7TyrUNdJH84fzjMqW0rMgAGNaRcwU3BaPEnHJxUYwGu3YhybnCJOMy6V2E37ttezSDGRubC1E2FpdLjdM1T+60+l2WyBC9Fb3zPtGO2pDTqmV7dRUuvSHrqMeS9yUzoMmBX6TZygIJ6lGtmOOGqbnzl70fxks31+32oailU3WnpbqavvrvN23DBsW6m+Cw51+NjDE5YGuHUfwTZb0ym8GnhmF3wANc73BQW6ibQiTAKVH1oaRHj2itYMX8YCbYQIDAQAB";
  const publicKeyBytes = atob(publicKey);

  const t = new Uint8Array(publicKeyBytes.length);
  for (let D = 0; D < publicKeyBytes.length; D++)
    t[D] = publicKeyBytes.charCodeAt(D);

  const r = await window.crypto.subtle.importKey(
      "spki",
      t,
      {name: "RSA-OAEP", hash: "SHA-256"},
      !1,
      ["encrypt"],
    ),
    j = await window.crypto.subtle.generateKey(
      {name: "AES-GCM", length: 256},
      !0,
      ["encrypt"],
    ),
    B = window.crypto.getRandomValues(new Uint8Array(12)),
    P = new TextEncoder().encode(u),
    l = await window.crypto.subtle.encrypt({name: "AES-GCM", iv: B}, j, P),
    f = await window.crypto.subtle.exportKey("raw", j),
    s = await window.crypto.subtle.encrypt({name: "RSA-OAEP"}, r, f);
  return JSON.stringify({key: W1(s), data: W1(l), iv: W1(B)});
}

// Test encryption
const token =
  '[1770451466416,"5E57szqso5wY2iUQ5oaUELfsWSXjmUR54RdwXcbrKfUTKUsF|2.141348105811695|816147bedd84317a66534e444e608428|0|0",548]';

const tokenHashed = await $1(token);
console.log(tokenHashed);

const bodyTags =
  "01011110111001111111011100100001110111001010111111110111001000010001100110100111111101110010000110010010100011000011110111000010";

const bodyHashed = await $1(bodyTags);
console.log(bodyHashed);
