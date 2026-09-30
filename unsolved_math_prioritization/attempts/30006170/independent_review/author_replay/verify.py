from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
import hashlib,json
checks=0
def ck(x):
 global checks
 assert x
 checks+=1
P=[[F(0),F(0),F(1,2),F(1,2)],[F(0),F(0),F(1,2),F(1,2)],[F(1,3),F(1,3),F(1,3),F(0)],[F(1,3),F(1,3),F(0),F(1,3)]]
pi=[F(1,5),F(1,5),F(3,10),F(3,10)];inv={0:1,1:0,2:3,3:2}
for i in range(4):
 ck(sum(P[i])==1);ck(sum(pi[j]*P[j][i] for j in range(4))==pi[i]);ck(P[i][inv[i]]==0)
 for j in range(4):
  ck(sum(P[c][i]*P[c][j] for c in range(4))>0)
  ck(pi[i]*P[i][j]==pi[j]*P[j][i])
ck(P[0][2]!=P[2][0]);ck(sum(pi)==1)
def words(n,legal):
 out=[()];layer=[()]
 for k in range(n):
  layer=[w+(s,) for w in layer for s in range(4) if not w or (P[w[-1]][s]>0 if legal else inv[w[-1]]!=s)]
  out+=layer
 return out
def reduce(w):
 st=[]
 for s in w:
  if st and inv[st[-1]]==s:st.pop()
  else:st.append(s)
 return tuple(st)
def height(w):
 return next((i for i,s in enumerate(w) if s!=0),len(w))
gs=words(5,False);xs=words(6,True);pairs=0
for g in gs:
 p=height(g);heights=[]
 for x in xs:
  tail=3 if x and x[-1]==3 else 2
  if x:ck(P[x[-1]][tail]>0)
  xx=x+(tail,)*(len(g)+8)
  y=reduce(g+xx);h=height(y)
  ck(h<len(y));ck(max(0,p-1)<=h<=p+1)
  heights.append(h);pairs+=1
 ck(max(heights)-min(heights)<=2)
# Finite permutation actions: direct paths versus products of return elements.
actions=0;setcases=0
for n in range(1,5):
 G=list(permutations(range(n)));e=tuple(range(n))
 def mul(g,h):return tuple(g[h[i]] for i in range(n))
 def img(g,A):return frozenset(g[i] for i in A)
 for mask in range(1,1<<n):
  A=frozenset(i for i in range(n) if mask>>i&1)
  R={g for g in G if A&img(g,A)};powers={e};paths={e}
  for k in range(4):
   ck(paths==powers)
   union=frozenset().union(*(img(g,A) for g in powers))
   for bm in range(1,1<<n):
    B=frozenset(i for i in range(n) if bm>>i&1)
    ck(bool(union&B)==any(img(g,A)&B for g in paths));setcases+=1
   paths={h for g in paths for h in G if img(g,A)&img(h,A)}
   powers={mul(g,r) for g in powers for r in R}
  actions+=1
receipt={'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'assertions':checks,'reduced_word_legal_tail_pairs':pairs,'positive_set_cases':actions,'finite_path_pair_tests':setcases,'scope':'Exact finite controls only; measurable-set and infinite-action arguments are proved in the text, not computationally certified.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
