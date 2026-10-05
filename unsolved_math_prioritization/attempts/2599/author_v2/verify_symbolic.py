#!/usr/bin/env python3
"""Optional SymPy check of the algebraic identities printed in PROOFS.md."""
import sympy as s
import json,pathlib
k,b,d,c,e=s.symbols('k b d c e',positive=True)
a1=k-b-1;a2=k-c-d;a3=k-e
L=s.Matrix([[0,k,0,0],[1,a1,b,0],[0,c,a2,d],[0,0,e,a3]])
L2=(L*L-a1*L-k*s.eye(4))/c;L3=((L-a2*s.eye(4))*L2-b*L)/e
assert s.factor((L3**2)[1,0]-(L3**2)[2,0]+d*(d+e-k-1)/c)==0
assert s.factor(((L2**2)[1,0]-(L2**2)[3,0]).subs(d,k+1-e)+(b*(c+1)-c*e)/c)==0
c,a,t=s.symbols('c a t',positive=True);k=t*(c+1)+a
P=s.Matrix([[1,k,t*k,k*(a+1)/(c+1)],[1,a+t,-t,-a-1],[1,-1,-t,t],[1,-c-1,a+c+1,-a-1]])
v=s.factor(sum(P[0,j] for j in range(4)));Q=(v*P.inv()).applyfunc(s.factor)
assert s.factor(v-(k+1)*(k+c+1)/(c+1))==0
D=(c+1)*(t*t-a-1)-a*(a+1)
den=(c+1)*(a+t+1)**2*(a+c+t+1)**2
formulas={(1,2):c*t*(k+1)*(k+c+1)*(2*a+c*t+c+2*t+2)/den,
(1,3):c*(k+1)*(k+c+1)*D/den,
(2,1):a*(a+1)*(k+1)*(k+c+1)/((c+1)*(a+t+1)**2),
(2,3):a*(a+1)*(k+1)*(k+c+1)/((c+1)*(a+t+1)**2),
(3,1):t*(t-1)*(k+1)*(k+c+1)/((c+1)*(a+c+t+1)**2),
(3,2):t*(t-1)*(k+1)*(k+c+1)/((c+1)*(a+c+t+1)**2)}
for (i,h),expected in formulas.items():assert s.factor(sum(Q[l,i]**2*P[h,l]for l in range(4))/v-expected)==0
p333=s.factor(sum(P[l,3]**2*Q[3,l]for l in range(4))/v)
assert s.factor(p333-(a*(a+1)/(c+1)+t-a-1))==0
# The spectral matrix obeys every distance-polynomial recurrence.
x=s.symbols('x');p2=(x*x-(a+t-1)*x-k)/c;p3=((x-(t-1)*(c+1))*p2-t*c*x)/(t*(c+1))
for j,theta in enumerate([k,a+t,-1,-c-1]):
 assert s.factor(P[j,2]-p2.subs(x,theta))==0
 assert s.factor(P[j,3]-p3.subs(x,theta))==0
 assert s.factor((theta-a)*P[j,3]-(a+1)*P[j,2])==0
out={'two_fusion_identities':True,'six_Krein_factorizations':True,'order_formula':True,'distance_recurrences':True,'distance_three_lambda':True,'dependency':'sympy '+s.__version__}
pathlib.Path(__file__).with_name('SYMBOLIC_CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
