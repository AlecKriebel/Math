#!/usr/bin/env python3
"""Independent controls transcribed from published formulas; no project imports."""
from fractions import Fraction as F
from itertools import product, permutations
from collections import Counter
from pathlib import Path
import json, hashlib, random

N=19
ZERO=(0,)*N
def add(a,b):
    r=a.copy()
    for m,c in b.items():
        r[m]=r.get(m,0)+c
        if not r[m]: del r[m]
    return r
def scale(a,k): return {m:c*k for m,c in a.items() if c*k}
def mul(a,b):
    r={}
    for m,c in a.items():
        for n,d in b.items():
            z=tuple(x+y for x,y in zip(m,n));r[z]=r.get(z,0)+c*d
    return {m:c for m,c in r.items() if c}
def prod(xs):
    r={ZERO:1}
    for x in xs:r=mul(r,x)
    return r
def var(i):
    z=list(ZERO);z[i]=1;return {tuple(z):1}
ONE={ZERO:1}
E=[[ONE]+[var(3*i+j) for j in range(3)] for i in range(6)]
lam=var(18); mu=mul(lam,add(ONE,scale(lam,-1)))
chars=[(x,y,x^y) for x in range(4) for y in range(4)]
names=[''.join('0CGT'[v] for v in h) for h in chars]
a,b,c,d,e,f=E
triangle={name:mul(prod([a[x],b[y],c[z]]),add(prod([lam,f[y],d[z]]),prod([add(ONE,scale(lam,-1)),f[x],e[z]]))) for name,(x,y,z) in zip(names,chars)}
tree={name:prod([a[x],b[y],c[z]]) for name,(x,y,z) in zip(names,chars)}
circuits=[(('000','CGT','GTC'),('0TT','C0C','GG0')), (('000','CTG','TGC'),('0GG','C0C','TT0')), (('000','GCT','TGC'),('0CC','GG0','T0T')), (('000','GTC','TCG'),('0CC','G0G','TT0')), (('000','CTG','GCT'),('0TT','CC0','G0G')), (('000','CGT','TCG'),('0GG','CC0','T0T'))]
def diff(x,y):return add(x,scale(y,-1))
arms=[prod([a[1],a[2],b[2],b[3],c[1],c[3]]),prod([a[1],a[3],b[2],b[3],c[1],c[2]]),prod([a[2],a[3],b[1],b[2],c[1],c[3]]),prod([a[2],a[3],b[1],b[3],c[1],c[2]]),prod([a[1],a[2],b[1],b[3],c[2],c[3]]),prod([a[1],a[3],b[1],b[2],c[2],c[3]])]
factors=[(1,diff(mul(f[1],f[3]),f[2]),diff(mul(d[1],e[3]),prod([d[3],e[1],f[2]]))), (1,diff(mul(f[1],f[2]),f[3]),diff(mul(d[1],e[2]),prod([d[2],e[1],f[3]]))),(-1,diff(mul(f[1],f[3]),f[2]),diff(prod([d[1],e[3],f[2]]),mul(d[3],e[1]))),(-1,diff(mul(f[1],f[2]),f[3]),diff(prod([d[1],e[2],f[3]]),mul(d[2],e[1]))),(-1,diff(f[1],mul(f[2],f[3])),diff(mul(d[2],e[3]),prod([d[3],e[2],f[1]]))), (1,diff(f[1],mul(f[2],f[3])),diff(prod([d[2],e[3],f[1]]),mul(d[3],e[2])))]
qterms=[(1,('000','CGT','GTC','TCG')),(-1,('000','CTG','GCT','TGC')),(-1,('0CC','CGT','G0G','TT0')),(1,('0CC','CTG','GG0','T0T')),(1,('0GG','C0C','GCT','TT0')),(-1,('0GG','CC0','GTC','T0T')),(-1,('0TT','C0C','GG0','TCG')),(1,('0TT','CC0','G0G','TGC'))]
def ev(p,x):return sum(F(v)*__import__('math').prod(x[i]**k for i,k in enumerate(m) if k) for m,v in p.items())
def deriv(p,j):return {m[:j]+(m[j]-1,)+m[j+1:]:c*m[j] for m,c in p.items() if m[j]}
def det(A):
    A=[list(map(F,row)) for row in A];ans=F(1)
    for i in range(len(A)):
        pivot=next((j for j in range(i,len(A)) if A[j][i]),None)
        if pivot is None:return F(0)
        if pivot!=i:A[i],A[pivot]=A[pivot],A[i];ans=-ans
        p=A[i][i];ans*=p
        for j in range(i+1,len(A)):
            t=A[j][i]/p
            for k in range(i+1,len(A)):A[j][k]-=t*A[i][k]
    return ans
