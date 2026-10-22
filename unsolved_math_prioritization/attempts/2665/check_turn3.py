"""Exact graph-label arithmetic; no topological theorem is certified by this script."""
from collections import Counter,deque
from itertools import combinations
from math import gcd,isqrt
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
def divisors(n):
 return sorted({d for a in range(1,isqrt(n)+1)if n%a==0 for d in (a,n//a)})
def graph(N):
 k=N//2;T={4*b*b*d*d%N for b in divisors(k)for d in divisors(k+1)}
 D={1:0};P={1:[]};q=deque([1])
 while q:
  x=q.popleft()
  for t in sorted(T):
   y=x*t%N
   if y not in D:D[y]=D[x]+1;P[y]=P[x]+[t];q.append(y)
 return T,D,P
rows=[]
for N in range(3,202,2):
 T,D,P=graph(N);H=set(D);layers={1}
 ck(1 in T and all(gcd(t,N)==1 for t in T),'unit_and_identity')
 ck({pow(t,-1,N)for t in T}==T,'inverse_symmetry')
 for r in range(max(D.values())+1):
  ck(layers=={h for h in H if D[h]<=r},'distance_equals_product_ball')
  layers={x*t%N for x in layers for t in T}
 for h,path in P.items():
  p=1
  for t in path:p=p*t%N
  ck(p==h and len(path)==D[h],'explicit_shortest_word')
 for a in H:
  for t in T:
   ck(abs(D[a]-D[a*t%N])<=1,'one_step_metric_inequality')
 for a in H:
  for b in H:
   ck(D[a*b%N]<=D[a]+D[b],'triangle_inequality')
 rows.append({'N':N,'T_size':len(T),'H_size':len(H),'diameter':max(D.values()),'outside_two_step_ball':sorted(h for h in H if D[h]>2)})
T,D,P=graph(37);T2={x*y%37 for x in T for y in T}
ck(T=={1,4,7,9,16,28,33,36},'N37_one_step_set')
ck(T2=={1,4,7,9,10,11,12,16,21,26,27,28,30,33,34,36},'N37_two_step_set')
ck(set(D)-T2=={3,25},'N37_exact_obstructed_residues')
ck(P[3]==[4,16,33] and D[3]==3,'N37_three_step_certificate')
ck(sum(r['N']<37 and bool(r['outside_two_step_ball']) for r in rows)==0,'first_gap_in_enumerated_range')
for N,aa in [(37,[1,3]),(13,[1,12])]:
 k=N//2
 for a in aa:
  V=[[a,k+1],[k,0]]
  ck(V[0][1]-V[1][0]==1,'skew_unimodular')
  ck(V[0][0]*V[1][1]-V[0][1]*V[1][0]==-k*(k+1),'core_determinant')
  for t in range(-5,6):
   det=(t-1)**2*V[0][0]*V[1][1]-(t*V[0][1]-V[1][0])*(t*V[1][0]-V[0][1])
   ck(det==-k*(k+1)*t*t+(2*k*(k+1)+1)*t-k*(k+1),'alexander_evaluation')
T,D,P=graph(13);H=set(D)
missing={tuple(sorted((a,b)))for a,b in combinations(H,2)if b*pow(a,-1,13)%13 not in T}
ck(missing=={(1,12),(3,10),(4,9)},'N13_forbidden_matching')
ck(D[12]==2,'N13_not_obstructed_by_two_step_test')
for r in range(7):
 for S in combinations(sorted(H),r):
  count=sum(set(e)<=set(S)for e in missing)
  ck((r<5 or count>=2),'N13_five_labels_need_two_nonedges')
ck(any(sum(set(e)<=set(S)for e in missing)<=1 for S in combinations(H,4)),'four_labels_pass_necessary_test_only')
# Literal graphs of one or two d-simplices as in the published theorem.
for d in range(5):
 options=[1]if d in (0,4)else[1,2]
 for count in options:
  faces=[set(range(d+1))]
  if count==2:faces.append(set(range(d))|{d+1})
  verts=set().union(*faces);edges={tuple(sorted(e))for f in faces for e in combinations(f,2)}
  nonedges=set(combinations(sorted(verts),2))-edges
  ck(len(verts)<=5,'published_simplex_vertex_bound')
  ck(len(nonedges)<=1,'published_simplex_nonedge_bound')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'enumerated_rows':rows,'scope':'Exact finite arithmetic and the combinatorics of the stated simplex input only; topology is a credited external theorem. No satellite realization or unrestricted obstruction certified.'},sort_keys=True,indent=2))
