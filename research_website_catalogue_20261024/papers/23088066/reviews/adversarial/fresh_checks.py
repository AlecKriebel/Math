#!/usr/bin/env python3
"""Fresh exact controls from the published formulas; no archived-code imports."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
from random import Random
import json,datetime
checks=[]
def ck(label,ok):
 if not ok:raise RuntimeError(label)
 checks.append(dict(name=label,pass_=True))
def rref(A):
 A=[[F(x) for x in row] for row in A];r=0;piv=[]
 for c in range(len(A[0])):
  k=next((k for k in range(r,len(A)) if A[k][c]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];v=A[r][c];A[r]=[x/v for x in A[r]]
  for k in range(len(A)):
   if k!=r and A[k][c]:
    v=A[k][c];A[k]=[x-v*y for x,y in zip(A[k],A[r])]
  piv.append(c);r+=1
  if r==len(A):break
 return A,piv
def det(A):
 A=[[F(x) for x in row]for row in A];d=F(1)
 for c in range(len(A)):
  k=next((k for k in range(c,len(A)) if A[k][c]),None)
  if k is None:return F(0)
  if k!=c:A[c],A[k]=A[k],A[c];d=-d
  t=A[c][c];d*=t
  for j in range(c+1,len(A)):
   v=A[j][c]/t
   for z in range(c+1,len(A)):A[j][z]-=v*A[c][z]
 return d
def gp(points,d):
 return all(det([[1]+list(points[k]) for k in J])!=0 for J in combinations(range(len(points)),d+1))
def radon(points,J):
 A=[[1]+list(points[j]) for j in J]
 cs=[(-1)**i*det(A[:i]+A[i+1:]) for i in range(len(J))]
 ck('Radon cofactor relation '+str(J),all(sum(cs[i]*A[i][k] for i in range(len(J)))==0 for k in range(len(A[0]))))
 if sum(c>0 for c in cs)==3 and sum(c<0 for c in cs)==3:
  return tuple(J[i] for i,c in enumerate(cs)if c>0),tuple(J[i] for i,c in enumerate(cs)if c<0)
 return None
# Full finite parameter inequalities, without huge logarithms or exponentiation.
n=1<<256;m=1<<320;p=F(1,1<<384);M=comb(n,3);c=F(1,645120);a=c*c/2
ck('n is required fourth power',n==(1<<64)**4)
ck('p and m exponents',p*p==F(1,n**3) and m**4==n**5)
ck('witness-size conditions',n>=12 and (1<<448)>=107520)
Wlo=F(comb(n,6),7)-m*M
ck('exact remaining witness bound',Wlo>=c*n**6)
mu=Wlo*p*p;den=F(M*M,2)*p*p+M**3*p**3
ck('expectation and dependence envelope',mu>=c*n**3 and den<=1<<1152)
ck('exponential lower bound',a*(1<<384)>1<<343)
# ln(n)<256, ln(m+1)<321; the second follows m+1<2**321 and ln2<1.
logpref=256*(20*n+3*m)+321
ck('prefactor log envelope',logpref<1<<331)
ck('net exponent',a*(1<<384)-logpref>1<<342)
ck('robust probability below one eighth',1<<342>3)
lam=M*p;EB=F(comb(n,2)*comb(n-2,2))*p*p
ck('edge collision count mean',EB<=F(n,4))
ck('collision Markov bound',EB/m<=F(1,1<<66))
ck('triangle mean',lam>1<<379)
ck('triangle count failure bound',4/lam<F(1,1<<377))
ck('surviving triangle count',lam/2-m>n)
ck('joint failure less than one',F(1,8)+F(1,1<<66)+F(1,1<<377)<1)
# Seeded generic configurations; circuit signs and seven-set witness property.
rng=Random(23088066);configs=[]
for npts in [7,8,9]:
 configs.append([(t,t*t,t**3,t**4) for t in range(1,npts+1)])
 for _ in range(3):
  while True:
   P=[tuple(rng.randint(-11,11)for _ in range(4))for j in range(npts)]
   if gp(P,4):configs.append(P);break
for ci,P in enumerate(configs):
 ck('configuration general position '+str(ci),gp(P,4));W=[]
 for J in combinations(range(len(P)),6):
  q=radon(P,J)
  if q:W.append(q)
 ck('double-count witness lower bound '+str(ci),7*len(W)>=comb(len(P),6))
 for J in combinations(range(len(P)),7):
  ck('balanced witness on seven-set '+str((ci,J)),any(set(A+B)<=set(J) for A,B in W))
ck('nongeneric control rejected',not gp([(t,t*t,0,0)for t in range(7)],4))
# Exhaustively inspect every triangle subfamily on five labels: adaptive edge cleanup.
triples=list(combinations(range(5),3))
for bits in range(1<<len(triples)):
 H=[t for j,t in enumerate(triples)if bits>>j&1]
 bad=[(x,y)for x,y in combinations(H,2)if len(set(x)&set(y))==2]
 deleted={min(x,y)for x,y in bad};remain=[t for t in H if t not in deleted]
 ck('exhaustive cleanup '+str(bits),len(deleted)<=len(bad) and all(len(set(x)&set(y))<=1 for x,y in combinations(remain,2)) and len(remain)>=len(H)-len(bad))
# LP vertices certify exact intersections of closed triangles. Compare every pair.
def intersection_vertices(P,Q):
 # Six barycentric variables, two normalization rows and three equality rows.
 mat=[[F(x[k])for x in P]+[-F(x[k])for x in Q]+[F(0)]for k in range(3)]
 mat += [[F(1)]*3+[F(0)]*3+[F(1)],[F(0)]*3+[F(1)]*3+[F(1)]]
 R,pivs=rref(mat)
 if 6 in pivs:return []
 rows=[r for r in R if any(r[:6])];rank=len(rows);out=[]
 for S in combinations(range(6),rank):
  A=[[r[j]for j in S]+[r[6]]for r in rows];B,piv=rref(A)
  if piv!=list(range(rank)):continue
  vals=[r[-1]for r in B]
  if all(v>=0 for v in vals):
   allvals=[F(0)]*6
   for j,v in zip(S,vals):allvals[j]=v
   out.append(allvals)
 return out
def subdivision(H,eps):
 verts=sorted(set(sum((list(t)for t in H),[])));coords={}
 for j,v in enumerate(verts):t=j+1;coords[('v',v)]=(F(t),F(t*t),F(t**3))
 faces=[]
 for j,T in enumerate(H):
  t=len(verts)+j+1;f=('f',j);coords[f]=(F(t),F(t*t),F(t**3))
  for i,k in combinations(T,2):
   e=('e',min(i,k),max(i,k));u=coords['v',i];v=coords['v',k];z=coords[f]
   coords[e]=tuple(z[a]+eps*(u[a]+v[a]-2*z[a])for a in range(3))
  for i in T:
   for k in T:
    if i!=k:faces.append((f,('v',i),('e',min(i,k),max(i,k))))
 return coords,faces
families={
 'single':[(0,1,2)],
 'disjoint':[(0,1,2),(3,4,5)],
 'shared_vertex':[(0,1,2),(0,3,4)],
 'incidence_cycle':[(0,1,2),(2,3,4),(4,5,0)],
 'fano_plane':[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
}
geometry=[]
for name,H in families.items():
 ck(name+' is linear',all(len(set(A)&set(B))<=1 for A,B in combinations(H,2)))
 coords,faces=subdivision(H,F(1,1<<50))
 ck(name+' distinct subdivision vertices',len(set(coords.values()))==len(coords))
 for A in faces:
  _,rank=rref([[1]+list(coords[k])for k in A]);ck(name+' nondegenerate '+str(A),len(rank)==3)
 pc=0
 for A,B in combinations(faces,2):
  sols=intersection_vertices([coords[v]for v in A],[coords[v]for v in B]);common=set(A)&set(B)
  ck(name+' correct triangle intersection '+str((A,B)),all(all(v==0 for k,v in zip(A+B,row)if k not in common)for row in sols) and (bool(sols)==bool(common)))
  pc+=1
 geometry.append(dict(family=name,triangles=len(faces),pairs=pc,epsilon='2^-50'))
coords,faces=subdivision([(0,1,2)],F(0))
ck('epsilon zero rejected by duplicate-vertex control',len(set(coords.values()))<len(coords))
ck('edge-sharing family rejected by linearity gate',len(set((0,1,2))&set((0,1,3)))==2)
# Negative controls for the exact intersection routine itself.
A=[(0,0,0),(2,0,0),(0,2,0)]
B=[(1,0,-1),(1,0,1),(1,2,0)]
ck('intersection engine detects transversal illegal crossing',bool(intersection_vertices(A,B)))
B=[(F(1,4),F(1,4),0),(F(1,2),F(1,4),0),(F(1,4),F(1,2),0)]
ck('intersection engine detects coplanar interior overlap',bool(intersection_vertices(A,B)))
B=[(10,0,0),(11,0,0),(10,1,0)]
ck('intersection engine rejects disjoint coplanar triangles',not intersection_vertices(A,B))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'count':len(checks),'geometry':geometry,'generic_configurations':len(configs),'cleanup_families_exhaustively_checked':1024,'checks':checks,'limits':'Finite exact controls do not establish the universal PL embedding, Janson theorem, order-type counting theorem, or explicit existence witness. Written proof and primary imports are separately reviewed.'}
Path(__file__).with_name('fresh-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='checks'},indent=2))
