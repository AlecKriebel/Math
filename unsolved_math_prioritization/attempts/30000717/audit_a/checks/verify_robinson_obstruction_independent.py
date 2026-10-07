#!/usr/bin/env python3
"""Exact independent arithmetic supporting a vanishing-line SOS obstruction.
No input, code, or computed output from the candidate verifier is imported.
The finite-polynomial contradiction itself is proved in the audit report.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp

x,y,z,t,a,b,c = sp.symbols('x y z t a b c')
vars_=(x,y,z)
R=sum(v**6 for v in vars_) - sum(u**4*v**2 for u in vars_ for v in vars_ if u!=v)+3*x*x*y*y*z*z
F=a**3+b**3+c**3-a*a*b-a*a*c-b*b*a-b*b*c-c*c*a-c*c*b+3*a*b*c
schur=(a-b)**2*(a+b-c)+c*(a-c)*(b-c)
assert sp.expand(F-schur)==0
assert sp.expand(R-F.subs({a:x*x,b:y*y,c:z*z}, simultaneous=True))==0
# Choose representatives in an independently specified, fixed order.
Z=[(1,s,u) for s in (-1,1) for u in (-1,1)]
Z += [(1,s,0) for s in (-1,1)]
Z += [(1,0,s) for s in (-1,1)]
Z += [(0,1,s) for s in (-1,1)]
assert len(Z)==10 and len(set(Z))==10
for i,p in enumerate(Z):
    for q in Z[i+1:]:
        assert sp.Matrix(p).cross(sp.Matrix(q)) != sp.zeros(3,1)
grad=[sp.diff(R,v) for v in vars_]
J=[sp.expand(vars_[j]*grad[i]-vars_[i]*grad[j]) for i in range(3) for j in range(i+1,3)]
K=[sp.expand(vars_[j]*grad[i]) for i in range(3) for j in range(3) if i!=j]
lines=[]
for p in Z:
    sub=dict(zip(vars_,[t*v for v in p]))
    r=sp.expand(R.subs(sub, simultaneous=True))
    g=[sp.expand(f.subs(sub, simultaneous=True)) for f in grad]
    js=[sp.expand(f.subs(sub, simultaneous=True)) for f in J]
    ks=[sp.expand(f.subs(sub, simultaneous=True)) for f in K]
    assert r==0 and g==[0]*3 and js==[0]*3 and ks==[0]*6
    lines.append({'point':p,'R_on_line':str(r),'gradient_on_line':list(map(str,g)), 'J_generators_on_line':list(map(str,js)), 'K_generators_on_line':list(map(str,ks))})
axis={x:t,y:0,z:0}
assert sp.expand(R.subs(axis, simultaneous=True))==t**6
assert [sp.expand(g.subs(axis, simultaneous=True)) for g in grad]==[6*t**5,0,0]
assert all(sp.expand(g.subs(axis, simultaneous=True))==0 for g in J+K)
# Rank checks in all four relevant homogeneous degrees avoid extrapolation.
ranks=[]
for d in range(4):
    exps=[(i,j,d-i-j) for i in range(d,-1,-1) for j in range(d-i,-1,-1)]
    mons=[x**i*y**j*z**k for i,j,k in exps]
    M=sp.Matrix([[m.subs(dict(zip(vars_,p)), simultaneous=True) for m in mons] for p in Z])
    assert M.rank()==len(mons)
    rec={'degree':d,'basis':list(map(str,mons)),'rank':M.rank(),'dimension':len(mons),'matrix':[[int(n) for n in row] for row in M.tolist()]}
    if d==3:
        rec['determinant']=int(M.det())
        assert abs(M.det())==128
    ranks.append(rec)
# Direct verification of the symbolic coefficient proof after the six pair lines.
A,B,C,D,E,Fc,G,H,I,L=sp.symbols('A B C D E F G H I L')
Q=A*x**3+B*y**3+C*z**3+D*x*x*y+E*x*x*z+Fc*x*y*y+G*y*y*z+H*x*z*z+I*y*z*z+L*x*y*z
reduced=sp.expand(Q.subs({Fc:-A,H:-A,D:-B,I:-B,E:-C,G:-C}))
for s,u in itertools.product((-1,1), repeat=2):
    assert sp.expand(reduced.subs({x:1,y:s,z:u})-(-A-B*s-C*u+L*s*u))==0
# Euler identity confirms this does not dispute the ordinary gradient-ideal theorem.
assert sp.expand(sum(v*g for v,g in zip(vars_,grad))-6*R)==0
payload={
 'verification':'PASS', 'arithmetic':'exact integer/rational SymPy arithmetic; no numerical tolerance',
 'sympy_version':sp.__version__, 'polynomial':str(R),
 'schur_ordered_identity':str(schur),
 'gradient':list(map(str,grad)), 'J_tangency_generators':list(map(str,J)),
 'K_all_off_diagonal_products':list(map(str,K)),
 'ten_zero_lines':lines, 'evaluation_checks':ranks,
 'axis':{'R':'t**6','gradient':['6*t**5','0','0'],'all_J_K_generators_zero':True},
 'euler_identity':'x*R_x+y*R_y+z*R_z=6*R',
 'checks_scope':'Supports exact-SOS obstruction for ordinary and real radicals of J and K. No epsilon-certificate conclusion.'
}
out=Path(__file__).resolve().parent.parent/'results'/'independent_exact_checks.json'
out.write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({'status':'PASS','result_path':str(out),'result_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'ranks':[(r['degree'],r['rank']) for r in ranks],'cubic_determinant':ranks[3]['determinant']},indent=2))
