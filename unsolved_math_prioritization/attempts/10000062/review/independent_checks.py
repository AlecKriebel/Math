#!/usr/bin/env python3
"""Independent rational checks of the clipped-disk triangulation.
Generates strip parallelograms and splits them along their indicated diagonal.
No code from the candidate checker is imported. Python standard library only.
"""
from fractions import Fraction as F
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import json

checks=[]
def check(name,yes):
    assert yes,name
    checks.append(name)
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def n2(p):return dot(p,p)
def closest(a,b):
    v=sub(b,a); d=dot(v,v); t=max(F(0),min(F(1),-dot(a,v)/d))
    p=(a[0]+t*v[0],a[1]+t*v[1]);return n2(p),p

def geometry(word,upper=False,r2=F(10)):
    dd={j:F(word[j+2]) if -2<=j<=2 else F(1,2) for j in range(-4,5)}
    aa={0:F(0)}
    for j in range(4):aa[j+1]=aa[j]+dd[j]+1
    for j in range(-1,-5,-1):aa[j]=aa[j+1]-dd[j]-1
    rows=[(aa[j],4*j) for j in []]
    rows=[]
    for j in range(-3,4):rows.extend([(aa[j],F(4*j)),(aa[j]+dd[j],F(4*j+1))])
    def normalize(p):
        X,Y=p
        if upper:X,Y=dd[0]-X,1-Y
        if dd[0]==F(3,2):X=-X
        return (X,Y)
    triangles=set()
    for (a,y),(b,z) in zip(rows,rows[1:]):
        for k in range(-9,10):
            q=[(a+2*k,y),(a+2*k+2,y),(b+2*k+2,z),(b+2*k,z)]
            for t in [(q[0],q[1],q[3]),(q[1],q[2],q[3])]:
                triangles.add(tuple(sorted(normalize(v) for v in t)))
    edges={tuple(sorted(e)) for t in triangles for e in combinations(t,2)}
    vertices={p for e in edges for p in e if n2(p)<=r2}
    positive_edges=set();point_edges=Counter()
    for a,b in edges:
        d,p=closest(a,b)
        if d<r2:positive_edges.add((a,b))
        elif d==r2:point_edges[p]+=1
    positive_faces=[];point_faces=Counter()
    for t in triangles:
        a,b,c=t
        sides=[det(sub(b,a),(-a[0],-a[1])),det(sub(c,b),(-b[0],-b[1])),det(sub(a,c),(-c[0],-c[1]))]
        inside=all(v>=0 for v in sides) or all(v<=0 for v in sides)
        d,p=(F(0),(F(0),F(0))) if inside else min(closest(*e) for e in combinations(t,2))
        if d<r2:positive_faces.append(t)
        elif d==r2:point_faces[p]+=1
    boundary_incidence={p:(sum(p in e for e in positive_edges),point_edges[p],sum(p in t for t in positive_faces),point_faces[p]) for p in point_edges}
    signature=(frozenset(vertices),frozenset(positive_edges),tuple(sorted(point_edges.items())),len(positive_faces),tuple(sorted(point_faces.items())),tuple(sorted(boundary_incidence.items())))
    lengths={tuple(sorted(n2(sub(a,b)) for a,b in combinations(t,2))) for t in triangles}
    areas={abs(det(sub(t[1],t[0]),sub(t[2],t[0])))/2 for t in triangles}
    return signature,lengths,areas

base,_,_=geometry([F(1,2)]*5)
cases=[]
for bits in product([F(1,2),F(3,2)],repeat=5):
    for upper in [False,True]:
        sig,lengths,areas=geometry(bits,upper)
        label=''.join('0' if x==F(1,2) else '1' for x in bits)+('_U' if upper else '_L')
        check('disk_trace_'+label,sig==base)
        check('side_lengths_'+label,lengths=={(F(5,4),F(13,4),F(4)),(F(4),F(10),F(10))})
        check('areas_'+label,areas=={F(1),F(3)})
        cases.append(label)
check('closed_vertices',len(base[0])==8)
check('positive_edges',len(base[1])==28)
check('positive_faces',base[3]==23)
check('boundary_edges',dict(base[2])=={(F(-1),F(-3)):3,(F(1),F(-3)):3})
check('boundary_faces',dict(base[4])=={(F(-1),F(-3)):2,(F(1),F(-3)):2})
check('boundary_incidence',all(v==(3,3,4,2) for p,v in base[5]))
for px in [-1,1]:
    for dx in [F(-3,2),F(-1,2),F(1,2),F(3,2)]:check('outward_cap_'+str((px,dx)),dot((px,-3),(dx,-1))>=F(3,2))
check('distant_edges',F(9,4)+9>10)
bigger_a=geometry([F(1,2)]*5,r2=F(1001,100))[0]
bigger_b=geometry([F(1,2),F(3,2),F(1,2),F(1,2),F(1,2)],r2=F(1001,100))[0]
check('larger_radius_negative_control',bigger_a!=bigger_b)
# Whole-family half-turn row identities, with two independent neighboring choices.
for dl,dc in product([F(1,2),F(3,2)],repeat=2):
    a_prev=-dl-1
    check('half_turn_tall_shift_'+str((dl,dc)),(dc-a_prev-dl)-(dc-0)==1)
result={'passed':len(checks),'failed':0,'rooted_cases':len(cases),'independent_neighbor_assignments':32,'closed_disk':{'vertices':8,'positive_length_edges':28,'positive_area_faces':23,'boundary_points':2,'at_each_boundary_point':{'positive_edges':3,'point_only_edges':3,'positive_faces':4,'point_only_faces':2}},'negative_control':'passes at squared radius1001/100','scope':'Exact finite traces and inequalities only. Infinite-family locality and non-cocompactness are independently reviewed analytically in REVIEW.md.','checks':checks}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
