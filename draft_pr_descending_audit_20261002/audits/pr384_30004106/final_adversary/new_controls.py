"""Independent finite adversarial controls. No author or old-review imports.
Finite calculations are controls, not proofs of the universal symmetry question.
"""
from itertools import product
from fractions import Fraction as F
from math import comb
from collections import defaultdict
import json
checks=defaultdict(int)
def ck(v,f):
 assert v,f
 checks[f]+=1
# Inseparable residue field stress. Over k=F2(t), A=[[0,t],[1,0]] has
# A^2=tI and irreducible minimal polynomial X^2-t. Over K=k(s), t=s^2,
# (A-sI)^2=0 with nonzero rank-one matrix. This is not a separable split.
# Polynomial arithmetic F2[s] implemented as bit sets, no numerical sampling.
def pm(a,b):
 out=0
 while b:
  if b&1:out^=a
  a<<=1;b>>=1
 return out
def matmul(a,b):
 return tuple(pm(a[2*i],b[j])^pm(a[2*i+1],b[j+2]) for i in range(2) for j in range(2))
s=2;t=4;A=(0,t,1,0);I=(1,0,0,1);N=(s,t,1,s)
ck(matmul(A,A)==(t,0,0,t),'inseparable')
ck(matmul(N,N)==(0,0,0,0) and N!=(0,0,0,0),'inseparable')
ck(pm(N[0],N[3])^pm(N[1],N[2])==0,'inseparable')
# Restriction-extension is two copies as k-vector module; test complex signed
# coefficient norm equality in a disjoint decomposition pattern with multiplicity.
for a,b in product(range(-8,9),repeat=2):
 ck(2*(abs(F(a,3))+abs(F(b,5)))==abs(2*F(a,3))+abs(2*F(b,5)),'scalar_norm')
# Compactness failure control: every finite initial collection x>=1/n (n>=1)
# is not the right model. The actual gap is varying defect epsilon. For cyclic
# order 2^j with selfadjoint incorrectly-fixed star, roots exp(2pi i/2^j)
# can be nonreal while tending to real. Keep epsilon fixed in any FIP claim.
for j in range(1,60):
 ck(F(1,2**j)>0 and F(1,2**j)<F(1,2**(j-1)),'fixed_gap_logic')
# Actual finite truncation feasibility boundary in polynomially weighted Z.
# Rational evaluations z>1 satisfy all product relations and disk bounds on
# a finite coordinate interval; their defects shrink and do not make a global
# weighted character. This catches replacing fixed-epsilon FIP by prefix tests.
for limit in range(2,34):
 z=F(limit*limit+1,limit*limit)
 vals={n:z**n for n in range(-limit,limit+1)}
 for n,v in vals.items():ck(abs(v)<=1+abs(n),'finite_feasibility_gap')
 for a,b in product(vals,repeat=2):
  if a+b in vals:ck(vals[a]*vals[b]==vals[a+b],'finite_feasibility_gap')
 ck(vals[-1]!=vals[1] and abs(vals[-1]-vals[1])<F(3,limit*limit),'finite_feasibility_gap')
 if limit>=4:ck(abs(vals[-1]-vals[1])<F(1,4),'finite_feasibility_gap')
# Independent quaternion signed-unit multiplication: 1,I,J,K with signs.
units=[(sg,b) for sg in (1,-1) for b in range(4)];uid={g:i for i,g in enumerate(units)}
def qm(g,h):
 a,i=g;b,j=h
 if i==0:return a*b,j
 if j==0:return a*b,i
 if i==j:return -a*b,0
 positive={(1,2):3,(2,3):1,(3,1):2}
 if (i,j) in positive:return a*b,positive[i,j]
 return -a*b,positive[j,i]
for a,b,c in product(units,repeat=3):ck(qm(qm(a,b),c)==qm(a,qm(b,c)),'quaternion_group')
one=1<<uid[1,0];aa=1<<uid[1,1];bb=1<<uid[1,2];kk=1<<uid[1,3];kp=1<<uid[-1,3];norm=255
# columns encoded as bit-vectors; convolution computed by an independent group table.
def ringmul(a,b):
 out=0
 for i,g in enumerate(units):
  if a>>i&1:
   for j,h in enumerate(units):
    if b>>j&1:out^=1<<uid[qm(g,h)]
 return out
