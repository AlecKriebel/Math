#!/usr/bin/env python3
"""Independent exact controls; no source files or network access are needed.

This is a finite regression suite, not a machine proof of measure-theoretic
compactness, infinite constructions, or a solution of the pointwise problem.
"""
from bisect import bisect_left, bisect_right
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

EXPECTED_MANIFEST = "5e1638e7589229caf8667fbcd6af98b2c92f5281e32b95e690d315ea9a39cf8e"
COUNTS = Counter()


def check(group, value):
    if not value:
        raise AssertionError(group)
    COUNTS[group] += 1


def replay_author(root):
    before = {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}
    check("frozen_manifest_digest", hashlib.sha256(before["AUTHOR_MANIFEST.json"]).hexdigest() == EXPECTED_MANIFEST)
    manifest = json.loads(before["AUTHOR_MANIFEST.json"])
    check("frozen_payload_count", len(manifest["files"]) == 6)
    check("frozen_payload_bytes", sum(row["bytes"] for row in manifest["files"].values()) == 42200)
    for name, row in manifest["files"].items():
        data = before[name]
        check("frozen_payload_identity", len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"])
    result = subprocess.run([sys.executable, str(root/"verify_controls.py"), "--check-manifest"], capture_output=True, check=True)
    check("original_replay_exact_bytes", result.stdout == before["CONTROL_RESULTS.json"])
    check("original_replay_count", json.loads(result.stdout)["total_checks"] == 11515)
    check("frozen_bytes_unchanged", before == {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()})


def exact_kernel_average_controls():
    # For alpha=p/q, choose interval-endpoint distances to be qth powers.
    # The antiderivative then gives a rational average A exactly. The claimed
    # inequality A <= C_alpha |s|^-alpha is checked after positive qth powers.
    values = [F(1, 16), F(1, 3), F(1), F(7, 4), F(8)]
    for q in range(2, 10):
        for p in range(1, q):
            alpha = F(p, q)
            C_power = F(2**p)/(1-alpha)**q
            for u, v in combinations(values, 2):
                u, v = max(u, v), min(u, v)
                for crosses in (False, True):
                    if crosses:
                        s = (u**q-v**q)/2
                        r = (u**q+v**q)/2
                        A = (u**(q-p)+v**(q-p))/(2*r*(1-alpha))
                    else:
                        s = (u**q+v**q)/2
                        r = (u**q-v**q)/2
                        A = (u**(q-p)-v**(q-p))/(2*r*(1-alpha))
                    check("exact_average_positive", s > 0 and r > 0 and A > 0)
                    check("exact_average_uniform_constant", A**q*s**p <= C_power)
                # A half interval touching the singularity is also integrable.
                s = r = u**q/2
                A = u**(q-p)/(2*r*(1-alpha))
                check("exact_average_endpoint_singularity", A**q*s**p <= C_power)
            # At the center, r=(2^-n)^q makes A_r k(0) exact and divergent.
            previous = F()
            for n in range(1, 21):
                A = F(2**(n*p))/(1-alpha)
                check("center_average_divergence", A > previous and A > 2**n)
                previous = A


def rational_cantor_controls():
    parameters = [(1,3,F(1,5)), (1,2,F(1,3)), (2,3,F(3,8)),
                  (3,4,F(2,5)), (9,10,F(49,100))]
    for p, q, r in parameters:
        check("cantor_admissible_parameter", 0 < r < F(1,2) and r**p > F(1,2)**q)
        K = 2+2*r/(1-2*r)
        for depth in range(8):
            # Direct digit sum, independently of recursive interval splitting.
            starts = sorted(sum((F(bit)*(1-r)*r**j for j,bit in enumerate(bits)), F())
                            for bits in product((0,1), repeat=depth))
            L = r**depth
            ends = [x+L for x in starts]
            check("cantor_direct_cylinder_count", len(starts) == 2**depth)
            check("cantor_direct_total_length", len(starts)*L == (2*r)**depth)
            if depth:
                gap = (1-2*r)*r**(depth-1)
                check("cantor_all_adjacent_gaps", all(b-a >= gap for a,b in zip(ends,starts[1:])))
            # Counts change only when x +/- L crosses an endpoint. Evaluating
            # every such breakpoint covers the maximal closed-window count.
            critical = sorted(set([a-L for a in starts]+[b+L for b in ends]))
            for x in critical:
                count = bisect_right(starts,x+L)-bisect_left(ends,x-L)
                check("cantor_all_window_breakpoints", F(count) <= K)
                check("cantor_ball_mass_bound", F(count,2**depth) <= K/F(2**depth))


def solve2(a,b):
    (a0,a1,c),(b0,b1,d) = a,b
    determinant = a0*b1-a1*b0
    if determinant == 0:
        return None
    return ((c*b1-a1*d)/determinant, (a0*d-c*b0)/determinant)


def finite_duality_controls():
    # A finite positive matrix analogue of min mass / bounded-potential dual.
    # Enumerate all vertices separately on each side, including degenerate and
    # zero-obstacle cases. This cannot justify the infinite-dimensional step.
    entries = (F(1,3), F(1), F(3))
    obstacles = ((F(),F()), (F(),F(2)), (F(2),F()), (F(1),F(1)),
                 (F(2),F(1,2)), (F(1,2),F(2)))
    for a,b,c,d in product(entries,repeat=4):
        for y0,y1 in obstacles:
            primal_lines = [(a,b,y0),(c,d,y1),(F(1),F(),F()),(F(),F(1),F())]
            primal=[]
            for l1,l2 in combinations(primal_lines,2):
                point=solve2(l1,l2)
                if point is not None:
                    u,v=point
                    if u>=0 and v>=0 and a*u+b*v>=y0 and c*u+d*v>=y1:
                        primal.append(u+v)
            dual_lines = [(a,c,F(1)),(b,d,F(1)),(F(1),F(),F()),(F(),F(1),F())]
            dual=[]
            for l1,l2 in combinations(dual_lines,2):
                point=solve2(l1,l2)
                if point is not None:
                    u,v=point
                    if u>=0 and v>=0 and a*u+c*v<=1 and b*u+d*v<=1:
                        dual.append(y0*u+y1*v)
            check("finite_primal_dual_feasibility", bool(primal) and bool(dual))
            check("finite_primal_dual_equality", min(primal)==max(dual))
            check("finite_zero_mass_corner", (min(primal)==0)==(y0==0 and y1==0))
    # Coordinatewise feasibility is inadequate: both coordinate constraints
    # require the whole budget, while their positive sum separates them.
    C=F(1)
    for cross in (F(1,10),F(1,3),F(3,4)):
        check("positive_combination_separation", 2*C > C*(1+cross))


def additional_scope_controls():
    # Rational versions of the dyadic spike scaling for many alpha=p/q.
    for q in range(2,10):
        for p in range(1,q):
            ratio=F(1,2**q)
            for n in range(1,16):
                length=ratio**n
                height=F(2**(p*n))
                mass=F(1,2**(p*n))
                tail=length/(1-ratio)
                check("general_rational_spike_scaling", length**p==mass**q)
                check("general_rational_spike_pairing", height*mass==1)
                check("general_rational_atomic_bound", height**q*tail**p==1/(1-ratio)**p)
                check("general_rational_integrability", F(2**p)*ratio<1)
    # Countable atomic repair retains an arbitrarily small total mass even if
    # points repeat, or form a dense set; its measure support need not be discrete.
    for N in range(1,101):
        epsilon=F(1,N)
        weights=[epsilon/F(2**j) for j in range(1,N+1)]
        check("atomic_repair_exact_budget", sum(weights,F())==epsilon*(1-F(1,2**N)))
        check("atomic_repair_positive_weights", min(weights)>0)
        # Each [2^-j,2^(-j+1)] contributes at least 1/2 to int dx/x.
        check("interval_cover_pairing_divergence", sum((F(1,2) for j in range(N)),F())==F(N,2))
    # This compactly supported test vanishes identically on atoms escaping to
    # infinity; probability mass is not weak-star continuous on C_0(R).
    for radius in range(1,21):
        for n in range(radius+1,radius+21):
            tent=max(F(),1-F(n,radius))
            check("c0_mass_escape", tent==0)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--author-dir", type=Path, default=Path(__file__).resolve().parent.parent/"author")
    args=parser.parse_args()
    replay_author(args.author_dir)
    exact_kernel_average_controls()
    rational_cantor_controls()
    finite_duality_controls()
    additional_scope_controls()
    print(json.dumps({"schema":"function-theory-2305073-independent-exact-controls/v1",
        "result":"PASS", "arithmetic":"Python standard-library Fraction; no floating point",
        "original_checks_replayed":11515, "original_stdout_byte_exact":True,
        "independent_counts":dict(sorted(COUNTS.items())),
        "independent_total_checks":sum(COUNTS.values()),
        "scope":"Finite regression checks only; the analytic proofs are reviewed in INDEPENDENT_AUDIT.md."},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
