#!/usr/bin/env python3
"""Fresh exact computation, no candidate checker imports and no floating arithmetic."""
from fractions import Fraction as F
from itertools import combinations, product, permutations
import json

SEG = {'A':(0,2),'B':(1,4),'C':(3,3),'D':(2,5),'T':(4,6)}
NAMES=tuple(SEG)
def need(p,msg):
    if not p: raise RuntimeError(msg)
def prec(u,v):
    a,b=u; c,d=v
    return a<c and c<=b+1 and b<d
def discrete_prec(u,v):
    U=set(range(u[0],u[1]+1));V=set(range(v[0],v[1]+1));W=U|V
    return min(U)<min(V) and not U<=V and not V<=U and W==set(range(min(W),max(W)+1))
def shifted(u,k=-1): return (u[0]+k,u[1]+k)
def flo(u,v):
    a,b=u;c,d=v
    return a<=c<=b<=d
def ladder(names):
    data=sorted(SEG[n] for n in names)
    return all(x[0]<y[0] and x[1]<y[1] for x,y in zip(data,data[1:]))

def graph(left,right,variant='correct',segments=SEG):
    X=tuple((u,v) for u in left for v in right if prec(segments[u],segments[v]))
    def ytest(u,v):
        a,b=segments[u]; c,d=segments[v]
        if variant=='right_shift': return prec((a+1,b+1),(c,d))
        if variant=='shift_second': return prec((a,b),(c-1,d-1))
        if variant=='no_shift': return prec((a,b),(c,d))
        return prec((a-1,b-1),(c,d))
    Y=tuple((u,v) for u in left for v in right if ytest(u,v))
    E={}
    for x in X:
        u,v=x
        E[x]=[]
        for y in Y:
            a,b=y
            first=prec(segments[b],segments[v])
            second=prec(segments[u],segments[a])
            if variant in ('reverse_both','reverse_first'): first=prec(segments[v],segments[b])
            if variant in ('reverse_both','reverse_second'): second=prec(segments[a],segments[u])
            if (u==a and first) or (v==b and second): E[x].append(y)
    return X,Y,E

def injections(X,E,used=frozenset()):
    if not X:return 1
    return sum(injections(X[1:],E,used|{y}) for y in E[X[0]] if y not in used)
def hall(X,E):
    deficits=[]
    for k in range(1,len(X)+1):
        for subset in combinations(X,k):
            neighbors=set(y for x in subset for y in E[x])
            if len(neighbors)<k: deficits.append(dict(vertices=subset,neighbors=sorted(neighbors),deficiency=k-len(neighbors)))
    return deficits
def graph_json(left,right,variant='correct',segments=SEG):
    X,Y,E=graph(left,right,variant,segments)
    count=injections(X,E); bad=hall(X,E)
    need(bool(count)==(not bad),'Hall/injection disagreement')
    return dict(left=left,right=right,X=X,Y=Y,edges=[dict(x=x,y=E[x]) for x in X],injections=count,hall_obstructions=bad)

def multiply(p,q):
    result=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):result[i+j]+=a*b
    return result
def vanish_one(p):
    order=0
    while sum(p)==0:
        need(len(p)>1,'identically zero polynomial')
        # Synthetic division by z-1, ascending coefficients.
        q=[F(0)]*(len(p)-1);q[-1]=p[-1]
        for k in range(len(q)-2,-1,-1):q[k]=p[k+1]+q[k+1]
        need(-q[0]==p[0],'polynomial division')
        p=q;order+=1
    return order,sum(p)
def l_exponents(u,v):
    # Tensor of the two Steinberg monodromy blocks, after dualizing v.
    n=u[1]-u[0]+1;m=v[1]-v[0]+1
    c=F(sum(u)-sum(v),2)
    return tuple(c+F(n+m-2,2)-k for k in range(min(n,m)))
def germ(u,v,q,zeta):
    p=l_exponents(u,v); r=l_exponents(v,u)
    num=[F(1)];den=[F(1)]
    for h in r:
        need(h.denominator==1,'nonintegral exponent')
        for shift in (0,1):num=multiply(num,[-zeta*F(q)**(-h-shift),F(1)])
    for h in p:
        for shift in (0,1):den=multiply(den,[F(1),-zeta*F(q)**(-h-shift)])
    no,nv=vanish_one(num);do,dv=vanish_one(den)
    return dict(P=p,Q=r,order=no-do,leading=nv/dv,z_power=-2*len(r))

