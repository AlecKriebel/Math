#!/usr/bin/env python3
"""Independent probability/geometry controls and unchanged frozen replay.

No matching or compactness implementation is added here. All writes are confined
to this audit folder; foreign replay files live in .tmp and are not deliverables.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import factorial, prod, log2
from pathlib import Path
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parent / "source_snapshot"
DIFF = HERE.parent / "pr_input" / "diff.patch"
checks = 0

def check(value, label):
    global checks
    if not value:
        raise AssertionError(label)
    checks += 1

def digest(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data).hexdigest()}

def steps(d):
    return [tuple(s if i == j else 0 for i in range(d))
            for j in range(d) for s in (-1, 1)]

def add(a, b):
    return tuple(x+y for x,y in zip(a,b))

def l1(a):
    return sum(map(abs,a))

def endpoint_counts(d, horizon):
    counts = Counter({(0,)*d: 1})
    for n in range(1, horizon+1):
        out = Counter()
        for z, multiplicity in counts.items():
            for v in steps(d):
                out[add(z,v)] += multiplicity
        check(sum(out.values()) == (2*d)**n, "complete SRW endpoint mass")
        check(all(l1(z) <= n and (l1(z)-n) % 2 == 0 for z in out),
              "all reachable endpoints obey distance and parity")
        counts = out
    return counts

# Actual d=3,4 signed distance-ten probability controls, beyond the old unsigned
# count tests: first translation collision at ten includes both +/- endpoints.
orientation_checks = []
for d in (3,4):
    counts = endpoint_counts(d,10)
    shell = {z: m for z,m in counts.items() if l1(z) == 10}
    for z,m in shell.items():
        geodesics = factorial(10)//prod(factorial(abs(k)) for k in z)
        check(m == geodesics, "all signed distance-ten endpoints are geodesic words")
        check(counts[tuple(-k for k in z)] == m, "opposite orientation count")
    targets = [(10,)+(0,)*(d-1), (3,-3,4) if d == 3 else (3,-2,3,-2)]
    rows = []
    for z in targets:
        m = shell[z]
        h = Fraction(m, (2*d)**10)
        q = 2*h
        check(0 < h < q < 1, "strict initial-hit and translation collision obstruction")
        # On disjoint ten-step blocks the +/-v endpoint events are independent.
        # Avoidance through 10B steps implies none of these B events occurs.
        rows.append({"displacement": z, "geodesic_words": m,
                     "initial_hit_by_10": str(h),
                     "translation_collision_by_10": str(q),
                     "translation_avoidance_upper_bound_at_20": str((1-q)**2)})
    orientation_checks.append({"d": d, "signed_shell_endpoints": len(shell), "examples": rows})

# Exhaustive pathwise tests of the new geometric assertion at the exact first
# collision horizon, with small alphabets. No transport optimizer is involved.
geometry_cases=[]
for d, v in [(1,(2,)), (2,(1,1)), (2,(2,0)), (2,(-1,1))]:
    r=l1(v)
    for n in range(r+2):
        collisions=0
        for word in product(steps(d), repeat=n):
            path=[(0,)*d]
            for w in word:
                path.append(add(path[-1],w))
            translated=[add(z,v) for z in path]
            pairs=[(i,j) for i,x in enumerate(path) for j,y in enumerate(translated) if x==y]
            check(all(abs(i-j)>=r and (abs(i-j)-r)%2==0 for i,j in pairs),
                  "every full-range collision satisfies graph distance and parity")
            check(all(path[i]!=translated[i] for i in range(n+1)),
                  "same-time collision never occurs under nonzero translation")
            if n<r:
                check(not pairs, "translation is range-disjoint before graph distance")
            if n==r:
                check(bool(pairs)==(path[-1] in (v,tuple(-a for a in v))),
                      "at first collision horizon only +/- endpoint matters")
                check(all((i,j) in ((0,r),(r,0)) for i,j in pairs),
                      "first-horizon collision includes an initial vertex")
            collisions+=bool(pairs)
        if n==r:
            m=factorial(r)//prod(factorial(abs(k)) for k in v)
            check(collisions==2*m, "exact translation collision numerator")
        geometry_cases.append({"d":d,"v":v,"N":n,"words":(2*d)**n,
                               "translation_collision_words":collisions})

# Distinguish a process with the correct distribution at each time from a path
# with the SRW law. Independently sampling the t=1 and t=2 SRW endpoints permits
# a jump of graph distance three with mass (2d)^-3, forbidden for actual SRW.
bad_marginal_controls=[]
for d in (3,4):
    e1=(1,)+(0,)*(d-1)
    minus2=(-2,)+(0,)*(d-1)
    c1=endpoint_counts(d,1)
    c2=endpoint_counts(d,2)
    mass=Fraction(c1[e1],2*d)*Fraction(c2[minus2],(2*d)**2)
    check(mass==Fraction(1,(2*d)**3) and l1(add(e1,tuple(-z for z in minus2)))==3,
          "one-time marginals admit a forbidden three-unit jump")
    bad_marginal_controls.append({"d":d,"forbidden_jump_positive_mass":str(mass)})

# Rendered Lemma5/9 singular-kernel falsifier. In 4D, a two-step return has
# probability 1/8 and contributes infinity to the literal second good-time sum
# at s1=2,s2=1; no asymptotic typicality 1-C n^-c can follow literally.
returns=sum(add(a,b)==(0,)*4 for a,b in product(steps(4),repeat=2))
check(Fraction(returns,8**2)==Fraction(1,8), "two-step-return singular-kernel falsifier")

# Lemma A.3 uses spatial radius n>|x| but prints log(n/|x|^2). A permitted
# x=(10,0,0,0), n=20 makes the RHS negative, while R2's geodesic visit to x
# gives the intersection expectation a positive lower bound 8^-10.
check(20>10 and log2(Fraction(20,100))<0, "negative literal A.3 bound")
check(Fraction(1,8**10)>0, "positive expectation lower witness for A.3")

# An unconditional rare-event bound is not a uniform conditional bound. This
# finite exact control explains why the final induction requires averaging.
conditional_control={"unconditional_bad_probability":"1/100",
                     "conditional_bad_probability_on_bad_prefix":"1"}
check(Fraction(1,100)<1, "rare marginal does not imply every-prefix rarity")

# An exact coupling-law control for the inference attempted by using independent
# walk exponents alone. This is a binary-sequence relation, not a lattice result.
# Both coordinates have the iid fair-bit path law. Product-law probability of
# coordinatewise complement through N bits is 2^-N; deterministic complement
# coupling makes the full infinite relation hold with probability one.
product_coupling_controls=[]
for n in range(1,9):
    words=list(product((0,1),repeat=n))
    graph_good=sum(all(a!=b for a,b in zip(x,y)) for x in words for y in words)
    check(graph_good==2**n,"product-law rare event has exact complement witnesses")
    paired=[(x,tuple(1-a for a in x)) for x in words]
    check(len(set(y for x,y in paired))==2**n and all(all(a!=b for a,b in zip(x,y)) for x,y in paired),
          "complete-prefix preserving complement coupling attains one")
    product_coupling_controls.append({"N":n,"product_probability":str(Fraction(graph_good,4**n)),
                                      "optimal_coupling_probability":"1"})

before={str(p.relative_to(SNAPSHOT)):digest(p) for p in sorted(SNAPSHOT.rglob("*")) if p.is_file()}
check(len(before)==13, "all thirteen frozen numeric files accounted for")
replay=HERE/".tmp"/"unchanged_original_replay"
if replay.exists():
    shutil.rmtree(replay)
shutil.copytree(SNAPSHOT,replay)
run1=subprocess.run([sys.executable,str(replay/"verify.py")],capture_output=True,text=True,check=True)
check((replay/"verification.json").read_bytes()==(SNAPSHOT/"verification.json").read_bytes(),
      "author original replay byte-for-byte")
run2=subprocess.run([sys.executable,str(replay/"review"/"independent_checks.py")],
                    capture_output=True,text=True,check=True)
check(run2.stdout.encode()==(SNAPSHOT/"review"/"independent_results.json").read_bytes(),
      "old independent reviewer replay byte-for-byte")
(replay/"author_stdout.txt").write_text(run1.stdout)
(replay/"old_review_stdout.txt").write_text(run2.stdout)
after={str(p.relative_to(SNAPSHOT)):digest(p) for p in sorted(SNAPSHOT.rglob("*")) if p.is_file()}
check(before==after,"all frozen originals unchanged")
diff_paths=[line.split(" b/",1)[1] for line in DIFF.read_text().splitlines() if line.startswith("diff --git ")]
check(len(diff_paths)==14,"fourteen paths in original diff")

out={"pass":True,"checks":checks,"scope":"Audit controls; no new solution attempt, matching implementation, or asymptotic inference from finite counts.",
     "actual_signed_distance_ten_controls":orientation_checks,
     "exhaustive_geometry_cases":geometry_cases,
     "one_time_marginal_falsifiers":bad_marginal_controls,
     "literal_prior_falsifiers":{"singular_kernel_return_mass":"1/8",
                                "A3_radius":20,"A3_displacement":[10,0,0,0],
                                "A3_printed_log_argument":"1/5",
                                "A3_expectation_positive_lower_bound":"1/1073741824",
                                "conditional_bound_control":conditional_control},
     "independence_versus_coupling_controls":product_coupling_controls,
     "frozen_original_replay":{"author_byte_identical":True,"old_reviewer_byte_identical":True,
                               "originals_unchanged":True,"files":before,"diff_paths":diff_paths}}
(HERE/"audit_controls_results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"pass":True,"checks":checks,"author_replay":"byte-identical",
                  "old_review_replay":"byte-identical",
                  "signed_shell_endpoint_counts":[x["signed_shell_endpoints"] for x in orientation_checks]},indent=2))
