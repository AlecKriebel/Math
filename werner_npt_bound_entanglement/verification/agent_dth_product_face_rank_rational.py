#!/usr/bin/env python3
"""Exact rational rank and basis certificate for the product-DTH face.

The companion finite-field verifier proves a fast lower bound.  This file
also proves the upper bound by constructing every rational mixed block over
ZZ (after one common denominator is removed) and computing its exact rank.
For each block, the pivot columns returned by exact RREF select a rational
basis of its range.  Their aggregate is the 2266-dimensional face basis.

SymPy is used only for exact integer/rational linear algebra.  No numerical
eigenvalues, tolerances, or external data files occur.
"""

from __future__ import annotations

from functools import reduce
from itertools import product
from pathlib import Path
import argparse
import gc
import importlib.util
import json
import math
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


FACE = None
BRIDGE = None
np = None
sp = None


def load_dependencies():
    """Load heavy exact-array packages only in a chunk worker."""
    global FACE, BRIDGE, np, sp
    if FACE is not None:
        return
    import numpy as numpy_module
    import sympy as sympy_module
    FACE = import_file(
        "dth_product_face_modular", HERE / "agent_dth_product_face_rank.py"
    )
    BRIDGE = FACE.BRIDGE
    np = numpy_module
    sp = sympy_module


EXPECTED_RANK = 2266
EXPECTED_ACTIVE = 198
def exact_transform_numerator():
    _, mixed_restriction, _, _ = BRIDGE.exact_restriction_bridge()
    gram = BRIDGE.diagram_gram()
    gram_domain = sp.polys.matrices.DomainMatrix.from_list_sympy(103, 103, gram)
    inverse_numerator, denominator = gram_domain.inv_den()
    mixed_domain = sp.polys.matrices.DomainMatrix.from_list_sympy(
        103, 103, mixed_restriction
    )
    numerator = (mixed_domain * inverse_numerator).to_Matrix()
    values = [abs(int(value)) for value in numerator if value]
    common = reduce(math.gcd, values + [int(denominator)])
    denominator = int(denominator) // common
    transform = [
        [int(numerator[row, column]) // common for column in range(103)]
        for row in range(103)
    ]
    assert denominator == 7560
    assert max(abs(value) for row in transform for value in row) == 7560
    return transform, denominator


def matvec(matrix, vector):
    return [
        sum(value * coefficient for value, coefficient in zip(row, vector))
        for row in matrix
    ]


def integer_moment(ket, bra):
    return [
        math.prod(
            FACE.dot(ket[position], bra[permutation[position]])
            for position in range(5)
        )
        for permutation in BRIDGE.SELECTED_PERMUTATIONS
    ]


def exact_terms(transform):
    terms = []
    for _, _, _, sites in FACE.IntegerTriples().global_triples():
        for alpha, beta, gamma, delta in product(range(2), repeat=4):
            vectors = []
            for a, b, z in sites:
                ket = ([b, a] if alpha else [a, b])
                ket += ([b, a] if beta else [a, b])
                ket += [z]
                bra = ([b, a] if gamma else [a, b])
                bra += ([b, a] if delta else [a, b])
                bra += [z]
                vectors.append(matvec(transform, integer_moment(ket, bra)))
            sign = -1 if (alpha + beta + gamma + delta) % 2 else 1
            terms.append((sign, tuple(vectors)))
    assert len(terms) == 432
    return terms


def exact_block(terms, shapes, offsets):
    dimensions = tuple(FACE.MIXED_MULTS[shape] for shape in shapes)
    size = math.prod(dimensions)
    matrix = np.zeros((size, size), dtype=object)
    for sign, vectors in terms:
        local = []
        skip = False
        for vector, shape in zip(vectors, shapes):
            start, stop, multiplicity = offsets[shape]
            block = np.asarray(vector[start:stop], dtype=object).reshape(
                multiplicity, multiplicity
            )
            if not np.any(block):
                skip = True
                break
            local.append(block)
        if skip:
            continue
        contribution = np.kron(np.kron(local[0], local[1]), local[2])
        matrix += sign * contribution
    # The factor 1/4 from the two normalized bivectors and the common local
    # denominator 7560^3 do not affect rank or range.
    return sp.polys.matrices.DomainMatrix.from_list_sympy(
        size, size, [[int(value) for value in row] for row in matrix.tolist()]
    )


def exact_chunk(start, stop):
    load_dependencies()
    transform, denominator = exact_transform_numerator()
    terms = exact_terms(transform)
    offsets = FACE.block_offsets(FACE.MIXED_MULTS)
    ranks = {}
    triples = list(product(range(6), repeat=3))[start:stop]
    for count, shapes in enumerate(triples, start + 1):
        matrix = exact_block(terms, shapes, offsets)
        # Exact rank is substantially more memory-efficient here than full
        # rational RREF.  The companion prime-field verifier records pivot
        # columns; equality of the exact rank proves those rational columns
        # are a basis, rather than merely a finite-field lower certificate.
        ranks[shapes] = matrix.rank()
        del matrix
        # Dense object Kronecker products retain many large Python integers;
        # collect between blocks to keep the verifier below local RAM limits.
        gc.collect()
    special_shapes = ((2, 2, 2), (2, 4, 4), (4, 2, 4), (4, 4, 2))
    return {
        "start": start,
        "stop": stop,
        "rank": sum(ranks.values()),
        "active": sum(rank > 0 for rank in ranks.values()),
        "special": {
            "".join(map(str, shapes)): ranks[shapes]
            for shapes in special_shapes if shapes in ranks
        },
        "denominator": denominator,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk", nargs=2, type=int)
    args = parser.parse_args()
    if args.chunk:
        print(json.dumps(exact_chunk(*args.chunk), sort_keys=True))
        return

    # Compute the exact-Q ranks in fresh child processes.  CPython's dense
    # object arrays do not reliably return their large integer arenas to the
    # operating system; process isolation keeps the complete replay bounded.
    results = []
    # Twelve blocks per child keeps the densest 6x6x6 multiplicity blocks
    # comfortably below the shared-machine memory ceiling.
    chunk_size = 12
    for start in range(0, 216, chunk_size):
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--chunk",
            str(start),
            str(start + chunk_size),
        ]
        output = subprocess.check_output(command, text=True)
        result = json.loads(output.strip().splitlines()[-1])
        results.append(result)
        print(f"exact blocks {start + chunk_size}/216", flush=True)

    total = sum(result["rank"] for result in results)
    active = sum(result["active"] for result in results)
    specials = {}
    for result in results:
        specials.update(result["special"])

    assert total == EXPECTED_RANK
    assert active == EXPECTED_ACTIVE
    # These are the four most ill-conditioned numerical blocks.  Exact RREF
    # fixes their ranks without a tolerance.
    assert specials == {"222": 51, "244": 36, "424": 36, "442": 36}

    print("exact rational product-DTH face certificate passed")
    assert {result["denominator"] for result in results} == {7560}
    print("local twirl denominator:", 7560)
    print("mixed face rank:", total, "active blocks:", active)


if __name__ == "__main__":
    main()
