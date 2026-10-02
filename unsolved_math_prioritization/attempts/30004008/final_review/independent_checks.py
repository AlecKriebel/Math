import itertools,json
count=0;cases=0
# All root-category assignments up to eight colors, collapsed to counts.
def comps(n,k):
 if k==1:yield (n,);return
 for a in range(n+1):
  for b in comps(n-a,k-1):yield (a,)+b
def matching(slots,roots,avail):
 match={}
 def aug(j,seen):
  for c in avail:
   if roots[c]==j or c in seen:continue
   seen.add(c)
   if c not in match or aug(match[c],seen):match[c]=j;return True
  return False
 return all(aug(j,set()) for j in slots)
for q in range(0,9):
 for k in range(0,min(3,q)+1):
  for A in range(k,q+1):
   if k==0:
    sizes=[()] if A==0 else []
   else:sizes=[a for a in comps(A,k) if min(a)>0]
   for a in sizes:
    d=q-A;slots=[j for j in range(k) for _ in range(a[j])]
    for c in comps(q,k+1):
     roots=[j for j in range(k+1) for _ in range(c[j])]
     L=[max(0,c[j]-A+a[j]) for j in range(k)]
     exists=False
     for jt in itertools.combinations(range(q),d):
      J=set(jt);avail=set(range(q))-J
      quota=all(sum(roots[t]==j for t in J)>=L[j] for j in range(k))
      actual=matching(slots,roots,avail)
      assert actual==quota;count+=1;exists|=actual
     assert exists==(sum(L)<=d);count+=1
     assert exists==all(a[j]+c[j]<=q for j in range(k));count+=1;cases+=1
# Exhaust side-count pigeonhole and all-root polynomial obstruction exactly.
for a in range(1,31):
 for b in range(1,31):
  for c in comps(a+b,3):assert c[1]<=b or c[2]<=a;count+=1
z=((2,1),(1,1),(-2,1),(-1,1))
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
v=[mul(z[0],z[1]),mul(z[1],z[3]),mul(z[2],z[3])]
assert tuple(map(sum,zip(*v)))==(0,0);count+=1
print(json.dumps({'assertions':count,'quota_count_vectors':cases,'status':'PASS'},sort_keys=True))
