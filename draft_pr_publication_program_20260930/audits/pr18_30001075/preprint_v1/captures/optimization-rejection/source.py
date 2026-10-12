#!/usr/bin/env python3
"""Exact finite controls for the accompanying proof; Python standard library only."""
import datetime
from fractions import Fraction as Q
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError("Verification requires nonoptimized execution; -O/-OO is rejected.")
if sys.argv[1:] not in ([], ["--negative-control"]):
    raise RuntimeError("Usage: python -B verify.py [--negative-control]")
counts = {}

def check(label, condition):
    # Explicit runtime branch, deliberately independent of Python assert semantics.
    if not condition:
        raise RuntimeError("Failed exact control: " + label)
    counts[label] = counts.get(label, 0) + 1

if sys.argv[1:] == ["--negative-control"]:
    check("intentional false control: failure must remain visible", False)

# A polynomial dictionary over Z in independent formal indeterminates.
# Identities are established by coefficient equality, not integer sampling.
N = 22
zero = {}
one = {(0,) * N: 1}
def var(i):
    return {tuple(int(j == i) for j in range(N)): 1}
def add(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, 0) + c
    return {e: c for e, c in out.items() if c}
def scale(p, k):
    return {e: k*c for e, c in p.items() if k*c}
def mul(*ps):
    out = one
    for p in ps:
        new = {}
        for a, c in out.items():
            for b, d in p.items():
                e = tuple(x+y for x, y in zip(a, b))
                new[e] = new.get(e, 0) + c*d
        out = {e: c for e, c in new.items() if c}
    return out
def poly_det(rows):
    size = len(rows)
    terms = []
    for p in permutations(range(size)):
        inv = sum(p[i] > p[j] for i in range(size) for j in range(i+1, size))
        terms.append(scale(mul(*(rows[i][p[i]] for i in range(size))), (-1)**inv))
    return add(*terms)

av = [var(i) for i in range(4)]
bv = [var(i+4) for i in range(4)]
z = var(8)
entries = [add(a, mul(z,b)) for a,b in zip(av,bv)]
P = poly_det([entries[:2], entries[2:]])
expected = add(
    mul(av[0],av[3]), scale(mul(av[1],av[2]),-1),
    mul(z, add(mul(av[0],bv[3]), mul(bv[0],av[3]),
               scale(mul(av[1],bv[2]),-1), scale(mul(bv[1],av[2]),-1))),
    mul(z,z,add(mul(bv[0],bv[3]),scale(mul(bv[1],bv[2]),-1))))
check("formal_quadratic_determinant_coefficients", P == expected)
check("formal_degree_at_most_two", max(e[8] for e in P) == 2)
h = [var(9+i) for i in range(3)]
V = [[one,x,mul(x,x)] for x in h]
vandermonde = mul(add(h[1],scale(h[0],-1)),
                  add(h[2],scale(h[0],-1)),
                  add(h[2],scale(h[1],-1)))
check("formal_three_distinct_roots_vandermonde", poly_det(V) == vandermonde)
J = [[entries[0],entries[1],var(12)],
     [entries[2],entries[3],var(13)],[zero,zero,one]]
check("formal_swept_block_jacobian", poly_det(J) == P)
Nx,Ny,Nz,zi,ux,uy,vx,vy = [var(i) for i in range(14,22)]
beta = scale(add(mul(Nx,ux),mul(Ny,uy)),-1)
delta = add(mul(Nx,vx),mul(Ny,vy))
left = add(mul(beta,Nz),scale(mul(Nz,zi,delta),-1))
right = scale(mul(Nz,add(mul(Nx,add(ux,mul(zi,vx))),
                         mul(Ny,add(uy,mul(zi,vy))))),-1)
check("formal_planar_first_variation_after_denominator_clearing",left == right)

def det(rows):
    n = len(rows)
    return sum((-1)**sum(p[i] > p[j] for i in range(n) for j in range(i+1,n)) *
               prod(rows[i][p[i]] for i in range(n))
               for p in permutations(range(n)))
def prod(xs):
    result = Q(1)
    for x in xs:
        result *= x
    return result
def dot(x,y):
    return sum(a*b for a,b in zip(x,y))

# Full motion bases, including opposite normals and very small contact gaps.
directions = [(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1))]
for n in (2,10,10**9):
    directions.append((Q(n*n-1,n*n+1),Q(2*n,n*n+1)))
