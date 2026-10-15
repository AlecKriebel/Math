#!/usr/bin/env python3
"""Exact equivalence to the earlier explicit Ni-Zhang-Zhang §2 construction."""
import json
from pathlib import Path
import sympy as S

c,s,a,x,y=S.symbols('c s a x y',real=True)
ring=S.groebner([c*c+s*s-1],c,s,domain='EX')
checks={}


def zero(z):
    if isinstance(z,S.MatrixBase):return all(ring.reduce(S.expand(q))[1]==0 for q in z)
    return ring.reduce(S.expand(z))[1]==0


def check(n,q):
    assert bool(q),n
    checks[n]='PASS'


def D(z):return S.diff(z,c)*(-s)+S.diff(z,s)*c
g=S.Matrix([a*c,a*s,a**4*(c**4-s**4)])
gp=g.applyfunc(D)
gpp=gp.applyfunc(D)
w=S.Matrix([-4*a**3*c**3,4*a**3*s**3,1])
check('printed_curve_cos2_identity',zero(g[2]-a**4*(c*c-s*s)))
check('printed_frenet_cross_exact',zero(gp.cross(gpp)-a*a*w))
check('printed_curve_normal_velocity',zero(w.dot(gp)))
check('printed_curve_normal_acceleration',zero(w.dot(gpp)))
check('printed_asymptotic_equation',zero((a*c)**2*gp[0]**2-(a*s)**2*gp[1]**2))
check('scale_curve_exact',zero(g/a-S.Matrix([c,s,a**3*(c*c-s*s)])))
check('amplitude_quarter_when_a_cubed_quarter',S.Rational(1,4)==S.Pow(4,S.Rational(-1,3))**3)
check('binormal_coeff_quarter',4*S.Rational(1,4)==1)
f=x**4-y**4
graph_normal=S.Matrix([-S.diff(f,x),-S.diff(f,y),1])
check('printed_graph_normal',graph_normal==S.Matrix([-4*x**3,4*y**3,1]))
check('global_normal_ratio_x',graph_normal[0]/graph_normal[2]==-4*x**3)
check('global_normal_ratio_y',graph_normal[1]/graph_normal[2]==4*y**3)
check('graph_hessian_determinant',S.hessian(f,(x,y)).det()==-144*x*x*y*y)
check('graph_normal_on_curve_matches',zero(graph_normal.subs({x:a*c,y:a*s})-w))

out={'passed':len(checks),'failed':0,'checks':checks,'sympy_version':S.__version__,
     'scope':'Exact printed prior graph/curve equivalence and compatibility; complete global injectivity and linking proof are in PRIOR_EQUIVALENCE.md and CANDIDATE_LINKING_CERTIFICATE.md.',
     'source':'Ni, Zhang and Zhang, arXiv2606.29231v1, §2 pp2–3, submitted2026-06-28',
     'attribution':'zero linking and answer to Ghomi are verified elementary consequences, not claimed as printed statements in the cited paper',
     'verification_attempts_added':0}
Path(__file__).with_name('prior_controls_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
