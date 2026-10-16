#!/usr/bin/python3
import pathlib,json,sympy as s
x,y,p,q,r=s.symbols('x y p q r',real=True)
z=x+s.I*y;w=p+s.I*q
def norm(v):return s.expand(v*s.conjugate(v))
checks={}
def ck(n,v):
    assert bool(v),n
    checks[n]='PASS'
ck('pseudohyperbolic_distance_defect',s.expand(norm(1-s.conjugate(w)*z)-norm(z-w)-(1-norm(z))*(1-norm(w)))==0)
ck('curvature_minus_four_radial_distance',s.diff(s.atanh(r),r)==1/(1-r*r))
v=s.symbols('v',positive=True)
ck('sinh_arsinh_radius_identity',s.simplify(s.sinh(s.asinh(v))-v)==0)
out={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Algebraic hyperbolic-distance identities; written path-crossing estimate is universal and is not a finite-sample inference.'}
pathlib.Path(__file__).with_name('distance_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
