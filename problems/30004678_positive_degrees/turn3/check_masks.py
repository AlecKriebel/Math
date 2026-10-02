import itertools,json
checks=0
def ck(x):
 global checks
 checks+=1;assert x
for q in range(2,21):
 code=lambda a:(1<<a)-1
 swap=lambda a:1-a if a<2 else a
 for s,t in [(0,1),(1,0)]:
  a=swap(0) if t else 0;b=swap(1) if t else 1
  gs=code(swap(a) if t else a);gt=code(swap(b) if t else b)
  fs=code(swap(a) if s else a);ft=code(swap(b) if s else b)
  ck(gs&gt==gs);ck(fs&1==1 and ft&1==0)
 for a in range(q):ck(swap(swap(a))==a)
for n in range(1,4):
 N=1<<n
 for f in itertools.product(range(2),repeat=N):
  if not all(f[x]<=f[y] for x in range(N) for y in range(N) if x&y==x):continue
  for bit in range(n):
   for x in range(N):
    if x&(1<<bit):continue
    ck(not(f[x]==1 and f[x|(1<<bit)]==0))
for bits in itertools.product(range(2),repeat=10):
 for mask in [0,1,0b10101,0b11111]:
  source=[bits[i]^((mask>>i)&1) for i in range(10)]
  target=[1-source[i] if i in (0,4,9) else source[i] for i in range(10)]
  result=[target[i] if i in (0,4,9) else source[i] for i in range(10)]
  ck(result==target)
def valuation(n):
 k=0
 while n%2==0:k+=1;n//=2
 return k
for k in range(10):
 for j in range(10):
  if j==k:continue
  for t in range(10):
   n=(1<<k)*(2*t+1)-1;ck(valuation(n+1)==k);ck(valuation(n+1)!=j)
print(json.dumps({'assertions':checks,'alphabet_sizes':list(range(2,21)),'finite_exception_profiles':4096,'scope':'finite witnesses only; genericity proves infinite nonreductions'},indent=2))
