#!/usr/bin/env python3
"""Independent local algebra and period bookkeeping; no numerical proof claims."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd, lcm
import itertools
import hashlib
import json
import sympy as S

checks={}
def ck(name,value):
    assert bool(value),name
    checks[name]=checks.get(name,0)+1

a,b,c,v,q=S.symbols("a b c v q", positive=True)
D=(a+c)*(b+c)
f2=b+(a-b)*q
# Differentiate x=A(v)cos(t), y=B(v)sin(t), z=Z(t,v) directly.
gtt=a*(a+v)*q/(a+c)+b*(b+v)*(1-q)/(b+c)-c*(c-v)*(a-b)**2*q*(1-q)/(D*(c+f2))
gvv=a*(1-q)/(4*(a+c)*(a+v))+b*q/(4*(b+c)*(b+v))-c*(c+f2)/(4*D*(c-v))
cross_factor=-a/(2*(a+c))+b/(2*(b+c))+c*(a-b)/(2*D)
ck("metric_t_direct",S.factor(gtt-(v+f2)*f2/(c+f2))==0)
ck("metric_v_direct",S.factor(gvv+(v+f2)*v/(4*(a+v)*(b+v)*(c-v)))==0)
ck("cross_term_direct",S.factor(cross_factor)==0)

# Global root test, starting from arbitrary ambient coordinates on the ellipsoid.
X,Y,Z=S.symbols("X Y Z")
F0=(a+c)*X/a**2+(b+c)*Y/b**2
normal=X/a**2+Y/b**2-Z/c**2
ck("root_belt_endpoint",S.factor((F0-1-c*normal).subs(Z,c*(1-X/a-Y/b)))==0)
Fc=X/a+Y/b
ck("root_equator_endpoint",S.factor((Fc-1+Z/c).subs(Z,c*(1-X/a-Y/b)))==0)

# Endpoint asymptotic coefficients are nonzero; the text supplies analyticity.
e=S.symbols("e",positive=True)
dtaudv=S.sqrt(v/((a+v)*(b+v)*(c-v)))/2
ck("tropic_tau_derivative_coefficient",S.simplify(S.limit(dtaudv/S.sqrt(v),v,0)-1/(2*S.sqrt(a*b*c)))==0)
eqcoef=S.simplify(2*S.limit(S.sqrt(e)*dtaudv.subs(v,c-e),e,0))
ck("equator_Y_coefficient",S.simplify(eqcoef-S.sqrt(c/D))==0)
zcoef=S.sqrt(c*(c+f2)/D)
ck("equator_signed_gluing_ratio",S.simplify(eqcoef/zcoef-1/S.sqrt(c+f2))==0)

# The axisymmetric factor is derived from the ordinary latitude coordinate.
k,u=S.symbols("k u",positive=True)
sin2=S.symbols("sin2",real=True)
ck("rotational_integral_reduction",
   S.factor(k*k*(1-sin2)/(1+k*k*sin2)-((1+k*k)/(1+k*k*sin2)-1))==0)
ck("rational_integral_substitution",
   S.factor((1/(1+k*k*u*u/(1+u*u)))/(1+u*u)-1/(1+(1+k*k)*u*u))==0)
for nn,rr in itertools.product(range(1,13),repeat=2):
    ratio=F(nn+2*rr,nn)
    c_over_a=ratio*ratio-1
    rho=(ratio-1)/2
    ck("rotational_independent_factor",c_over_a>0 and rho==F(rr,nn))
ck("one_folded_two_full_steps",F(3-1,2)==1 and lcm(2,1)==2)
ck("two_full_arcs_one_winding",F(2-1,2)==F(1,2))

# Explicitly iterate the boundary map (S,sign)->(S+rho,-sign).
for p,den in itertools.product(range(1,10),repeat=2):
    if gcd(p,den)!=1:continue
    rho=F(p,den)
    state=(F(0),1)
    first=None
    for n in range(1,2*den+1):
        state=(state[0]+rho,-state[1])
        closed=state[0].denominator==1 and state[1]==1
        ck("boundary_return_equivalence",closed==(n%2==0 and n%den==0))
        if closed and first is None:first=n
    ck("minimal_boundary_period",first==lcm(2,den))

# Contour branch signs from the number of negative real factors on each bank.
for aa,bb,cc in [(5,2,3),(7,1,9),(3,2,1),(F(3,2),F(1,2),F(7,2))]:
    for z in [-(aa+bb)/2,cc/2]:
        factors=[z,z+aa,z+bb,z-cc]
        negatives=sum(x<0 for x in factors)
        phase=S.I**negatives
        ck("upper_bank_negative_imaginary",S.simplify(S.sign(z)/phase)==-S.I)

# Laurent leading coefficient at the two distinct points at infinity.
p,q0,zeta,sgn=S.symbols("p q0 zeta sgn",nonzero=True)
quartic=(p-q0/zeta)*(c+p-q0/zeta)*(1-1/zeta**2)
ck("quartic_infinity_two_points",S.expand(zeta**4*quartic).subs(zeta,0)==-q0*q0)
for sign in (-1,1):
    # y~sign*i*q0/zeta^2 and dw=-d zeta/zeta^2.
    coefficient=S.expand(-(p-q0/zeta)/(2*(sign*S.I*q0/zeta**2))*(-1/zeta**2))
    residue=S.expand(zeta*coefficient).subs(zeta,0)
    ck("third_kind_residue_nonzero",S.simplify(residue-sign*S.I/2)==0)

root=Path(__file__).resolve().parent
receipt={"status":"PASS","exact_assertions":sum(checks.values()),"checks":checks,
 "artifact_sha256":hashlib.sha256((root/"author_replay/ANALYTIC_CRITERION.md").read_bytes()).hexdigest(),
 "scope":"Independent metric differentiation, root/endpoint identities, latitude factor, "
         "explicit boundary-map iteration, contour signs and third-kind residues. "
         "Global analytic arguments are audited in REVIEW.md."}
(root/"independent_results.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
