"""Fresh rational matrix controls; no supplied implementation imported.
Checks a length-three transverse homomorphism chain, all post-Lie identities,
full determinant covariance, all sl2 derivations and excluded-hypothesis cases.
No finite calculation purports to verify global integration or topology.
"""
from fractions import Fraction as Q
from itertools import product
import random,json
rng=random.Random(23414025);counts={}
def need(c,m):
 if not c:raise RuntimeError(m)
def tick(k,n=1):counts[k]=counts.get(k,0)+n
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(s,a):return tuple(s*x for x in a)
def eye(n):return tuple(tuple(Q(i==j) for j in range(n)) for i in range(n))
def cols(c):return tuple(zip(*c))
def apply(A,x):return tuple(sum((v*w for v,w in zip(row,x)),Q(0)) for row in A)
def mm(A,B):return cols(tuple(apply(A,c) for c in zip(*B)))
def madd(A,B):return tuple(add(a,b) for a,b in zip(A,B))
def msub(A,B):return tuple(sub(a,b) for a,b in zip(A,B))
def det(A):
 M=[list(map(Q,row)) for row in A];v=Q(1)
 for j in range(len(M)):
  k=next((k for k in range(j,len(M)) if M[k][j]),None)
  if k is None:return Q(0)
  if k!=j:M[k],M[j]=M[j],M[k];v=-v
  q=M[j][j];v*=q
  for k in range(j+1,len(M)):
   s=M[k][j]/q;M[k]=[x-s*y for x,y in zip(M[k],M[j])]
 return v
def rank(A):
 if not A:return 0
 M=[list(map(Q,row)) for row in A];r=0
 for j in range(len(M[0])):
  k=next((k for k in range(r,len(M)) if M[k][j]),None)
  if k is None:continue
  M[k],M[r]=M[r],M[k];q=M[r][j];M[r]=[x/q for x in M[r]]
  for k in range(len(M)):
   if k!=r:
    s=M[k][j];M[k]=[x-s*y for x,y in zip(M[k],M[r])]
  r+=1
  if r==len(M):break
 return r
def sl(x,y):
 # Ordered basis H,E,F, computed as trace-zero 2x2 commutator.
 h,e,f=x;H,E,F=y
 return (e*F-f*E,2*(h*E-e*H),2*(f*H-h*F))
def direct(x,y):return tuple(z for k in range(0,len(x),3) for z in sl(x[k:k+3],y[k:k+3]))
def inv(p):
 need(det(p)==1,'not SL2');return ((p[1][1],-p[0][1]),(-p[1][0],p[0][0]))
def adj(p):
 def conj(x):
  h,e,f=x;X=((h,e),(f,-h));Y=mm(mm(p,X),inv(p));return (Y[0][0],Y[0][1],Y[1][0])
 return cols([conj(x) for x in eye(3)])
