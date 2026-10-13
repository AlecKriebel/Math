#!/usr/bin/env python3
"""Independent finite controls. Does not implement the general PL search.
No author verification functions are imported. Standard library only.
"""
from itertools import combinations_with_replacement, product, permutations
from fractions import Fraction as F
from collections import Counter
import json
counts=Counter(); examples={}
def check(x):
 assert x
 counts['assertions']+=1

def components(vertices,edges):
 adj={v:set() for v in vertices}
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 groups=[]; seen=set()
 for v in vertices:
  if v in seen:continue
  todo=[v];g=set()
  while todo:
   u=todo.pop()
   if u in g:continue
   g.add(u);todo.extend(adj[u]-g)
  seen|=g;groups.append(g)
 return groups

def cycles(mapping):
 seen=set();ans=0
 for a in mapping:
  local=set();x=a
  while x in mapping and x not in seen and x not in local:
   local.add(x);x=mapping[x]
  if x in local:ans+=1
  seen|=local
 return ans

def tables(arr,n):
 opts=[]
 for v in range(n):
  inc=[a for a,(s,t) in enumerate(arr) if t==v];out=[a for a,(s,t) in enumerate(arr) if s==v]
  if len(inc)>2 or len(out)>2:return
  pairs=list(product(inc,out));local=[]
  for bits in product((0,1),repeat=len(pairs)):
   r={p for p,b in zip(pairs,bits) if b}
   if all(sum((a,b) in r for b in out)<=1 and sum((a,b) not in r for b in out)<=1 for a in inc) and all(sum((a,b) in r for a in inc)<=1 and sum((a,b) not in r for a in inc)<=1 for b in out):local.append(r)
  opts.append(local)
 for groups in product(*opts):yield set().union(*groups)

def construct(n,original,relations):
 arr=list(original);rel=set(relations);leaf=n
 for v in range(n):
  inc=[i for i,(s,t) in enumerate(arr) if t==v];out=[i for i,(s,t) in enumerate(arr) if s==v]
  old=list(product(inc,out))
  while len(inc)<2:inc.append(len(arr));arr.append((leaf,v));leaf+=1
  while len(out)<2:out.append(len(arr));arr.append((v,leaf));leaf+=1
  candidates=[set(zip(inc,p)) for p in permutations(out)]
  good=[r for r in candidates if all((p in r)==(p in rel) for p in old)]
  check(bool(good));rel|=good[0]
 A=len(arr)
 # A lozenge has cyclic corners (source, green, target, red).
 # Build equivalence classes as connected components, not union-find.
 ce=[];se=[];used=set()
 for i,(s,t) in enumerate(arr):
  for j,(u,z) in enumerate(arr):
   if t!=u:continue
   ce.append((4*i+2,4*j))
   if (i,j) in rel:ce.append((4*i+3,4*j+3));e,f=4*i+2,4*j+3
   else:ce.append((4*i+1,4*j+1));e,f=4*i+1,4*j
   check(e not in used and f not in used);used|={e,f};se.append((e,f))
 corner=components(range(4*A),ce); side=components(range(4*A),se)
 c={x:i for i,g in enumerate(corner) for x in g};boundary=[]
 for i in range(A):
  for k in range(4):
   if 4*i+k not in used:boundary.append((c[4*i+k],c[4*i+(k+1)%4]))
 bdverts={v for e in boundary for v in e};deg=Counter(v for e in boundary for v in e)
 check(all(d==2 for d in deg.values()));b=len(components(bdverts,boundary))
 green={c[4*i+1] for i in range(A)};red={c[4*i+3] for i in range(A)}
 pw=len(green-bdverts);pb=len(red-bdverts)
 chi=len(corner)-len(side)+A;g=(2-b-chi)//2
 # Independently traverse the two kinds of maximal arrow paths; their
 # endpoint matchings give the boundary circles (PPP Remark 4.11).
 maps=[];matchedges=[]
 for related in (False,True):
  mp={i:j for i,(s,t) in enumerate(arr) for j,(u,z) in enumerate(arr) if t==u and (((i,j) in rel)==related)}
  maps.append(mp)
  for i,(s,t) in enumerate(arr):
   if s<n:continue
   seen=set();j=i
   while j in mp:
    check(j not in seen);seen.add(j);j=mp[j]
   check(arr[j][1]>=n);matchedges.append((s,arr[j][1]))
 check(len(components(range(n,leaf),matchedges))==b)
 check(pw==cycles(maps[0]));check(pb==cycles(maps[1]))
 check(pw==0);check(len(green&bdverts)==2*n-len(original))
 check(chi-pb==n-len(original));check(g>=0 and 2-2*g-b==chi)
 check(len(green&bdverts)==len(red&bdverts))
 return g,b,pb

for n in range(1,4):
 alphabet=list(product(range(n),repeat=2))
 for m in range(0,2*n):
  for arr in combinations_with_replacement(alphabet,m):
   if len(components(range(n),arr))!=1:continue
   for rel in tables(arr,n):
    permitted={i:j for i,(s,t) in enumerate(arr) for j,(u,z) in enumerate(arr) if t==u and (i,j) not in rel}
    if cycles(permitted):continue # finite-dimensional iff permitted transition graph acyclic
    g,b,p=construct(n,arr,rel);counts['connected_gentle_inputs']+=1
    counts['genus_'+str(g)]+=1
    examples.setdefault(str((g,b,p)),{'vertices':n,'arrows':arr,'relations':sorted(rel)})

# Exact determinant intersection formula vs orientation-sign criterion,
# exhaustively on a small rational grid, including endpoint degeneracies.
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def sub(u,v):return(u[0]-v[0],u[1]-v[1])
def orient(a,b,c):return cross(sub(b,a),sub(c,a))
def det_inter(a,b,c,d):
 u,v,w=sub(b,a),sub(d,c),sub(c,a);den=cross(u,v)
 if den==0:return False
 return 0<F(cross(w,v),den)<1 and 0<F(cross(w,u),den)<1
pts=list(product((F(-1,2),F(0),F(1,2)),repeat=2))
for a,b,c,d in product(pts,repeat=4):
 check(det_inter(a,b,c,d)==(orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0));counts['intersection_controls']+=1

# A standard genus-g geometric handle system has a symplectic pairing.
# Compare the displayed Arf formula under every symplectic transvection.
for g in (1,2,3):
 vecs=list(product((0,1),repeat=2*g))
 def pairing(x,y):return sum(x[2*i]*y[2*i+1]+x[2*i+1]*y[2*i] for i in range(g))%2
 basis=[tuple(int(i==j) for i in range(2*g)) for j in range(2*g)]
 for linear in vecs:
  def q(v):return (sum(v[2*i]*v[2*i+1] for i in range(g))+sum(x*y for x,y in zip(v,linear)))%2
  arf=sum(q(basis[2*i])*q(basis[2*i+1]) for i in range(g))%2
  for v in vecs:
   changed=[tuple(x^((pairing(e,v))*y) for x,y in zip(e,v)) for e in basis]
   check(sum(q(changed[2*i])*q(changed[2*i+1]) for i in range(g))%2==arf);counts['arf_controls']+=1
print(json.dumps({'status':'PASS','counts':dict(counts),'topological_examples':examples,'scope':'Supplementary finite construction/intersection/Arf controls, not a complete implementation or proof of the universal search.'},indent=2))
