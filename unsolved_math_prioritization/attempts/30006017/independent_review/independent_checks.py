#!/usr/bin/env python3
"""Independent exact contour/topology/genericity controls and labeled Fourier diagnostics."""
from fractions import Fraction as F
from collections import Counter,defaultdict
from itertools import product
import json,random,math,cmath
C=Counter();D=Counter()
def check(v,k):
 assert v,k;C[k]+=1

def det(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def signed_area(P):return sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2

# Every rooted ordered tree through8vertices, represented by its child tuple.
TREES={1:[()]}
def forests(size):
 if size==0:return [()]
 return [(T,)+R for first in range(1,size+1) for T in TREES[first] for R in forests(size-first)]
for n in range(2,9):TREES[n]=forests(n-1)
def sizes(T):
 children=[sizes(t) for t in T];n=1+sum(x[0] for x in children)
 return n,[n]+[k for x in children for k in x[1]]
def walk(T):
 out=[1]
 def rec(T,h):
  for t in T:
   out.append(h+1);rec(t,h+1);out.append(h)
 rec(T,1)
 return [0]+out+[0]
trees=0
for n,ts in TREES.items():
 for T in ts:
  trees+=1;nn,k=sizes(T);W=walk(T);check(nn==n and len(W)==2*n+1,'contour_length')
  # Excursion component intervals at height j+u have length 2*(K-u).
  stack=[];halfspans=[]
  for i in range(2*n):
   if W[i+1]>W[i]:stack.append(i)
   else:
    a=stack.pop();halfspans.append((i+1-a)//2)
  check(sorted(halfspans)==sorted(k),'fringe_interval_spans')
  for alpha in range(1,7):
   atoms=sum(F(v,n)**alpha for v in k)
   continuous=sum(F(v**(alpha+1)-(v-1)**(alpha+1),(alpha+1)*n**alpha) for v in halfspans)
   # Both sides multiplied by 2*sqrt(n); bound becomes alpha.
   check(0<=atoms-continuous<=alpha,'contour_moment_error_bound')
   if alpha==1:check(atoms-continuous==F(1,2),'contour_area_normalization')
check(trees==626,'tree_count')

# Independent abstract-strip topology and Euclidean orientation checks.
q=[(F(1),F(1)),(F(-1),F(1)),(F(-1),F(-1)),(F(1),F(-1))]
for N in range(1,25):
 m=4*N;V=2*(m+1);tri=[]
 for j in range(m):tri += [(2*j,2*j+2,2*j+3),(2*j,2*j+3,2*j+1)]
 incid=defaultdict(list);links=defaultdict(list)
 for t in tri:
  for i in range(3):
   a,b=t[i],t[(i+1)%3];incid[tuple(sorted((a,b)))].append((a,b))
   links[t[i]].append((t[(i+1)%3],t[(i+2)%3]))
 boundary=[e for e,L in incid.items() if len(L)==1]
 check(V-len(incid)+len(tri)==1,'strip_euler_characteristic')
 check(len(boundary)==8*N+2,'strip_boundary_count')
 for e,L in incid.items():check(len(L)==1 or (len(L)==2 and L[0]==L[1][::-1]),'oriented_edge_incidence')
 for v,edges in links.items():
  adj=defaultdict(set)
  for a,b in edges:adj[a].add(b);adj[b].add(a)
  seen={next(iter(adj))};todo=list(seen)
  while todo:
   for z in adj[todo.pop()]:
    if z not in seen:seen.add(z);todo.append(z)
  check(len(seen)==len(adj) and sorted(map(len,adj.values())).count(1)==2 and max(map(len,adj.values()))<=2,'all_vertex_links_are_boundary_paths')
 adj=defaultdict(set)
 for a,b in boundary:adj[a].add(b);adj[b].add(a)
 seen={0};todo=[0]
 while todo:
  for z in adj[todo.pop()]:
   if z not in seen:seen.add(z);todo.append(z)
 check(len(seen)==V and all(len(L)==2 for L in adj.values()),'single_boundary_cycle')
 for a in [F(1,3),F(2,7),F(3,5)]:
  points=[(scale*q[j%4][0],scale*q[j%4][1]) for j in range(m+1) for scale in [1,a]]
  for i,j,k in tri:check(det(sub(points[j],points[i]),sub(points[k],points[i]))>0,'triangle_orientation')
  boundary_order=list(range(0,V,2))+list(range(V-1,0,-2))
  P=[points[i] for i in boundary_order];area=signed_area(P)
  check(area==4*N*(1-a*a),'strip_stokes_area')
  edges=[sub(P[(i+1)%V],P[i]) for i in range(V)];Q=sum(x*x+y*y for x,y in edges)
  check(Q==16*N*(1+a*a)+4*(1-a)**2,'strip_energy')
  check(2*area/Q==F(8*N)*(1-a*a)/(16*N*(1+a*a)+4*(1-a)**2),'normalized_strip_area')

# Two actual rational generic perturbed disks, checking EVERY forbidden pair.
examples=[]
for case,a in enumerate([F(1,2),F(1,3)]):
 rng=random.Random(603017+case);den=6*10**12
 coords=[]
 # Boundary order: outer0..4, inner4..0; starting cut ends stay distinct.
 for scale,j in [(1,j) for j in range(5)]+[(a,j) for j in range(4,-1,-1)]:
  coords.append((int(scale*q[j%4][0]*den)+rng.randrange(-10**8,10**8),int(scale*q[j%4][1]*den)+rng.randrange(-10**8,10**8)))
 side=[sub(coords[(i+1)%10],coords[i]) for i in range(10)]
 sums=[(0,0)]*(1<<10)
 for s in range(1,1<<10):
  bit=s&-s;i=bit.bit_length()-1;b=sums[s^bit];sums[s]=(b[0]+side[i][0],b[1]+side[i][1])
 check(sums[-1]==(0,0),'generic_side_closure')
 for U in range(1,1024):
  rest=1023^U;V=(rest-1)&rest
  while V:
   check(det(sums[U],sums[V])!=0,'actual_generic_subset_determinants');V=(V-1)&rest
 # Map strip vertices into the boundary-order vector.
 for j in range(4):
  A=coords[j];B=coords[j+1];CC=coords[8-j];DD=coords[9-j]
  check(det(sub(B,A),sub(CC,A))>0 and det(sub(CC,A),sub(DD,A))>0,'perturbed_triangle_orientation')
 examples.append({'a':str(a),'common_denominator':den,'boundary_integer_coordinates':coords})

# Signed area, affine covariance and Fourier checks on independent closed walks.
rng=random.Random(60017)
for n in range(3,31):
 for trial in range(8):
  inc=[(rng.randrange(-5,6),rng.randrange(-5,6)) for _ in range(n-1)]
  inc.append((-sum(x for x,y in inc),-sum(y for x,y in inc)))
  P=[(0,0)]
  for x,y in inc[:-1]:P.append((P[-1][0]+x,P[-1][1]+y))
  A=F(sum(det(P[i],P[(i+1)%n]) for i in range(n)),2)
  check(A==F(sum(det(inc[i],inc[j]) for i in range(n) for j in range(i+1,n)),2),'increment_pair_area_identity')
  L=[(2*x+y,x+y) for x,y in P]
  check(F(sum(det(L[i],L[(i+1)%n]) for i in range(n)),2)==A,'determinant_one_affine_area')
  g=[complex(x,y) for x,y in inc];U=[sum(g[j]*cmath.exp(-2j*math.pi*p*j/n) for j in range(n))/math.sqrt(n) for p in range(1,n)]
  spectral=sum((math.cos(math.pi*p/n)/math.sin(math.pi*p/n))*abs(U[p-1])**2/4 for p in range(1,n))
  assert abs(spectral-float(A))<1e-8*(1+abs(A));D['floating_fourier_diagnostics']+=1

print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'exact_breakdown':dict(C),'floating_diagnostics':dict(D),'plane_trees':trees,'generic_examples':examples,'scope':'Independent verification controls only. No simulation or finite check establishes the original disk-area limit or replaces the credited analytic theorems.'},indent=2,sort_keys=True))
