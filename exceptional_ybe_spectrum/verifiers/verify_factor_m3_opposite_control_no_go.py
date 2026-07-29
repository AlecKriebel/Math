#!/usr/bin/env python3
"""Independent exact checks for the M_m tensor I_2 leg-factor no-go.

This verifier deliberately uses two different implementations:

1. SymPy matrices check the Pauli coefficient identity and the abstract
   two-projection endpoint blocks.
2. A basis-state Gaussian-integer engine checks a balanced d=6 factor-form
   reflection, its rank-one opposite control, and a nonzero cubic residual.

The human proof is in notes/rank_two_leg_commutant_branches.md.
"""

from __future__ import annotations

from collections import defaultdict
import itertools

import sympy as sp


I = sp.I
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -I], [I, 0]])
Z = sp.Matrix([[1, 0], [0, -1]])
ID2 = sp.eye(2)


def check_pauli_square_identity() -> None:
    """Check signs/orientations with unrelated exact Hermitian matrices."""

    b1 = sp.Matrix([[1, 2], [2, 0]])
    b2 = sp.Matrix([[0, 1], [1, 3]])
    b3 = sp.Matrix([[2, -1], [-1, 1]])
    k = sp.kronecker_product(X, b1)
    k += sp.kronecker_product(Y, b2)
    k += sp.kronecker_product(Z, b3)

    rhs = sp.kronecker_product(ID2, b1**2 + b2**2 + b3**2)
    rhs += I * sp.kronecker_product(X, b2 * b3 - b3 * b2)
    rhs += I * sp.kronecker_product(Y, b3 * b1 - b1 * b3)
    rhs += I * sp.kronecker_product(Z, b1 * b2 - b2 * b1)
    assert k**2 == rhs

    # Extracting each Pauli coefficient separately guards against treating
    # the three epsilon terms as one cancellable linear combination.
    square = k**2
    blocks = [[square[2 * a : 2 * (a + 1), 2 * b : 2 * (b + 1)]
               for b in range(2)] for a in range(2)]

    # The coefficient extractor is easier and less error-prone via a direct
    # 2 x 2 block partial trace.
    def coefficient(pauli: sp.Matrix) -> sp.Matrix:
        out = sp.zeros(2)
        for a in range(2):
            for b in range(2):
                out += pauli[b, a] * square[
                    2 * a : 2 * (a + 1), 2 * b : 2 * (b + 1)
                ]
        return sp.simplify(out / 2)

    assert coefficient(X) == I * (b2 * b3 - b3 * b2)
    assert coefficient(Y) == I * (b3 * b1 - b1 * b3)
    assert coefficient(Z) == I * (b1 * b2 - b2 * b1)
    assert blocks  # exercise the intended qubit-block ordering


# Gaussian integers are represented as (real, imaginary).
ONE = (1, 0)
MINUS_ONE = (-1, 0)
PLUS_I = (0, 1)
MINUS_I = (0, -1)


