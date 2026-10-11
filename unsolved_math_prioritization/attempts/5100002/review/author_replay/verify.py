#!/usr/bin/env python3
"""Exact six-period counterexample certificate; no floating-point orbit solver."""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
from functools import reduce
from operator import mul
import json
import sympy as s
R=s.Rational;rt=s.sqrt
counts={}
def ck(name,statement):
    if not bool(statement):
        raise RuntimeError("check failed: "+name)
    counts[name]=counts.get(name,0)+1

def dot(x,y):return s.simplify(sum(a*b for a,b in zip(x,y)))
def det(x,y):return s.simplify(x[0]*y[1]-x[1]*y[0])
def sub(x,y):return tuple(s.simplify(a-b) for a,b in zip(x,y))
def area(P):return s.simplify(sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2)

H=[(2,0),(R(4,3),rt(5)/3),(-R(4,3),rt(5)/3),(-2,0),(-R(4,3),-rt(5)/3),(R(4,3),-rt(5)/3)]
V=[(0,1),(-4*rt(2)/3,R(1,3)),(-4*rt(2)/3,-R(1,3)),(0,-1),(4*rt(2)/3,-R(1,3)),(4*rt(2)/3,R(1,3))]
QH=[(2,rt(5)/5),(0,3*rt(5)/5),(-2,rt(5)/5),(-2,-rt(5)/5),(0,-3*rt(5)/5),(2,-rt(5)/5)]
QV=[(-rt(2),1),(-3*rt(2)/2,0),(-rt(2),-1),(rt(2),-1),(3*rt(2)/2,0),(rt(2),1)]
fixtures=[('H',H,QH,[1,R(8,3),1,1,R(8,3),1],[-R(1,9),-R(2,3),-R(2,3),-R(1,9),-R(2,3),-R(2,3)],20*rt(5)/9,16*rt(5)/5,R(125,324),R(11664,3125)),
          ('V',V,QV,[2,R(2,3),2,2,R(2,3),2],[-R(7,9),-R(1,3),-R(1,3),-R(7,9),-R(1,3),-R(1,3)],32*rt(2)/9,5*rt(2),R(32,81),R(3645,1024))]
