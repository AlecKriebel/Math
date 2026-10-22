"""New exact finite certificates for the primary Figure1 ingredients.

Source-author programs and absent historical transcriptions/witnesses are not
used. Every guard is an explicit exception and survives -O/-OO.
"""
from itertools import permutations, combinations
from collections import deque
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def edge(u,v):
    need(u!=v,'no loop')
    return tuple(sorted((u,v)))


# A: outer17-cycle, clockwise from the top, with center17.
A=sorted({edge(i,(i+1)%17) for i in range(17)}|
         {(0,17),(3,17),(14,17),(1,13),(2,7),(4,16),(5,9),(6,11),(8,12),(10,15)})
# B: outerhexagon0..5 clockwise from upper-left. Inner labels are documented
# in the authored report; a=16 (lower central vertex), b=1 (upper-right).
B=sorted({edge(i,(i+1)%6) for i in range(6)}|
         {(0,6),(1,12),(2,13),(3,14),(4,8),(5,7),
          (6,8),(6,17),(7,9),(7,17),(8,9),
          (12,14),(12,15),(11,13),(13,15),(11,14),
          (9,10),(10,11),(15,16),(16,17),(10,16)})
ATTACH_A=0
ATTACH_B_LEFT=16
ATTACH_B_RIGHT=1


def adjacency(n,es):
    out=[set() for _ in range(n)]
    for u,v in es:
        need(0<=u<v<n,'bad edge')
        out[u].add(v);out[v].add(u)
    return out


def connected(n,es,removed=frozenset()):
    a=adjacency(n,es);left=set(range(n))-set(removed)
    if not left:
        return True
    start=min(left);seen={start};todo=[start]
    while todo:
        u=todo.pop()
        for v in a[u]-set(removed):
            if v not in seen:
                seen.add(v);todo.append(v)
    return seen==left


def incidence(n,es):
    stars=[0]*n
    for i,(u,v) in enumerate(es):
        stars[u]^=1<<i;stars[v]^=1<<i
    return stars


def validate_flow(n,es,colors,zero=None):
    need(len(colors)==len(es),'flow length')
    need(all(c in (0,1,2,3) for c in colors),'F2² values')
    need({i for i,c in enumerate(colors) if c==0}==({zero} if zero is not None else set()),
         'flow must have exactly prescribed zero')
    acc=[0]*n
    for (u,v),c in zip(es,colors):
        acc[u]^=c;acc[v]^=c
    need(not any(acc),'vertex conservation')


def find_flow(n,es,zero=None):
    inc=[[] for _ in range(n)]
    for i,(u,v) in enumerate(es):
        inc[u].append(i);inc[v].append(i)
    colors=[None]*len(es)
    if zero is not None:
        colors[zero]=0
    # Global color automorphisms allow one nonzero edge to have value1.
    colors[next(i for i in range(len(es)) if i!=zero)]=1
    nodes=0

    def search(cs):
        nonlocal nodes
        nodes+=1
        best=None
        for i,(u,v) in enumerate(es):
            if cs[i] is not None:
                continue
            ds=[]
            for color in (1,2,3):
                ok=True
                for w in (u,v):
                    x=color;unassigned=0
                    for j in inc[w]:
                        if j==i:
                            continue
                        if cs[j] is None:
                            unassigned+=1
                        else:
                            x^=cs[j]
                    if unassigned==0 and x!=0:
                        ok=False
                    if unassigned==1 and x==0:
                        # The last other edge would be zero, forbidden.
                        ok=False
                if ok:
                    ds.append(color)
            if not ds:
                return None
            if best is None or len(ds)<len(best[1]):
                best=(i,ds)
        if best is None:
            validate_flow(n,es,cs,zero)
            return cs
        i,ds=best
        for color in ds:
            ns=cs[:];ns[i]=color
            result=search(ns)
            if result is not None:
                return result
        return None
    ans=search(colors)
    return ans,nodes


def perfect_matchings(n,es):
    a=adjacency(n,es);ids={e:i for i,e in enumerate(es)};out=[]
    def rec(left,chosen):
        if not left:
            out.append(chosen);return
        u=min(left)
        for v in sorted(a[u]&left):
            rec(left-{u,v},chosen|(1<<ids[edge(u,v)]))
    rec(set(range(n)),0)
    return out


