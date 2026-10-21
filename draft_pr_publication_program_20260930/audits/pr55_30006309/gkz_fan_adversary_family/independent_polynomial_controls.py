#!/usr/bin/python3
"""Exact independent controls for the GKZ labels, signs, projection and walls."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import hashlib, json, random
import sympy as sp
ROOT=Path(__file__).resolve().parent
cfg=json.loads((ROOT/'independent_input.json').read_text())
rng=random.Random(cfg['seed']);checks=0

def need(v,msg):
 global checks
 checks+=1
 if not v: raise AssertionError(msg)

def det(a):
 a=[[F(x) for x in row] for row in a];out=F(1)
 for i in range(len(a)):
  j=next((j for j in range(i,len(a)) if a[j][i]),None)
  if j is None:return F(0)
  if j!=i:a[j],a[i]=a[i],a[j];out=-out
  pivot=a[i][i];out*=pivot
  for k in range(i+1,len(a)):
   r=a[k][i]/pivot
   for t in range(i,len(a)):a[k][t]-=r*a[i][t]
 return out

def solve(a,b):
 a=[[F(x) for x in row]+[F(y)] for row,y in zip(a,b)];n=len(a)
 for i in range(n):
  j=next((j for j in range(i,n) if a[j][i]),None)
  if j is None:return None
  a[j],a[i]=a[i],a[j];p=a[i][i];a[i]=[x/p for x in a[i]]
  for k in range(n):
   if k!=i:
    p=a[k][i];a[k]=[x-p*y for x,y in zip(a[k],a[i])]
 return [row[-1] for row in a]

def lower(points,h):
 n=len(points[0]);out=[]
 for ids in combinations(range(len(points)),n+1):
  plane=solve([[1]+list(points[i]) for i in ids],[h[i] for i in ids])
  if plane is None:continue
  gaps=[F(h[i])-sum(c*x for c,x in zip(plane,[1]+list(p))) for i,p in enumerate(points)]
  if min(gaps)>=0:
   if any(gaps[i]==0 for i in range(len(points)) if i not in ids):return None
   out.append(ids)
 return tuple(out)

def lower_line(h):
 v=[]
 for i in range(len(h)):
  while len(v)>=2 and (h[v[-1]]-h[v[-2]])*(i-v[-1]) >= (h[i]-h[v[-1]])*(v[-1]-v[-2]):v.pop()
  v.append(i)
 return v

def line_mass(v,d):
 m=[0]*(d+1)
 for a,b in zip(v,v[1:]):m[a]+=b-a;m[b]+=b-a
 m[0]-=1;m[-1]-=1
 return tuple(m)

def dot(a,b):return sum(x*y for x,y in zip(a,b))

line_records=[]
x=sp.symbols('x')
for d in cfg['univariate_degrees']:
 cs=sp.symbols('c0:'+str(d+1));disc=sp.Poly(sp.discriminant(sum(c*x**i for i,c in enumerate(cs)),x),*cs)
 support=tuple(mon for mon,co in disc.terms() if co)
 labels={line_mass((0,)+ids+(d,),d) for k in range(d) for ids in combinations(range(1,d),k)}
 need(labels.issubset(set(support)),'Every segment-triangulation label must be an actual discriminant monomial')
 need(all(sum(z)==2*d-2 for z in support),'Discriminant homogeneous degree')
 generic=walls=0
 for q in range(cfg['generic_height_tests_per_degree']):
  while True:
   h=[rng.randrange(-1000,1001) for i in range(d+1)]
   if all((h[b]-h[a])*(c-b)!=(h[c]-h[b])*(b-a) for a,b,c in combinations(range(d+1),3)):break
  m=line_mass(lower_line(h),d);best=min(dot(z,h) for z in support)
  need(dot(m,h)==best,'Lower-height massive label must minimize actual discriminant polynomial')
  need(sum(dot(z,h)==best for z in support)==1,'Generic explicit discriminant face is a point')
  need(dot(m,h)==min(dot(z,h) for z in labels),'All line triangulations give the same minimum')
  generic+=1
 for h in [[0]*(d+1),list(range(d+1)),[i*i for i in range(d+1)],[-i*i for i in range(d+1)]]:
  m=line_mass(lower_line(h),d)
  need(dot(m,h)==min(dot(z,h) for z in support),'Wall/coarse label still minimizes polynomial')
  walls+=1
 line_records.append({'degree':d,'terms':len(support),'triangulation_labels':len(labels),'generic_heights':generic,'wall_or_convex_limit_cases':walls})
# Sign and endpoint subtraction are independently caught on the quadratic.
quad_support=[(0,2,0),(1,0,1)];h=[0,-1,0]
need(dot((0,2,0),h)<max(dot(z,h) for z in quad_support),'Reversing min/max must be detectable')
need((1,2,1) not in quad_support,'Using principal instead of ordinary determinant must be detectable')

# Q = [0,1]^2, P = [0,1]^3. Its hyperdeterminant is the discriminant of
# det(M0+t*M1), derived independently of any massive-vector implementation.
A=((0,0),(0,1),(1,0),(1,1));B=tuple((a[0],a[1],v) for a in A for v in (0,1))
bs=sp.symbols('b0:8');t=sp.symbols('t')
M0=sp.Matrix([[bs[0],bs[2]],[bs[4],bs[6]]]);M1=sp.Matrix([[bs[1],bs[3]],[bs[5],bs[7]]])
hyper=sp.Poly(sp.discriminant((M0+t*M1).det(),t),*bs)
hsupport=tuple(mon for mon,co in hyper.terms() if co)
need(len(hsupport)==12,'Cayley 2x2x2 hyperdeterminant twelve terms')
need(all(sum(z)==4 for z in hsupport),'Hyperdeterminant degree four')

def cube_mass(tets):
 eta=[[0]*8 for k in range(4)]
 for k in range(4):
  faces={tuple(ids) for ids in tets for ids in combinations(ids,k+1)}
  for ids in faces:
   varying=[j for j in range(3) if len({B[i][j] for i in ids})>1]
   if len(varying)!=k:continue
   if k==0:vol=1
   else:vol=abs(det([[B[i][j]-B[ids[0]][j] for j in varying] for i in ids[1:]]))
   need(vol.denominator==1 if isinstance(vol,F) else True,'Integral induced-face volume')
   for i in ids:eta[k][i]+=int(vol)
 return tuple(eta[3][i]-eta[2][i]+eta[1][i]-eta[0][i] for i in range(8))

def square_hurwitz(tris):
 eta2=[0]*4;eta1=[0]*4
 for ids in tris:
  vol=abs(det([[A[i][j]-A[ids[0]][j] for j in range(2)] for i in ids[1:]]))
  for i in ids:eta2[i]+=int(vol)
 edges={ids for tri in tris for ids in combinations(tri,2)}
 for a,b in edges:
  if any(A[a][j]==A[b][j] for j in range(2)):eta1[a]+=1;eta1[b]+=1
 return tuple(2*x-y for x,y in zip(eta2,eta1))

def project(z):return tuple(z[2*i]+z[2*i+1] for i in range(4))
projected_support={project(z) for z in hsupport}
endpoints={(2,0,0,2),(0,2,2,0)}
need(projected_support==endpoints|{(1,1,1,1)},'Exact polynomial exposes a nonextreme projected monomial')
general=0;seen_labels=set();nonextreme_witness=None
while general<cfg['cube_general_height_tests']:
 h=[rng.randrange(-100000,100001) for i in range(8)];tets=lower(B,h)
 if tets is None:continue
 m=cube_mass(tets);best=min(dot(z,h) for z in hsupport)
 need(m in hsupport,'Generic cube massive label must occur in independently derived hyperdeterminant')
 need(dot(m,h)==best,'Full coefficient-height cube minimum label')
 need(sum(dot(z,h)==best for z in hsupport)==1,'Generic cube minimum is unique')
 need(sum(abs(det([[B[i][j]-B[ids[0]][j] for j in range(3)] for i in ids[1:]])) for ids in tets)==6,'Tetrahedra cover cube in normalized volume')
 if project(m)==(1,1,1,1) and nonextreme_witness is None:nonextreme_witness={'height':h,'tetrahedra':[list(x) for x in tets],'massive_vector':list(m),'projection':list(project(m))}
 seen_labels.add(m);general+=1
# Force a central normalized-volume-2 tetrahedron, independent of chance.
for sign in (1,-1):
 base=[-1 if (sum(p)%2==0) else 0 for p in B]
 h=[1000000*x+sign*(17**i) for i,x in enumerate(base)]
 tets=lower(B,h)
 if tets is not None:
  m=cube_mass(tets)
  need(dot(m,h)==min(dot(z,h) for z in hsupport),'Central tetrahedron perturbation label')
  if project(m)==(1,1,1,1) and nonextreme_witness is None:nonextreme_witness={'height':h,'tetrahedra':[list(x) for x in tets],'massive_vector':list(m),'projection':list(project(m))}
need(nonextreme_witness is not None,'A projected discriminant vertex need not be extreme')
equal=0;equal_witnesses=[]
while equal<cfg['cube_equal_column_tests']:
 w=[rng.randrange(-30,31) for i in A]
 tris=lower(A,w)
 if tris is None:continue
 q=[rng.randrange(-200,201) for i in B]
 hh=[cfg['equal_column_scale']*w[i//2]+q[i] for i in range(8)]
 tets=lower(B,hh)
 if tets is None:continue
 need(all(any(set(i//2 for i in tet).issubset(set(tri)) for tri in tris) for tet in tets),'Equal-column perturbation must refine parent product cells')
 m=cube_mass(tets);H=square_hurwitz(tris)
 need(project(m)==H,'Exact product massive projection matches Hurwitz model')
 need(dot(m,hh)==min(dot(z,hh) for z in hsupport),'Perturbed label minimizes polynomial')
 old=[w[i//2] for i in range(8)]
 need(dot(m,old)==min(dot(z,old) for z in hsupport),'Passing perturbation to zero retains weak minimum')
 need(dot(H,w)==min(dot(z,w) for z in endpoints),'Projected support function of actual polynomial')
 if equal<2:equal_witnesses.append({'w':w,'q':q,'parent_triangles':[list(z) for z in tris],'tetrahedra':[list(z) for z in tets],'projection':list(H)})
 equal+=1
result={'status':'PASS_FINITE_EXPLICIT_POLYNOMIAL_CONTROLS','require_evaluations':checks,'univariate':line_records,'cube':{'hyperdeterminant_terms':len(hsupport),'general_generic_heights':general,'distinct_full_labels_seen':len(seen_labels),'equal_column_generic_perturbations':equal,'nonextreme_projection_witness':nonextreme_witness,'two_equal_column_witnesses':equal_witnesses},'negative_controls':2,'scope':cfg['scope'],'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_sha256':hashlib.sha256((ROOT/'independent_input.json').read_bytes()).hexdigest()}
(ROOT/'INDEPENDENT_POLYNOMIAL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('cube','univariate')},sort_keys=True))
