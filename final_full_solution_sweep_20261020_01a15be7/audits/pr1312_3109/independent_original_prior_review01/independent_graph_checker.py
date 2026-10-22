"""Exact independent Petersen-fragment checks, with no external graph package."""
from itertools import combinations
from collections import Counter, deque
import hashlib
import json


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def edge(u,v):
    return tuple(sorted((u,v)))


def petersen(step=2):
    return sorted({edge(i,(i+1)%5) for i in range(5)} |
                  {edge(5+i,5+(i+step)%5) for i in range(5)} |
                  {edge(i,5+i) for i in range(5)})


def graph(n, step=2, closing=True, restore=False, reverse=False):
    need(n >= 1, 'positive block count')
    e=petersen(step)
    out=set()
    for i in range(n):
        out.update(edge(10*i+u,10*i+v) for u,v in e if (u,v)!=(0,5) or restore)
    links=[]
    for i in range(n if closing else n-1):
        uv=edge(10*i+(0 if reverse else 5),10*((i+1)%n)+(5 if reverse else 0))
        need(uv not in out, 'link duplicates an internal edge')
        out.add(uv)
        links.append(uv)
    return 10*n,sorted(out),links


def adjacency(N,edges):
    a=[set() for _ in range(N)]
    for u,v in edges:
        need(0<=u<N and 0<=v<N and u!=v,'simple edge domain')
        need(v not in a[u], 'parallel edge')
        a[u].add(v); a[v].add(u)
    return a


def reached(a, start=0, deleted=None):
    seen={start}; todo=[start]
    while todo:
        u=todo.pop()
        for v in a[u]:
            if deleted is not None and edge(u,v)==deleted:
                continue
            if v not in seen:
                seen.add(v); todo.append(v)
    return seen


def bridgeless(N,edges):
    a=adjacency(N,edges)
    return len(reached(a))==N and all(len(reached(a,deleted=uv))==N for uv in edges)


def perfect_matchings(N,edges):
    a=adjacency(N,edges)
    masks=[sum(1<<v for v in neighbors) for neighbors in a]
    ei={uv:i for i,uv in enumerate(edges)}
    def visit(rem,chosen):
        if not rem:
            yield chosen
            return
        vertices=[]; scan=rem
        while scan:
            bit=scan & -scan; scan-=bit
            u=bit.bit_length()-1
            neighbors=masks[u]&rem
            if not neighbors:
                return
            vertices.append((neighbors.bit_count(),u,neighbors))
        unused,u,neighbors=min(vertices)
        while neighbors:
            bit=neighbors & -neighbors; neighbors-=bit
            v=bit.bit_length()-1
            yield from visit(rem ^ (1<<u) ^ bit,chosen | (1<<ei[edge(u,v)]))
    yield from visit((1<<N)-1,0)


def factor_lengths(N,edges,matching):
    factor=[uv for i,uv in enumerate(edges) if not (matching>>i)&1]
    a=adjacency(N,factor)
    need(all(len(s)==2 for s in a),'spanning degree two')
    lengths=[]; unseen=set(range(N))
    while unseen:
        component=reached(a,start=min(unseen))
        need(component<=unseen,'component partition')
        unseen-=component; lengths.append(len(component))
    return tuple(sorted(lengths))


def family(n, step=2, reverse=False):
    N,edges,links=graph(n,step=step,reverse=reverse)
    a=adjacency(N,edges)
    need(all(len(v)==3 for v in a),'cubic')
    need(bridgeless(N,edges),'bridgeless and connected')
    linkmask=sum(1<<edges.index(uv) for uv in links)
    full=(1<<len(edges))-1
    hist=Counter(); states=Counter(); seen=set()
    oddness=N; allodd=True
    for matching in perfect_matchings(N,edges):
        need(matching not in seen,'duplicate perfect matching')
        seen.add(matching)
        need(matching.bit_count()*2==N,'matching cardinality')
        lengths=factor_lengths(N,edges,matching)
        mask=(full ^ matching)&linkmask
        hist[lengths]+=1
        states[mask.bit_count()]+=1
        allodd &= all(length%2 for length in lengths)
        oddness=min(oddness,sum(length%2 for length in lengths))
    return {'n':n,'vertices':N,'edges':len(edges),'perfect_matchings':len(seen),
            'histogram':[{'lengths':list(k),'count':v} for k,v in sorted(hist.items())],
            'link_count_histogram':dict(sorted(states.items())),
            'all_factors_all_odd':bool(allodd),'oddness':oddness,
            'edge_sha256':hashlib.sha256(json.dumps(edges,separators=(',',':')).encode()).hexdigest()}


