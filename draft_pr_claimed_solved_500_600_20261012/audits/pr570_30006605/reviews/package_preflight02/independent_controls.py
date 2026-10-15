#!/usr/bin/env python3
"""Fresh exact controls. No imports of candidate, prior review, or replay code."""
from fractions import Fraction as F
from collections import deque,Counter
from itertools import combinations,product
from pathlib import Path
import random,math,json,hashlib
HERE=Path(__file__).resolve().parent
stats=Counter()

def distances(adj):
    ds=[]
    for v in range(len(adj)):
        d=[-1]*len(adj);d[v]=0;q=deque([v])
        while q:
            x=q.popleft()
            for y in adj[x]:
                if d[y]<0:d[y]=d[x]+1;q.append(y)
        assert all(x>=0 for x in d)
        ds.append(d)
    return ds

def triple_check(d):
    n=len(d)
    intervals=[[{z for z in range(n) if d[x][z]+d[z][y]==d[x][y]} for y in range(n)] for x in range(n)]
    for x,y,z in combinations(range(n),3):
        assert len(intervals[x][y]&intervals[y][z]&intervals[x][z])==1
        stats['median_triples']+=1

def graph(n,edges):
    a=[set() for _ in range(n)]
    for x,y in edges:a[x].add(y);a[y].add(x)
    return a

def cube(k):
    return graph(1<<k,[(x,x^(1<<j)) for x in range(1<<k) for j in range(k) if not x&(1<<j)])

def pendant(a,v,count):
    a=[set(x) for x in a];old=len(a)
    a.extend({v} for _ in range(count));a[v].update(range(old,old+count));return a

def budget(w,R,D):
    lo,hi=0,D+1
    while hi-lo>1:
        k=(hi+lo)//2
        if k*w<=R:lo=k
        else:hi=k
    return lo

def decision(d,w,R):
    if R<0:return []
    D=len(w)-1
    b=[budget(v,R,D) for v in w]
    assert all(0<=x<=D for x in b)
    labels=[D-v for v in b]
    return [x for x in range(len(w)) if max(d[x][u]+labels[u] for u in range(len(w)))<=D]

