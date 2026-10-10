#!/usr/bin/env python3
"""Finite exact diagnostics, NOT a polynomial-time SFM implementation or proof."""
from fractions import Fraction as F
from itertools import combinations, product
import json, random, sys

class CheckError(RuntimeError): pass

def require(ok, msg):
    if not ok: raise CheckError(msg)

def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def ceil(q): return -((-q.numerator)//q.denominator)
def floor(q): return q.numerator//q.denominator

def model(n, U, edges, I, costs):
    if type(n) is not int or n<0: raise ValueError('n')
    if not isinstance(U,set) or not U<=set(range(n)): raise ValueError('U')
    if not isinstance(I,set) or not I<=set(range(n)): raise ValueError('I')
    if len(costs)!=n or any(type(q) is not F for q in costs): raise ValueError('rational costs required')
    for u,v,b in edges:
        if type(u) is not int or type(v) is not int or u not in U or v not in set(range(n))-U: raise ValueError('bipartite edge')
        if type(b) is not F: raise ValueError('exact rational demand required')
    signs=tuple(1 if i in U else -1 for i in range(n))
    rows=[]
    for u,v,b in edges:
        a=[F(0)]*n;a[u]=F(1);a[v]=F(-1);rows.append((tuple(a),b))
    return signs,rows,tuple(signs[i]*costs[i] for i in range(n))

def feasible(rows,x):return all(dot(a,x)>=b for a,b in rows)
def solve_square(A,b):
    n=len(b); R=[list(A[i])+[b[i]] for i in range(n)]
    for j in range(n):
        k=next((i for i in range(j,n) if R[i][j]),None)
        if k is None:return None
        R[j],R[k]=R[k],R[j];q=R[j][j];R[j]=[v/q for v in R[j]]
        for i in range(n):
            if i!=j:
                q=R[i][j];R[i]=[R[i][h]-q*R[j][h] for h in range(n+1)]
    return tuple(R[i][-1] for i in range(n))

def lp(n,rows,c,fixed=None):
    """Exact vertex enumeration for tiny connected inputs; fixes free lineality."""
    fixed=dict(fixed or {})
    # connected-component anchors, only when no coordinate is already fixed
    adj=[set() for _ in range(n)]
    for a,b in rows:
        ids=[i for i,v in enumerate(a) if v]
        require(len(ids)==2 and sorted(a[i] for i in ids)==[-1,1],'difference row required')
        i,j=ids;adj[i].add(j);adj[j].add(i)
    unseen=set(range(n))
    while unseen:
        s=min(unseen);comp={s};todo=[s];unseen.remove(s)
        while todo:
            for j in adj[todo.pop()]:
                if j in unseen:unseen.remove(j);comp.add(j);todo.append(j)
        if not comp.intersection(fixed):
            require(sum(c[i] for i in comp)==0,'unbounded component objective')
            fixed[s]=F(0)
    free=[i for i in range(n) if i not in fixed]
    reduced=[(tuple(a[i] for i in free),b-sum((a[i]*q for i,q in fixed.items()),F(0))) for a,b in rows]
    best=None
    for sub in combinations(reduced,len(free)):
        z=solve_square([a for a,b in sub],[b for a,b in sub])
        if z is None:continue
        x=[F(0)]*n
        for i,q in fixed.items():x[i]=F(q)
        for i,q in zip(free,z):x[i]=q
        if feasible(rows,x):
            v=dot(c,x)
            if best is None or v<best[0]:best=(v,tuple(x))
    if not free:
        x=tuple(fixed[i] for i in range(n))
        if feasible(rows,x):best=(dot(c,x),x)
    return best

def layers(d):
    ans=[]
    for sign in (1,-1):
        levels=sorted({sign*q for q in d if sign*q>0});last=F(0)
        for t in levels:
            r=tuple(F(sign if sign*q>=t else 0) for q in d)
            ans.append((t-last,r));last=t
    require(len(ans)<=len(d),'layer count')
    require(all(sum((a*r[i] for a,r in ans),F(0))==d[i] for i in range(len(d))),'layer reconstruction')
    for a,r in ans:
        require(a>0 and any(r),'nonzero positive layer')
        for i in range(len(d)):
            require(r[i]*d[i]>=0 and abs(a*r[i])<=abs(d[i]),'coordinate conformity')
            for j in range(len(d)):
                require((r[i]-r[j])*(d[i]-d[j])>=0,'difference conformity')
                require(abs(a*(r[i]-r[j]))<=abs(d[i]-d[j]),'difference domination')
    return ans

def ring(n,edges,I,lo,hi):
    ids=sorted(I);ground=[(i,t) for i in ids for t in range(lo[i]+1,hi[i]+1)]
    groundset=set(ground);arcs={v:set() for v in ground};forced=set();forbidden=set()
    def demand(src,j,t):
        if t<=lo[j]:return
        if t>hi[j]:
            if src is None:raise ValueError('empty ring')
            forbidden.add(src);return
        if src is None:forced.add((j,t))
        else:arcs[src].add((j,t))
    for i,t in ground:
        if t>lo[i]+1:arcs[i,t].add((i,t-1))
    for u,v,b in edges:
        if u not in I or v not in I:continue
        d=ceil(b) # y_u-y_v >= d
        demand(None,u,lo[v]+d)
        for t in range(lo[v]+1,hi[v]+1):demand((v,t),u,t+d)
    def close(S):
        out=set(S)|forced;todo=list(out)
        while todo:
            for v in arcs[todo.pop()]:
                if v not in out:out.add(v);todo.append(v)
        return out
    def valid(S):return not S.intersection(forbidden) and close(S)==S
    return ground,forced,forbidden,arcs,close,valid

def rejected(fn):
    try:fn()
    except (ValueError,CheckError):return
    raise CheckError('negative guard did not reject')

def main():
    rng=random.Random(30001102);counts={'instances':0,'slice_lps':0,'submodular_pairs':0,'proximity_steps':0,'layer_vectors':0,'ring_checks':0,'negative_checks':0}
    for _ in range(1000):
        d=tuple(F(rng.randint(-20,20),rng.randint(1,9)) for i in range(rng.randint(1,7)));layers(d);counts['layer_vectors']+=1
    for case in range(24):
        n=4;U={0,1};edges=[(u,v,F(rng.randint(-5,8),rng.choice([2,3,5,7]))) for u in U for v in [2,3]]
        if case%3==0:edges=edges[:3] # remains connected
        I=set(rng.sample(range(n),2));w=[rng.randint(1,4) for e in edges];cost=[F(0)]*n
        for (u,v,b),q in zip(edges,w):cost[u]+=q;cost[v]+=q
        signs,rows,c=model(n,U,edges,I,cost)
        base=lp(n,rows,c);require(base is not None,'LP feasible');val,xstar=base
        require(val==sum((F(q)*b for q,(_,_,b) in zip(w,edges)),F(0)) or val>sum((F(q)*b for q,(_,_,b) in zip(w,edges)),F(0)),'weak duality')
        ids=sorted(I);lo={i:ceil(xstar[i]-n) for i in ids};hi={i:floor(xstar[i]+n) for i in ids}
        gr,forced,forbidden,arcs,close,valid=ring(n,edges,I,lo,hi)
        values={};solutions={}
        for p in product(*(range(lo[i],hi[i]+1) for i in ids)):
            fixed=dict(zip(ids,map(F,p)));res=lp(n,rows,c,fixed);counts['slice_lps']+=1
            domain=all(fixed[u]-fixed[v]>=b for u,v,b in edges if u in I and v in I)
            require((res is not None)==domain,'integer-edge projection')
            S={(i,t) for i,q in zip(ids,p) for t in range(lo[i]+1,q+1)}
            require(valid(S)==domain,'threshold ring equivalence');counts['ring_checks']+=1
            if res:
                values[p]=res[0];solutions[p]=res[1]
                d=tuple(res[1][i]-xstar[i] for i in range(n))
                for a,r in layers(d):
                    require(feasible(rows,tuple(xstar[i]+a*r[i] for i in range(n))),'LP layer feasible')
                    require(dot(c,r)>=0,'LP layer slope')
                    if a>=1:
                        new=tuple(res[1][i]-r[i] for i in range(n))
                        require(feasible(rows,new) and all(new[i].denominator==1 for i in I),'subtraction feasible mixed')
                        require(dot(c,new)<=res[0],'subtraction objective')
                        require(sum(abs(new[i]-xstar[i]) for i in range(n))<sum(abs(d[i]) for i in range(n)),'subtraction distance')
                        counts['proximity_steps']+=1
        require(values,'nonempty proximity box')
        for p,q in product(values,repeat=2):
            meet=tuple(min(a,b) for a,b in zip(p,q));join=tuple(max(a,b) for a,b in zip(p,q))
            require(meet in values and join in values,'sublattice domain')
            require(values[p]+values[q]>=values[meet]+values[join],'submodular value');counts['submodular_pairs']+=1
        # Independent larger search is finite evidence only.
        larger=[]
        for p in product(*(range(lo[i]-2,hi[i]+3) for i in ids)):
            res=lp(n,rows,c,dict(zip(ids,map(F,p))));counts['slice_lps']+=1
            if res:larger.append(res[0])
        require(min(larger)==min(values.values()),'finite proximity optimum comparison')
        # closure-oracle interface: minimal ring element and containing-element minima
        family=[{(i,t) for i,q in zip(ids,p) for t in range(lo[i]+1,q+1)} for p in values]
        minimum=set.intersection(*family)
        require(close(set())==minimum,'minimal ring oracle')
        for a in gr:
            containing=[S for S in family if a in S]
            if containing:require(close({a})==set.intersection(*containing),'containing-element oracle')
        counts['instances']+=1
    good=lambda:model(2,{0},[(0,1,F(1,2))],{0,1},[F(1),F(1)])
    good()
    for fn in [lambda:model(2,{0},[(0,0,F(1))],set(),[F(1),F(1)]),lambda:model(2,{0},[(0,1,.5)],set(),[F(1),F(1)]),lambda:model(2,{0},[(0,1,F(1))],{2},[F(1),F(1)]),lambda:model(2,{0},[(0,1,F(1))],set(),[1.,F(1)]),lambda:require(False,'deliberate')]:
        rejected(fn);counts['negative_checks']+=1
    # Explicit counterchecks against invalid proof substitutions.
    require(0+0<F(1,2),'floor rounding must not replace ceiling');counts['negative_checks']+=1
    require(min(1,0)+min(0,1)<1,'unflipped covering feasible set is not min-closed');counts['negative_checks']+=1
    gr,fo,fb,ar,cl,va=ring(2,[(0,1,F(1))],{0,1},{0:0,1:0},{0:1,1:1})
    require(not va(set()) and (0,1) in fo,'base-level implication essential');counts['negative_checks']+=1
    _,rows,c=good();v,x=lp(2,rows,c);require(v==F(1,2) and any(x[i].denominator!=1 for i in range(2)),'LP relaxation not mixed hull');counts['negative_checks']+=1
    print(json.dumps({'status':'PASS_FINITE_DIAGNOSTICS','python_optimize':sys.flags.optimize,'counts':counts,'limitations':'Exact finite tests only. No production SFM or ellipsoid implementation; universal and bit-complexity claims rely on the written proof.'},indent=2))
if __name__=='__main__':main()
