#!/usr/bin/env python3
"""Finite diagnostics for authored elementary lemmas; not theorem certification."""
import itertools
import json
import sys

CHECKS=0

def check(ok, label):
    global CHECKS
    CHECKS+=1
    if not ok: raise ValueError(label)

def require(ok,label):
    if not ok:raise ValueError(label)

def valid_set(A,N):
    require(type(N) is int and 0<=N<=64,'invalid path order')
    require(type(A) in (list,tuple,set,frozenset),'invalid neighbor collection')
    require(all(type(a) is int and 0<=a<N for a in A),'invalid neighbor')
    require(len(A)==len(set(A)),'duplicate neighbor')
    return tuple(sorted(A))

def delta(A):
    return frozenset(b-a for a,b in itertools.combinations(sorted(A),2))

def delta_mask(mask,N):
    require(type(mask) is int and 0<=mask<(1<<N),'invalid subset mask')
    result=0
    rest=mask
    while rest:
        bit=rest&-rest
        i=bit.bit_length()-1
        result|=mask>>i
        rest-=bit
    return result&~1

def subsets(U):
    U=tuple(U)
    for mask in range(1<<len(U)):
        yield tuple(x for i,x in enumerate(U) if (mask>>i)&1)

def edges_path(N):return [(i,i+1) for i in range(N-1)]

def apex_graph(N,A,B=None):
    A=valid_set(A,N)
    E=edges_path(N)+[(N,a) for a in A]
    if B is None:return N+1,E
    B=valid_set(B,N)
    return N+2,E+[(N+1,b) for b in B]

def faudree(m,B):
    require(type(m) is int and 2<=m<=30,'Faudree family requires m>=2')
    B=valid_set(B,2*m+1)
    require(all(m+1<=b<=2*m for b in B),'invalid Faudree neighbor')
    return apex_graph(2*m-1,(0,)+tuple(b-2 for b in B))

def cycle_lengths(n,edges):
    """Independent DFS, smallest vertex fixed to remove rotation duplicates."""
    require(type(n) is int and 0<=n<=18,'invalid graph order')
    adj=[set() for _ in range(n)]
    seen=set()
    for edge in edges:
        require(type(edge) in (list,tuple) and len(edge)==2,'invalid edge')
        a,b=edge
        require(type(a) is int and type(b) is int and 0<=a<n and 0<=b<n and a!=b,'invalid vertex or loop')
        pair=tuple(sorted((a,b)))
        require(pair not in seen,'duplicate edge')
        seen.add(pair);adj[a].add(b);adj[b].add(a)
    lengths=set()
    for root in range(n):
        stack=[(root,1<<root,1)]
        while stack:
            v,mask,length=stack.pop()
            for w in adj[v]:
                if w==root and length>=3:lengths.add(length)
                elif w>root and not ((mask>>w)&1):stack.append((w,mask|(1<<w),length+1))
    return frozenset(lengths)

def twohub(N,A,B):
    A=valid_set(A,N);B=valid_set(B,N)
    C={d+2 for d in delta(A)|delta(B)}
    intervals=[(min(a,b),max(a,b),abs(a-b)) for a in A for b in B]
    for i,(a,b,d) in enumerate(intervals):
        for c,e,f in intervals[i+1:]:
            if b<c or e<a:C.add(d+f+4)
    return frozenset(C)

def fibonacci(n):
    a,b=0,1
    for _ in range(n):a,b=b,a+b
    return a

def partitions(total,minimum=1):
    if total==0:yield ()
    for first in range(minimum,total+1):
        for rest in partitions(total-first,first):yield (first,)+rest

def theta(lengths):
    require(type(lengths) in (list,tuple) and all(type(x) is int and x>=1 for x in lengths),'invalid lengths')
    require(sum(x==1 for x in lengths)<=1,'parallel direct edges disallowed')
    E=[];nextv=2
    for length in lengths:
        vertices=[0]+list(range(nextv,nextv+length-1))+[1]
        nextv+=length-1
        E.extend(zip(vertices,vertices[1:]))
    return nextv,E

def bouquet(S):
    require(len(S)==len(set(S)) and all(type(x) is int and x>=3 for x in S),'invalid cycle set')
    E=[];nextv=1
    for length in S:
        vertices=[0]+list(range(nextv,nextv+length-1))+[0]
        nextv+=length-1
        E.extend(zip(vertices,vertices[1:]))
    return nextv,E

def finite_f(n):
    """Separate cycle-edge-mask enumeration, independent of DFS."""
    E=list(itertools.combinations(range(n),2));pos={edge:i for i,edge in enumerate(E)}
    cycles=[]
    for length in range(3,n+1):
        for verts in itertools.combinations(range(n),length):
            first=verts[0]
            for tail in itertools.permutations(verts[1:]):
                if tail[0]>tail[-1]:continue
                seq=(first,)+tail+(first,)
                cm=0
                for a,b in zip(seq,seq[1:]):cm|=1<<pos[tuple(sorted((a,b)))]
                cycles.append((cm,1<<length))
    images=set()
    for mask in range(1<<len(E)):
        spec=0
        for cm,lb in cycles:
            if mask&cm==cm:spec|=lb
        images.add(spec)
    return len(images)

