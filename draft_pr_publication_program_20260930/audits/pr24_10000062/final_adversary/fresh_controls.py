#!/usr/bin/env python3
"""Independent exact acceptance controls, without imports from other reviewers.

Full restriction graphs use clipped segment geometry rather than exterior
endpoints. Ambiguous singleton cells are matched by exhaustive graph bijection.
The materially new mechanism exhausts all rooted ambient isometries from the
unique shortest incident edge, and tests an incidence-preserving-count mutation.
"""
from fractions import Fraction as F
from itertools import combinations, product, permutations
from collections import defaultdict, Counter
from math import gcd, lcm
from pathlib import Path
import json, hashlib

HERE = Path(__file__).resolve().parent
CHECKS = []
ORIGIN = (F(0), F(0))

def require(name, value):
    if not value:
        raise AssertionError(name)
    CHECKS.append(name)

def sub(a,b): return (a[0]-b[0], a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def n2(a): return dot(a,a)

def mesh(word, upper=False, rootj=0, rootk=0, guard=4):
    def delta(j): return word.get(j,F(1,2) if j%3 else F(3,2))
    a={0:F(0)}
    for j in range(max(0,rootj+guard+2)): a[j+1]=a[j]+delta(j)+1
    for j in range(-1,min(0,rootj-guard-2)-1,-1): a[j]=a[j+1]-delta(j)-1
    root=(a[rootj]+2*rootk+(delta(rootj) if upper else 0),F(4*rootj+int(upper)))
    faces=set()
    for j in range(rootj-guard,rootj+guard+1):
        for k in range(rootk-20,rootk+21):
            l=(a[j]+2*k,F(4*j)); u=(a[j]+delta(j)+2*k,F(4*j+1)); z=(a[j+1]+2*k,F(4*j+4))
            for t in [(l,(l[0]+2,l[1]),u),((u[0]-2,u[1]),u,l),
                      (u,(u[0]+2,u[1]),z),((z[0]-2,z[1]),z,u)]:
                faces.add(tuple(sorted(sub(p,root) for p in t)))
    return faces

def nearest(e):
    a,b=e; v=sub(b,a)
    q=max(F(0),min(F(1),-dot(a,v)/n2(v)))
    p=(a[0]+q*v[0],a[1]+q*v[1])
    return n2(p),p

def line(a,b,witness=None):
    v=sub(b,a); z=(-v[1],v[0],v[1]*a[0]-v[0]*a[1])
    if witness is not None:
        if z[0]*witness[0]+z[1]*witness[1]+z[2]<0: z=tuple(-x for x in z)
    elif next(x for x in z if x)!=abs(next(x for x in z if x)):
        z=tuple(-x for x in z)
    multiple=lcm(*(v.denominator for v in z)); z=tuple(int(v*multiple) for v in z)
    divisor=gcd(*z)
    return tuple(v//divisor for v in z)

def segment_geometry(e,r2):
    inside=tuple(p for p in e if n2(p)<=r2)
    direction=0
    if len(inside)==1:
        other=next(p for p in e if p!=inside[0]); v=sub(other,inside[0])
        first=next(x for x in v if x); direction=1 if first>0 else -1
    return ('segment',line(*e),inside,direction)

def restriction(faces,r2=F(10)):
    es={tuple(sorted(e)) for t in faces for e in combinations(t,2)}
    nodes={}; incidence=set()
    for p in {v for e in es for v in e}:
        if n2(p)<=r2: nodes[(0,p)]=('vertex',p)
    for e in es:
        d,p=nearest(e)
        if d<r2: nodes[(1,e)]=segment_geometry(e,r2)
        elif d==r2: nodes[(1,e)]=('singleton_edge',p)
    for t in faces:
        planes=[line(*e,next(v for v in t if v not in e)) for e in combinations(t,2)]
        d,p=(F(0),ORIGIN) if all(z[2]>=0 for z in planes) else min(nearest(e) for e in combinations(t,2))
        if d<r2:
            active=tuple(sorted(z for e,z in zip(combinations(t,2),planes) if nearest(e)[0]<r2))
            nodes[(2,t)]=('area_face',active)
        elif d==r2: nodes[(2,t)]=('singleton_face',p)
    for node in nodes:
        dim,cell=node
        if dim:
            for p in cell:
                v=(0,p)
                if v in nodes: incidence.add((v,node))
        if dim==2:
            for e in combinations(cell,2):
                edge=(1,tuple(sorted(e)))
                if edge in nodes: incidence.add((edge,node))
    return nodes,incidence

def bijections(g,h,stop=2):
    n,e=g; m,f=h
    left=defaultdict(list); right=defaultdict(list)
    for node,key in n.items(): left[(node[0],key)].append(node)
    for node,key in m.items(): right[(node[0],key)].append(node)
    if Counter({k:len(v) for k,v in left.items()})!=Counter({k:len(v) for k,v in right.items()}): return []
    mapping={}; choices=[]
    for k in sorted(left):
        u=sorted(left[k]); v=sorted(right[k])
        if len(u)==1: mapping[u[0]]=v[0]
        else: choices.append((u,list(permutations(v))))
    answers=[]
    for selected in product(*(options for u,options in choices)):
        candidate=dict(mapping)
        for (u,options),v in zip(choices,selected): candidate.update(zip(u,v))
        if {(candidate[a],candidate[b]) for a,b in e}==f:
            answers.append(candidate)
            if len(answers)>=stop: break
    return answers

def apply(A,p): return (A[0][0]*p[0]+A[0][1]*p[1],A[1][0]*p[0]+A[1][1]*p[1])
def mul(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def possible_root_maps(source,target):
    def neighbors(faces):
        es={tuple(sorted(e)) for t in faces for e in combinations(t,2)}
        return {next(p for p in e if p!=ORIGIN) for e in es if ORIGIN in e}
    a=neighbors(source); b=neighbors(target)
    shortest=min(n2(p) for p in a)
    us=[p for p in a if n2(p)==shortest]; vs=[p for p in b if n2(p)==shortest]
    require('unique_shortest_incident_source',len(us)==1)
    require('unique_shortest_incident_target',len(vs)==1)
    u,v=us[0],vs[0]; norm=n2(u)
    c,s=dot(u,v)/norm,det(u,v)/norm
    rotate=((c,-s),(s,c))
    reflect=tuple(tuple(2*u[i]*u[j]/norm-int(i==j) for j in range(2)) for i in range(2))
    options=[rotate,mul(rotate,reflect)]
    # Any O(2) transformation mapping the unique shortest edge must be one
    # of these two. The complete incident star eliminates the wrong option.
    survivors=[A for A in options if {apply(A,p) for p in a}==b]
    return options,survivors

def transformed(faces,A): return {tuple(sorted(apply(A,p) for p in t)) for t in faces}
def plain(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    return x

def main():
    reference=mesh({j:F(1,2) for j in range(-5,6)})
    graph=restriction(reference)
    require('complete_counts',Counter(k[0] for k in graph[0])=={0:8,1:34,2:27})
    require('complete_incidences',len(graph[1])==164)
    cases=[]
    for bits in product((F(1,2),F(3,2)),repeat=3):
        word=dict(zip((-1,0,1),bits))
        for upper in (False,True):
            source=mesh(word,upper)
            options,survivors=possible_root_maps(source,reference)
            require('exactly_one_ambient_star_match',len(survivors)==1)
            answers=bijections(restriction(transformed(source,survivors[0])),graph)
            require('unique_full_cell_bijection',len(answers)==1)
            cases.append({'word':plain(bits),'upper':upper,'orthogonal_options':plain(options),
                          'surviving_map':plain(survivors[0]),'cell_bijections':len(answers)})
    # Large arbitrary translated roots, independent of central origin choice.
    for rootj,rootk,upper in product((-13,11),(-97,83),(False,True)):
        word={j:F(1,2) if j in {-14,-13,-1,0,10,12} else F(3,2) for j in range(-20,21)}
        source=mesh(word,upper,rootj,rootk)
        options,survivors=possible_root_maps(source,reference)
        require('arbitrary_root_unique_match',len(survivors)==1)
        require('arbitrary_root_full_bijection',len(bijections(restriction(transformed(source,survivors[0])),graph))==1)
    baseline={j:F(1,2) for j in range(-5,6)}
    changed=dict(baseline); changed[-1]=F(3,2)
    a=mesh(baseline); b=mesh(changed)
    options,survivors=possible_root_maps(a,b)
    require('enlarged_star_forces_identity',survivors==[((F(1),F(0)),(F(0),F(1)))])
    radius_controls=[]
    for r2 in (F(10),F(10)+F(1,4096),F(1001,100)):
        matches=[]
        for A in options:
            if bijections(restriction(transformed(a,A),r2),restriction(b,r2)):matches.append(A)
        require('all_ambient_maps_radius_'+str(r2),len(matches)==(1 if r2==10 else 0))
        radius_controls.append({'radius_squared':str(r2),'all_O2_candidates':2,'matching_ambient_isometries':len(matches)})
    # Degree-preserving two-switch of edge-face incidence at one collapsed
    # boundary point. Every cell geometry/count and every node degree stays
    # unchanged, while the parent-cell incidence system becomes inequivalent.
    nodes,relations=graph; p=(F(1),F(-3))
    pointedges=[e for e in nodes if nodes[e]==('singleton_edge',p)]
    capedge=next(e for e in pointedges if any(a==e and nodes[b][0]=='area_face' and nodes[b][1]==((0,-1,-3),) for a,b in relations))
    outward=next(e for e in pointedges if e!=capedge and any(a==e and nodes[b][0]=='area_face' for a,b in relations))
    singletonface=next(b for a,b in relations if a==capedge and nodes[b][0]=='singleton_face')
    tallface=next(b for a,b in relations if a==outward and nodes[b][0]=='area_face')
    mutant=set(relations)
    mutant.remove((capedge,singletonface));mutant.remove((outward,tallface))
    mutant.add((capedge,tallface));mutant.add((outward,singletonface))
    degree=lambda edges:Counter(x for a,b in edges for x in (a,b))
    require('incidence_mutation_keeps_degrees',degree(mutant)==degree(relations))
    require('incidence_mutation_keeps_geometry_counts',len(mutant)==len(relations))
    require('incidence_mutation_no_cell_bijection',not bijections(graph,(nodes,mutant)))
    result={'status':'PASS','checks':len(CHECKS),'rooted_cases':len(cases),'additional_large_roots':8,
            'counts':{'vertices':8,'positive_edges':28,'singleton_edges':6,'positive_faces':23,'singleton_faces':4,'incidences':164},
            'new_mechanisms':['Exhaustive all rooted ambient O(2) maps from the unique shortest incident edge, then full clipped-cell graph bijection',
                              'Degree/geometry/count-preserving edge-face incidence two-switch rejected by exhaustive ambiguous-singleton graph matching'],
            'radius_controls':radius_controls,'incidence_mutation':'rejected with all geometry, counts and degrees unchanged',
            'cases':cases,'checks_passed':CHECKS,
            'limits':'Finite exact acceptance controls supplement EARLY_CRITERIA_AND_RECONSTRUCTION universal proof. Larger-radius result concerns these two specified patches at the listed radii, not all radii or all sequences.',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'FRESH_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'cases','checks_passed'}},indent=2))

if __name__=='__main__':main()
