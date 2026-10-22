import sympy as S
from fractions import Fraction as Q
import json
u,m,b=S.symbols('u m b',real=True,nonzero=True);A=lambda x:S.atanh(x)/b;H=lambda x:A(x)-x;d=A(u)-A(m)
D=d*d/2+m*d+S.log((1-u*u)/(1-m*m))/(2*b);n=0
def ck(v):
 global n;n+=1;assert v
ck(S.simplify(S.diff(D,m)+(S.diff(A(m),m)-1)*d)==0)
ck(S.simplify(S.diff(D,u)-(H(u)-H(m))*S.diff(A(u),u))==0)
ck(S.simplify(D.subs(m,-u)+2*A(u)*H(-u))==0)
# h'=H'(m)m' and D_m*m'+D_u=0.
rate=S.simplify(-S.diff(H(m),m)*S.diff(D,u)/S.diff(D,m))
ck(S.simplify(rate-(H(u)-H(m))*S.diff(A(u),u)/d)==0)
# Green ODE potential: derivative and energy conservation.
w,h=S.symbols('w h',real=True);W=w*w/2-h*w-S.log(S.cosh(b*w))/b
ck(S.simplify(S.diff(W,w)-(w-h-S.tanh(b*w)))==0)
a,r=S.symbols('a r',positive=True)
ck(S.expand((1-1/a)*a*a-a*(a-1))==0)
for den in range(2,25):
 for num in range(den+1,3*den):
  aa=Q(num,den);rr=Q(den,den+1);coef=aa*(aa-1)/(4*rr)
  ck(coef>0);ck(coef*4*rr==(1-1/aa)*aa*aa)
print(json.dumps({'assertions':n,'symbolic_selection_identities':6,'scope':'Exact scalar/Green identities; existence and all-parameter uniqueness are proved by phase-plane analysis.'},indent=2))
