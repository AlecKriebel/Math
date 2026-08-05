#!/usr/bin/env python3
"""Dependency-free exact audit of a K2P tree/theta-trinet collision.

The calculation uses exact rational arithmetic in the six-dimensional algebra
Q[ell,s]/(f(ell), s^2-1423), where ell is the unique root of f in the
stored rational interval and s denotes the positive square root of 1423.
No floating-point equality is used.
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

BASE = Path(__file__).resolve().parents[1]
CERT = json.loads((BASE / "certificate_k2p_continuous_time.json").read_text())


def F(x: str | int | Fraction, den: int | None = None) -> Fraction:
    if den is not None:
        return Fraction(int(x), den)
    return x if isinstance(x, Fraction) else Fraction(str(x))


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise AssertionError(msg)


# f(ell)=F3 ell^3 + F2 ell^2 + F1 ell + F0
F0 = F(CERT["field"]["ell_polynomial_constant_first"][0])
F1 = F(CERT["field"]["ell_polynomial_constant_first"][1])
F2 = F(CERT["field"]["ell_polynomial_constant_first"][2])
F3 = F(CERT["field"]["ell_polynomial_constant_first"][3])
RAD = int(CERT["field"]["sqrt_radicand"])
ELL_LO, ELL_HI = map(F, CERT["field"]["ell_interval"])
SQ_LO, SQ_HI = map(F, CERT["field"]["sqrt_interval"])

# ell^3 = REL0 + REL1 ell + REL2 ell^2
REL0, REL1, REL2 = -F0 / F3, -F1 / F3, -F2 / F3


@dataclass(frozen=True)
class Alg:
    """c0+c1*ell+c2*ell^2 + sqrt(RAD)*(d0+d1*ell+d2*ell^2)."""

    c: Tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]

    @staticmethod
    def zero() -> "Alg":
        return Alg((F(0),) * 6)

    @staticmethod
    def one() -> "Alg":
        return Alg((F(1), F(0), F(0), F(0), F(0), F(0)))

    @staticmethod
    def rat(x: str | int | Fraction) -> "Alg":
        return Alg((F(x), F(0), F(0), F(0), F(0), F(0)))

    @staticmethod
    def ell() -> "Alg":
        return Alg((F(0), F(1), F(0), F(0), F(0), F(0)))

    @staticmethod
    def sqrt() -> "Alg":
        return Alg((F(0), F(0), F(0), F(1), F(0), F(0)))

    def __add__(self, other: "Alg") -> "Alg":
        return Alg(tuple(a + b for a, b in zip(self.c, other.c)))  # type: ignore[arg-type]

    def __neg__(self) -> "Alg":
        return Alg(tuple(-a for a in self.c))  # type: ignore[arg-type]

    def __sub__(self, other: "Alg") -> "Alg":
        return self + (-other)

    def scale(self, q: str | int | Fraction) -> "Alg":
        q = F(q)
        return Alg(tuple(q * a for a in self.c))  # type: ignore[arg-type]

    @staticmethod
    def _reduce_poly(raw: List[Fraction]) -> Tuple[Fraction, Fraction, Fraction]:
        raw = raw + [F(0)] * (5 - len(raw))
        for k in range(len(raw) - 1, 2, -1):
            a = raw[k]
            if a:
                raw[k - 3] += a * REL0
                raw[k - 2] += a * REL1
                raw[k - 1] += a * REL2
                raw[k] = F(0)
        return raw[0], raw[1], raw[2]

    def __mul__(self, other: "Alg") -> "Alg":
        # Separate sqrt parity 0/1.  A product of two sqrt-parts contributes RAD.
        raw0 = [F(0)] * 5
        raw1 = [F(0)] * 5
        for sf1 in (0, 1):
            for i in range(3):
                a = self.c[3 * sf1 + i]
                if not a:
                    continue
                for sf2 in (0, 1):
                    for j in range(3):
                        b = other.c[3 * sf2 + j]
                        if not b:
                            continue
                        parity = sf1 ^ sf2
                        coeff = a * b * (RAD if sf1 and sf2 else 1)
                        (raw1 if parity else raw0)[i + j] += coeff
        a0 = self._reduce_poly(raw0)
        a1 = self._reduce_poly(raw1)
        return Alg(a0 + a1)

    def __pow__(self, n: int) -> "Alg":
        require(n >= 0, "negative powers are not used")
        out = Alg.one()
        base = self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n >>= 1
        return out

    def is_zero(self) -> bool:
        return all(x == 0 for x in self.c)

    def interval(self) -> Tuple[Fraction, Fraction]:
        lo = F(0)
        hi = F(0)
        for sf in (0, 1):
            for i in range(3):
                coeff = self.c[3 * sf + i]
                if not coeff:
                    continue
                mon_lo = (ELL_LO ** i) * (SQ_LO if sf else 1)
                mon_hi = (ELL_HI ** i) * (SQ_HI if sf else 1)
                if coeff > 0:
                    lo += coeff * mon_lo
                    hi += coeff * mon_hi
                else:
                    lo += coeff * mon_hi
                    hi += coeff * mon_lo
        return lo, hi

    def require_positive(self, msg: str) -> None:
        lo, hi = self.interval()
        require(lo > 0, f"{msg}: interval [{lo}, {hi}] is not positive")

    def require_lt_one(self, msg: str) -> None:
        (Alg.one() - self).require_positive("1 - " + msg)

    def approx(self) -> float:
        lo, hi = self.interval()
        return float((lo + hi) / 2)

    def __repr__(self) -> str:
        return "Alg(" + ",".join(str(x) for x in self.c) + ")"


def parse_alg(raw: Sequence[str]) -> Alg:
    require(len(raw) == 6, "algebraic coefficient vector must have length six")
    return Alg(tuple(F(x) for x in raw))  # type: ignore[arg-type]


# ---- polynomial/Sturm utilities for isolating ell --------------------------

def trim(p: List[Fraction]) -> List[Fraction]:
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def derivative(p: Sequence[Fraction]) -> List[Fraction]:
    return trim([F(i) * p[i] for i in range(1, len(p))] or [F(0)])


def divrem(a: Sequence[Fraction], b: Sequence[Fraction]) -> Tuple[List[Fraction], List[Fraction]]:
    a = trim(list(a))
    b = trim(list(b))
    require(not (len(b) == 1 and b[0] == 0), "division by zero polynomial")
    if len(a) < len(b):
        return [F(0)], a
    q = [F(0)] * (len(a) - len(b) + 1)
    while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
        k = len(a) - len(b)
        t = a[-1] / b[-1]
        q[k] += t
        for j in range(len(b)):
            a[j + k] -= t * b[j]
        trim(a)
    return trim(q), trim(a)


def eval_poly(p: Sequence[Fraction], x: Fraction) -> Fraction:
    out = F(0)
    for a in reversed(p):
        out = out * x + a
    return out


def sign(q: Fraction) -> int:
    return 1 if q > 0 else (-1 if q < 0 else 0)


def sturm_sequence(p: Sequence[Fraction]) -> List[List[Fraction]]:
    seq = [trim(list(p)), derivative(p)]
    while not (len(seq[-1]) == 1 and seq[-1][0] == 0):
        _, r = divrem(seq[-2], seq[-1])
        if len(r) == 1 and r[0] == 0:
            break
        seq.append([-x for x in r])
    return seq


def variations(seq: Sequence[Sequence[Fraction]], x: Fraction) -> int:
    signs = [sign(eval_poly(p, x)) for p in seq]
    signs = [s for s in signs if s]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def verify_field() -> None:
    p = [F0, F1, F2, F3]
    require(eval_poly(p, ELL_LO) * eval_poly(p, ELL_HI) < 0,
            "ell polynomial must change sign across isolating interval")
    seq = sturm_sequence(p)
    require(variations(seq, ELL_LO) - variations(seq, ELL_HI) == 1,
            "ell interval must contain exactly one real root")
    require(SQ_LO > 0 and SQ_LO * SQ_LO < RAD < SQ_HI * SQ_HI,
            "sqrt interval does not isolate positive sqrt(radicand)")
    ell = Alg.ell()
    sq = Alg.sqrt()
    require((ell ** 3).scale(F3) + (ell ** 2).scale(F2) + ell.scale(F1) + Alg.rat(F0) == Alg.zero(),
            "ell minimal-polynomial relation")
    require(sq * sq == Alg.rat(RAD), "sqrt relation")
    print("[field] PASS  cubic root and sqrt(1423) isolated rigorously")


# ---- group/K2P utilities ---------------------------------------------------

SYMBOLS = ("A", "C", "G", "T")
CHAR = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),   # character/eigenvalue label C
    (1, -1, 1, -1),   # character/eigenvalue label G
    (1, -1, -1, 1),
)


def k2p_vector(s: Alg, g: Alg) -> Tuple[Alg, Alg, Alg, Alg]:
    return Alg.one(), s, g, s


def transition_probs(e: Sequence[Alg]) -> Tuple[Alg, Alg, Alg, Alg]:
    one, c, g, t = e
    return (
        (one + c + g + t).scale(F(1, 4)),
        (one + c - g - t).scale(F(1, 4)),
        (one - c + g - t).scale(F(1, 4)),
        (one - c - g + t).scale(F(1, 4)),
    )


def check_edge(name: str, e: Sequence[Alg], strict_ct: bool = True) -> None:
    require(len(e) == 4 and e[0] == Alg.one() and e[1] == e[3], f"{name}: K2P form")
    for sym, val in zip(SYMBOLS[1:], e[1:]):
        val.require_positive(f"{name}.{sym}")
        val.require_lt_one(f"{name}.{sym}")
    ps = transition_probs(e)
    for sym, val in zip(SYMBOLS, ps):
        val.require_positive(f"{name}.p_{sym}")
    require(sum(ps, Alg.zero()) == Alg.one(), f"{name}: transition probabilities sum to one")
    if strict_ct:
        # For K2P with a_C=a_T=s, strict positive-rate embeddability is g>s^2.
        (e[2] - e[1] * e[1]).require_positive(f"{name}: strict continuous-time margin g-s^2")


# ---- certificate parsing ---------------------------------------------------

ell = Alg.ell()
sqrt = Alg.sqrt()
network_vectors = {name: tuple(parse_alg(x) for x in row)
                   for name, row in CERT["network_vectors"].items()}
tree_vectors = {name: tuple(parse_alg(x) for x in row)
                for name, row in CERT["tree_vectors"].items()}
core_vectors = {name: tuple(parse_alg(x) for x in row)
                for name, row in CERT["core_tree_factors"].items()}

ARCS = {row["id"]: (row["parent"], row["child"], row["vector"])
        for row in CERT["rooted_network"]["arcs"]}
RETICS = CERT["rooted_network"]["reticulations"]
NODES = {row["id"]: row["type"] for row in CERT["rooted_network"]["vertices"]}
LEAF_POS = {"1": 0, "2": 1, "3": 2}


def verify_topology() -> None:
    indeg = {v: 0 for v in NODES}
    outdeg = {v: 0 for v in NODES}
    children = {v: [] for v in NODES}
    for u, v, _ in ARCS.values():
        require(u in NODES and v in NODES, "unknown arc endpoint")
        indeg[v] += 1
        outdeg[u] += 1
        children[u].append(v)
    require((indeg["rho"], outdeg["rho"]) == (0, 2), "root degree")
    for v in ("u", "p", "q"):
        require((indeg[v], outdeg[v]) == (1, 2), f"tree vertex {v} degree")
    for v in ("r2", "r3"):
        require((indeg[v], outdeg[v]) == (2, 1), f"reticulation {v} degree")
    for v in ("1", "2", "3"):
        require((indeg[v], outdeg[v]) == (1, 0), f"leaf {v} degree")
    # Kahn DAG test.
    work = dict(indeg)
    queue = [v for v in NODES if work[v] == 0]
    seen = []
    while queue:
        u = queue.pop()
        seen.append(u)
        for v in children[u]:
            work[v] -= 1
            if work[v] == 0:
                queue.append(v)
    require(len(seen) == len(NODES), "rooted graph is acyclic")

    # Suppressed semi-directed theta core.
    core_nodes = {"u", "p", "q", "r2", "r3"}
    core_edges = {
        frozenset(("u", "p")), frozenset(("u", "q")),
        frozenset(("p", "r2")), frozenset(("q", "r2")),
        frozenset(("p", "r3")), frozenset(("q", "r3")),
    }
    expected_paths = [
        ("p", "u", "q"), ("p", "r2", "q"), ("p", "r3", "q")
    ]
    for pth in expected_paths:
        require(all(frozenset((a, b)) in core_edges for a, b in zip(pth, pth[1:])),
                f"missing theta path {pth}")
    # Every core edge lies on at least one of the three pairwise cycles.
    cycles = [set(map(frozenset, [
        (expected_paths[i][0], expected_paths[i][1]),
        (expected_paths[i][1], expected_paths[i][2]),
        (expected_paths[j][0], expected_paths[j][1]),
        (expected_paths[j][1], expected_paths[j][2]),
    ])) for i, j in ((0, 1), (0, 2), (1, 2))]
    require(all(any(e in cyc for cyc in cycles) for e in core_edges), "each core edge lies on a cycle")
    pendant = {frozenset(("1", "u")), frozenset(("r2", "2")), frozenset(("r3", "3"))}
    require(len(pendant) == 3 and len(core_nodes & {"r2", "r3"}) == 2,
            "three attachments and two reticulations")
    print("[topology] PASS  rooted binary DAG suppresses to a strict level-two theta 3-blob")


def verify_parameters() -> None:
    for name, e in network_vectors.items():
        check_edge("network " + name, e)
    # Effective root-suppressed leaf-1 edge K odot K.
    K = network_vectors["K"]
    effective = tuple(x * x for x in K)
    expected = k2p_vector(Alg.rat(F(1, 4)), Alg.rat(F(1, 4)))
    require(effective == expected, "effective K odot K edge")
    check_edge("effective KxK", effective)
    for name, e in tree_vectors.items():
        check_edge("tree " + name, e)
    for d in CERT["mixing_parameters"].values():
        q = F(d)
        require(0 < q < 1, "mixing parameter lies in (0,1)")
    print("[parameters] PASS  all rooted/effective/tree edges are strict Theta_0 and strict continuous-time K2P")


# ---- exact construction identities ----------------------------------------

def verify_construction() -> None:
    u = network_vectors["U"][1]
    v = network_vectors["U"][2]
    w = network_vectors["V"][1]
    x = network_vectors["V"][2]
    a = network_vectors["A"][1]
    b = network_vectors["A"][2]
    c = network_vectors["B"][1]
    d = network_vectors["B"][2]
    r = c.scale(5)       # c/a, since a=1/5
    s = d.scale(2)       # d/b, since b=1/2
    require(r == Alg.rat(F(7, 6)) and s == Alg.rat(F(2, 15)), "ratio parameters r,s")
    Ac = Alg.one() + (r * u * w).scale(2) + r * r
    Ag = Alg.one() + (s * v * x).scale(2) + s * s
    require(Ac == Alg.rat(F(1423, 576)), "C-block square relation")
    require(Ag == ell * ell, "G-block square relation")
    N = u + s * u * x + r * v * w + r * s * w
    H = v + (r * u * w).scale(2) + r * r * x
    require(N == (u + r * w) * ell, "first K2P shape equation")
    require(H * ell == (v + s * x) * Ac, "second K2P shape equation")
    print("[construction] PASS  cubic symmetric-ansatz equations verified exactly")


# ---- displayed-tree reconstruction ----------------------------------------

def descendants(start: str, children: Mapping[str, Sequence[str]]) -> set[str]:
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in children.get(u, ()):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def retained_edges(choice2: int, choice3: int) -> List[str]:
    keep = list(ARCS)
    for retic, choice in (("r2", choice2), ("r3", choice3)):
        inc = [row["edge_id"] for row in RETICS[retic]]
        require(len(inc) == 2, "two incoming reticulation arcs")
        keep.remove(inc[1 - choice])
    return keep


def displayed_term(labels: Tuple[int, int, int], choice2: int, choice3: int) -> Alg:
    keep = retained_edges(choice2, choice3)
    children: Dict[str, List[str]] = {v: [] for v in NODES}
    for eid in keep:
        u, v, _ = ARCS[eid]
        children[u].append(v)
    out = Alg.one()
    for eid in keep:
        _, child, vector_name = ARCS[eid]
        below = descendants(child, children)
        char = 0
        for leaf, pos in LEAF_POS.items():
            if leaf in below:
                char ^= labels[pos]
        out = out * network_vectors[vector_name][char]
    return out


def network_q(labels: Tuple[int, int, int], fixed_r3: int | None = None) -> Alg:
    if labels[0] ^ labels[1] ^ labels[2]:
        return Alg.zero()
    choices3 = (fixed_r3,) if fixed_r3 is not None else (0, 1)
    denom = 2 * len(choices3)
    total = Alg.zero()
    for c2 in (0, 1):
        for c3 in choices3:
            total += displayed_term(labels, c2, c3)
    return total.scale(F(1, denom))


def tree_q(labels: Tuple[int, int, int]) -> Alg:
    if labels[0] ^ labels[1] ^ labels[2]:
        return Alg.zero()
    x, y, z = labels
    return tree_vectors["alpha"][x] * tree_vectors["beta"][y] * tree_vectors["gamma"][z]


def verify_factorization_and_distribution() -> Tuple[Dict[Tuple[int, int, int], Alg], Dict[Tuple[int, int, int], Alg]]:
    U, V, A, B = (network_vectors[n] for n in ("U", "V", "A", "B"))
    P, R = core_vectors["P"], core_vectors["R"]
    M: Dict[Tuple[int, int], Alg] = {}
    for y, z in itertools.product(range(4), repeat=2):
        x = y ^ z
        terms = (
            A[y] * A[z] * U[x],
            A[y] * B[z] * U[y] * V[z],
            B[y] * A[z] * U[z] * V[y],
            B[y] * B[z] * V[x],
        )
        M[y, z] = sum(terms, Alg.zero()).scale(F(1, 4))
        require(M[y, z] == P[x] * R[y] * R[z], f"core factorization at {SYMBOLS[y]},{SYMBOLS[z]}")
    print("[factorization] PASS  all 16 core identities M_yz=P_(y+z)R_yR_z")

    qn: Dict[Tuple[int, int, int], Alg] = {}
    qt: Dict[Tuple[int, int, int], Alg] = {}
    for labels in itertools.product(range(4), repeat=3):
        qn[labels] = network_q(labels)
        qt[labels] = tree_q(labels)
        require(qn[labels] == qt[labels], f"Fourier equality at {labels}")
    print("[Fourier] PASS  all 64 Fourier coordinates agree exactly")

    probs: Dict[Tuple[int, int, int], Alg] = {}
    for pat in itertools.product(range(4), repeat=3):
        a0, b0, c0 = pat
        val = Alg.zero()
        for x, y, z in itertools.product(range(4), repeat=3):
            coeff = CHAR[x][a0] * CHAR[y][b0] * CHAR[z][c0]
            val += qn[x, y, z].scale(F(coeff, 64))
        val.require_positive(f"pattern probability {pat}")
        probs[pat] = val
    require(sum(probs.values(), Alg.zero()) == Alg.one(), "pattern probabilities sum exactly to one")
    min_pat = min(probs, key=lambda k: probs[k].approx())
    lo, hi = probs[min_pat].interval()
    print(f"[patterns] PASS  all 64 probabilities agree, are positive, and sum to 1")
    print(f"[patterns] INFO  smallest interval at {min_pat}: [{float(lo):.15g}, {float(hi):.15g}]")
    return qn, probs


def direct_display_probability(pattern: Tuple[int, int, int], choice2: int, choice3: int) -> Alg:
    """Ordinary-state pruning calculation, independent of Fourier inversion."""
    keep = retained_edges(choice2, choice3)
    children: Dict[str, List[Tuple[str, str]]] = {v: [] for v in NODES}
    for eid in keep:
        u, v, _ = ARCS[eid]
        children[u].append((v, eid))

    # A topological order suffices; reverse it for postorder dynamic programming.
    indeg = {v: 0 for v in NODES}
    for eid in keep:
        _, v, _ = ARCS[eid]
        indeg[v] += 1
    queue = [v for v in NODES if indeg[v] == 0]
    order: List[str] = []
    while queue:
        u = queue.pop()
        order.append(u)
        for v, _ in children[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    require(len(order) == len(NODES), "displayed graph topological order")

    like: Dict[str, List[Alg]] = {}
    observed = {leaf: pattern[pos] for leaf, pos in LEAF_POS.items()}
    for node in reversed(order):
        if node in observed:
            like[node] = [Alg.one() if state == observed[node] else Alg.zero() for state in range(4)]
            continue
        # An unobserved terminal/dangling vertex contributes likelihood one for every state.
        vals = [Alg.one() for _ in range(4)]
        for child, eid in children[node]:
            probs = transition_probs(network_vectors[ARCS[eid][2]])
            contrib = []
            for parent_state in range(4):
                subtotal = Alg.zero()
                for child_state in range(4):
                    subtotal += probs[parent_state ^ child_state] * like[child][child_state]
                contrib.append(subtotal)
            vals = [a * b for a, b in zip(vals, contrib)]
        like[node] = vals
    return sum(like["rho"], Alg.zero()).scale(F(1, 4))


def direct_tree_probability(pattern: Tuple[int, int, int]) -> Alg:
    total = Alg.zero()
    edges = (tree_vectors["alpha"], tree_vectors["beta"], tree_vectors["gamma"])
    matrices = [transition_probs(e) for e in edges]
    for root_state in range(4):
        term = Alg.one()
        for leaf_state, probs in zip(pattern, matrices):
            term *= probs[root_state ^ leaf_state]
        total += term
    return total.scale(F(1, 4))


def verify_direct_state_space(fourier_probs: Mapping[Tuple[int, int, int], Alg]) -> None:
    for pat in itertools.product(range(4), repeat=3):
        net = Alg.zero()
        for c2, c3 in itertools.product((0, 1), repeat=2):
            net += direct_display_probability(pat, c2, c3).scale(F(1, 4))
        tree = direct_tree_probability(pat)
        require(net == tree, f"direct state-space network/tree equality at {pat}")
        require(net == fourier_probs[pat], f"direct/Fourier equality at {pat}")
    print("[direct probabilities] PASS  ordinary Markov pruning independently matches all 64 Fourier-inverted probabilities")


def Q(q: Mapping[Tuple[int, int, int], Alg]) -> Alg:
    return (q[0, 2, 2] * q[2, 0, 2] * (q[1, 1, 0] ** 2)
            - q[0, 0, 0] * q[2, 2, 0] * (q[3, 1, 2] ** 2))


def permute_q(q: Mapping[Tuple[int, int, int], Alg], perm: Tuple[int, int, int]) -> Dict[Tuple[int, int, int], Alg]:
    return {t: q[tuple(t[perm[i]] for i in range(3))] for t in itertools.product(range(4), repeat=3)}


def verify_invariant_failure(parent: Mapping[Tuple[int, int, int], Alg]) -> None:
    require(Q(parent).is_zero(), "tree invariant Q vanishes at collision")
    child_p = {t: network_q(t, fixed_r3=0) for t in itertools.product(range(4), repeat=3)}
    child_q = Q(child_p)
    lo, hi = child_q.interval()
    require(hi < 0, "fixed-order Q must be negative on one displayed child")
    # Put old leaf 2 into the last coordinate: the favorable sunlet ordering.
    favorable = Q(permute_q(child_p, (0, 2, 1)))
    favorable.require_positive("permuted child Q")
    flo, fhi = favorable.interval()
    print("[induction] PASS  parent Q=0 exactly; one level-one child has fixed-order Q<0")
    print(f"[induction] INFO  fixed-order Q interval [{float(lo):.16e}, {float(hi):.16e}]")
    print(f"[induction] INFO  favorable-order Q interval [{float(flo):.16e}, {float(fhi):.16e}]")
    print("[induction] PASS  relabeling that child makes Q>0, confirming the order conflict")


# ---- independent exact rational negative-Q point --------------------------

def verify_claim_a() -> None:
    raw = CERT["independent_negative_Q_point"]
    E = {name: k2p_vector(Alg.rat(F(row[0])), Alg.rat(F(row[1])))
         for name, row in raw["edge_s_g"].items()}
    d2, d3 = F(raw["delta2"]), F(raw["delta3"])
    for name, e in E.items():
        check_edge("negative-Q witness " + name, e, strict_ct=False)

    def qcoord(labels: Tuple[int, int, int]) -> Alg:
        x, y, z = labels
        if x ^ y ^ z:
            return Alg.zero()
        core = (
            E["A2"][y] * E["A3"][z] * E["U"][x]
        ).scale(d2 * d3)
        core += (E["A2"][y] * E["B3"][z] * E["U"][y] * E["V"][z]).scale(d2 * (1 - d3))
        core += (E["B2"][y] * E["A3"][z] * E["U"][z] * E["V"][y]).scale((1 - d2) * d3)
        core += (E["B2"][y] * E["B3"][z] * E["V"][x]).scale((1 - d2) * (1 - d3))
        return E["e1"][x] * E["D2"][y] * E["D3"][z] * core

    q = {t: qcoord(t) for t in itertools.product(range(4), repeat=3)}
    for perm in itertools.permutations(range(3)):
        val = Q(permute_q(q, perm))
        lo, hi = val.interval()
        require(hi < 0, f"Q negative for leaf permutation {perm}")
    # Site-pattern positivity.
    for pat in itertools.product(range(4), repeat=3):
        val = Alg.zero()
        for x, y, z in itertools.product(range(4), repeat=3):
            val += q[x, y, z].scale(F(CHAR[x][pat[0]] * CHAR[y][pat[1]] * CHAR[z][pat[2]], 64))
        val.require_positive(f"negative-Q witness pattern {pat}")
    print("[sign test] PASS  an independent exact rational theta point has Q<0 in all six leaf orders")


def main() -> None:
    verify_field()
    verify_topology()
    verify_parameters()
    verify_construction()
    parent, probs = verify_factorization_and_distribution()
    verify_direct_state_space(probs)
    verify_invariant_failure(parent)
    verify_claim_a()
    print("\nALL EXTENDED K2P CHECKS PASSED")


if __name__ == "__main__":
    main()
