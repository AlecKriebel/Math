#!/usr/bin/env python3
"""Exact identities, signed-permutation controls, and bounded family reductions. Requires SymPy."""
import sympy as S,json
from itertools import permutations,product
from collections import Counter
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
x,M,N,c,a=S.symbols('x M N c a');f=x**5+2*x+1
ck(S.resultant(f,M*x+N,x)==N**5+2*M**4*N-M**5,'norm_resultant')
disc=S.discriminant(f,x);ck(disc==11317 and not S.integer_nthroot(disc,2)[1],'quintic_discriminant_nonsquare')
q=x*x-8*x-7;r=x**3+8*x*x+3*x-5
ck(S.Poly(f-q*r,x,modulus=17).is_zero,'mod17_factorization')
ck(7 not in {i*i%17 for i in range(17)},'quadratic_mod17_irreducible')
for i in range(17):ck(r.subs(x,i)%17!=0,'cubic_mod17_no_root')
def cycles(p):
 seen=set();out=[]
 for v in range(len(p)):
  if v in seen:continue
  z=v;n=0
  while z not in seen:seen.add(z);n+=1;z=p[z]
  out.append(n)
 return sorted(out)
blocks=[p for p in permutations(range(5)) if cycles(p)==[5]];ten=0
for p in blocks:
 for signs in product(range(2),repeat=5):
  perm=tuple(2*p[i]+(j^signs[i]) for i in range(5) for j in range(2));yes=cycles(perm)==[10]
  ck(yes==(sum(signs)%2==1),'signed_5cycle_lifts');ten+=yes
# Every 5-cycle with every transposition generates S5 (finite control of the proof).
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
for p in blocks:
 for i in range(5):
  for j in range(i+1,5):
   t=list(range(5));t[i],t[j]=t[j],t[i];t=tuple(t);group={tuple(range(5))};todo=list(group)
   while todo:
    u=todo.pop()
    for gen in (p,t):
     v=comp(gen,u)
     if v not in group:group.add(v);todo.append(v)
   ck(len(group)==120,'5cycle_transposition_generates_S5')
P=a**4*x**10+5*c*a**3*x**8+10*c*c*a*a*x**6+10*c**3*a*x**4+(5*c**4+2)*x*x-1
H=f.subs(x,a*x*x+c)
ck(S.expand(H-a*P)==c**5+2*c+1+a,'generic_family_expansion')
ck(S.expand((N**5+2*M**4*N-M**5).subs({M:4*a,N:-4*a*c})+4**5*a**5*(c**5+2*c+1))==0,'generic_norm_formula')
samples=[]
for C0 in range(-3,4):
 A0=-(C0**5+2*C0+1);h=S.Poly(P.subs({a:A0,c:C0}),x)
 ck(h.content()==1 and h.degree()==10,'family_primitive_degree10')
 for p in S.primerange(2,32):
  hp=S.Poly(h,x,modulus=p)
  if A0%p:
   ck(hp.degree()==10 and not hp.is_irreducible,'sample_full_degree_reducible_modp');state='reducible degree ten'
  else:
   ck(hp.degree()<=2 and hp.nth(0)%p==p-1,'sample_badprime_degree_drop');state='degree drop'
  samples.append({'c':C0,'p':int(p),'case':state})
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'by_scope':dict(C),'arithmetic':'exact SymPy polynomial algebra and finite permutations','discriminant':int(disc),'five_cycles':len(blocks),'signed_lifts':len(blocks)*32,'ten_cycle_lifts':ten,'sample_reductions':len(samples),'samples':samples,'scope':'Finite controls support a proof using credited Dedekind/Chebotarev. No prime search bound or full degree-five superirreducibility solution is claimed.'},indent=2,sort_keys=True))
