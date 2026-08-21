"""Linear-cone search using all <=3-block selfadjoint grouping inequalities."""

from itertools import combinations

import numpy as np
from scipy.optimize import linprog

from search_grouped_inversion_cone import parts, subset_mask


def canonical(mask):
    return min(mask, 15 ^ mask)


# Variables: eight A purities, eight B purities, then q_T (except q_0 and
# q_K are identified with common A variables through index()).
areps = sorted({canonical(mask) for mask in range(16)})
apos = {mask: i for i, mask in enumerate(areps)}
bpos = {mask: 8 + i for i, mask in enumerate(areps)}
qbase = 16
nvar = 32


def av(mask):
    x = np.zeros(nvar)
    x[apos[canonical(mask)]] = 1
    return x


def bv(mask):
    x = np.zeros(nvar)
    x[bpos[canonical(mask)]] = 1
    return x


def qv(mask):
    # Equal norm, and equal K marginal (K is party 0).
    if mask == 0:
        return av(0)
    if mask == 1:
        return av(1)
    x = np.zeros(nvar)
    x[qbase + mask] = 1
    return x


def impose_common_linear_subspace(v):
    """Substitute B norm=A norm and B_K=A_K."""
    # b_empty position -> a_empty
    for mask in (0, 15):
        bp = bpos[canonical(mask)]
        ap = apos[canonical(mask)]
        if bp != ap:
            v[ap] += v[bp]
            v[bp] = 0
    # b_K = a_K; canonical complement applies.
    bp = bpos[canonical(1)]
    ap = apos[canonical(1)]
    v[ap] += v[bp]
    v[bp] = 0
    return v


def q_partition(which, partition):
    m = len(partition)
    ans = np.zeros(nvar)
    for choose in range(1 << m):
        mask = 0
        for j, block in enumerate(partition):
            if choose >> j & 1:
                mask |= subset_mask(block)
        coeff = (-0.5) ** choose.bit_count()
        ans += coeff * {"a": av, "b": bv, "q": qv}[which](mask)
    return impose_common_linear_subspace(ans)


def target_d():
    # 3q_K-2 sum q_Ki+sum q_Kij+(T^2-q_all)/2.
    ans = 3 * qv(1)
    for i in (1, 2, 3):
        ans -= 2 * qv(1 | (1 << i))
    for i, j in combinations((1, 2, 3), 2):
        ans += qv(1 | (1 << i) | (1 << j))
    ans += 0.5 * (qv(0) - qv(15))
    return impose_common_linear_subspace(ans)


def main():
    generators = []
    labels = []
    parties = (0, 1, 2, 3)
    # Every set partition into m<=3 blocks: selfadjoint PA-PB and the two
    # rank-one sharp slacks.
    for partition in parts(parties):
        m = len(partition)
        if m > 3:
            continue
        qa = q_partition("a", partition)
        qb = q_partition("b", partition)
        qq = q_partition("q", partition)
        generators.append(qa + qb - 2 * qq)
        labels.append(("self", partition))
        if m == 3:
            # Strong PSD rank-two theorem for PA+PB at equal weights.
            generators.append(qa + qb + 2 * qq - 0.5 * qv(15))
            labels.append(("positive_sum", partition))
        base = 2 ** (-m) * av(0)
        generators.append(qa - base)
        labels.append(("rank1a", partition))
        generators.append(qb - base)
        labels.append(("rank1b", partition))

    # Exact swap-sector masses of A tensor B are nonnegative:
    # p_R=2^-4 sum_T (-1)^|R cap T| q_T.
    for rmask in range(16):
        v = np.zeros(nvar)
        for tmask in range(16):
            v += ((-1) ** ((rmask & tmask).bit_count())) * qv(tmask) / 16
        generators.append(impose_common_linear_subspace(v))
        labels.append(("sector", rmask))

    matrix = np.stack(generators, axis=1)
    # Delete coordinates constrained to zero by substitution.
    live = np.flatnonzero(np.any(abs(matrix) > 1e-12, axis=1)
                          | (abs(target_d()) > 1e-12))
    result = linprog(
        np.ones(len(generators)),
        A_eq=matrix[live],
        b_eq=target_d()[live],
        bounds=(0, None),
        method="highs",
    )
    print(result.success, result.message)
    if result.success:
        for weight, label in zip(result.x, labels):
            if weight > 1e-8:
                print(weight, label)


if __name__ == "__main__":
    main()