def expand(coeff):
 rows=len(coeff);cols=len(coeff[0]);out=[]
 for j in range(cols):
  for g in range(8):
   out.append(sum(ringmul(coeff[i][j],1<<g)<<(8*i) for i in range(rows)))
 return out,8*rows
def rk(cols):
 piv={}
 for v in cols:
  while v:
   b=v.bit_length()-1
   if b in piv:v^=piv[b]
   else:piv[b]=v;break
 return len(piv)
def apply(cols,v):
 z=0
 for j,c in enumerate(cols):
  if v>>j&1:z^=c
 return z
maps=[[[aa^one,bb^one]],[[bb^one,kp^one],[kk^one,aa^one]],[[aa^one],[bb^one]],[[norm]]]
expanded=[expand(d) for d in maps]
for j in range(4):
 a,_=expanded[j];b,_=expanded[(j+1)%4]
 ck(all(apply(a,c)==0 for c in b),'quaternion_exactness')
ck([rk(a) for a,_ in expanded]==[7,9,7,1],'quaternion_exactness')
# Restrict actual syzygy images to central C2 using right multiplication by -1.
z=units.index((-1,0));central=[]
for a,dim in expanded[:3]:
 blocks=dim//8
 cols=[]
 for j in range(dim):
  block,g=divmod(j,8);gg=uid[qm(units[g],units[z])]
  cols.append((1<<(8*block+gg))^(1<<j))
 rr=rk([apply(cols,c) for c in a]);dd=rk(a)
 ck(dd-2*rr==1,'quaternion_actual_restriction');central.append({'dim':dd,'C2_free_summands':rr,'C2_trivial_summands':dd-2*rr})
