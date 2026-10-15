"""Fresh reviewer 2's bounded symmetric-chain and plateau checks.

These exact checks falsify possible mistakes in the displayed chain formula;
they do not prove EGH or replace the manuscript's general induction.
"""
from itertools import product
import json


def symmetric_chains(bounds):
    chains = [[()]]
    for b in bounds:
        following = []
        for old in chains:
            a = len(old) - 1
            if a <= b:
                for r in range(a + 1):
                    following.append(
                        [old[r] + (j,) for j in range(b - r + 1)]
                        + [old[i] + (b - r,) for i in range(r + 1, a + 1)]
                    )
            else:
                for r in range(b + 1):
                    following.append(
                        [old[i] + (r,) for i in range(a - r + 1)]
                        + [old[a - r] + (j,) for j in range(r + 1, b + 1)]
                    )
        chains = following
    return chains


def main():
    cases = elements = 0
    for n in range(6):
        for bounds in product(range(4), repeat=n):
            chains = symmetric_chains(bounds)
            flat = [e for chain in chains for e in chain]
            box = set(product(*(range(b + 1) for b in bounds)))
            assert len(flat) == len(set(flat)) and set(flat) == box
            c = sum(bounds)
            counts = [sum(sum(e) == j for e in flat) for j in range(c + 1)]
            for chain in chains:
                assert sum(chain[0]) + sum(chain[-1]) == c
                for e, f in zip(chain, chain[1:]):
                    assert sum(f) == sum(e) + 1
                    assert all(a <= b for a, b in zip(e, f))
            for j in range(c):
                if counts[j] <= counts[j + 1]:
                    for chain in chains:
                        for pos, e in enumerate(chain):
                            if sum(e) == j:
                                assert pos + 1 < len(chain)
            cases += 1
            elements += len(box)
    print(json.dumps({
        "purpose": "Independent bounded symmetric-chain and plateau check; not a proof of EGH.",
        "bound_domain": "all 0<=b_i<=3 in up to five factors, including zero factors and empty product",
        "cases": cases,
        "box_elements": elements,
        "status": "passed",
    }, indent=2))


if __name__ == "__main__":
    main()