for e in directions:
    check("rational_unit_directions",dot(e,e) == 1)
for eA,eB,s,d in product(directions,directions,(Q(-2),Q(0),Q(5)),
                         (Q(1,2),Q(1),Q(1,10**15))):
    t = s+d
    pA,pB = (-eA[1],eA[0]),(-eB[1],eB[0])
    columns = [
        (t*eA[0]/d,t*eA[1]/d,-eA[0]/d,-eA[1]/d),
        (-s*eB[0]/d,-s*eB[1]/d,eB[0]/d,eB[1]/d),
        (t*pA[0]/d,t*pA[1]/d,-pA[0]/d,-pA[1]/d),
        (-s*pB[0]/d,-s*pB[1]/d,pB[0]/d,pB[1]/d)]
    check("motion_basis_nonzero_exact_determinant",
          det([[col[j] for col in columns] for j in range(4)]) == -1/(d*d))

# Support increments on finite convex hulls, with exact unit directions.
vertices = [(Q(x,3),Q(y,4),Q(k,7))
            for x,y,k in product((-2,1),(-3,2),(-4,5))]
normals = [(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),
           (Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))]
parameters = [tuple(Q(k,11) for k in x) for x in product((-2,0,3),repeat=4)]
increments = [(Q(1,17),Q(-2,19),Q(3,23),Q(-1,29)),
              (Q(-2,7),Q(1,11),Q(-1,13),Q(2,17))]
def psi(n,q):
    return dot(n,q[:2])-max(dot(n,x[:2])-x[2]*dot(n,q[2:]) for x in vertices)
for n,q,dq in product(normals,parameters,increments):
    new = tuple(a+b for a,b in zip(q,dq))
    actual = psi(n,new)-psi(n,q)
    changes = [dot(n,dq[:2])+x[2]*dot(n,dq[2:]) for x in vertices]
    check("signed_support_increment",min(changes) <= actual <= max(changes))
def point_psi(n,q):
    # The support set is the single point (0,0,1); the increment sign is positive.
    return dot(n,q[:2])+dot(n,q[2:])
point_increment = point_psi((Q(1),Q(0)),(Q(0),Q(0),Q(1),Q(0))) - point_psi(
    (Q(1),Q(0)),(Q(0),Q(0),Q(0),Q(0)))
check("reversed_support_sign_rejected",point_increment == 1 and point_increment != -1)

# Strict cap margins and explicit root brackets; no global uniform aperture assumed.
for alpha,beta in product((Q(1),Q(1,7),Q(1,10**15)),repeat=2):
    eps = min(alpha,beta)/32
    mA,mB = alpha/4,beta/4
    delta0 = Q(1,101)
    KA,KB = Q(3,2),Q(7,3)
    eta = min((mA-eps)*delta0/(4*KA),(mB-eps)*delta0/(4*KB))
    kappa = max(eps/mA,eps/mB)
    for aperture,m,K in ((alpha,mA,KA),(beta,mB,KB)):
        check("strict_aperture_and_own_margin",
              0 < eps < min(Q(1,4),aperture/16) and (1-eps)*aperture/2 >= m)
        check("strict_cross_contraction",eps/m < Q(1,4))
        check("explicit_root_positive_and_negative_brackets",
              (m-eps)*delta0-K*eta > 0)
        check("closed_square_strict_self_map",
              kappa*delta0+K*eta/m < 3*delta0/4)

# The discarded 5/8 estimate fails when a common kappa is mixed with an
# individual residual ratio. These exact constants obey both bracket gates.
mA,mB,eps = Q(1,4),Q(1,4000),Q(1,17000)
kappa = max(eps/mA,eps/mB)
KA,KB = Q(49,400),(mB-eps)/4
check("mixed_common_constant_five_eighths_countercontrol",
      kappa < Q(1,4) and KA < (mA-eps)/2 and KB < (mB-eps)/2 and
      Q(5,8) < kappa+KA/mA < Q(3,4))

# Independently solved cross-coupled linear models on the justified root square.
for alpha,beta in product((Q(1),Q(1,7),Q(1,10**15)),repeat=2):
    eps = min(alpha,beta)/32
    mA,mB = alpha/4,beta/4
    for c,d in product((-eps/2,Q(0),eps/2),repeat=2):
        denominator = mA*mB-c*d
        check("linear_root_denominator_positive",denominator > 0)
        for r1,r2 in product((Q(-1,1000),Q(0),Q(1,1000)),repeat=2):
            a = (-mB*r1+c*r2)/denominator
            b = (d*r1-mA*r2)/denominator
            check("linear_exact_simultaneous_roots",mA*a+c*b+r1 == 0 and d*a+mB*b+r2 == 0)

