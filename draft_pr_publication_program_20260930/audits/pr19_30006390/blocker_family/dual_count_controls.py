#!/usr/bin/env python3
"""Supplementary cyclic/Singer and dual inclusion-exclusion controls.

Designed after the independent seal and source diagnostic reads. Unlike the
source diagnostics, uses cyclic difference sets, incremental minimal hitting
families, and inclusion-exclusion over line subsets. No candidate code import.
"""
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from math import comb
from pathlib import Path
import json


def members(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length()-1
        mask ^= low


def geometry_tables(lines, n):
    joins = {}
    for i, line in enumerate(lines):
        for pair in combinations(members(line), 2):
            assert pair not in joins
            joins[pair] = i
    assert len(joins) == comb(n, 2)
    meets = {}
    for i, j in combinations(range(n), 2):
        common = lines[i] & lines[j]
        assert common.bit_count() == 1
        meets[i, j] = common.bit_length()-1
    return joins, meets


def closure_isomorphism(source_lines, target_lines, source_frame, target_frame, n):
    sj, sm = geometry_tables(source_lines, n)
    tj, tm = geometry_tables(target_lines, n)
    pmap, lmap = dict(zip(source_frame, target_frame)), {}
    while True:
        old = len(pmap)+len(lmap)
        for p, r in combinations(sorted(pmap), 2):
            source_line = sj[p, r]
            target_line = tj[tuple(sorted((pmap[p], pmap[r])))]
            if source_line in lmap:
                assert lmap[source_line] == target_line
            else:
                assert target_line not in lmap.values()
                lmap[source_line] = target_line
        for first, second in combinations(sorted(lmap), 2):
            source_point = sm[first, second]
            target_point = tm[tuple(sorted((lmap[first], lmap[second])))]
            if source_point in pmap:
                assert pmap[source_point] == target_point
            else:
                assert target_point not in pmap.values()
                pmap[source_point] = target_point
        if len(pmap)+len(lmap) == old:
            break
    assert len(pmap) == len(lmap) == n
    def remap(mask):
        return sum(1 << pmap[p] for p in members(mask))
    for i, line in enumerate(source_lines):
        assert remap(line) == target_lines[lmap[i]]
    return pmap, remap


def main():
    own = Path(__file__).resolve().parent
    certificates = json.loads((own / "fresh_certificates.json").read_text())
    fresh = json.loads((own / "fresh_checks.json").read_text())
    result = []
    for cert, summary in zip(certificates, fresh["planes"]):
        q, n = cert["q"], len(cert["points"])
        difference_set = (0, 1, 3) if q == 2 else (0, 1, 3, 9)
        differences = Counter((a-b) % n for a in difference_set for b in difference_set if a != b)
        assert differences == Counter({i:1 for i in range(1,n)})
        lines = [sum(1 << ((d+t) % n) for d in difference_set) for t in range(n)]
        geometry_tables(lines, n)
        assert all(line.bit_count() == q+1 for line in lines)
        assert all(sum(bool(line & (1 << p)) for line in lines) == q+1 for p in range(n))
        target_frame = next(frame for frame in combinations(range(n),4)
                            if all(sum(bool(line & (1 << p)) for p in frame) < 3 for line in lines))
        pmap, remap = closure_isomorphism(cert["line_point_masks"], lines,
                                         summary["quadrangle_indices"], target_frame, n)
        # Berge's incremental construction: extend only missed constraints;
        # remove supersets after every line. The invariant is the complete
        # antichain of minimal hitting sets of the lines processed so far.
        family = {0}
        stage_sizes = []
        for line in lines:
            extended = set()
            for blocker in family:
                if blocker & line:
                    extended.add(blocker)
                else:
                    extended.update(blocker | (1 << p) for p in members(line))
            antichain = []
            for blocker in sorted(extended, key=lambda mask:(mask.bit_count(),mask)):
                if not any(smaller & blocker == smaller for smaller in antichain):
                    antichain.append(blocker)
            family = set(antichain)
            stage_sizes.append(len(family))
        assert family == {remap(mask) for mask in cert["minimal_ordinary_blocker_masks"]}
        # Exact blocker cardinality polynomial by dual inclusion-exclusion:
        # selected lines all missed => B avoids their union; coefficient at
        # z^k is sum_S (-1)^|S| binom(n-|union S|, k).
        unions = [0]*(1 << n)
        polynomial = [0]*(n+1)
        for selection in range(1 << n):
            if selection:
                low = selection & -selection
                unions[selection] = unions[selection ^ low] | lines[low.bit_length()-1]
            available = n-unions[selection].bit_count()
            sign = -1 if selection.bit_count() % 2 else 1
            for k in range(available+1):
                polynomial[k] += sign*comb(available,k)
        # Direct enumeration on our sealed affine system crosschecks every
        # polynomial coefficient, independently of candidate stored counts.
        direct_counts = Counter(mask.bit_count() for mask in range(1 << n)
                                if all(mask & line for line in cert["line_point_masks"]))
        assert polynomial == [direct_counts[k] for k in range(n+1)]
        assert sum(polynomial) == summary["ordinary_blockers"]
        minimal_histogram = Counter(mask.bit_count() for mask in family)
        assert {str(k):v for k,v in sorted(minimal_histogram.items())} == summary["minimal_blocker_size_histogram"]
        result.append({"q":q,"cyclic_difference_set":difference_set,
                       "difference_property_verified":True,
                       "explicit_affine_to_cyclic_point_map":[pmap[i] for i in range(n)],
                       "join_meet_closure_isomorphism_verified":True,
                       "berge_minimal_family_stage_sizes":stage_sizes,
                       "minimal_blocker_histogram":dict(sorted(minimal_histogram.items())),
                       "dual_line_subsets_examined":1 << n,
                       "blocker_cardinality_polynomial_coefficients":polynomial,
                       "all_coefficients_match_sealed_affine_enumeration":True})
    report = {"utc":datetime.now(timezone.utc).isoformat(),"status":"pass",
              "phase":"supplementary_postseal_control",
              "mechanisms":["cyclic perfect difference sets","incidence join/meet closure isomorphism",
                            "incremental minimal hitting antichains","dual line-subset inclusion-exclusion"],
              "planes":result,"limit":"Exact small-order controls only; no conjecture-resolution claim."}
    (own / "dual_count_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
