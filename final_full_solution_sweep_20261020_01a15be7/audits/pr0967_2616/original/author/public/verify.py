#!/usr/bin/env python3
"""Exact finite checks only; no finite test models a free ultrafilter."""
import itertools
import json
import math
import sys


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def bad_constant(value):
    raise Invalid("non-finite JSON constant")


def finite_json(value):
    if type(value) is float:
        need(math.isfinite(value), "non-finite JSON number")
    elif type(value) is list:
        for item in value:
            finite_json(item)
    elif type(value) is dict:
        for item in value.values():
            finite_json(item)


def load(raw):
    need(type(raw) is bytes and len(raw) <= 65536, "invalid or oversized input")
    value = json.loads(raw, object_pairs_hook=no_duplicates,
                       parse_constant=bad_constant)
    finite_json(value)
    return value


EXPECTED = {
    "schema_version": 1, "problem_id": 2616, "approaches_counted": 1,
    "group_coordinates": 4, "max_fiber_coordinate": 12,
    "coloring_coordinates": 8, "coloring_classes": 6,
    "arithmetic_progression_max_period": 5,
    "block_coordinates": 3, "labeled_blocks": 3,
}


def validate(value):
    need(type(value) is dict, "object required")
    need(set(value) == set(EXPECTED), "missing or extra fixture key")
    for key, expected in EXPECTED.items():
        need(type(value[key]) is int, key + ": exact integer required")
        need(value[key] == expected, key + ": pinned fixture value required")
    return value


def valuation2(value):
    need(type(value) is int and value > 0, "positive exact integer required")
    return (value & -value).bit_length() - 1


def maximum(mask):
    need(type(mask) is int and mask > 0, "nonempty exact support required")
    return mask.bit_length() - 1


def subgroup_member(mask, available):
    return mask & ~available == 0


def next_size(size, color):
    q = size
    while valuation2(q + 1) != color:
        q += 1
    return q


def audit(d):
    counts = {}
    bound = 1 << d["group_coordinates"]
    count = 0
    for a, s, t in itertools.product(range(bound), repeat=3):
        need((s ^ t) ^ t == s, "Boolean cancellation")
        need(s ^ t == t ^ s, "Boolean commutativity")
        if subgroup_member(s, a) and subgroup_member(t, a):
            need(subgroup_member(s ^ t, a), "subgroup closure")
        # Cosets x+H_A and y+H_A are equal iff x+y belongs to H_A.
        coset_s = {s ^ u for u in range(bound) if subgroup_member(u, a)}
        coset_t = {t ^ u for u in range(bound) if subgroup_member(u, a)}
        need((coset_s == coset_t) == subgroup_member(s ^ t, a), "coset equality")
        need(not (coset_s & coset_t) or coset_s == coset_t, "coset disjointness")
        count += 1
    counts["group_and_coset_cases"] = count
    for k in range(d["max_fiber_coordinate"] + 1):
        elements = [s for s in range(1, 1 << (k + 1)) if maximum(s) == k]
        need(len(elements) == 1 << k, "finite maximum fiber")
        need(all((1 << k) <= s < (1 << (k + 1)) for s in elements), "fiber range")
    counts["maximum_fibers"] = d["max_fiber_coordinate"] + 1
    count = 0
    for s in range(1 << d["coloring_coordinates"]):
        size = s.bit_count()
        need(valuation2(size + 1) >= 0, "color defined including identity")
        for color in range(d["coloring_classes"]):
            q = next_size(size, color)
            need(q >= size and valuation2(q + 1) == color, "target size color")
            for period in range(1, d["arithmetic_progression_max_period"] + 1):
                for residue in range(period):
                    # A={residue+period*m:m>=0} is infinite. This tests only
                    # the append-to-support lemma, not ultrafilter membership.
                    t, n, added = 0, residue, 0
                    while added < q - size:
                        bit = 1 << n
                        if not (s & bit):
                            t |= bit
                            added += 1
                        n += period
                    need(s & t == 0, "extension outside old support")
                    need((s ^ t).bit_count() == q, "extension cardinality")
                    need(valuation2((s ^ t).bit_count() + 1) == color, "dense color")
                    need(all((i - residue) % period == 0 for i in range(t.bit_length())
                             if t & (1 << i)), "extension lies in A")
                    count += 1
    counts["dense_coloring_extensions"] = count
    count = 0
    elements = list(range(1, 1 << d["block_coordinates"]))
    for assignment in itertools.product(range(d["labeled_blocks"] + 1), repeat=len(elements)):
        blocks = [[] for _ in range(d["labeled_blocks"])]
        for s, label in zip(elements, assignment):
            if label:
                blocks[label - 1].append(s)
        maxima = [{maximum(s) for s in block} for block in blocks]
        selected, used = [], set()
        for n, image in enumerate(maxima):
            if image and not image & used:
                selected.append(n)
                used.update(image)
        unions = [set(), set()]
        for j, n in enumerate(selected):
            unions[j % 2].update(maxima[n])
        need(not unions[0] & unions[1], "parity unions disjoint")
        universe = (1 << d["block_coordinates"]) - 1
        for parity in (0, 1):
            removed = sum(1 << k for k in unions[parity])
            available = universe ^ removed
            for j, n in enumerate(selected):
                if j % 2 == parity:
                    need(all(not subgroup_member(s, available) for s in blocks[n]),
                         "maximum exclusion misses entire block")
        count += 1
    counts["finite_disjoint_block_assignments"] = count
    return {"ok": True, "problem_id": 2616, "exact_finite_checks": True,
            "infinite_proof_mechanized": False, "free_ultrafilter_simulated": False,
            "counts": counts}


def main():
    need(len(sys.argv) == 2, "usage: verify.py fixtures.json | --stdin")
    if sys.argv[1] == "--stdin":
        raw = sys.stdin.buffer.read(65537)
    else:
        with open(sys.argv[1], "rb") as stream:
            raw = stream.read(65537)
    result = audit(validate(load(raw)))
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    try:
        main()
    except (Invalid, ValueError, TypeError, KeyError, OSError, UnicodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, allow_nan=False), file=sys.stderr)
        sys.exit(1)
