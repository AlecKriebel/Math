#!/usr/bin/env python3
"""Exact finite and symbolic diagnostics; not a numerical proof of local convergence."""
from fractions import Fraction as F
from itertools import combinations, product
from math import prod
from pathlib import Path
import hashlib,json
import sympy as sp

count=0;families={}
def ck(v,f):
 global count
 assert v,f
 count+=1;families[f]=families.get(f,0)+1

def dag(n):return [(i,j) for i in range(n) for j in range(i)]
def indeg(n,E):return [sum(m for (u,v),m in E.items() if v==x) for x in range(n)]
def degrees(n,E):return [sum(m*((u==x)+(v==x)) for (u,v),m in E.items()) for x in range(n)]
def discrepancy(A,B):return sum(abs(A.get(e,0)-B.get(e,0)) for e in A.keys()|B.keys())
def ball(n,E,o,r):
 V={o}
 for _ in range(r):
  W=set(V)
  for (u,v),m in E.items():
   if m and (u in V or v in V):W.update((u,v))
  V=W
 return frozenset(V),tuple(sorted((e,m) for e,m in E.items() if m and set(e)<=V))
def prune(n,E,K):
 ds=indeg(n,E); H={e:m for e,m in E.items() if ds[e[1]]<=K}
 ds=degrees(n,H); J={e:m for e,m in H.items() if ds[e[0]]<=K and ds[e[1]]<=K}
 return H,J

params=list(product([F(0),F(1,3),F(2,3),F(9,10)],[F(1,4),F(1)]))
# Exact conditional Bernoulli moments, exhaustively over small valid graph states.
for n in range(1,5):
 edges=dag(n)
 for bits in product((0,1),repeat=len(edges)):
  G={e:m for e,m in zip(edges,bits) if m};ds=indeg(n,G);T=sum(bits)
  for a,b in params:
   w=[a*d+b for d in ds];S=sum(w);Q=sum(x*x for x in w);ps=[x/n for x in w]
   ck(all(0<=p<=1 for p in ps),'source_probability_validity')
   mass=Et=Et2=Eq=El2=F(0)
   for row in product((0,1),repeat=n):
    p=prod((x if z else 1-x for x,z in zip(ps,row)),start=F(1));L=sum(row)
    mass+=p;Et+=p*(T+L);Et2+=p*(T+L)**2;El2+=p*L**2
    Eq+=p*(sum((x+a*z)**2 for x,z in zip(w,row))+b*b)
   ck(mass==1,'conditional_row_mass')
   ck(Et==T+S/n,'edge_mean_recurrence')
   ck(Et2==(T+S/n)**2+sum(p*(1-p) for p in ps),'edge_second_moment')
   ck(El2==(S/n)**2+sum(p*(1-p) for p in ps),'outdegree_second_moment')
   ck(Eq==(1+2*a/n)*Q+a*a*S/n+b*b,'squared_weight_recurrence')

# The normalization estimate uses the Poisson graph's own weight sum.
n=3;edges=dag(n)
for ab in product((0,1),repeat=len(edges)):
 A={e:m for e,m in zip(edges,ab) if m};da=indeg(n,A)
 for bb in product(range(3),repeat=len(edges)):
  B={e:m for e,m in zip(edges,bb) if m};db=indeg(n,B);D=discrepancy(A,B)
  for a,b in params:
   lam=b/(1-a);wa=[a*d+b for d in da];wb=[a*d+b for d in db];S=sum(wb)
   ck(sum(abs(x-y) for x,y in zip(da,db))<=D,'indegree_discrepancy')
   lhs=sum(abs(x/n-lam*y/S) for x,y in zip(wa,wb))
   ck(lhs<=a*D/n+abs(S/n-lam),'normalization_inequality')
   ck(S==a*sum(bb)+b*n,'affine_weight_sum')

# Sequential updating is a convex mixture with the frozen target law.
for ds in product(range(3),repeat=3):
 for a,b in params:
  w=[a*d+b for d in ds];S=sum(w)
  for j in range(4):
   for hist in product(range(j+1),repeat=3):
    if sum(hist)!=j:continue
    p=[x/S for x in w];q=[(x+a*h)/(S+a*j) for x,h in zip(w,hist)]
    tv=sum(abs(x-y) for x,y in zip(p,q))/2
    ck(sum(q)==1 and tv<=a*j/(S+a*j),'sequential_target_tv')
    ck(a*j/(S+a*j)<=a*j/(b*3),'sequential_denominator_bound')

