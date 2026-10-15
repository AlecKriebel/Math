"""Round-two independent finite adversarial controls, stdlib exact arithmetic.
Neither author scripts nor previous audit controls are imported.
Universal claims are separately justified in INDEPENDENT_PROOF_SEAL.md.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,permutations
from math import comb
import datetime,json,random
ROOT=Path(__file__).resolve().parent
counts={};details={}
def check(family,condition):
 if not condition:raise AssertionError(family)
 counts[family]=counts.get(family,0)+1

def det(matrix):
 a=[list(map(F,row)) for row in matrix];value=F(1)
 for k in range(len(a)):
  pivot=next((r for r in range(k,len(a)) if a[r][k]),None)
  if pivot is None:return F(0)
  if pivot!=k:a[k],a[pivot]=a[pivot],a[k];value=-value
  v=a[k][k];value*=v
  for r in range(k+1,len(a)):
   if a[r][k]:
    ratio=a[r][k]/v
    for c in range(k+1,len(a)):a[r][c]-=ratio*a[k][c]
 return value

# All 1,024 auxiliary event graphs on five independent Bernoulli selectors.
# The logarithmic lower bound uses a positive rational series, not floating exp.
edgelist=list(combinations(range(5),2))
for mask in range(1,1<<len(edgelist)):
 edges=[e for i,e in enumerate(edgelist) if mask>>i&1]
 degrees=[sum(v in e for e in edges) for v in range(5)]
 overlap=sum(d*(d-1) for d in degrees)
 check('ordered_overlap_identity',overlap==sum(a!=b and bool(set(a)&set(b)) for a in edges for b in edges))
 for p in [F(1,7),F(1,2),F(6,7)]:
  pr=F(0)
  for selected in range(32):
   if not any(selected>>a&1 and selected>>b&1 for a,b in edges):
    k=bin(selected).count('1');pr+=p**k*(1-p)**(5-k)
  mu=len(edges)*p*p;den=mu+overlap*p**3;rate=mu*mu/(2*den)
  z=(1-pr)/(1+pr);term=z;partial=F(0)
  for k in range(200):
   partial+=2*term/(2*k+1)
   if partial>=rate:break
   term*=z*z
  check('exact_all_event_graph_Janson',partial>=rate)
# A false independent-pairs model is rejected by a two-edge star.
p=F(1,2);actual=F(5,8);independent=(1-p*p)**2
check('dependency_mutation_rejected',actual>independent)
print('Exhaustive auxiliary-graph probability controls PASS',flush=True)

# Exhaustively clean all 1,024 triangle families on five labels, using two
# different deterministic choices of which member of each collision to remove.
triples=list(combinations(range(5),3))
for mask in range(1<<len(triples)):
 family=[t for i,t in enumerate(triples) if mask>>i&1]
 collisions=[(a,b) for a,b in combinations(family,2) if len(set(a)&set(b))==2]
 for which in [0,1]:
  deleted={pair[which] for pair in collisions};survive=[t for t in family if t not in deleted]
  check('exhaustive_adaptive_cleanup',len(deleted)<=len(collisions) and len(survive)>=len(family)-len(collisions) and all(len(set(a)&set(b))<=1 for a,b in combinations(survive,2)))
print('All small cleanup controls PASS',flush=True)

# Seven-point controls with random nonconvex integer coordinates and severe
# invertible affine distortion. Each five-minor and every six-circuit is exact.
rng=random.Random(261001439);accepted=0;attempts=0
while accepted<40:
 attempts+=1;points=[tuple(rng.randrange(-17,18) for _ in range(4)) for _ in range(7)]
 minors={s:det([[1]*5]+[[points[i][d] for i in s] for d in range(4)]) for s in combinations(range(7),5)}
 if not all(minors.values()):continue
 partitions=[]
 for s in combinations(range(7),6):
  coeff=[(-1)**j*minors[s[:j]+s[j+1:]] for j in range(6)]
  check('six_point_affine_circuit',sum(coeff)==0 and all(sum(coeff[j]*points[s[j]][d] for j in range(6))==0 for d in range(4)))
  if sum(x>0 for x in coeff)==3:partitions.append(s)
 check('fresh_balanced_seven_point',bool(partitions))
 distorted=[(-p[0]*2**80+31,p[1]+p[0]*2**50,p[2]*2**-0+19,p[3]*2**20-7) for p in points]
 dm={s:det([[1]*5]+[[distorted[i][d] for i in s] for d in range(4)]) for s in minors}
 check('invertible_distortion_preserves_order_type',all(dm[s]/minors[s]==-2**100 for s in minors))
 accepted+=1
print('Generic circuits and severe affine-distortion controls PASS',flush=True)

# Independent finite parameter certificate, avoiding evaluation of huge exp.
n=1<<256;m=1<<320;p=F(1,1<<384);M=comb(n,3);c=F(1,645120);rate=c*c*(1<<384)/2
entropy_upper=20*n*256+321+3*m*256
bounds=[n>=12,n**7>=107520**4,F(comb(n,6),7)-m*M>=c*n**6,F(M*M,2)*p*p+M**3*p**3<=n**4*(1<<128),rate>1<<343,entropy_upper<1<<331,rate-entropy_upper>1<<342,M*p>1<<379,M*p/2-m>n,F(n,4*m)==F(1,1<<66),F(1,8)+F(1,1<<66)+4/(M*p)<1]
for b in bounds:check('finite_exact_constants',b)
print('Finite parameter controls PASS',flush=True)

# Exact feasibility for all disjoint nonempty subdivision faces. A nonempty
# bounded convex-intersection polytope has a basic feasible solution with at
# most five positive variables. Overdetermined systems reject spurious BFS.
def solve(columns):
 width=len(columns);rhs=[0,0,0,1,1]
 a=[[F(columns[j][i]) for j in range(width)]+[F(rhs[i])] for i in range(5)];row=0
 for col in range(width):
  pivot=next((i for i in range(row,5) if a[i][col]),None)
  if pivot is None:return None
  a[row],a[pivot]=a[pivot],a[row];v=a[row][col];a[row]=[x/v for x in a[row]]
  for i in range(5):
   if i!=row and a[i][col]:
    v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[row])]
  row+=1
 if any(not any(r[:-1]) and r[-1] for r in a):return None
 return [a[i][-1] for i in range(width)]
def intersects(A,B,positions):
 cols=[positions[v]+(1,0) for v in A]+[tuple(-x for x in positions[v])+(0,1) for v in B]
 for k in range(2,min(5,len(cols))+1):
  for support in combinations(range(len(cols)),k):
   if not any(i<len(A) for i in support) or not any(i>=len(A) for i in support):continue
   sol=solve([cols[i] for i in support])
   if sol is not None and min(sol)>=0:return True
 return False
families={'cycle4':[(0,1,2),(2,3,4),(4,5,6),(6,7,0)],'valence4':[(0,1,2),(0,3,4),(0,5,6),(0,7,8)],'disconnected':[(0,1,2),(3,4,5)],'single':[(0,1,2)]}
for name,family in families.items():
 vertices=sorted(set(v for t in family for v in t));nodes=[('v',v) for v in vertices]+[('f',i) for i in range(len(family))]
 rng.shuffle(nodes);D=1<<44
 positions={node:(t*D,t*t*D,t*t*t*D) for t,node in enumerate(nodes,1)}
 facets=[]
 for i,t in enumerate(family):
  f=('f',i)
  for u,v in combinations(t,2):
   edge=('e',min(u,v),max(u,v));positions[edge]=tuple(positions[f][k]+(positions[('v',u)][k]+positions[('v',v)][k]-2*positions[f][k])//D for k in range(3))
  for u,v in permutations(t,2):facets.append((f,('v',u),('e',min(u,v),max(u,v))))
 faces=set()
 for tri in facets:
  for k in [1,2,3]:
   for subset in combinations(tri,k):faces.add(frozenset(subset))
 checked=0
 for A,B in combinations(sorted(faces,key=lambda s:str(sorted(s))),2):
  if A&B:continue
  check('all_disjoint_subdivision_faces_'+name,not intersects(tuple(A),tuple(B),positions));checked+=1
 details[name]={'original_facets':len(family),'subdivision_faces':len(faces),'disjoint_face_pairs':checked,'epsilon':'1/2^44','node_parameters':'independent fixed-seed permutation'}
 print(name,'all-face geometry PASS',checked,flush=True)
# Fault control: coincident vertex images must be detected as intersecting.
check('geometry_fault_control',intersects((0,),(1,),{0:(0,0,0),1:(0,0,0)}))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':counts,'total':sum(counts.values()),'geometry':details,'generic_configurations':accepted,'attempts':attempts,'scope':'Fresh finite controls supplement independent universal analysis; not witness enumeration, priority certificate, or formal verification.'}
(ROOT/'FRESH_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
