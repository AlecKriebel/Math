"""Independent exact checks. Does not import the submitted checkers."""
from pathlib import Path
from itertools import combinations, permutations, product
from collections import Counter
from fractions import Fraction as Q
import hashlib,json,math
import sympy as s
ROOT=Path(__file__).resolve().parent
p=(3,1,5,2,4); n=5
f=lambda j:p[(j-1)%n]+n*((j-1)//n)+(n if p[(j-1)%n] <= (j-1)%n+1 else 0)
J=[]
for r in range(1,n+1):
 I={(f(j)-1)%n+1 for j in range(r-n,r) if r<=f(j)}
 assert len(I)==3 and r in I
 J.append(sorted(I-{r}))
eps=[(-1)**sum(p[j-1]<=j for j in range(1,r)) for r in range(1,n+1)]
assert J==[[2,4],[3,4],[1,4],[1,5],[1,2]]
assert eps==[1,1,-1,-1,1]

# Reconstruct gamma from source necklace formula in the fixed sin(t),cos(t) basis,
# using rational points of the unit circle to avoid floating trig/determinants.
def sc(q): return (2*q/(1+q*q),(1-q*q)/(1+q*q))
def diff(x,y): return x[0]*y[1]-x[1]*y[0]
def add(x,y):return (x[0]*y[1]+x[1]*y[0],x[1]*y[1]-x[0]*y[0])
def H(x,y):
 A,B,C=x;D,E,F=y
 return tuple(map(Q,(0,B*E,B*D,A*E,A*D,A*F,C*E,C*D,C*F,0)))
def normal(v):
 z=sum(v); assert z!=0
 return tuple(x/z for x in v)
unit_inputs=[Q(i,7) for i in range(1,7)]
checked=0
for qa,qb,qc,qd in product(unit_inputs,repeat=4):
 if qc>=qd:continue
 a,b,c,d=map(sc,(qa,qb,qc,qd))
 angles=[(-a[0],a[1]),(Q(0),Q(1)),b,c,d]
 # l_i(t) = cos(theta_i) sin(t) - sin(theta_i) cos(t).
 cols=[]
 for pair,e in zip(J,eps):
  (sp,cp),(sq,cq)=[angles[i-1] for i in pair]
  cols.append([e*cp*cq,-e*(cp*sq+sp*cq),e*sp*sq])
 M=s.Matrix(3,5,lambda i,j:cols[j][i])
 minors=[Q(M[:,idx].det()) for idx in combinations(range(5),3)]
 A,B,C=a[0],b[0],add(a,b)[0]
 D,E,F=c[0],diff(d,c),d[0]
 assert normal(minors)==normal(H((A,B,C),(D,E,F)))
 checked+=1

# All-boundary symbolic inverse identities: normalization is sum 2.
A,B,D,E=s.symbols('A B D E');C=2-A-B;F=2-D-E
v=[0,B*E,B*D,A*E,A*D,A*F,C*E,C*D,C*F,0]
den=v[4]+v[3]+v[7]+v[6]
L=2/(1+(v[2]+v[1])/den);R=2/(1+(v[5]+v[8])/den)
recon=[L*(v[4]+v[3])/den,L*(v[2]+v[1])/den,L*(v[7]+v[6])/den,
       R*(v[4]+v[7])/den,R*(v[3]+v[6])/den,R*(v[5]+v[8])/den]
assert all(s.cancel(x-y)==0 for x,y in zip(recon,[A,B,C,D,E,F]))
# Check all 49 face-type pairs, with one exact relative-interior point per face;
# this tests only H, NOT the source-defined stratification.
vertices=[(Q(0),Q(1),Q(1)),(Q(1),Q(0),Q(1)),(Q(1),Q(1),Q(0))]
facepoints=vertices+[tuple(sum(v[k] for v in pair)/2 for k in range(3)) for pair in combinations(vertices,2)]+[(Q(2,3),)*3]
assert len(facepoints)==7
vectors=[normal(H(x,y)) for x,y in product(facepoints,repeat=2)]
assert len(set(vectors))==49

# Source strand test implemented via alternation in sorted endpoints, with strands
# initially indexed by START rather than by terminal label as in submitted code.
def strand_edges(perm):
 intervals=[sorted((2*i+1,2*(j-1))) for i,j in enumerate(perm)]
 edges=[]
 for i,j in combinations(range(len(perm)),2):
  a,b=intervals[i];c,d=intervals[j]
  if a<c<b<d or c<a<d<b: edges.append((i,j))
 return edges
def connected(n,edges):
 seen={0}
 for _ in range(n):
  seen|={j for i,j in edges if i in seen}|{i for i,j in edges if j in seen}
 return len(seen)==n
strand_counts={}
for nn in range(2,9):
 counts=Counter()
 for perm in permutations(range(1,nn+1)):
  edges=strand_edges(perm)
  if connected(nn,edges):
   disps=[(j-i-1)%nn or nn for i,j in enumerate(perm)]
   assert all(2<=d<=nn-1 for d in disps)
   k=sum(disps)//nn;counts[k]+=1
   if k in (2,nn-1):assert all(d==k for d in disps)
 strand_counts[nn]=dict(sorted(counts.items()))
submitted=json.loads((ROOT/'strand_enumeration.json').read_text())
for nn,counts in strand_counts.items():
 if nn>=3:assert {str(k):v for k,v in counts.items()}==submitted[str(nn)]['by_rank']
bowtie_edges=sorted(tuple(sorted((p[i],p[j]))) for i,j in strand_edges(p))
assert bowtie_edges==[(1,2),(1,3),(2,3),(2,4),(2,5),(4,5)]
# Generic formula genuinely drops rank at admissible a=pi/3,c=2pi/3,b=pi/6,d=5pi/6.
r3=s.sqrt(3)
angles=[(-r3/2,s.Rational(1,2)),(0,1),(s.Rational(1,2),r3/2),(r3/2,-s.Rational(1,2)),(s.Rational(1,2),-r3/2)]
cols=[]
for pair,e in zip(J,eps):
 (sp,cp),(sq,cq)=[angles[i-1] for i in pair]
 cols.append([e*cp*cq,-e*(cp*sq+sp*cq),e*sp*sq])
M=s.Matrix(3,5,lambda i,j:cols[j][i]); assert M.rank()==2
out={'status':'PASS','necklace_reduced_sets':J,'epsilon':eps,'exact_generic_gamma_samples':checked,'symbolic_boundary_inverse':'PASS','product_face_points_checked':49,'product_face_points_do_not_certify_source_strata':True,'strand_counts':strand_counts,'bowtie_crossings':bowtie_edges,'exceptional_admissible_gamma_rank':2}
(ROOT/'independent_audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