# Column pruning and the exact induced-ball stability statement.
n=4;edges=dag(n)
for bits in product((0,1),repeat=len(edges)):
 A={e:m for e,m in zip(edges,bits) if m}
 for v in range(n):
  col=[e for e in edges if e[1]==v]
  for repl in product((0,1),repeat=len(col)):
   B={e:m for e,m in A.items() if e[1]!=v};B.update({e:m for e,m in zip(col,repl) if m})
   union={e:max(A.get(e,0),B.get(e,0)) for e in A.keys()|B.keys()}
   bad={x for e in A.keys()|B.keys() if A.get(e,0)!=B.get(e,0) for x in e}
   for r in range(3):
    for root in range(n):
     V,_=ball(n,union,root,r)
     if not V.intersection(bad):ck(ball(n,A,root,r)==ball(n,B,root,r),'induced_ball_stability')
   da=degrees(n,A);db=degrees(n,B);du=degrees(n,union)
   ck(sum(abs(x-y) for x,y in zip(da,db))<=2*discrepancy(A,B),'total_degree_discrepancy')
   ck(all(u<=2*x+abs(y-x) for u,x,y in zip(du,da,db)),'union_degree_bound')
   for K in (1,2,3):
    HA,JA=prune(n,A,K);HB,JB=prune(n,B,K)
    ck(discrepancy(HA,HB)<=2*K,'capped_column_resampling')
    ck(max(degrees(n,JA)+degrees(n,JB),default=0)<=K,'final_pruning_degree')
    ck(discrepancy(JA,JB)<=2*K+24*K*K,'pruning_bounded_difference')
    removed=discrepancy(A,JA);dg=degrees(n,A)
    ck(removed<=2*sum(x for x in dg if x>K),'pruning_tail_bound')

# Symbolic scalar, Gamma--Poisson and age-coordinate identities.
a,b,n,T,L,z,t,u,v,k=sp.symbols('a b n T L z t u v k',positive=True)
lam=b/(1-a)
ck(sp.simplify(a*lam+b-lam)==0,'matching_poisson_mean')
m=a*T/n+b
bound=(1+a/n)**2*T**2+(2*b*(1+a/n)+a/n)*T+b*b+b
ck(sp.expand((T+m)**2+m-bound)==0,'global_second_moment_algebra')
ck(sp.simplify((1+a/n)*n/(1-a)+1-(n+1)/(1-a))==0,'linear_recursion_comparison')
ck(sp.simplify(sp.diff(sp.exp(L*(z-1)),z,2).subs(z,1)-L**2)==0,'poisson_factorial_second_moment')
ck(sp.simplify(a*sp.exp(a*t)*(b/a+k)/sp.exp(a*t)-(a*k+b))==0,'gamma_posterior_birth_rate')
older=b*u**(a-1)*v**(-a)
antiderivative=b*u**(a-1)*v**(1-a)/(1-a)
ck(sp.simplify(sp.diff(antiderivative,v)-older)==0,'older_intensity_antiderivative')
ck(sp.simplify(antiderivative.subs(v,u)-lam)==0,'older_poisson_mass')
younger=a*L*u**(-a)*v**(a-1)
anti=L*u**(-a)*v**a
ck(sp.simplify(sp.diff(anti,v)-younger)==0,'younger_intensity_antiderivative')
ck(sp.simplify((anti.subs(v,1)-anti.subs(v,u))-L*(u**(-a)-1))==0,'younger_poisson_mass')
ck(sp.integrate(u**b,(u,0,1))==1/(b+1),'isolated_root_integral')
for aa,bb,uu in [(F(1,2),F(1,2),F(1,4)),(F(1,4),F(1,2),F(1,16)),(F(1,3),F(2,3),F(1,8))]:
 aa,bb,uu=map(sp.Rational,(aa,bb,uu))
 ck(sp.simplify((uu**(-aa))**(-bb/aa)-uu**bb)==0,'gamma_zero_younger_probability')

root=Path(__file__).resolve().parent
result={'problem_id':30005451,'artifact_sha256':hashlib.sha256((root/'CANDIDATE.md').read_bytes()).hexdigest(),
        'exact_assertions':count,'families':families,'status':'passed',
        'finite_checks_prove_local_convergence':False,'dependencies':['Python standard library','SymPy']}
(root/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
