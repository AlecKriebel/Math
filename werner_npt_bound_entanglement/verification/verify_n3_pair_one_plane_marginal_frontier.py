#!/usr/bin/env python3
"""Exact checks for the normalized one-plane marginal frontier.

This script uses only Python's standard library.  It verifies:

* the Walsh coefficients of the swap-sector defect;
* the equivalence of the signed and positive-mass forms;
* the trace-replacement expansion of the marginal operator;
* the exact sparse counterexample to the uncompensated Hodge core.
"""

from fractions import Fraction as F
from itertools import product


PARTIES = 4  # physical sites 0,1,2 and auxiliary K=3


def sector_value(k_sign: int, physical_signs: tuple[int, int, int]) -> int:
    """Eigenvalue of the full positive-sector defect."""
    r = sum(sign == -1 for sign in physical_signs)
    return (
        int(k_sign == -1 and r == 0)
        + int(k_sign == -1 and r == 1)
        + int(k_sign == 1 and r == 2)
        + 5 * int(k_sign == 1 and r == 3)
        - 4 * int(k_sign == -1 and r == 3)
    )


def walsh_coefficients():
    """Return coefficients of monomials in (F_K,F_1,F_2,F_3)."""
    coefficients = {}
    for mask in range(1 << PARTIES):
        value = F(0)
        for signs in product((1, -1), repeat=PARTIES):
            monomial = 1
            for bit in range(PARTIES):
                if mask & (1 << bit):
                    monomial *= signs[bit]
            value += sector_value(signs[0], signs[1:]) * monomial
        coefficients[mask] = value / 16
    return coefficients


# Apart from the explicit identity term, a trace-replacement monomial
# is represented by the set of physical sites on which e_i acts.
# Expand (3I - 3 sum e_j e_k + 2 sum e_k - R)/4.
marginal_coefficients = {
    "I": F(3, 4),
    frozenset(): F(-1, 4),
    frozenset((0,)): F(1, 2),
    frozenset((1,)): F(1, 2),
    frozenset((2,)): F(1, 2),
    frozenset((0, 1)): F(-3, 4),
    frozenset((0, 2)): F(-3, 4),
    frozenset((1, 2)): F(-3, 4),
}


def swap_to_trace_coefficients(walsh):
    """Convert swap monomials to trace replacements in an expectation.

    A swap on a subset S of the four parties contracts to trace
    replacement on its complement.  The Walsh expansion below has only
    one monomial which does not contain F_K: the constant monomial,
    which gives an explicit multiple of the identity.  Every other
    surviving monomial contains F_K and therefore gives a physical
    trace replacement while leaving K untouched.  Finally
    e_1 e_2 e_3(R)=I/2 converts its coefficient into the remaining
    identity contribution.
    """
    result = {"I": F(0)}
    for mask, coefficient in walsh.items():
        if not coefficient:
            continue
        if not (mask & 1):
            assert mask == 0
            result["I"] += coefficient
            continue
        # Bit order in the Walsh table is K,1,2,3.
        swapped_physical = {
            site for site in range(3) if mask & (1 << (site + 1))
        }
        traced_physical = frozenset(set(range(3)) - swapped_physical)
        result[traced_physical] = (
            result.get(traced_physical, F(0)) + coefficient
        )
    # The all-physical trace replacement equals I/2 on a normalized
    # code purification.  It is the only such term.
    result["I"] += result.pop(frozenset((0, 1, 2))) / 2
    return {key: value for key, value in result.items() if value}


walsh = walsh_coefficients()
assert swap_to_trace_coefficients(walsh) == marginal_coefficients