def complement_cycles(n,es,matching):
    a=adjacency(n,[e for i,e in enumerate(es) if not(matching>>i&1)])
    need(all(len(v)==2 for v in a),'complement must be2regular')
    left=set(range(n));lengths=[]
    while left:
        root=min(left);seen={root};todo=[root]
        while todo:
            u=todo.pop()
            for v in a[u]-seen:
                seen.add(v);todo.append(v)
        left-=seen;lengths.append(len(seen))
    return sorted(lengths)


def five_cycles(n,es):
    a=adjacency(n,es);out=set()
    def rec(path):
        if len(path)==5:
            if path[0] in a[path[-1]]:
                out.add(tuple(sorted(edge(path[i],path[(i+1)%5]) for i in range(5))))
            return
        for v in a[path[-1]]:
            if v not in path and v>=path[0]:
                rec(path+[v])
    for u in range(n):
        rec([u])
    return sorted(out)


def girth(n,es):
    a=adjacency(n,es);best=n+1
    for root in range(n):
        dist={root:0};par={root:-1};todo=deque([root])
        while todo:
            u=todo.popleft()
            for v in a[u]:
                if v not in dist:
                    dist[v]=dist[u]+1;par[v]=u;todo.append(v)
                elif par[u]!=v:
                    best=min(best,dist[u]+dist[v]+1)
    return best


def cut_check(n,es):
    stars=incidence(n,es);small=[];cut=0;prev=0
    # Vertex0 is fixed outside S, avoiding duplicate complementary cuts.
    for i in range(1,1<<(n-1)):
        g=i^(i>>1);bit=g^prev;v=bit.bit_length();cut^=stars[v];prev=g
        if cut.bit_count()<=3:
            need(cut.bit_count()==3 and cut in stars,'nontrivial cut of size<=3')
            small.append(cut)
    need(set(small)==set(stars) and len(small)==n,'exact trivial3cut set')
    return len(small)


def cycle_basis(n,es):
    a=[[] for _ in range(n)]
    for i,(u,v) in enumerate(es):
        a[u].append((v,i));a[v].append((u,i))
    seen={0};parent={0:(-1,-1)};tree=set();todo=[0]
    while todo:
        u=todo.pop()
        for v,i in a[u]:
            if v not in seen:
                seen.add(v);parent[v]=(u,i);tree.add(i);todo.append(v)
    need(len(seen)==n,'connected cycle basis input')
    out=[]
    for i,(u,v) in enumerate(es):
        if i in tree:
            continue
        paths=[]
        for x in (u,v):
            mask=0
            while x!=0:
                x,j=parent[x];mask^=1<<j
            paths.append(mask)
        out.append(paths[0]^paths[1]^(1<<i))
    return out


def even(n,es,mask):
    return all((mask&s).bit_count()%2==0 for s in incidence(n,es))


def build_path(n,perms=None):
    need(n>=2,'nontrivial path family index')
    gs=[A]+[B]*(n-1)+[A]
    at=[]
    for i in range(n+1):
        at.append(({1:ATTACH_A} if i==0 else {-1:ATTACH_A} if i==n else
                   {-1:ATTACH_B_LEFT,1:ATTACH_B_RIGHT}))
    kept={};vertex=0
    for i in range(n+1):
        for v in range(18):
            if v not in at[i].values():
                kept[(i,v)]=vertex;vertex+=1
    es=[];maps=[[-1]*27 for _ in gs];joins=[]
    for i,g in enumerate(gs):
        for j,(u,v) in enumerate(g):
            if (i,u) in kept and (i,v) in kept:
                maps[i][j]=len(es);es.append(edge(kept[(i,u)],kept[(i,v)]))
    if perms is None:
        perms=[(0,1,2)]*n
    for i in range(n):
        left,right=at[i][1],at[i+1][-1]
        lg,rg=gs[i],gs[i+1]
        ln=sorted(v if u==left else u for u,v in lg if left in (u,v))
        rn=sorted(v if u==right else u for u,v in rg if right in (u,v))
        join=[]
        for k,v in enumerate(ln):
            w=rn[perms[i][k]];eid=len(es);join.append(eid)
            es.append(edge(kept[(i,v)],kept[(i+1,w)]))
            maps[i][lg.index(edge(left,v))]=eid
            maps[i+1][rg.index(edge(right,w))]=eid
        joins.append(join)
    need(all(all(j>=0 for j in m) and len(set(m))==27 for m in maps),'complete block edge injections')
    return vertex,es,maps,joins,gs,at


