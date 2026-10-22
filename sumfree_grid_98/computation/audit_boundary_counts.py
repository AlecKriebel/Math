"""Independent convolution counts, without inclusion-exclusion binomial formulas."""
import json
from isolated_completion import calculate
from boundary_completion import count,best

def ranks(d,n):
 c=[1]
 for _ in range(d):
  out=[0]*(len(c)+n)
  for s,a in enumerate(c):
   for x in range(1,n+1):out[s+x]+=a
  c=out
 return c

def get(c,s):return c[s] if 0<=s<len(c) else 0
results=[]
for d,n in [(3,11),(4,5),(5,4),(6,3),(3,15),(3,20),(3,29),(3,30),(3,50),(3,100),(4,11),(5,9),(6,8)]:
 c=ranks(d,n);lower=ranks(d,n-1);small=ranks(d,n-2)
 iso=[get(c,s)-get(lower,s)-get(lower,s-d)+get(small,s-d) for s in range(d*n+1)]
 values=[]
 for t in range(1,d*n+1):
  plain=sum(c[t:2*t]);isolated=plain+sum(iso[:t])+sum(iso[2*t:])
  boundary=plain+sum(get(c,s)-get(lower,s) for s in range(t))+sum(get(c,s)-get(lower,s-d) for s in range(2*t,d*n+1))
  if t>=d and boundary!=count(d,n,t):raise ValueError('B formula mismatch')
  values.append((plain,isolated,boundary,t))
 pb=max(v[0] for v in values);ib=max(v[1] for v in values);bb=max(v[2] for v in values)
 if ib!=calculate(d,n)['completed_best']['completed'] or pb!=calculate(d,n)['plain_best']['slice'] or bb!=best(d,n)['size']:raise ValueError('maximum mismatch')
 results.append(dict(d=d,n=n,plain_best=pb,isolated_best=ib,boundary_best=bb))
print(json.dumps(results,indent=2))
