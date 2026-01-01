

function M(...e) {
  return e.length = 1, e.c苧la = -85, typeof TextDecoder < "u" && TextDecoder ? new TextDecoder().decode(new Uint8Array(e[0])) : typeof w0 < "u" && w0 ? w0.from(e[0]).toString("utf-8") : W0(e[0]);
}

var r = (f, p, a, d, s) => {
  if (typeof d === 'undefined' && (d = c), typeof s === 'undefined' && (s = K), a == f)
    return p[K[a]] = r(f, p);
  if (a == d)
    return p ? f[s[p]] : K[f] || (a = s[f] || d, K[f] = a(O[f]));
  if (p)
    return [s, p] = [d(s), f || a], r(f, s, a);
  if (d === r)
    return c = p, c(a);
  if (f !== p)
    return s[f] || (s[f] = d(O[f]));
};

function c(f, p = 'RohOMq|yN<CAf`"mPdQUL!D$J_lp}/9eF%6j[b+BIY8gtTkvE(&0Vs3;:a@uSXG1{cnWKi2w]>H)=*r~5.7#x?4zZ,^', a, d, s = [], o, w = 0, i, k, y) {
  for (a = "" + (f || ""), d = a.length, o = 0, i = -1, k = 0; k < d; k++)
    if (y = p.indexOf(a[k]), y !== -1)
      if (i < 0)
        i = y;
      else {
        i += y * 91, o |= i << w, w += (i & 8191) > 88 ? 13 : 14;
        do
          s.push(o & 255), o >>= 8, w -= 8;
        while (w > 7);
        i = -1;
      }
  return i > -1 && s.push((o | i << w) & 255), M(s);
}

var K = [];
function B(...e) {
  return e[e['length'] - 1];
}

function f1() {
  const e = 0.4294846358501722, r = 3, c = 1;
  return {
    ['name']: 'PolyTransform',
    ['encrypt']: ((...f) => (f['length'] = 1, f[59] = f[0], e * f[59] ** 2 + r * f[59] + c), 1),
  };
}

async function e1(e) {
  const r = new (TextEncoder)()['encode'](e), c = await crypto.subtle.digest('SHA-256', r);
  return Array['from'](new (Uint8Array)(c))['map'](P((...f) => (f['length'] = 1, f[58] = f[0], f[58]['toStri' + "ng"](16)['padStart'](2, '0')), 1))['join']("")['substring'](0, 32);
}

const s1 = [null, f1];
const d1 = P(async (...e) => {
  e['length'] = 4;
  e.ub氍r = e[3];

  const r = Date.now();
  const c = s1[2];
  const f = c().encrypt(e[0]);
  const p = new (Uint16Array)(1);
  const a = B(window.crypto.getRandomValues(p), p[0] % 2001);
  const d = Navigator.userAgent;
  const s = await e1(d);
  let o = "" + f;
  let w = `${e[1]}|${o}|${s}|${e[2] ? 1 : 0}|${e.ub氍r ? 1 : 0}`;
  let i = n1(document.head.outerHTML);
  return [r, w, a, i];
}, 4);

const de = async (e, t) => {
  B.length === 0 && (B = await He(e));
  const r = Le(B, t);
  return {
    providerAccount: r.address,
    provider: {
      url: r.url,
      datasetId: r.datasetId
    }
  };
};

const [L, Y, J, Q] = await d1(s, p.account.address, o, w);
// -- L = 1767271479820
// -- Y = 'user crypto address|2.0337924089322748|62d18984722ed057781bce4342a00927|0|0'
// -- J = 1555
// -- Q = '01001110110001111110011100110001110010001100011111100111001100010101100111000111111001110011000110111100100111001011110111001111'


const y = await de('production', J);
const i = await encrypt(JSON.stringify([L, Y, J]));
const k = await encrypt(Q);

const res = { token: i, provider: y, shadowDomCleanup: r, encryptHeadHash: k, userAccount: p };