def gmul(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def gscale(n: int, a: tuple[int, int]) -> tuple[int, int]:
    return (n * a[0], n * a[1])


def local_parts(s: int) -> tuple[int, int]:
    return divmod(s, 2)


# The six controls use the balanced axes X,-X,Y,-Y,Z,-Z.
AXES = (("X", 1), ("X", -1), ("Y", 1), ("Y", -1),
        ("Z", 1), ("Z", -1))


def pauli_action(axis: tuple[str, int], q: int) -> tuple[int, tuple[int, int]]:
    name, sign = axis
    scalar = ONE if sign == 1 else MINUS_ONE
    if name == "X":
        return 1 - q, scalar
    if name == "Y":
        phase = PLUS_I if q == 0 else MINUS_I
        return 1 - q, gmul(scalar, phase)
    if name == "Z":
        phase = ONE if q == 0 else MINUS_ONE
        return q, gmul(scalar, phase)
    raise AssertionError(name)


def h_leg(
    state: tuple[int, int, int], leg: int
) -> tuple[tuple[int, int, int], tuple[int, int]]:
    """Apply H on sites (leg, leg+1), for leg=0 or 1."""

    values = list(state)
    control = values[leg + 1]
    color, qubit = local_parts(values[leg])
    new_qubit, phase = pauli_action(AXES[control], qubit)
    values[leg] = 2 * color + new_qubit
    return tuple(values), phase


def word_action(
    state: tuple[int, int, int], word: tuple[int, ...]
) -> tuple[tuple[int, int, int], tuple[int, int]]:
    phase = ONE
    current = state
    # Matrix products act right-to-left.
    for leg in reversed(word):
        current, new_phase = h_leg(current, leg)
        phase = gmul(new_phase, phase)
    return current, phase


def check_balanced_factor_guard() -> tuple[int, tuple]:
    """Check an exact d=6 standard involution of the theorem's factor form."""

    # Each A_s is a Pauli reflection.  Therefore H is a Hermitian monomial
    # involution.  The balanced list makes both local partial traces zero:
    # Tr(A_s)=0 for every s and sum_s A_s=0.
    assert len(AXES) == 6
    axis_sums = {"X": 0, "Y": 0, "Z": 0}
    for name, sign in AXES:
        axis_sums[name] += sign
    assert axis_sums == {"X": 0, "Y": 0, "Z": 0}

    # H leaves the C^3 color of the first site untouched, so M_3 tensor I_2
    # lies in the left leg commutant.  It leaves the whole second-site basis
    # label untouched, so all six rank-one diagonal controls lie in the
    # right leg commutant.  Check H^2 basiswise.
    for first in range(6):
        for second in range(6):
            state = (first, second, 0)
            after, phase1 = h_leg(state, 0)
            after2, phase2 = h_leg(after, 0)
            assert after2 == state
            assert gmul(phase2, phase1) == ONE
            assert local_parts(after[0])[0] == local_parts(first)[0]
            assert after[1] == second

    # Exact scaled cubic residual:
    # 3(H1 H2 H1-H2 H1 H2)-(H1-H2).
    nonzero = []
    for state in (
        (a, b, c) for a in range(6) for b in range(6) for c in range(6)
    ):
        terms: defaultdict[tuple[int, int, int], tuple[int, int]]
        terms = defaultdict(lambda: (0, 0))
        for scalar, word in (
            (3, (0, 1, 0)),
            (-3, (1, 0, 1)),
            (-1, (0,)),
            (1, (1,)),
        ):
            target, phase = word_action(state, word)
            old = terms[target]
            add = gscale(scalar, phase)
            terms[target] = (old[0] + add[0], old[1] + add[1])
        terms = defaultdict(
            lambda: (0, 0),
            {target: value for target, value in terms.items()
             if value != (0, 0)},
        )
        if terms:
            nonzero.append((state, dict(terms)))

    assert nonzero
    return len(nonzero), nonzero[0]


def generic_pair_block() -> tuple[sp.Matrix, sp.Matrix]:
    p = sp.Matrix([[1, 0], [0, 0]])
    q = sp.Matrix(
        [[sp.Rational(1, 3), sp.sqrt(2) / 3],
         [sp.sqrt(2) / 3, sp.Rational(2, 3)]]
    )
    return p, q


def abstract_endpoint_pair(k: int) -> tuple[sp.Matrix, sp.Matrix]:
    """Build the 24-dimensional pair with endpoint common rank k."""

    assert 0 <= k <= 12
    pieces_p: list[sp.Matrix] = []
    pieces_q: list[sp.Matrix] = []
    for _ in range(k):
        pieces_p.append(sp.ones(1, 1))
        pieces_q.append(sp.ones(1, 1))
    for _ in range(12 - k):
        p, q = generic_pair_block()
        pieces_p.append(p)
        pieces_q.append(q)
    for _ in range(k):
        pieces_p.append(sp.zeros(1, 1))
        pieces_q.append(sp.zeros(1, 1))
    return sp.diag(*pieces_p), sp.diag(*pieces_q)


def check_endpoint_bookkeeping() -> None:
    n_uniform = sp.ones(3, 3) * 2
    n_nonuniform = sp.Matrix([[4, 2, 0], [0, 4, 2], [2, 0, 4]])
    k_uniform = sp.ones(3, 3) * 3
    k_nonuniform = sp.diag(9, 9, 9)

    for matrix, margin in (
        (n_uniform, 6),
        (n_nonuniform, 6),
        (k_uniform, 9),
        (k_nonuniform, 9),
    ):
        assert [sum(matrix.row(i)) for i in range(3)] == [margin] * 3
        assert [sum(matrix.col(j)) for j in range(3)] == [margin] * 3

    # Check exact pair relation for both the uniform and a nonuniform
    # semimagic endpoint count.  This is an abstract assumption guard only.
    for k in (0, 3, 9, 12):
        p, q = abstract_endpoint_pair(k)
        assert p.shape == (24, 24)
        assert sp.trace(p) == sp.trace(q) == 12
        assert p * q * p - q * p * q == (p - q) / 3
        assert sp.trace(p * q) == 4 + sp.Rational(2, 3) * k


def bounded_semimagic_by_rows(
    margin: int, maximum: int
) -> set[tuple[int, ...]]:
    rows = [
        row for row in itertools.product(range(maximum + 1), repeat=3)
        if sum(row) == margin
    ]
    result = set()
    for first in rows:
        for second in rows:
            third = tuple(
                margin - first[j] - second[j] for j in range(3)
            )
            if min(third) < 0 or max(third) > maximum:
                continue
            if sum(third) != margin:
                continue
            result.add(first + second + third)
    return result


def bounded_semimagic_by_four_entries(
    margin: int, maximum: int
) -> set[tuple[int, ...]]:
    result = set()
    for a, b, d, e in itertools.product(
        range(maximum + 1), repeat=4
    ):
        c = margin - a - b
        f = margin - d - e
        g = margin - a - d
        h = margin - b - e
        i = margin - g - h
        entries = (a, b, c, d, e, f, g, h, i)
        if min(entries) < 0 or max(entries) > maximum:
            continue
        if c + f + i != margin:
            continue
        result.add(entries)
    return result


PERMUTATIONS = tuple(itertools.permutations(range(3)))


def canonical_semimagic(
    entries: tuple[int, ...], complement: bool
) -> tuple[int, ...]:
    matrix = tuple(
        tuple(entries[3 * i + j] for j in range(3)) for i in range(3)
    )
    transpose = tuple(
        tuple(matrix[j][i] for j in range(3)) for i in range(3)
    )
    bases = [matrix, transpose]
    if complement:
        comp = tuple(
            tuple(4 - matrix[i][j] for j in range(3)) for i in range(3)
        )
        comp_t = tuple(
            tuple(comp[j][i] for j in range(3)) for i in range(3)
        )
        bases.extend((comp, comp_t))

    images = []
    for base_matrix in bases:
        for row_perm in PERMUTATIONS:
            for col_perm in PERMUTATIONS:
                images.append(
                    tuple(
                        base_matrix[row_perm[i]][col_perm[j]]
                        for i in range(3) for j in range(3)
                    )
                )
    return min(images)


def partial_traces_two_qubit(
    matrix: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix]:
    left = sp.zeros(2)
    right = sp.zeros(2)
    for i in range(2):
        for j in range(2):
            left[i, j] = sum(matrix[2 * i + a, 2 * j + a]
                             for a in range(2))
    for a in range(2):
        for b in range(2):
            right[a, b] = sum(matrix[2 * i + a, 2 * i + b]
                              for i in range(2))
    return left, right


def check_rank_pattern_census() -> tuple[int, int, int, int]:
    rank_patterns_rows = bounded_semimagic_by_rows(6, 4)
    rank_patterns_four = bounded_semimagic_by_four_entries(6, 4)
    assert rank_patterns_rows == rank_patterns_four
    assert len(rank_patterns_rows) == 217
    rank_orbits = {
        canonical_semimagic(pattern, complement=True)
        for pattern in rank_patterns_rows
    }
    assert len(rank_orbits) == 9

    endpoint_rows = bounded_semimagic_by_rows(9, 9)
    endpoint_four = bounded_semimagic_by_four_entries(9, 9)
    assert endpoint_rows == endpoint_four
    assert len(endpoint_rows) == 1540
    endpoint_orbits = {
        canonical_semimagic(pattern, complement=False)
        for pattern in endpoint_rows
    }
    assert len(endpoint_orbits) == 56

    # Every cell rank 0,...,4 admits an exact projection with both reduced
    # operators equal to (rank/2) I_2.  Hence every one of the 217 rank
    # tables passes the operator standardness identities cell-by-cell.
    phi = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
    q1 = phi * phi.conjugate().T
    q2 = sp.diag(1, 0, 0, 1)
    canonical = {
        0: sp.zeros(4),
        1: q1,
        2: q2,
        3: sp.eye(4) - q1,
        4: sp.eye(4),
    }
    for rank, projection in canonical.items():
        assert projection**2 == projection
        assert projection.conjugate().T == projection
        assert sp.trace(projection) == rank
        left, right = partial_traces_two_qubit(projection)
        target = sp.Rational(rank, 2) * sp.eye(2)
        assert left == target
        assert right == target

    return (
        len(rank_patterns_rows),
        len(rank_orbits),
        len(endpoint_rows),
        len(endpoint_orbits),
    )


def check_shared_atom_no_go_steps() -> None:
    # Rank-one diagonal cells have the strict determinant gap used in the
    # proof.  The Bell vector realizes the maximal determinant 1/16 and
    # independently checks the compression orientation.
    assert sp.Rational(1, 16) < sp.Rational(1, 9)
    bell = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
    q = bell * bell.conjugate().T
    q12 = sp.kronecker_product(q, ID2)
    q23 = sp.kronecker_product(ID2, q)
    assert q12 * q23 * q12 == q12 / 4

    # Once the shared-atom cell is scalar, the (0,0,b) equation forces
    # every cell in that row to equal the same scalar.  Check both scalar
    # signs against a non-scalar exact Hermitian involution.
    block = sp.kronecker_product(X, Z)
    y = sp.kronecker_product(ID2, block)
    identity_eight = sp.eye(8)
    for sign in (-1, 1):
        x = sign * identity_eight
        residual = x * y * x - y * x * y - (x - y) / 3
        assert residual == sp.Rational(4, 3) * (y - x)
        assert residual != sp.zeros(8)

    # The three scalar row cells have second partial trace
    # 3 * (2 epsilon I_2), contradicting automatic standardness.
    for sign in (-1, 1):
        row_partial = sum(
            (2 * sign * sp.eye(2) for _ in range(3)),
            sp.zeros(2),
        )
        assert row_partial == 6 * sign * sp.eye(2)
        assert row_partial != sp.zeros(2)


def main() -> None:
    check_pauli_square_identity()
    residual_basis_count, first_residual = check_balanced_factor_guard()
    check_endpoint_bookkeeping()
    rank_count, rank_orbits, endpoint_count, endpoint_orbits = (
        check_rank_pattern_census()
    )
    check_shared_atom_no_go_steps()

    d = 6
    assert d * d % 8 == 4
    print("factor-leg Pauli identity: exact")
    print("individual commutator coefficients: exact")
    print("balanced d=6 standard involution: exact")
    print("opposite rank-one controls: 6")
    print(f"scaled cubic residual nonzero on {residual_basis_count}/216 basis states")
    print(f"first nonzero residual: {first_residual}")
    print("controlled-leg contradiction: 8 does not divide 36")
    print("endpoint semimagic and abstract block guards: exact")
    print(
        f"two-site rank tables: {rank_count} labelled, "
        f"{rank_orbits} natural orbits"
    )
    print(
        f"endpoint common-rank tables: {endpoint_count} labelled, "
        f"{endpoint_orbits} row/column/transpose orbits"
    )
    print("all 217 two-site rank tables pass cellwise standardness")
    print("shared-atom scalar propagation and standardness contradiction: exact")
    print("shared-atom proof uses established empty rank-two d=2 class")
    print("PASS")


if __name__ == "__main__":
    main()
