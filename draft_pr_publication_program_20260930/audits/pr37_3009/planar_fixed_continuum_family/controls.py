#!/usr/bin/env python3
"""Replayable exact hypothesis/boundary controls; no topological certificate."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
checks = {}

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"

def norm2(x):
    return sum(t*t for t in x)

def chordal2(x, y):
    return 4*norm2(tuple(a-b for a,b in zip(x,y)))/((1+norm2(x))*(1+norm2(y)))

def seal_valid(data, expected):
    return hashlib.sha256(data).hexdigest() == expected

frozen = json.loads((AUDIT / "snapshot_manifest.json").read_text())
for entry in frozen["files"]:
    if entry["path"] not in {"source_record.json", "PARTIAL.md"}:
        continue
    data = (AUDIT / "source_snapshot" / entry["path"]).read_bytes()
    check("frozen_" + entry["path"], seal_valid(data, entry["sha256"]))
    check("bit_flip_detected_" + entry["path"], not seal_valid(data[:-1]+bytes([data[-1]^1]), entry["sha256"]))

# The zero-bound case must precede the ball construction: B(a,0) is empty.
check("zero_bound_requires_identity_branch", not F(0) < F(0))

# The base-ball witness is safely interior even at |h^k(a)-a|=D.
for D in (F(1,10), F(1), F(1000)):
    check(f"common_member_witness_margin_D{D}", D < 2*D)
    check(f"closed_fixed_regions_strictly_disjoint_D{D}", 7*D > 6*D)
    check(f"tangent_regions_do_not_certify_distinct_points_D{D}", not 6*D > 6*D)
    for R in (D+F(1,10), 2*D, 10*D):
        B = 4*D*D/((1+R*R)*(1+(R-D)**2))
        for radius in (R, R+D, 2*R):
            for ex,ey in ((-D,F(0)),(D,F(0)),(F(0),D),(3*D/5,4*D/5)):
                x=(radius,F(0)); y=(radius+ex,ey)
                check(f"tail_R{R}_D{D}_r{radius}_e{ex},{ey}", chordal2(x,y)<=B)
                for t in (F(0),F(1,3),F(1)):
                    H=(radius+t*ex,t*ey)
                    check(f"proper_R{R}_D{D}_r{radius}_e{ex},{ey}_t{t}", norm2(H)>=(radius-D)**2)

# Counterexample to replacing one common bound by individually bounded orbits:
# half-turn h(x)=-x is recurrent, fixes only 0, and diam(orbit(x))=2|x|.
D=F(1); a=(F(10),F(0)); ha=(-a[0],-a[1])
check("half_turn_period_two", tuple(-t for t in ha)==a)
check("individual_orbit_bound_does_not_supply_common_D", norm2(tuple(t-s for t,s in zip(ha,a)))>D*D)
check("half_turn_breaks_proposed_union_intersection_without_common_bound", norm2(tuple(t-s for t,s in zip(ha,a)))>(4*D)**2)

# The invariant unit circle is separating and contains no half-turn fixed point.
# Its filled disk contains the fixed origin. Omitting the filling step is unsafe.
check("circle_without_nonseparation_rejects_CL", norm2((F(0),F(0))) != F(1))
check("filled_circle_contains_fixed_origin", norm2((F(0),F(0))) <= F(1))

# Sphere reflection (x,y,z)->(x,y,-z) is a nonidentity recurrent map fixing
# the entire equator; it refutes an orientation-free two-fixed-point theorem.
equator=((F(1),F(0),F(0)),(F(0),F(1),F(0)),(F(-1),F(0),F(0)))
check("orientation_reversing_sphere_has_three_distinct_fixed_points", len(set(equator))==3 and all((x,y,-z)==(x,y,z) for x,y,z in equator))
check("sphere_reflection_nonidentity", (F(0),F(0),F(-1)) != (F(0),F(0),F(1)))

# Compact-supported radial twist angle 2*pi*r in the unit disk, identity
# outside: full orbit diameters <=2 and boundary fixed, but no uniform return.
# For every m>=1, r=1-1/(2m), m*r=m-1/2 and displacement 2r>=1.
for m in range(1,101):
    r=1-F(1,2*m)
    check(f"twist_exact_half_turn_after_m{m}", m*r==m-F(1,2))
    check(f"twist_no_uniform_disk_return_m{m}", 2*r>=1)

# Greater-dimensional final-count obstruction: diag(-1,-1,1,1) on S^3.
M=(-1,-1,1,1)
check("S3_rotation_orientation_preserving", M[0]*M[1]*M[2]*M[3]==1)
check("S3_rotation_period_two_nonidentity", all(v*v==1 for v in M) and M!=(1,1,1,1))
check("S3_rotation_fixed_circle_samples", all(tuple(v*w for v,w in zip(M,p))==p for p in ((0,0,1,0),(0,0,0,1),(0,0,-1,0))))

result={"passed":len(checks),"failed":0,"scope":"Exact rational boundary, hypothesis counterexample, and frozen-byte corruption controls. These do not certify connectedness, nonseparation, or any imported theorem.","checks":checks}
(HERE / "control_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))
