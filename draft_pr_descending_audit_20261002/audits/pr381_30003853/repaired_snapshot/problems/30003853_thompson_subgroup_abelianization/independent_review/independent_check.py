"""Independent bounded controls; no author imports or external dependencies."""
import itertools,json
n=0
def check(b):
 global n
 assert b
 n+=1
# Laurent kernel: use coefficient cumulative sums rather than differentiation code.
for m in range(1,9):
 for c in itertools.product(range(-2,3),repeat=5):
  if sum(c)!=0: continue
  q=[]; prev=0
  for a in c:
   prev-=a; q.append(prev)
  check(q[-1]==0)
  derivative=sum((i-2)*a for i,a in enumerate(c))
  check(sum(q)==derivative)
  check((sum(q)%m==0)==(derivative%m==0))
# Reconstruct nilpotent models, commutators, signed powers independently.
def mul(u,v,m):
 a,b,c=u; d,e,f=v
 return a+d,b+e,c+f+m*a*e
def inv(u,m):
 a,b,c=u; return -a,-b,-c+m*a*b
def power(u,k,m):
 a,b,c=u; return k*a,k*b,k*c+m*k*(k-1)*a*b//2
pts=list(itertools.product(range(-2,3),repeat=3))
for m in (2,3,7):
 for u in pts:
  check(mul(u,inv(u,m),m)==(0,0,0))
  for k in range(-4,5):
   check(mul(power(u,k,m),u,m)==power(u,k+1,m))
  for v in pts:
   w=mul(mul(mul(u,v,m),inv(u,m),m),inv(v,m),m)
   check(w==(0,0,m*(u[0]*v[1]-v[0]*u[1])))
   conjugate=mul(mul(inv(v,m),u,m),v,m)
   check((conjugate>(0,0,0))==(u>(0,0,0)))
# Nontrivial finite support cannot be forward invariant under a nonzero shift.
for size in range(1,6):
 for s in itertools.combinations(range(-5,6),size):
  for k in (-4,-1,1,3):
   check(not {i+k for i in s}.issubset(s))
print(json.dumps({'assertions':n,'result':'PASS','scope':'Bounded exact controls only; universal statements require the reviewed proofs.'},indent=2))
