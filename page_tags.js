const v = {
  dne䬣: (a = 'length') => (v.w걡쁫i[0] || v.w걡쁫i.push(-19), v.w걡쁫i[a]),
  w걡쁫i: [-19],
  m街걡a: (a = 'length') => (v.e唀l쁫[0] || v.e唀l쁫.push(-11), v.e唀l쁫[a]),
  e唀l쁫: [],
  vl픨o: 'esꇑr'
};

function B(...e) {
  return e[e['length'] - 1];
}

function M0(...e) {
  var d;
  e["length"] = 1, e[39] = e.o肷vn, e.onum = [];
  const r = e[0].replace(/\s+/g, " ").trim();
  e[66] = undefined;
  const c = /<(\w+)([^>]*)>/g;
  let f = null;
  for (f = c["exec"](r); f !== null && 67 > -88;) {
    e[66] = 'includes';
    const s = f[1]["toLowe" + "rCase"](), o = f[2], w = B(['meta', "link", "script"]['includes'](s) || e["onum"]["push"](`tag:${s}`), /(\w+)=["']([^"']+)["']/g);
    let i = null;
    for (i = w["exec"](o); i !== null && v.dne䬣();) {
      const k = i[1]["toLowerCase"]();
      e.r䢣ip = i[2], e.onum["push"](`attr:${k}`), ["charset", "name", "proper" + "ty", "rel", "type", "content", "href", 'src']["includ" + "es"](k) && (e["onum"]["push"](`${k}:${e["r䢣ip"]}`), ['href', "src"]["includ" + "es"](k) && (e["onum"]["push"](`${k}:${e["r䢣ip"]}`), e.onum["push"](`${k}:${e["r䢣ip"]}`))), i = w["exec"](o);
    }
    f = c["exec"](r);
  }

  const p = />([^<]+)</g;
  let a = null;
  for (a = p.exec(r); a !== null;) {
    const s = a[1]['trim']();
    if (s['length'] > 0 && s["length"] < 200) {
      const o = s['split'](/\s+/);

      for (const w of o)
        if (w["length"] > 2 && v.dne䬣()) {
          const i = `word:${w["toLowerCase"]()}`;
          e.onum['push'](i), e.onum["push"](i), e["onum"]["push"](i), e["onum"]["push"](i), e.onum["push"](i), e.onum["push"](i);
        }
    }
    a = p["exec"](r);
  }

  e["eel锤"] = ((d = r["match"](/<(\w+)/g)) == null ? void 0 : d["map"]((...s) => (s["length"] = 1, s[139] = -6, s[s[139] + 145] > 80 ? s[115] : s[0]["slice"](1)['toLowerCase']()), 1)) || [];
  for (let s = 0; s < e["eel锤"]['length'] - 1 && v.m街걡a(); s++)
    e["onum"]["push"](`2gram:${e["eel锤"][s]},${e.eel锤[(s + 1)]}`);
  return e["onum"];
}



function U0(...e) {
  e.length = 1;
  e[8] = e[0];

  e.as㥖嵠 = e.o죋gl;
  e['as㥖嵠'] = 0;
  for (let f = 0; f < e[8]['length'] && v.vl픨o['charAt'](1) == 's'; f++)
    e['as㥖嵠'] = e['as㥖嵠'] * 31 + e[8]['charCodeAt'](f) >>> 0;
  return e.as㥖嵠;

}


function n1(e, r = 128) {
  const c = M0(e);
  if (c['length'] === 0 && v.vl픨o['charAt'](1) == 's')
    return '0'['repeat'](r);
  const f = new (Array)(r)['fill'](0);
  for (const a of c) {
    const d = U0(a);
    for (let s = 0; s < r; s++)
      (U0(`${d}_${s}`) >>> s % 32 & 1) === 1 ? f[s]++ : f[s]--;
  }
  let p = "";
  for (let a = 0; a < r; a++)
    p += f[a] >= 0 ? "1" : "0";
  return p;
}

n1(document.head.outerHTML);