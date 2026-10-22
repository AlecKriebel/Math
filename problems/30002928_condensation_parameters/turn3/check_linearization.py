import sympy as S
from random import Random
import json
r=Random(30002928);n=0
def ck(x):
 global n;n+=1;assert x
alpha,a=S.symbols('alpha a');mp=alpha/(1-alpha)
ck(S.simplify(mp-a*(mp+1)-(alpha-a)/(1-alpha))==0)
ck(S.simplify((mp-a*(mp+1)).subs(a,alpha))==0)
# Exact finite Schur identities, not a replacement for the Fredholm argument.
cases=0
for d in range(1,6):
 for _ in range(40):
  L=S.Matrix([[r.randrange(-3,4) for j in range(d)] for i in range(d)])+7*S.eye(d)
  if not L.det():continue
  g=S.Matrix([r.randrange(-3,4) for i in range(d)]);c=S.Matrix([[r.randrange(-2,3) for i in range(d)]]);b=S.Rational(r.randrange(1,10),11)
  schur=b-(c*L.inv()*g)[0];M=L.row_join(g).col_join(c.row_join(S.Matrix([[b]])))
  ck(S.simplify(M.det()-L.det()*schur)==0)
  if schur:ck(M.det()!=0)
  cases+=1
for den in range(2,31):
 for num in range(1,den):
  aa=S.Rational(num,den)
  for k in [1,2,5,10]:
   partial=sum(aa**j for j in range(k));ck((1-aa)*partial==1-aa**k);ck(aa**k/(1-aa)>0)
print(json.dumps({'assertions':n,'finite_schur_cases':cases,'scope':'Symbolic linearization and finite algebra only; Banach inverse proven in TURN_3.md.'},indent=2))
