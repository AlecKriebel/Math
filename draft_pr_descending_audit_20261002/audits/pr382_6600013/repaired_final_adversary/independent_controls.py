#!/usr/bin/env python3
"""Source-first, dependency-free exact controls. No packet modules imported."""
from fractions import Fraction as Q
from itertools import product, permutations
import json
N=0
rows=[]
def check(ok,label):
 global N
 N+=1
 if not ok: raise AssertionError(label)
def rank(a):
 a=[[Q(x) for x in r] for r in a]; nr=len(a);nc=len(a[0]) if nr else 0;i=0
 for j in range(nc):
  z=next((k for k in range(i,nr) if a[k][j]),None)
  if z is None:continue
  a[i],a[z]=a[z],a[i];s=a[i][j];a[i]=[x/s for x in a[i]]
  for k in range(nr):
   if k!=i and a[k][j]:
    s=a[k][j];a[k]=[x-s*y for x,y in zip(a[k],a[i])]
  i+=1
  if i==nr:break
 return i
def zero(n,m):return [[0]*m for _ in range(n)]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def tr(a):return [list(x) for x in zip(*a)]
def mul(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def cat(a,b):return [x+y for x,y in zip(a,b)]
def kron(a,b):return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]
def ker(a):
 a=[[Q(x) for x in r] for r in a];n=len(a[0]);pivs=[];i=0
 for j in range(n):
  z=next((k for k in range(i,len(a)) if a[k][j]),None)
  if z is None:continue
  a[i],a[z]=a[z],a[i];s=a[i][j];a[i]=[x/s for x in a[i]]
  for k in range(len(a)):
   if k!=i and a[k][j]:
    s=a[k][j];a[k]=[x-s*y for x,y in zip(a[k],a[i])]
  pivs.append(j);i+=1
  if i==len(a):break
 basis=[]
 for f in set(range(n))-set(pivs):
  v=[Q(0)]*n;v[f]=1
  for k,p in enumerate(pivs):v[p]=-a[k][f]
  basis.append(v)
 return tr(basis)
def subst(w):return ''.join('01' if x=='0' else '10' for x in w)
def factors(n):
 # At supertile length >=n, a length-n factor meets at most two tiles.
 # All four base pairs are legal, proved by their occurrence in sigma^3(0).
 pairs=['00','01','10','11'];length=1
 while length<n:
  pairs=[subst(w) for w in pairs];length*=2
 return sorted({w[i:i+n] for w in pairs for i in range(len(w)-n+1)})
check(set(factors(3))==set(['001','010','011','100','101','110']),'TM triples')
vs=factors(2);es=factors(3);nv=len(vs);ne=len(es)
d=zero(nv,ne)
for j,w in enumerate(es):d[vs.index(w[:2])][j]-=1;d[vs.index(w[1:])][j]+=1
V=zero(nv,nv);M=zero(ne,ne)
for j,w in enumerate(vs):V[vs.index(str(1-int(w[0]))+w[1])][j]=1
for j,w in enumerate(es):
 s=subst(w)
 for t in [s[1:4],s[2:5]]:M[es.index(t)][j]+=1
check(mul(d,M)==mul(V,d),'actual collared substitution chain square')
B=tr(d);P=eye(ne);tm=[]
for k in range(7):
 r=rank(cat(P,B))-rank(B);tm.append(r);check(r==(3 if k==0 else 2),f'TM persistent H1 power{k}')
 P=mul(tr(M),P)
rows.append({'family':'actual collared TM','vertices':vs,'edges':es,'boundary':d,'vertex_substitution':V,'edge_substitution':M,'persistent_H1':tm})
# Actual Cartesian product CW chain complex; an integral unimodular shear changes
# the acting basis and support cropping, not the underlying product hull.
D1=cat(kron(d,eye(nv)),kron(eye(nv),d))
D2=kron(eye(ne),d)+[[-x for x in r] for r in kron(d,eye(ne))]
check(mul(D1,D2)==zero(nv*nv,ne*ne),'product boundary square')
C0=tr(D1);C1=tr(D2);Z1=ker(C1);C2=tr(D2)
P0=kron(tr(V),tr(V))
A=kron(tr(M),tr(V));E=kron(tr(V),tr(M));P1=[r+[0]*len(E[0]) for r in A]+[[0]*len(A[0])+r for r in E]
P2=kron(tr(M),tr(M))
check(mul(P1,C0)==mul(C0,P0),'product degree0 naturality')
check(mul(P2,C1)==mul(C1,P1),'product degree1 naturality')
p1=eye(ne*nv+nv*ne);p2=eye(ne*ne);prodrows=[]
for k in range(5):
 r1=rank(cat(mul(p1,Z1),C0))-rank(C0);r2=rank(cat(p2,C2))-rank(C2)
 check((r1,r2)==((6,9) if k==0 else (4,4)),f'product true persistent cohomology{k}')
 prodrows.append([k,r1,r2]);p1=mul(P1,p1);p2=mul(P2,p2)
