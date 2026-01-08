(function () {
    "use strict";
    /*! noble-hashes - MIT License (c) 2022 Paul Miller (paulmillr.com) */

    function A(t) {
        return t instanceof Uint8Array || ArrayBuffer.isView(t) && t.constructor.name === "Uint8Array";
    }

    function b(t, ...e) {
        if (!A(t)) throw new Error("Uint8Array expected");
        if (e.length > 0 && !e.includes(t.length)) throw new Error("Uint8Array expected of length " + e + ", got length=" + t.length);
    }

    function k(t, e = !0) {
        if (t.destroyed) throw new Error("Hash instance has been destroyed");
        if (e && t.finished) throw new Error("Hash#digest() has already been called");
    }

    function E(t, e) {
        b(t);
        const a = e.outputLen;
        if (t.length < a) throw new Error("digestInto() expects output buffer of length at least " + a);
    }

    function y(...t) {
        for (let e = 0; e < t.length; e++) t[e].fill(0);
    }

    function w(t) {
        return new DataView(t.buffer, t.byteOffset, t.byteLength);
    }

    function d(t, e) {
        return t << 32 - e | t >>> e;
    }

    function U(t) {
        if (typeof t != "string") throw new Error("string expected");
        return new Uint8Array(new TextEncoder().encode(t));
    }

    function x(t) {
        return typeof t == "string" && (t = U(t)), b(t), t;
    }
    class q { }

    function B(t) {
        const e = r => t().update(x(r)).digest(),
            a = t();
        return e.outputLen = a.outputLen, e.blockLen = a.blockLen, e.create = () => t(), e;
    }

    function L(t, e, a, r) {
        if (typeof t.setBigUint64 == "function") return t.setBigUint64(e, a, r);
        const o = BigInt(32),
            n = BigInt(4294967295),
            i = Number(a >> o & n),
            l = Number(a & n),
            c = r ? 4 : 0,
            u = r ? 0 : 4;
        t.setUint32(e + c, i, r), t.setUint32(e + u, l, r);
    }

    function I(t, e, a) {
        return t & e ^ ~t & a;
    }

    function H(t, e, a) {
        return t & e ^ t & a ^ e & a;
    }
    class T extends q {
        constructor(e, a, r, o) {
            super(), this.finished = !1, this.length = 0, this.pos = 0, this.destroyed = !1, this.blockLen = e, this.outputLen = a, this.padOffset = r, this.isLE = o, this.buffer = new Uint8Array(e), this.view = w(this.buffer);
        }
        update(e) {
            k(this), e = x(e), b(e);
            const {
                view: a,
                buffer: r,
                blockLen: o
            } = this, n = e.length;
            for (let i = 0; i < n;) {
                const l = Math.min(o - this.pos, n - i);
                if (l === o) {
                    const c = w(e);
                    for (; o <= n - i; i += o) this.process(c, i);
                    continue;
                }
                r.set(e.subarray(i, i + l), this.pos), this.pos += l, i += l, this.pos === o && (this.process(a, 0), this.pos = 0);
            }
            return this.length += e.length, this.roundClean(), this;
        }
        digestInto(e) {
            k(this), E(e, this), this.finished = !0;
            const {
                buffer: a,
                view: r,
                blockLen: o,
                isLE: n
            } = this;
            let {
                pos: i
            } = this;
            a[i++] = 128, y(this.buffer.subarray(i)), this.padOffset > o - i && (this.process(r, 0), i = 0);
            for (let s = i; s < o; s++) a[s] = 0;
            L(r, o - 8, BigInt(this.length * 8), n), this.process(r, 0);
            const l = w(e),
                c = this.outputLen;
            if (c % 4) throw new Error("_sha2: outputLen should be aligned to 32bit");
            const u = c / 4,
                m = this.get();
            if (u > m.length) throw new Error("_sha2: outputLen bigger than state");
            for (let s = 0; s < u; s++) l.setUint32(4 * s, m[s], n);
        }
        digest() {
            const {
                buffer: e,
                outputLen: a
            } = this;
            this.digestInto(e);
            const r = e.slice(0, a);
            return this.destroy(), r;
        }
        _cloneInto(e) {
            e || (e = new this.constructor), e.set(...this.get());
            const {
                blockLen: a,
                buffer: r,
                length: o,
                finished: n,
                destroyed: i,
                pos: l
            } = this;
            return e.destroyed = i, e.finished = n, e.length = o, e.pos = l, o % a && e.buffer.set(r), e;
        }
        clone() {
            return this._cloneInto();
        }
    }
    const h = Uint32Array.from([1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225]),
        _ = Uint32Array.from([1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, 2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037, 2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298]),
        p = new Uint32Array(64);
    class D extends T {
        constructor(e = 32) {
            super(64, e, 8, !1), this.A = h[0] | 0, this.B = h[1] | 0, this.C = h[2] | 0, this.D = h[3] | 0, this.E = h[4] | 0, this.F = h[5] | 0, this.G = h[6] | 0, this.H = h[7] | 0;
        }
        get() {
            const {
                A: e,
                B: a,
                C: r,
                D: o,
                E: n,
                F: i,
                G: l,
                H: c
            } = this;
            return [e, a, r, o, n, i, l, c];
        }
        set(e, a, r, o, n, i, l, c) {
            this.A = e | 0, this.B = a | 0, this.C = r | 0, this.D = o | 0, this.E = n | 0, this.F = i | 0, this.G = l | 0, this.H = c | 0;
        }
        process(e, a) {
            for (let s = 0; s < 16; s++, a += 4) p[s] = e.getUint32(a, !1);
            for (let s = 16; s < 64; s++) {
                const g = p[s - 15],
                    f = p[s - 2],
                    z = d(g, 7) ^ d(g, 18) ^ g >>> 3,
                    v = d(f, 17) ^ d(f, 19) ^ f >>> 10;
                p[s] = v + p[s - 7] + z + p[s - 16] | 0;
            }
            let {
                A: r,
                B: o,
                C: n,
                D: i,
                E: l,
                F: c,
                G: u,
                H: m
            } = this;
            for (let s = 0; s < 64; s++) {
                const g = d(l, 6) ^ d(l, 11) ^ d(l, 25),
                    f = m + g + I(l, c, u) + _[s] + p[s] | 0,
                    v = (d(r, 2) ^ d(r, 13) ^ d(r, 22)) + H(r, o, n) | 0;
                m = u, u = c, c = l, l = i + f | 0, i = n, n = o, o = r, r = f + v | 0;
            }
            r = r + this.A | 0, o = o + this.B | 0, n = n + this.C | 0, i = i + this.D | 0, l = l + this.E | 0, c = c + this.F | 0, u = u + this.G | 0, m = m + this.H | 0, this.set(r, o, n, i, l, c, u, m);
        }
        roundClean() {
            y(p);
        }
        destroy() {
            this.set(0, 0, 0, 0, 0, 0, 0, 0), y(this.buffer);
        }
    }
    const C = {
        256: B(() => new D)
    }[256],
        M = "words".split("|"),
        F = "Invalid entropy";

    function S(t) {
        return Number.parseInt(t, 2);
    }

    function j(t) {
        return t.map(e => e.toString(2).padStart(8, "0")).join("");
    }

    function V(t) {
        return j(Array.from(C(t))).slice(0, t.length * 8 / 32);
    }

    function $(t, e = M) {
        if (t.length % 4 !== 0 || t.length < 16 || t.length > 32) throw new Error(F);
        const r = `${j(Array.from(t))}${V(t)}`.match(/(.{1,11})/g)?.map(o => e[S(o)]);
        if (!r || r.length < 12) throw new Error("Unable to map entropy to mnemonic");
        return r.join(" ");
    }
    self.addEventListener("message", async t => {
        const {
            taskId: e,
            task: a,
            data: r
        } = t.data;
        try {
            let o;
            switch (a) {
                case "test":
                    o = "ready";
                    break;
                case "entropyToMnemonic":
                    if (!r.entropy) throw new Error("Entropy data is required");
                    o = await G(r.entropy);
                    break;
                default:
                    throw new Error(`Unknown task: ${a}`);
            }
            const n = {
                taskId: e,
                result: o
            };
            self.postMessage(n);
        } catch (o) {
            const n = {
                taskId: e,
                error: o instanceof Error ? o.message : "Unknown error"
            };
            self.postMessage(n);
        }
    });
    async function G(t) {
        try {
            return $(t);
        } catch (e) {
            throw new Error(`Failed to process entropy: ${e instanceof Error ? e.message : "Unknown error"}`);
        }
    }
})();