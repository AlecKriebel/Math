#!/usr/bin/env python3
"""Exact odd-degree norm/CRT descent and formal local curve controls. Requires SymPy."""
from math import isqrt
from itertools import product
from collections import Counter
import sympy as S,json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
def vp(n,p):
 if n==0:return 10**9
 n=abs(n);v=0
 while n%p==0:n//=p;v+=1
 return v
def descent(M,N,Z,d):
 mod=abs(M)
 if mod==1:return 0
 residues=[]
 for pp,mm in S.factorint(mod).items():
  p=int(pp);m=int(mm);q=p**m;n=vp(N,p)
  if n>=m:r=0;C['descent_zero_residue_branch']+=1
  else:
   ck(n%2==0,'odd_degree_forces_even_valuation')
   N0=N//p**n;Z0=Z//p**(d*n//2);q0=p**(m-n)
   ck(Z%p**(d*n//2)==0 and vp(Z,p)==d*n//2,'norm_square_valuation')
   y=(Z0*pow(pow(N0,(d-1)//2,q0),-1,q0))%q0;r=(p**(n//2)*y)%q
   ck((r*r-N)%q==0,'norm_constructed_local_square')
   C['descent_unit_branch_p2' if p==2 else 'descent_unit_branch_odd_p']+=1
  residues.append((r,q))
 R=0
 for r,q in residues:
  Q=mod//q;R=(R+r*Q*pow(Q,-1,q))%mod
 ck((R*R-N)%mod==0,'CRT_global_square_residue')
 return R
# Any monic odd homogeneous polynomial qualifies; no irreducibility assumption in the lemma.
polys=[(3,[0,1,-1]),(3,[1,-2,3]),(5,[0,0,0,2,-1]),(5,[1,-2,3,0,2]),(7,[0,0,0,0,0,2,-1])]
cases=0;norms=0
for d,cs in polys:
 for M,N in product(range(-40,41),repeat=2):
  if not M:continue
  norms+=1;F=N**d+sum(c*M**j*N**(d-j) for j,c in enumerate(cs,1))
  if F<=0 or isqrt(F)**2!=F:continue
  r=descent(M,N,isqrt(F),d);ck((r*r-N)%abs(M)==0,'bounded_norm_square_congruence');cases+=1
# Actual cubic root-field squares, including noncoprime M,N and negative M.
x=S.symbols('x');constructed=0
for p,q,s in product(range(-3,4),range(-3,4),range(-3,4)):
 if (p-s*s)%2:continue
 f=x**3+p*x+q
 if not S.Poly(f,x).is_irreducible:continue
 t=(p-s*s)//2;beta=x*x+s*x+t
 M=-s**3-s*p-q;N=t*t-2*s*q
 if not M:continue
 ck(S.rem(beta*beta-(M*x+N),f,x)==0,'actual_cubic_linear_square')
 Z=abs(int(S.resultant(f,beta,x)));ck(Z*Z==int(S.resultant(f,M*x+N,x)),'actual_cubic_norm_square')
 r=descent(M,N,Z,3);g=M*x*x+2*r*x+(r*r-N)//M
 ck((r*r-N)%M==0 and S.Poly(g,x).degree()==2,'integer_counter_substitution')
 ck(not S.Poly(f.subs(x,g),x).is_irreducible,'constructed_composition_reducible');constructed+=1
# A degree-five actual-square scope control distinct from Du's candidate.
f5=x**5-2*x**3+x-1;beta=x**3-x
ck(S.rem(beta*beta-x,f5,x)==0,'degree_five_known_linear_square')
ck(S.expand(f5.subs(x,x*x)-(x**5-x-1)*(x**5-x+1))==0,'degree_five_composition_factorization')
ck(6%4 not in {r*r%4 for r in range(4)} and 6**2-2*4**2==4,'even_degree_limitation')
# Formal square-root series to order eight in the Du quotient algebra.
u=S.symbols('u');f=x**5+2*x+1;z=S.rem(sum(S.binomial(S.Rational(1,2),n)*u**n*x**n for n in range(9)),f,x).expand()
a=[z.coeff(x,i) for i in range(5)]
r=S.rem(z*z-(1+u*x),f,x).expand()
for i in range(5):ck(all(S.expand(r.coeff(x,i)).coeff(u,j)==0 for j in range(9)),'formal_square_identity_through_order8')
leading=[S.Integer(1),S.Rational(1,2)*u,-u*u/8,u**3/16,-5*u**4/128]
for i in range(5):
 ck(S.expand(a[i]-leading[i]).as_poly(u).degree()<0 if a[i]==leading[i] else all(S.expand(a[i]-leading[i]).coeff(u,j)==0 for j in range(5)),'formal_leading_terms')
D=S.expand(a[2]*a[4]-a[3]**2)
ck(all(D.coeff(u,j)==0 for j in range(6)) and D.coeff(u,6)==S.Rational(1,1024),'local_curve_denominator_leading_term')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'by_scope':dict(C),'arithmetic':'exact integer valuations, modular inverses, CRT and SymPy rational algebra','bounded_homogeneous_norms_examined':norms,'bounded_nonzero_square_norms':cases,'actual_cubic_counterexample_constructions':constructed,'formal_coefficients':[str(t) for t in a],'scope':'The odd-degree descent and all-completions curve points are proved in the text. These controls neither determine the residual curve rational points nor solve the source existence question.'},indent=2,sort_keys=True))
