#!/usr/bin/env python3
"""Independent distance-CSP, rooted-tree states and arbitrary-list greedy controls."""
from collections import deque,Counter
from itertools import combinations,product
from functools import lru_cache
import json,hashlib,random

C=Counter();H=hashlib.sha256()
V=['a','b','c','d','e','a1','a2','b1','d1','e1','e2']
E=[('a','b'),('b','c'),('c','d'),('d','e'),('a','a1'),('a','a2'),('b','b1'),('d','d1'),('e','e1'),('e','e2')]
A=tuple(range(1,6));B=(1,3,4,5,6)
BAD={v:B if v in ['a1','a2','e1','e2'] else A for v in V}
W=dict(zip(V,[1,5,3,1,5,3,4,2,4,2,3]));LEAVES=['a1','a2','b1','d1','e1','e2']


def need(x,m):
    if not x:raise RuntimeError(m)


def graph(vertices,edges):
    g={v:[] for v in vertices}
    for a,b in edges:
        need(a!=b and a in g and b in g and b not in g[a],'Invalid simple graph')
        g[a].append(b);g[b].append(a)
    return g


def distances(g):
    out={}
    for s in g:
        d={s:0};q=deque([s])
        while q:
            v=q.popleft()
            for u in g[v]:
                if u not in d:d[u]=d[v]+1;q.append(u)
        need(len(d)==len(g),'Disconnected graph');out[s]=d
    return out


def valid(g,L,w):
    d=distances(g)
    return set(w)==set(g) and all(w[v] in L[v] and type(w[v]) is int and w[v]>=1 for v in g) and all(abs(w[a]-w[b])>=(2 if d[a][b]==1 else 1) for a,b in combinations(g,2) if d[a][b] in [1,2])


def csp(g,L,edge_gap=2,two_gap=1):
    d=distances(g);order={v:i for i,v in enumerate(g)};first=None
    def go(dom,assignment):
        nonlocal first
        C['CSP_recursion_nodes']+=1
        if not dom:
            if first is None:first=dict(assignment)
            return 1
        v=min(dom,key=lambda x:(len(dom[x]),order[x]));total=0
        for x in dom[v]:
            new={};ok=True
            for u,values in dom.items():
                if u==v:continue
                gap=edge_gap if d[v][u]==1 else two_gap if d[v][u]==2 else 0
                vals=tuple(y for y in values if abs(x-y)>=gap) if gap else values
                if not vals:ok=False;break
                new[u]=vals
            if ok:
                assignment[v]=x;total+=go(new,assignment);assignment.pop(v)
        return total
    total=go({v:tuple(sorted(set(L[v]))) for v in g},{})
    return total,first


def tree_states(g,L,root):
    parent={root:None};order=[root]
    for v in order:
        for u in g[v]:
            if u==parent[v]:continue
            need(u not in parent,'State method requires a tree');parent[u]=v;order.append(u)
    need(len(order)==len(g),'Tree not connected')
    children={v:[u for u in g[v] if parent.get(u)==v] for v in g}
    @lru_cache(None)
    def F(v,y,x):
        C['tree_state_evaluations']+=1
        if x not in L[v]:return 0
        p=parent[v]
        if p is None:
            if y is not None:return 0
        elif y not in L[p] or abs(x-y)<2:return 0
        cs=children[v]
        def match(i,used):
            if i==len(cs):return 1
            u=cs[i];total=0
            for z in L[u]:
                if abs(z-x)<2 or z==y or z in used:continue
                ways=F(u,x,z)
                if ways:total+=ways*match(i+1,used|{z})
            return total
        return match(0,set())
    total=sum(F(root,None,x) for x in L[root])
    return total,F,parent


