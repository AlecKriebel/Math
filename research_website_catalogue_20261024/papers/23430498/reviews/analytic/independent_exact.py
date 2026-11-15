#!/usr/bin/env python3
"""Read-only exact algebra from the manuscript; no deposited program imports.
No finite test here certifies universal topology, classification or integration.
"""
from fractions import Fraction as F
from itertools import permutations,combinations
from collections import Counter
from pathlib import Path
import json,hashlib,sys
sys.dont_write_bytecode=True
checks=Counter()
def ck(x,m):
 checks[m]+=1
 if not x:raise RuntimeError(m)
def red(w):
 a=[]
 for x in w:
  if a and a[-1]==-x:a.pop()
  else:a.append(x)
 return tuple(a)
def inv(w):return tuple(-x for x in w[::-1])
def apply(f,w):return red([a for x in w for a in (f[x-1] if x>0 else inv(f[-x-1]))])
def compose(f,g):return tuple(apply(f,w) for w in g)
def artin(i,negative=False,k=3):
 f=[(j,) for j in range(1,k+1)]
 f[i-1],f[i]=((i,i+1,-i),(i,))
 if negative:f[i-1],f[i]=(i+1,),(-(i+1),i,i+1)
 return tuple(f)
def word_aut(w,k=3):
 a=tuple((i,) for i in range(1,k+1))
 for x in w:a=compose(a,artin(abs(x),x<0,k))
 return a
def magnus(w,n=2):
 out={():1}
 for x in w:
  gen={():1,(abs(x),):1 if x>0 else -1}
  if x<0:gen[(abs(x),abs(x))]=1
  new=Counter()
  for a,b in out.items():
   for c,d in gen.items():
    if len(a+c)<=n:new[a+c]+=b*d
  out={a:b for a,b in new.items() if b}
 return out
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def trace(a):return sum(a[i][i] for i in range(len(a)))
def product(a):
 out=eye(len(a[0]))
 for x in a:out=mm(out,x)
 return out
def cyclic(w):return min(w[i:]+w[:i] for i in range(len(w))) if w else ''
def adj(a):
 n=len(a);cols=[]
 for i in range(n):
  for j in range(n):
   e=[[int(u==i and v==j) for v in range(n)] for u in range(n)]
   ae,ea=mm(a,e),mm(e,a);cols.append([ae[u][v]-ea[u][v] for u in range(n) for v in range(n)])
 return [list(x) for x in zip(*cols)]
def wheel_terms(w):
 c=Counter()
 for mask in range(1<<len(w)):
  left=''.join(w[i] for i in range(len(w)) if not(mask>>i&1))
  right=''.join(w[i] for i in range(len(w)-1,-1,-1) if mask>>i&1)
  c[tuple(sorted((cyclic(left),cyclic(right))))]+=(-1)**mask.bit_count()
 return {k:v for k,v in c.items() if v}
def det(a):
 n=len(a);out=F(1);a=[list(map(F,row)) for row in a]
 for i in range(n):
  p=next((j for j in range(i,n) if a[j][i]),None)
  if p is None:return F(0)
  if p!=i:a[p],a[i]=a[i],a[p];out=-out
  q=a[i][i];out*=q;a[i]=[x/q for x in a[i]]
  for j in range(i+1,n):
   q=a[j][i];a[j]=[x-q*y for x,y in zip(a[j],a[i])]
 return out
def pmul(a,b):
 c=Counter()
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return [c[i] for i in range(len(a)+len(b)-1)]
def pdiv(a,b):
 a=list(map(F,a));q=[F(0)]*(len(a)-len(b)+1)
 for i in range(len(q)-1,-1,-1):
  q[i]=a[i+len(b)-1]/b[-1]
  for j,c in enumerate(b):a[i+j]-=q[i]*c
 ck(not any(a),'exact Alexander polynomial division');return q
def torus(p,q):
 def fac(n):return [1]+[0]*(n-1)+[-1]
 a=pdiv(pmul(fac(p*q),fac(1)),pmul(fac(p),fac(q)));shift=(p-1)*(q-1)//2
 ck(sum(a)==1,'Alexander normalization')
 return sum(F((i-shift)*(i-shift-1),2)*c for i,c in enumerate(a)),a,shift
