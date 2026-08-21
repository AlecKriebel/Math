"""LP search for positive-map decompositions by grouped universal inversions."""

from itertools import combinations

import numpy as np
from scipy.optimize import linprog


def parts(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    first = items[0]
    for tail in parts(items[1:]):
        # New block.
        yield ((first,),) + tail
        # Insert into an existing block.
        for j in range(len(tail)):
            block = tuple(sorted((first,) + tail[j]))
            yield tail[:j] + (block,) + tail[j + 1 :]


def subset_mask(values):
    ans = 0
    for v in values:
        ans |= 1 << v
    return ans


def generator(traced, partition, scales=None):
    """E_traced prod_block(scale_block E_block-I), in E_S basis."""
    coeff = np.zeros(16)
    tmask = subset_mask(traced)
    m = len(partition)
    if scales is None:
        scales = (1,) * m
    for choose in range(1 << m):
        mask = tmask
        count = 0
        factor = 1
        for j, block in enumerate(partition):
            if choose >> j & 1:
                mask |= subset_mask(block)
                count += 1
                factor *= scales[j]
        coeff[mask] += factor * (-1) ** (m - count)
    return coeff


def all_generators():
    out = []
    parties = tuple(range(4))
    for tmask in range(16):
        traced = tuple(i for i in parties if tmask >> i & 1)
        active = tuple(i for i in parties if not (tmask >> i & 1))
        for partition in parts(active):
            # c E_block-I is completely copositive for every c>=1.
            for code in range(4 ** len(partition)):
                raw = code
                scales = []
                for _ in partition:
                    scales.append((1, 2, 3, 4)[raw % 4])
                    raw //= 4
                scales = tuple(scales)
                out.append(
                    (traced, tuple(zip(partition, scales)),
                     generator(traced, partition, scales))
                )
    return out


def target_unshifted():
    # id_K tensor prod_{i=1}^3 (2 E_i-I)
    ans = np.zeros(16)
    for smask in range(8):
        mask = smask << 1
        count = smask.bit_count()
        ans[mask] = 2 ** count * (-1) ** (3 - count)
    return ans


def target_sharp():
    # 1/2 R_global + sum R_iR_j + 3 R_1R_2R_3.
    ans = np.zeros(16)
    ans[15] += 0.5
    ans[0] -= 0.5
    for i, j in combinations((1, 2, 3), 2):
        ans[0] += 1
        ans[1 << i] -= 1
        ans[1 << j] -= 1
        ans[(1 << i) | (1 << j)] += 1
    for smask in range(8):
        mask = smask << 1
        ans[mask] += 3 * (-1) ** (3 - smask.bit_count())
    return ans


def target_odd():
    # R-monomial description from the exterior recoupling:
    # 1/2 on all singleton/pair/quadruple terms, 2 on physical triple,
    # zero on triples containing K.
    ans = np.zeros(16)
    for rmask in range(1, 16):
        size = rmask.bit_count()
        if size in (1, 2, 4):
            weight = 0.5
        elif size == 3 and not (rmask & 1):
            weight = 2
        else:
            weight = 0
        for emask in range(16):
            if emask & ~rmask:
                continue
            ans[emask] += weight * (-1) ** (size - emask.bit_count())
    return ans


def solve(target):
    gens = all_generators()
    matrix = np.stack([x[2] for x in gens], axis=1)
    result = linprog(
        np.ones(len(gens)),
        A_eq=matrix,
        b_eq=target,
        bounds=(0, None),
        method="highs",
    )
    print(result.success, result.message)
    if result.success:
        for weight, (traced, partition, _) in zip(result.x, gens):
            if weight > 1e-8:
                print(weight, "trace", traced, "blocks", partition)


if __name__ == "__main__":
    print("unshifted")
    solve(target_unshifted())
    print("sharp")
    solve(target_sharp())
    print("odd")
    solve(target_odd())
