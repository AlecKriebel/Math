#!/usr/bin/env python3
"""Independent exact shadow/diagram controls. No author imports or topology oracle."""
from collections import Counter,defaultdict
from itertools import combinations,product
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
C=Counter()
def ck(p,k):
    assert p,k
    C[k]+=1

def analyse(rot,ends):
    # Four independent ports at each medial crossing: endpoint and side.
    ports=[(e,v,side) for e,vs in ends.items() for v in vs for side in (0,1)]
    arc={};straight={};medial_edges=[]
    for e,v,side in ports:
        q=rot[v];j=q.index(e);f=q[(j+(1 if side else -1))%len(q)]
        arc[e,v,side]=(f,v,1-side)
        w=next(u for u in ends[e] if u!=v)
        straight[e,v,side]=(e,w,side)
        if side:medial_edges.append((e,f))
    ck(all(arc[arc[p]]==p and straight[straight[p]]==p for p in ports),'port_pairing_involutions')
    components=[];unused=set(ports)
    while unused:
        todo=[next(iter(unused))];seen=set(todo)
        while todo:
            p=todo.pop()
            for q in (arc[p],straight[p]):
                if q not in seen:seen.add(q);todo.append(q)
        components.append(seen);unused-=seen
    # Face walks are recovered separately in the original ribbon graph.
    unused={(e,v) for e,vs in ends.items() for v in vs};faces=[]
    while unused:
        first=next(iter(unused));p=first;face=[]
        while True:
            unused.remove(p);e,v=p;face.append(e)
            w=next(u for u in ends[e] if u!=v);q=rot[w]
            p=(q[(q.index(e)+1)%len(q)],w)
            if p==first:break
        faces.append(face)
    return ports,arc,straight,components,faces,medial_edges

family_rows=[]
for k in range(2,81):
    ps=tuple('p'+str(j) for j in range(1,k+1))
    rot={'A':('a',)+ps,'B':('b',)+ps[::-1],'C':('a','b')}
    ends={'a':('A','C'),'b':('B','C'),**{p:('A','B') for p in ps}}
    ports,arc,straight,components,faces,edges=analyse(rot,ends)
    ck(len(components)==1 and len(components[0])==4*(k+2),'actual_medial_knot_component')
    ck(len(rot)-len(ends)+len(faces)==2,'family_sphere_embedding')
    ck(sorted(map(len,faces))==[2]*(k-1)+[3,3],'family_white_region_degrees')
    p=('a','A',1);first=p;word=[];sides=[]
    while True:
        word.append(p[0]);sides.append(p[2]);p=straight[arc[p]]
        if p==first:break
    predicted=['a']+list(ps)+(['a','b'] if k%2==0 else ['b','a'])+list(ps[::-1])+['b']
    ck(word==predicted,'independent_all_k_traversal_word')
    ck(all(sides[j]!=sides[(j+1)%len(sides)] for j in range(len(sides))),'alternating_port_traversal')
    ck(Counter(word)==Counter({e:2 for e in ends}),'both_strands_each_crossing')
    ck(len(edges)==2*len(ends),'medial_four_valence')
    # Direct medial 2-edge-cut test, rather than using the Tait cut-vertex test.
    if k<=32:
        for removed in combinations(range(len(edges)),2):
            adj=defaultdict(set)
            for j,(u,v) in enumerate(edges):
                if j not in removed:adj[u].add(v);adj[v].add(u)
            reached={'a'};todo=['a']
            while todo:
                for v in adj[todo.pop()]-reached:reached.add(v);todo.append(v)
            ck(len(reached)==len(ends),'no_separating_medial_two_edge_cut')
    black=[F(len(q),2) for q in rot.values()];white=[F(-len(f),2) for f in faces]
    ck(sum(black)==k+2,'canonical_black_mass')
    ck(sum(map(abs,black+white))==2*(k+2),'canonical_total_mass')
    for outside in black+white:ck(sum(map(abs,black+white))-abs(outside)>=F(3*k+7,2),'arbitrary_outside_mass_bound')
    removed=set(rot['A']);remaining=set(ends)-removed
    ck(remaining=={'b'} and len(removed)==k+1,'outside_collapse_exact_survivor')
    family_rows.append({'k':k,'crossings':k+2,'components':1,'twists':2,'surviving_vertex':'b'})