def search(w, feasible, optimum, choose_high=False, save=True):
    n=len(w);D=n-1;B=D*max(w)
    if B==0:assert optimum==0;return B
    rows=[[0,D] for _ in w]
    calls=0
    while True:
        lengths=[max(0,h-l+1) for l,h in rows];M=sum(lengths)
        if M==0:break
        if save:assert B==optimum or any(any(k*w[u]==optimum for k in range(l,h+1)) for u,(l,h) in enumerate(rows))
        mids=sorted((w[u]*((l+h)//2),lengths[u]) for u,(l,h) in enumerate(rows) if lengths[u])
        q=None
        acc=0
        for value,mass in (reversed(mids) if choose_high else mids):
            acc+=mass
            if 2*acc>=M:q=value;break
        assert q is not None
        yes=feasible(q)
        if yes and save:B=min(B,q)
        for u,(l,h) in enumerate(rows):
            if l>h:continue
            low,high=l,h+1
            while low<high:
                k=(low+high)//2
                # First >=q when feasible; first >q when infeasible.
                pred=(k*w[u]>=q) if yes else (k*w[u]>q)
                if pred:high=k
                else:low=k+1
            rows[u]=[l,low-1] if yes else [low,h]
        left=sum(max(0,h-l+1) for l,h in rows)
        assert 4*(M-left)>=M
        stats['pivots']+=1;calls+=1
        assert calls<=math.ceil(math.log(n*n,4/3))+1
    if save:assert B==optimum
    return B

def cuts(vertices,d):
    result=set()
    for u,v in combinations(vertices,2):
        if d[u][v]!=1:continue
        a=frozenset(x for x in vertices if d[x][u]<d[x][v]);b=vertices-a
        assert a and b and a|b==vertices
        pair=tuple(sorted((tuple(sorted(a)),tuple(sorted(b)))))
        result.add(pair)
    return [(set(a),set(b)) for a,b in sorted(result)]

def gate(x,H,d):
    q=min(H,key=lambda z:d[x][z])
    assert all(d[x][q]+d[q][y]==d[x][y] for y in H)
    assert [z for z in H if d[x][z]==d[x][q]]==[q]
    stats['gate_factorizations']+=len(H)
    return q

def source_recursion(d,a,V=None,depth=0,rootN=None):
    if V is None:V=set(range(len(a)))
    s=len(V);assert s>0
    if rootN is None:rootN=s
    stats['source_nodes']+=1
    stats['max_source_depth']=max(stats['max_source_depth'],depth)
    direct={x:max(d[x][u]+a[u] for u in V) for x in V}
    if s<=2:stats['source_base']+=1;return direct
    f=2*(s-1).bit_length()
    options=cuts(V,d)
    bal=[(A,B) for A,B in options if f*min(len(A),len(B))>=s]
    if bal:
        stats['source_balanced']+=1
        A,B=bal[0]
        assert len(A)+len(B)==s and max(len(A),len(B))*f<=s*(f-1)
        eA=source_recursion(d,a,A,depth+1,rootN);eB=source_recursion(d,a,B,depth+1,rootN)
        result={}
        for H,K,eH,eK in [(A,B,eA,eB),(B,A,eB,eA)]:
            for x in H:
                g=gate(x,K,d)
                result[x]=max(eH[x],d[x][g]+eK[g])
    else:
        stats['source_unbalanced']+=1
        minorities=[A if len(A)<len(B) else B for A,B in options]
        base=V-set().union(*minorities)
        assert len(base)==1
        v0=next(iter(base))
        umax=max(sorted(V),key=lambda u:d[v0][u]+a[u])
        if direct[v0]==a[v0]:umax=v0
        if umax==v0:
            stats['source_dominance']+=1
            result={x:d[x][v0]+a[v0] for x in V}
        else:
            ladder=[H for H in minorities if umax in H and any(d[v0][y]==1 for y in H)]
            assert ladder and len(ladder)<=(s-1).bit_length()
            # Incident ladder classes contain every cube corner (orthogonality test).
            for mask in range(1<<len(ladder)):
                corner=[x for x in V if d[v0][x]==mask.bit_count() and all((x in H)==bool(mask&(1<<j)) for j,H in enumerate(ladder))]
                assert len(corner)==1
            remaining=set(V);slices=[]
            for H in ladder:
                S=remaining&H;remaining-=S
                assert S and len(S)*f<s
                slices.append(S)
            assert 2*sum(map(len,slices))<=s
            result={x:d[x][v0]+direct[v0] for x in remaining}
            assert all(d[x][umax]==d[x][v0]+d[v0][umax] for x in remaining)
            remainders=[];G=set(V)
            for S in slices:
                outside=G-S
                wstar=dict(a)
                fibers={x:[] for x in S}
                for y in outside:fibers[gate(y,S,d)].append(y)
                for x,Fx in fibers.items():
                    if Fx:
                        wstar[x]=max(d[x][y]+a[y] for y in Fx)
                        if wstar[x]<a[x]:stats['fiber_below_original']+=1
                    else:wstar[x]=a[x]
                e=source_recursion(d,a,S,depth+1,rootN)
                es=source_recursion(d,wstar,S,depth+1,rootN)
                remainders.append((S,outside,e,es));G=outside
            later={}
            for S,outside,e,es in reversed(remainders):
                for x in later:
                    g=gate(x,S,d);later[x]=max(later[x],d[x][g]+e[g])
                later.update({x:max(e[x],es[x]) for x in S})
            result.update(later)
    assert result==direct,(V,a,result,direct)
    return result

def main():
    rng=random.Random(13757002)
    graphs=[('Q'+str(k),cube(k)) for k in range(6)]
    graphs += [('P'+str(n),graph(n,[(j,j+1) for j in range(n-1)])) for n in (3,4,7,12)]
    graphs += [('star'+str(n),graph(n,[(0,j) for j in range(1,n)])) for n in (7,11,22)]
    graphs += [('Q2_pendant22',pendant(cube(2),0,18)),('Q3_pendant50',pendant(cube(3),0,42)),('grid3x3',graph(9,[(3*x+y,3*x+y+1) for x in range(3) for y in range(2)]+[(3*x+y,3*(x+1)+y) for x in range(2) for y in range(3)]))]
    # A gated vertex amalgam of Q3 and Q2, plus a pendant at a nonbase cube vertex.
    mix=cube(3)
    mix.extend([set(),set(),set()])
    for x,y in ((0,8),(0,9),(8,10),(9,10)):mix[x].add(y);mix[y].add(x)
    graphs.append(('amalgam',pendant(mix,5,3)))
    records=[]
    for name,adj in graphs:
        n=len(adj);d=distances(adj);triple_check(d)
        profiles=[[F(0)]*n,[F(1)]*n,[F(int(i==0)) for i in range(n)],[F(int(i==n-1))*10**40 for i in range(n)],
                  [F(i%2) for i in range(n)],[F(2**257+i,3**29+i) for i in range(n)],
                  [F(0) if i%3==0 else F(1+i,2**128+3*i+1) for i in range(n)]]
        for _ in range(11):profiles.append([rng.choice([F(0),F(1,7),F(1),F(3,2),F(10**30)]) for _ in range(n)])
        for w in profiles:
            radii=[max(w[u]*d[x][u] for u in range(n)) for x in range(n)]
            rho=min(radii);centers=[x for x,v in enumerate(radii) if v==rho]
            for high in (False,True):assert search(w,lambda R:bool(decision(d,w,R)),rho,high)==rho
            candidates=sorted({k*w[u] for u in range(n) for k in range(n)})
            selected=[F(-1),F(0),rho,rho+F(1,17),rho-F(1,17),candidates[-1]]
            selected += candidates if len(candidates)<=25 else [candidates[j*len(candidates)//12] for j in range(12)]
            for R in set(selected):
                got=decision(d,w,R);expected=[x for x,v in enumerate(radii) if v<=R]
                assert got==expected
                stats['threshold_vectors']+=1
            assert decision(d,w,rho)==centers
            stats['graph_profiles']+=1
        for j in range(8):
            a={x:(10 if j==0 and x==n-1 else 1000 if j==1 and x==0 else 0 if j<2 else rng.randrange(0,25)) for x in range(n)}
            source_recursion(d,a)
            stats['source_profiles']+=1
        records.append({'graph':name,'n':n,'m':sum(map(len,adj))//2,'median_checked':True,'profiles':len(profiles)})
    # Abstract sorted-row optimization includes every attained threshold, independent of graph structure.
    for n in range(1,7):
        for w in product((F(0),F(1,3),F(1)),repeat=n):
            candidates=sorted({k*u for u in w for k in range(n)})
            for target in candidates:
                for high in (False,True):search(w,lambda q:q>=target,target,high)
                stats['abstract_optimizations']+=2
    # Exact numerical certificate for the literal source volume estimate.
    N=10**12;K=30;leaf=17_000_000_000;root=488_926_258_176
    minority=(1<<(K-1))+leaf
    union=(1<<K)-1+K*leaf
    assert (1<<K)+K*leaf+root==N
    assert 56*minority<N and 2*union>N
    esum=sum(F(7**j,math.factorial(j)) for j in range(21))
    assert esum>1000 # e^7>1000, so ln N=4ln1000<28.
    cert={'N':N,'coordinate_minority':minority,'56_times_minority':56*minority,'minority_union':union,'two_slice_copy_volume':2*union,'e7_positive_taylor_sum_0_through_20':str(esum),'antipode_arrival':N-1,'unique_farthest_antipode':N-1+K> K+1}
    # Falsification controls isolate mechanisms that the full algorithm must retain.
    d=distances(graph(3,[(0,1),(1,2)]));w=[F(1)]*3
    bad=search(w,lambda q:q>=1,F(1),save=False)
    assert bad!=1
    # Star's heavy slice vertex must keep its original additive arrival as well as exterior fiber.
    sd=distances(graph(22,[(0,j) for j in range(1,22)]));a={j:10 if j==1 else 0 for j in range(22)}
    exterior=max(sd[1][j]+a[j] for j in range(22) if j!=1)
    assert exterior==2 and max(sd[1][j]+a[j] for j in range(22))==10
    # A nonintegral edge distance invalidates the threshold bridge if the distance integrality promise is dropped.
    assert F(1)*F(1,2)<=F(3,4) and not (F(1,2)<=0)
    negatives={'omit_incumbent_save':{'wrong':str(bad),'correct':'1'},'omit_original_slice_call':{'wrong':2,'correct':10},'drop_integral_distance_promise':{'distance':'1/2','weight':'1','R':'3/4','integer_budget':0,'actual_feasible':True,'budget_feasible':False}}
    assert stats['source_unbalanced'] and stats['source_balanced'] and stats['source_dominance'] and stats['fiber_below_original']
    result={'status':'PASS','seed':13757002,'no_candidate_or_prior_code_import':True,'graphs':records,'counts':dict(stats),'source_counterexample':cert,'negative_controls':negatives,'limits':'Exact finite falsification controls and brute structural/shortest-path reference methods; not a fast implementation or experimental proof of asymptotic complexity. Abstract and graph cases overlap and are not a distinct-instance count.'}
    (HERE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