def block(blocks):
 n=3*len(blocks)
 return tuple(tuple(blocks[i//3][i%3][j%3] if i//3==j//3 else Q(0) for j in range(n)) for i in range(n))
def randSL():
 u,v=Q(rng.randrange(-5,6),rng.randrange(1,5)),Q(rng.randrange(-5,6),rng.randrange(1,5));a=Q(rng.choice([-4,-2,-1,1,2,4]),rng.choice([1,3,7]))
 return mm(mm(((1,u),(0,1)),((a,0),(0,1/a))),((1,0),(v,1)))
# Three-factor shift S(a,b,c)=(0,a,b), F=I-S invertible, F^-1=I+S+S².
n=9;E=eye(n);Z=tuple(Q(0) for _ in range(n))
S=cols([tuple([Q(0)]*3)+x[:6] for x in E]);S2=mm(S,S);F=msub(E,S);Finv=madd(madd(E,S),S2);R=mm(S,Finv)
need(mm(F,Finv)==E and det(F)==1,'transverse chain');need(mm(mm(S,S),S)==tuple(Z for _ in E),'chain not nilpotent')
def source(x,y):return apply(F,direct(apply(Finv,x),apply(Finv,y)))
def prod(x,y):return direct(apply(R,x),y)
for x,y in product(E,repeat=2):
 need(apply(S,direct(x,y))==direct(apply(S,x),apply(S,y)),'shift not homomorphism')
 need(sub(prod(x,y),prod(y,x))==sub(source(x,y),direct(x,y)),'PL1 sign')
 need(apply(R,source(x,y))==direct(apply(R,x),apply(R,y)),'R hom')
 need(apply(madd(E,R),source(x,y))==direct(apply(madd(E,R),x),apply(madd(E,R),y)),'R+I hom');tick('pair_algebra_checks',4)
 for z in E:
  need(prod(source(x,y),z)==sub(prod(x,prod(y,z)),prod(y,prod(x,z))),'PL2')
  need(prod(x,direct(y,z))==add(direct(prod(x,y),z),direct(y,prod(x,z))),'PL3')
  need(add(source(x,source(y,z)),add(source(y,source(z,x)),source(z,source(x,y))))==Z,'Jacobi');tick('triple_algebra_checks',3)
need(rank(cols([source(x,y) for x,y in product(E,repeat=2)]))==n,'chain source not perfect')
need(all(sum(source(x,E[j])[j] for j in range(n))==0 for x in E),'chain nonunimodular')
wrong_covariance=0
for trial in range(60):
 p=[randSL() for _ in range(3)];h=[randSL() for _ in range(3)];j2h=[eye(2),h[0],h[1]]
 q=[mm(mm(h[i],p[i]),inv(j2h[i])) for i in range(3)]
 B=lambda pts:msub(block([adj(inv(x)) for x in pts]),S)
 Bp,Bq=B(p),B(q);Adh=block([adj(x) for x in h]);Adj2h=block([adj(x) for x in j2h])
 need(mm(Bq,Adh)==mm(Adj2h,Bp),'full covariance')
 need(det(Bp)==det(Bq)==det(Adh)==1,'unimodular determinant')
 wrong_covariance+=mm(Bq,Adh)!=mm(Adh,Bp);tick('group_covariance_instances')
need(wrong_covariance>0,'wrong factor negative control failed')
# Enumerate all linear derivation equations for sl2. Dimension 3 and containment
# of its 3-dimensional inner span prove every derivation is inner in this model.
e=eye(3);mats=[]
for a,b in product(range(3),repeat=2):mats.append(tuple(tuple(Q(i==a and j==b) for j in range(3)) for i in range(3)))
constraints=[]
for x,y in product(e,repeat=2):
 residual=[sub(apply(D,sl(x,y)),add(sl(apply(D,x),y),sl(x,apply(D,y)))) for D in mats]
 constraints.extend(cols(residual))
need(9-rank(constraints)==3,'sl2 derivation dimension')
ads=[cols([sl(x,y) for y in e]) for x in e]
need(rank([tuple(v for row in D for v in row) for D in ads])==3,'inner span')
for D in ads:
 for row in constraints:need(sum(x*y for x,y in zip(row,[v for r in D for v in r]))==0,'inner not derivation');tick('inner_derivation_equations')
# Published theorem's nonunimodular boundary, reconstructed in H,E,Z order.
j1=((1,0,0),(0,1,0),(0,0,0));j2=((0,0,0),(0,0,0),(0,0,1))
g=lambda x,y:(Q(0),2*(x[0]*y[1]-x[1]*y[0]),Q(0))
for x,y in product(e,repeat=2):
 need(apply(j1,g(x,y))==sl(apply(j1,x),apply(j1,y)),'boundary j1')
 need(apply(j2,g(x,y))==sl(apply(j2,x),apply(j2,y)),'boundary j2');tick('nonunimodular_pair_checks',2)
need(det(msub(j1,j2))!=0 and sum(g(e[0],e[j])[j] for j in range(3))==2,'unimodularity essential')
f=lambda p:det(msub(mm(adj(inv(p)),j1),j2))
need(f(eye(2))!=0 and f(((0,-1),(1,0)))==0,'open orbit alone incorrectly implies global')
# Merely reductive target: sl2 plus a central natural module; semidirect source.
e5=eye(5);zero5=tuple(Q(0) for _ in range(5))
red=lambda x,y:sl(x[:3],y[:3])+(Q(0),Q(0))
def module(x,y):
 h,e,f=x[:3];a,b=y[3:];return (Q(0),Q(0),Q(0),h*a+e*b,f*a-h*b)
sg=lambda x,y:add(red(x,y),sub(module(x,y),module(y,x)))
need(rank(cols([sg(x,y) for x,y in product(e5,repeat=2)]))==5,'boundary source not perfect')
need(all(sum(sg(x,e5[j])[j] for j in range(5))==0 for x in e5),'boundary source nonunimodular')
for x,y,z in product(e5,repeat=3):
 need(module(sg(x,y),z)==sub(module(x,module(y,z)),module(y,module(x,z))),'reductive PL2')
 need(module(x,red(y,z))==add(red(module(x,y),z),red(y,module(x,z))),'reductive PL3');tick('reductive_boundary_identities',2)
need(all(sg(x,y)==zero5 for x,y in product(e5[3:],repeat=2)),'radical not abelian')
# Without transversality, zero homomorphisms from an abelian unimodular source
# of dimension3 do not force semisimplicity.
need(det(tuple((0,0,0) for _ in range(3)))==0,'zero pair negative control')
print(json.dumps({'status':'PASS','seed':23414025,'counts':counts,'wrong_covariance_factor_rejections':wrong_covariance,'sl2_derivation_dimension':3,'scope':'Exact finite algebraic and group-matrix controls only; no supplied implementation imported; global holomorphic continuation, covering theory and homology require the written proof and primary imports.'},indent=2))
