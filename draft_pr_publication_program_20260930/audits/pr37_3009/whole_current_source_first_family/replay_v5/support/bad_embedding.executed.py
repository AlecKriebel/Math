#!/usr/bin/env python3
"""Exact algebraic controls; imported topological theorems are not tested by code."""
from pathlib import Path
import json
import sympy as s
checks={}
def check(name,value):
    assert bool(value),name
    checks[name]='PASS'
x1,x2,y1,y2=s.symbols('x1 x2 y1 y2',real=True)
x=s.Matrix([x1,x2]);y=s.Matrix([y1,y2])
def stereo(x):
    z=x.dot(x); return s.Matrix([3*x[0],2*x[1],z-1])/(1+z)
a=stereo(x);b=stereo(y)
check('stereographic_unit_sphere',s.factor(a.dot(a)-1)==0)
check('chordal_metric_identity',s.factor((a-b).dot(a-b)-4*(x-y).dot(x-y)/((1+x.dot(x))*(1+y.dot(y))))==0)
# Squared tail bound is monotone decreasing for R>D>0.
R,D=s.symbols('R D',positive=True)
bound2=4*D*D/((1+R*R)*(1+(R-D)**2))
expected=-bound2*(2*R/(1+R*R)+2*(R-D)/(1+(R-D)**2))
check('tail_bound_derivative',s.factor(s.diff(bound2,R)-expected)==0)
check('tail_bound_limit',s.limit(bound2,R,s.oo)==0)
# Exact finite instances, not evidence for the topological conclusion.
for d in [s.Rational(1,2),1,3]:
    prev=None
    for n in [2,4,8,16]:
        r=n*d; val=s.simplify(bound2.subs({R:r,D:d}))
        check(f'positive_tail_d{d}_n{n}',val>0)
        if prev is not None:check(f'decreasing_tail_d{d}_n{n}',val<prev)
        prev=val
check('two_fixed_point_regions_disjoint',7*D>3*D+3*D)
# Higher-dimensional sphere rotations can have infinitely many fixed points.
c=s.Rational(3,5);q=s.Rational(4,5)
M=s.Matrix([[c,-q,0,0],[q,c,0,0],[0,0,1,0],[0,0,0,1]])
check('sphere3_rotation_orthogonal',M.T*M==s.eye(4))
check('sphere3_rotation_positive_orientation',M.det()==1)
check('sphere3_fixed_plane',M*s.Matrix([0,0,x1,x2])==s.Matrix([0,0,x1,x2]))
check('sphere3_rotation_nonidentity',M!=s.eye(4))
# A planar irrational rotation illustrates why compact-open recurrence must
# not be confused with Euclidean uniform recurrence: any nonzero rotation
# displacement grows linearly with radius.
r,cost,sint=s.symbols('r cost sint',real=True)
z=s.Matrix([r,0]);Rot=s.Matrix([[cost,-sint],[sint,cost]])
check('rotation_displacement_polynomial',s.expand((Rot*z-z).dot(Rot*z-z)-r*r*((cost-1)**2+sint**2))==0)
out={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Stereographic and displacement algebra only. No computed certificate for Cartwright-Littlewood, Kolev-Peroueme, or higher-dimensional resolution.'}
Path(__file__).with_name('check_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