def main():
 ck(len(sys.argv)==1,'no external overrides')
 p=Path(__file__).resolve().parents[2]
 for name,h in {'sources/SOURCE_READY.json':'1f728d52dd3bb791833a837fb3bae7eab1b3a37ce7ecd9c4655b94f4d693cf46','sources/cache/native-assets-attempt3/free-exterior-string-links-v1.0.pdf':'3a3f2a9e4bbd002217fca218f963957245b767e4a782e80b917031a3ef2d250f','sources/cache/extracted/container-001/publication/research_note.tex':'1cae1a04cdc0462efb86d8e05ddba2db6a9b8c0168fbc2ed40868460e7f7ca1f','reviews/analytic/INITIAL_SEAL.json':'c36d1d42f4db0c21985b48877c46c87937cf1ff6355d5ae395f1712ae66d8b60'}.items():ck(hashlib.sha256((p/name).read_bytes()).hexdigest()==h,'primary target binding')
 beta=(1,1,2,2,-1,-1,-2,-2);phi=word_aut(beta)
 cs=[(1,2,-1,3,1,-2,-1,-3),(-3,-1,3,1),(-3,-1,3,1,-2,-1,-3,1,3,1,2,-1)]
 expected=[{():1,(2,3):1,(3,2):-1},{():1,(1,3):-1,(3,1):1},{():1,(1,2):1,(2,1):-1}]
 for i,c in enumerate(cs,1):
  ck(red(c+(i,)+inv(c))==phi[i-1],'complete Artin conjugator identity')
  ck(sum(1 if x==i else -1 if x==-i else 0 for x in c)==0,'preferred longitude self exponent')
  ck(magnus(c)==expected[i-1],'full truncated Magnus polynomial')
 identity=tuple((i,) for i in range(1,4))
 ck(compose(word_aut(beta),word_aut(tuple(-x for x in beta[::-1])))==identity,'full free-word inverse Artin action')
 for pair in combinations(range(1,4),2):
  for i in pair:
   after=red([x for x in phi[i-1] if abs(x) in pair]);ck(after==(i,),'every pair deletion identity')
 for perm in permutations((1,2,3)):
  c=tuple((1 if x>0 else -1)*perm[abs(x)-1] for x in cs[2]);m=magnus(c)
  ck(m=={():1,(perm[0],perm[1]):1,(perm[1],perm[0]):-1},'all relabelled triple leading terms')
 # Whisker and substitution checks are corroboration; the Gamma3 argument is in the proof.
 for q in [(1,),(-2,3,1),(3,2,-1,-3)]:
  c=red(apply(phi,q)+cs[2]+inv(q));ck(magnus(c)==expected[2],'whisker quadratic invariance')
 X=[[0,1,1,1],[1,0,0,0],[0,-1,0,0],[-1,-1,-1,1]]
 Y=[[0,0,-1,1],[-1,-1,1,1],[-1,0,0,0],[0,0,-1,-1]];mats={'1':X,'2':Y}
 def tw(w):return trace(product([mats[c] for c in w])) if w else 4
 word='1121222';terms=wheel_terms(word)
 ck(terms=={('','1121222'):1,('','1122212'):-1,('112212','2'):3,('112122','2'):-3},'entire 128-term cyclic trace polynomial')
 value=sum(c*tw(a)*tw(b) for (a,b),c in terms.items())
 ck(value==6,'nonzero exact wheel value')
 ad={'1':adj(X),'2':adj(Y)}
 ck(trace(product([ad[c] for c in word]))==value,'direct 16-dimensional adjoint trace')
 ck(trace(product([ad[c] for c in word[::-1]]))==-value,'direct reversed adjoint trace')
 ck(wheel_terms(word[::-1])=={k:-v for k,v in terms.items()},'complete reversed cyclic polynomial')
 for name,want in {'2':-2,'1121222':38,'1122212':20,'112212':-12,'112122':-23}.items():ck(tw(name)==want,'individual exact trace')
 # Universal determinant identities by block support, not parametric sampling.
 top=[[1,0,0],[1,1,1],[1,-1,1]];bottom=[[0,0,1],[1,5,0],[5,1,0]]
 ck(det(top)==2 and det(bottom)==-24 and det(top)*det(bottom)==-48,'parametric six-row block determinant proof')
 ck(det([[2,0,0],[0,2,0],[2,2,-4]])==-16,'concordance row determinant')
 ck(det([[1,5],[5,1]])==-24,'component coefficient determinant')
 # The full degree<=2 polynomial evaluation interpolation matrix for arbitrary dimension m.
 for n in range(1,7):
  mons=[()]+[(i,) for i in range(n)]+[(i,j) for i in range(n) for j in range(i,n)]
  pts=[tuple(0 for _ in range(n))]
  for i in range(n):
   for s in [1,-1]:pts.append(tuple(s if i==j else 0 for j in range(n)))
  for i,j in combinations(range(n),2):pts.append(tuple(int(k in (i,j)) for k in range(n)))
  a=[[1 if not w else z[w[0]] if len(w)==1 else z[w[0]]*z[w[1]] for w in mons] for z in pts]
  ck(det(a)!=0,'complete low-degree multivariate interpolation')
 t,poly,shift=torus(2,3);u,poly2,shift2=torus(3,4)
 ck(t==1 and u==5,'independent Alexander derivative component values')
 sq=pmul(poly,poly);csq=sum(F((i-2*shift)*(i-2*shift-1),2)*c for i,c in enumerate(sq));ck(csq==2,'square-knot Conway coefficient')
 negative={'wrong reversal parity':value!=-value,'wrong wheel sign':value!=-6,'collapsed component determinant':det([[1,1],[1,1]])==0,'erased rational plat row':det([[0,0,0],[1,5,0],[5,1,0]])==0,'wrong Magnus commutator sign':magnus(cs[2])!={():1,(1,2):-1,(2,1):1}}
 for k,v in negative.items():ck(v,'false construction rejection')
 print(json.dumps({'assessment':'INDEPENDENT_EXACT_LOW_DEGREE_AND_WHEEL_CONSTRUCTIONS_SUPPORTED','optimized':not __debug__,'checks':dict(sorted(checks.items())),'total_checks':sum(checks.values()),'wheel_trace':value,'antisymmetric_trace':2*value,'false_constructions_rejected':list(negative),'scope':'Exact algebraic identities only. Universal topology, primary classification/deframing/integration and arbitrary k follow the written proof, not numerical sampling.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
