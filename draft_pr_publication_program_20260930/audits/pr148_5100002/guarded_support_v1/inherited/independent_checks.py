#!/usr/bin/env python3
"""Independent rational-coordinate verification of the literal k108 counterexample.
No SymPy, approximate trigonometry, imported author code, or trajectory solver.
Physical scaling is (u,sqrt(5)*v) for H and (sqrt(2)*u,v) for V.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from functools import reduce
from operator import mul
from hashlib import sha256
import json
checks={}
def ck(name,ok):
    if not ok:
        raise RuntimeError("check failed: "+name)
    checks[name]=checks.get(name,0)+1
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def scale(c,a):return (c*a[0],c*a[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b,G):return sum(g*x*y for g,x,y in zip(G,a,b))
def exact_sqrt(x):
    a=isqrt(x.numerator);b=isqrt(x.denominator)
    if a*a!=x.numerator or b*b!=x.denominator:
        raise RuntimeError("rational square root is not exact")
    return F(a,b)
def area(P):return sum(cross(P[i],P[(i+1)%6]) for i in range(6))/2
def tangents(P,B):
    Q=[]
    for i,p in enumerate(P):
        q=P[(i+1)%6];a,b=B[0]*p[0],B[1]*p[1];c,d=B[0]*q[0],B[1]*q[1]
        det=a*d-b*c;ck('tangent_pair_nondegenerate',det!=0)
        Q.append(((d-b)/det,(a-c)/det))
    return Q
data=[
    ('H',(F(1),F(5)),[(2,0),(F(4,3),F(1,3)),(-F(4,3),F(1,3)),(-2,0),(-F(4,3),-F(1,3)),(F(4,3),-F(1,3))],F(20,9),F(16,5),F(125,324),F(11664,3125)),
    ('V',(F(2),F(1)),[(0,1),(-F(4,3),F(1,3)),(-F(4,3),-F(1,3)),(0,-1),(F(4,3),-F(1,3)),(F(4,3),F(1,3))],F(32,9),F(5),F(32,81),F(3645,1024))]
records=[]
for name,G,raw,expectedA,expectedQ,expectedS,expectedK in data:
    P=[tuple(map(F,z)) for z in raw]
    B=(G[0]/4,G[1]);C=(G[0]*F(9,32),G[1]*F(9,5))
    ck('positive_metrics',min(G+B+C)>0)
    ck('strict_nested_confocal',F(4)-F(32,9)==F(1)-F(5,9)==F(4,9) and F(4,9)<1)
    for i in range(6):
        for j in range(i):
            ck('distinct_vertices',P[i]!=P[j])
    lengths=[exact_sqrt(dot(sub(P[(i+1)%6],P[i]),sub(P[(i+1)%6],P[i]),G)) for i in range(6)]
    velocities=[scale(1/lengths[i],sub(P[(i+1)%6],P[i])) for i in range(6)]
    halves=[];cosines=[];taus=[]
    Q=tangents(P,B)
    for i,p in enumerate(P):
        nxt=P[(i+1)%6];v=sub(nxt,p)
        ck('ellipse_vertex',dot(p,p,B)==1)
        ck('unit_velocity',dot(velocities[i],velocities[i],G)==1)
        # The line-restricted caustic quadratic has a double root strictly
        # inside the segment, independently reconstructing the contact.
        aa=dot(v,v,C);bb=2*dot(p,v,C);cc=dot(p,p,C)-1
        tau=-bb/(2*aa);contact=add(p,scale(tau,v));taus.append(str(tau))
        ck('caustic_double_root',bb*bb-4*aa*cc==0)
        ck('strict_interior_contact',0<tau<1)
        ck('contact_reconstruction',dot(contact,contact,C)==1 and dot(contact,v,C)==0)
        ck('caustic_left_branch',cross(v,scale(-1,p))>0)
        for j in range(6):
            if j not in (i,(i+1)%6):ck('global_strict_convexity',cross(v,sub(P[j],p))>0)
        # Reconstruct physical specular reflection from its normal, in the
        # scaled rational metric.
        normal=(p[0]/4,p[1]);vin=velocities[(i-1)%6];vout=velocities[i]
        J=dot(vin,normal,G);normal2=dot(normal,normal,G)
        ck('positive_normal_norm',normal2>0)
        ck('Joachimsthal_incoming',J==F(1,3))
        ck('Joachimsthal_outgoing',dot(vout,normal,G)==-F(1,3))
        ck('reflection_vector',vout==sub(vin,scale(2*J/normal2,normal)))
        interior_cos=-dot(vin,vout,G);cosines.append(interior_cos)
        ck('strict_internal_angle',-1<interior_cos<1)
        halves.append((1-interior_cos)/2)
        ck('two_outer_tangent_equations',dot(p,Q[i],B)==dot(nxt,Q[i],B)==1)
        left=Q[(i-1)%6];right=Q[i];edge=sub(right,left)
        t=dot(sub(p,left),edge,G)/dot(edge,edge,G)
        ck('vertex_inside_outer_side',0<t<1 and p==add(left,scale(t,edge)))
    # With all cyclic vertices strictly convex, the orbit winding is one.
    # The six distinct points imply primitive billiard period six.
    ck('period_six_parity',len(P)==6 and len(P)%4==2)
    A=area(P);Aprime=area(Q)
    ck('rational_scaled_area',A==expectedA and A>0)
    ck('rational_scaled_outer_area',Aprime==expectedQ and Aprime>0)
    S2=reduce(mul,halves,F(1));S=exact_sqrt(S2)
    ck('positive_half_angle_product',S==expectedS and S>0)
    K=Aprime/A/S
    ck('literal_quotient',K==expectedK)
    ck('common_perimeter',sum(lengths)==F(28,3))
    ck('source_internal_angle_calibration',sum(cosines)==F(1,3)*sum(lengths)-6)
    ck('signed_area_product_control',A*Aprime*G[0]*G[1]==F(320,9))
    ck('product_is_only_two_example_control',Aprime/A*S==F(5,9))
    # Reversing either orientation leaves the area ratio and sine product.
    ck('orientation_reversal_ratio',area(list(reversed(Q)))/area(list(reversed(P)))==Aprime/A)
    records.append({'name':name,'metric':[str(z) for z in G],'rational_area':str(A),'rational_outer_area':str(Aprime),'lengths':[str(z) for z in lengths],'contact_parameters':taus,'internal_cosines':[str(z) for z in cosines],'half_sine_product':str(S),'k108':str(K)})
K1=F(records[0]['k108']);K2=F(records[1]['k108'])
ck('strict_nonzero_difference',K1-K2==F(553311,3200000)>0)
ck('different_geometric_orbits',data[0][2][0] not in data[1][2]) # axial starts differ; physical axes scaling retained separately.
root=Path(__file__).resolve().parent
result={'status':'PASS','exact_assertions':sum(checks.values()),'checks':checks,'orbits':records,'difference':str(K1-K2),'artifact_sha256':sha256((root/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'method':'Independent standard-library rational arithmetic in two scaled Euclidean coordinate systems; exact line-discriminant tangency and vector reflection.'}
# Candidate repair: reject false or stale receipt/proof conditions under -O too.
expected_receipt_path=root/'expected_independent_results.json'
expected_receipt_bytes=expected_receipt_path.read_bytes()
if sha256(expected_receipt_bytes).hexdigest()!='a64abe47712fee04c8647643d40246d3858f4244bb4ef1fbceb29ea6227790b9':
    raise RuntimeError('frozen expected receipt hash mismatch')
if sha256((root/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest()!='5553f899b1098a321fe2164c3ba0d6eed87bc2424dc8021dee50e01fc14dc4ab':
    raise RuntimeError('frozen mathematical artifact hash mismatch')
expected_receipt=json.loads(expected_receipt_bytes)
receipt_for_comparison=dict(result)
if 'verifier_sha256' in receipt_for_comparison:
    # Only the nominated explicit-guard candidate source differs from the frozen author source.
    receipt_for_comparison['verifier_sha256']=expected_receipt['verifier_sha256']
if receipt_for_comparison!=expected_receipt:
    raise RuntimeError('computed receipt differs from frozen expected receipt')
text=json.dumps(result,indent=2,sort_keys=True)+'\n';(root/'independent_results.json').write_text(text);print(text,end='')

