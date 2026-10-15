"""Exact algebra checks for the priority routine-specialization bridge.
No PDE constants or numerical evolution are assumed certified by this script.
"""
import json, sys, sympy as s
h, x, A, d, t, eps = s.symbols("h x A d t eps", positive=True)
pi=s.pi
checks=[]
def check(name, condition):
    condition=bool(condition)
    checks.append({"name":name,"passed":condition})
    if not condition: raise AssertionError(name)
z=2*h*s.sin(pi*h)/pi**2
loss=2*h**2-2*h*s.sin(pi*h)/pi
r2=2*h**3
check("linear endpoint by centered sine integral",s.simplify(h*s.integrate(s.cos(pi*t),(t,-h,h))/pi-z)==0)
check("linear terminal velocity cancellation",s.simplify(h*s.integrate(-s.sin(pi*t),(t,-h,h)))==0)
check("pulse first-order loss",s.simplify(h*s.integrate(1-s.cos(pi*t),(t,-h,h))-loss)==0)
check("loss leading order",s.limit(loss/h**4,h,0)==pi**2/3)
check("terminal square leading order",s.limit(z**2/(2*h**4),h,0)==2/pi**2)
check("pure linear gap ratio tends zero",s.limit((loss+z**2/2)/r2,h,0)==0)
ndc=loss/r2+z**2/(2*r2)
check("NDC exact expression",s.simplify(ndc-(1/h-s.sin(pi*h)/(pi*h**2)+s.sin(pi*h)**2/(pi**4*h)))==0)
check("NDC leading order",s.simplify(s.limit(ndc/h,h,0)-(pi**2/6+1/pi**2))==0)
check("Hessian degenerates on normalized pulses",s.limit(z**2/r2,h,0)==0)
b=A/pi+d*A**2
scalar=A-pi*b+b*b/2
check("local projection algebra",s.expand(scalar-(A*A/(2*pi*pi)-pi*d*A*A+d*A**3/pi+d*d*A**4/2))==0)
check("quadratic threshold level-set asymptotic",s.limit((2/pi)*s.acos(1-eps)/s.sqrt(eps),eps,0)==2*s.sqrt(2)/pi)
# The independently checked Dunn reproduction has nonzero critical directions.
u=3*eps
diff=s.integrate(2*(1-2*x)*u-u*u,(x,s.Rational(1,2)-eps,s.Rational(1,2)))
check("Dunn reproduced pulse improvement",s.expand(diff+3*eps**3)==0)
# CT2012's elementary positive-Hessian/nonminimum example:
v=2*t
value=s.integrate(t*v*v-v**3,(t,0,h))
check("CT2012 positive Hessian example failure",s.expand(value+h**4)==0)
print(json.dumps({"python":sys.version,"sympy":s.__version__,"assertions":len(checks),"passed":all(q["passed"] for q in checks),"checks":checks},indent=2))
