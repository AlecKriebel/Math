#!/usr/bin/env python3
"""Independent exact controls for the fixed-width averaging proof.
Requires SymPy; no candidate code is imported. Does not certify Reichel's theorem.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sympy as s
import json
checks=[]
def check(name,yes):
    assert bool(yes),name
    checks.append(name)
z,theta=s.symbols('z theta',real=True)
a,r,R,h=s.symbols('a r R h',positive=True)
p=s.Matrix([s.sqrt(1-z*z)*s.cos(theta),s.sqrt(1-z*z)*s.sin(theta),z])
cross=p.diff(theta).cross(p.diff(z))
check('longitude_height_area_element',s.simplify(cross.dot(cross)-1)==0)
check('orientation_integral',s.integrate(s.integrate(1,(theta,0,2*s.pi)),(z,-a/r,a/r))==4*s.pi*a/r)
check('sphere_strip_potential_factor',s.simplify((2*s.pi*R*h)/(h/2)-4*s.pi*R)==0)
x,y,w=s.symbols('x y w',real=True)
newton=1/s.sqrt(x*x+y*y+w*w)
check('Newton_kernel_harmonic_away_from_zero',s.simplify(sum(s.diff(newton,v,2) for v in (x,y,w)))==0)
t=s.symbols('t',real=True)
f=1+s.cos(2*s.pi*t/h)/2
check('periodic_density_integral',s.simplify(s.integrate(f,(t,x,x+h))-h)==0)
check('periodic_density_nonconstant',f.subs(t,0)==s.Rational(3,2) and f.subs(t,h/2)==s.Rational(1,2))
V=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
check('facet_norm_squared',all(sum(q*q for q in v)==3 for v in V))
check('facet_normals_sum_zero',all(sum(v[i] for v in V)==0 for i in range(3)))
for i,normal in enumerate(V):
    check(f'facet_equation_{i}',all(sum(a*b for a,b in zip(normal,v))==-1 for j,v in enumerate(V) if j!=i))
for u in product(range(-2,3),repeat=3):
    if not any(u):continue
    values=[sum(a*b for a,b in zip(u,v)) for v in V]
    width=max(values)-min(values)
    largest=sorted(map(abs,u),reverse=True)
    check('tetrahedron_width_'+str(u),width==2*(largest[0]+largest[1]))
    check('tetrahedron_lower_bound_'+str(u),width**2>=4*sum(q*q for q in u))
check('minimum_width_attained',max(v[0] for v in V)-min(v[0] for v in V)==2)
check('inradius_gap',F(3,2)<2 and F(3,2)**2>F(4,3))
# Exact entire admissible interval of the nested-sphere diagnostic.
lo,hi=F(-2),F(-1);small=F(1,2);fullwidth=F(3)
check('nested_all_lower_planes_below_inner',hi<=-small)
check('nested_all_upper_planes_above_inner',lo+fullwidth>=small)
check('nested_area_coefficient',2*2*fullwidth+4*small**2==13)
check('nested_diameter_condition',fullwidth<4)
result={'passed':len(checks),'failed':0,'checks':checks,'sympy_version':s.__version__,'full_target_solved':False,'scope':'Exact kernel, normalization, support-function, and negative-control checks; the analytic theorem and imported rigidity scope are reviewed in REVIEW.md.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS {len(checks)} independent exact controls')
