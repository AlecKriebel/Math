"""Independent algebra checks for the continuous-family proof.

Requires SymPy. Polynomial remainders use the two exact defining equations,
not numerical substitutions or the submitted verifier.
"""
from pathlib import Path
import json
import sympy as s

A,B,c,d,delta=s.symbols("A B c d delta", real=True)
U=A*d*d+B*c*c
unit=c*c+d*d-1
delta_eq=delta*delta-A*A*d*d-B*B*c*c
basis=s.groebner([delta_eq,unit],delta,c,d,A,B,order="lex")
checks=[]

def zero_mod_constraints(label, expression):
    remainder=s.expand(basis.reduce(s.expand(expression))[1])
    if remainder != 0: raise ValueError(label+": "+str(remainder))
    checks.append({"identity":label,"remainder":str(remainder)})

zero_mod_constraints("support-square of PQ equals line-level square",
    A*(delta*d-B*c)**2+B*(delta*c+A*d)**2-(A+B)*U**2)
zero_mod_constraints("Delta squared plus AB equals (A+B)U",
    delta**2+A*B-(A+B)*U)
zero_mod_constraints("new squared normalization equals (AB/Delta)^2",
    A*A*(B*c)**2+B*B*(-A*d)**2-A*A*B*B)

# Derive the confocal tangency / normal-projection identity independently.
x,y,vx,vy,lam,a,b=s.symbols("x y vx vy lam a b", real=True)
tangent=(x*vy-y*vx)**2-(a*a-lam)*vy*vy-(b*b-lam)*vx*vx
normal=a*a*b*b*(x*vx/(a*a)+y*vy/(b*b))**2-lam
sum_expr=s.expand(tangent+normal)
expected=(x*x/(a*a)+y*y/(b*b)-1)*(b*b*vx*vx+a*a*vy*vy)+lam*(vx*vx+vy*vy-1)
if s.simplify(sum_expr-expected) != 0:
    raise ValueError("tangency / normal identity is wrong")
checks.append({"identity":"tangency plus normal-square equals ellipse/velocity constraints",
               "remainder":"0"})

# General area and angle values, including strictness as a squared eccentricity.
S=A+B
kd=2*A*B/S**2
kr=S**2/(8*A*B)
gap=s.factor(kr-kd)
expected_gap=(A-B)**2*(A*A+6*A*B+B*B)/(8*A*B*S**2)
if s.simplify(gap-expected_gap) != 0: raise ValueError("general gap factorization")
checks.append({"identity":"general k107 gap factorization",
               "exact_factor":str(gap),"remainder":"0"})
if s.simplify(kd*kr-s.Rational(1,4)) != 0: raise ValueError("product relation")
checks.append({"identity":"representative k107 product equals 1/4","remainder":"0"})

output={"status":"PASS_POLYNOMIAL_IDENTITIES","sympy_version":s.__version__,
        "variable_convention":"A=a^2, B=b^2, delta=Delta>0; c^2+d^2=1",
        "constraints":[str(delta_eq),str(unit)],"checks":checks,
        "analytic_obligations":"Positive square-root branches, convexity, physical direction signs, strict contact interiors, and family membership are proved in INDEPENDENT_REPORT.md."}
Path(__file__).with_name("POLYNOMIAL_IDENTITIES.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps({"status":output["status"],"checks":len(checks),"gap":str(gap)}))