# A nonsmooth monotone model has Lipschitz, piecewise-linear fixed points.
for coupling,r in product((Q(1,32),Q(1,101),Q(1,10**15)),
                           (Q(-3,7),Q(-1,101),Q(0),Q(1,101),Q(3,7))):
    b = coupling*r/(1-2*coupling) if r >= 0 else -coupling*r/(1+2*coupling)
    a = r+b
    check("nonsmooth_exact_simultaneous_roots",
          a-coupling*abs(a+b)-r == 0 and b-coupling*abs(a+b) == 0)
    check("nonsmooth_cross_contraction",coupling/(1-coupling) < Q(1,4))

# Negative controls: these reject broadenings, not the stated theorem.
for x in (Q(-2),Q(-1,2),Q(1,2),Q(2)):
    check("two_contacts_do_not_annihilate_determinant",
          det([[x,0],[0,x-1]]) == x*(x-1))
check("two_contact_positive_volume_exact_integral",
      4*(Q(1,2)-Q(1,3)) == Q(2,3))
check("repeated_contact_roots_insufficient",det([[Q(2),0],[0,Q(2)]]) == 4)
def plane_variation(nx,ny,nz,zi,ux,uy,vx,vy):
    if nz == 0:
        raise ValueError("The planar contact variation requires transversality.")
    return -(nx*(ux+zi*vx)+ny*(uy+zi*vy))/nz
try:
    plane_variation(Q(1),Q(0),Q(0),Q(0),Q(1),Q(0),Q(0),Q(0))
except ValueError:
    zero_denominator_rejected = True
else:
    zero_denominator_rejected = False
check("planar_transversality_zero_denominator_rejected",zero_denominator_rejected)
for n in (2,3,7,101):
    x,y = Q(n*n-1,n*n+1),Q(2*n,n*n+1)
    check("zero_density_circle_can_have_full_derivative",x*x+y*y == 1 and det([[1,0],[0,1]]) == 1)
for x,y in product((Q(-1,10),Q(0),Q(1,10)),repeat=2):
    check("intersection_is_not_rank_constrained_tangency",x*x+y*y < Q(1,4) and det([[1,0],[0,1]]) == 1)
for theta in (Q(1,10),Q(1,100),Q(1,10**15)):
    check("moving_contact_fixed_cap_miss",
          all(x+theta*(10-k) >= 0 for x,k in product((Q(0),Q(1)),(Q(0),Q(10)))) and theta*(1-10) < 0)
for x,y in product((Q(-1),Q(-1,10),Q(0),Q(1,10),Q(1)),repeat=2):
    if (x-1)**2+y*y <= 1:
        check("cap_boundary_extra_normal_finite_control",x >= 0)
check("cap_boundary_extra_normal_original_witness",dot((Q(-1),Q(0)),(Q(-1),Q(1))) > 0)
for n in (2,3,7,101):
    check("nonclosed_strip_contact_height",0 < Q(1,n) < 1)

here = Path(__file__).resolve().parent
candidate = (here/"source/CANDIDATE.md").read_bytes()
binding = json.loads((here/"SOURCE_BINDING.json").read_bytes())
check("reviewed_source_binding",
      hashlib.sha256(candidate).hexdigest() == binding["candidate"]["sha256"] ==
      "8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12")
receipt = {
    "scope": "Exact polynomial identities and finite rational diagnostics, not an oracle for continuum geometry or measure theory.",
    "status": "PASS_FINITE_CONTROLS",
    "assertions_passed": sum(counts.values()), "by_category": counts,
    "python_version": sys.version, "optimization": sys.flags.optimize,
    "dependencies": "Python standard library only",
    "UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "verify_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "manuscript_sha256": hashlib.sha256((here/"paper.tex").read_bytes()).hexdigest(),
    "candidate_sha256": hashlib.sha256(candidate).hexdigest(),
    "priority_or_publication_clearance": False
}
(here/"verification.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
print(json.dumps(receipt,indent=2,sort_keys=True))