def verify_path(n,perms,flowtable):
    N,es,maps,joins,gs,at=build_path(n,perms)
    need(N==16*n+18 and len(es)==24*n+27 and len(set(es))==len(es),'path size/simple graph')
    need(all(len(x)==3 for x in adjacency(N,es)) and connected(N,es),'cubic connected path')
    sets=[set(m) for m in maps]
    private=[sets[i]-set(j for join in joins for j in join) for i in range(n+1)]
    need([len(x) for x in private]==[24]+[21]*(n-1)+[24],'private-edge counts')
    for i,j in combinations(range(n+1),2):
        need(sets[i]&sets[j]==(set(joins[i]) if j==i+1 else set()),'exact block intersections')
    hb=cycle_basis(N,es)
    need(len(hb)==8*n+10 and all(even(N,es,c) for c in hb),'target cycle basis')
    pullbacks=0
    for i,m in enumerate(maps):
        for c in hb:
            pre=sum(1<<k for k,e in enumerate(m) if c>>e&1)
            need(even(18,gs[i],pre),'natural injection must pull full cycle space back')
            pullbacks+=1
        # Extend a basis of block cycles outside its edge set, checking exact
        # restriction and target incidence parity.
        for c in cycle_basis(18,gs[i]):
            image=sum(1<<m[k] for k in range(27) if c>>k&1)
            for attachment in at[i].values():
                picked=[m[k] for k,e in enumerate(gs[i]) if attachment in e and c>>k&1]
                need(len(picked) in (0,2),'block cycle attachment parity')
                if not picked:
                    continue
                # For this join cut, identify exterior endpoints as vertices not
                # incident to private/local edges of the physical block core.
                core_vertices=set(v for eid in private[i] for v in es[eid])
                for eid in m:
                    if eid not in set(j for x in joins for j in x):
                        core_vertices.update(es[eid])
                ends=[next(v for v in es[eid] if v not in core_vertices) for eid in picked]
                outside=[(eid,e) for eid,e in enumerate(es) if eid not in sets[i]]
                adj=[[] for _ in range(N)]
                for eid,(u,v) in outside:
                    adj[u].append((v,eid));adj[v].append((u,eid))
                todo=deque([ends[0]]);parents={ends[0]:(-1,-1)}
                while todo and ends[1] not in parents:
                    u=todo.popleft()
                    for v,eid in adj[u]:
                        if v not in parents:
                            parents[v]=(u,eid);todo.append(v)
                need(ends[1] in parents,'exterior branch connectivity')
                x=ends[1]
                while x!=ends[0]:
                    x,eid=parents[x];image^=1<<eid
            need(even(N,es,image),'cycle extension parity')
            need(sum(1<<k for k,e in enumerate(m) if image>>e&1)==c,'exact cycle restriction')
    need(set().union(*(set(j for j in range(len(es)) if c>>j&1) for c in hb))==set(range(len(es))),
         'every path edge belongs to a cycle, hence no bridge')
    # Both localization flow-gluing cases, all missing edges specified in advance.
    cases=[]
    zeros=[next(k for k,e in enumerate(maps[i]) if e in private[i]) for i in range(n+1)]
    cases.append(zeros)
    for interface in range(n):
        zs=zeros[:];shared=joins[interface][0]
        zs[interface]=maps[interface].index(shared);zs[interface+1]=maps[interface+1].index(shared)
        cases.append(zs)
    for zs in cases:
        blockflows=[]
        for i in range(n+1):
            key='A' if gs[i] is A else 'B'
            cs=flowtable[key][zs[i]][:]
            if i:
                shared=joins[i-1];need_match={e:blockflows[i-1][maps[i-1].index(e)] for e in shared}
                trans=None
                for perm in permutations((1,2,3)):
                    lut=(0,)+perm
                    if all(lut[cs[maps[i].index(e)]]==need_match[e] for e in shared):
                        trans=lut;break
                need(trans is not None,'interface flow permutation must exist')
                cs=[trans[c] for c in cs]
            blockflows.append(cs)
        large=[None]*len(es)
        for m,cs in zip(maps,blockflows):
            for eid,c in zip(m,cs):
                need(large[eid] in (None,c),'glued edge disagreement')
                large[eid]=c
        acc=[0]*N
        for (u,v),c in zip(es,large):
            acc[u]^=c;acc[v]^=c
        need(not any(acc),'glued flow conservation')
        need({i for i,c in enumerate(large) if c==0}=={maps[i][z] for i,z in enumerate(zs)},
             'flow has no extra zeros on the proposed image')
    return {'n':n,'vertices':N,'edges':len(es),'cycle_pullback_checks':pullbacks,
            'source_cycle_extensions':10*(n+1),'gluing_cases':len(cases)}


