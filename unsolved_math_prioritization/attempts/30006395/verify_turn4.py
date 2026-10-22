"""Exact low-degree/Wick controls for Turn 4. No external source code.
The universal diagram and uniform-tail proofs are in TURN_4.md.
"""
from itertools import combinations,product
from fractions import Fraction as F
from collections import Counter,defaultdict
from math import comb,prod,factorial
import json
import mpmath as mp
counts=Counter()
def ck(x,kind):
    assert x,kind
    counts[kind]+=1
def addpoly(dst,src,scale=1):
    for key,v in src.items():dst[key]+=scale*v

def multiply_masks(A,B,q,b):
    shared=A&B;exclusive=A^B;out={};sub=shared
    while True:
        out[exclusive|sub]=q**(shared.bit_count()-sub.bit_count())*b**sub.bit_count()
        if not sub:break
        sub=(sub-1)&shared
    return out

def geometry(n):
    edges=list(combinations(range(n),2));idx={e:i for i,e in enumerate(edges)}
    em=[1<<i for i in range(len(edges))]
    wedges=[]
    for center in range(n):
        for u,v in combinations([x for x in range(n) if x!=center],2):
            wedges.append((1<<idx[tuple(sorted((center,u)))])|(1<<idx[tuple(sorted((center,v)))]))
    return edges,em,wedges

def support(mask,edges):
    return {x for i,e in enumerate(edges) if mask>>i&1 for x in e}

cases=0
for n in range(4,13):
    edges,em,wedges=geometry(n);NE=len(em);NW=len(wedges)
    ck(NE==comb(n,2) and NW==n*comb(n-1,2),'copy_normalizations')
    supports={x:support(x,edges) for x in em+wedges}
    for p in [F(1,3),F(2,n),F(3,n)]:
        q=p*(1-p);b=1-2*p
        # Y_(two edges) - (X_edge²-1), in the raw centered-edge basis.
        raw=defaultdict(F)
        for A in em:
            for B in em:
                if supports[A].isdisjoint(supports[B]):raw[A|B]+=1
                addpoly(raw,multiply_masks(A,B,q,b),-1)
        raw[0]+=NE*q
        target=defaultdict(F)
        for A in em:target[A]-=b
        for A in wedges:target[A]-=2
        keys=set(raw)|set(target)
        for key in keys:ck(raw[key]==target[key],'first_wick_polynomial_identity')
        norm=sum(value*value*q**key.bit_count() for key,value in raw.items())/(NE*NE*q*q)
        ck(norm==b*b/(NE*q)+F(4*NW,NE*NE),'first_wick_error_norm')
        # X_edge X_wedge minus the vertex-disjoint product.
        raw=defaultdict(F)
        for A in em:
            for B in wedges:
                if not supports[A].isdisjoint(supports[B]):addpoly(raw,multiply_masks(A,B,q,b))
        target=defaultdict(F)
        for A in em:target[A]+=2*(n-2)*q
        for A in wedges:target[A]+=2*b
        triples={'path':0,'star':0,'triangle':0}
        for trio in combinations(range(NE),3):
            mask=sum(1<<j for j in trio);deg=Counter(x for j in trio for x in edges[j]);v=len(deg)
            if v==3:kind='triangle';coef=3
            elif v==4 and max(deg.values())==3:kind='star';coef=3
            elif v==4 and sorted(deg.values())==[1,1,2,2]:kind='path';coef=2
            else:continue
            target[mask]+=coef;triples[kind]+=1
        for key in set(raw)|set(target):ck(raw[key]==target[key],'mixed_disjoint_forest_identity')
        norm=sum(value*value*q**key.bit_count() for key,value in raw.items())/(NE*NW*q**3)
        expected=F(4*(n-2)**2,NW)+4*b*b/(NE*q)+F(4*triples['path']+9*triples['star']+9*triples['triangle'],NE*NW)
        ck(norm==expected,'mixed_wick_error_norm')
        cases+=1
# Check the power-counting equality cases on finite tuples of wedges.
edges,em,wedges=geometry(4)
for r in [2,3,4]:
    for copies in product(wedges,repeat=r):
        mult=Counter(i for A in copies for i in range(len(edges)) if A>>i&1)
        if any(x==1 for x in mult.values()):continue
        union=0
        for A in copies:union|=A
        verts=support(union,edges);adj={x:[] for x in verts}
        for i in mult:
            u,v=edges[i];adj[u].append(v);adj[v].append(u)
        comps=[];seen=set()
        for v in verts:
            if v in seen:continue
            todo=[v];seen.add(v);C=set()
            while todo:
                w=todo.pop();C.add(w)
                for z in adj[w]:
                    if z not in seen:seen.add(z);todo.append(z)
            comps.append(C)
        power=F(len(verts)-len(mult))-F(r,2)
        ck(power<=0,'diagram_nonpositive_power')
        if power==0:
            ck(2*len(comps)==r,'leading_diagram_pairs')
            for C in comps:
                inside=[A for A in copies if support(A,edges)<=C]
                ck(len(inside)==2 and inside[0]==inside[1],'leading_identical_tree_pair')
# Bernoulli moments for the first connected-tree statistic, by full null enumeration.
for n in [3,4,5]:
    E=comb(n,2);p=F(1,3);q=p*(1-p);m2=F(0);m4=F(0)
    for bits in range(1<<E):
        e=bits.bit_count();w=p**e*(1-p)**(E-e);X=F(e)-E*p;m2+=w*X**2;m4+=w*X**4
    ck(m2==E*q,'edge_variance_exact')
    ck(m4/(E*E*q*q)==3+(1/q-6)/E,'edge_fourth_moment_exact')
# Separate numerical diagnostics for the closed-form variance and TV profile.
mp.mp.dps=60;diagnostics=[]
for cstr in ['3','4','10']:
    c=mp.mpf(cstr);tau=-mp.lambertw(-1/c);A=c*tau/(1-tau)-1
    partial=sum(c**(1-s)*mp.mpf(s)**s/mp.factorial(s) for s in range(2,801))
    assert abs(A-partial)<mp.mpf('1e-30')
    for astr in ['0.25','0.5','1']:
        a=mp.mpf(astr);sigma=a*mp.sqrt(A);tv=mp.erf(sigma/(2*mp.sqrt(2)))
        diagnostics.append({'c':cstr,'a':astr,'A_closed_form':mp.nstr(A,24),'A_series_800_terms':mp.nstr(partial,24),'limiting_TV':mp.nstr(tv,24),'status':'numerical diagnostic, not proof'})
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'exact_geometry_parameter_cases':cases,'diagnostic_decimal_precision':60,'closed_variance_and_TV_diagnostics':diagnostics,'scope':'Exact finite Wick identities, error norms and diagram controls; Gaussian/Wick limits and uniform L2 tail are proved in TURN_4.md. No inference at c=e is made.'},indent=2,sort_keys=True))
