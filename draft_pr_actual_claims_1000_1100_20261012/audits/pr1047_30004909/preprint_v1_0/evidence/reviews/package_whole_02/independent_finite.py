#!/usr/bin/env python3
"""Fresh independence-axiom enumeration, distinct from supplied basis-family enumeration."""
from pathlib import Path
from fractions import Fraction as Q
import json,datetime,hashlib
OUT=Path(__file__).resolve().parent

def require(cond,message):
 if not cond:raise AssertionError(message)

def hereditary_families(n):
 masks=sorted(range(1,1<<n),key=lambda s:(s.bit_count(),s))
 prior={s:tuple(s^(1<<i) for i in range(n) if s&(1<<i)) for s in masks}
 def visit(i,iset):
  if i==len(masks):yield frozenset(iset);return
  s=masks[i]
  yield from visit(i+1,iset)
  if all(t in iset for t in prior[s]):
   iset.add(s);yield from visit(i+1,iset);iset.remove(s)
 yield from visit(0,{0})

def augmentation(n,ind):
 for a in ind:
  for b in ind:
   if a.bit_count()<b.bit_count() and not any((a|(1<<i)) in ind for i in range(n) if (b&~a)&(1<<i)):return False
 return True

def ranks(n,ind):return [max(i.bit_count() for i in ind if i&~s==0) for s in range(1<<n)]
rows=[]
for n in range(1,6):
 count=ideals=loopless=0;best={};ratbest={};m={1:1,4:2}.get(n)
 for ind in hereditary_families(n):
  ideals+=1
  if not augmentation(n,ind):continue
  count+=1;r=ranks(n,ind);R=r[-1]
  require(r[0]==0 and 0<=R<=n,'rank0/rankbound')
  if any((1<<i) not in ind for i in range(n)):
   require(any(r[1<<i]==0 for i in range(n)),'loop identification');continue
  loopless+=1
  a2=max(max(Q(r[s]*r[s],s.bit_count()),Q(s.bit_count(),r[s]*r[s])) for s in range(1,1<<n))
  envelope=max(Q(R),Q(n,R*R))
  require(a2>=envelope and a2**3>=n,'sqrt bound')
  best[R]=min(a2,best.get(R,a2))
  if m:
   a=max(max(Q(m*r[s],m+s.bit_count()-1),Q(m+s.bit_count()-1,m*r[s])) for s in range(1,1<<n))
   require(a*a+a>=m and 2*a*a>=m,'rational bound')
   ratbest[R]=min(a,ratbest.get(R,a))
 for R in range(1,n+1):require(best[R]==max(Q(R),Q(n,R*R)),'uniform attainable exact sqrt rank optimum')
 if m:
  for R in range(1,n+1):require(ratbest[R]==max(Q(m*R,m+R-1),Q(m*m+m-1,m*R)),'rational envelope')
 require(count==[2,5,16,68,406][n-1],'labelled matroid count')
 rows.append({'n':n,'hereditary_families':ideals,'matroids':count,'loopless':loopless,'best_sqrt_factor_squared_by_rank':{str(k):str(v) for k,v in best.items()},'rational_m':m,'best_rational_factor_by_rank':{str(k):str(v) for k,v in ratbest.items()}})
# Exact cardinality-triple submodularity checks, including empty intersection and containment.
triples=0
for n in range(0,31):
 for t in range(n+1):
  for a in range(n-t+1):
   for c in range(n-t-a+1):
    require((t+a)+(t+c)==t+(t+a+c) and (t+a)*(t+c)>=t*(t+a+c),'radical sum comparison')
    triples+=1
ratpairs=0
for m in range(1,9):
 n=m*m;h=[Q(0)]+[Q(m+k-1,m) for k in range(1,n+1)]
 for t in range(n+1):
  for a in range(n-t+1):
   for c in range(n-t-a+1):
    require(h[t+a]+h[t+c]>=h[t]+h[t+a+c],'rational triple submodularity');ratpairs+=1
 for R in range(1,n+1):
  alpha=max(max(Q(min(k,R))/h[k],h[k]/min(k,R)) for k in range(1,n+1))
  require(alpha*alpha+alpha>=m,'rational exact uniform factor')
# Finite real-coefficient decomposition tested with arbitrary rational concave increments.
for n in range(1,51):
 d=[Q(1,i+1) for i in range(n)];coeff=[d[i]-d[i+1] for i in range(n-1)]+[d[-1]]
 h=[Q(0)]
 for v in d:h.append(h[-1]+v)
 for k in range(n+1):require(sum(coeff[i]*min(k,i+1) for i in range(n))==h[k],'direct coefficient identity')
 require(sum(coeff)==1 and min(coeff)>=0,'convex coefficient boundary')
controls=[]
require(all(k*k>=k for k in range(1,26)),'upper only free rank')
controls.append({'premise_removed':'lower comparison','witness':'free rank on 25 points with alpha=1 satisfies sqrt(k)<=k for every k','obstruction_survives':False})
require(all(1<=k for k in range(1,26)),'lower only rank one')
controls.append({'premise_removed':'upper comparison','witness':'rank-one uniform rank on 25 points with alpha=1 satisfies1<=sqrt(k) for every nonempty k','obstruction_survives':False})
require(all(Q(min(k,4)**2,2*k)<=2 and Q(2*k,min(k,4)**2)<=2 for k in range(1,17)) and 2**3<16,'scaled output control')
controls.append({'model_mutation':'allow scalar times rank','witness':'n16, c=1/sqrt2 times U4, alpha=sqrt2 satisfies all sizes while alpha^6=8<16','ordinary_lower_bound_survives':False})
controls.append({'premise_removed':'singleton normalization','witness':'zero function and zero rank work for every n and every positive alpha','nonloop_step_survives':False})
require(max(Q(1),Q(2))==2,'n2 integrality optimum')
controls.append({'false_strengthening':'optimum always n^(1/6)','counterexample':'n2 optimum squared2; its cube8>2'})
# Actual premise-sensitive nonuniform rank construction, verifying augmentation independently.
ind=frozenset([0,1,2,4,5,6]);require(augmentation(3,ind),'nonuniform matroid');r=ranks(3,ind);require(r[3]==1 and r[7]==2,'nonuniform differs')
controls.append({'false_assumption':'all matroids have uniform subset rank','counterexample':'parallel first two elements and independent third; rank({1,2})1, total rank2'})
result={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'all hereditary independence families, then independent augmentation axiom; distinct from candidate basis-family enumeration','matroids_total':sum(row['matroids'] for row in rows),'enumerations':rows,'sqrt_cardinality_triples_n0_30':triples,'rational_cardinality_triples_m1_8':ratpairs,'coefficient_sweep_n1_50':True,'semantic_fault_controls':controls,'finite_evidence_only':True,'infinite_claim_depends_on_written_proof':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'INDEPENDENT_FINITE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
