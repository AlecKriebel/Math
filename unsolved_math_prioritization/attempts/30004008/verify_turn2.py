"""Articulation reduction controls. No external packages."""
import itertools as it,json,random
from verify_turn1 import arb,root
N=0;reductions=0;basecalls=0
def check(x):
 global N
 N+=1
 assert x

def comps(V,E):
 out=[];left=set(V)
 while left:
  X={min(left)}
  while True:
   Y=X|{v for u,v in E if u in X and v in V}|{u for u,v in E if v in X and u in V}
   if Y==X:break
   X=Y
  out.append(X);left-=X
 return out

def orient(V,E,r):
 X={r};T=[]
 while len(X)<len(V):
  e=next(((u,v) if u in X else (v,u) for u,v in E if (u in X) != (v in X)),None)
  if e is None:return None
  T.append(e);X.add(e[1])
 return tuple(T)

def matching(es,A):
 m={}
 def aug(e,seen):
  for c,T in A.items():
   if e in T and c not in seen:
    seen.add(c)
    if c not in m or aug(m[c],seen):m[c]=e;return True
  return False
 for e in es:
  if not aug(e,set()):return None
 return list(m.items())

def solve(V,A,H=None):
 global reductions,basecalls
 check(len(A)==len(V)-1)
 if len(V)==1:return []
 if H is None:H={tuple(sorted(e)) for T in A.values() for e in T}
 for v in sorted(V):
  cc=comps(V-{v},[(u,w) for u,w in H if v not in (u,w)])
  if len(cc)<=1:continue
  S=cc[0]|{v};W=(V-cc[0]);a=len(S)-1;b=len(W)-1
  c1=sum(root(V,T) in S-{v} for T in A.values());c2=sum(root(V,T) in W-{v} for T in A.values())
  check(c1<=b or c2<=a)
  if c1>b:S,W=W,S;a,b=b,a
  I=[c for c,T in A.items() if root(V,T) not in S-{v}][:a];check(len(I)==a)
  for T in A.values():
   for U in [S,W]:check(arb(U,[e for e in T if set(e)<=U]))
  B=[];X={v}
  for c in I:
   T=[e for e in A[c] if set(e)<=S];check(root(S,T)==v)
   e=next((e for e in T if e[0] in X and e[1] not in X),None);check(e is not None)
   B.append((c,e));X.add(e[1]);check(arb(X,[e for c,e in B]))
  check(X==S);R={c:tuple(e for e in T if set(e)<=W) for c,T in A.items() if c not in I}
  C=solve(W,R,{e for e in H if set(e)<=W});ans=B+C;reductions+=1
  check(arb(V,[e for c,e in ans]));check(len({c for c,e in ans})==len(A));check(all(e in A[c] for c,e in ans))
  return ans
 basecalls+=1
 # Terminal cycle/edge scaffold: enumerate its spanning paths and roots,
 # and find a distinct-color assignment by an independent augmenting matcher.
 if len(H)==len(V)-1:forests=[H]
 elif len(H)==len(V):forests=[H-{e} for e in sorted(H)]
 else:
  for es in it.product(*A.values()):
   if arb(V,es):return list(zip(A,es))
  raise AssertionError('No base witness')
 for F in forests:
  for r in sorted(V):
   T=orient(V,F,r)
   if T is None:continue
   B=matching(T,A)
   if B is not None:check(arb(V,[e for c,e in B]));return B
 raise AssertionError('No cycle witness')

def colored_trees(V,H):
 ans=[]
 for E in it.combinations(sorted(H),len(V)-1):
  if len(comps(V,E))!=1:continue
  for r in sorted(V):ans.append(orient(V,E,r))
 return ans

def main():
 algebra=0
 for a in range(1,16):
  for b in range(1,16):
   for c1 in range(a+b+1):
    for c2 in range(a+b-c1+1):check(c1<=b or c2<=a);algebra+=1
 V=set(range(5));H={(0,1),(1,2),(0,2),(0,3),(3,4),(0,4)};T=colored_trees(V,H);check(len(T)==45);small=0
 for ix in it.combinations_with_replacement(range(len(T)),4):
  A={c:T[j] for c,j in enumerate(ix)};B=solve(V,A,H);check(arb(V,[e for c,e in B]));small+=1
 rng=random.Random(300040082);large=0;sizes=[]
 for lengths in [[3,3,3],[4,5],[3,4,5],[6,6,6],[8,3,4,5],[3]*8]:
  V={0};H=set();blocks=[]
  for length in lengths:
   v=rng.choice(sorted(V));new=list(range(len(V),len(V)+length-1));vs=[v]+new;V.update(new)
   E={tuple(sorted((vs[j],vs[(j+1)%length]))) for j in range(length)};H|=E;blocks.append(E)
  sizes.append(len(V))
  for rep in range(120):
   A={}
   for c in range(len(V)-1):
    F=set().union(*(E-{rng.choice(sorted(E))} for E in blocks));r=rng.choice(sorted(V));A[c]=orient(V,F,r);check(arb(V,A[c]))
   B=solve(V,A,H);check(arb(V,[e for c,e in B]));check(len(set(c for c,e in B))==len(A));large+=1
 print(json.dumps({'problem_id':30004008,'turn':2,'status':'PASS','exact_assertions':N,'root_count_triples':algebra,'exhaustive_two_triangle_color_multisets':small,'larger_cactus_instances':large,'larger_vertex_counts':sizes,'articulation_reductions':reductions,'terminal_solver_calls':basecalls,'limits':'Finite validation of the construction only; all-cactus theorem uses the separate articulation proof and credited cycle existence theorem.'},indent=2))
if __name__=='__main__':main()
