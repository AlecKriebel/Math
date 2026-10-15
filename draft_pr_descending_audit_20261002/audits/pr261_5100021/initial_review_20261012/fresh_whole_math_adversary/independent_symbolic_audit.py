"""Polynomial and local-series audit, independent of submitted checker."""
from pathlib import Path
import sys, json
sys.path.insert(0,str(Path(__file__).parent/'dependencies'))
import sympy as z
k,s,S,c,d,C,D,t = z.symbols('k s S c d C D t')
relations={C:1-S*S,D:1-k*k*S*S,d:1-k*k*s*s,t:1-k*k,c:1-s*s}
def canonical(expr):
    # Relations are monic triangular quadratic extensions. Reduction in the
    # displayed order is exact polynomial remainder, with k,s,S free.
    p=z.expand(z.fraction(z.cancel(expr))[0])
    for v,r in relations.items():
        p=z.rem(p,v*v-r,v)
    return z.factor(p)

L=1-k*k*s*s*S*S
H=1-2*k*k*s*s+k*k*s**4
R=z.Matrix((-(H*S+k*(c*c-d*d*S*S))/(c*c*L), C*(2*t*t-H*(1+k*S))/(t*c*c*L)))
end=[]
for e in [-1,1]:
    end.append(z.Matrix((-d*(S*c*d+e*s*C*D)/(c*L),t*(C*c-e*S*s*D*d)/(c*L))))
checks={}
for j,P in enumerate(end):
    checks['antipedal_line_'+str(j)]=canonical((P-z.Matrix((k,0))).dot(R-P))==0
normal_det=z.det(z.Matrix.hstack(end[0]-z.Matrix((k,0)),end[1]-z.Matrix((k,0))))
checks['focal_normal_determinant']=canonical(normal_det-2*t*s*d*D*(1+k*S)/(c*L))==0
n=z.Matrix((-S,C/t))
q=z.Matrix((k,0))+(1-n.dot(z.Matrix((k,0))))*n/n.dot(n)
for j,v in enumerate(((k-S)/(1-k*S),t*C/(1-k*S))):
    checks['pedal_projection_'+str(j)]=canonical(q[j]-v)==0
checks['pedal_unit_circle']=canonical(((k-S)/(1-k*S))**2+(t*C/(1-k*S))**2-1)==0
assert all(checks.values())

u=z.symbols('u')
cn=1-u*u/2+(1+4*k*k)*u**4/24
dn=1-k*k*u*u/2+k*k*(4+k*k)*u**4/24
Sn=dn/(k*cn)
Cn=-z.I*t/(k*cn)
qx=(k-Sn)/(1-k*Sn)
qy=t*Cn/(1-k*Sn)
leadx=z.simplify(z.limit(u*u*qx,u,0))
leady=z.simplify(z.limit(u*u*qy,u,0).subs(t*t,1-k*k))
assert leadx==2/k and leady==2*z.I/k

print(json.dumps({'status':'PASS','exact_line_and_projection_checks':checks,'quarter_shift_pedal_double_pole_leading_vector':[str(leadx),str(leady)],'local_evenness':'Both coordinates at K+iKprime+u are even functions of u by quarter-shift formulas.','pole_cancellation':'The incident neighbor difference is odd and holomorphic, so multiplying the even order-two singular vertex gives at most order one.','limitations':'No finite symbolic arithmetic enumeration is used to assert all-period trace cancellation; that is established by the independent analytic derivation.'},indent=2))
