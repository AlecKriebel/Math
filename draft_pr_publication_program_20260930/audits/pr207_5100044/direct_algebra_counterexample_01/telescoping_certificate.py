"""Exact independent certificate for a direct cyclic telescoping identity.
The certificate establishes the rational identities, not research novelty.
"""
import sympy as s
import json
from pathlib import Path
k,t,x,U,V,W=s.symbols('k t x U V W')
H=U*U-k*k*V*V*x
L=(1-k*k*t*x)*(U*U+k*k*V*(V+2*U)*x)
A=(1-t)/(U-V)**2
B=U*(U**3*t+U**2*V*k*k*t-2*U**2*V-2*U*V**2*k*k*t+U*V**2+V**3*k*k)/((U*U-k*k*V*V)*(U-V)**2)
D=k*k*V*(V*V-U*U*t)/((U*U-k*k*V*V)*(U-V))
checks={}
def record(name,e):
    res=s.factor(s.together(e))
    checks[name]={'residual':str(res),'passed':res==0}
record('generic_rational_decomposition',L-A*H*H-B*(1-k*k*x)*H-D*(1-k*k*x)*(U*U+(k*k*V*V-2*U*U)*x))
# Reciprocal dn addition: with y=sn(delta)^2, the common denominator factors.
y=s.symbols('y')
record('shifted_reciprocal_common_denominator',(1-k*k*x)*(1-k*k*y)-k**4*x*y*(1-x)*(1-y)-(1-k*k*x*y)*((1-k*k*y)-k*k*x*(1-y)))
# d(sn(u)cn(u))/du=dn(u)(1-2x), dx/du=2 sn(u)cn(u)dn(u).
# The derivative of sn(u)cn(u)/H has numerator shown below.
record('shifted_reciprocal_difference_derivative',(1-2*x)*H+2*k*k*V*V*x*(1-x)-(U*U+(k*k*V*V-2*U*U)*x))
h,cv,dv=s.symbols('h cv dv',nonzero=True)
Q=(V*V-U*U*t)/(4*h*cv*dv*(U*U-k*k*V*V)*(U-V))
sdelta=2*h*cv*dv/W; cdelta=V/W
record('derivative_coefficient_conversion',Q*2*k*k*sdelta*cdelta*W*W-D)
actual={U:1-2*k*k*t+k*k*t*t,V:1-2*t+k*k*t*t,W:1-k*k*t*t}
Lambda=U*(k**4*t**3+k**4*t*t-5*k*k*t+k*k+2)/(2*(1-k*k)**2*W**3)
record('cyclic_coefficient_closed_form',(A+B/(W*U)-Lambda).subs(actual))
record('N4_Vzero_A',A.subs(V,0)-(1-t)/U**2)
record('N4_Vzero_B',B.subs(V,0)-t)
record('N4_Vzero_D',D.subs(V,0))
# Q has no V denominator. Its finite V=0 value multiplies a zero shift difference.
record('N4_Vzero_Q',Q.subs(V,0)+t/(4*h*cv*dv*U))
result={'sympy_version':s.__version__,'all_passed':all(x['passed'] for x in checks.values()),'checks':checks,'coefficient_labels':{'A':str(A),'B':str(B),'D':str(D),'Q':str(Q),'Lambda':str(Lambda)},'scope':'Exact symbolic rational identities. Applying the cyclic-sum conclusion also uses the ordinary Jacobi addition/differentiation formulas and periodicity.'}
Path(__file__).with_name('telescoping_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['all_passed']
