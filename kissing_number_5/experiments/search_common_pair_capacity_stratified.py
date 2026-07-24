#!/usr/bin/env python3
"""Reoptimize the five-node model with stratified common-pair capacities.

Discovery code only.  This wraps the existing degree-four cutting-plane
search but supplements its cumulative threshold rows by the pointwise
capacity theorem summed separately over each exact base color.
"""

from fractions import Fraction as Q

import numpy as np

import experiments.search_local_hybrid_degree3 as local


ORIGINAL_ROWS = local.common_pair_capacity_rows


def stratified_rows(nodes, ordered_counts, triples):
    answer = list(ORIGINAL_ROWS(nodes, ordered_counts, triples))
    for base_color, base_value in enumerate(nodes):
        if base_value > 0:
            continue
        for high_threshold in (node for node in nodes if node > 0):
            if base_value == -1:
                p, capacity = None, 0
            else:
                p = 2 * high_threshold**2 / (1 + base_value)
                capacity = local.common_pair_capacity(p)
            if capacity is None:
                continue
            row = np.array(
                [
                    sum(
                        triple[position] == base_color
                        and all(
                            nodes[triple[other]] >= high_threshold
                            for other in range(3)
                            if other != position
                        )
                        for position in range(3)
                    )
                    for triple in triples
                ],
                dtype=float,
            )
            upper = capacity * ordered_counts[base_color] // 2
            # The solve routine treats the first two fields as printable
            # threshold labels only.
            answer.append(
                (
                    f"exact-color-{base_color}",
                    high_threshold,
                    p,
                    capacity,
                    row,
                    upper,
                )
            )
    return tuple(answer)


def main():
    local.common_pair_capacity_rows = stratified_rows
    local.solve(
        total_degree=4,
        require_rank_five=True,
        require_color_degree=True,
        require_common_pair_capacity=True,
        support="local5",
        integer=True,
        lp_warm_start=True,
        rank_outer_band="3/100",
        max_rounds=120,
    )


if __name__ == "__main__":
    main()