# Check the scalar sector identities symbolically on eight independent
# formal variables.
formal_s = [F(2), F(3), F(5), F(7)]
formal_a = [F(11), F(13), F(17), F(19)]
total = sum(formal_s) + sum(formal_a)
scale = F(1, 4) / sum(formal_a)
formal_s = [scale * value for value in formal_s]
formal_a = [scale * value for value in formal_a]
# Impose only sum a=1/4; sum s=3/4 is needed as well, so rescale s.
formal_s_scale = F(3, 4) / sum(formal_s)
formal_s = [formal_s_scale * value for value in formal_s]
assert sum(formal_a) == F(1, 4)
assert sum(formal_s) == F(3, 4)
d = [formal_s[r] - formal_a[r] for r in range(4)]
assert sum(d) == F(1, 2)
signed_defect = F(1, 4) + d[2] + 5 * d[3]
positive_defect = (
    formal_a[0]
    + formal_a[1]
    + formal_s[2]
    + 5 * formal_s[3]
    - 4 * formal_a[3]
)
assert signed_defect == positive_defect


State = dict[tuple[int, ...], F]


def tensor(first: State, second: State) -> State:
    output = {}
    for left, left_value in first.items():
        for right, right_value in second.items():
            key = left + right
            output[key] = output.get(key, F(0)) + left_value * right_value
    return {key: value for key, value in output.items() if value}


def swap(state: State, party: int) -> State:
    """Swap party between two replicas.

    State keys have order (p1,p2,p3,K,p1',p2',p3',K').
    """
    output = {}
    for key, value in state.items():
        image = list(key)
        image[party], image[party + PARTIES] = (
            image[party + PARTIES],
            image[party],
        )
        image_key = tuple(image)
        output[image_key] = output.get(image_key, F(0)) + value
    return {key: value for key, value in output.items() if value}


def project_sign(state: State, party: int, sign: int) -> State:
    swapped = swap(state, party)
    keys = set(state) | set(swapped)
    return {
        key: (state.get(key, F(0)) + sign * swapped.get(key, F(0))) / 2
        for key in keys
        if state.get(key, F(0)) + sign * swapped.get(key, F(0))
    }


def norm_squared(state: State) -> F:
    return sum(value * value for value in state.values())


# The amplitudes of normalized Psi and x are all rational (1/2).
psi: State = {
    (0, 0, 0, 0): F(1, 2),
    (1, 1, 1, 0): F(1, 2),
    (0, 0, 1, 1): F(1, 2),
    (1, 1, 0, 1): F(1, 2),
}
x: State = {
    (0, 0, 1, 0): F(-1, 2),
    (1, 1, 0, 0): F(1, 2),
    (0, 0, 0, 1): F(-1, 2),
    (1, 1, 1, 1): F(1, 2),
}
assert norm_squared(psi) == 1
assert norm_squared(x) == 1
z = tensor(psi, x)
assert norm_squared(z) == 1


def exact_sector_mass(k_sign: int, negative_physical: frozenset[int]) -> F:
    projected = project_sign(z, 3, k_sign)
    for site in range(3):
        sign = -1 if site in negative_physical else 1
        projected = project_sign(projected, site, sign)
    return norm_squared(projected)


s = [F(0) for _ in range(4)]
a = [F(0) for _ in range(4)]
for negative_count in range(4):
    for bits in product((0, 1), repeat=3):
        negative = frozenset(site for site, bit in enumerate(bits) if bit)
        if len(negative) != negative_count:
            continue
        s[negative_count] += exact_sector_mass(1, negative)
        a[negative_count] += exact_sector_mass(-1, negative)

assert s == [F(5, 16), F(3, 8), F(1, 16), F(0)]
assert a == [F(1, 8), F(1, 16), F(0), F(1, 16)]
assert sum(s) == F(3, 4)
assert sum(a) == F(1, 4)

core = s[2] + a[1] - 4 * a[3]
compensator = a[0] + 5 * s[3]
full = core + compensator
assert core == F(-1, 8)
assert compensator == F(1, 8)
assert full == 0

print(
    "verified exact swap/marginal equivalences and the "
    "sparse -1/8 uncompensated-core counterexample"
)
