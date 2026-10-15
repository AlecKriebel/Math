#!/usr/bin/env python3
"""Reviewer-authored exact checks; no author/external program imported.
Coordinates are four rational coefficients modulo Phi_5, not the author's
quadratic-complex representation. Faces and crossing parameters are literal
mathematical input from the conflicting certificate.
"""
from fractions import Fraction as F
from collections import Counter, deque
import hashlib, json
from pathlib import Path

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def scale(a,c): return tuple(x*c for x in a)
def mul(a,b):
    q=[F(0)]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):q[i+j]+=x*y
    for i in range(6,3,-1):
        for j in range(1,5):q[i-j]-=q[i]
    return tuple(q[:4])
zero=(F(0),)*4;one=(F(1),F(0),F(0),F(0));r=(F(0),F(1),F(0),F(0))
rp=[one]
for _ in range(5):rp.append(mul(rp[-1],r))
assert rp[5]==one

def conj(a):
    z=zero
    for i,c in enumerate(a):z=add(z,scale(rp[(-i)%5],c))
    return z
S=(-F(1),F(0),-F(2),-F(2)) # sqrt(5) = 1 + 2(r+r^-1)
assert mul(S,S)==scale(one,5)
def quadratic(a,b=0): return add(scale(one,F(a)),scale(S,F(b)))
def qsign(a,b):
    if not b:return (a>0)-(a<0)
    if not a:return (b>0)-(b<0)
    if a*b>0:return (a>0)-(a<0)
    z=a*a-5*b*b
    return ((z>0)-(z<0))*((a>0)-(a<0))
def imsign(z):
    # Im(z)/sin(72deg) = z1 + (z2-z3)(sqrt5-1)/2.
    d=z[2]-z[3]
    return qsign(z[1]-d/2,d/2)
def crosssign(u,v):return imsign(mul(conj(u),v))

def polygon(cycle,a,b,pa,pb):
    i=cycle.index(a);assert cycle[(i+1)%5]==b
    z=pa;e=sub(pb,pa);d={a:pa}
    for k in range(1,5):
        z=add(z,e);d[cycle[(i+k)%5]]=z;e=mul(e,r)
    assert add(z,e)==pa
    return d
faces=[[6,18,4,8,10],[10,8,0,16,2],[17,16,0,12,1],[3,13,2,16,17],[5,9,1,12,14],[14,12,0,8,4],[5,14,4,18,19],[3,17,1,9,11],[11,9,5,19,7],[6,10,2,13,15],[19,18,6,15,7],[15,13,3,11,7]]
word=[1,3,11,8,6,5,1,3,11,10,8,6,4,5,2,1]
edges=[(2,16),(3,13),(7,11),(5,19),(4,14),(0,8),(2,16),(3,13),(7,15),(7,19),(5,19),(5,14),(12,14),(0,12),(0,16)]
# t=(a+b sqrt5), s=(c+d sqrt5), from the printed external certificate.
params=[('-1/2','1/4','5/8','1/8'),('7/2','-3/2','-2','1'),('-5/8','3/8','3/8','1/8'),('7','-3','-4','2'),('-3/4','1/2','1/8','1/8'),('21/2','-9/2','-6','3'),('-7/8','5/8','-1/8','1/8'),('14','-6','-8','4'),('-15/11','10/11','-3/11','2/11'),('-2','6/5','-1/2','3/10'),('-17/22','15/22','1/22','3/22'),('-1','4/5','0','1/5'),('-2/11','5/11','4/11','1/11'),('0','2/5','1/2','-1/10'),('9/22','5/22','7/22','-1/22')]
ps=[polygon(faces[1],0,16,zero,one)]
labels=[{v:i for i,v in enumerate([0,16,2,10,8])}]
for k,f in enumerate(word[1:],1):
    a,b=edges[k-1];cy=faces[f]
    assert set(cy)&set(faces[word[k-1]])=={a,b}
    if cy[(cy.index(a)+1)%5]!=b:a,b=b,a
    ps.append(polygon(cy,a,b,ps[-1][a],ps[-1][b]))
    # Label transport is purely combinatorial: physical cyclic orientation
    # stays CCW; reflected billiard labels alternate orientation each face.
    i=cy.index(a);sgn=(-1)**k
    lab={cy[(i+j)%5]:(labels[-1][a]+sgn*j)%5 for j in range(5)}
    assert lab[b]==labels[-1][b];labels.append(lab)
