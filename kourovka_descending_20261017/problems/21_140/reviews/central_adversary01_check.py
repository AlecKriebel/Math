#!/usr/bin/env python3
"""Independent exact audit: words of PL atoms, not composed vertex graphs.

This file imports no candidate implementation. The cocycle is evaluated as
P(b_h, b_g precomposed with h), using chain-rule logarithmic derivatives of
the individual word atoms. Finite checks supplement the written proof.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
import json
import random


def log2(q):
    n, d = q.numerator, q.denominator
    assert n > 0 and n & (n - 1) == 0 and d & (d - 1) == 0
    return n.bit_length() - d.bit_length()


@dataclass(frozen=True)
class Atom:
    vertices: tuple

    def value(self, x):
        for (a, b), (c, d) in zip(self.vertices, self.vertices[1:]):
            if a <= x <= c:
                return b + (x - a) * (d - b) / (c - a)
        raise ValueError(x)

    def derivative_log(self, x, side):
        x = Q(x)
        if x == 1:
            x = Q(0)
        if x == 0 and side == "left":
            (a, b), (c, d) = self.vertices[-2:]
            return log2((d - b) / (c - a))
        for (a, b), (c, d) in zip(self.vertices, self.vertices[1:]):
            if (a <= x < c if side == "right" else a < x <= c):
                return log2((d - b) / (c - a))
        raise ValueError((x, side))

    def inverse(self):
        return Atom(tuple((y, x) for x, y in self.vertices))

    def reflection(self):
        return Atom(tuple((1 - x, 1 - y) for x, y in self.vertices[::-1]))

    def clone(self, start, end):
        length = end - start
        pts = {(Q(0), Q(0)), (Q(1), Q(1))}
        pts.update((start + length*x, start + length*y) for x, y in self.vertices)
        return Atom(tuple(sorted(pts)))


@dataclass(frozen=True)
class Word:
    atoms: tuple = ()

    def value(self, x):
        for a in self.atoms[::-1]:
            x = a.value(x)
        return x

    def derivative_log(self, x, side):
        result = 0
        for a in self.atoms[::-1]:
            result += a.derivative_log(x, side)
            x = a.value(x)
        return result

    def inverse(self):
        return Word(tuple(a.inverse() for a in self.atoms[::-1]))

    def reflection(self):
        return Word(tuple(a.reflection() for a in self.atoms))

    def clone(self, start=Q(1, 8), end=Q(3, 8)):
        return Word(tuple(a.clone(start, end) for a in self.atoms))

    def __mul__(self, other):
        return Word(self.atoms + other.atoms)

    @lru_cache(maxsize=None)
    def breakpoints(self):
        result = {Q(0)}
        for i, a in enumerate(self.atoms):
            suffix_inverse = Word(self.atoms[i+1:]).inverse()
            result.update(suffix_inverse.value(x) for x, _ in a.vertices[:-1])
        return frozenset(result)


def cocycle_terms(g, h):
    # Jump locations of b_h and b_g precomposed with h.
    locs = h.breakpoints() | {h.inverse().value(x) for x in g.breakpoints()}
    result = {}
    for x in sorted(locs):
        y = h.value(x)
        hr, hl = h.derivative_log(x, "right"), h.derivative_log(x, "left")
        gr, gl = g.derivative_log(y, "right"), g.derivative_log(y, "left")
        value = hr*(gr-gl) - gr*(hr-hl)
        if value:
            result[str(x)] = value
    return result


def cocycle(g, h):
    return sum(cocycle_terms(g, h).values())


def cup(g, h):
    return g.derivative_log(Q(0), "right") * h.derivative_log(Q(0), "left")


def mirrored(f):
    k = f.clone()
    return k * k.reflection()


def same(f, g):
    return all(f.value(x) == g.value(x) for x in f.breakpoints() | g.breakpoints() | {Q(1)})


def main():
    a = Atom(((Q(0),Q(0)), (Q(1,2),Q(1,4)), (Q(3,4),Q(1,2)), (Q(1),Q(1))))
    A = Word((a,))
    B = A.clone(Q(1,2),Q(1))
    end_f, end_g = A.clone(Q(0),Q(1,4)), A.clone(Q(3,4),Q(1))
    int_f, int_g = A.clone(Q(1,4),Q(1,2)), A.clone(Q(1,2),Q(3,4))
    witnesses = {}
    for name, f, g in (("endpoint",end_f,end_g), ("interior",int_f,int_g)):
        assert same(f*g,g*f)
        witnesses[name] = {"cup":cup(f,g)-cup(g,f),
                           "C_fg":cocycle(f,g), "C_gf":cocycle(g,f),
                           "fg_terms":cocycle_terms(f,g), "gf_terms":cocycle_terms(g,f)}
    assert witnesses["endpoint"]["cup"] == -1
    assert witnesses["endpoint"]["C_fg"] == -1 and witnesses["endpoint"]["C_gf"] == 1
    assert witnesses["interior"]["cup"] == 0
    assert witnesses["interior"]["C_fg"] == 1 and witnesses["interior"]["C_gf"] == -1
    # Negative control: separated clones without reflection do not cancel.
    def unmirrored(f):
        return f.clone() * f.clone(Q(5,8),Q(7,8))
    unmirrored_pairing = cocycle(unmirrored(int_f),unmirrored(int_g))-cocycle(unmirrored(int_g),unmirrored(int_f))
    assert unmirrored_pairing == 4
    u, v = A*B.inverse(), A.inverse()*B*A
    v2 = A.inverse()*A.inverse()*B*A*A
    assert same(u*v,v*u) and same(u*v2,v2*u)
    source_alternations = [cocycle(u,v)-cocycle(v,u), cocycle(u,v2)-cocycle(v2,u)]
    assert source_alternations == [0,-2]

    rng = random.Random(2026101721140)
    gens = [A, B, A.inverse(), B.inverse()]
    samples = [Word(), A, B, A.inverse(), B.inverse(), end_f, end_g, int_f, int_g]
    for _ in range(18):
        f = Word()
        for _ in range(rng.randint(1,8)):
            f = f*rng.choice(gens)
        samples.append(f)
    counts = {name:0 for name in ["cocycle", "reflection", "mirrored_zero", "local_additivity", "homomorphism", "reflection_derivative"]}
    for _ in range(140):
        f, g, h = (rng.choice(samples) for _ in range(3))
        assert cocycle(g,h)-cocycle(f*g,h)+cocycle(f,g*h)-cocycle(f,g) == 0
        counts["cocycle"] += 1
        assert cocycle(f.reflection(),g.reflection()) == -cocycle(f,g)
        counts["reflection"] += 1
        assert cocycle(mirrored(f),mirrored(g)) == 0
        counts["mirrored_zero"] += 1
        kf, kg = f.clone(), g.clone()
        assert cocycle(mirrored(f),mirrored(g)) == cocycle(kf,kg)+cocycle(kf.reflection(),kg.reflection())
        counts["local_additivity"] += 1
        assert same(mirrored(f*g),mirrored(f)*mirrored(g))
        counts["homomorphism"] += 1
        for x in f.reflection().breakpoints():
            y = Q(0) if x == 0 else 1-x
            assert f.reflection().derivative_log(x,"right") == f.derivative_log(y,"left")
            assert f.reflection().derivative_log(x,"left") == f.derivative_log(y,"right")
        counts["reflection_derivative"] += 1
    print(json.dumps({"implementation":"independent word atoms; direct P(b_h,b_g composed with h)",
                      "arithmetic":"Fraction", "random_seed":2026101721140,
                      "sample_count":len(samples), "witnesses":witnesses,
                      "negative_control_unmirrored_pairing":unmirrored_pairing,
                      "source_alternations":source_alternations,
                      "checks_passed":counts}, indent=2))


if __name__ == "__main__":
    main()