lam=R(4,9);ac2=R(32,9);bc2=R(5,9)
ck('strict_nested_confocal',0<lam<1 and 4-ac2==1-bc2==lam and ac2-bc2==3)
ck('required_parity',6%4==2)
records=[]
for name,P,expectedQ,lengths,cosines,expectedA,expectedAprime,expectedS,expectedK in fixtures:
    P=[tuple(map(s.sympify,p)) for p in P];Q=[];sins=[];actual_lengths=[];contacts=[]
    ck('exact_algebraic_input',all(not z.has(s.Float) for p in P for z in p))
    for p,q in combinations(P,2):ck('six_distinct_vertices',dot(sub(p,q),sub(p,q))>0)
    for i,p in enumerate(P):
        prev=P[(i-1)%6];nxt=P[(i+1)%6]
        ck('outer_ellipse',s.simplify(p[0]**2/4+p[1]**2-1)==0)
        incoming=sub(p,prev);outgoing=sub(nxt,p)
        ck('counterclockwise_convex_turn',det(incoming,outgoing)>0)
        n=(nxt[1]-p[1],p[0]-nxt[0]);height=dot(n,p)
        ck('caustic_left',height>0)
        ck('caustic_tangent_line',s.simplify(height**2-ac2*n[0]**2-bc2*n[1]**2)==0)
        contact=(s.simplify(ac2*n[0]/height),s.simplify(bc2*n[1]/height))
        ck('contact_on_caustic',s.simplify(contact[0]**2/ac2+contact[1]**2/bc2-1)==0)
        tau=s.simplify(dot(sub(contact,p),outgoing)/dot(outgoing,outgoing))
        ck('contact_on_segment',0<tau<1 and all(s.simplify(contact[j]-p[j]-tau*outgoing[j])==0 for j in range(2)))
        contacts.append([str(x) for x in contact])
        for j,z in enumerate(P):
            if j not in (i,(i+1)%6):ck('other_vertices_strictly_left',s.simplify(dot(n,z)-height)<0)
        lp=s.sqrt(dot(incoming,incoming));lq=s.sqrt(dot(outgoing,outgoing));actual_lengths.append(lq)
        ck('edge_length',lq==lengths[i])
        ein=tuple(s.simplify(z/lp) for z in incoming);eout=tuple(s.simplify(z/lq) for z in outgoing)
        normal=(p[0]/4,p[1]);projection=dot(ein,normal)
        ck('common_J_incoming',projection==R(1,3))
        ck('common_J_outgoing',dot(eout,normal)==-R(1,3))
        reflected=tuple(s.simplify(ein[j]-2*projection/dot(normal,normal)*normal[j]) for j in range(2))
        ck('specular_reflection',all(s.simplify(eout[j]-reflected[j])==0 for j in range(2)))
        cos=s.simplify(-dot(ein,eout))
        ck('internal_angle_cosine',cos==cosines[i] and -1<cos<1)
        half=s.simplify(s.sqrt((1-cos)/2));sins.append(half)
        ck('positive_half_sine',half>0 and s.simplify(2*half**2+cos-1)==0)
        tangent_system=s.Matrix([[p[0]/4,p[1]],[nxt[0]/4,nxt[1]]])
        ck('outer_tangents_not_parallel',tangent_system.det()!=0)
        outer=tuple(s.simplify(z) for z in tangent_system.inv()*s.ones(2,1));Q.append(outer)
        ck('outer_intersection_coordinates',all(s.simplify(outer[j]-expectedQ[i][j])==0 for j in range(2)))
        ck('both_tangent_equations',s.simplify(p[0]*outer[0]/4+p[1]*outer[1]-1)==0 and s.simplify(nxt[0]*outer[0]/4+nxt[1]*outer[1]-1)==0)
    for i,p in enumerate(P):
        l=Q[(i-1)%6];r=Q[i];edge=sub(r,l)
        tau=s.simplify(dot(sub(p,l),edge)/dot(edge,edge))
        ck('orbit_vertex_on_outer_edge',0<tau<1 and all(s.simplify(p[j]-l[j]-tau*edge[j])==0 for j in range(2)))
    A=area(P);Aprime=area(Q);product=s.simplify(reduce(mul,sins,s.S.One));K=s.simplify(Aprime/A/product)
    ck('orbit_area',A==expectedA and A>0)
    ck('outer_area',Aprime==expectedAprime and Aprime>0)
    ck('half_angle_product',product==expectedS and product>0)
    ck('exact_k108',K==expectedK)
    ck('common_perimeter',s.simplify(sum(actual_lengths))==R(28,3))
    ck('source_angle_normalization',sum(cosines)==R(1,3)*R(28,3)-6)
    ck('area_product_control',s.simplify(A*Aprime)==R(320,9))
    ck('alternative_product_only_control',s.simplify(Aprime/A*product)==R(5,9))
    records.append({'name':name,'orbit_area':str(A),'outer_area':str(Aprime),'perimeter':'28/3','half_sines':[str(z) for z in sins],'half_angle_product':str(product),'k108':str(K),'caustic_contacts':contacts})
ck('unequal_values',R(11664,3125)-R(3645,1024)==R(553311,3200000)>0)
root=Path(__file__).parent
out={'problem_id':5100002,'status':'PASS_EXACT_SIX_PERIOD_COUNTEREXAMPLE','assertions':sum(counts.values()),'groups':counts,
     'proof_sha256':sha256((root/'COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
     'period':6,'caustic_lambda':'4/9','k108_difference':'553311/3200000','orbits':records,
     'scope':'Two convex primitive six-period trajectories in the same strictly nested confocal ellipse pair. Exact source k108 quotient fails; no repaired all-period invariant or novelty is certified.'}
# Candidate repair: reject false or stale receipt/proof conditions under -O too.
expected_receipt_path=root/'expected_verification.json'
expected_receipt_bytes=expected_receipt_path.read_bytes()
if sha256(expected_receipt_bytes).hexdigest()!='fa59d8484cb4ca6d8a411e39d4ed320755932b5f5f69b70eff127dd1a5d80a42':
    raise RuntimeError('frozen expected receipt hash mismatch')
if sha256((root/'COUNTEREXAMPLE.md').read_bytes()).hexdigest()!='5553f899b1098a321fe2164c3ba0d6eed87bc2424dc8021dee50e01fc14dc4ab':
    raise RuntimeError('frozen mathematical artifact hash mismatch')
expected_receipt=json.loads(expected_receipt_bytes)
receipt_for_comparison=dict(out)
if 'verifier_sha256' in receipt_for_comparison:
    # Only the nominated explicit-guard candidate source differs from the frozen author source.
    receipt_for_comparison['verifier_sha256']=expected_receipt['verifier_sha256']
if receipt_for_comparison!=expected_receipt:
    raise RuntimeError('computed receipt differs from frozen expected receipt')
(root/'verification.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
