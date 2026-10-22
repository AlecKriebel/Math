from pathlib import Path
from itertools import combinations,product
import argparse,importlib.util,json,random
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);args=ap.parse_args();n=0
def check(c):
 global n
 assert c;n+=1
# Exhaust every single-row transition contribution in the nine-label machine.
M=9;far=[{a for a in range(M) if abs(a-c)>=2} for c in range(M)]
for b in range(M):
 for mask in range(1<<M):
  S={a for a in range(M) if mask>>a&1}
  literal={(b,c) for a in S for c in range(M) if abs(a-c)>=2 and abs(b-c)>=2}
  encoded=sum(1<<(M*c+b) for c in range(M) if b in far[c] and S&far[c])
  decoded={(b0,c) for b0 in range(M) for c in range(M) if encoded>>(M*c+b0)&1}
  check(literal==decoded)
# Deficit lemma independently checked on all short families within a six-label universe.
weighted=0
for d,q in [(1,3),(2,3)]:
 lists=[set(A) for k in range(1,2*d+1) for A in combinations(range(6),k)]
 for L in product(lists,repeat=q):
  if sum(max(0,2*d-len(A)) for A in L)>=2*d:continue
  B=set(L[0])
  for A in L[1:]:B={b for b in A if any(abs(a-b)>=d for a in B)}
  check(bool(B));weighted+=1
# Exact original distance-two graph after removal of any residue class.
for size in range(3,101):
 for r in range(3):
  I=set(range(r,size,3));J=[j for j in range(size) if j not in I]
  expected={(J[k],J[k+1]) for k in range(len(J)-1)}
  actual={(a,b) for a,b in combinations(J,2) if b-a<=2};check(expected==actual)
# Independently brute-force anchor assignments, comparing only the final optimum.
spec=importlib.util.spec_from_file_location('frozen_anchor',args.packet/'anchor_solver.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rng=random.Random(13000417);instances=0
for size in range(3,12):
 for d in range(1,4):
  for trial in range(12):
   L=[sorted(rng.sample(range(12),3)) for _ in range(size)]
   for r in range(3):
    I=list(range(r,size,3))
    def cost(vals):
     total=0
     for j in range(size):
      if j in I:continue
      allowed=sum(all(abs(x-v)>=d for i,v in zip(I,vals) if abs(i-j)<=2) for x in L[j])
      total+=max(0,2*d-allowed)
     return total
    best=min(cost(v) for v in product(*(L[i] for i in I)))
    result=mod.optimize_anchors(L,d,r);check(best==result['cost']);check(cost([v for _,v in result['anchors']])==best);instances+=1
# Audit large method certificate directly.
c=json.loads((args.packet/'TURN_4_CERTIFICATE.json').read_text())
L=c['lists'];d=c['d'];f=c['explicit_valid_labeling'];check(len(L)==len(f)==42)
for i,a in enumerate(f):
 check(a in L[i])
 for j in range(max(0,i-2),i):check(abs(a-f[j])>=d)
large_optima=[]
for r in range(3):
 I=list(range(r,len(L),3));factors=[[] for _ in I]
 for j in range(len(L)):
  if j in I:continue
  neighbors=[h for h,i in enumerate(I) if abs(i-j)<=2]
  factors[max(neighbors)].append((j,neighbors))
 scores={None:0}
 for h,i in enumerate(I):
  nxt={}
  for b in L[i]:
   options=[]
   for a,previous in scores.items():
    extra=0
    for j,neighbors in factors[h]:
     forbidden=[b if z==h else a for z in neighbors]
     allowed=sum(all(abs(x-v)>=d for v in forbidden) for x in L[j])
     extra+=max(0,2*d-allowed)
    options.append(previous+extra)
   nxt[b]=min(options)
  scores=nxt
 optimum=min(scores.values());check(optimum==4);large_optima.append(optimum)
print(json.dumps({'status':'PASS','independent_assertions':n,'weighted_families':weighted,'brute_anchor_instances':instances,'large_certificate_optima':large_optima,'scope':'all local transition masks, weighted path witnesses, exact induced geometry and independent exhaustive anchor optima; full closure separately replayed'},indent=2))