def fixed_and_model_cases():
    g=graph(V,E);results={}
    fixed=[('common4',{v:tuple(range(1,5)) for v in V}),('common5',{v:A for v in V}),('common6',{v:tuple(range(1,7)) for v in V}),('displayed_bad5',BAD)]
    for name,L in fixed:
        count,w=csp(g,L)
        if w is not None:need(valid(g,L,w),'Direct returned witness invalid')
        roots={}
        for r in V:
            got,_,_=tree_states(g,L,r);need(got==count,'Independent count/root discrepancy');roots[r]=got;C['fixed_count_all_root_comparisons']+=1
        results[name]={'CSP_count':count,'all_root_state_counts':roots,'first_witness':w}
    need(results['common4']['CSP_count']==0 and results['common5']['CSP_count']==8 and results['displayed_bad5']['CSP_count']==0,'Independent elementary deductions mismatch')
    need(valid(g,{v:A for v in V},W),'Printed witness independently fails')
    variations={
      'uniform_translation':{v:tuple(x+10**30 for x in L) for v,L in BAD.items()},
      'uniform_reflection_positive':{v:tuple(sorted(7-x for x in L)) for v,L in BAD.items()},
      'uniform_dilation2':{v:tuple(2*x for x in L) for v,L in BAD.items()}}
    for name,L in variations.items():
        n,w=csp(g,L);q,_,_=tree_states(g,L,'c');need(n==q,'Transformed-list solver mismatch');need(n==0 if name!='uniform_dilation2' else n>0,'Numerical-list model control');results[name]={'CSP_count':n,'first_witness':w};C['list_transformation_controls']+=1
        if w:need(valid(g,L,w),'Transformed witness invalid')
    weak={}
    for name,eg,tg in [('adjacency_only_no_distance2',2,0),('all_distinct_constraints_gap1',1,1)]:
        n,w=csp(g,BAD,eg,tg);need(n>0,'Altered-model positive control unexpectedly infeasible');weak[name]={'count':n,'witness':w};C['weakened_model_controls']+=1
    vv=[v for v in V if v!='a2'];ee=[e for e in E if 'a2' not in e];gg=graph(vv,ee);ll={v:BAD[v] for v in vv};n,w=csp(gg,ll);q,_,_=tree_states(gg,ll,'c');need(n==q and n>0 and valid(gg,ll,w),'Deleted-twin control');weak['deleted_a2']={'count':n,'witness':w}
    return results,weak


def exhaustive_small():
    subsets=[tuple(i+1 for i in range(4) if mask>>i&1) for mask in range(1,16)]
    for n in [1,2,3]:
        g=graph(list(range(n)),[(i,i+1) for i in range(n-1)])
        for number,lists in enumerate(product(subsets,repeat=n)):
            L=dict(enumerate(lists));a,w=csp(g,L);b,_,_=tree_states(g,L,0);need(a==b,'Exhaustive small-list discrepancy')
            if w:need(valid(g,L,w),'Small-list witness')
            if number%17==0:
                other,_,_=tree_states(g,L,n-1);need(a==other,'Alternate-root boundary discrepancy');C['small_alternate_root_comparisons']+=1
            C['exhaustive_all_nonempty_subset_list_instances']+=1
            H.update(str((n,lists,a)).encode())
    opts=list(combinations(range(1,6),2));g=graph([0,1,2,3],[(0,1),(0,2),(0,3)])
    for lists in product(opts,repeat=4):
        L=dict(enumerate(lists));a,w=csp(g,L);b,_,_=tree_states(g,L,0);need(a==b,'Exhaustive star state mismatch')
        if w:need(valid(g,L,w),'Star witness invalid')
        C['exhaustive_star_two_list_instances']+=1;H.update(str((lists,a)).encode())


def greedy(g,L,root):
    delta=max(map(len,g.values()));order=[root];parent={root:None}
    for v in order:
        for u in g[v]:
            if u not in parent:parent[u]=v;order.append(u)
    d=distances(g);w={}
    for v in order:
        forbidden={x for x in L[v] if any(d[v][u] in [1,2] and abs(x-y)<(2 if d[v][u]==1 else 1) for u,y in w.items())}
        earlier_neighbours=[u for u in w if d[v][u]==1];earlier_two=[u for u in w if d[v][u]==2]
        if parent[v] is not None:need(earlier_neighbours==[parent[v]] and len(earlier_two)<=delta-1 and len(forbidden)<=delta+2,'Greedy quantified forbidden-set bound')
        choices=sorted(set(L[v])-forbidden);need(choices,'Greedy choice missing');w[v]=choices[0];C['greedy_vertex_steps']+=1
    need(valid(g,L,w),'Greedy output invalid');return w


def arbitrary_list_greedy():
    rng=random.Random(23440389)
    for case in range(256):
        n=1+case%31;g=graph(list(range(n)),[(v,rng.randrange(v)) for v in range(1,n)]);delta=max(map(len,g.values()));k=delta+3;L={}
        for v in g:
            values=set()
            while len(values)<k:
                x=1+rng.randrange(k+11)
                if case%3==1:x+=2**256
                if case%3==2:x=17*x+101*v
                values.add(x)
            L[v]=tuple(sorted(values))
        greedy(g,L,rng.randrange(n));C['arbitrary_integer_list_greedy_trees']+=1


