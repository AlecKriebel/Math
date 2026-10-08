#!/usr/bin/env python3
"""Exact finite checks supplementing the independent five-approach audit."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import os
import sys
import json


MUTANT = None

def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def require_readonly():
    require(os.getuid() != 0 and os.geteuid() != 0, "read-only verification requires a real nonroot process")
    source = Path(__file__).resolve()
    require(not os.access(source, os.W_OK), "checker input is writable")
    require(not os.access(source.parent, os.W_OK), "checker input directory is writable")
    probe = source.parent / (".audit-write-probe-" + str(os.getpid()))
    try:
        with probe.open("x"):
            pass
    except PermissionError:
        return
    else:
        probe.unlink()
        raise RuntimeError("actual input-directory write probe unexpectedly succeeded")


def emit_result(result, output):
    payload = json.dumps(result, indent=2) + "\n"
    if output is None:
        sys.stdout.write(payload)
        return
    destination = Path(output)
    require(destination.is_absolute(), "output must be an absolute external destination")
    parent = destination.parent.resolve(strict=True)
    destination = parent / destination.name
    source_directory = Path(__file__).resolve().parent
    require(not destination.is_relative_to(source_directory), "output must be outside the checker input directory")
    require(not destination.exists() and not destination.is_symlink(), "output destination already exists")
    with destination.open("x") as stream:
        stream.write(payload)


MUTATIONS = ['drop-free-closed-color', 'ignore-conflicting-colors', 'drop-new-closed-component', 'wrong-euler-weight', 'wrong-gram-power', 'commutative-dihedral-product', 'wrong-fourier-sign', 'uniform-component-normalization']

def partitions(size):
    if size == 0:
        return [()]
    result = []
    for old in partitions(size - 1):
        for label in range(max(old, default=-1) + 2):
            result.append(old + (label,))
    return result


def coefficient(n, partition, closed, incoming, outgoing, chi, q):
    block_colors = {}
    for block, color in zip(partition, incoming + outgoing):
        if block in block_colors and block_colors[block] != color:
            return Q(1) if MUTANT == "ignore-conflicting-colors" else Q(0)
        block_colors[block] = color
    return Q(n) ** (0 if MUTANT == "drop-free-closed-color" else closed) * q ** (chi + (1 if MUTANT == "wrong-euler-weight" else 0))


def compose(p, middle, r, left, lc, right, rc):
    """Glue component partitions; explicitly retain new closed components."""
    lb = max(left, default=-1) + 1
    rb = max(right, default=-1) + 1
    offset = lb + lc
    parent = list(range(lb + lc + rb + rc))

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        parent[root(x)] = root(y)

    for j in range(middle):
        union(left[p + j], offset + right[j])
    external = [root(left[j]) for j in range(p)]
    external += [root(offset + right[middle + j]) for j in range(r)]
    names = {}
    labels = tuple(names.setdefault(x, len(names)) for x in external)
    closed = len({root(x) for x in parent} - set(external))
    return labels, (0 if MUTANT == "drop-new-closed-component" else closed)


def d8_multiply(x, y):
    i, j = x
    k, ell = y
    return ((i + (1 if MUTANT == "commutative-dihedral-product" else (-1) ** j) * k) % 4, (j + ell) % 2)


def gauss_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def gauss_multiply(x, y):
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def main():
    composition_cases = 0
    q = Q(1, 2)
    for n in (1, 2, 3):
        for p, middle, r in product(range(3), repeat=3):
            ins = list(product(range(n), repeat=p))
            seams = list(product(range(n), repeat=middle))
            outs = list(product(range(n), repeat=r))
            for left, right in product(partitions(p + middle), partitions(middle + r)):
                for lc, rc in product(range(2), repeat=2):
                    glued, closed = compose(p, middle, r, left, lc, right, rc)
                    xchi, ychi = p - middle, middle - r
                    for u, v in product(ins, outs):
                        composed = sum((
                            coefficient(n, left, lc, u, seam, xchi, q)
                            * coefficient(n, right, rc, seam, v, ychi, q)
                            for seam in seams
                        ), Q(0))
                        direct = coefficient(n, glued, closed, u, v, xchi + ychi, q)
                        require(composed == direct, ('invariant failed: composed == direct', (n, p, middle, r, left, right, lc, rc, u, v)))
                    composition_cases += 1

    identity_entries = 0
    for n in range(1, 5):
        for size in range(4):
            partition = tuple(range(size)) * 2
            for u, v in product(product(range(n), repeat=size), repeat=2):
                require(coefficient(n, partition, 0, u, v, 0, q) == int(u == v), 'invariant failed: coefficient(n, partition, 0, u, v, 0, q) == int(u == v)')
                identity_entries += 1
    # Birth followed by death creates a freely colored closed component.
    require(compose(0, 1, 0, (0,), 0, (0,), 0) == ((), 1), 'invariant failed: compose(0, 1, 0, (0,), 0, (0,), 0) == ((), 1)')

    gram_cases = 0
    for n, q in product(map(Q, (-2, -1, Q(1, 2), 1, 2, 4, 32)), map(Q, (-2, -1, Q(1, 2), 1, 2))):
        a, b, c = n*n*q**(3 if MUTANT == "wrong-gram-power" else 4), n*q**2, n
        det = a*c-b*b
        require(det == n*n*(n-1)*q**4, 'invariant failed: det == n*n*(n-1)*q**4')
        require((det == 0) == (n == 1), 'invariant failed: (det == 0) == (n == 1)')
        gram_cases += 1

    group = list(product(range(4), range(2)))
    require(all(d8_multiply(d8_multiply(x,y),z) == d8_multiply(x,d8_multiply(y,z))
               for x,y,z in product(group, repeat=3)), 'invariant failed: all(d8_multiply(d8_multiply(x,y),z) == d8_multiply(x,d8_multiply(y,z)) for x,y,z in product(group, repeat=3))')
    r, s = (1,0), (0,1)
    require(d8_multiply(r,s) == (1,1), 'invariant failed: d8_multiply(r,s) == (1,1)')
    require(d8_multiply(s,r) == (3,1), 'invariant failed: d8_multiply(s,r) == (3,1)')
    require(d8_multiply(r,s) != d8_multiply(s,r), 'invariant failed: d8_multiply(r,s) != d8_multiply(s,r)')
    require(8 * 2**2 == 32, 'invariant failed: 8 * 2**2 == 32')

    # C4 Fourier inversion in the exact Gaussian rationals.
    roots = [(Q(1),Q(0)), (Q(0),Q(1)), (Q(-1),Q(0)), (Q(0),Q(-1))]
    fourier_cases = 0
    for multiplicities in product(range(4), repeat=4):
        traces = []
        for j in range(4):
            value = (Q(0),Q(0))
            for ell, multiplicity in enumerate(multiplicities):
                value = gauss_add(value, gauss_multiply((Q(multiplicity),Q(0)), roots[(ell*j)%4]))
            traces.append(value)
        recovered = []
        for ell in range(4):
            value = (Q(0),Q(0))
            for j in range(4):
                value = gauss_add(value,gauss_multiply(roots[((ell*j) if MUTANT == "wrong-fourier-sign" else (-ell*j))%4],traces[j]))
            recovered.append((value[0]/4,value[1]/4))
        require(recovered == [(Q(x),Q(0)) for x in multiplicities], 'invariant failed: recovered == [(Q(x),Q(0)) for x in multiplicities]')
        fourier_cases += 1
    require(((Q(1)+3)/2,(Q(1)-3)/2) == (2,-1), 'invariant failed: ((Q(1)+3)/2,(Q(1)-3)/2) == (2,-1)')

    # Disconnected-Y regression: two components exchanged by an involution.
    # The mapping-torus component counts are 2 and 1. Component normalization
    # lambda=1/n therefore gives (n**2*lambda**2,n*lambda)=(1,1).
    # In the MMT C2 example n**3=4, so the naive common-lambda Fourier ratio
    # (n+1)/(n-1) is irrational, as proved in the audit. This arithmetic sample
    # checks the differing exponents without approximating that algebraic n.
    for n in (Q(1,2),Q(2),Q(4),Q(32)):
        lam = 1/n
        require((n*n*lam*(1 if MUTANT == "uniform-component-normalization" else lam),n*lam) == (1,1), 'invariant failed: (n*n*lam*lam,n*lam) == (1,1)')
        if n != 1:
            require((n*n*lam,n*lam) != (1,1), 'invariant failed: (n*n*lam,n*lam) != (1,1)')

    result = {
        "status":"PASS",
        "arithmetic":"Integers, rational numbers, and exact Gaussian rational pairs",
        "component_coloring_composition_cases":composition_cases,
        "identity_matrix_entries":identity_entries,
        "gram_determinant_cases":gram_cases,
        "dihedral_associativity_cases":len(group)**3,
        "dihedral_noncommuting_products":[list(d8_multiply(r,s)),list(d8_multiply(s,r))],
        "C4_fourier_inversion_cases":fourier_cases,
        "disconnected_mapping_torus_normalization_regression":"PASS",
        "limitations":[
            "Finite component-partition tests supplement the proof of the coloring bijection.",
            "Assigned Euler integers are formal tests, not claims that every tested combination is a realized bordism.",
            "No finite computation proves all TQFT axioms or source theorem hypotheses.",
            "The irrational disconnected-Y example is proved symbolically in the audit."
        ]
    }
    return result

def cli():
    global MUTANT
    parser = argparse.ArgumentParser(description="Exact source-free audit checks; stdout by default")
    parser.add_argument("--output", help="Optional absolute new file outside the input directory")
    parser.add_argument("--require-readonly", action="store_true", help="Require nonroot execution and actual nonwritable input")
    parser.add_argument("--mutant", choices=MUTATIONS, help="Deliberate semantic corruption; every choice must fail a guard")
    args = parser.parse_args()
    MUTANT = args.mutant
    if args.require_readonly:
        require_readonly()
    emit_result(main(), args.output)


if __name__ == "__main__":
    cli()
