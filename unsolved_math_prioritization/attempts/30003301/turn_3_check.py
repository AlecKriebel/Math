"""Exact controls for the invariant-Heisenberg-quotient completion obstruction."""
import sympy as s
import json
from itertools import product
checks=0
O=s.Matrix([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]])
P=s.Matrix([[1,0,0,1],[0,1,1,0]])
def v(p,q):return s.Matrix([p,q,-q,-p])
def N(v):return -v*v.T*O
def zero(x):
 global checks
 if isinstance(x,s.MatrixBase):
  for z in x:assert s.expand(z)==0;checks+=1
 else:assert s.expand(x)==0;checks+=1
p,q,r,t=s.symbols('p q r t',real=True)
a=v(p,q);b=v(r,t)
zero(P*a);zero((a.T*O*b)[0]);zero(N(a)*N(b))
zero((s.eye(4)+N(a))*(s.eye(4)+N(b))-s.eye(4)-N(a)-N(b))
zero(s.trace(a*a.T)-2*(p*p+q*q))
for pp,qq in product(range(-5,6),repeat=2):
 a=v(pp,qq);zero(P*a);zero(N(a)*N(a))
 assert (N(a)==s.zeros(4))==((pp,qq)==(0,0));checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'kernel_basis':[[1,0,0,-1],[0,1,-1,0]],'symbolic_trace_gram':'2*(p^2+q^2)','limitations':'Symbolic linear-algebra controls for a restricted no-go result. The no-Torelli theorem is an external credited input; original relation lifting remains unresolved.'},indent=2))
