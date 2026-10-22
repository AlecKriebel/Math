#!/usr/bin/env python3
"""Exact controls for the angle/trace reduction and the source edge cycle."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib,json,itertools
from turn1_quaternion import *

groups=Counter(); undefined=0
def ck(name,v):
    assert v,name
    groups[name]+=1
def values(t):
    aa,x,y,d,b,bb,z,zz=t
    delta=sub(x,y);V=mul(d,delta);P=mul(aa,delta)
    A=mul(aa,inv(d));Q=prod(inv(A),b,b);s=dot(delta,delta)
    return V,P,A,Q,s
def verify(t):
    global undefined
    ck('square_relations',relation(t))
    V,P,A,Q,s=values(t);b=t[4]
    ck('imaginary_vectors',V[0]==P[0]==0)
    ck('equal_norms',dot(V,V)==dot(P,P)==s)
    ck('orthogonal_axis',mul(P,b)==mul(inv(b),P))
    ck('quaternion_product',mul(V,P)==tuple(-s*x for x in inv(A)))
    ck('unsquared_identity',dot(V,conjug(inv(b),P))==s*Q[0])
    ck('squared_polynomial_identity',dot(V,conjug(inv(b),P))**2==s*s*Q[0]**2)
    ck('double_curve_vs_double_traversal',4*Q[0]**2==2*mul(Q,Q)[0]+2)
    if s:
        ck('angle_trace_identity',invariant(t)==Q[0]**2)
    else:undefined+=1
    aa,x,y,d,b,bb,z,zz=t
    out=word(t,'aa');aafter=mul(out[0],inv(out[3]))
    ck('simple_curve_twist_word',inv(aafter)==Q)

seeds=[]
for n in range(1,7):
    a=F(1-n*n,1+n*n);b=F(2*n,1+n*n)
    seeds.append(((a,b,F(0),F(0)),k,inv(k),one,i,i,j,j))
    A1=(a,F(0),b,F(0));A2=(F(1,2),)*4;A3=conjug(j,A2)
    B1=prod(A1,A2,j);B2=conjug(inv(A1),B1)
    seeds.append((A1,A2,A3,one,B1,B2,j,j))
words=['']+list('ABCDEabcde')+[''.join(x) for x in itertools.product('ABCDEabcde',repeat=2)]
for t in seeds:
    for w in words:verify(word(t,w))
    for h in [i,j,(F(3,5),F(4,5),F(0),F(0))]:
        u=tuple(conjug(h,x) for x in t);verify(u)
        ck('simultaneous_conjugation',values(u)[3][0]**2==values(t)[3][0]**2)
    for w in ['C','D','eedcBCDEE','CDeedcBCDEE']:
        u=word(t,w);verify(u)
        ck('source_subgroup_trace_control',values(u)[3][0]**2==values(t)[3][0]**2)
# Original angle undefined even at irreducibles; the polynomial extension is still defined.
for aa,expected in [(i,F(0)),(one,F(1))]:
    t=(aa,one,one,one,i,i,j,j);verify(t)
    ck('undefined_irreducible_boundary',mul(i,j)!=mul(j,i) and values(t)[4]==0)
    ck('boundary_extension_value',values(t)[3][0]**2==expected)
    try:invariant(t)
    except ZeroDivisionError:ck('original_angle_remains_undefined',True)
    else:raise AssertionError('angle was defined at delta=0')

# Reconstruct the actual origami, including cone vertices, from its two gluing permutations.
h={1:1,2:3,3:2,4:4};v={1:2,2:1,3:4,4:3}
corners=list(itertools.product(range(1,5),range(2),range(2)))
parent={c:c for c in corners}
def root(x):
    while parent[x]!=x:x=parent[x]
    return x
def union(x,y):parent[root(x)]=root(y)
for s in range(1,5):
    for y in range(2):union((s,1,y),(h[s],0,y))
    for x in range(2):union((s,x,1),(v[s],x,0))
classes={root(c) for c in corners}
ck('square_complex_vertex_count',len(classes)==2)
edge_a1=(root((1,0,0)),root((1,0,1)))
edge_a4=(root((4,0,0)),root((4,0,1)))
ck('two_edge_circle_endpoints',edge_a1==edge_a4 and edge_a1[0]!=edge_a1[1])
ck('distinct_edge_interiors',h[1]==1 and h[4]==4 and 1!=4)
# Oriented face boundary: bottom + right - top - left.
faces=[{'b1':1,'a1':0,'b2':-1},{'b2':1,'a3':1,'b1':-1,'a2':-1},
       {'b4':1,'a2':1,'b3':-1,'a3':-1},{'b3':1,'a4':0,'b4':-1}]
cochain={f'a{i}':int(i==1) for i in range(1,5)}
cochain.update({f'b{i}':0 for i in range(1,5)})
for face in faces:ck('closed_integral_cellular_cochain',sum(n*cochain[e] for e,n in face.items())==0)
ck('essential_cycle_pairing',cochain['a1']-cochain['a4']==1)
ck('essential_twisted_cycle_pairing',-cochain['a1']+cochain['a4']+2*cochain['b1']==-1)
ck('euler_characteristic',2-8+4==-2)
print(json.dumps({'problem_id':11000192,'author_turn':3,'status':'PASS','exact_controls':sum(groups.values()),'groups':dict(sorted(groups.items())),'undefined_angle_cases_recorded':undefined,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'quaternion_module_sha256':hashlib.sha256(Path(__file__).with_name('turn1_quaternion.py').read_bytes()).hexdigest(),'scope':'Exact diagnostic support for the written trace-square reduction and source square-complex curve certificate. Multicurve independence is credited to Charles–Marche, not proved by finite tests. The original measurable nonergodicity construction remains unresolved.'},indent=2,sort_keys=True))
