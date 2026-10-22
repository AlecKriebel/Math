"""Own exact field/Cayley and full-to-special conjugacy-law controls."""
from itertools import product,permutations
from collections import Counter
import json,sys
C=Counter();out={}
def ck(ok,key):
 C[key]+=1
 if not ok:raise RuntimeError(key)
def trim(a):
 a=list(a)
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def rem(a,b,p):
 a=trim(a);b=trim(b)
 while len(a)>=len(b) and a!=[0]:
  c=a[-1]*pow(b[-1],-1,p)%p;d=len(a)-len(b)
  for j,x in enumerate(b):a[j+d]=(a[j+d]-c*x)%p
  a=trim(a)
 return a
def irreducible4(f,p):
 return all(rem(f,[*x,1],p)!=[0]for d in [1,2]for x in product(range(p),repeat=d))
class Field4:
 def __init__(self,p):
  self.p=p;self.Q=p**4
  self.mod=next([*x,1]for x in product(range(p),repeat=4)if x[0]and irreducible4([*x,1],p))
  self.ds=[tuple((a//p**j)%p for j in range(4))for a in range(self.Q)]
 def enc(self,z):return sum((v%self.p)*self.p**i for i,v in enumerate(z))
 def add(self,a,b):return self.enc([x+y for x,y in zip(self.ds[a],self.ds[b])])
 def neg(self,a):return self.enc([-x for x in self.ds[a]])
 def sub(self,a,b):return self.add(a,self.neg(b))
 def mul(self,a,b):
  z=[0]*7
  for i,x in enumerate(self.ds[a]):
   for j,y in enumerate(self.ds[b]):z[i+j]=(z[i+j]+x*y)%self.p
  z=rem(z,self.mod,self.p);return self.enc(z)
 def pw(self,a,n):
  v=1
  while n:
   if n&1:v=self.mul(v,a)
   a=self.mul(a,a);n//=2
  return v
 def div(self,a,b):
  if not b:raise RuntimeError('division by zero')
  return self.mul(a,self.pw(b,self.Q-2))
 def degree(self,a):
  z=self.pw(a,self.p);j=1
  while z!=a:z=self.pw(z,self.p);j+=1
  return j
 def minpoly(self,a):
  roots=[];v=a
  while v not in roots:roots.append(v);v=self.pw(v,self.p)
  f=[1]
  for v in roots:
   z=[0]*(len(f)+1)
   for j,c in enumerate(f):z[j]=self.sub(z[j],self.mul(v,c));z[j+1]=self.add(z[j+1],c)
   f=z
  ck(all(x<self.p for x in f),'Cayley_minpoly_in_base_field')
  return tuple(f)
fields=[]
for p in [3,5]:
 E=Field4(p);fib=Counter();polys=set();maximal=0
 for lam in range(1,E.Q):
  if E.pw(lam,(E.Q-1)//2)==1:continue
  maximal+=1
  if E.degree(lam)!=4:continue
  kap=E.neg(E.pw(E.div(E.sub(lam,1),E.add(lam,1)),2))
  ck(kap not in [0,E.neg(1)] and E.degree(kap)==4,'Cayley_full_degree_and_exclusions')
  norm=E.pw(kap,(E.Q-1)//(p-1));norm1=E.pw(E.add(kap,1),(E.Q-1)//(p-1))
  ck(norm<p and norm1<p and pow(norm,(p-1)//2,p)==1 and pow(norm1,(p-1)//2,p)==p-1,'distinguished_norm_characters')
  ck(E.mul(E.pw(E.add(lam,1),2),E.add(kap,1))==E.mul(4%p,lam),'Cayley_one_plus_identity')
  fib[kap]+=1;polys.add(E.minpoly(kap))
 ck(maximal==(E.Q-1)//2,'maximal_2part_half_cyclic_group')
 ck(all(x==2 for x in fib.values()),'Cayley_exact_two_to_one')
 ck(len(polys)*32>=E.Q,'distinguished_factor_lower_bound_k4')
 fields.append({'q':p,'modulus':E.mod,'maximal_2part_lambdas':maximal,'kappa_count':len(fib),'irreducible_kappa_polynomials':len(polys)})
out['Cayley_fields']=fields
# Enumerate all GL3(3) and SL3(3) conjugators of the actual strong t=diag(-1,-1,1).
def det3(a,p):return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))%p
def inverse(a,p):
 b=[r[:]+[int(i==j)for j in range(3)]for i,r in enumerate(a)]
 for j in range(3):
  k=next(k for k in range(j,3)if b[k][j]);b[k],b[j]=b[j],b[k];s=pow(b[j][j],-1,p);b[j]=[v*s%p for v in b[j]]
  for k in range(3):
   if k!=j:
    s=b[k][j];b[k]=[(x-s*y)%p for x,y in zip(b[k],b[j])]
 return [r[3:]for r in b]
D=Counter();J=Counter()
for x in product(range(3),repeat=9):
 a=[list(x[j:j+3])for j in [0,3,6]];d=det3(a,3)
 if not d:continue
 ai=inverse(a,3)
 cl=tuple(sum(ai[i][k]*[-1,-1,1][k]*a[k][j]for k in range(3))%3 for i in range(3)for j in range(3))
 D[cl]+=1
 if d==1:J[cl]+=1
ck(sum(D.values())==11232 and sum(J.values())==5616,'GL_SL_full_group_sizes')
ck(D.keys()==J.keys() and len(D)==117,'GL_SL_identical_actual_t_class')
ck(set(D.values())=={96} and set(J.values())=={48},'GL_SL_uniform_fibers')
ck(all(D[k]==2*J[k]for k in D),'GL_SL_equal_conjugacy_laws')
ck(sum(J.values())<sum(D.values()),'REJECT_uniform_SL_as_near_uniform_GL')
out['GL_SL']={'field':3,'dimension':3,'GL_size':sum(D.values()),'SL_size':sum(J.values()),'class_size':len(D),'full_fiber':96,'special_fiber':48}
# F9=F3[i], i²=-1. This separately checks GU3(3)->SU3(3), not restriction-of-scalars dimension6.
def add(a,b):return (a%3+b%3)%3+3*((a//3+b//3)%3)
def neg(a):return ((-(a%3))%3)+3*((-(a//3))%3)
def sub(a,b):return add(a,neg(b))
def mult(a,b):
 x,y=a%3,a//3;z,w=b%3,b//3
 return (x*z-y*w)%3+3*((x*w+y*z)%3)
def conj(a):return a%3+3*((-(a//3))%3)
def sm(xs):
 v=0
 for x in xs:v=add(v,x)
 return v
def dot(v,w):return sm(mult(conj(a),b)for a,b in zip(v,w))
def cross(v,w):return [sub(mult(v[1],w[2]),mult(v[2],w[1])),sub(mult(v[2],w[0]),mult(v[0],w[2])),sub(mult(v[0],w[1]),mult(v[1],w[0]))]
def determinant(a):
 v=0
 for perm in permutations(range(3)):
  z=1
  for i,j in enumerate(perm):z=mult(z,a[i][j])
  odd=sum(perm[i]>perm[j]for i in range(3)for j in range(i+1,3))%2
  v=add(v,neg(z)if odd else z)
 return v
vectors=[v for v in product(range(9),repeat=3)if dot(v,v)==1];DU=Counter();JU=Counter()
for v in vectors:
 for w in vectors:
  if dot(v,w)!=0:continue
  u=cross([conj(x)for x in v],[conj(x)for x in w]);norm=dot(u,u)
  ck(norm in [1,2]and dot(v,u)==dot(w,u)==0,'unitary_orthogonal_complement_line')
  for scalar in range(1,9):
   if mult(mult(conj(scalar),scalar),norm)!=1:continue
   z=[mult(scalar,x)for x in u];a=[list(row)for row in zip(v,w,z)];d=determinant(a)
   ck(mult(conj(d),d)==1,'GU_determinant_norm_one')
   cl=tuple(sm(mult(mult(conj(a[k][i]),[2,2,1][k]),a[k][j])for k in range(3))for i in range(3)for j in range(3))
   DU[cl]+=1
   if d==1:JU[cl]+=1
ck(sum(DU.values())==24192 and sum(JU.values())==6048,'GU_SU_full_group_sizes')
ck(DU.keys()==JU.keys() and len(DU)==63,'GU_SU_identical_actual_t_class')
ck(set(DU.values())=={384}and set(JU.values())=={96},'GU_SU_uniform_fibers')
ck(all(DU[k]==4*JU[k]for k in DU),'GU_SU_equal_conjugacy_laws')
ck(len(vectors)==252,'GU_unit_vectors')
out['GU_SU']={'q':3,'natural_F9_dimension':3,'GU_size':sum(DU.values()),'SU_size':sum(JU.values()),'class_size':len(DU),'full_fiber':384,'special_fiber':96}
print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'checks':sum(C.values()),'categories':dict(sorted(C.items())),'detail':out,'scope':'Independent exact k4 field controls and full group conjugacy-law enumerations only. No large-dimension or generation claim; no author code imported.'},indent=2))
