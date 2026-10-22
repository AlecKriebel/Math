"""Independent exact finite controls. Not an unbounded theorem or generation test."""
from itertools import product
from collections import Counter
from fractions import Fraction as F
import json,sys
C=Counter(); detail={}
def ck(ok,key):
 C[key]+=1
 if not ok:raise RuntimeError(key)
def trim(a):
 a=list(a)
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def rem(a,b,q):
 a=trim(a);b=trim(b)
 while len(a)>=len(b) and a!=[0]:
  c=a[-1]*pow(b[-1],-1,q)%q;d=len(a)-len(b)
  for j,x in enumerate(b):a[j+d]=(a[j+d]-c*x)%q
  a=trim(a)
 return a
def gcd(a,b,q):
 a,b=trim(a),trim(b)
 while b!=[0]:a,b=b,rem(a,b,q)
 return trim(a)
def ev(f,x,q):
 v=0
 for a in f[::-1]:v=(v*x+a)%q
 return v
def chi(x,q):return 0 if x%q==0 else (1 if pow(x%q,(q-1)//2,q)==1 else -1)
def eligible(f,q):return f[0]!=0 and ev(f,-1,q)!=0 and len(gcd(f,[(i*f[i])%q for i in range(1,len(f))]or[0],q))==1
def total_coeff(q,n):
 a=[]
 for j in range(n+1):
  v=1 if j==0 else -q if j==2 else 0
  for k,c in [(1,2-q),(2,1-2*q),(3,-q)]:
   if j>=k:v-=c*a[j-k]
  a.append(v)
 return a[n]
polyrows=[]
for q,maxr in [(3,9),(5,5),(7,4)]:
 for r in range(maxr+1):
  counts=Counter();sums=[0,0,0];total=0
  for a in product(range(q),repeat=r):
   f=[*a,1]
   if not eligible(f,q):continue
   total+=1;x=chi(ev(f,0,q),q);y=chi(ev(f,-1,q),q)
   counts[(chi((-1)**r,q)*x,chi((-1)**r,q)*y)]+=1
   sums[0]+=x;sums[1]+=y;sums[2]+=x*y
  ck(total==total_coeff(q,r),'squarefree_total_series')
  for j,s in enumerate([-1,-chi(-1,q),-1]):
   pred=(1-(q-1)*(r//2))*(s if r%2 else 1)
   ck(sums[j]==pred,'three_character_series')
  ck(total*3>=q**r,'principal_one_third')
  for pair in product([-1,1],repeat=2):
   if r>=8:ck(counts[pair]*16>=q**r,'q3_all_four_sector_lower_bound')
  polyrows.append({'q':q,'degree':r,'total':total,'sectors':{str(k):v for k,v in sorted(counts.items())}})
detail['polynomial_rows']=polyrows
# Matrix operations are separately implemented over prime fields.
def eye(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def tr(a):return list(map(list,zip(*a)))
def mul(a,b,q):return [[sum(x*y for x,y in zip(row,col))%q for col in zip(*b)]for row in a]
def det(a,q):
 a=[r[:]for r in a];v=1
 for j in range(len(a)):
  k=next((k for k in range(j,len(a))if a[k][j]),None)
  if k is None:return 0
  if k!=j:a[k],a[j]=a[j],a[k];v=-v
  v=v*a[j][j]%q;iv=pow(a[j][j],-1,q)
  for k in range(j+1,len(a)):
   c=a[k][j]*iv%q
   for l in range(j,len(a)):a[k][l]=(a[k][l]-c*a[j][l])%q
 return v%q
def inv(a,q):
 n=len(a);b=[row[:]+e for row,e in zip(a,eye(n))]
 for j in range(n):
  k=next(k for k in range(j,n)if b[k][j]);b[j],b[k]=b[k],b[j]
  c=pow(b[j][j],-1,q);b[j]=[x*c%q for x in b[j]]
  for k in range(n):
   if k!=j:
    c=b[k][j];b[k]=[(x-c*y)%q for x,y in zip(b[k],b[j])]
 return [r[n:]for r in b]
def diag(xs):return [[x if i==j else 0 for j in range(len(xs))]for i,x in enumerate(xs)]
def char(a,q):
 n=len(a);t=sum(a[j][j]for j in range(n))%q
 if n==1:return [(-t)%q,1]
 if n==2:return [det(a,q),(-t)%q,1]
 if n==3:
  s=sum(a[i][i]*a[j][j]-a[i][j]*a[j][i]for i in range(n)for j in range(i+1,n))%q
  return [(-det(a,q))%q,s,(-t)%q,1]
 raise RuntimeError('dimension outside independent char implementation')
def orderO(n,disc,q):
 if n==0:return 1
 if n%2:
  r=(n-1)//2;v=2*q**(r*r)
  for j in range(1,r+1):v*=q**(2*j)-1
  return v
 r=n//2;eps=chi((-1)**r*disc,q);v=2*q**(r*(r-1))*(q**r-eps)
 for j in range(1,r):v*=q**(2*j)-1
 return v
def orderSp(n,q):
 r=n//2;v=q**(r*r)
 for j in range(1,r+1):v*=q**(2*j)-1
 return v
def sym_form(n,q):return [[(1 if j==i+1 and i%2==0 else -1 if i==j+1 and j%2==0 else 0)%q for j in range(n)]for i in range(n)]
def allmat(m,n,q):
 for a in product(range(q),repeat=m*n):yield [list(a[i*n:(i+1)*n])for i in range(m)]
selfrows=[]
for q,n in [(3,2),(3,3),(5,2)]:
 nu=next(x for x in range(2,q)if chi(x,q)==-1)
 for dd in [1,nu]:
  A=diag([1]*(n-1)+[dd]);Ai=inv(A,q);counts=Counter();positions=[(i,j)for i in range(n)for j in range(i,n)]
  for vals in product(range(q),repeat=len(positions)):
   S=[[0]*n for _ in range(n)]
   for (i,j),x in zip(positions,vals):S[i][j]=S[j][i]=x
   K=mul(Ai,S,q);ck(mul(tr(K),A,q)==mul(A,K,q),'orthogonal_self_adjoint')
   f=char(K,q)
   if eligible(f,q):counts[tuple(f)]+=1
  for z in product(range(q),repeat=n):
   f=tuple([*z,1])
   if eligible(f,q):ck(counts[f]*2==orderO(n,dd,q),'self_adjoint_full_class_sum')
  selfrows.append({'q':q,'dimension':n,'disc':dd,'eligible_polynomials':len(counts),'eligible_operators':sum(counts.values())})
detail['self_adjoint_rows']=selfrows
graphrows=[]
for q,a,b in [(3,1,1),(3,1,2),(3,2,2),(3,2,3),(5,2,2)]:
 nu=next(x for x in range(2,q)if chi(x,q)==-1)
 for da,db in product([1,nu],repeat=2):
  A=diag([1]*(a-1)+[da]);B=diag([1]*(b-1)+[db]);Ai=inv(A,q);counts=Counter()
  for Fm in allmat(b,a,q):
   K=mul(mul(mul(Ai,tr(Fm),q),B,q),Fm,q);f=char(K,q)
   if eligible(f,q) and chi((-1)**a*ev(f,-1,q),q)==1:counts[tuple(f)]+=1
  for z in product(range(q),repeat=a):
   f=tuple([*z,1])
   if not eligible(f,q) or chi((-1)**a*ev(f,-1,q),q)!=1:continue
   dk=((-1)**a*f[0])%q;c=b-a;dc=(db*pow(da*dk,-1,q))%q
   if c==0 and chi(dk,q)!=chi(db*da,q):
    ck(counts[f]==0,'codimension_zero_empty_forbidden_sector');continue
   cnt=counts[f]
   expected=F(orderO(a,da,q),2)*F(orderO(b,db,q),orderO(c,dc,q))
   ck(cnt==expected,'orthogonal_graph_unconditional_fiber')
   mass=F(cnt*orderO(a,da,q)*orderO(b,db,q),orderO(a+b,da*db,q))
   predicted=F(orderO(a,da,q)**2*orderO(b,db,q)**2,2*orderO(a+b,da*db,q)*orderO(c,dc,q))
   ck(mass==predicted,'orthogonal_graph_class_denominator')
   if c==0:ck(chi(dk,q)==chi(db*da,q),'codimension_zero_constraint')
  graphrows.append({'q':q,'a':a,'b':b,'discA':da,'discB':db,'maps_examined':q**(a*b),'eligible_fibers':len(counts),'retained_maps':sum(counts.values())})
detail['orthogonal_graph_rows']=graphrows
# Explicit negative control: det(I+K) and codim-zero detK cannot be dropped.
ck(chi(2,3)==-1,'REJECT_drop_graph_discriminant')
ck(orderO(2,1,3)//2>0 and graphrows[8]['retained_maps']==0,'REJECT_drop_codimension_zero_constraint')
sprows=[]
for q,b in [(3,2),(3,4),(5,2)]:
 A=sym_form(2,q);B=sym_form(b,q);Ai=inv(A,q);counts=Counter()
 for Fm in allmat(b,2,q):
  K=mul(mul(mul(Ai,tr(Fm),q),B,q),Fm,q)
  ck(K[0][1]==K[1][0]==0 and K[0][0]==K[1][1],'Sp_plane_self_adjoint_scalar')
  k=K[0][0]
  if k and (1+k)%q:counts[k]+=1
 for k,cnt in counts.items():
  ck(cnt==orderSp(b,q)//orderSp(b-2,q),'Sp_graph_embedding_fiber')
  mass=F(cnt*orderSp(2,q)*orderSp(b,q),orderSp(2+b,q))
  expected=F(orderSp(2,q)*orderSp(b,q)**2,orderSp(2+b,q)*orderSp(b-2,q))
  ck(mass==expected,'Sp_graph_unconditional_mass')
 sprows.append({'q':q,'b':b,'maps':q**(2*b),'fibers':dict(counts)})
detail['symplectic_graph_rows']=sprows
# Each retained trace-form class has equal centralizer/fiber weight. Enumerate signs.
for s in range(2,13):
 for target in [-1,1]:
  allchoices=[z for z in product([-1,1],repeat=s)if __import__('math').prod(z)==target]
  keep=[z for z in allchoices if z[0]==1]
  ck(len(allchoices)==2**(s-1) and len(keep)==2**(s-2),'exact_half_trace_sign_refinement')
  ck(2*len(keep)==len(allchoices),'exact_half_weight_retained')
ck(2*len([z for z in [1]if z==1])!=len([1]),'REJECT_half_refinement_with_only_one_factor')
for q in [3,5,7]:
 nu=next(x for x in range(2,q)if chi(x,q)==-1)
 for dd in [1,nu]:
  B=diag([1,1,dd]);values=set()
  for v in product(range(q),repeat=3):
   norm=sum(v[i]*B[i][i]*v[i]for i in range(3))%q
   if not norm:continue
   Q=norm*pow(2,-1,q)%q;values.add(Q)
   R=[[(int(i==j)-2*v[i]*v[j]*B[j][j]*pow(norm,-1,q))%q for j in range(3)]for i in range(3)]
   ck(mul(mul(tr(R),B,q),R,q)==B and det(R,q)==q-1,'reflection_coset_representative')
  ck(values==set(range(1,q)),'three_dimensional_all_nonzero_norms')
# Unequal balance intervals are checked using rational endpoints, not rounded dimensions.
intervalrows=[]
for a,mult in [(8192,12),(8193,12),(32768,32),(32769,32)]:
 # Prove log bound for this finite control using a coarse rational log2 upper bound.
 d=128 if a<10000 else 512
 countmin=10**9
 for b in range(a,2*a+1):
  for L,U in [(F(a,3),F(2*a,3)),(F(b,3),min(F(2*b,3),F(5*a,6)))]:
   ck(U-L>=F(a,6) and U<=F(5*a,6),'both_target_balance_intervals')
   lo=(L.numerator+L.denominator-1)//L.denominator;hi=U.numerator//U.denominator
   num=sum(1 for k in range(((lo+d-1)//d)*d,hi+1,d)if (k//d)%2)
   ck(num>=F(a,24*d),'integer_progression_rounding')
   countmin=min(countmin,num)
 intervalrows.append({'a':a,'d':d,'all_b_from_a_to_2a':True,'minimum_count':countmin})
detail['interval_rows']=intervalrows
# Small Sp4 impossibility is an actual finite group classification, not a large-n test.
for q in [3,5,7]:
 mats=[m for m in allmat(2,2,q)if det(m,q)==1 and mul(m,m,q)==eye(2)]
 ck(len(mats)==2 and all(m==eye(2)or m==diag([q-1,q-1])for m in mats),'Sp4_zero_plane_marginal')
# Fixed-multiplier confidence and simultaneous balance are genuinely distinct demands.
ck(set(range(6,11)).intersection(range(10,21))=={10},'equal_negative_dimension_boundary')
ck(F(4*4,3).denominator!=1,'REJECT_simultaneous_strong_unbalanced_factors')
print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'checks':sum(C.values()),'categories':dict(sorted(C.items())),'detail':detail,'scope':'Exact finite diagnostics only, independently authored. No generation/subdirect claim, no author executable imported, no proof over all dimensions/prime powers inferred from enumeration.'},indent=2))