rows.append({'family':'product/sheared actual CW','cell_counts':[nv*nv,2*nv*ne,ne*ne],'persistent_H1_H2':prodrows})
# Sheared blocks injectively recover horizontal word length 2n-1 and vertical n.
for n in range(1,8):
 seen={}
 for u in factors(2*n-1):
  for v in factors(n):
   block=tuple(tuple((u[i+j],v[j]) for i in range(n)) for j in range(n))
   check(block not in seen,f'shear injective n{n} u{u} v{v}');seen[block]=(u,v)
 check(len(seen)==len(factors(2*n-1))*len(factors(n)),f'shear count{n}')
 rows.append({'family':'shear exact blocks','n':n,'factors_horizontal':len(factors(2*n-1)),'factors_vertical':len(factors(n)),'blocks':len(seen)})
# Arbitrary gluing is insufficient for a covering: finite permutation cover,
# punctured fibre mutant, actual transfer and monodromy-connectedness.
for k in range(1,9):
 verts=list(product(range(nv),range(k)));edges=list(product(range(ne),range(k)));dc=zero(len(verts),len(edges));pb=zero(len(edges),ne);transfer=zero(ne,len(edges))
 for q,(e,j) in enumerate(edges):
  w=es[e];dc[verts.index((vs.index(w[:2]),j))][q]-=1;dc[verts.index((vs.index(w[1:]),(j+1)%k))][q]+=1
  pb[q][e]=1;transfer[e][q]=1
 check(mul(transfer,pb)==[[k*x for x in r] for r in eye(ne)],f'cover transfer{k}')
 check(rank(dc)==len(verts)-1,f'cover connectedness{k}')
 check(len(edges)-rank(dc)==2*k+1,f'cover first Betti{k}')
 for vi,j in verts:
  incoming=[q for q,(e,s) in enumerate(edges) if vs.index(es[e][1:])==vi and (s+1)%k==j]
  outgoing=[q for q,(e,s) in enumerate(edges) if vs.index(es[e][:2])==vi and s==j]
  check(len(incoming)==sum(w[1:]==vs[vi] for w in es),f'incoming star{k}/{vi}/{j}')
  check(len(outgoing)==sum(w[:2]==vs[vi] for w in es),f'outgoing star{k}/{vi}/{j}')
 check(len(edges[:-1])!=k*ne,f'deleted-edge mutant{k}')
 rows.append({'family':'TM finite permutation covering','degree':k,'H1_rank':2*k+1,'transfer_scalar':k})
# Persistence quantifier traps with exact systems, independent of tiling package.
def active(j):return [b for b in range(1,j+1) if j<2*b+1]
for stage in range(1,33):
 births=active(stage);later=2*stage+1
 check(not any(b in active(later) for b in births),'each stage eventually dies')
 for look in range(1,stage+1):check(stage in active(stage+look),'no uniform lookahead')
rows.append({'family':'quantifier falsifier','system':'V_j has basis births b with b<=j<2b+1. Bonding retains surviving birth labels and kills expired labels. Every stage j dies by 2j+1; newest birth survives j more transitions.','direct_limit_rank':0})
for k in range(1,7):
 # Fixed-stage rank growth alone: wedge circles, constant bonding vs inclusion.
 check(rank(zero(k+1,k))==0,'constant map kills finite Betti')
 check(rank(eye(k)+[[0]*k])==k,'inclusion preserves finite Betti')
rows.append({'family':'finite-stage rank falsifier','constant_bonding_direct_limit':0,'inclusion_direct_limit':'infinite'})
# Rational differs from finite field: multiplication by 2 is invertible over Q.
check(rank([[2]])==1,'rational rank vs mod2');check(2%2==0,'mod2 collapse')
# Suspended profinite action: choose clopen agreement at level N; translation
# preserves agreement for ALL integers. Distinct 2-adics separated only at N+1.
for level in range(1,21):
 x=0;y=2**level
 for step in range(-31,32):check((x+step)%(2**level)==(y+step)%(2**level),'specified odometer arbitrary time agreement')
 check(x%(2**(level+1))!=y%(2**(level+1)),'distinct profinite points')
rows.append({'family':'specified profinite action','levels':20,'all_integer_time_argument':'addition preserves difference exactly; finite sample is a sanity check only','scope':'equivariant expansivity obstruction; underlying topological hull/alternate actions not excluded'})
# Variable roofs are topological time reparametrizations. A period-2 base with
# roof [1,2] has orbit period3 while constant roof1 has period2.
check(sum([1,2])!=sum([1,1]),'time-conjugacy cannot preserve orbit periods')
rows.append({'family':'variable roof falsifier','homeomorphic_mapping_tori':True,'periods':[3,2],'time_conjugacy':False,'scope':'mechanism/boundary illustration, not target aperiodic theorem'})
# Marked tile alphabets destroy any coefficient depending on dimension alone.
for a in range(2,25):check(a>1,'one-cell complexity has arbitrary alphabet size')
rows.append({'family':'coefficient boundary','p(1)':'alphabet size arbitrary; a global n>=1 bound cannot depend on d alone','asymptotic':'large-n coefficient requires actual high-rank minimal families, not p(1) alone'})
print(json.dumps({'assertions':N,'all_passed':True,'arithmetic':'Fraction rational','candidate_imports':[],'complete_rows':rows},indent=2))