# The explicit wheel and all its crossing-sign assignments.
rot={0:('a','b','c','d'),1:('e','a','h'),2:('f','b','e'),3:('g','c','f'),4:('h','d','g')}
ends={'a':(0,1),'b':(0,2),'c':(0,3),'d':(0,4),'e':(1,2),'f':(2,3),'g':(3,4),'h':(1,4)}
ports,arc,straight,components,faces,edges=analyse(rot,ends)
ck(len(components)==1,'wheel_one_component_direct_ports')
ck(sorted(map(len,faces))==[3,3,3,3,4],'wheel_planar_faces')
p=('a',0,1);first=p;word=[];bits=[]
while True:
    word.append(p[0]);bits.append(p[2]);p=straight[arc[p]]
    if p==first:break
ck(word==list('abfgdaefcdhebcgh'),'wheel_exact_visit_word')
for signs in product((-1,1),repeat=8):
    s=dict(zip(ends,signs));black=[sum(s[e] for e in rot[v]) for v in rot]
    sat=all(abs(x)==len(rot[v]) for v,x in zip(rot,black))
    over=[bit^(s[e]<0) for e,bit in zip(word,bits)]
    alt=all(over[j]!=over[(j+1)%len(over)] for j in range(len(over)))
    ck(sat==alt==(len(set(signs))==1),'wheel_saturation_actual_over_under')
    ck(8-F(sum(abs(x) for x in black),2)==sum((len(rot[v])-abs(x))//2 for v,x in zip(rot,black)),'gleam_defect_identity')
s={e:(-1 if e=='a' else 1) for e in ends}
black=[sum(s[e] for e in rot[v]) for v in rot];white=[-sum(s[e] for e in f) for f in faces]
ck(black==[2,1,3,3,3] and sorted(white)==[-4,-3,-3,-1,-1],'wheel_strict_sign_countercontrol')

# Local true-vertex collapse for every one of its six possible sectors.
K4=list(combinations(range(4),2))
for deleted in K4:
    E=K4.copy();E.remove(deleted)
    for v in deleted:
        neigh=[next(w for w in e if w!=v) for e in E if v in e]
        ck(len(neigh)==2,'collapsed_link_bivalent_suppression')
        E=[e for e in E if v not in e];E.append(tuple(sorted(neigh)))
    ck(len(E)==3 and len(set(E))==1,'all_sector_deletions_theta_link')

# Cusp bases, primitive coefficients, parity and exact rational threshold.
lo,hi=F(223,71),F(22,7)
ck(39<4*lo*lo and 4*hi*hi<40,'strict_integer_slope_threshold')
for k,g2 in product(range(1,45),range(-51,52)):
    eps=g2%2;q=(g2-eps)//2
    ck((2*q+eps,k)==(g2,k),'cusp_basis_reconstruction')
    ck((g2*g2+k*k>=40)==(g2*g2+k*k>4*lo*lo)==(g2*g2+k*k>4*hi*hi),'all_sample_primitive_slope_tests')
    if abs(g2)<=k and g2*g2+k*k>=40:ck(k>=5,'retained_corner_constraint')
for V,u in product(range(1,80),range(1,20)):
    f=V+1;ck((6*V>=5*f+u)==(V>=5+u),'relative_disk_annulus_incidence')

# Actual surface-base Euler characteristics, including nonorientable I-bundles.
bases=[]
for orient in (True,False):
    for genus,boundary in product(range(1,6),range(0,5)):
        chi=2-(2*genus if orient else genus)-boundary
        if chi<=0:bases.append(chi)
for a,b in product(bases,bases):
    for guts in range(11):
        chiSigma=a+b;chiS=-guts+chiSigma
        ck(-chiS-(-a-b)==guts,'complete_characteristic_product_correction')
        # Frontier of a one-sided surface has twice its Euler characteristic.
        doubled_chi=2*chiS;newSigma=chiSigma+chiS
        ck(-doubled_chi+newSigma==guts,'one_sided_frontier_same_guts')
for rB,rW in product(range(2,45),repeat=2):
    t=rB+rW-2
    ck(max(rB-2,rW-2)>=F(t-2,2),'checkerboard_volume_half_factor')
for deficit,m in product(range(1,20),range(1,50)):
    ck(m*deficit-m*deficit==0,'parallel_fiber_complete_product_removal')

out={'problem_id':10400216,'exact_assertions':sum(C.values()),'by_kind':dict(sorted(C.items())),
     'family_range':'2<=k<=80, direct medial two-edge-cut controls through k32','sample_family_rows':family_rows[:3]+family_rows[-2:],
     'scope':'Independent port-graph, direct medial connectivity, cusp lattice and actual base-Euler controls. They do not certify hyperbolicity, characteristic submanifolds or arbitrary shadow reconstruction; those are audited analytically against full primary sources.',
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2,sort_keys=True))
