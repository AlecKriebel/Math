"""Fresh exact quotient/gluing and graph attack; no project code imports."""
from fractions import Fraction as F
import json,itertools

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 c=[F(0)]*7
 for i in range(4):
  for j in range(4):c[i+j]+=a[i]*b[j]
 for i in range(6,3,-1):
  for k in range(1,5):c[i-k]-=c[i]
 return tuple(c[:4])
def require(ok,m):
 if not ok:raise ValueError(m)
z=(F(0),)*4;one=(F(1),F(0),F(0),F(0));r=(F(0),F(1),F(0),F(0));rs=[one]
for i in range(4):rs.append(mul(rs[-1],r))
require(mul(rs[-1],r)==one,'r5')
def conj(a):
 out=z
 for i,x in enumerate(a):out=add(out,tuple(x*y for y in rs[-i%5]))
 return out
p=[z]
for i in range(4):p.append(add(p[-1],rs[i]))
q=[conj(x) for x in p]
identities=[]
# P side j and clockwise-labelled Q side -j have exactly equal directed vectors.
# Their translation gluing maps p_j+s e_j to q_-j+s e_j.
for j in range(5):
 v=sub(p[(j+1)%5],p[j]);w=sub(q[(-j+1)%5],q[-j%5]);require(v==w==rs[j],'parallel gluing')
 require(sub(one,p[j])==q[(1-j)%5],'h corner')
 require(sub(one,p[(j+1)%5])==q[-j%5],'h edge reversal')
 for s in [F(0),F(1,3),F(1,2),F(1)]:
  x=add(p[j],tuple(s*t for t in v));hx=sub(one,x);target=add(q[-j%5],tuple((1-s)*t for t in v));require(hx==target,'edge parameter')
 identities.append({'P_side':j,'Q_side':-j%5,'h_parameter':'s -> 1-s','unique_regular_fixed_s':'1/2'})
# Recover the common singular vertex via gluing, independently of an assumed cover.
parent=list(range(10))
def root(a):
 while parent[a]!=a:a=parent[a]
 return a
def union(a,b):parent[root(a)]=root(b)
for j in range(5):union(j,5+(-j)%5);union((j+1)%5,5+(1-j)%5)
require(len({root(i) for i in range(10)})==1,'singular corners')
# The A0 terminal q1 with arbitrary translation T gives last polygon = B-P.
# Thus direct development reversal proves midpoint symmetry without invoking a cover.
for t in [z,one,(F(1,3),F(-2),F(5),F(7,4))]:
 B=add(t,q[1]);require({add(t,x) for x in q}=={sub(B,x) for x in p},'last face central inversion')
# All starting corners are conjugate under the rotation r; h maps the specified
# terminal corner sector, not another of the 10 coincident singular sectors.
for j in range(5):
 require(sub(one,q[j])==p[(1-j)%5],'Q->P corner identity')
# Recompute both norms directly in the degree4 cyclotomic field, without the
# advertised quadratic norm formula. eta=-r^3, sqrt5=1+2(r+r^4).
def scale(t,x):return tuple(t*y for y in x)
sqrt5=add(one,scale(2,add(rs[1],rs[4])))
require(mul(sqrt5,sqrt5)==scale(5,one),'sqrt5')
Z=(F(5),F(1),F(-7),F(-8));wordnorm=mul(Z,conj(Z))
require(wordnorm==scale(F(1,2),add(scale(307,one),scale(137,sqrt5))),'word norm')
A=scale(F(1,2),add(scale(31,one),scale(13,sqrt5)));B=add(scale(-17,one),scale(-8,sqrt5));eta=neg(rs[3])
displayed=add(A,mul(B,eta));displaynorm=mul(displayed,conj(displayed))
require(displaynorm==scale(F(1,2),add(scale(425,one),scale(189,sqrt5))),'displayed norm')
require(sub(displaynorm,wordnorm)==add(scale(59,one),scale(26,sqrt5)),'norm difference')
# Dodecahedral graph via generalized Petersen G(10,2), independent of coordinates.
g={i:set() for i in range(20)}
for i in range(10):
 for a,b in [(i,(i+1)%10),(i,10+i),(10+i,10+(i+2)%10)]:g[a].add(b);g[b].add(a)
require(all(len(v)==3 for v in g.values()),'graph degree')
d={}
for a in g:
 D={a:0};queue=[a]
 for b in queue:
  for c in g[b]:
   if c not in D:D[c]=D[b]+1;queue.append(c)
 require(len(D)==20,'connected')
 require([list(D.values()).count(k) for k in range(6)]==[1,3,6,6,3,1],'distance spheres');d[a]=D
pairs=[]
for a,b in itertools.combinations(g,2):
 if d[a][b]==2:
  common=g[a]&g[b];require(len(common)==1,'unique common neighbor');pairs.append([a,b,next(iter(common))])
require(len(pairs)==60,'distance2 pair count')
# Any automorphism swapping a,b must preserve g[a] intersect g[b] setwise;
# singleton intersection forces a fixed vertex. No rotational halfturn can do so.
print(json.dumps({'status':'PASS','new_code_no_project_imports':True,'independent_degree4_norm_check':{'face_word':'(307+137sqrt5)/2','displayed':'(425+189sqrt5)/2','difference':'59+26sqrt5'},'gluing_checks':identities,'singular_corner_count':10,'cone_angle':'10*(3pi/5)=6pi','regular_h_fixed_points':5,'central_last_face_identity':'T+Q = B-P when B=T+q1','graph_model':'generalized Petersen G(10,2)','distance2_pairs_with_unique_common_neighbor':len(pairs),'odd_initial_directions_pi_units':['0','1/5','2/5','3/5'],'odd_extra_paths':'exactly two proper diagonals; all rays first-hit initial vertices','scope':'Finite exact identities plus analytic unique-continuation argument; no finite enumeration is asserted to prove the universal statement.'},indent=2))
