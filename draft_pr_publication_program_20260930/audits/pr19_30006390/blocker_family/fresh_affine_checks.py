#!/usr/bin/env python3
"""First-party independent affine-completion and exhaustive-cover audit.

Only Python's standard library is required. This file was designed without
reading either candidate diagnostic program or earlier review artifacts.
"""
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import hashlib
import json


class Checks:
    def __init__(self):
        self.counts = Counter()

    def require(self, value, family):
        self.counts[family] += 1
        if not value:
            raise AssertionError(f"failed {family}, ordinal {self.counts[family]}")


def affine_completion(q):
    # Index affine points first; append q slope points and one vertical point.
    points = [("affine", x, y) for x in range(q) for y in range(q)]
    points += [("slope", m) for m in range(q)] + [("vertical",)]
    lines = []
    names = []
    for m in range(q):
        for b in range(q):
            lines.append({x*q + (m*x+b) % q for x in range(q)} | {q*q+m})
            names.append(("slope", m, b))
    for b in range(q):
        lines.append({b*q+y for y in range(q)} | {q*q+q})
        names.append(("vertical", b))
    lines.append(set(range(q*q, q*q+q+1)))
    names.append(("infinity",))
    return points, names, [sum(1 << x for x in line) for line in lines]


def bit_indices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def downset_min(values, n):
    # Fast subset transform, independent of transversal enumeration below.
    result = values.copy()
    for p in range(n):
        bit = 1 << p
        for mask in range(1 << n):
            if mask & bit:
                result[mask] = min(result[mask], result[mask ^ bit])
    return result


