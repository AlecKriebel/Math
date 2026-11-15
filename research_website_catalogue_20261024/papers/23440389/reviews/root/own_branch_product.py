# Independent root branch-product count derived from the paper only.
# No supplied verification or prior/current scientific opinion is imported.
from itertools import product
import json

def count(A,B):
 def branch(c,b):
  total=0
  for a in A:
   if abs(a-b)<2 or a==c:continue
   pendant=sum(abs(t-b)>=2 and t!=c and t!=a for t in A)
   m=sum(abs(t-a)>=2 and t!=b for t in B)
   total+=pendant*m*(m-1)
  return total
 return sum(branch(c,b)*branch(c,d) for c,b,d in product(A,repeat=3)
            if abs(c-b)>=2 and abs(c-d)>=2 and b!=d)

v=['a','b','c','d','e','a1','a2','b1','d1','e1','e2']
edges=[('a','b'),('b','c'),('c','d'),('d','e'),('a','a1'),('a','a2'),('b','b1'),('d','d1'),('e','e1'),('e','e2')]
g={x:set() for x in v}
for a,b in edges:g[a].add(b);g[b].add(a)
w=dict(zip(v,[1,5,3,1,5,3,4,2,4,2,3]))
D={}
for a in v:
 dist={a:0};queue=[a]
 for x in queue:
  for y in g[x]:
   if y not in dist:dist[y]=dist[x]+1;queue.append(y)
 D[a]=dist
assert len(v)==11 and len(edges)==10 and all(len(d)==11 for d in D.values())
assert max(map(len,g.values()))==3 and min(max(d.values()) for d in D.values())==3 and max(max(d.values()) for d in D.values())==6
for a,b in product(v,repeat=2):
 assert D[a][b]!=1 or abs(w[a]-w[b])>=2
 assert D[a][b]!=2 or w[a]!=w[b]
counts={str(k):count(list(range(1,k+1)),list(range(1,k+1))) for k in [4,5,6]}
bad=count([1,2,3,4,5],[1,3,4,5,6])
assert counts=={'4':0,'5':8,'6':6336} and bad==0
print(json.dumps({'method':'Exact center-rooted branch-product formula; same construction input, independently derived mechanism, not independent discovery','common_palette_counts':counts,'bad_five_list_count':bad,'ordinary_witness_valid':True,'vertices':11,'edges':10,'maximum_degree':3,'radius':3,'diameter':6,'scope':'Fixed original instance only; universal list bound and arbitrary path-family proved analytically','foreign_or_supplied_code_imported':False},indent=2))
