#!/usr/bin/env python3
"""Exact diagnostics for hypotheses omitted in standalone exported statements.

These are not counterexamples to the correctly stated main-manuscript theorem.
"""
import itertools
import json
from pathlib import Path
import sympy as S

def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)

s=S.symbols('s')
u=S.Matrix([100,1,1])
v=S.Matrix([S.Rational(1,300),S.Rational(1,3),S.Rational(1,3)])
J=-S.eye(3)+u*v.T
D=S.Matrix([[S.Rational(4,3),S.Rational(-2,3),0],
            [S.Rational(-2,3),S.Rational(4,3),0],[0,0,1]])
minors={k:[(-1)**k*J.extract(I,I).det() for I in itertools.combinations(range(3),k)] for k in (1,2)}
require(J.det()==0,'singular J')
require(all(x>0 for x in minors[1]) and sum(minors[2])>0,'all stated J hypotheses')
require(all(x>0 for x in D.eigenvals()),'symmetric positive definite D')
p=S.Poly((s*D-J).det(),s)
require(p.nth(2)==-S.Rational(8801,450),'negative beta2')
require(S.expand(p.as_expr()-s*(600*s*s-8801*s-9451)/450)==0,'exact determinant')
missing_singularity=(s*S.eye(2)+S.eye(2)).det()
require(missing_singularity.subs(s,0)==1,'constant not zero without det J=0')
out={
 'status':'PASS',
 'scope':'Standalone theorem summary and proof skeleton omit assumptions stated correctly in the main manuscript.',
 'missing_diagonality':{
   'J':[[str(x) for x in row] for row in J.tolist()],
   'D':[[str(x) for x in row] for row in D.tolist()],
   'J_eigenvalues':{str(k):v for k,v in J.eigenvals().items()},
   'D_eigenvalues':{str(k):v for k,v in D.eigenvals().items()},
   'signed_minors':{str(k):list(map(str,vals)) for k,vals in minors.items()},
   'det_sD_minus_J':str(S.factor(p.as_expr())),
   'beta2':str(p.nth(2))},
 'missing_singularity':{'J':'-I_2','D':'I_2','det_sD_minus_J':str(missing_singularity),'constant_coefficient':'1'},
}
Path(__file__).with_name('standalone_hypothesis_counterexamples.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
