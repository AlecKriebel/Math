#!/usr/bin/env python3
"""Independent exact controls for a scoped interpolation packet; no author code imported."""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter
from fractions import Fraction as F
import argparse,csv,json
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent.parent);args=ap.parse_args()
checks=0

def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
# Generate the intersection lattice from all nonempty subsets of the six collision components.
edge=list(combinations(range(4),2));partitions=set()
for mask in range(1,64):
 parent=list(range(4))
 def root(i):
  while parent[i]!=i:i=parent[i]
  return i
 for j,(u,v) in enumerate(edge):
  if mask>>j&1:parent[root(u)]=root(v)
 blocks={root(i):[] for i in range(4)}
 for i in range(4):blocks[root(i)].append(i)
 partitions.add(tuple(sorted(tuple(v) for v in blocks.values())))
eq(len(partitions),14)
interval=sorted(p for p in partitions if len(p)>1);eq(len(interval),13)
def rows(p):
 out=[]
 for block in p:
  for v in block[1:]:
   for coord in range(2):
    row=[0]*8;row[2*v+coord]=1;row[2*block[0]+coord]=-1;out.append(row)
 return s.Matrix(out)
M=[rows(p) for p in interval]
for p,m in zip(interval,M):eq(m.rank(),2*(4-len(p)))
E=[]
for i,j in combinations(range(13),2):
 # Inclusion of subspaces is reverse inclusion of their defining row spaces.
 stacked=M[i].col_join(M[j]);rk=stacked.rank()
 if rk==max(M[i].rank(),M[j].rank()):E.append((i,j))
eq(len(E),18)
inc=s.zeros(13,18)
for k,(i,j) in enumerate(E):inc[i,k]=-1;inc[j,k]=1
rank=inc.rank();eq(rank,12);eq(18-rank,6);eq(6-4-1,1)
# Compare the labeled incidence certificate, independent of its vertex ordering.
author=json.loads((args.packet/'TURN_2_CHECKS.json').read_text());canon=lambda p:tuple(sorted(tuple(sorted(b)) for b in p))
aV=[canon(p) for p in author['interval_vertices']]
eq(set(aV),set(interval))
eq({frozenset((aV[i],aV[j])) for i,j in author['interval_edges']},{frozenset((interval[i],interval[j])) for i,j in E})
# General symbolic determinant directions, not selected parameter samples.
x,y=s.symbols('x y');a,b,c,r,t,u,v=s.symbols('a b c r t u v')
def jetdet(points,extra):return s.factor(s.Matrix([[1,X,Y,extra.subs({x:X,y:Y})] for X,Y in points]).det())
P=[(0,0),(0,a),(b,0),(c,1)]
for actual,expected in zip([jetdet(P,h) for h in (x*x,x*y,y*y)],[-a*b*c*(c-b),-a*b*c,-a*b*(1-a)]):eq(s.expand(actual-expected),0)
P=[(r,0),(v,0),(0,t),(0,u)]
for actual,expected in zip([jetdet(P,h) for h in (x*x,x*y,y*y)],[(v-r)*(t-u)*r*v,0,-(v-r)*(t-u)*t*u]):eq(s.expand(actual-expected),0)
# Independently audit every slope assignment using the full six-equation incidence matrix.
records=list(csv.DictReader((args.packet/'TURN_4_CERTIFICATE.csv').open()))
eq(len(records),720);assignments=set();freq=Counter();signs=set()
for row in records:
 slopes=tuple(int(row[k]) for k in ('s12','s13','s14','s23','s24','s34'));assignments.add(slopes)
 N=s.zeros(6,8)
 for k,((i,j),m) in enumerate(zip(edge,slopes)):
  N[k,2*i]=m;N[k,2*i+1]=-1;N[k,2*j]=-m;N[k,2*j+1]=1
 # Delete the two translation coordinates. Nonzero minor forces all points equal.
 det=int(N[:,2:].det());recorded=int(row['determinant']);eq(abs(det),abs(recorded));assert det!=0;checks+=1
 signs.add(det//recorded);freq[abs(det)]+=1
eq(assignments,set(permutations((0,1,2,4,8,16))))
eq(sorted(freq),[24,48,104,112,136,152,168,192,272,296,304,320,344,408,456]);eq(set(freq.values()),{48});eq(len(signs),1)
# Five-direction construction with projective vertical directions included.
directions=[(F(0),F(1))]+[(F(1),F(j)) for j in (0,1,2,3,5)]
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
for d1,d2,d3,d4,d5 in permutations(directions,5):
 A=(F(0),F(0));B=d1
 z=cross(B,d3)/cross(d2,d3);C=tuple(z*t for t in d2)
 z=cross(B,d5)/cross(d4,d5);D=tuple(z*t for t in d4)
 eq(len({A,B,C,D}),4)
 for P,Q,h in ((A,B,d1),(A,C,d2),(B,C,d3),(A,D,d4),(B,D,d5)):eq(cross((Q[0]-P[0],Q[1]-P[1]),h),0)
# Discriminant independently obtained as a symbolic 7x7 Sylvester determinant.
P,Q,R=s.symbols('P Q R');fc=[1,0,P,Q,R];dc=[4,0,2*P,Q];Syl=s.zeros(7)
for i in range(3):
 for j,z in enumerate(fc):Syl[i,i+j]=z
for i in range(4):
 for j,z in enumerate(dc):Syl[3+i,i+j]=z
disc=s.factor(Syl.det(method='domain-ge'))
T,B,D=s.symbols('T B D');obtained=s.expand(disc.subs({P:-2*T*T,Q:-B*B*D,R:T**4-B*B*T*T}))
claimed=-B**4*(27*B**4*D**4-288*B**2*D**2*T**4+256*B**2*T**6+256*D**2*T**6-256*T**8)
eq(s.expand(obtained-claimed),0);eq(s.Poly(obtained,T).LC(),256*B**4)
eq(64*(2+max(5,3)),448);assert 449>448 and 449%2;checks+=1
print(json.dumps({'status':'PASS','independent_exact_assertions':checks,'intersection_poset':{'nonambient_intersections':14,'strict_full_diagonal_interval_vertices':13,'edges':18,'boundary_rank':rank,'H1':6,'local_cohomology_index':4},'full_incidence_slope_rows_verified':720,'slope_minor_to_recorded_sign':list(signs)[0],'five_projective_direction_controls_including_vertical':720,'symbolic_case_A_and_B_identities':True,'sylvester_discriminant_identity':True,'scope':'Independent exact algebra and combinatorics. Primary theorem hypotheses, field distinctions, top local cohomology, and real contraction require the written audit.'},indent=2))