def main():
    sizes={n:b-a+1 for n,(a,b) in SEG.items()};need(sum(sizes.values())==15,'GL degree')
    interval_grid=[(a,b) for a in range(-2,4) for b in range(a,4)]
    for u,v in product(interval_grid,repeat=2):need(prec(u,v)==discrete_prec(u,v),'set/endpoint precedence disagreement')
    orders=('TDCBA','TCDBA','TDBCA')
    order_checks=[]
    for o in orders:
        checks=[dict(first=u,second=v,FLO_relation=flo(SEG[u],SEG[v])) for i,u in enumerate(o) for v in o[i+1:]]
        need(not any(x['FLO_relation'] for x in checks),'period basis hypothesis')
        order_checks.append(dict(order=o,checks=checks))
    linked=[('T','D'),('B','A'),('T','C'),('D','B'),('C','A')]
    need(all(prec(SEG[v],SEG[u]) for u,v in linked),'rank-one linkage orientation')
    rows=[]
    for u,v in combinations('TDCBA',2):
        for q,zeta in product((3,9),(1,-1)):
            g=germ(SEG[u],SEG[v],q,zeta)
            need(g['order']>=0,'unexpected pole in standard pair direction')
            if zeta==-1:need(g['order']==0 and g['leading']!=0,'eta unit')
            rows.append(dict(pair=u+v,q=q,zeta=zeta,**g))
    for u,v in linked:
        expected=1 if (u,v) in (('T','C'),('C','A')) else 2
        need(germ(SEG[u],SEG[v],3,1)['order']==expected,'linked zero order')
    nested=[]
    for u,v in (('D','C'),('C','B')):
        need(F(sum(SEG[u])-sum(SEG[v]),2)==F(1,2),'positive chamber')
        for q,zeta in product((3,9),(1,-1)):
            g=germ(SEG[u],SEG[v],q,zeta)
            expected={ (3,1):F(9,13),(3,-1):F(9,7),(9,1):F(81,91),(9,-1):F(81,73)}[(q,zeta)]
            need(g['order']==0 and g['leading']==expected,'nested exact unit')
            nested.append(dict(pair=u+v,q=q,zeta=zeta,value=expected))
    labels=[]
    for bits in product((0,1),repeat=4):
        e={'T':0,**dict(zip('DCBA',bits))}
        bad=[u+v for u,v in linked if e[u]==e[v]]
        need(bool(bad),'odd cycle surviving coordinate')
        labels.append(dict(labels=e,equal_edges=bad))
    prefix=[sum(all(e['labels'][u]!=e['labels'][v] for u,v in linked[:k]) for e in labels) for k in range(6)]
    need(prefix==[16,8,4,2,1,0],'coordinate eliminations')
    deletion_controls=[]
    for j in range(5):
        remaining=linked[:j]+linked[j+1:]
        survivors=[e['labels'] for e in labels if all(e['labels'][u]!=e['labels'][v] for u,v in remaining)]
        need(len(survivors)==1,'one-edge deletion did not restore a coloring')
        deletion_controls.append(dict(omitted_edge=linked[j],survivors=survivors))
    # Every graph is regenerated in both directions; no manuscript witness is input.
    partitions=[]
    for k in (1,2):
        for left in combinations(NAMES,k):
            right=tuple(n for n in NAMES if n not in left)
            need(ladder(left) or ladder(right),'one ladder side')
            graphs=[graph_json(left,right),graph_json(right,left)]
            need(any(g['injections']==0 for g in graphs),'unexcluded partition')
            need(any(len(h['vertices'])==1 for g in graphs for h in g['hall_obstructions']),'missing singleton witness')
            partitions.append(dict(left=left,right=right,left_ladder=ladder(left),right_ladder=ladder(right),graphs=graphs))
    need(len(partitions)==15,'partition count')
    # Exhaustive small endpoint universe calibrates arrows/shift on positive as well as negative cases.
    universe=[(a,b) for a in range(4) for b in range(a,4)]
    variants=('right_shift','shift_second','no_shift','reverse_both','reverse_first','reverse_second')
    distinguished={v:None for v in variants};small_cases=0
    # Two occurrences on each side permit nontrivial matchings and isolated obstructions.
    for data in combinations(universe,4):
        segments=dict(zip('wxyz',data))
        for left in combinations('wxyz',2):
            right=tuple(n for n in 'wxyz' if n not in left)
            g=graph_json(left,right,segments=segments); small_cases+=1
            for variant in variants:
                b=graph_json(left,right,variant,segments)
                if bool(g['injections'])!=bool(b['injections']) and distinguished[variant] is None:
                    distinguished[variant]=dict(segments=segments,correct=g,wrong=b)
    need(all(distinguished.values()),'undistinguished incorrect graph convention')
    result=dict(status='PASS',degree=15,lengths=sizes,orders=order_checks,germs=rows,nested_units=nested,
                coordinate_labels=labels,successive_coordinate_counts=prefix,partitions=partitions,
                positive_negative_small_graph_cases=small_cases,definition_controls=distinguished,
                discrete_set_endpoint_precedence_cases=len(interval_grid)**2,edge_deletion_controls=deletion_controls,
                no_candidate_imports=True,exact_rational_only=True,computes_Hom_space=False)
    print(json.dumps(result,indent=2,sort_keys=True,default=lambda x:str(x) if isinstance(x,F) else list(x)))

if __name__=='__main__':main()
