"""Exact finite controls for the source-component reduction; stdlib only."""
import itertools as it,json,random
from collections import Counter
N=0
def check(x):
 global N
 N+=1
 assert x

def reach(V,E,r):
 X={r}
 while True:
  Y=X|{v for u,v in E if u in X}
  if Y==X:return X
  X=Y

def root(V,E):
 deg={v:0 for v in V}
 for u,v in E:deg[v]+=1
 z=[v for v in V if deg[v]==0]
 return z[0] if len(z)==1 and max(deg.values())<=1 else None

def arb(V,E):
 if len(E)!=len(V)-1:return False
 r=root(V,E)
 return r is not None and reach(V,E,r)==set(V)

def trees(n):
 V=range(n);ans=[]
 for r in V:
  W=[v for v in V if v!=r]
  for pp in it.product(V,repeat=n-1):
   E=tuple(zip(pp,W))
   if arb(V,E):ans.append(E)
 return ans

def source(V,A):
 E=[e for T in A for e in T];r=root(V,A[0]);R=reach(V,E,r)
 return {v for v in R if r in reach(V,E,v)}

def solve(V,A,colors):
 if len(V)==1:return []
 opts=[[e for e in A[c] if e[0] in V and e[1] in V] for c in colors]
 for es in it.product(*opts):
  if arb(V,es):return list(zip(colors,es))
 return None

def inspect(V,A,all_subsets=True):
 S=source(V,A);check(bool(S));check(not any(u not in S and v in S for T in A for u,v in T))
 check(all(root(V,T) in S for T in A))
 for T in A:check(arb(S,[e for e in T if e[0] in S and e[1] in S]))
 subsets=it.combinations(range(len(A)),len(S)-1)
 tested=0
 for J in subsets:
  B=solve(S,A,J);check(B is not None);X=set(S)
  for c in range(len(A)):
   if c in J:continue
   exits=[(u,v) for u,v in A[c] if u in X and v not in X];check(bool(exits))
   e=exits[0];B.append((c,e));X.add(e[1]);check(arb(X,[e for _,e in B]))
  check(X==set(V));check(len({c for c,e in B})==len(A));check(arb(V,[e for c,e in B]));tested+=1
  if not all_subsets:break
 return tested,len(S)

def capacity(counts):
 z=sorted(counts,reverse=True)+[0,0]
 return sum(c>0 for c in counts)+max(0,z[0]-1)+max(0,z[1]-1)

def main():
 counts={};local=0;proper=0
 for n in range(2,5):
  T=trees(n);check(len(T)==n**(n-1));cases=0
  for ix in it.combinations_with_replacement(range(len(T)),n-1):
   a,s=inspect(set(range(n)),[T[i] for i in ix]);local+=a;proper+=s<n;cases+=1
  counts[str(n)]=cases
 # Capacity identity: exhaustive root multiplicities up to five roots, each <=4.
 capcases=0
 for R in range(1,6):
  for cs in it.product(range(1,5),repeat=R):
   feasible=[]
   for ss in it.product(*(range(c+1) for c in cs)):
    if sum(c>=2 for c in ss)<=2:feasible.append(sum(ss))
   check(max(feasible)==capacity(cs));check(set(feasible)==set(range(capacity(cs)+1)));capcases+=1
 # Larger instances use all source vertices as roots and complete source stars for each color,
 # guaranteeing their union's source component; append a random rooted outside tree.
 rng=random.Random(30004008);large=0
 for n in range(5,13):
  for s in range(2,min(5,n)):
   for rep in range(7):
    V=set(range(n));A=[]
    for c in range(n-1):
     r=c%s;E=[(r,v) for v in range(s) if v!=r]
     E += [(rng.randrange(v),v) for v in range(s,n)]
     A.append(tuple(E));check(arb(V,E))
    a,t=inspect(V,A);check(t==s);large+=1;local+=a
 print(json.dumps({'problem_id':30004008,'turn':1,'status':'PASS','exact_assertions':N,'exhaustive_color_multiset_instances_by_n':counts,'proper_source_instances_in_small_enumeration':proper,'larger_constructed_instances':large,'restricted_color_subsets_lifted':local,'root_capacity_vectors':capcases,'limits':'Finite checks validate these instances only. The all-n source-component reduction and capacity formula are proved separately; full conjecture unresolved.'},indent=2))
if __name__=='__main__':main()