def audit(q, checks):
    points, names, lines = affine_completion(q)
    n = q*q+q+1
    limit = 1 << n
    universe = limit-1
    all_lines = (1 << n)-1
    checks.require(len(points) == len(lines) == n, "axiom_counts")
    checks.require(len(set(lines)) == n, "distinct_lines")
    for line in lines:
        checks.require(line.bit_count() == q+1, "line_size")
    for p in range(n):
        checks.require(sum(bool(line & (1 << p)) for line in lines) == q+1,
                       "point_degree")
    for first, second in combinations(lines, 2):
        checks.require((first & second).bit_count() == 1, "unique_line_meet")
    for p, r in combinations(range(n), 2):
        pair = (1 << p) | (1 << r)
        checks.require(sum(line & pair == pair for line in lines) == 1,
                       "unique_point_join")
    quadrangle = next((quad for quad in combinations(range(n), 4)
                       if all(sum(bool(line & (1 << p)) for p in quad) < 3
                              for line in lines)), None)
    checks.require(quadrangle is not None, "quadrangle")

    # Coverage is a line index mask, distinct from the point mask.
    point_coverage = [sum(1 << i for i, line in enumerate(lines)
                          if line & (1 << p)) for p in range(n)]
    coverage = [0]*limit
    for mask in range(1, limit):
        bit = mask & -mask
        coverage[mask] = coverage[mask ^ bit] | point_coverage[bit.bit_length()-1]
    ordinary = [covered == all_lines for covered in coverage]
    contains_line = [any(mask & line == line for line in lines)
                     for mask in range(limit)]
    minimal = [False]*limit
    tangent_masks = [0]*limit
    for mask in range(limit):
        tangent = 0
        for line in lines:
            section = mask & line
            if section.bit_count() == 1:
                tangent |= section
        tangent_masks[mask] = tangent
        deletion_minimal = ordinary[mask] and all(
            not ordinary[mask ^ (1 << p)] for p in bit_indices(mask))
        tangent_minimal = ordinary[mask] and tangent == mask
        checks.require(deletion_minimal == tangent_minimal, "tangent_minimal_equivalence")
        minimal[mask] = tangent_minimal
        checks.require(ordinary[mask] == all((universe ^ mask) & line != line
                                            for line in lines), "complement_independence")
        if minimal[mask] and contains_line[mask]:
            checks.require(mask in lines, "minimal_whole_line_is_line")
        if ordinary[mask]:
            checks.require(mask.bit_count() >= q+1, "ordinary_incidence_bound")
        if ordinary[mask] and not contains_line[mask]:
            k = mask.bit_count()
            a = k-q-1
            r = [(mask & line).bit_count() for line in lines]
            checks.require(a >= 0, "bruen_nonnegative_a")
            checks.require(all(1 <= t <= a+1 for t in r), "bruen_local_bounds")
            checks.require(sum(r) == k*(q+1), "bruen_incidence_sum")
            checks.require(sum(t*(t-1) for t in r) == k*(k-1), "bruen_ordered_pairs")
            checks.require(k*(k-1) <= (a+1)*(k*(q+1)-n), "bruen_inequality")
            checks.require((a+1)*(k*(q+1)-n)-k*(k-1) == q*(a*a-q),
                           "bruen_algebra")
            checks.require(a*a >= q, "bruen_integer_bound")

    sentinel = n+1
    ordinary_min = downset_min([mask.bit_count() if ordinary[mask] else sentinel
                               for mask in range(limit)], n)
    minimal_min = downset_min([mask.bit_count() if minimal[mask] else sentinel
                              for mask in range(limit)], n)
    tau = []
    cover_candidates = 0
    for retained in range(limit):
        # Exhaustive direct exact-cover optimization: all B <= R. No
        # ordinary-blocker or minimal-blocker criterion enters this search.
        best = retained.bit_count()
        candidate = retained
        while True:
            cover_candidates += 1
            if coverage[candidate] == coverage[retained]:
                best = min(best, candidate.bit_count())
            if not candidate:
                break
            candidate = (candidate-1) & retained
        tau.append(best)
        checks.require(ordinary_min[retained] == minimal_min[retained],
                       "every_blocker_contains_minimal")
        if ordinary[retained]:
            checks.require(best == ordinary_min[retained], "nonempty_section_reduction")
        if ordinary[retained] and not contains_line[retained]:
            checks.require((best-q-1)**2 >= q and best >= q+1,
                           "good_event_integer_lower")
        if any(retained & line == retained for line in lines):
            checks.require(best == retained.bit_count(), "subset_of_line_boundary")
    checks.require(tau[0] == 0, "empty_R_boundary")
    for line in lines:
        checks.require(tau[line] == q+1 and minimal[line], "whole_line_boundary")

    empty_sections_count = sum(not value for value in ordinary)
    whole_line_count = sum(contains_line)
    checks.require(empty_sections_count <= n*(1 << (n-q-1)), "empty_union_bound")
    checks.require(whole_line_count <= n*(1 << (n-q-1)), "whole_line_union_bound")
    for first, second in combinations(lines, 2):
        both_missed = sum(not(retained & (first | second)) for retained in range(limit))
        marginal = 1 << (n-q-1)
        checks.require(both_missed == 1 << (n-2*q-1), "shared_point_joint_exact")
        checks.require(both_missed*limit == 2*marginal*marginal,
                       "independence_negative_control")
    for k in range(n+1):
        exact_low = sum(value <= k for value in tau)
        minimal_low = sum(value <= k for value in minimal_min)
        # Weight is the exact number of retained supersets of the blocker.
        weighted = sum(1 << (n-mask.bit_count()) for mask in range(limit)
                       if minimal[mask] and mask.bit_count() <= k)
        checks.require(exact_low <= empty_sections_count + weighted,
                       "first_moment_all_R")
        checks.require(minimal_low <= weighted, "weighted_union_of_minimals")
        for retained in range(limit):
            if ordinary[retained]:
                checks.require((tau[retained] <= k) == (minimal_min[retained] <= k),
                               "minimal_threshold_equivalence")

    # A nontrivial positive control at q=3; at q=2 this construction
    # becomes a whole line, guarding against an unqualified transfer.
    vertices = [0, q, 1]  # (0,0), (1,0), (0,1)
    triangle_sides = [next(line for line in lines
                           if line & ((1 << p) | (1 << r)) == ((1 << p) | (1 << r)))
                      for p, r in combinations(vertices, 2)]
    triangle_boundary = 0
    for side in triangle_sides:
        triangle_boundary |= side
    for p in vertices:
        triangle_boundary &= ~(1 << p)
    checks.require(ordinary[triangle_boundary], "triangle_positive_control")
    if q == 3:
        checks.require(triangle_boundary.bit_count() == 6 and
                       not contains_line[triangle_boundary] and
                       minimal[triangle_boundary] and tau[triangle_boundary] == 6,
                       "q3_nontrivial_integer_bound_attainment")
    elif q == 2:
        checks.require(triangle_boundary in lines, "q2_triangle_whole_line_control")

    nontrivial = [mask for mask in range(limit) if ordinary[mask] and not contains_line[mask]]
    report = {
        "q": q, "n": n, "point_subsets": limit,
        "direct_exact_cover_candidates": cover_candidates,
        "ordinary_blockers": sum(ordinary), "nontrivial_blockers": len(nontrivial),
        "minimal_blocker_size_histogram": dict(sorted(Counter(mask.bit_count()
                                  for mask in range(limit) if minimal[mask]).items())),
        "nontrivial_blocker_size_histogram": dict(sorted(Counter(mask.bit_count()
                                  for mask in nontrivial).items())),
        "tau_histogram": dict(sorted(Counter(tau).items())),
        "empty_sections_count": empty_sections_count,
        "whole_line_count": whole_line_count,
        "good_event_count": len(nontrivial),
        "quadrangle_indices": quadrangle,
        "triangle_control_mask": triangle_boundary,
        "triangle_control_points": [points[p] for p in bit_indices(triangle_boundary)],
        "triangle_control_tau": tau[triangle_boundary],
    }
    certificate = {"q": q, "points": points, "line_names": names,
                   "line_point_masks": lines, "tau_by_retained_mask": tau,
                   "minimal_ordinary_blocker_masks": [mask for mask in range(limit)
                                                       if minimal[mask]]}
    return report, certificate


def main():
    output_dir = Path(__file__).resolve().parent
    checks = Checks()
    reports, certificates = [], []
    for q in (2, 3):
        report, certificate = audit(q, checks)
        reports.append(report)
        certificates.append(certificate)
    # Integer evaluations guard transcription; general algebra is separately
    # proved in the sealed analytic note.
    for q in range(2, 101):
        for a in range(0, q+2):
            k, n = q+a+1, q*q+q+1
            checks.require((a+1)*(k*(q+1)-n)-k*(k-1) == q*(a*a-q),
                           "general_algebra_evaluation_control")
    cert_path = output_dir / "fresh_certificates.json"
    cert_path.write_text(json.dumps(certificates, indent=2)+"\n")
    results = {"audit_type": "independent_affine_completion_exact_cover",
               "utc": datetime.now(timezone.utc).isoformat(),
               "status": "pass", "planes": reports,
               "checks": dict(sorted(checks.counts.items())),
               "assertions": sum(checks.counts.values()),
               "total_subsets": sum(r["point_subsets"] for r in reports),
               "certificate_sha256": hashlib.sha256(cert_path.read_bytes()).hexdigest(),
               "limit": "Exhaustive only for PG(2,2), PG(2,3); no asymptotic inference."}
    (output_dir / "fresh_checks.json").write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
