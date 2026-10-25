"""Fresh exact falsification controls, written before reading submitted verify.py.

This finite calculation is neither a convex-set oracle nor a universal proof.
The independent analytic ball-family classification is recorded in REVIEW.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, random, datetime

if not __debug__:
    raise RuntimeError('Exact assertions must be enabled')
counts = {}
def ck(group, truth):
    counts[group] = counts.get(group, 0)+1
    assert truth, group
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(t,a): return tuple(t*x for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def det(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def md(A,B,z):return det([[A[i][j]+z*B[i][j] for j in range(2)] for i in range(2)])
seed = 23127955
rng=random.Random(seed)
def rf():return F(rng.randrange(-8,9),rng.randrange(1,8))

# Equal radius balls with centres (0,0,z_i), z_i=0,3,6.
# Squared distance times |d|^2 is |(z e3-p) x d|^2.
# Three tangencies force a quadratic to vanish identically; its leading
# coefficient is d_x^2+d_y^2, so the line is vertical. Conversely vertical
# lines at transverse radius one meet all three disjoint balls tangentially.
for k in range(1200):
    p=tuple(rf() for _ in range(3));d=tuple(rf() for _ in range(3))
    if not any(d): d=(F(0),F(0),F(1))
    C=cross(mul(-1,p),d);D=cross((0,0,1),d)
    coeff=(dot(C,C)-dot(d,d),2*dot(C,D),dot(D,D))
    ck('equal_ball_leading_coefficient',coeff[2]==d[0]**2+d[1]**2)
    for z in (-5,0,3,6,F(11,7)):
        val=dot(cross(sub((0,0,z),p),d),cross(sub((0,0,z),p),d))-dot(d,d)
        ck('equal_ball_distance_polynomial',val==coeff[0]+coeff[1]*z+coeff[2]*z*z)
    if all(coeff[0]+coeff[1]*z+coeff[2]*z*z==0 for z in (0,3,6)):
        ck('three_ball_tangency_classification',coeff==(0,0,0) and d[0]==d[1]==0)
for t in [F(i,17) for i in range(-80,81)]:
    p=((1-t*t)/(1+t*t),2*t/(1+t*t),F(0));d=(0,0,1)
    for z in (0,3,6):
        ck('three_ball_exact_positive_family',dot(cross(sub((0,0,z),p),d),cross(sub((0,0,z),p),d))==1)

# An entire fixed cap can be missed by nearby tangents to the original box.
# A=[-1,0]x[-1,1]x[0,1], L_delta=(delta*(1-z),0,z).
# x+delta*z=delta is supporting, contacts occur only at z=1, so no contact
# can lie in a ball of radius 1/10 around (0,0,1/4).
box=list(product((F(-1),F(0)),(F(-1),F(1)),(F(0),F(1))))
for k in range(1,31):
    delta=F(1,2**k)
    ck('fixed_cap_miss_support',max(x+delta*z for x,y,z in box)==delta)
    ck('fixed_cap_miss_contact',(F(1)-F(1,4))**2>F(1,10)**2)
    for z in [F(i,10) for i in range(10)]:
        ck('fixed_cap_miss_unique_contact',delta*(1-z)>0)

# Independent exact support-increment verification on arbitrary finite vertex
# hulls, with affine dimension determined by the selected vertices. No smooth
# support function is assumed or evaluated. Raw rational normals suffice.
for k in range(2400):
    vertices=[tuple(rf() for _ in range(3)) for _ in range(rng.randrange(1,10))]
    n=tuple(rf() for _ in range(2));u=tuple(rf() for _ in range(2));v=tuple(rf() for _ in range(2))
    du=tuple(rf() for _ in range(2));dv=tuple(rf() for _ in range(2))
    def psi(uu,vv):return dot(n,uu)-max(n[0]*(x-z*vv[0])+n[1]*(y-z*vv[1]) for x,y,z in vertices)
    inc=psi(add(u,du),add(v,dv))-psi(u,v)
    bounds=[dot(n,add(du,mul(z,dv))) for x,y,z in vertices]
    ck('nonsmooth_support_increment',min(bounds)<=inc<=max(bounds))

# Exhaustive small matrix pencils: three distinct roots annihilate the full
# quadratic; two repeated roots alone demonstrably do not.
matrices=[((a,b),(c,d)) for a,b,c,d in product((-1,0,1),repeat=4)]
for A in matrices:
    for B in matrices:
        c0=det(A);c2=det(B);c1=md(A,B,1)-c0-c2
        ck('matrix_pencil_coefficients',all(md(A,B,z)==c0+c1*z+c2*z*z for z in (-3,0,1,4)))
        if all(md(A,B,z)==0 for z in (-2,0,3)):
            ck('three_distinct_contact_heights',c0==c1==c2==0)

# Fresh negative controls addressing tempting false extensions.
# (i) Three disjoint planes have empty ambient interior, but a transverse
# line is not contained in any of their unique supporting planes.
vertical=(0,0,1)
ck('negative_empty_interior_definition',dot(vertical,(0,0,1))!=0)
# (ii) Independent two-contact family through transverse horizontal segments:
# (s,0,0), (0,t,2). Sweep=((1-z/2)*s,(z/2)*t,z), Jacobian=(1-z/2)*z/2.
A=((F(1),F(0)),(F(0),F(0)));B=((F(-1,2),F(0)),(F(0),F(1,2)))
ck('negative_two_contacts',md(A,B,0)==md(A,B,2)==0 and md(A,B,1)==F(1,4))
# (iii) Three identical singleton sets allow the two-parameter family through
# 0, F(q)=(0,q), whose sweep Jacobian z^2 is nonzero away from the repeated contact.
A=((0,0),(0,0));B=((1,0),(0,1))
ck('negative_repeated_contacts',md(A,B,0)==0 and md(A,B,1)==1)
# (iv) Vertical lines tangent to the unit ball at the parameter circle have
# transverse derivative I; this does not contradict an a.e. density-one lemma.
ck('negative_missing_density',det(((1,0),(0,1)))==1)
# (v) Arbitrary line transversals to three disjoint balls can have rank two:
# q in a small disk, vertical through q, intersects all interiors; not supporting.
for q in [(F(0),F(0)),(F(1,3),F(1,4)),(F(-1,4),F(1,5))]:
    ck('negative_interior_transversals',dot(q,q)<1)

result={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'seed':seed,'assertions':sum(counts.values()),'groups':counts,
        'negative_extension_controls':5,
        'scope':'Finite exact controls and an independently derived three-collinear-equal-balls classification; not a universal convex-set or measure-theory proof.',
        'submitted_verifier_read_before_this_run':False}
Path(__file__).with_name('fresh-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
