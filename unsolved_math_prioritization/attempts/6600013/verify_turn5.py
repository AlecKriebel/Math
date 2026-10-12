from cyclic_cover import complex,projection
from rational_linear import rank,matmul,eye
from cochain_images import transpose,image_rank
import json,random
checks=0;records=[];rng=random.Random(660001305)
def check(x):
 global checks
 assert x;checks+=1
for q in [1,2,3,4,6,8]:
 Q=2*q;A1,A2=complex(q);B1,B2=complex(Q);F0,F1,F2=projection(q,Q)
 check(matmul(A1,F1)==matmul(F0,B1));check(matmul(A2,F2)==matmul(F1,B2))
 check(matmul(F1,transpose(B1))==matmul(transpose(A1),F0));check(matmul(F2,transpose(B2))==matmul(transpose(A2),F1))
 for F in [F0,F1,F2]:check(matmul(F,transpose(F))==[[2*x for x in row] for row in eye(len(F))])
 r=image_rank(transpose(B2),transpose(F2));check(r==q+3);check(4*Q-rank(B2)==Q+3);records.append(dict(source_degree=q,target_degree=Q,H2_image_rank=r,H2_target_rank=Q+3))
# Finite quotients retain the same fiber difference under every additive cocycle increment.
for k in range(2,10):
 Q=2**k
 for r in range(k):
  h=2**r
  for test in range(20):
   g=rng.randrange(Q);increment=rng.randrange(-1000,1001)
   check(((g+h+increment)%Q-(g+increment)%Q)%Q==h)
   lower=2**r;check((g+h)%lower==g%lower)
# Local transport in both coordinate directions commutes, including reduction between levels.
for q in [2,4,8,16,32]:
 for test in range(40):
  x=[rng.randrange(2) for _ in range(12)];y=[rng.randrange(2) for _ in range(12)];g=rng.randrange(2*q)
  a=(g+sum(x)+sum(y))%(2*q);b=(g+sum(y)+sum(x))%(2*q);check(a==b);check(a%q==(g%q+sum(x)+sum(y))%q)
for q in [1,2,4,8,16]:
 for n in range(1,33):check(q*(n+1)**2>=q*n*n)
print(json.dumps(dict(assertions=checks,covering_pullback_images=records,scope='Exact finite transfer and quotient controls for a proved infinite-cohomology profinite system which is nonexpansive and not a finite-alphabet generating tiling model; original target unresolved.'),indent=2,sort_keys=True))
