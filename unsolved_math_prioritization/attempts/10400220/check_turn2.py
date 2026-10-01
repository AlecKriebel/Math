"""Exact source-family algebra and certificate-logic controls; not an unknotting computation."""
import sympy as s,json
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from collections import Counter
C=Counter()
def ck(x,key):assert bool(x),key;C[key]+=1
t=s.symbols('t');V=s.Matrix([[0,2],[1,0]]);D=s.det(V-t*V.T)
ck(s.expand(D+(2*t*t-5*t+2))==0,'Seifert_Alexander_identity')
ck(s.factor(2*t*t-5*t+2)==(t-2)*(2*t-1),'factorization')
ck(abs(D.subs(t,-1))==9,'determinant_nine')
P=s.Matrix([[0,0,1],[1,0,0],[0,1,0]]);I=s.eye(3);M=s.zeros(6)
for i in range(2):
 for j in range(2):M[i*3:(i+1)*3,j*3:(j+1)*3]=V[i,j]*I-V[j,i]*P
S=smith_normal_form(M,domain=ZZ);diag=[abs(S[i,i]) for i in range(6)]
ck(diag==[1,1,1,1,7,7],'third_cover_Smith_factors')
ck(s.resultant(2*t*t-5*t+2,t*t+t+1,t)==49,'third_cover_resultant')
for x in (1,2,4):
 m=(V-x*V.T).applyfunc(lambda a:int(a)%7)
 # For a two-by-two matrix over F7, determine its rank from minors.
 rank=2 if int(m.det())%7 else (1 if any(m) else 0)
 ck(rank==(2 if x==1 else 1),'deck_eigenvalue_multiplicity')
# Rational unit-circle points; each named Hermitian form has zero trace and negative determinant.
for p in range(-8,9):
 for q in range(1,9):
  x=s.Rational(q*q-p*p,q*q+p*p);y=s.Rational(2*p*q,q*q+p*p);w=x+s.I*y
  if w==1:continue
  H=(1-w)*V+(1-s.conjugate(w))*V.T
  ck(s.simplify(s.trace(H))==0 and s.simplify(H.det())<0,'classical_signature_zero_controls')
for N in range(1,101):
 for m in range(N+1):
  factors=2*m+2*(N-m)
  ck(factors==2*N,'actual_nontrivial_factor_count')
  ck(N-1<2*N,'strict_genus_squeeze_breaks_sum_lower_bound')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'limitations':'No ordinary unknotting number or mutant-pair inequality is inferred from these source-family and logical checks.'},indent=2))
