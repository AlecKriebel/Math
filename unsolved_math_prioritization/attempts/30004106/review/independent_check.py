import itertools,json
checks=0
def ck(b):
 global checks
 assert b;checks+=1
# All based associativity and regular/dimension checks in small abstract rings.
for m in range(3,9):
 for q in range(2,6):
  c=q-1;d=c+m;N=m+1
  basis=[tuple(int(i==j) for i in range(N)) for j in range(N)]
  def mul(a,b):
   out=[0]*N
   for i,x in enumerate(a):
    for j,y in enumerate(b):
     if not x*y:continue
     if not i:out[j]+=x*y
     elif not j:out[i]+=x*y
     else:
      out[1+(i+j-2)%m]+=c*x*y
      for k in range(1,N):out[k]+=x*y
   return tuple(out)
  dim=lambda a:a[0]+d*sum(a[1:])
  rho=(0,)+(1,)*m
  for a,b in itertools.product(basis,repeat=2):
   ck(dim(mul(a,b))==dim(a)*dim(b));ck(mul(a,b)==mul(b,a))
   for z in basis:ck(mul(mul(a,b),z)==mul(a,mul(b,z)))
  for a in basis:ck(mul(a,rho)==tuple(dim(a)*v for v in rho))
# Subspace lattice F2^3, generated directly by XOR-closed subsets.
subs=[]
for mask in range(256):
 S=frozenset(i for i in range(8) if mask>>i&1)
 if 0 in S and all(a^b in S for a in S for b in S):subs.append(S)
subs.sort(key=lambda s:(len(s),tuple(sorted(s))))
mu={}
for H in subs:
 for L in subs:
  if L<=H:
   mu[L,H]=1 if L==H else -sum(mu[L,K] for K in subs if L<=K<H)
for J,H in itertools.product(subs[1:],repeat=2):
 ck(sum(mu[L,H] for L in subs if J<=L<=H)==int(J==H))
for H,K in itertools.product(subs,repeat=2):
 HK={a^b for a in H for b in K}
 ck((8//len(HK))*(8//len(H&K))==(8//len(H))*(8//len(K)))
# F8 arithmetic, centralizer of J and order-two restrictions.
def fmul(a,b):
 out=0
 while b:
  if b&1:out^=a
  b>>=1;a<<=1
  if a&8:a^=11
 return out
def mm(A,B):
 return tuple(fmul(A[2*i],B[j])^fmul(A[2*i+1],B[2+j]) for i in range(2) for j in range(2))
J=(0,1,0,0);I=(1,0,0,1)
for a,b,c,d in itertools.product(range(8),repeat=4):
 M=(a,b,c,d);ck((mm(M,J)==mm(J,M))==(c==0 and a==d))
for lam in range(1,8):
 M=(1,lam,0,1);ck(mm(M,M)==I);ck(M!=I)
print(json.dumps({'result':'PASS','assertions':checks,'scope':'Independent bounded controls; no author imports'},indent=2))
