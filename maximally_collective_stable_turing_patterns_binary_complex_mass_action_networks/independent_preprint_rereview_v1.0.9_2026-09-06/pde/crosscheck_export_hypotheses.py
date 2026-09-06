#!/usr/bin/env python3
"""Independently check the algebra referee's standalone-export witnesses."""
import itertools
import json
from pathlib import Path
import sympy as S


def check(truth, label):
    if not truth:
        raise RuntimeError(label)


s = S.symbols("s")
u = S.Matrix([100,1,1])
v = S.Matrix([S.Rational(1,300),S.Rational(1,3),S.Rational(1,3)])
J = -S.eye(3)+u*v.T
D = S.Matrix([[S.Rational(4,3),-S.Rational(2,3),0],
              [-S.Rational(2,3),S.Rational(4,3),0],[0,0,1]])
check(J.det()==0,"J nonsingular")
check(J.eigenvals()=={-1:2,0:1},"wrong homogeneous spectrum")
check(all(value>0 for value in D.eigenvals()),"D not SPD")
minors={}
for size in (1,2):
    values=[S.factor((-1)**size*J.extract(I,I).det())
            for I in itertools.combinations(range(3),size)]
    check(all(value>0 for value in values),"nonpositive signed minor")
    minors[str(size)]=[str(value) for value in values]
polynomial=S.factor((s*D-J).det())
check(S.expand(polynomial-s*(600*s*s-8801*s-9451)/450)==0,"wrong pencil witness")
check(S.Poly(polynomial,s).coeff_monomial(s*s)<0,"beta2 not negative")
J2=-S.eye(2)
det2=S.expand((s*S.eye(2)-J2).det())
check(det2==s*s+2*s+1,"wrong singularity witness")
Path(__file__).with_name("EXPORT_HYPOTHESIS_CROSSCHECK.json").write_text(json.dumps({
    "status":"PASS", "J":[[str(x) for x in row] for row in J.tolist()],
    "D":[[str(x) for x in row] for row in D.tolist()],
    "J_spectrum":{str(k):v for k,v in J.eigenvals().items()},
    "D_spectrum":{str(k):v for k,v in D.eigenvals().items()},
    "signed_principal_minors":minors,"det_sD_minus_J":str(polynomial),
    "omitted_singularity_example":{"J":"-I2","D":"I2","det_sD_minus_J":str(det2)}
},indent=2)+"\n")
print("EXPORT_HYPOTHESES_CROSSCHECK_PASS")
