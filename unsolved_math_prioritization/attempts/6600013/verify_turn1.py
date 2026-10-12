from quadratic_rotation import language
from rational_linear import rank,matmul,eye,kron
from itertools import product
from math import prod,comb
import random,json
checks=0;graphs={};rng=random.Random(660001301)
def check(x):
 global checks
 assert x;checks+=1
for n in range(1,25):
 vertices=sorted(language(n));edges=sorted(language(n+1));index={w:i for i,w in enumerate(vertices)}
 check(len(vertices)==n+1);check(len(edges)==n+2)
 B=[[0]*len(edges) for _ in vertices]
 for j,w in enumerate(edges):
  check(w[:-1] in index and w[1:] in index);B[index[w[:-1]]][j]-=1;B[index[w[1:]]][j]+=1
 r=rank(B);check(r==len(vertices)-1);check(len(edges)-r==2);graphs[n]=(B,len(vertices),len(edges))
product_complexes=0
for n,m in product(range(1,5),repeat=2):
 A,V,E=graphs[n];B,W,F=graphs[m]
 left=kron(A,eye(W));right=kron(eye(V),B);D1=[a+b for a,b in zip(left,right)]
 D2=[[-x for x in row] for row in kron(eye(E),B)]+kron(A,eye(F))
 check(all(not x for row in matmul(D1,D2) for x in row));r1=rank(D1);r2=rank(D2)
 check([V*W-r1,E*W+V*F-r1-r2,E*F-r2]==[1,4,4]);product_complexes+=1
# Sharp product and coefficient identities, as finite controls of the proven formulas.
for d in range(1,7):
 for n in range(1,25):
  check(prod([n+1]*d)==(n+1)**d)
  betti=[comb(d,k)*2**k for k in range(d+1)];check(sum(betti)==3**d)
for ranks in product(range(7),repeat=3):check(prod(r+1 for r in ranks)<=27*prod(max(1,r-1) for r in ranks))
# Products of linear maps: image rank never exceeds an intervening dimension.
for case in range(80):
 dims=[rng.randrange(1,8) for _ in range(5)];C=eye(dims[0]);bound=dims[0]
 for a,b in zip(dims,dims[1:]):
  M=[[rng.randrange(-2,3) for _ in range(a)] for _ in range(b)];C=matmul(M,C);bound=min(bound,b);check(rank(C)<=bound)
# A nilpotent system kills all stage classes; a mixed diagonal system retains just one.
J=[[0,1,0],[0,0,1],[0,0,0]];C=eye(3)
for k in range(1,5):C=matmul(J,C);check(rank(C)==max(0,3-k))
M=[[2,0,0],[0,0,1],[0,0,0]];C=eye(3)
for k in range(1,5):C=matmul(M,C);check(rank(C)==(2 if k==1 else 1))
print(json.dumps(dict(assertions=checks,full_sturmian_languages=25,product_chain_complexes=product_complexes,scope='Exact finite language, graph, Kunneth and persistence controls for the proved Cartesian-product subclass; arbitrary higher-dimensional target unresolved.'),indent=2,sort_keys=True))
