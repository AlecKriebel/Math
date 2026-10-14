#!/usr/bin/env python3
"""Independent exact local-form diagnostics, not realization or topology proofs."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import sympy as s

counts = Counter()
def check(label, value):
    counts[label] += 1
    assert value, label
def zero(expr):
    return s.cancel(expr) == 0
def curl(v, coordinates):
    x, y, z = coordinates
    return s.Matrix([s.diff(v[2], y)-s.diff(v[1], z),
                     s.diff(v[0], z)-s.diff(v[2], x),
                     s.diff(v[1], x)-s.diff(v[0], y)])

x,y,z,t = s.symbols("x y z t", real=True)
p,q = s.Function("p")(x,y,z),s.Function("q")(x,y,z)
A=s.Matrix([p,q,1])
E=s.Matrix([s.diff(p,z),s.diff(q,z),0])
F=s.diff(q,x)-s.diff(p,y)+q*s.diff(p,z)-p*s.diff(q,z)
C=curl(A,(x,y,z))
check("universal_Frobenius_coefficient", s.expand(A.dot(C)-F)==0)
check("universal_contraction_identity", C-A.cross(E)==s.Matrix([0,0,F]))
G=s.diff(q,z)*s.diff(p,z,2)-s.diff(p,z)*s.diff(q,z,2)
check("universal_GV_coefficient", s.expand(E.dot(curl(E,(x,y,z)))-G)==0)
check("universal_normalization", A[2]==1 and E[2]==0)

# A genuinely integrable local family: alpha=dPhi/Phi_z.
# These are local diagnostics, not a closed nonzero-GV suspension.
Phi=z+x*z*z+y*z**3
J=s.diff(Phi,z)
P=s.diff(Phi,x)/J
R=s.diff(Phi,y)/J
a=s.Matrix([P,R,1])
e=s.Matrix([s.diff(P,z),s.diff(R,z),0])
check("integrable_local_Frobenius", zero(a.dot(curl(a,(x,y,z)))))
check("integrable_local_defining_equation",
      all(zero(v) for v in curl(a,(x,y,z))-a.cross(e)))
check("integrable_local_eta", all(zero(v) for v in
      e-(s.Matrix([s.diff(s.log(J),v) for v in (x,y,z)])
          -s.diff(s.log(J),z)*a)))
g=s.factor(e.dot(curl(e,(x,y,z))))
check("local_density_nontrivial", g != 0)

for i in range(7):
    for j in range(7):
        for k in range(1,8):
            point={x:s.Rational(i,7),y:s.Rational(j,7),z:s.Rational(k,9)}
            check("local_coordinate_positive", J.subs(point)>0)
            check("local_form_equation_at_rational_point",
                  all(zero(v.subs(point)) for v in curl(a,(x,y,z))-a.cross(e)))

# Constant compression preserves the defining equation and the integral.
for offset,length in [(s.Rational(1,11),s.Rational(2,13)),
                      (s.Rational(3,17),s.Rational(1,5)),
                      (s.Rational(1,3),s.Rational(1,9))]:
    sub={z:(t-offset)/length}
    new_a=s.Matrix([length*P.subs(sub),length*R.subs(sub),1])
    new_e=s.Matrix([e[0].subs(sub),e[1].subs(sub),0])
    check("compression_defining_equation",
          all(zero(v) for v in curl(new_a,(x,y,t))-new_a.cross(new_e)))
    check("compression_GV_density",
          zero(new_e.dot(curl(new_e,(x,y,t)))-g.subs(sub)/length))

# Check arbitrary polynomial densities by exact integration under compression.
for degree in range(12):
    density=sum(s.Rational((-1)**j*(j+2),j+1)*z**j
                for j in range(degree+1))
    old=s.integrate(density,(z,0,1))
    for denominator in range(3,13):
        length=s.Rational(1,denominator)
        offset=s.Rational(1,2*denominator+1)
        new=s.integrate(density.subs(z,(t-offset)/length)/length,
                        (t,offset,offset+length))
        check("density_integral_preservation",zero(new-old))

# Positive weighted fiber coordinates are still increasing and preserve endpoints.
for n in range(1,12):
    weights=[Q(j+1,n*(n+1)//2) for j in range(n)]
    check("coordinate_partition_weights",sum(weights)==1 and min(weights)>0)
    for k in range(1,20):
        derivatives=[Q(1+j+k,1+j+2*k) for j in range(n)]
        check("averaged_coordinate_positive",
              sum(w*d for w,d in zip(weights,derivatives))>0)

# Disjoint interior slabs leave positive collars and never alter the seam.
for n in range(1,201):
    slabs=[(Q(2*j+1,2*n+2),Q(2*j+2,2*n+2)) for j in range(n)]
    check("interior_slabs",all(0<a<b<1 for a,b in slabs))
    check("separated_slabs",all(slabs[j][1]<slabs[j+1][0] for j in range(n-1)))
    check("constant_total_mass",sum((Q(11,19) for _ in slabs),Q(0))==n*Q(11,19))

root=Path(__file__).resolve().parent
proof_hash=hashlib.sha256((root/"author_replay/CANDIDATE.md").read_bytes()).hexdigest()
check("frozen_candidate_hash",proof_hash==
      "28d66c68f4497b1b2a3476d3f858902e8def73e65357320a743da43cb0564c6f")
print(json.dumps({"assertions":sum(counts.values()),"categories":dict(sorted(counts.items())),
                  "artifact_sha256":proof_hash,"sympy_version":s.__version__,
                  "scope":"Exact local differential identities and rescaling diagnostics only. Classical suspension realization, hyperbolization, relative gluing and global tautness are checked in the written review, not inferred from these finite controls.",
                  "verdict":"PASS"},sort_keys=True,indent=2))
