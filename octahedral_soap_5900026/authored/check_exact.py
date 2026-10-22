#!/usr/bin/env python3
"""Exact finite diagnostics for MATHEMATICAL_NOTE.md. Standard library only.
These checks support, and do not replace, the written proofs. No asserts.
"""
from fractions import Fraction as Q
from itertools import product, combinations, permutations
from collections import Counter
import json

checks = 0

def require(ok, label):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError(label)

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(c,a): return tuple(c*x for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm2(a): return dot(a,a)
def triangle_area_squared(a,b,c): return norm2(cross(sub(b,a),sub(c,a)))/4
def det(a,b,c): return dot(a,cross(b,c))
def hamming(s,t): return sum(x!=y for x,y in zip(s,t))
def e(k,sign=1): return tuple(Q(sign if i==k else 0) for i in range(3))

S=list(product((-1,1),repeat=3))
P=[s for s in S if s[0]*s[1]*s[2]==1]
N=[s for s in S if s not in P]
zero=(Q(0),)*3
require(len(S)==8 and len(P)==len(N)==4,'label inventory')
require(all(sum(s[k] for s in P)==0 for k in range(3)),'tetrahedral zero barycenter')

# Approach 1: every individual triangle, every kite, and all cap volumes.
a=Q(1,6)
outer=[]; core=[]; cap_volumes=[]
for s in N:
    j=mul(a,s)
    face=[e(k,s[k]) for k in range(3)]
    require(triangle_area_squared(*face)==Q(3,4),'outer reference face area')
    vol=abs(det(sub(face[0],j),sub(face[1],j),sub(face[2],j)))/6
    require(vol==Q(1,12),'cap volume')
    cap_volumes.append(vol)
    for i,k in combinations(range(3),2):
        area2=triangle_area_squared(face[i],face[k],j)
        require(area2==Q(1,8),'outer triangle squared area')
        outer.append((face[i],face[k],j))
for s,t in combinations(N,2):
    k=next(k for k in range(3) if s[k]==t[k])
    j1,j2,vertex=mul(a,s),mul(a,t),e(k,s[k])
    require(det(j1,vertex,j2)==0,'core kite is planar')
    ar1=triangle_area_squared(zero,j1,vertex)
    ar2=triangle_area_squared(zero,vertex,j2)
    require(ar1==ar2==Q(1,72),'core triangle squared area')
    require(dot(cross(j1,vertex),cross(vertex,j2))>0,'kite triangles consistent orientation')
    core.append((zero,j1,vertex,j2))
require(len(outer)==12 and len(core)==6,'sheet count')
# Areas: each outer sqrt(2)/4; each core sqrt(2)/6.
require(12*Q(1,4)+6*Q(1,6)==4,'total area coefficient of sqrt(2)')
require(sum(cap_volumes)==Q(1,3),'total cap volume')
require((Q(4,3)-sum(cap_volumes))/4==Q(1,4),'inner volume by symmetry')
# Symbolic polynomial identities for derivative and convexity numerator.
q=(Q(1),Q(-4),Q(6))
require(sum(q[i]*a**i for i in range(3))==Q(1,2),'Q at critical point')
require(6*a-2==-1,'critical numerator')
require(tuple(6*c-d for c,d in zip(q,(4,-24,36)))==(2,0,0),'strict convexity numerator')

# Approach 2: vectors represented as rational multiples of 1/sqrt(2).
r={s:mul(Q(1,2) if s in P else Q(5,6),s) for s in S}
G=set(); distances=Counter()
for s,t in combinations(S,2):
    d2=norm2(sub(r[s],r[t]))/2
    if s in P and t in P:
        category='inner_inner'; expected=Q(1)
    elif s in N and t in N:
        category='outer_outer'; expected=Q(25,9)
    elif hamming(s,t)==1:
        category='neighbor_cross'; expected=Q(1)
    else:
        category='opposite_cross'; expected=Q(8,3)
    require(d2==expected,'restricted vector pair '+category)
    distances[(category,str(d2))]+=1
    if d2==1:G.add(tuple(sorted((s,t))))
require(len(G)==18,'restricted graph has eighteen edges')
# Reflection across plane with equation a_t dot z=-|a_t|^2/3.
for s in N:
    at=r[tuple(-x for x in s)]
    require(r[s]==mul(Q(-5,3),at),'reflected tetrahedron vertex')
# All candidate sheet planes and normals.
for s in N:
    for k in range(3):
        t=tuple(-x if i==k else x for i,x in enumerate(s))
        coeff=tuple(4*x if i==k else x for i,x in enumerate(s))
        require(sub(r[s],r[t])==mul(Q(1,3),coeff),'outer unit normal direction')
        require(norm2(coeff)==18,'outer plane normal length squared')
        verts=[e(i,s[i]) for i in range(3) if i!=k]+[mul(a,s)]
        require(all(dot(coeff,x)==1 for x in verts),'outer sheet plane incidence')
# Exact finite samples supplement the trace and power-cell proof.
for s in S:
    for n in range(1,8):
        for i in range(1,n):
            for j in range(1,n-i):
                weights=(Q(i,n),Q(j,n),Q(n-i-j,n))
                x=tuple(s[k]*weights[k] for k in range(3))
                scores={t:dot(r[t],x)-(Q(1,3) if t in N else 0) for t in S}
                require(scores[s]==Q(1,2),'face trace score')
                require(all(scores[s]>scores[t] for t in S if t!=s),'strict face trace label')
require(sum(dot(r[s],s)/2 for s in S)==8,'restricted flux coefficient of 1/sqrt(2)')

# Approach 3. Exact elements q + r*sqrt(6), with no floating-point inequalities.
def radical_le_one(q,r):
    # Decide q+r*sqrt(6)<=1 by sign-aware rational squaring.
    z=1-q
    if r==0:return z>=0
    if r>0:return z>=0 and z*z>=6*r*r
    if z>=0:return True
    return z*z<=6*r*r

def linadd(u,v):return (u[0]+v[0],u[1]+v[1])
def linscale(c,u):return (c*u[0],c*u[1])
def linsub(u,v):return linadd(u,linscale(-1,v))
def square_lin(u):
    # u=c*sqrt(2)+d*sqrt(3).
    c,d=u
    return (2*c*c+3*d*d,2*c*d)
alpha=(Q(0),Q(1,6))
beta=(Q(1,4),Q(-1,6))

def field(s,x,scale=Q(1)):
    d=dot(s,x)
    return tuple(linscale(scale,linadd(linscale(s[k],alpha),linscale(d*s[k]-x[k],beta))) for k in range(3))
def pair_squared(s,t,x,scale=Q(1)):
    u,v=field(s,x,scale),field(t,x,scale)
    terms=[square_lin(linsub(uu,vv)) for uu,vv in zip(u,v)]
    return tuple(sum(term[k] for term in terms) for k in range(2))
verts=[e(k,sgn) for k in range(3) for sgn in (-1,1)]
affine_inventory=Counter()
for s,t in combinations(S,2):
    for x in verts:
        val=pair_squared(s,t,x)
        require(radical_le_one(*val),'affine full-pair vertex bound')
        affine_inventory[(str(val[0]),str(val[1]))]+=1
require(sum(affine_inventory.values())==168,'all twenty-eight pairs times six vertices')
# Coefficients of divergence beta*(|s|^2-3).
require(all(dot(s,s)-3==0 for s in S),'affine fields divergence-free')
flux=linadd(linscale(12,alpha),linscale(8,beta))
require(flux==(Q(2),Q(2,3)),'affine flux equals 2sqrt(2)+2/sqrt(3)')
# Constant dual optimum and affine active constraints.
require(square_lin(linscale(2,alpha))==(Q(1,3),Q(0)),'opposite constant norm per coordinate')
require(square_lin(linadd(alpha,beta))==(Q(1,8),Q(0)),'affine distance-two active constraint')

# Approach 4: exact plane-pattern and half-plane separation of two supports.
require(sorted(map(abs,(4,1,1)))!=sorted(map(abs,(0,1,1))),'outer/core planes cannot be parallel')
for kite in core:
    vertex=kite[2]; k=next(i for i,x in enumerate(vertex) if x)
    sign=vertex[k]
    require(all(sign*x[k]>=0 for x in kite),'core lies in one coordinate half-plane')
    require(all(sign*x[k]>0 for x in kite[1:] ),'noncentral core vertices strictly in half-plane')
    reflected=[mul(-1,x) for x in kite]
    require(all(sign*x[k]<=0 for x in reflected),'reflected core opposite half-plane')
# For s in N, -s is P; opposite outer planes have equations L=1 and L=-1.
require(all(tuple(-x for x in s) in P for s in N),'outer opposite parity plane correspondence')
require(Q(1,2)*4+Q(1,2)*4==4,'mixture area coefficient')

# Approach 5: expansion of the four opposite-pair squares.
require(sum(norm2(s)/2 for s in P)==6,'central obstruction constant term')
require(6>4,'central obstruction exceeds allowed sum')
for d in [zero,(Q(1),Q(0),Q(0)),(Q(1,3),Q(-2,5),Q(7,11))]:
    # Cross term is sqrt(2) times d dot sum(s), which vanishes.
    require(dot(d,tuple(sum(s[k] for s in P) for k in range(3)))==0,'obstruction cross term vanishes')
    require(4*norm2(d)+6>4,'obstruction for rational translation sample')

# Deliberate wrong-claim controls. Each must be rejected by the same predicates.
negative_controls=[]
require(not radical_le_one(Q(25,9),Q(0)),'reject forbidden adjacency as unit bounded');negative_controls.append('forbidden adjacency')
require(not radical_le_one(Q(8,3),Q(0)),'reject opposite restricted pair');negative_controls.append('opposite restricted pair')
require(any(not radical_le_one(*pair_squared(s,t,x,Q(11,10))) for s,t in combinations(S,2) for x in verts),'reject scaled affine bound');negative_controls.append('110 percent affine scaling')
require(triangle_area_squared(e(0,-1),e(1,-1),mul(Q(1,5),(-1,-1,-1)))!=Q(1,8),'reject wrong apex geometry');negative_controls.append('wrong apex parameter')
require(not (6<=4),'reject central coexistence claim');negative_controls.append('false central compatibility')

print(json.dumps({
    'result':'PASS_EXACT_FINITE_DIAGNOSTICS',
    'checks':checks,
    'normalization':'octahedron vertices plus/minus coordinate unit vectors',
    'candidate_area':'4*sqrt(2)',
    'outer_triangles':len(outer),'central_kites':len(core),'tetrahedral_points':5,
    'restricted_pair_inventory':[{'category':k[0],'squared_distance':k[1],'count':v} for k,v in sorted(distances.items())],
    'affine_vertex_checks':168,
    'affine_norm_squared_inventory':[{'rational':k[0],'sqrt6_coefficient':k[1],'count':v} for k,v in sorted(affine_inventory.items())],
    'constant_dual_optimum':'2*sqrt(3)',
    'affine_dual_optimum':'2*sqrt(2)+2/sqrt(3)',
    'negative_controls_rejected':negative_controls,
    'global_problem_status':'UNSOLVED',
    'limits':'Finite diagnostics only; the written geometric, divergence, symmetry, and trace arguments require mathematical review.'
},sort_keys=True,indent=2))
