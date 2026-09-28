"""Reed-Solomon GF(2^8) Error Correcting Code Engine.
100% Python Standard Library.
"""

class GaloisField256:
    """Galois Field GF(2^8) with primitive polynomial 0x11d."""
    def __init__(self, prim=0x11d):
        self.exp = [0] * 512
        self.log = [0] * 256
        x = 1
        for i in range(255):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & 0x100:
                x ^= prim
        for i in range(255, 512):
            self.exp[i] = self.exp[i - 255]

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def div(self, a, b):
        if b == 0:
            raise ZeroDivisionError("GF(256) division by zero")
        if a == 0:
            return 0
        return self.exp[(self.log[a] - self.log[b] + 255) % 255]

    def poly_mul(self, p, q):
        r = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                r[i + j] ^= self.mul(a, b)
        return r

class ReedSolomonCoder:
    """Systematic Reed-Solomon (N, K) coder in GF(2^8)."""
    def __init__(self, nsym=4):
        self.gf = GaloisField256()
        self.nsym = nsym
        g = [1]
        for i in range(nsym):
            root = self.gf.exp[i]
            g = self.gf.poly_mul(g, [1, root])
        self.gen = g

    def encode(self, msg):
        out = list(msg) + [0] * self.nsym
        for i in range(len(msg)):
            coef = out[i]
            if coef != 0:
                for j in range(1, len(self.gen)):
                    out[i + j] ^= self.gf.mul(self.gen[j], coef)
        return list(msg) + out[len(msg):]

    def compute_syndromes(self, codeword):
        syn = []
        for i in range(self.nsym):
            alpha_i = self.gf.exp[i]
            val = 0
            for byte in codeword:
                val = self.gf.mul(val, alpha_i) ^ byte
            syn.append(val)
        return syn