def rank(A):
    A=[list(map(F,row)) for row in A];r=0
    for c in range(len(A[0])):
        p=next((j for j in range(r,len(A)) if A[j][c]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];v=A[r][c]
        for j in range(r+1,len(A)):
            t=A[j][c]/v
            for k in range(c,len(A[0])):A[j][k]-=t*A[r][k]
        r+=1
        if r==len(A):break
    return r
def strict(t,ct=False):
    c,g,h=t
    return min(c,g,h,1-c,1-g,1-h,1+c-g-h,1-c+g-h,1-c-g+h)>0 and (not ct or min(c-g*h,g-c*h,h-c*g)>0)

def rootings(edges,retics,leaves):
    # Each edge is (u,v,arrowhead_at_v); for the present examples no double heads.
    V={x for a,b,_ in edges for x in (a,b)};result=[]
    for rootedge,(a,b,head) in enumerate(edges):
        fixed=[(u,v) for i,(u,v,h) in enumerate(edges) if i!=rootedge and h]+[('ROOT',a),('ROOT',b)]
        ordinary=[(u,v) for i,(u,v,h) in enumerate(edges) if i!=rootedge and not h]
        for choices in product((0,1),repeat=len(ordinary)):
            arcs=fixed+[(v,u) if flip else (u,v) for (u,v),flip in zip(ordinary,choices)]
            parents={v:set() for v in V|{'ROOT'}}; children={v:set() for v in V|{'ROOT'}}
            for u,v in arcs:children[u].add(v);parents[v].add(u)
            if any((len(parents[v]),len(children[v])) != ((0,2) if v=='ROOT' else (1,0) if v in leaves else (2,1) if v in retics else (1,2)) for v in parents):continue
            order=[];waiting=set(parents)
            while waiting:
                nxt=[v for v in waiting if parents[v]<=set(order)]
                if not nxt:break
                order.extend(nxt);waiting-=set(nxt)
            if waiting:continue
            dom={'ROOT':{'ROOT'}}
            for v in order[1:]:dom[v]={v}|set.intersection(*(dom[p] for p in parents[v]))
            if set.intersection(*(dom[v] for v in leaves))!={'ROOT'}:continue
            tc=all(any(w not in retics for w in children[v]) for v in children if v not in leaves)
            result.append({'root_edge':[a,b],'tree_child':tc,'arcs':arcs})
    return result

def main():
    report={'method':'Independent standard-library sparse polynomial, rational matrix, and exhaustive oriented-graph controls. No supplied checker or stored conclusions imported.'}
    expanded=[]
    for j,((left,right),(sign,p1,p2),arm) in enumerate(zip(circuits,factors,arms)):
        computed=diff(prod([triangle[n] for n in left]),prod([triangle[n] for n in right]))
        assert computed==scale(prod([mu,arm,p1,p2]),sign),j
        assert not diff(prod([tree[n] for n in left]),prod([tree[n] for n in right]))
        expanded.append(computed)
    report['six_circuits_exact_pullback_terms']=[len(p) for p in expanded]
    q0=[F(1,2)]*15+[F(1,3)]*3+[F(1,2)]
    values={n:ev(p,q0) for n,p in triangle.items()}
    expected={n:F(1) if n=='000' else F(1,12) if '0' in n else F(1,48) for n in names}
    assert values==expected
    h14checks=[]
    for perm in permutations(range(3)):
        oriented={n:triangle[''.join(n[i] for i in perm)] for n in names}
        pullback={}
        for sign,mon in qterms:pullback=add(pullback,scale(prod([oriented[n] for n in mon]),sign))
        assert not pullback,perm
        J=[[ev(deriv(oriented[n],j),q0) for j in range(N)] for n in names[1:]]
        assert rank(J)==14
        h14checks.append({'port_permutation':perm,'exact_pullback_zero':True,'rank':14})
    report['h14_six_port_permutations']=h14checks
    rows=[1,2,3,4,6,8,7,10,12,9,13,5,11,15];cols=[0,1,2,3,4,5,6,7,8,9,10,15,16,17]
    D=det([[ev(deriv(triangle[names[i]],j),q0) for j in cols] for i in rows])
    assert D==F(-1,760840571584512);report['printed_triangle_minor']=str(D)
    gradient=[]
    for n in names[1:]:
        dval=F(0)
        for sign,mon in qterms:
            for k,v in enumerate(mon):
                if v==n:dval+=sign*__import__('math').prod(values[z] for i,z in enumerate(mon) if i!=k)
        gradient.append(dval)
    assert Counter(abs(v) for v in gradient)==Counter({F(0):9,F(1,6912):6})
    report['h14_gradient_nonzero_values']=[str(x) for x in gradient if x]
    rng=random.Random(22178672);tested=0;nonct=0
    for _ in range(200):
        params=[]
        for i in range(6):
            while True:
                t=[F(rng.randrange(1,29),30) for _ in range(3)]
                if strict(t):break
            nonct+=not strict(t,True);params.extend(t)
        params.append(F(rng.randrange(1,20),20))
        assert any(ev(p,params) for p in expanded)
        tested+=1
    report['exact_sample_separator_controls']={'samples':tested,'non_CT_edges_in_strict_principal_domain':nonct,'all_separated':True,'scope':'Samples supplement, do not replace, the printed algebraic proof.'}
    boundary=q0.copy();boundary[-1]=0
    assert all(ev(p,boundary)==0 for p in expanded)
    report['inheritance_boundary_negative_control']='At lambda=0 all six vanish as expected; strict inheritance is essential.'
    W=[('S','U',False),('S','V',True),('U','X',True),('V','Z',False),('Z','X',True),('U','V',True),('Z','L1',False),('X','L2',False),('L0','S',False)]
    WP=[('S','U',False),('S','X0',True),('V','X0',True),('U','X1',True),('V','X1',True),('U','V',False),('X0','L1',False),('X1','L2',False),('L0','S',False)]
    leaf={'L0','L1','L2'}
    out={}
    for label,edges,retics,expected_census in [('W',W,{'V','X'},(5,2,3)),('Wprime',WP,{'X0','X1'},(7,2,5))]:
        rs=rootings(edges,retics,leaf);tc=sum(r['tree_child'] for r in rs)
        census=(len(rs),tc,len(rs)-tc);assert census==expected_census
        out[label]={'census':census,'rootings':rs}
    report['independent_rooting_censuses']=out
    iw=sorted({v for a,b,_ in W for v in (a,b)}-leaf);ip=sorted({v for a,b,_ in WP for v in (a,b)}-leaf)
    target={frozenset((a,b)) for a,b,_ in WP};iso=[]
    for p in permutations(ip):
        tr=dict(zip(iw,p));tr.update({v:v for v in leaf})
        if {frozenset((tr[a],tr[b])) for a,b,_ in W}==target:iso.append(tr)
    assert not iso;report['underlying_labelled_graph_nonisomorphism']={'internal_vertex_bijections':__import__('math').factorial(len(iw)),'isomorphisms':0}
    u=[F(2,5),F(4,9),F(3,7)];v=[F(3,7),F(5,11),F(4,9)]
    assert strict(u,True) and strict(v,True)
    cherry=F(8)*__import__('math').prod(u)/__import__('math').prod(v)
    assert cherry==F(176,25);report['cherry_determinant']=str(cherry)
    report['all_controls_pass']=True
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='independent_rooting_censuses'},indent=2))
if __name__=='__main__':main()
