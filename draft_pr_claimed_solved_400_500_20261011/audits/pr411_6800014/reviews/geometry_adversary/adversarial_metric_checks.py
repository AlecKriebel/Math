#!/usr/bin/env python3
"""Exact same-group witnesses and bounded metric falsification search.

This was added after independent reconstruction was sealed and author source
was read. It is not an all-metrics proof: see INDEPENDENT_RECONSTRUCTION.md.
"""
import json,random
import sympy as s
J=s.Matrix([[0,-1],[1,0]])
def inv(A):
 S=(A+A.T)/2; C=A*A.T-A.T*A
 T=s.trace(S*S);q=s.trace(C*C)
 return s.factor(q-8*T*T),s.factor(T*T/(T*T+q/4))
u,a=s.symbols('u a',positive=True)
D=s.Matrix([[0,u],[0,0]]);A=s.diag(J,D)
X=s.diag(a,-u*a);Z=J*X+X*D
T=s.eye(4);T[:2,2:]=Z
M=J.row_join(X).col_join(s.zeros(2).row_join(D))
assert (T*A*T.inv()-M).applyfunc(s.expand)==s.zeros(4)
# G_n=T^t T is positive definite and realizes M in the frame T^-1.
G=T.T*T
assert G.det()==1
P,F=inv(M)
assert s.factor(P-(2*(1-4*u*u)*a*a-4*u*u*a**4))==0
assert s.factor(P.subs(u,s.Rational(1,2)))==-a**4
assert s.factor(F.subs(u,s.Rational(1,2))-s.Rational(1,3)-16*a**4/(3*(59*a**4+30*a*a+3)))==0
# Independently validate the author-supplied nonglobal comparison.
B=s.Matrix([[0,-1,0,0],[1,0,0,0],[1,0,0,1],[0,-1,0,0]])
Tb=s.eye(4);Tb[2:,:2]=s.Matrix([[0,2],[1,0]])
Hs=s.diag(1,1,1/u,1)
assert Tb*Hs*A*(Tb*Hs).inv()==B
assert inv(B)[1]==s.Rational(9,17)
# All-metric samples include ideal mixing, e0 length, and complement shifts.
rng=random.Random(6800014)
counts={};negative=[]
for uv,eps in [(s.Rational(1,10),s.Rational(1,500)),(s.Rational(1,4),s.Rational(1,500)),(s.Rational(49,100),s.Rational(1,10000))]:
 A0=A.subs(u,uv);count=0
 for i in range(20):
  R=s.Matrix(4,4,[rng.randint(-3,3) for _ in range(16)])
  h=s.eye(4)+eps*R
  assert h.det()!=0
  scale=1+eps*rng.randint(-3,3)
  w=eps*s.Matrix([rng.randint(-3,3) for _ in range(4)])
  frame=s.zeros(5);frame[0,0]=scale;frame[1:,0]=scale*w;frame[1:,1:]=h
  Gram=frame.inv().T*frame.inv()
  assert Gram.det()>0 # SPD follows more strongly from Gram=L^-t L^-1.
  gram_bracket=scale*h.inv()*A0*h
  pv,fv=inv(gram_bracket)
  if pv<0:negative.append({'u':str(uv),'sample':i,'P':str(pv),'F':str(fv)})
  assert pv>=0 and fv<=s.Rational(1,3)
  count+=1
 counts[str(uv)]={'epsilon':str(eps),'exact_positive_metric_samples':count}
print(json.dumps({'boundary_conjugator':'T=[[I,JX+XD],[0,I]]; G_n=T^t T','boundary_P':str(s.factor(P)),'threshold_F_minus_one_third':str(s.factor(F.subs(u,s.Rational(1,2))-s.Rational(1,3))),'nonglobal_F':'9/17','bounded_falsification_search':counts,'negative_samples':negative,'search_limit':'60 rational samples; supports falsification attempts only; universal theorem is textual'},indent=2))
