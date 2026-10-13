"""Independent exact checks for sparse multiplicity through exponent digits.

This is a research-route check, not a uniform implementation of upstream dense
factoring. It never enumerates a field in the algorithm. Enumeration occurs
only in exhaustive small-input test generation. No third-party packages.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import finite_fields as ff


class Quotient:
    """K[X]/g for a promised monic irreducible g, with little-endian elements."""

    def __init__(self, K, g):
        self.K, self.g = K, g
        self.p = K.p
        self.zero, self.one = (), (K.one,)
        self.nodes = self.inspected_coefficients = 0

    def add(self, a, b):
        return ff.add(self.K, a, b)

    def mul(self, a, b):
        return ff.divmod_poly(self.K, ff.mul(self.K, a, b), self.g)[1]

    def scale_prime(self, a, r):
        return ff.scale(self.K, a, self.K.element(r))

    def constant(self, c):
        return () if c == self.K.zero else (c,)

    def pow(self, a, n):
        v = self.one
        while n:
            if n & 1:
                v = self.mul(v, a)
            n >>= 1
            if n:
                a = self.mul(a, a)
        return v


def initial_term(E, terms):
    """Initial Y-term of sum w*(1+Y)**e in characteristic p.

    Exponents are distinct nonnegative integers, all weights are nonzero. An
    iterative postorder trie avoids a Python recursion limit depending on N.
    """
    stack = [(0, terms, None)]
    results = {}
    next_node = 1
    while stack:
        node_id, node_terms, children = stack.pop()
        if children is None:
            E.nodes += 1
            if len(node_terms) == 1:
                # Every (1+Y)^e has initial order zero and initial coefficient 1.
                results[node_id] = (0, node_terms[0][1])
                continue
            buckets = {}
            for exponent, weight in node_terms:
                q, r = divmod(exponent, E.p)
                buckets.setdefault(r, []).append((q, weight))
            children = []
            for r, child_terms in sorted(buckets.items()):
                child_id = next_node
                next_node += 1
                children.append((r, child_id))
            stack.append((node_id, node_terms, children))
            for (r, child_id), child_terms in zip(children, sorted(buckets.items())):
                stack.append((child_id, child_terms[1], None))
            continue
        v = min(results[child_id][0] for _, child_id in children)
        active = [(r, results[child_id][1]) for r, child_id in children
                  if results[child_id][0] == v]
        # Binomial column recurrence; j < len(active) <= p, so j! is invertible.
        binomials = [1] * len(active)
        for j in range(len(active)):
            c = E.zero
            for k, (r, a) in enumerate(active):
                c = E.add(c, E.scale_prime(a, binomials[k]))
            E.inspected_coefficients += 1
            if c != E.zero:
                results[node_id] = (E.p * v + j, c)
                break
            if j + 1 == len(active):
                continue
            denominator_inverse = pow(j + 1, -1, E.p)
            for k, (r, _) in enumerate(active):
                binomials[k] = binomials[k] * (r - j) * denominator_inverse % E.p
        else:
            raise AssertionError("Vandermonde initial-term guarantee failed")
    return results[0]


def multiplicity(K, sparse, g):
    E = Quotient(K, g)
    alpha = ff.divmod_poly(K, (K.zero, K.one), g)[1]
    if not alpha:
        return min(e for e, _ in sparse), E
    terms = [(e, E.mul(E.constant(c), E.pow(alpha, e))) for e, c in sparse]
    return initial_term(E, terms)[0], E


def dense_reference(K, sparse, g):
    f = [K.zero] * (max(e for e, _ in sparse) + 1)
    for e, c in sparse:
        f[e] = c
    f = ff.trim(K, f)
    v = 0
    while f:
        q, r = ff.divmod_poly(K, f, g)
        if r:
            return v
        v += 1
        f = q
    raise AssertionError("nonzero test polynomial unexpectedly vanished")


def main():
    fields = [(2, (0, 1), 9), (3, (0, 1), 5), (5, (0, 1), 3),
              (2, (1, 1, 1), 4), (2, (1, 1, 0, 1), 3)]
    checks = 0
    max_nodes = 0
    for p, h, maximum_degree in fields:
        K = ff.FiniteField(p, h)
        elements = list(K.elements_for_testing())
        for degree in range(maximum_degree + 1):
            for coefficients in itertools.product(elements, repeat=degree):
                f = tuple(coefficients) + (K.one,)
                sparse = [(e, c) for e, c in enumerate(f) if c != K.zero]
                for alpha in elements:
                    g = (K.neg(alpha), K.one)
                    got, E = multiplicity(K, sparse, g)
                    want = dense_reference(K, sparse, g)
                    if got != want:
                        raise AssertionError((p, h, sparse, g, got, want))
                    checks += 1
                    max_nodes = max(max_nodes, E.nodes)
    # Irreducible degree-two roots over base F_2 and F_3, not only known scalars.
    for p, g_raw, maximum_degree in [(2, (1, 1, 1), 10), (3, (1, 0, 1), 6)]:
        K = ff.FiniteField(p, (0, 1))
        g = K.poly(g_raw)
        assert ff.irreducible(K, g)
        for degree in range(maximum_degree + 1):
            for coefficients in itertools.product(range(p), repeat=degree):
                sparse = [(e, K.element(c)) for e, c in enumerate(coefficients + (1,)) if c]
                got, E = multiplicity(K, sparse, g)
                assert got == dense_reference(K, sparse, g)
                checks += 1
                max_nodes = max(max_nodes, E.nodes)
    huge = []
    for p, h, k in [(2, (0, 1), 2048), (3, (0, 1), 127),
                    (2, (1, 1, 1), 73), (2, (1, 1, 0, 1), 91),
                    (2, (1, 1, 0, 0, 1), 71),
                    (1000000007, (0, 1), 11)]:
        K = ff.FiniteField(p, h)
        alpha = K.one if K.m == 1 else K.basis()[1]
        pk = p ** k
        ak = K.pow(alpha, pk)
        # (X-alpha)**(p**k+1) = (X**pk-alpha**pk)*(X-alpha).
        sparse = [(0, K.mul(ak, alpha)), (1, K.neg(ak)),
                  (pk, K.neg(alpha)), (pk + 1, K.one)]
        g = (K.neg(alpha), K.one)
        got, E = multiplicity(K, sparse, g)
        assert got == pk + 1
        huge.append({"p": p, "m": K.m, "exponent_digit_depth": k + 1,
                     "multiplicity_bits": got.bit_length(), "trie_nodes": E.nodes,
                     "coefficient_checks": E.inspected_coefficients,
                     "expected_multiplicity_expression": f"{p}^{k}+1"})
    divisible = []
    K = ff.FiniteField(3, (0, 1))
    for k in (1, 83, 257):
        pk = 3 ** k
        # (X-1)^(2*3^k) = (X^pk-1)^2, including huge p-divisible orders.
        sparse = [(0, K.one), (pk, K.one), (2 * pk, K.one)]
        got, E = multiplicity(K, sparse, (K.element(-1), K.one))
        assert got == 2 * pk
        divisible.append({"p": 3, "multiplicity_expression": f"2*3^{k}",
                          "trie_nodes": E.nodes,
                          "coefficient_checks": E.inspected_coefficients})
    formal = []
    for p, g_raw, k in ((2, (1, 1, 1), 137), (3, (1, 0, 1), 83)):
        K = ff.FiniteField(p, (0, 1))
        g = K.poly(g_raw)
        pk = p ** k
        sparse_map = {}
        for i, ci in enumerate(g):
            for j, cj in enumerate(g):
                exponent = i * pk + j
                c = K.mul(K.pow(ci, pk), cj)
                sparse_map[exponent] = K.add(sparse_map.get(exponent, K.zero), c)
        sparse = [(e, c) for e, c in sorted(sparse_map.items()) if c != K.zero]
        got, E = multiplicity(K, sparse, g)
        assert got == pk + 1
        formal.append({"p": p, "g": list(g_raw), "sparse_terms": len(sparse),
                       "multiplicity_expression": f"{p}^{k}+1", "trie_nodes": E.nodes,
                       "coefficient_checks": E.inspected_coefficients})
    path = Path(__file__).resolve()
    output = {"test": "independent sparse exponent-digit multiplicity",
              "exhaustive_dense_comparisons": checks,
              "maximum_small_trie_nodes": max_nodes,
              "huge_binary_multiplicity_examples": huge,
              "huge_p_divisible_multiplicity_examples": divisible,
              "formal_irreducible_root_examples": formal,
              "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "base_arithmetic_sha256": hashlib.sha256(Path(ff.__file__).read_bytes()).hexdigest(),
              "scope": "Exact algorithm vs dense repeated division; scalar and irreducible roots. "
                       "Does not implement the uniform dense factorization input theorem."}
    destination = path.with_name("sparse_extension_independent_checks.json")
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
