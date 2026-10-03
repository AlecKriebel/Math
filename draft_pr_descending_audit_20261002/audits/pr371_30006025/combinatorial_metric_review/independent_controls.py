#!/usr/bin/env python3
"""Independent finite map checks and explicit falsification controls; no geometric oracle."""
from fractions import Fraction as Q
from math import factorial, comb
from collections import Counter
import itertools, json
counts=Counter();checks=0
def ck(v,label):
 global checks
 assert v,label
 checks+=1;counts[label]+=1
def cyc(p):
 seen=set();out=[]
 for i in p:
  if i in seen:continue
  j=i;orbit=[]
  while j not in seen:seen.add(j);orbit.append(j);j=p[j]
  ck(j==i,'permutation_cycle_closes')
  out.append(orbit)
 return out
def matchings(labels):
 if not labels:yield {};return
 a=labels[0]
 for j,b in enumerate(labels[1:],1):
  rest=labels[1:j]+labels[j+1:]
  for tail in matchings(rest):yield {a:b,b:a,**tail}
def rotations(words):
 return {x:w[(j+1)%len(w)] for w in words for j,x in enumerate(w)}
# Explicit positive control and negative mutant: same vertex quotient, wrong rotation genus.
a={'a':'x','x':'a','b':'y','y':'b'}
rotA={'a':'b','b':'x','x':'y','y':'a'};rotB={'a':'b','b':'y','y':'x','x':'a'}
facesA=cyc({x:rotA[a[x]] for x in a});facesB=cyc({x:rotB[a[x]] for x in a})
ck(len(facesA)==1 and len(facesB)==3,'naive_rotation_mutant_detected')
rotation_example={'alpha':a,'one_face_rotation':rotA,'one_face_cycles':facesA,'three_face_rotation':rotB,'three_face_cycles':facesB,'genera':[1,0]}
# Complete canonical rooted one-face pairings through n=7. Convention phi=alpha sigma.
mapcounts={};genuscounts={};trisection_totals={}
for n in range(1,8):
 h=tuple(range(2*n));by_genus=Counter();tri=Counter();total=0
 for alpha in matchings(h):
  sigma={i:alpha[(i+1)%(2*n)] for i in h};verts=cyc(sigma);V=len(verts)
  numerator=n+1-V;ck(numerator>=0 and numerator%2==0,'one_face_euler_genus')
  g=numerator//2;by_genus[g]+=1;total+=1
  minima={x:min(v) for v in verts for x in v}
  trisections=sum(sigma[x]<=x and sigma[x]!=minima[x] for x in h)
  ck(trisections==2*g,'all_pairings_trisection_identity');tri[g]+=trisections
  word=list(range(2*n));edgekeys={tuple(sorted((i,alpha[i]))) for i in h}
  ck(len(edgekeys)==n and all(sum(tuple(sorted((i,alpha[i])))==e for i in word)==2 for e in edgekeys),'boundary_edge_copies')
 ck(total==factorial(2*n)//(2**n*factorial(n)),'complete_pairing_count')
 ck(by_genus[0]==comb(2*n,n)//(n+1),'plane_tree_catalan_count')
 mapcounts[n]=total;genuscounts[n]=dict(by_genus);trisection_totals[n]=dict(tri)
# Exact all-size counting cross-check, using cycle-type enumeration rather than map code.
# Signed odd permutations: choose a cycle-type m and count m! / prod j^a a!, then 2^#cycles.
def oddtypes(m,j=1):
 if m==0:yield {};return
 for size in range(j,m+1,2):
  for tail in oddtypes(m-size,size):
   t=dict(tail);t[size]=t.get(size,0)+1;yield t
# Avoid duplicate multisets from recursion (one recurrence path can still repeat equal sizes).
for n in range(1,8):
 m=n+1;seen=set();signed=Counter()
 for typ in oddtypes(m):
  key=tuple(sorted(typ.items()))
  if key in seen:continue
  seen.add(key);c=sum(typ.values());g=(m-c)//2;den=1
  for j,a in typ.items():den*=j**a*factorial(a)
  signed[g]+=factorial(m)//den*2**c
 cat=comb(2*n,n)//(n+1)
 for g,num in genuscounts[n].items():ck(cat*signed[g]==2**(n+1)*num,'signed_CFF_cardinality')
# Cubic genus-two one-face example with a separating bridge, independent of K3,3.
a2={0:2,2:0,1:3,3:1,4:6,6:4,5:7,7:5}
bouquet_sigma={i:((a2[i]+1)%8) for i in range(8)}
b=cyc(bouquet_sigma)[0]
for j in range(5):a2[8+2*j]=9+2*j;a2[9+2*j]=8+2*j
words=[[b[0],b[1],8]]
for j in range(1,5):words.append([b[j+1],8+2*j,9+2*(j-1)])
words.append([b[6],b[7],17]);sigma2=rotations(words);face2={i:sigma2[a2[i]] for i in a2};f2=cyc(face2)
ck(len(f2)==1 and len(words)==6 and len(a2)//2==9,'bridge_example_cubic_genus_two')
vert={x:j for j,w in enumerate(words) for x in w};edges=[tuple(sorted((i,a2[i]))) for i in a2 if i<a2[i]]
bridge=[]
for edge in edges:
 adjacency={j:set() for j in range(6)}
 for e in edges:
  if e==edge:continue
  u,v=vert[e[0]],vert[e[1]];adjacency[u].add(v);adjacency[v].add(u)
 reached={0};front=[0]
 while front:
  u=front.pop()
  for v in adjacency[u]-reached:reached.add(v);front.append(v)
 if len(reached)<6:bridge.append(edge)
ck(len(bridge)==1,'separating_bridge_detected')
lengths={e:Q(j+1,7) for j,e in enumerate(edges)};perimeter=sum(lengths[tuple(sorted((i,a2[i])))] for i in f2[0])
ck(perimeter==2*sum(lengths.values()),'bridge_perimeter_factor_two')
ck(perimeter!=sum(lengths.values()),'factor_one_perimeter_mutant_detected')
# Rational negative control: a cap C=1 cannot satisfy any positive required increase.
for E in range(1,9):
 raw=[Q(i+1) for i in range(E)];x=[v/sum(raw) for v in raw]
 for k in range(E+1):
  top=sum(sorted(x,reverse=True)[:k],Q(0))
  for chosen in itertools.combinations(range(E),k):
   ck(sum(x[i] for i in chosen)<=top,'adaptive_capacity_subsets')
   y=[v/2 if i in chosen else v for i,v in enumerate(x)]
   ck(sum(y)-1<=0,'unit_cap_no_positive_increase')
   ck(sum(y)-1<=Q(4,3)*top,'decrease_included_capacity')
# All-E broken-stick mean alternative: exact simplex-volume integration to E=40.
for E in range(1,41):
 H=[Q(0)]
 for i in range(1,E+1):H.append(H[-1]+Q(1,i))
 rank=[sum((Q((-1)**(r-j)*comb(r-1,j-1)*comb(E,r),r*E) for r in range(j,E+1)),Q(0)) for j in range(1,E+1)]
 for k in range(E+1):ck(sum(rank[:k],Q(0))==Q(k,E)*(1+H[E]-H[k]),'independent_simplex_integrals')
 ck(sum(rank,Q(0))==1,'all_edges_identity')
print(json.dumps({'status':'PASS','assertions':checks,'by_scope':dict(counts),'all_rooted_pairings_by_edges':mapcounts,'genus_counts':genuscounts,'trisection_totals':trisection_totals,'naive_rotation_counterexample':rotation_example,'cubic_bridge_example':{'alpha':a2,'vertex_cycles':words,'face_cycles':f2,'bridge_darts':bridge,'face_perimeter':str(perimeter),'sum_edge_lengths':str(sum(lengths.values()))},'negative_controls':['naive concatenation changes genus','one-copy perimeter rejected','unit stretch cap cannot add positive length'],'scope':'Finite independently implemented falsification controls. Universal proofs and credited geometric, analytic and probability theorems are audited in MATHEMATICAL_VERDICT.md; no full-source solution or novelty follows from these checks.'},indent=2,sort_keys=True))
