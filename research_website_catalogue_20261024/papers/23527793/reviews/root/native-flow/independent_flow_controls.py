#!/usr/bin/env python3
"""Fresh exact primal/dual controls; imports no author or prior-review code."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from collections import deque
import json, random

OUT=Path(__file__).resolve().parent

def maxflow(d):
    """Rational Dinic; return a primal matrix and residual-cut dual witness."""
    k=len(d); s=2*k; z=s+1; n=z+1
    original=[[Q(0) for _ in range(n)] for _ in range(n)]
    for i in range(k):
        original[s][i]=2*k; original[k+i][z]=2*k
        for j in range(k):original[i][k+j]=d[i][j]
    residual=[r.copy() for r in original]; value=Q(0)
    while True:
        level=[-1]*n;level[s]=0;q=deque([s])
        while q:
            u=q.popleft()
            for v in range(n):
                if level[v]<0 and residual[u][v]>0:
                    level[v]=level[u]+1;q.append(v)
        if level[z]<0:break
        nxt=[0]*n
        def push(u,amount):
            if u==z:return amount
            while nxt[u]<n:
                v=nxt[u]
                if residual[u][v]>0 and level[v]==level[u]+1:
                    got=push(v,min(amount,residual[u][v]))
                    if got:
                        residual[u][v]-=got;residual[v][u]+=got
                        return got
                nxt[u]+=1
            return Q(0)
        while True:
            got=push(s,Q(2*k*k))
            if not got:break
            value+=got
    reach={s};todo=[s]
    while todo:
        u=todo.pop()
        for v in range(n):
            if v not in reach and residual[u][v]>0:reach.add(v);todo.append(v)
    assert z not in reach
    dual=sum(original[u][v] for u in reach for v in range(n) if v not in reach)
    y=[[original[i][k+j]-residual[i][k+j] for j in range(k)] for i in range(k)]
    assert dual==value==sum(map(sum,y))
    assert all(0<=y[i][j]<=d[i][j] for i in range(k) for j in range(k))
    assert all(sum(r)<=2*k for r in y)
    assert all(sum(y[i][j] for i in range(k))<=2*k for j in range(k))
    return value,y

def cut_lines(x):
    k=len(x);ls=[]
    for mask in range(1<<(2*k)):
        A=[i for i in range(k) if mask&(1<<i)]
        B=[j for j in range(k) if mask&(1<<(k+j))]
        rectangle=[(i,j) for i in A for j in range(k) if j not in B]
        ls.append((Q(2*k*(k-len(A)+len(B))+len(rectangle)),sum((x[i][j] for i,j in rectangle),Q(0))))
    return ls

def envelope(ls,t):
    val=min(b+(t-1)*m for b,m in ls)
    active=[m for b,m in ls if b+(t-1)*m==val]
    return val,min(active),max(active)

def physical(k,y):
    """Use binary-word edges, unlike the frozen heap/BFS implementations."""
    assert k>=2 and k&(k-1)==0
    bits=k.bit_length()-1;H=bits+1
    leaves0=['0'+format(i,'0'+str(bits)+'b') for i in range(k)]
    leaves1=['1'+format(i,'0'+str(bits)+'b') for i in range(k)]
    edges=[''.join(e) for depth in range(1,H+1) for e in product('01',repeat=depth)]
    load={e:Q(0) for e in edges};capacity={e:Q(2*k*sum(w.startswith(e) for w in leaves0+leaves1)) for e in edges}
    for i,j in product(range(k),repeat=2):
        route=[leaves0[i][:a] for a in range(1,H+1)]+[leaves1[j][:a] for a in range(1,H+1)]
        assert len(set(route))==2*H
        for e in route:load[e]+=y[i][j]
    assert len(edges)==4*k-2
    assert all(load[e]<=capacity[e] for e in edges)
    # Independently verify each load equals the advertised terminal subtotal.
    for e in edges:
        expected=sum(sum(y[i]) for i,w in enumerate(leaves0) if w.startswith(e))
        expected+=sum(sum(y[i][j] for i in range(k)) for j,w in enumerate(leaves1) if w.startswith(e))
        assert load[e]==expected
    return load,capacity

def demands(x,t):return [[1+(t-1)*v for v in row] for row in x]

def main():
    cases=0;kinks=0;primal_duals=0;physical_edges=0;phase_unique=0
    for flat in product([Q(1,7),Q(1),Q(7)],repeat=4):
        x=[list(flat[:2]),list(flat[2:])];ls=cut_lines(x)
        for t in [Q(1),Q(5,4),Q(3,2),Q(2),Q(5,2),Q(4)]:
            d=demands(x,t);v,y=maxflow(d);assert v==envelope(ls,t)[0]
            loads,caps=physical(2,y);physical_edges+=len(loads);primal_duals+=1;cases+=1
            strict=all(sum(row)<4 for row in d) and all(sum(d[i][j] for i in range(2))<4 for j in range(2))
            if strict:
                assert v==sum(map(sum,d)) and y==d and all(loads[e]<caps[e] for e in loads);phase_unique+=1
            if v==8:assert all(loads[e]==caps[e] for e in loads)
        intersections={Q(1)}
        for b,m in ls:
            for c,n in ls:
                if m!=n:
                    t=1+(c-b)/(m-n)
                    if t>=1:intersections.add(t)
        ordered=sorted(intersections)
        for i,t in enumerate(ordered):
            value,right,left=envelope(ls,t)
            if right==left:continue
            gaps=[Q(1,100)]
            if i:gaps.append((t-ordered[i-1])/3)
            if i+1<len(ordered):gaps.append((ordered[i+1]-t)/3)
            h=min(gaps);assert (envelope(ls,t+h)[0]-value)/h==right
            if t>1:assert (value-envelope(ls,t-h)[0])/h==left
            assert maxflow(demands(x,t))[0]==value;kinks+=1;primal_duals+=1

    rng=random.Random(202610210397)
    for k in [4,8]:
        for rep in range(12):
            x=[[Q(rng.randrange(1,100),13) for _ in range(k)] for _ in range(k)]
            max_terminal=max(max(map(sum,x)),max(sum(x[i][j] for i in range(k)) for j in range(k)))
            low=1+Q(k,2)/max_terminal
            high=1+1/min(min(row) for row in x)
            for t,kind in [(low,'low'),(high,'high')]:
                d=demands(x,t);v,y=maxflow(d);loads,caps=physical(k,y);physical_edges+=len(loads);primal_duals+=1;cases+=1
                if kind=='low':
                    assert y==d and all(loads[e]<caps[e] for e in loads);phase_unique+=1
                else:
                    assert v==2*k*k and all(loads[e]==caps[e] for e in loads)

    # Independent critical tie and entry-slope normalization controls.
    ties=[]
    for k in [2,4]:
        for rate in [Q(1,3),Q(1),Q(7)]:
            x=[[rate]*k for _ in range(k)];t=1+1/rate
            value,right,left=envelope(cut_lines(x),t)
            assert value==2*k*k and right==0 and left==k*k*rate
            ties.append({'k':k,'rate':str(rate),'t':str(t),'right_marginal':0,'left_marginal':1})
    x=[[Q(1,7),Q(2,7)],[Q(3,7),Q(4,7)]];S=sum(map(sum,x))
    value,right,_=envelope(cut_lines(x),Q(1));assert right==S and right/S==1 and right/4!=1

    # Optimizer dependence in the excluded region, constructed without LP.
    d=[[Q(4),Q(4)],[Q(6,5),Q(6,5)]]
    y1=[[Q(14,5),Q(6,5)],[Q(6,5),Q(6,5)]]
    y2=[[Q(2),Q(2)],[Q(6,5),Q(6,5)]]
    v=maxflow(d)[0];assert v==Q(32,5)==sum(map(sum,y1))==sum(map(sum,y2))
    counts=[]
    for y in [y1,y2]:
        assert all(y[i][j]<=d[i][j] for i,j in product(range(2),repeat=2))
        loads,caps=physical(2,y);counts.append(sum(loads[e]<caps[e] for e in loads))
    assert counts[0]!=counts[1]

    # A new mixed-cut witness with all terminal offered totals above capacity.
    d=[[Q(3),Q(3),Q(11,10),Q(13,10)] for _ in range(3)]+[[Q(6,5),Q(6,5),Q(5),Q(5)]]
    assert all(sum(row)>8 for row in d) and all(sum(d[i][j] for i in range(4))>8 for j in range(4))
    v,y=maxflow(d);assert v==Q(156,5)<32
    assert sum(d[i][j] for i in range(3) for j in [2,3])==Q(36,5)<8
    physical(4,y)
    report={'all_assertions_passed':True,'no_candidate_or_prior_review_code_imported':True,
        'exact_rational_flow_instances':cases,'exact_primal_dual_certificates':primal_duals,
        'true_envelope_kinks':kinks,'physical_edge_identities_checked':physical_edges,
        'strict_full_demand_cases':phase_unique,'tie_controls':ties,
        'baseline_vs_actual_slope_control':{'actual_slope':str(S),'baseline':4,'normalized_right_marginal':'1'},
        'excluded_region_optimizer_spare_counts':counts,
        'mixed_cut_witness':{'all_terminal_totals_above_capacity':True,'maximum_total':str(v),'global_capacity':32,'violating_rectangle_demand':'36/5','required':8},
        'scope':'Exact controls supplement independent general proof; neither novelty nor source-model adequacy follows from finite tests.'}
    (OUT/'INDEPENDENT_FLOW_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