def main():
    global CHECKS
    require(sys.flags.isolated==1,'isolated Python required')
    # Formula (1), with an independent graph traversal.
    fan_cases=0
    for N in range(1,9):
        for A in subsets(range(N)):
            check(cycle_lengths(*apex_graph(N,A))=={d+2 for d in delta(A)},'one-hub formula')
            fan_cases+=1
    for m in range(2,8):
        images=set()
        for B in subsets(range(m+1,2*m+1)):
            # Relabel vertex 1 as apex; path 2,...,2m becomes 0,...,2m-2.
            C=cycle_lengths(*faudree(m,B))
            check({x for x in C if x>m}==set(B),'Faudree high-band recovery')
            images.add(C)
        check(len(images)==1<<m,'Faudree image count')
    A=(0,1,4,6);B=(0,1,2,3,6)
    check(delta(A)==delta(B)==set(range(1,7)),'non-reflection collision')
    check(len(A)!=len(B),'collision not reflection')
    d_counts=[]
    for N in range(1,17):
        images={delta_mask(mask,N) for mask in range(1<<N)}
        d_counts.append(len(images))
        if N<=10:
            for mask in range(1<<N):
                A=tuple(i for i in range(N) if mask>>i&1)
                check(delta_mask(mask,N)==sum(1<<d for d in delta(A)),'distance mask implementation')
    # Missing-distance count: independent exhaustion versus path recurrence.
    missing_cases=0
    for N in range(2,13):
        ds=[delta_mask(mask,N) for mask in range(1<<N)]
        for d in range(1,N):
            actual=sum(not ((D>>d)&1) for D in ds)
            q,r=divmod(N,d)
            predicted=fibonacci(q+2)**(d-r)*fibonacci(q+3)**r
            check(actual==predicted,'Fibonacci missing-distance count')
            # Match all residue paths with consecutive pairs, independently.
            matching=sum(len(range(a,N,d))//2 for a in range(d))
            check(2*matching>=N-d,'matching lower bound')
            check(actual*4**matching<=2**N*3**matching,'matching probability bound exact arithmetic')
            missing_cases+=1
    # Cactus sufficiency, explicit graph realization, and exact finite counts.
    cactus_counts=[]
    for n in range(1,19):
        count=0
        for S in subsets(range(3,n+1)):
            if sum(x-1 for x in S)<=n-1:
                check(cycle_lengths(*bouquet(S))==set(S),'bouquet realization')
                count+=1
        cactus_counts.append(count)
    # Generalized theta sum formula, variable number of paths.
    theta_cases=0
    for total in range(0,10):
        for parts in partitions(total):
            for direct in (False,True):
                lengths=tuple(x+1 for x in parts)+((1,) if direct else ())
                C={a+b for a,b in itertools.combinations(lengths,2)}
                check(cycle_lengths(*theta(lengths))==C,'theta cycle formula')
                theta_cases+=1
    # Two-hub formula over all pairs of neighbor subsets for path orders <=5.
    twohub_cases=0
    for N in range(1,6):
        ss=list(subsets(range(N)))
        for A in ss:
            for B in ss:
                check(cycle_lengths(*apex_graph(N,A,B))==twohub(N,A,B),'two-hub interval formula')
                twohub_cases+=1
    B1=(6,7,9,11);B2=(6,7,8,9,11);expected={3,4,5,6,7,8,9,10,11,13}
    for B in [B1,B2]:
        C=cycle_lengths(*apex_graph(12,(0,5),(0,)+B))
        check(C==expected,'two-hub decoder counterexample')
        check(C=={b+2 for b in B}|{d+2 for d in delta(B)}|{7}|{b-1 for b in B},'specialized formula')
    # A complete check of formula (7), beyond the one counterexample.
    fixed_cases=0
    for m in range(2,7):
        for t in range(1,m):
            for B in subsets(range(m,2*m)):
                C={b+2 for b in B}|{d+2 for d in delta(B)}|{t+2}|{b-t+4 for b in B}
                check(C==twohub(2*m,(0,t),(0,)+B),'specialized complete two-hub formula')
                fixed_cases+=1
    twohub_counts=[]
    for m in range(1,8):
        ss=[(0,)+B for B in subsets(range(m,2*m))]
        images={twohub(2*m,A,B) for A in ss for B in ss}
        twohub_counts.append(len(images))
    check(twohub_counts==[3,6,19,46,127,310,721],'two-hub exact family counts')
    small_f=[finite_f(n) for n in range(7)]
    check(small_f==[1,1,1,2,4,6,11],'small graph spectrum counts')
    check(cycle_lengths(2,[(0,1)])==set() and small_f[2]==1,'degenerate m=1 has no 2-cycle and f(2)=1')
    # Explicit malformed-input controls, surviving -O and -OO.
    bad=[lambda:faudree(1,(2,)),lambda:apex_graph(3,(True,)),lambda:apex_graph(3,(0,0)),lambda:apex_graph(3,(-1,)),lambda:apex_graph(3,(3,)),lambda:apex_graph(-1,()),lambda:apex_graph(3,'12'),lambda:cycle_lengths(3,[(0,0)]),lambda:cycle_lengths(3,[(0,1),(1,0)]),lambda:cycle_lengths(3,[(0,3)]),lambda:cycle_lengths(True,[]),lambda:theta((1,1)),lambda:theta((0,2)),lambda:bouquet((2,)),lambda:bouquet((3,3)),lambda:delta_mask(-1,4),lambda:delta_mask(True,4)]
    for test in bad:
        rejected=False
        try:test()
        except ValueError:rejected=True
        check(rejected,'malformed control accepted')
    return {'checks':CHECKS,'one_hub_graph_cases':fan_cases,'distance_counts_n1_to_n16':d_counts,'missing_distance_cases':missing_cases,'cactus_counts_n1_to_n18':cactus_counts,'theta_graph_cases':theta_cases,'two_hub_graph_cases':twohub_cases,'specialized_two_hub_cases':fixed_cases,'two_hub_family_counts_m1_to_m7':twohub_counts,'exact_f_n0_to_n6':small_f,'malformed_input_rejections':len(bad),'main_problem_resolved':False,'formal_certification':False,'optimize':sys.flags.optimize}

if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (ValueError,TypeError,OverflowError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
