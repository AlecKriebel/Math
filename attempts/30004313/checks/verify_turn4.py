"""Exact controls for arbitrary image-column Rees retractions."""
from itertools import product,permutations
from collections import Counter
import json
C=Counter();models=[]
def ck(q,k):assert q,k;C[k]+=1
def sides(r,a,b,c):
 u,v=r(a,b);w,z=r(v,c);x,y=r(u,w);L=(x,y,z)
 u,v=r(b,c);w,z=r(a,u);x,y=r(z,v);R=(w,x,y)
 return L,R
def examine(G,gm,gi,P,fs,label):
 X=list(product(range(2),G,range(3)));ix={a:i for i,a in enumerate(X)};N=len(X);J=[a for a in range(N) if X[a][2] in (0,1)]
 def m(a,b):
  i,g,l=X[a];j,h,mu=X[b]
  return ix[i,gm(gm(g,P[2*l+j]),h),mu]
 def inv(a):
  i,g,l=X[a];q=gi(P[2*l+i]);return ix[i,gm(gm(q,gi(g)),q),l]
 z=lambda a:m(a,inv(a))
 hist=Counter()
 for f in fs(X,ix,J):
  ck(all(f[j]==j for j in J) and all(a in J for a in f),'multi_column_actual_retraction')
  hf=lambda b:m(inv(f[b]),b)
  row=all(X[f[b]][0]==X[b][0] for b in range(N))
  residual=all(f[hf(b)]==z(f[b]) for b in range(N))
  r=lambda a,b:(m(a,f[b]),hf(b))
  good=True
  for a,b,c in product(range(N),repeat=3):
   L,R=sides(r,a,b,c)
   if row:
    expectedL=(m(m(a,b),f[c]),z(m(b,f[c])),hf(c))
    expectedR=(m(m(a,b),f[c]),m(z(m(b,f[c])),f[hf(c)]),hf(hf(c)))
    ck(L==expectedL and R==expectedR,'reduced_all_three_braid_outputs')
   if L!=R:good=False;break
  ck(good==(row and residual),'exact_row_residual_YBE_criterion')
  if row:
   H={(i,g,l):X[hf(ix[i,g,l])][1] for i,g,l in X}
   K={(i,g,l):X[f[ix[i,g,l]]][2] for i,g,l in X}
   idem=all(H[i,H[i,g,l],l]==H[i,g,l] for i,g,l in X)
   labels=all(K[i,H[i,g,l],l]==K[i,g,l] for i,g,l in X)
   ck(residual==(idem and labels),'residual_equivalent_idempotence_and_labels')
   for i,g,l in X:
    delta=K[i,g,l];q=gm(gm(g,gi(H[i,g,l])),gi(P[2*delta+i]))
    ck(f[ix[i,g,l]]==ix[i,q,delta],'parameter_recovery_in_original_sandwich_coordinates')
  hist[f'YBE={good},row={row},residual={residual}']+=1
 models.append({'label':label,'distribution':dict(hist)})
def all_c2(X,ix,J):
 outside=[a for a in range(len(X)) if a not in J]
 for vals in product(J,repeat=len(outside)):
  f=list(range(len(X)))
  for a,b in zip(outside,vals):f[a]=b
  yield f
examine(range(2),lambda a,b:(a+b)%2,lambda a:a,(0,1,1,0,0,0),all_c2,'C2-all4096-retractions-to-two-columns')
Pms=list(permutations(range(3)));idx={p:i for i,p in enumerate(Pms)}
gm=lambda a,b:idx[tuple(Pms[a][Pms[b][i]] for i in range(3))]
gi=lambda a:idx[tuple(Pms[a].index(i) for i in range(3))]
P=(1,2,3,4,5,1)
def samples(X,ix,J):
 # H and K on the outside column; columns0/1 are fixed by f.
 cases=[([0]*6,[1]*6,[0]*6,[1]*6),
        (list(range(6)),list(range(6)),[0,1,0,1,0,1],[1,0,1,0,1,0]),
        ([0,1,0,1,0,1],[0,0,2,0,2,0],[0,1,0,1,0,1],[1,1,0,1,0,1]),
        ([0]*6,[0]*6,[0,1,0,0,0,0],[1]*6)]
 for h0,h1,k0,k1 in cases:
  f=list(range(len(X)))
  for i,g,l in X:
   if l!=2:continue
   h=[h0,h1][i][g];k=[k0,k1][i][g]
   q=gm(gm(g,gi(h)),gi(P[2*k+i]))
   f[ix[i,g,l]]=ix[i,q,k]
  yield f
examine(range(6),gm,gi,P,samples,'S3-noncommuting-sandwich-and-coupled-labels')
# The explicit one-row label obstruction from TURN_4 section4.
X=list(product(range(2),range(3)))
mul=lambda a,b:((a[0]+b[0])%2,b[1])
f=lambda a:a if a[1] in (0,1) else (a[0],a[0])
inv=lambda a:a
r=lambda a,b:(mul(a,f(b)),mul(inv(f(b)),b))
for a,b,c in product(X,repeat=3):
 ck(f(mul(a,f(c)))==mul(a,f(c)),'label_counterexample_brace_identity')
b=(1,2);hb=mul(inv(f(b)),b)
ck(f(hb)==(0,0) and mul(f(b),inv(f(b)))==(0,1),'exact_column_label_obstruction')
fails=[(a,b,c,L,R) for a,b,c in product(X,repeat=3) for L,R in [sides(r,a,b,c)] if L!=R]
ck(bool(fails),'label_counterexample_actual_braid_failure')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'models':models,'label_failure':fails[0],'scope':'Finite diagnostics for the all-size classification of retracted additions over presented Rees semigroups; arbitrary additions and general completely regular coupling remain outside the theorem.'},indent=2,sort_keys=True))
