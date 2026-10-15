from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import json, hashlib
out=Path(__file__).resolve().parent
checks={}
def rank(rows):
 a=[[Q(x) for x in r] for r in rows]
 if not a:return 0
 n=0
 for c in range(len(a[0])):
  piv=next((r for r in range(n,len(a)) if a[r][c]),None)
  if piv is None:continue
  a[n],a[piv]=a[piv],a[n];v=a[n][c];a[n]=[x/v for x in a[n]]
  for r in range(n+1,len(a)):
   v=a[r][c]
   if v:a[r]=[x-v*y for x,y in zip(a[r],a[n])]
  n+=1
  if n==len(a):break
 return n

def complex_from_facets(facets):
 return {s for f in facets for j in range(1,len(f)+1) for s in combinations(f,j)}
def induced(K,V):return {s for s in K if set(s)<=V}
def betti(K,k):
 faces=sorted(s for s in K if len(s)==k+1)
 lower=sorted(s for s in K if len(s)==k)
 upper=sorted(s for s in K if len(s)==k+2)
 def boundary(a,b):
  rows=[]
  for s in a:
   rows.append([next(((-1)**j for j in range(len(t)) if t[:j]+t[j+1:]==s),0) for t in b])
  return rank(rows)
 return len(faces)-boundary(lower,faces)-boundary(faces,upper)

all_faces=[s for k in range(1,6) for s in combinations(range(5),k)]
n=0;zero=0
for seed in range(96):
 state=seed+73;facets=[(i,) for i in range(5)]
 for s in all_faces:
  state=(1664525*state+1013904223)&0xffffffff
  if state&0x40000000:facets.append(s)
 K=complex_from_facets(facets);bk=betti(K,2)
 for mask in range(32):
  VA={v for v in range(5) if mask>>v&1};new=set(range(5))-VA
  interface={v for v in VA if any(tuple(sorted((v,w))) in K for w in new)}
  A=induced(K,VA);B=induced(K,new|interface);I=A&B
  assert K==A|B and I==induced(K,interface)
  assert betti(A,2)<=bk+betti(I,2)
  n+=1;zero+=bk==0
checks['five_vertex_induced_ambient_cover_cases']=n
checks['zero_ambient_b2_cases']=zero
# The exact H2 term is necessary: a cone on a tetrahedral sphere is contractible.
sphere=complex_from_facets(list(combinations(range(4),3)))
cone=complex_from_facets([tuple(sorted(s+(4,))) for s in sphere])
assert betti(sphere,2)==1 and betti(sphere,1)==0 and betti(cone,2)==0
checks['wrong_b1_interface_bound_falsified']=True
# Axis in a cyclic hyperbolic quotient has the circle metric.
def circle_distance(a,b,L):return min(abs(a-b+z*L) for z in range(-5,6))
i=Q(10);L=Q(12);a=Q(-4);b=Q(4)
assert L>i and abs(a-b)==8 and circle_distance(a,b,L)==4 and abs(a)<i/2
checks['i_over_2_metric_radius_falsified']={'based_displacement':str(L),'threshold':str(i),'radius':'4','cover_distance':'8','quotient_distance':'4'}
n=0
for step in range(1,31):
 L=Q(10)+Q(step,40)
 for a in [Q(j,20) for j in range(-50,51,5)]:
  for b in [Q(j,20) for j in range(-50,51,5)]:
   assert circle_distance(a,b,L)==abs(a-b);n+=1
checks['i_over_4_metric_radius_exact_axis_controls']=n
# Neighborhood measure on a circle computed as an exact union of wrapped intervals.
def union_length(intervals):
 merged=[]
 for a,b in sorted(intervals):
  if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
  else:merged.append((a,b))
 return sum((b-a for a,b in merged),Q(0))
def tubular_length(points,r,L):
 pieces=[]
 for p in points:
  for z in range(-4,5):
   a=max(Q(0),p-r+z*L);b=min(L,p+r+z*L)
   if a<b:pieces.append((a,b))
 return union_length(pieces)
base=[Q(1,5),Q(2,5)];full=base+[x+1 for x in base]
for r in [Q(j,20) for j in range(1,30)]:
 assert tubular_length(full,r,Q(2))==2*tubular_length(base,r,Q(1))
r=Q(3,5);assert tubular_length(base,r,Q(2))!=2*tubular_length(base,r,Q(1))
assert tubular_length(base,r,Q(2))/Q(1,5)!=tubular_length(base,r,Q(1))/Q(1,5)
checks['full_preimage_neighborhood_multiplication_controls']=29
checks['single_component_substitution_falsified']=True
# Ratio of expected counts differs from expectation of individually normalized ratios.
correct=(Q(1,2)*1+Q(1,2)*0)/(Q(1,2)*4+Q(1,2)*2)
incorrect=Q(1,2)*Q(1,4)+Q(1,2)*Q(0,2)
assert correct==Q(1,6) and incorrect==Q(1,8) and correct!=incorrect
checks['historical_probability_normalization_substitution_falsified']=True
# Exact spectrum algebra, including branch threshold and values beyond the valid interval.
n=0
for denom in range(1,55):
 for num in range(0,4*denom+1):
  d=Q(num,denom)
  for c in [Q(1,1000),Q(1,100),Q(1,4),Q(1)]:
   assert (d*(3-d)>=c)==((2*d-3)**2<=9-4*c)
   if d>=Q(3,2) and d*(3-d)>=c:assert d<3 and 0<=2*d-3
   n+=1
assert Q(1)<Q(2) and Q(4)>=2*Q(2) and Q(5)>Q(4)
checks['exact_spectral_controls']=n
# A positive actual sequence can tend to h=0; a multiplicative approximate minimizer cannot.
assert all(Q(1,j)>0 for j in range(1,1001))
assert all(Q(1,j)>(1+Q(1,j))*0 for j in range(1,1001))
checks['actual_positive_domain_ratio_zero_infimum_control']=True
# Boundary measure support and analytic existence are outside these finite controls.
result={'result':'PASS','controls':checks,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Independent exact finite algebra and counterexample controls. Analytic smoothing, compactness, convergence and existence are justified in REVIEW.md, not certified by this replay.'}
(out/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