ck(central[0]['C2_free_summands']+central[2]['C2_free_summands']==6,'quaternion_actual_restriction')
# Exact Fourier control over Q(i), complete idempotents in C[C4].
def ca(a,b):return a[0]+b[0],a[1]+b[1]
def cm(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def cp(z,n):
 y=(F(1),F(0))
 for _ in range(n%4):y=cm(y,z)
 return y
def cv(a,b):
 c=[(F(0),F(0)) for _ in range(4)]
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[(i+j)%4]=ca(c[(i+j)%4],cm(x,y))
 return c
roots=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
ids=[[(F(1,4)*cp(z,-j)[0],F(1,4)*cp(z,-j)[1]) for j in range(4)] for z in roots]
h=[(F(-2),0),(F(1),0),(0,0),(F(1),0)]
for i,j in product(range(4),repeat=2):ck(cv(ids[i],ids[j])==(ids[i] if i==j else [(0,0)]*4),'ambient_fourier')
for i,e in enumerate(ids):
 lam=[0,-2,-4,-2][i]
 ck(cv(h,e)==[(lam*x,lam*y) for x,y in e] and any(x or y for x,y in e),'ambient_fourier')
# Noncyclic abstract ring controls, determinant of multiplication by c+s.
def det(M):
 M=[[F(x) for x in r] for r in M];v=F(1)
 for j in range(len(M)):
  z=next((i for i in range(j,len(M)) if M[i][j]),None)
  if z is None:return 0
  if z!=j:M[j],M[z]=M[z],M[j];v=-v
  pivot=M[j][j];v*=pivot
  for i in range(j+1,len(M)):
   t=M[i][j]/pivot
   for k in range(j,len(M)):M[i][k]-=t*M[j][k]
 return v
abstract=[]
for orders in [(3,2),(4,2),(3,3),(3,2,2)]:
 H=list(product(*(range(n) for n in orders)));m=len(H);ix={g:i+1 for i,g in enumerate(H)}
 def gm(g,h):return tuple((a+b)%n for a,b,n in zip(g,h,orders))
 for q in (2,3,7):
  c=q-1;d=c+m;size=m+1
  def bas(i,j):
   out=[0]*size
   if i==0:out[j]=1
   elif j==0:out[i]=1
   else:
    out=[0]+[1]*m;out[ix[gm(H[i-1],H[j-1])]]+=c
   return out
  def mv(v,j):
   out=[0]*size
   for i,a in enumerate(v):
    for k,b in enumerate(bas(i,j)):out[k]+=a*b
   return out
  for i,j,k in product(range(size),repeat=3):ck(mv(bas(i,j),k)==mv(bas(j,k),i),'abstract_noncyclic')
  for i,j in product(range(size),repeat=2):
   v=bas(i,j)
   ck(v[0]==int(i==j==0) and all(a>=0 for a in v),'abstract_axioms')
   ck(v[0]+d*sum(v[1:])==(1 if i==0 else d)*(1 if j==0 else d),'abstract_axioms')
  for i in range(1,size):ck(mv(bas(i,i),i)[i]>=2,'abstract_axioms')
  ck(det([[c*int(i==j)+1 for j in range(m)] for i in range(m)])==d*c**(m-1),'abstract_semisimple')
  abstract.append({'orders':orders,'q':q,'rank':size})
# Actual syzygy restriction functor: on nontrivial H<=C2^3, T_syzygy(H)=Z
# for dim H>=2, trivial for lines. Restrictions between ranks>=2 are identity;
# restriction to lines is zero. Dimension weights come from minimal Betti ranks.
vectors=list(range(8));subs=[]
for mask in range(256):
 S=frozenset(x for x in vectors if mask>>x&1)
 if 0 in S and all(x^y in S for x in S for y in S):subs.append(S)
subs.sort(key=lambda H:(len(H),sorted(H)));ix={H:i for i,H in enumerate(subs)};mu={}
for j,H in enumerate(subs):
 for i,L in enumerate(subs):
  if L<=H:mu[i,j]=1 if i==j else -sum(mu[i,k] for k,K in enumerate(subs[:j]) if L<=K<=H)
def rankH(j):return len(subs[j]).bit_length()-1
def res(i,j,t):return 0 if rankH(i)==1 else t
def w(j,t):
 r=rankH(j)
 if r==1:return 1
 dd=1
 for n in range(abs(t)):dd=2**r*comb(n+r-1,r-1)-dd
 return dd
def clean(a):return {k:v for k,v in a.items() if v}
def add(a,b):
 c=defaultdict(F,a)
 for k,v in b.items():c[k]+=v
 return clean(c)
def times(a,b):
 out=defaultdict(F)
 for (i,t),c in a.items():
  for (j,u),d in b.items():
   l=ix[subs[i]&subs[j]]
   if l:out[l,res(l,i,t)+res(l,j,u)]+=c*d
 return clean(out)
pp={j:{(i,0):F(mu[i,j]) for i in range(1,j+1) if (i,j) in mu and mu[i,j]} for j in range(1,len(subs))}
for j in pp:
 for n in range(-5,6):
  if rankH(j)==1 and n:continue
  for m in range(-5,6):
   if rankH(j)==1 and m:continue
   ck(w(j,n+m)<=w(j,n)*w(j,m),'actual_syzygy_weight')
   image=times(pp[j],{(j,n):F(1)})
   other=times(pp[j],{(j,m):F(1)})
   ck(times(image,other)==times(pp[j],{(j,n+m):F(1)}),'nonconstant_restriction_blocks')
 # Signed rational coefficient strings exercise lower-level restriction collisions.
 for shift in range(-6,7):
  f={(j,t):F(((t+shift)%7)-3,5) for t in range(-5,6) if rankH(j)>=2 or t==0}
  im=times(pp[j],f)
  inn=sum(abs(a)*w(h,t) for (h,t),a in f.items());out=sum(abs(a)*w(h,t) for (h,t),a in im.items())
  C=sum(abs(a) for a in pp[j].values())
  ck(inn<=out<=C*inn,'completed_weighted_norm_control')
  ck({t:a for (h,t),a in im.items() if h==j}=={t:a for (h,t),a in clean(f).items()},'completed_weighted_norm_control')
# F8 ordinary and shifted cyclic restrictions: the ordinary seven lines all act
# freely; a nonzero k-linear combination of augmentation operators can vanish.
def fm(a,b):
 out=0
 while b:
  if b&1:out^=a
  b>>=1;a<<=1
  if a&8:a^=11
 return out
for lam in range(1,8):ck(any(fm(lam,x)==1 for x in range(1,8)),'F8_ordinary_restrictions')
# x2+z*x1 acts as zJ+zJ=0, giving a shifted line with nonfree restriction.
ck(2^fm(2,1)==0,'F8_shifted_restriction')
# Explicit centralizer idempotents prove indecomposability without unit counting.
for a,b in product(range(8),repeat=2):
 square=(fm(a,a),fm(a,b)^fm(b,a))
 ck((square==(a,b))==((a,b) in [(0,0),(1,0)]),'F8_actual_indecomposable')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),'families':dict(checks),'quaternion_actual_C2_restrictions':central,'noncyclic_abstract_cases':abstract,'scope':'New finite controls; no author imports; no universal proof or novelty claim'},indent=2))
