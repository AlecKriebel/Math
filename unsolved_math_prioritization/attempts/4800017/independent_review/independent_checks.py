#!/usr/bin/env python3
"""Independent exact convention controls; not a proof of the published theorem."""
from fractions import Fraction as F
from itertools import permutations, product
from math import lcm
from pathlib import Path
import hashlib,json
counts={}
def ck(v,k):
 assert v,k
 counts[k]=counts.get(k,0)+1

def compose(a,b):return tuple(a[b[x]] for x in range(len(a)))
def power(a,k):
 if k<0:
  a=tuple(a.index(x) for x in range(len(a)));k=-k
 out=tuple(range(len(a)))
 for _ in range(k):out=compose(a,out)
 return out

def order(a):
 n=1;b=a
 while b!=tuple(range(len(a))):b=compose(a,b);n+=1
 return n

def rank(rows):
 a=[[F(x) for x in r] for r in rows];k=0
 for j in range(len(a[0])):
  p=next((i for i in range(k,len(a)) if a[i][j]),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k];c=a[k][j];a[k]=[x/c for x in a[k]]
  for i in range(k+1,len(a)):
   c=a[i][j];a[i]=[x-c*y for x,y in zip(a[i],a[k])]
  k+=1
 return k

vectors=[v for v in product((-1,0,1),repeat=3) if any(v)]
for u,v in product(vectors,repeat=2):
 minors=[u[i]*v[j]-u[j]*v[i] for i in range(3) for j in range(i+1,3)]
 ck((rank([u,v])==2)==any(minors),'polynomial_rank')
 ck(rank([u,v])==rank([tuple(-x for x in u),tuple(-x for x in v)]),'polynomial_rank')
 # Adding a zero constant coordinate cannot introduce a nonzero constant relation.
 ck(rank([u,v])==rank([(0,)+u,(0,)+v]),'zero_constant')

pairs=[]
for N in range(1,4):
 ps=list(permutations(range(N)))
 pairs.extend((a,b) for a,b in product(ps,repeat=2) if compose(a,b)==compose(b,a))
pairs.extend([
 ((0,1,2,3),(0,1,2,3)),
 ((1,0,2,3),(0,1,3,2)),
 ((1,2,3,0),(2,3,0,1)),
 ((1,0,3,2),(2,3,0,1)),
 ((1,2,0,3),(0,1,2,3))])
systems=0;nonergodic=0
for a,b in pairs:
 N=len(a);L=lcm(order(a),order(b));G=list(product(range(L),repeat=2));index={g:i for i,g in enumerate(G)}
 ck(compose(a,b)==compose(b,a),'commutation')
 ap=[power(a,k) for k in range(L)];bp=[power(b,k) for k in range(L)]
 remaining=set(range(N));orbits=[]
 while remaining:
  x=min(remaining);O={ap[s][bp[t][x]] for s,t in G};orbits.append(O);remaining-=O
 den=sum(range(1,len(orbits)+1));weights={x:F(i+1,den*len(O)) for i,O in enumerate(orbits) for x in O}
 ck(sum(weights.values(),F(0))==1,'invariant_weights')
 for x in range(N):ck(weights[x]==weights[a[x]]==weights[b[x]],'invariant_weights')
 for mask in range(1<<N):
  A={x for x in range(N) if mask>>x&1};systems+=1;nonergodic+=len(orbits)>1
  Phi={x:tuple(int(ap[s][bp[t][x]] in A) for s,t in G) for x in range(N)}
  nu={}
  for x,z in Phi.items():nu[z]=nu.get(z,F(0))+weights[x]
  ck(sum(nu.values(),F(0))==1,'symbolic_pushforward')
  for i,T in enumerate((a,b)):
   shift=lambda z:tuple(z[index[((s+(i==0))%L,(t+(i==1))%L)]] for s,t in G)
   for x,z in Phi.items():ck(shift(z)==Phi[T[x]],'symbolic_equivariance')
   for z,mass in nu.items():ck(nu[shift(z)]==mass,'factor_invariance')
   for k in range(-3,4):
    im={power(T,k)[x] for x in A}
    coordinate=((-k)%L,0) if i==0 else (0,(-k)%L)
    for x in range(N):ck((x in im)==bool(Phi[x][index[coordinate]]),'set_sign')
  for n in range(1,L+2):
   # Independent polynomials of the same degree n^2 and n^2+n.
   p,q=n*n,n*n+n
   im1={power(a,p)[x] for x in A};im2={power(b,q)[x] for x in A}
   original=sum((weights[x] for x in A&im1&im2),F(0))
   factored=sum((mass for z,mass in nu.items() if z[index[(0,0)]] and z[index[(-p%L,0)]] and z[index[(0,-q%L)]]),F(0))
   ck(original==factored,'intersection_measure')
   # Original positive image equals inverse transformation negative image.
   ck(im1=={power(power(a,-1),-p)[x] for x in A},'inverse_conversion')
  for r in range(1,4):
   n=L*r
   ck({power(a,n*n)[x] for x in A}==A,'finite_period_control')
   ck({power(b,n*n+n)[x] for x in A}==A,'finite_period_control')
  mu=sum((weights[x] for x in A),F(0));ck(mu>=mu**3,'degenerate_sets_and_recurrence')

# Bernoulli-coordinate diagnostic for sharpness: distinct positive evaluation
# sites of (j+1)n^j ensure the exact intersection probability alpha^(ell+1).
for ell in range(1,9):
 for n in range(1,51):
  sites=[0]+[(j+1)*n**j for j in range(1,ell+1)]
  ck(len(set(sites))==ell+1,'sharp_exponent_sites')
  for alpha in [F(1,5),F(1,2),F(4,5)]:
   prob=F(1)
   for _ in sites:prob*=alpha
   ck(prob==alpha**(ell+1),'sharp_exponent_probability')
   ck(prob<alpha**ell,'sharp_exponent_probability')
root=Path(__file__).resolve().parent
receipt={'status':'PASS','assertions':sum(counts.values()),'groups':counts,'finite_system_set_cases':systems,'nonergodic_system_set_cases':nonergodic,'scope':'Independent finite algebra, symbolic-factor and sharpness diagnostics. General recurrence and syndeticity are credited to the published theorem, not established by these tests.','artifact_sha256':hashlib.sha256((root/'author_replay/KNOWN_RESULT.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(root/'independent_results.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(json.dumps(receipt,indent=2,sort_keys=True))
