#!/usr/bin/env python3
"""Fresh exact plane/segment geometry, Gale-kernel and probability controls.
No imports from supplied verification programs. Finite tests are not a proof.
"""
from fractions import Fraction as Q
from itertools import combinations,permutations,product
from collections import Counter
from math import comb,factorial
from pathlib import Path
import random,json,hashlib,datetime,time
counts=Counter();start=time.monotonic()
def check(c,k):
 counts[k]+=1
 if not c:raise AssertionError(k)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(s,a):return tuple(s*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def project(v,k):return tuple(x for i,x in enumerate(v) if i!=k)
def normal(tri):return cross(sub(tri[1],tri[0]),sub(tri[2],tri[0]))
def point_in_tri(p,t):
 n=normal(t)
 if dot(n,sub(p,t[0])):return False
 k=next(i for i,x in enumerate(n) if x);p=project(p,k);a,b,c=[project(x,k) for x in t]
 signs=[orient(a,b,p),orient(b,c,p),orient(c,a,p)]
 return all(x>=0 for x in signs) or all(x<=0 for x in signs)
def on_segment(p,a,b):
 d=sub(b,a)
 if not any(d):return p==a
 k=next(i for i,x in enumerate(d) if x);s=(p[k]-a[k])/d[k]
 return 0<=s<=1 and p==add(a,scale(s,d))
def edge_tri(a,b,t):
 n=normal(t);da=dot(n,sub(a,t[0]));db=dot(n,sub(b,t[0]));pts=set()
 if da!=db:
  s=da/(da-db)
  if 0<=s<=1:
   p=add(a,scale(s,sub(b,a)))
   if point_in_tri(p,t):pts.add(p)
 elif da==0:
  if point_in_tri(a,t):pts.add(a)
  if point_in_tri(b,t):pts.add(b)
  k=next(i for i,x in enumerate(n) if x);a2,b2=project(a,k),project(b,k);r=sub(b2,a2)
  for c,d in [(t[0],t[1]),(t[1],t[2]),(t[2],t[0])]:
   c2,d2=project(c,k),project(d,k);s=sub(d2,c2);den=r[0]*s[1]-r[1]*s[0]
   if den:
    w=sub(c2,a2);u=(w[0]*s[1]-w[1]*s[0])/den;v=(w[0]*r[1]-w[1]*r[0])/den
    if 0<=u<=1 and 0<=v<=1:pts.add(add(a,scale(u,sub(b,a))))
   else:
    for p in (a,b,c,d):
     if on_segment(p,a,b) and on_segment(p,c,d):pts.add(p)
 return pts
def intersection_points(a,b):
 pts=set()
 for t,u in [(a,b),(b,a)]:
  for x,y in [(t[0],t[1]),(t[1],t[2]),(t[2],t[0])]:pts.update(edge_tri(x,y,u))
 return pts
# The intersection is convex. Its extreme points come from these edge/plane or
# coplanar edge/edge intersections, including contained vertices.
def expected(p,common):
 if len(common)==0:return False
 if len(common)==1:return p==common[0]
 if len(common)==2:return on_segment(p,*common)
 return point_in_tri(p,common)
def mc(t,d=3):return tuple(Q(t)**i for i in range(1,d+1))
# Distinct families from the supplied Fano stress case.
families={
 'pasch':[(0,1,2),(0,3,4),(1,3,5),(2,4,5)],
 'windmill6':[(0,2*i+1,2*i+2) for i in range(6)],
 'linear_cycle5':[(i,(i+1)%5,5+i) for i in range(5)],
 'disconnected':[(0,1,2),(3,4,5)]}
# The affine plane of order 3 has 9 points and 12 line triples.
affine=[]
for slope in range(3):
 for c in range(3):affine.append(tuple(3*x+(slope*x+c)%3 for x in range(3)))
for x in range(3):affine.append(tuple(3*x+y for y in range(3)))
families['affine_plane3']=affine
geometry=[];rng=random.Random(23088066);eps=Q(1,10**18)
for name,facets in families.items():
 check(all(len(set(f)&set(g))<=1 for f,g in combinations(facets,2)),'linear_test_families')
 verts=sorted(set().union(*map(set,facets)));keys=[('v',v) for v in verts]+[('f',i) for i in range(len(facets))]
 ts=list(range(-len(keys),len(keys),2));rng.shuffle(ts);pos={k:mc(t) for k,t in zip(keys,ts)}
 tris=[]
 for fi,f in enumerate(facets):
  center=pos[('f',fi)]
  for i,j in combinations(f,2):pos[('e',tuple(sorted((i,j))))]=add(center,scale(eps,sub(add(pos[('v',i)],pos[('v',j)]),scale(2,center))))
  for i,j in permutations(f,2):
   kk=(('v',i),('e',tuple(sorted((i,j)))),('f',fi));t=tuple(pos[k] for k in kk);check(any(normal(t)),'subdivision_nondegeneracy');tris.append((kk,t))
 hit=0
 for (ka,a),(kb,b) in combinations(tris,2):
  common=[pos[k] for k in ka if k in kb];pts=intersection_points(a,b)
  check(all(expected(p,common) for p in pts),'subdivision_exact_intersection')
  check(all(p in pts for p in common),'common_faces_present')
  hit+=len(pts)
 for isolated in [mc(2*len(keys)+1),mc(-2*len(keys)-1)]:
  for kk,t in tris:check(not point_in_tri(isolated,t),'isolated_vertex_separation')
 geometry.append({'family':name,'facets':len(facets),'subdivision_triangles':len(tris),'triangle_pairs':comb(len(tris),2),'intersection_candidate_points':hit})
# Mutation: epsilon=0 collapses every edge-barycenter to its facet node.
check(not any(normal((mc(0),mc(1),mc(0)))),'zero_epsilon_degeneracy_detected')
# Exact matrix inverse solver, different from per-six cofactor generation.
def solve(A,b):
 M=[list(map(Q,row))+[Q(v)] for row,v in zip(A,b)];n=len(A)
 for j in range(n):
  k=next((i for i in range(j,n) if M[i][j]),None)
  if k is None:return None
  M[j],M[k]=M[k],M[j];s=M[j][j];M[j]=[x/s for x in M[j]]
  for i in range(n):
   if i!=j:
    s=M[i][j];M[i]=[x-s*y for x,y in zip(M[i],M[j])]
 return [M[i][-1] for i in range(n)]
def det(A):
 A=[list(map(Q,row)) for row in A];r=Q(1)
 for j in range(len(A)):
  k=next((i for i in range(j,len(A)) if A[i][j]),None)
  if k is None:return Q(0)
  if k!=j:A[j],A[k]=A[k],A[j];r=-r
  s=A[j][j];r*=s
  for i in range(j+1,len(A)):
   q=A[i][j]/s
   for k in range(j+1,len(A)):A[i][k]-=q*A[j][k]
 return r
accepted=0;attempts=0;balanced_hist=Counter()
while accepted<40:
 attempts+=1;pts=[tuple(Q(rng.randrange(-12,13)) for _ in range(4)) for _ in range(7)];cols=[(Q(1),)+p for p in pts]
 if any(det([[cols[j][i] for j in s] for i in range(5)])==0 for s in combinations(range(7),5)):continue
 M=[[cols[j][i] for j in range(5)] for i in range(5)]
 u=solve(M,[-x for x in cols[5]])+[Q(1),Q(0)];v=solve(M,[-x for x in cols[6]])+[Q(0),Q(1)]
 check(all(sum(u[j]*cols[j][i] for j in range(7))==sum(v[j]*cols[j][i] for j in range(7))==0 for i in range(5)),'gale_kernel_equations')
 balanced=0
 for j in range(7):
  z=[v[j]*u[k]-u[j]*v[k] for k in range(7)]
  check(sum(x==0 for x in z)==1,'single_zero_per_gale_crossing')
  check(all(sum(z[k]*cols[k][i] for k in range(7))==0 for i in range(5)),'gale_crossing_affine_equations')
  posi=[k for k,x in enumerate(z) if x>0];negi=[k for k,x in enumerate(z) if x<0]
  if len(posi)==len(negi)==3:
   balanced+=1;s=sum(z[k] for k in posi)
   left=tuple(sum(z[k]*pts[k][i] for k in posi)/s for i in range(4));right=tuple(sum(-z[k]*pts[k][i] for k in negi)/s for i in range(4))
   check(left==right,'balanced_crossing_equal_convex_combinations')
 check(balanced>0,'balanced_seven_point_existence');balanced_hist[balanced]+=1;accepted+=1
# Six generic points can have only an unbalanced 1+5 Radon partition.
six=[(Q(0),)*4]+[tuple(Q(i==j) for i in range(4)) for j in range(4)]+[(Q(1,5),)*4]
check(all(det([[(Q(1),)+six[j]][0] for j in s])!=0 for s in combinations(range(6),5)),'six_point_negative_control_general_position')
check(all(sum(six[j][i] for j in range(5))/5==six[5][i] for i in range(4)),'six_point_unbalanced_radon_control')
# Exhaust all witness graphs on five independent triangle variables. Exact
# probabilities and moments test ordered overlap + diagonal conventions.
edges=list(combinations(range(5),2));q=Q(1,3);mass={mask:q**mask.bit_count()*(1-q)**(5-mask.bit_count()) for mask in range(32)}
adaptive_strict=0
for gm in range(1,1<<len(edges)):
 E=[e for k,e in enumerate(edges) if (gm>>k)&1];degrees=Counter(x for e in E for x in e);ordered=sum(d*(d-1) for d in degrees.values());mu=len(E)*q*q;delta=ordered*q**3
 mean=second=p0=fixed=adaptive=Q(0)
 for mask in range(32):
  present=[e for e in E if all((mask>>x)&1 for x in e)];z=len(present);pr=mass[mask];mean+=z*pr;second+=z*z*pr
  if not present:p0+=pr
  if all(0 in e for e in present):fixed+=pr
  if not present or set.intersection(*(set(e) for e in present)):adaptive+=pr
 check(mean==mu,'exhaustive_witness_graph_mean')
 check(second==mu+delta+(len(E)*(len(E)-1)-ordered)*q**4,'exhaustive_ordered_overlap_second_moment')
 rate=mu*mu/(2*(mu+delta));exp_lower=sum((-rate)**k/Q(factorial(k)) for k in range(10))
 check(p0<=exp_lower,'janson_small_graph_lower_taylor_control')
 check(fixed<=adaptive,'adaptive_vs_fixed_deletion')
 if fixed<adaptive:adaptive_strict+=1
check(adaptive_strict>0,'adaptive_deletion_negative_control')
# Independent exact n=2^(4k), m=2^(5k), p=2^(-6k) parameter scan.
valid=[]
for k in range(1,65):
 n=1<<(4*k);m=1<<(5*k);p=Q(1,1<<(6*k));M=comb(n,3);W=Q(comb(n,6),7)-m*M
 if W<=0:continue
 den=Q(M*M,2)*p*p+M**3*p**3;rate=(W*p*p)**2/(2*den);entropy=m+4*k*(20*n+3*m);net=rate-entropy
 lam=M*p;conf=comb(n,2)*comb(n-2,2)*p*p
 if net>0 and Q(1,1+net)+conf/m+4/lam<1 and lam/2-m>n:valid.append(k)
check(64 in valid,'finite_parameters_positive_joint_probability')
n=1<<256;m=1<<320;p=Q(1,1<<384);M=comb(n,3);c=Q(1,645120);a=c*c/2
for name,predicate in {
 'robust_pair_constant':Q(comb(n,6),7)-m*M>=c*n**6,
 'displayed_negative_exponent':a*(1<<384)>(1<<343),
 'displayed_entropy_bound':m+256*(20*n+3*m)<(1<<331),
 'displayed_net_exponent':(1<<343)-(1<<331)>(1<<342),
 'displayed_retained_count':M*p/2-m>n,
 'displayed_combined_failures':Q(1,8)+Q(1,1<<66)+Q(1,1<<377)<1,
 'degree_sum_after_cleanup':3*(n+1)>3*n,
 'wrong_dimension_four_not_general_upper':6>4+1,
}.items():check(predicate,name)
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':sum(counts.values()),'families':dict(counts),'geometry_method':'Exact plane/segment intersections and coplanar 2D orientations, not supplied basic-feasible-solution enumeration','geometry':geometry,'epsilon':str(eps),'gale_generic_seven_sets':accepted,'gale_attempts':attempts,'gale_balanced_crossing_histogram':dict(balanced_hist),'witness_graphs_exhausted':1023,'adaptive_strict_graphs':adaptive_strict,'power_parameter_scan':{'first_certified_k':min(valid),'tested_through':64,'not_a_minimal_witness_claim':True},'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':round(time.monotonic()-start,3),'limits':'Finite exact controls supplement the universal proof and primary imports. No huge witness facet list, formal verification or novelty certification.'}
Path(__file__).with_name('independent_controls_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
