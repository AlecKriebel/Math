#!/usr/bin/env python3
"""Independent exhaustive audit of bounded stable-set shadow/end-slice claims.

No external packages, arithmetic, or upstream implementation is used.  Stable
sets are the upper sets of the directed graph of allowed coordinate transfers.
The include/exclude recursion enumerates every upper set exactly once: including
a vertex forces its upper closure; excluding it forces its lower closure.
"""
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path


def degree_box(bounds, degree):
    return sorted((u for u in itertools.product(*(range(b + 1) for b in bounds))
                   if sum(u) == degree), reverse=True)


def transfer_closures(box, bounds):
    idx = {u: i for i, u in enumerate(box)}
    ups = []
    for i, u in enumerate(box):
        closure = 1 << i
        for h in range(len(bounds)):
            for ell in range(h + 1, len(bounds)):
                if u[ell] and u[h] < bounds[h]:
                    v = list(u)
                    v[h] += 1
                    v[ell] -= 1
                    j = idx[tuple(v)]
                    assert j < i
                    closure |= ups[j]
        ups.append(closure)
    downs = [sum(1 << j for j, upper in enumerate(ups) if upper & (1 << i))
             for i in range(len(box))]
    return ups, downs


def upper_sets(ups, downs):
    full = (1 << len(ups)) - 1

    def visit(included, excluded):
        undecided = full & ~(included | excluded)
        if not undecided:
            yield included
            return
        bit = undecided & -undecided
        i = bit.bit_length() - 1
        if not (ups[i] & excluded):
            yield from visit(included | ups[i], excluded)
        if not (downs[i] & included):
            yield from visit(included, excluded | downs[i])

    yield from visit(0, 0)


def union_shadow(mask, shadows):
    result = 0
    while mask:
        bit = mask & -mask
        result |= shadows[bit.bit_length() - 1]
        mask ^= bit
    return result


def decode(mask, box):
    return [list(u) for i, u in enumerate(box) if mask & (1 << i)]


def audit_degree(bounds, degree):
    box = degree_box(bounds, degree)
    target = degree_box(bounds, degree + 1)
    target_idx = {u: i for i, u in enumerate(target)}
    shadows = []
    for u in box:
        shadow = 0
        for h, b in enumerate(bounds):
            if u[h] < b:
                v = list(u)
                v[h] += 1
                shadow |= 1 << target_idx[tuple(v)]
        shadows.append(shadow)
    zero = sum(1 << i for i, u in enumerate(box) if u[-1] == 0)
    top = sum(1 << i for i, u in enumerate(box) if u[-1] == bounds[-1])
    target_zero = sum(1 << i for i, u in enumerate(target) if u[-1] == 0)
    ups, downs = transfer_closures(box, bounds)
    lex_shadows = [union_shadow((1 << size) - 1, shadows)
                   for size in range(len(box) + 1)]
    for lex_shadow in lex_shadows:
        # In lex order, an initial segment is exactly an all-ones low bit mask.
        assert lex_shadow == (1 << lex_shadow.bit_count()) - 1
    predecessors = [tuple(x - int(h == max(i for i, x in enumerate(v) if x))
                          for h, x in enumerate(v)) for v in target] if degree >= 0 else []
    assert all(predecessors[i] >= predecessors[i + 1]
               for i in range(len(predecessors) - 1))
    count = 0
    strict = [0, 0, 0]
    seen = set() if len(box) <= 12 else None
    for mask in upper_sets(ups, downs):
        count += 1
        if seen is not None:
            assert mask not in seen
            seen.add(mask)
        size = mask.bit_count()
        lex = (1 << size) - 1
        shadow = union_shadow(mask, shadows)
        lhs = [shadow.bit_count(), (mask & zero).bit_count(), (mask & top).bit_count()]
        rhs = [lex_shadows[size].bit_count(), (lex & zero).bit_count(), (lex & top).bit_count()]
        if not (lhs[0] >= rhs[0] and lhs[1] >= rhs[1] and lhs[2] <= rhs[2]):
            return {"failure": True, "bounds": bounds, "degree": degree,
                    "X": decode(mask, box), "Y": decode(lex, box),
                    "shadow_X": decode(shadow, target),
                    "shadow_Y": decode(lex_shadows[size], target),
                    "left_counts": lhs, "right_counts": rhs}
        assert shadow.bit_count() == ((shadow & target_zero).bit_count()
                                      + size - (mask & top).bit_count())
        for k in range(3):
            strict[k] += lhs[k] != rhs[k]
    if seen is not None:
        direct = {mask for mask in range(1 << len(box))
                  if all(not (mask & (1 << i)) or not (ups[i] & ~mask)
                         for i in range(len(box)))}
        assert seen == direct
    return {"failure": False, "count": count, "strict_counts": strict,
            "size": len(box), "bounds": list(bounds), "degree": degree}


def main():
    start = time.monotonic()
    test_bounds = set()
    for r in range(1, 4):
        test_bounds.update(itertools.product(range(1, 5), repeat=r))
    test_bounds.update(itertools.product(range(1, 4), repeat=4))
    test_bounds.update(itertools.product(range(1, 3), repeat=5))
    test_bounds.update({(1,) * 6, (1,) * 7, (1,) * 8,
                        (1, 1, 1, 1, 1, 2), (2, 1, 1, 1, 1, 1),
                        (4, 1, 3, 2), (2, 4, 1, 3), (3, 2, 4, 1)})
    rows = []
    skipped = []
    limit = 70
    output = Path(__file__).with_suffix(".json")
    for bounds in sorted(test_bounds, key=lambda b: (len(b), b)):
        for degree in range(-1, sum(bounds) + 2):
            size = len(degree_box(bounds, degree))
            if size > limit:
                skipped.append({"bounds": list(bounds), "degree": degree, "size": size})
                continue
            row = audit_degree(bounds, degree)
            rows.append(row)
            if row["failure"]:
                output.write_text(json.dumps({"status": "counterexample", "row": row}, indent=2) + "\n")
                print(json.dumps(row))
                return
        print(json.dumps({"completed_bounds": bounds,
                          "stable_sets_checked_so_far": sum(row["count"] for row in rows),
                          "elapsed_seconds": round(time.monotonic() - start, 2)}), flush=True)
    result = {"status": "no_counterexample_in_exhaustive_domain",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": round(time.monotonic() - start, 3),
              "bound_tuples": len(test_bounds), "degree_boxes": len(rows),
              "stable_sets": sum(row["count"] for row in rows),
              "max_stable_sets_in_degree_box": max(row["count"] for row in rows),
              "strict_comparison_counts": [sum(row["strict_counts"][k] for row in rows) for k in range(3)],
              "max_degree_box_size": max(row["size"] for row in rows),
              "unordered_bound_degree_boxes": sum(any(b1 > b2 for b1, b2 in zip(row["bounds"], row["bounds"][1:])) for row in rows),
              "checks": ["lex shadows are lex", "largest predecessor preserves lex order",
                         "shadow lower bound", "zero-slice lower bound", "top-slice upper bound",
                         "stable shadow counting identity", "upper-set enumeration agrees with direct subset scan when degree-box size <=12"],
              "enumeration_method": "exact upper-set recursion on allowed unit-transfer graph",
              "limits": {"maximum_degree_box_size": limit,
                         "skipped_larger_degree_boxes": skipped}, "rows": rows}
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("rows", "limits")}))


if __name__ == "__main__":
    main()