def main():
    P=petersen(); a=adjacency(10,P)
    allmatch=list(perfect_matchings(10,P))
    direct=[]
    for positions in combinations(range(15),5):
        degrees=[0]*10
        for k in positions:
            u,v=P[k]; degrees[u]+=1; degrees[v]+=1
        if degrees==[1]*10:
            direct.append(sum(1<<k for k in positions))
    need(set(allmatch)==set(direct) and len(direct)==6,'independent Petersen matching exhaustion')
    need(all(factor_lengths(10,P,m)==(5,5) for m in allmatch),'all Petersen factors')
    cuts=[]
    for mask in range(1,(1<<10)-1):
        cuts.append(sum(((mask>>u)&1)!=((mask>>v)&1) for u,v in P))
    need(min(cuts)==3,'all Petersen edge cuts')
    girth=100
    for u,v in P:
        todo=deque([(u,0)]); seen={u}
        while todo:
            w,d=todo.popleft()
            if w==v:
                girth=min(girth,d+1); break
            for z in a[w]:
                if edge(w,z)==edge(u,v) or z in seen:
                    continue
                seen.add(z); todo.append((z,d+1))
    need(girth==5,'Petersen girth')
    for uv in P:
        need(bridgeless(10,[x for x in P if x!=uv]),'every deleted-edge fragment')
        index=P.index(uv)
        need(sum(bool(m&(1<<index)) for m in allmatch)==2,'two avoiding/four containing factor states')
    results=[]
    for n in range(1,8):
        rec=family(n)
        need(rec['perfect_matchings']==2**n+4**n,'complete global matching count')
        need(rec['link_count_histogram']=={0:2**n,n:4**n},'global link alternatives')
        expected=Counter()
        expected[tuple([5]*(2*n))]+=2**n
        expected[tuple(sorted([5]*n+[5*n]))]+=4**n
        got={tuple(x['lengths']):x['count'] for x in rec['histogram']}
        need(got==dict(expected),'all global factor cycle types')
        need(rec['oddness']==(n+1 if n%2 else n),'oddness including even foils')
        need(rec['all_factors_all_odd']==bool(n%2),'oddness premise parity')
        results.append(rec)
    controls=[]
    def control(name,ok):
        need(ok,'control '+name); controls.append(name)
    N,e,_=graph(3,closing=False)
    control('missing_closing_link_is_not_cubic',any(len(x)!=3 for x in adjacency(N,e)))
    N,e,_=graph(3,restore=True)
    control('restoring_spokes_breaks_cubicity',any(len(x)!=3 for x in adjacency(N,e)))
    for n in [2,4,6]:
        control('even_n_'+str(n)+'_violates_all_odd_premise',not results[n-1]['all_factors_all_odd'])
    control('n1_is_only_Petersen_oddness_two',results[0]['oddness']==2)
    wrong=family(3,step=1)
    control('prism_fragments_fail_all_odd',not wrong['all_factors_all_odd'])
    control('zero_link_case_does_not_determine_minimum',results[2]['oddness']==4 and results[2]['oddness']!=6)
    control('Petersen_fragment_has_two_edge_boundary',len(graph(3)[2])==3 and
            sum((u<10)!=(v<10) for u,v in graph(3)[1])==2)
    reverse=family(3,reverse=True)
    control('reversing_all_links_is_a_valid_positive_foil',reverse['histogram']==results[2]['histogram'])
    cycle=[0,1,2,5,4]
    control('nonedge_cycle_corruption_rejected',any(edge(u,v) not in P for u,v in zip(cycle,cycle[1:]+cycle[:1])))
    print(json.dumps({'schema':'independent-pr1312-exact-v1','status':'PASS',
        'petersen':{'girth':girth,'cut_subsets':len(cuts),'minimum_edge_cut':min(cuts),
                    'perfect_matchings':len(allmatch),'all15_deleted_fragments_bridgeless':True},
        'families':results,'controls':controls,'control_count':len(controls),
        'source_author_programs_executed':False,
        'limitation':'Full finite checks corroborate, but do not replace, the written proof for every odd n>=3.'},sort_keys=True,indent=2))


if __name__=='__main__':
    main()
