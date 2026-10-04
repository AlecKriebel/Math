import itertools,json
from math import gcd
checks=0;graph_pairs=0;word_pairs=0
def test(c):
 global checks
 assert c;checks+=1
def theta(w,sigma):return tuple(sigma[a] for a in reversed(w))
def alternating(w,p,sigma):
 u=w[:p]
 if len(u)!=p:return False
 block=u+theta(u,sigma)
 return all(a==block[i%(2*p)] for i,a in enumerate(w))
def period(w,p):return all(w[i]==w[i+p] for i in range(len(w)-p))
for sigma in ((0,1),(1,0)):
 for L in range(1,12):
  for w in itertools.product(range(2),repeat=L):
   ps=[p for p in range(1,L+1) if alternating(w,p,sigma)]
   W=theta(w,sigma)+w
   for p in ps:test(period(W,2*p))
   for p in ps:
    for q in ps:
     d=gcd(p,q)
     if L>=p+q-d:
      test(period(W,2*d));test(alternating(w,d,sigma));word_pairs+=1
# Equality-closure certificate for all alphabets/involutions at each fixed pair.
for p in range(1,101):
 for q in range(1,p+1):
  d=gcd(p,q);L=p+q-d;parent=list(range(2*L))
  def root(x):
   while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
   return x
  def join(a,b):parent[root(a)]=root(b)
  def fold(i,k):
   r=i%(2*k)
   return (r,0) if r<k else (2*k-1-r,1)
  for k in (p,q):
   for i in range(k,L):
    j,e=fold(i,k);join(2*i,2*j+e);join(2*i+1,2*j+1-e)
  for i in range(d,L):
   j,e=fold(i,d);test(root(2*i)==root(2*j+e))
  graph_pairs+=1
w=(0,1,1);sigma=(0,1);test(alternating(w,2,sigma));test(alternating(w,3,sigma));test(not alternating(w,1,sigma))
print(json.dumps({'assertions':checks,'exhaustive_binary_period_pairs':word_pairs,'universal_constraint_graph_pairs':graph_pairs,'scope':'finite exact reflection, threshold and alphabet-involution controls; written proof uses classical Fine-Wilf for all periods'},indent=2))