W=ps[-1][2]
assert mul(W,conj(W))==quadratic(F(307,2),F(137,2))
assert W==add(quadratic(8,4),mul(quadratic(F(1,2),F(1,2)),r))
cuts=[zero];last=(F(0),F(0));strict=0
for i,(a,b,c,d) in enumerate(params):
    a,b,c,d=map(F,(a,b,c,d));t=quadratic(a,b);s=quadratic(c,d)
    assert qsign(a,b)>0 and qsign(1-a,-b)>0
    assert qsign(c,d)>0 and qsign(1-c,-d)>0
    assert qsign(a-last[0],b-last[1])>0
    u,v=edges[i]
    assert mul(t,W)==add(ps[i][u],mul(s,sub(ps[i][v],ps[i][u])))
    cuts.append(t);last=(a,b);strict+=1
cuts.append(one)
collinear=[]
for i,p in enumerate(ps):
    midpoint=mul(W,scale(add(cuts[i],cuts[i+1]),F(1,2)))
    cy=faces[word[i]]
    for a,b in zip(cy,cy[1:]+cy[:1]):assert crosssign(sub(p[b],p[a]),sub(midpoint,p[a]))>0
    for v,z in p.items():
        if crosssign(W,z)==0:collinear.append((i,v))
assert collinear==[(0,0),(15,2)]
assert labels[-1]=={0:3,16:2,2:1,10:0,8:4}
source_ray=sub(ps[-1][16],W);physical_ray=sub(ps[-1][10],W)
assert source_ray==rp[3] and physical_ray==neg(rp[4])
assert crosssign(one,W)>0 and crosssign(W,neg(rp[3]))>0
# Therefore 0<alpha<36deg; source reverse-tangent sector is 36deg-alpha.
# Fig8 has pi-beta in that sector, so beta-alpha=144deg, type A1.
graph={i:set() for i in range(20)}
for cy in faces:
    for a,b in zip(cy,cy[1:]+cy[:1]):graph[a].add(b);graph[b].add(a)
assert len({tuple(sorted((a,b))) for a in graph for b in graph[a]})==30
assert all(len(g)==3 for g in graph.values())
assert all(len(graph[a]&graph[b])<=1 for a in graph for b in graph if a!=b) # no4cycles
assert 2 not in graph[0] and graph[0]&graph[2]=={16}

# Independent purely graph-theoretic control: G(10,2), the dodecahedral graph.
# This is a consistency check, not needed for the unique-common-neighbor proof.
V=[(t,i) for t in 'uv' for i in range(10)];gp={x:set() for x in V}
for i in range(10):
    for a,b in [(('u',i),('u',(i+1)%10)),(('u',i),('v',i)),(('v',i),('v',(i+2)%10))]:gp[a].add(b);gp[b].add(a)
tau=lambda x:(x[0],(1-x[1])%10)
assert all(tau(x)!=x and tau(tau(x))==x and {tau(y) for y in gp[x]}==gp[tau(x)] for x in V)
hist=Counter()
for x in V:
    d={x:0};todo=deque([x])
    while todo:
        a=todo.popleft()
        for b in gp[a]:
            if b not in d:d[b]=d[a]+1;todo.append(b)
    hist[d[tau(x)]]+=1
assert hist==Counter({1:4,3:8,4:4,5:4})

# Literal-shortcut counterexample: p0->p2, no crossings, N=1.
# ray angles 0,36,144,216deg give alpha36, terminal interior72,beta108.
# Hence beta-alpha72 but parity-aware typeA2, endpoints distance2.
P=ps[0]
assert sub(P[10],P[2])==rp[2] and graph[0]&graph[2]=={16}

frozen={n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in ['CANDIDATE_PROOF.md','EXTERNAL_CERTIFICATE_AUDIT.md','check_certificate.py','check_half_turn.py']}
result={'exact_arithmetic':'Q[z]/(z^4+z^3+z^2+z+1), independent reviewer implementation','external_witness':{'strict_crossings':strict,'all_face_subsegments_inside':True,'collinear_vertex_occurrences':collinear,'graph_distance':2,'squared_length':'(307+137 sqrt5)/2','terminal_billiard_labels':labels[-1],'terminal_source_ray':'z^3','terminal_physical_outgoing_ray':'-z^4','alpha_range_degrees':[0,36],'source_beta_minus_alpha_degrees':144,'source_type':'A1'},'dodecahedral_graph':{'no_four_cycles':True,'distance_two_common_neighbor_unique':True,'independent_G10_2_histogram':dict(hist)},'literal_shorthand_control':{'path':'one pentagon diagonal p0->p2','face_occurrences':1,'alpha_degrees':36,'beta_degrees':108,'beta_minus_alpha_degrees':72,'graph_distance':2,'parity_aware_source_type':'A2'},'frozen_input_sha256':frozen}
print(json.dumps(result,indent=2))