def extensions():
    records=[]
    cases=list(product(range(3),repeat=6))+[(11,0,0,0,0,0),(0,7,2,0,4,9),(4,1,8,2,0,5)]
    oldg=graph(V,E);oldd=distances(oldg)
    for lengths in cases:
        vv=V.copy();ee=E.copy();paths=[]
        for leaf,length in zip(LEAVES,lengths):
            path=[];p=leaf
            for i in range(length):
                x=leaf+'x'+str(i+1);vv.append(x);ee.append((p,x));path.append(x);p=x
            paths.append(path)
        g=graph(vv,ee);d=distances(g);need(len(g)==11+sum(lengths) and len(ee)==10+sum(lengths) and max(map(len,g.values()))==3,'Extended graph invariant')
        need(all(d[a][b]==oldd[a][b] for a in V for b in V),'Old distances changed')
        w=dict(W)
        for path in paths:
            for v in path:
                choices=[x for x in A if all(d[v][u] not in [1,2] or abs(x-y)>=(2 if d[v][u]==1 else 1) for u,y in w.items())];need(choices,'Universal path extension lost a choice');w[v]=choices[0]
        need(valid(g,{v:A for v in vv},w),'Extended ordinary witness invalid')
        for i,p in enumerate(paths):
            for q in paths[i+1:]:need(all(d[x][y]>=4 for x in p for y in q),'Cross-added-path distance claim')
        L={v:BAD[v] if v in BAD else A for v in vv};count,_,_=tree_states(g,L,'c');need(count==0,'Bad assignment restricts incorrectly')
        diameter=max(max(x.values()) for x in d.values());expected=max(lengths[i]+oldd[a][b]+lengths[j] for i,a in enumerate(LEAVES) for j,b in enumerate(LEAVES) if i<j);need(diameter==expected,'Full independent-length diameter formula')
        C['six_tuple_extension_cases']+=1
        if lengths in [(0,0,0,0,0,0),(11,0,0,0,0,0)]:records.append({'lengths':lengths,'vertices':len(vv),'diameter':diameter,'ordinary_witness':w,'bad_list_count':count})
    return records


def state_falsifiers():
    g=graph([0,1],[(0,1)]);L={0:(1,),1:(3,)};n,F,p=tree_states(g,L,0)
    tests={'outside_vertex_list_rejected':F(1,1,4)==0,'outside_parent_list_rejected':F(1,0,3)==0,'root_nonempty_parent_rejected':F(0,1,1)==0}
    g=graph([0,1],[(0,1)]);L={0:(1,2),1:(2,3)};n,F,p=tree_states(g,L,0);tests['gap1_local_state_rejected']=F(1,1,2)==0
    g=graph([0,1,2],[(0,1),(0,2)]);L={0:(1,),1:(3,),2:(3,)};a,_=csp(g,L);b,_,_=tree_states(g,L,0);tests['sibling_injectivity_trap']=a==b==0
    g=graph([0,1,2],[(0,1),(1,2)]);L={0:(1,),1:(3,),2:(1,)};a,_=csp(g,L);b,_,_=tree_states(g,L,0);tests['grandparent_equality_trap']=a==b==0
    need(all(tests.values()),'State/model falsifier failed');return tests


def main():
    fixed,weak=fixed_and_model_cases();exhaustive_small();arbitrary_list_greedy();ex=extensions();faults=state_falsifiers()
    print(json.dumps({'status':'PASS','fixed_cases':fixed,'altered_model_or_graph_cases':weak,'state_admissibility_and_boundary_falsifiers':faults,'extension_boundary_records':ex,'counts':dict(sorted(C.items())),'small_case_digest_SHA256':H.hexdigest(),'native_checker_or_specimen_imports':False,'source_code_results_read_for_implementation':False,'limitations':['Exhaustive finite instances do not prove the universal arbitrary-six-list bound or all extension tuples; the initial proofs do.','No minimum-order, independent-discovery, new-mechanism, firstness or current-open-status claim.','All counts label vertices individually, without quotienting automorphisms.'],'network':0,'writes':0},sort_keys=True))


if __name__=='__main__':main()
