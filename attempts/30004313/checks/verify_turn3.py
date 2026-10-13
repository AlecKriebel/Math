"""Exact controls for the fixed-column Rees-retraction classification."""
from itertools import product,permutations
from collections import Counter
import json
C=Counter();models=[]
def ck(q,k):assert q,k;C[k]+=1
def sides(r,a,b,c):
 u,v=r(a,b);w,z=r(v,c);x,y=r(u,w);L=(x,y,z)
 u,v=r(b,c);w,z=r(a,u);x,y=r(z,v);R=(w,x,y)
 return L,R

def run(G,gm,gi,P,fs,label):
 X=list(product(range(2),G,range(2)));ind={a:i for i,a in enumerate(X)};N=len(X);J=[i for i,a in enumerate(X) if a[2]==0]
 def mul(a,b):
  i,g,l=X[a];j,h,mu=X[b]
  return ind[i,gm(gm(g,P[2*l+j]),h),mu]
 def inv(a):
  i,g,l=X[a];p=gi(P[2*l+i]);return ind[i,gm(gm(p,gi(g)),p),l]
 stat=Counter()
 for f in fs(X,ind,J):
  ck(all(f[j]==j for j in J) and all(x in J for x in f),'actual_retraction_onto_column')
  ck(all(f[mul(a,f[b])]==mul(a,f[b]) for a,b in product(range(N),repeat=2)),'column_image_left_ideal_brace_condition')
  row_ok=all(X[f[a]][0]==X[a][0] for a in range(N))
  H={(i,g,l):gm(gi(X[f[ind[i,g,l]]][1]),g) for i,g,l in X}
  idem=all(H[i,H[i,g,l],l]==H[i,g,l] for i,g,l in X)
  criterion=row_ok and idem
  r=lambda a,b:(mul(a,f[b]),mul(inv(f[b]),b))
  valid=True;triple_count=0
  for a,b,c in product(range(N),repeat=3):
   L,R=sides(r,a,b,c);triple_count+=1
   i,g,la=X[a];j,h,mu=X[b];ll,z,nu=X[c]
   k,q,_=X[f[b]];m,t,_=X[f[c]];nn,u,_=X[f[ind[m,gm(gi(t),z),nu]]]
   predictedL=((i,gm(gm(gm(g,P[2*la+k]),h),gm(P[2*mu+m],t)),0),(k,0,0),(m,gm(gi(t),z),nu))
   predictedR=((i,gm(gm(gm(g,P[2*la+j]),h),gm(P[2*mu+m],t)),0),(j,u,0),(nn,gm(gi(u),gm(gi(t),z)),nu))
   ck(tuple(X[a] for a in L)==predictedL and tuple(X[a] for a in R)==predictedR,'all_three_symbolic_braid_coordinates')
   if L!=R:valid=False;break
  ck(valid==criterion,'full_retraction_YBE_iff_structural_criterion')
  hom=all(f[mul(a,b)]==mul(f[a],f[b]) for a,b in product(range(N),repeat=2))
  stat[f'YBE={valid},endomorphism={hom}']+=1
 models.append({'label':label,'distribution':dict(stat)})

def exhaustive(X,ind,J):
 outside=[i for i in range(len(X)) if i not in J]
 for values in product(J,repeat=len(outside)):
  f=list(range(len(X)))
  for a,b in zip(outside,values):f[a]=b
  yield f
for P in [(0,0,0,0),(0,0,0,1)]:run(range(2),lambda a,b:(a+b)%2,lambda a:a,P,exhaustive,'C2-'+str(P))
perms=list(permutations(range(3)));idx={p:i for i,p in enumerate(perms)}
gm=lambda a,b:idx[tuple(perms[a][perms[b][i]] for i in range(3))]
gi=lambda a:idx[tuple(perms[a].index(i) for i in range(3))]
def samples(X,ind,J):
 choices=[([0]*6,list(range(6))),([1]*6,[2]*6),([0,1,0,1,0,1],[0,0,2,0,2,0]),([1,0,2,3,4,5],[0]*6)]
 for h0,h1 in choices:
  f=[]
  for i,g,l in X:
   h=0 if l==0 else [h0,h1][i][g]
   f.append(ind[i,gm(g,gi(h)),0])
  yield f
run(range(6),gm,gi,(0,0,1,2),samples,'noncommutative-S3-nonfactorizing-P')
# Verify the one-row normalization for all 2x2 sandwich matrices over C2.
for P in product(range(2),repeat=4):
 for a,b in product(list(product(range(2),repeat=3)),repeat=2):
  i,g,l=a;j,h,mu=b;v=[P[0],P[1]]
  old=(i,(g+P[2*l+j]+h)%2,mu)
  N=lambda a:(a[0],(v[a[0]]+a[1])%2,a[2])
  aa,bb=N(a),N(b);new=(i,(aa[1]+P[2*l+j]+v[j]+bb[1])%2,mu)
  ck(N(old)==new,'arbitrary_sandwich_base_row_normalization')
# The broad endomorphic-retraction criterion, checked on all CR tables of
# orders at most3. The analytic proof is in TURN_3.md, not this finite loop.
for n in (1,2,3):
 X=range(n);triples=list(product(X,repeat=3));pairs=list(product(X,repeat=2))
 for tab in product(X,repeat=n*n):
  m=lambda a,b:tab[n*a+b]
  if not all(m(m(a,b),c)==m(a,m(b,c)) for a,b,c in triples):continue
  inv=[]
  for a in X:
   cand=[b for b in X if m(m(a,b),a)==a and m(m(b,a),b)==b and m(a,b)==m(b,a)]
   if len(cand)!=1:break
   inv.append(cand[0])
  if len(inv)!=n:continue
  for f in product(X,repeat=n):
   if not all(f[f[a]]==f[a] for a in X):continue
   if not all(f[m(a,b)]==m(f[a],f[b]) and f[m(a,f[b])]==m(a,f[b]) for a,b in pairs):continue
   J=set(f);zero=lambda a:m(a,inv[a]);crit=all(zero(m(a,b))==zero(m(zero(a),b)) for a,b in product(J,repeat=2))
   r=lambda a,b:(m(a,f[b]),m(inv[f[b]],b))
   good=all(L==R for L,R in (sides(r,a,b,c) for a,b,c in triples))
   ck(good==crit,'general_CR_endomorphic_retraction_criterion')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'models':models,'scope':'Finite exact controls for all-size structural proofs, not a full classification of generalized semi-braces.'},indent=2,sort_keys=True))
