"""Exact finite controls for Clifford rigidity and arbitrary-group obstructions."""
from itertools import product,permutations
from collections import Counter
import json
C=Counter();summary=[]
def ck(q,k):assert q,k;C[k]+=1
def braid(r,a,b,c):
 u,v=r(a,b);w,z=r(v,c);x,y=r(u,w);L=(x,y,z)
 u,v=r(b,c);w,z=r(a,u);x,y=r(z,v);R=(w,x,y)
 return L,R
def audit_clifford(X,m,inv,name):
 E=[a for a in X if m(a,a)==a];zero=lambda a:m(a,inv[a]);le=lambda a,b:m(a,b)==a
 for a,b in product(X,repeat=2):
  ck(inv[m(a,b)]==m(inv[b],inv[a]) and zero(m(a,b))==m(zero(a),zero(b)),'Clifford_inverse_and_idempotent_products')
 for mask in product((0,1),repeat=len(E)):
  F={e for e,take in zip(E,mask) if take}
  if not F or not all(d in F for e in F for d in E if le(d,e)):continue
  J=[a for a in X if zero(a) in F];outside=[a for a in X if a not in J]
  tau={};exists=True
  for e in E:
   cand=[d for d in F if le(d,e)]
   top=[d for d in cand if all(le(c,d) for c in cand)]
   if len(top)!=1:exists=False;break
   tau[e]=top[0]
  canonical={a:m(tau[zero(a)],a) for a in X} if exists else None
  dist=Counter()
  for vals in product(J,repeat=len(outside)):
   f={a:a for a in J};f.update(zip(outside,vals))
   ck(all(f[f[a]]==f[a] for a in X),'Clifford_actual_retraction')
   ck(all(f[m(a,f[b])]==m(a,f[b]) for a,b in product(X,repeat=2)),'Clifford_left_ideal_brace_condition')
   r=lambda a,b:(m(a,f[b]),m(inv[f[b]],b))
   h=lambda b:m(inv[f[b]],b)
   good=True
   for a,b,c in product(X,repeat=3):
    L,R=braid(r,a,b,c)
    predictedL=(m(m(m(a,zero(f[b])),b),f[c]),zero(m(h(b),f[c])),h(c))
    predictedR=(m(m(a,b),f[c]),m(zero(m(b,f[c])),h(c)),zero(h(c)))
    ck(L==predictedL and R==predictedR,'all_three_Clifford_braid_formulas')
    if L!=R:good=False;break
   hom=all(f[m(a,b)]==m(f[a],f[b]) for a,b in product(X,repeat=2))
   ck(good==hom,'Clifford_solution_iff_endomorphic_retraction')
   ck(good==(exists and f==canonical),'Clifford_unique_greatest_idempotent_restriction')
   dist['solutions' if good else 'failures']+=1
  summary.append({'model':name,'ideal_idempotents':str(sorted(F,key=str)),'greatest_restrictions_exist':exists,'distribution':dict(dist)})
for name,Y,meet in [('chain2',range(2),min),('chain3',range(3),min),('fork_no_top',range(3),lambda a,b:a if a==b else 0),('diamond',range(4),lambda a,b:a&b)]:
 X=list(product(Y,range(2)))
 m=lambda a,b:(meet(a[0],b[0]),(a[1]+b[1])%2)
 inv={a:a for a in X}
 audit_clifford(X,m,inv,name+'-C2')
# Noncommuting upper group and a non-injective connecting homomorphism.
perms=list(permutations(range(3)));idx={p:i for i,p in enumerate(perms)}
gm=lambda a,b:idx[tuple(perms[a][perms[b][i]] for i in range(3))]
gi=lambda a:idx[tuple(perms[a].index(i) for i in range(3))]
parity=lambda a:sum(perms[a][i]>perms[a][j] for i in range(3) for j in range(i+1,3))%2
X=[(0,g) for g in range(2)]+[(1,g) for g in range(6)]
def m(a,b):
 if a[0]==b[0]==1:return(1,gm(a[1],b[1]))
 return(0,((a[1] if a[0]==0 else parity(a[1]))+(b[1] if b[0]==0 else parity(b[1])))%2)
iv={a:(a[0],a[1] if a[0]==0 else gi(a[1])) for a in X}
audit_clifford(X,m,iv,'S3-to-C2-sign-connecting-map')
# Same rectangular-group multiplication, one genuinely two-argument addition
# failing and the coinciding-law addition succeeding, for arbitrary-group models.
groups=[('C1',range(1),lambda a,b:0,lambda a:0),('C2',range(2),lambda a,b:(a+b)%2,lambda a:a),('C3',range(3),lambda a,b:(a+b)%3,lambda a:(-a)%3),('S3',range(6),gm,gi)]
product_receipts=[]
for name,G,mm,ii in groups:
 X=list(product(range(4),G));cm=lambda a,b:2*(a//2)+b%2;ca=lambda a,b:2 if a and b else 0
 m=lambda a,b:(cm(a[0],b[0]),mm(a[1],b[1]))
 add=lambda a,b:(ca(a[0],b[0]),mm(a[1],b[1]))
 inv=lambda a:(a[0],ii(a[1]))
 r=lambda a,b:(m(a,add(inv(a),b)),m(inv(add(inv(a),b)),b))
 rgood=lambda a,b:(m(a,m(inv(a),b)),m(inv(m(inv(a),b)),b))
 for a,b,c in product(X,repeat=3):
  ck(add(add(a,b),c)==add(a,add(b,c)),'two_argument_product_addition_associative')
  ck(m(a,add(b,c))==add(m(a,b),m(a,add(inv(a),c))),'two_argument_product_brace_identity')
  L,R=braid(rgood,a,b,c)
  ck(L==R,'same_multiplication_coinciding_law_solution')
 L,R=braid(r,(0,0),(1,0),(1,0))
 ck(L==((0,0),(0,0),(3,0)) and R==((0,0),(0,0),(1,0)),'arbitrary_group_exact_braid_obstruction')
 product_receipts.append({'group':name,'order':len(X),'bad_addition_fails':True,'coinciding_addition_solves':True})
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'Clifford_retractions':summary,'two_argument_product_models':product_receipts,'scope':'Exact finite diagnostics for the written all-size Clifford rigidity and product obstruction theorems. The original arbitrary generalized-left-semi-brace classification remains unresolved.'},indent=2,sort_keys=True))