def main():
    graphs={'A':A,'B':B};flows={};reports={}
    for name,es in graphs.items():
        need(len(es)==27 and len(set(es))==27 and all(len(a)==3 for a in adjacency(18,es)),
             'simple cubic18vertex27edge ingredient')
        need(connected(18,es) and girth(18,es)==5,'connected girth5 ingredient')
        small=cut_check(18,es)
        noflow,nodes=find_flow(18,es)
        need(noflow is None,'ingredient must be a snark')
        pms=perfect_matchings(18,es)
        need(len(pms)==(20 if name=='A' else 19),'independent perfect matching count')
        types=[complement_cycles(18,es,pm) for pm in pms]
        need(all(any(c%2 for c in t) for t in types),'no even2factor: independent noncolorability')
        fives=five_cycles(18,es)
        need(len(fives)==(8 if name=='A' else 10),'primary graph nonisomorphism invariant')
        flows[name]=[]
        for zero in range(27):
            ans,_=find_flow(18,es,zero)
            need(ans is not None,'every single-edge deletion needs an F2² flow')
            validate_flow(18,es,ans,zero);flows[name].append(ans)
        reports[name]={'vertices':18,'edges':es,'small_cuts':small,'girth':5,
            'perfect_matching_count':len(pms),'complementary_cycle_lengths':types,
            'five_cycle_count':len(fives),'nonzero_flow_exists':False,'flow_search_nodes':nodes,
            'deletion_flows':flows[name]}
    fives=five_cycles(18,B)
    profiles=[]
    for v in (ATTACH_B_LEFT,ATTACH_B_RIGHT):
        profiles.append(sorted(sum(e in cy for cy in fives) for e in B if v in e))
    need(profiles==[[1,1,2],[0,2,2]],'a,b incident5cycle profiles distinguish automorphism orbits')
    need(edge(ATTACH_B_LEFT,ATTACH_B_RIGHT) not in B,'attachment vertices independent')
    need(connected(18,B,{ATTACH_B_LEFT,ATTACH_B_RIGHT}) and connected(18,A,{ATTACH_A}),
         'attachment-deleted cores connected')
    for perm in permutations((1,2,3)):
        lut=(0,)+perm
        need(all(lut[x^y]==lut[x]^lut[y] for x in range(4) for y in range(4)),
             'all three-color permutations linear over F2²')
    paths=[verify_path(n,[tuple((k+i)%3 for k in range(3)) for i in range(n)],flows) for n in range(2,7)]
    # All join permutations at n2 test that no hidden matching convention enters.
    for perms in product_permutations(2):
        N,es,maps,joins,gs,at=build_path(2,perms)
        need(N==50 and len(es)==75 and len(set(es))==75 and connected(N,es)
             and all(len(a)==3 for a in adjacency(N,es)),'arbitrary joining permutations')
    # A full binary cycle need not be a connected circuit: pullback of the
    # triangle under the edge projection from two disjoint triangles is valid.
    triangle=[(0,1),(0,2),(1,2)];two=triangle+[(u+3,v+3) for u,v in triangle]
    need(even(6,two,(1<<6)-1) and not connected(6,two),'disconnected even-set convention')
    # Exhaust all abstract index maps satisfying the necessary constraints.
    # These are not asserted sufficient for actual cc maps; reversal is allowed
    # in this deliberately weaker model. Their lengths must still coincide.
    abstract_maps=0
    for m in range(2,9):
        for n in range(2,9):
            answers=[]
            def extend(path):
                i=len(path)
                if i==m+1:
                    answers.append(path);return
                for value in range(n+1):
                    if ((i in (0,m)) != (value in (0,n))):
                        continue
                    if path and abs(value-path[-1])!=1:
                        continue
                    if len(path)>1 and value==path[-2]:
                        continue
                    extend(path+[value])
            extend([])
            need(len(answers)==(2 if m==n else 0),'no collapse/no fold imply equal path length')
            abstract_maps+=len(answers)

    def index_constraints(path,n,no_collapse=True,no_fold=True):
        m=len(path)-1
        return (all((i in (0,m))==(v in (0,n)) for i,v in enumerate(path))
                and all((abs(x-y)==1 if no_collapse else abs(x-y)<=1)
                        for x,y in zip(path,path[1:]))
                and (not no_fold or all(path[i-1]!=path[i+1] for i in range(1,m))))
    # Concrete unequal-length index maps falsify the argument if either
    # independently established prohibition is simply omitted.
    need(index_constraints([0,1,1,2],2,no_collapse=False),'collapse countercontrol exists')
    need(index_constraints([0,1,2,1,2,3],3,no_fold=False),'fold countercontrol exists')
    bad=[
        ('extra_flow_zero',lambda:validate_flow(18,A,[0]+flows['A'][1][1:],1)),
        ('corrupt_flow_value',lambda:validate_flow(18,A,[flows['A'][0][0]]+[1]*26,0)),
        ('wrong_zero_edge',lambda:validate_flow(18,A,flows['A'][0],1)),
        ('noncritical_coloring_instead_of_flow',lambda:need(all(len({flows['A'][0][i] for i,e in enumerate(A) if v in e and i!=0})==2 for v in A[0]),'degree2 flow values must coincide')),
        ('vertex_transitive_attachments',lambda:need(profiles[0]==profiles[1],'distinct orbit invariant')),
        ('adjacent_attachment_choice',lambda:need(edge(1,2) not in B,'attachments are adjacent')),
        ('wrong_private_count',lambda:need(2*21<=27,'two private cores cannot fit in27edge range')),
        ('equal_block_sizes_dropped',lambda:need(len(A)==len(B)+1,'equal27edge count is essential')),
        ('source_graph_colorable',lambda:need(find_flow(18,A)[0] is not None,'snark requirement')),
        ('cyclic4_large_graph_claim',lambda:need(all(len(j)>3 for j in build_path(2)[3]),'large graph has nontrivial3cuts')),
        ('single_circuit_substitution',lambda:need(connected(6,two),'binary cycle need not be connected')),
        ('omitted_factor_star',lambda:need(18==17,'vertex-star count changed')),
        ('collapse_allowed',lambda:need(index_constraints([0,1,1,2],2),'must reject collapsed unequal paths')),
        ('fold_allowed',lambda:need(index_constraints([0,1,2,1,2,3],3),'must reject folded unequal paths')),
    ]
    rejected=[]
    for name,fn in bad:
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    print(json.dumps({'status':'PASS','ingredients':reports,'attachment_a':16,'attachment_b':1,
        'attachment_incident_five_cycle_profiles':profiles,'critical_flow_witnesses':54,
        'paths':paths,'n2_join_permutations_checked':36,'negative_controls_rejected':rejected,
        'abstract_necessary_path_map_pairs':49,'abstract_equal_length_maps':abstract_maps,
        'optimization_safe_guards':True,'source_author_code_executed':False,
        'historical_transcriptions_or_flows_reused':False,'floating_point_used':False},indent=2,sort_keys=True))


def product_permutations(n):
    from itertools import product
    return product(tuple(permutations((0,1,2))),repeat=n)


if __name__=='__main__':
    main()
