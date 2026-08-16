#!/usr/bin/env python3
"""Primitive convention-frontier enumerator.

The input is only a rooted binary DAG.  The program implements two reductions:
  sd0   : retain reticulation arrowheads, suppress the root once, reject if the
          result is not already a simple binary mixed graph;
  clean : perform the same root operation and then repeatedly identify the
          resulting parallel copy and suppress the resulting unlabelled
          degree-two chain.

It enumerates the full root-created parallel-theta family (1,1,L), L=2..9,
an explicit strict rooting-fibre witness, and the four-leaf sharpness source.
No frozen topology table is read.
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "certificates" / "primary_convention_frontier.json"

@dataclass(frozen=True)
class MixedEdge:
    u: str
    v: str
    heads: tuple[str, ...] = ()
    def normalized(self):
        a,b=sorted((self.u,self.v))
        return MixedEdge(a,b,tuple(sorted(self.heads)))


def degrees(vertices, edges):
    indeg=Counter(); outdeg=Counter()
    for u,v in edges:
        outdeg[u]+=1; indeg[v]+=1
    return indeg,outdeg


def is_acyclic(vertices, edges):
    indeg=Counter(v for _,v in edges)
    child=defaultdict(list)
    for u,v in edges: child[u].append(v)
    q=deque(sorted(v for v in vertices if indeg[v]==0)); seen=0
    while q:
        u=q.popleft(); seen+=1
        for v in child[u]:
            indeg[v]-=1
            if indeg[v]==0:q.append(v)
    return seen==len(vertices)


def reachable(root, edges):
    child=defaultdict(list)
    for u,v in edges: child[u].append(v)
    seen={root}; q=deque([root])
    while q:
        u=q.popleft()
        for v in child[u]:
            if v not in seen:
                seen.add(v);q.append(v)
    return seen


def is_lsa(root, vertices, edges, leaves):
    """Root is the unique vertex stable for every leaf."""
    for ban in sorted(vertices-{root}):
        child=defaultdict(list)
        for u,v in edges:
            if ban not in (u,v): child[u].append(v)
        seen={root};q=deque([root])
        while q:
            u=q.popleft()
            for v in child[u]:
                if v not in seen:seen.add(v);q.append(v)
        if all(x not in seen for x in leaves): return False
    return True


def biconnected_components(vertices, undirected_edges):
    """Tarjan edge-block decomposition; returns vertex sets of edge blocks."""
    adj=defaultdict(list)
    for i,(a,b) in enumerate(undirected_edges):
        adj[a].append((b,i));adj[b].append((a,i))
    disc={};low={};parent_edge={};stack=[];time=0;blocks=[]
    def dfs(u):
        nonlocal time
        time+=1;disc[u]=low[u]=time
        for v,eid in adj[u]:
            if eid==parent_edge.get(u):continue
            if v not in disc:
                parent_edge[v]=eid;stack.append(eid);dfs(v);low[u]=min(low[u],low[v])
                if low[v]>=disc[u]:
                    block=set()
                    while stack:
                        x=stack.pop();a,b=undirected_edges[x];block|={a,b}
                        if x==eid:break
                    if block:blocks.append(block)
            elif disc[v]<disc[u]:
                stack.append(eid);low[u]=min(low[u],disc[v])
    for u in sorted(vertices):
        if u not in disc:dfs(u)
    return blocks


def classify_rooted(vertices, edges, root, leaves):
    vertices=set(vertices);leaves=set(leaves);edges=tuple(edges)
    if len(edges)!=len(set(edges)) or any(u==v for u,v in edges):return None
    if not is_acyclic(vertices,edges) or reachable(root,edges)!=vertices:return None
    indeg,outdeg=degrees(vertices,edges);types={}
    for v in vertices:
        d=(indeg[v],outdeg[v])
        if v==root:
            if d!=(0,2):return None
            types[v]='root'
        elif v in leaves:
            if d!=(1,0):return None
            types[v]='leaf'
        elif d==(1,2):types[v]='tree'
        elif d==(2,1):types[v]='retic'
        else:return None
    if not is_lsa(root,vertices,edges,leaves):return None
    ch=defaultdict(list)
    for u,v in edges:ch[u].append(v)
    tc=all(any(types[c] in {'tree','leaf'} for c in ch[v]) for v in vertices-leaves)
    internal=vertices-leaves
    und=[(u,v) for u,v in edges if u in internal and v in internal]
    retics={v for v,t in types.items() if t=='retic'}
    blocks=biconnected_components(internal,und)
    level=max([len(retics & b) for b in blocks] or [0])
    return {'types':types,'tree_child':tc,'level':level,'retics':sorted(retics),
            'blocks':[sorted(b) for b in blocks]}


def raw_semideorientation(vertices,edges,root,leaves):
    info=classify_rooted(vertices,edges,root,leaves)
    if not info:raise ValueError('invalid rooted input')
    types=info['types'];children=[v for u,v in edges if u==root]
    if len(children)!=2:raise AssertionError
    raw=[]
    for u,v in edges:
        if u==root:continue
        raw.append(MixedEdge(u,v,(v,) if types[v]=='retic' else ()).normalized())
    p,q=children
    heads=tuple(sorted(v for v in (p,q) if types[v]=='retic'))
    raw.append(MixedEdge(p,q,heads).normalized())
    return {'vertices':set(vertices)-{root},'leaves':set(leaves),'edges':raw,'root_children':children,'types':types}


def edge_map_from(raw):
    em={}
    for e in raw:
        k=(e.u,e.v)
        em.setdefault(k,[]).append(tuple(e.heads))
    return em


def sd0_reduce(vertices,edges,root,leaves):
    raw=raw_semideorientation(vertices,edges,root,leaves)
    em=edge_map_from(raw['edges'])
    if any(len(v)!=1 for v in em.values()):return None
    # A standard mixed edge cannot have two arrowheads.
    if any(len(h[0])>1 for h in em.values()):return None
    m={'vertices':raw['vertices'],'leaves':raw['leaves'],
       'edges':[MixedEdge(a,b,h[0]) for (a,b),h in sorted(em.items())]}
    return m if is_simple_binary_mixed(m) else None


def merge_parallel(edge_map,a,b,heads):
    if a==b:raise ValueError('loop')
    a,b=sorted((a,b));key=(a,b)
    old=edge_map.get(key,())
    edge_map[key]=tuple(sorted(set(old)|set(heads)))


def clean_reduce(vertices,edges,root,leaves,trace=False):
    raw=raw_semideorientation(vertices,edges,root,leaves)
    edge_map={};steps=[]
    for e in raw['edges']:
        before=(e.u,e.v) in edge_map
        merge_parallel(edge_map,e.u,e.v,e.heads)
        if before:steps.append({'operation':'identify_parallel','pair':[e.u,e.v]})
    active=set(raw['vertices']);leaves=set(leaves)
    while True:
        inc=defaultdict(list)
        for (a,b),h in edge_map.items():
            inc[a].append(((a,b),h));inc[b].append(((a,b),h))
        candidates=[v for v in sorted(active-leaves) if len(inc[v])==2]
        if not candidates:break
        v=candidates[0];(k1,h1),(k2,h2)=inc[v]
        a=k1[1] if k1[0]==v else k1[0]
        b=k2[1] if k2[0]==v else k2[0]
        del edge_map[k1];del edge_map[k2];active.remove(v)
        if a==b:raise ValueError('loop during cleanup')
        heads=[]
        if a in h1:heads.append(a)
        if b in h2:heads.append(b)
        was=(tuple(sorted((a,b))) in edge_map)
        merge_parallel(edge_map,a,b,heads)
        steps.append({'operation':'suppress_degree_two','vertex':v,'neighbors':[a,b],
                      'created_parallel':was})
    m={'vertices':active,'leaves':leaves,
       'edges':[MixedEdge(a,b,h) for (a,b),h in sorted(edge_map.items())]}
    if not is_simple_binary_mixed(m):raise ValueError('cleanup did not yield simple binary mixed graph')
    if trace:m['cleanup_trace']=steps
    return m


def mixed_stats(m):
    deg=Counter();incoming=Counter();outgoing=Counter();und=Counter()
    for e in m['edges']:
        deg[e.u]+=1;deg[e.v]+=1
        if not e.heads:und[e.u]+=1;und[e.v]+=1
        elif len(e.heads)==1:
            h=e.heads[0];incoming[h]+=1;outgoing[e.v if h==e.u else e.u]+=1
        else:
            incoming[e.u]+=1;incoming[e.v]+=1
    return deg,incoming,outgoing,und


def is_simple_binary_mixed(m):
    seen=set();deg,incoming,outgoing,und=mixed_stats(m)
    for e in m['edges']:
        if e.u==e.v or (e.u,e.v) in seen or len(e.heads)>1:return False
        seen.add((e.u,e.v))
    for v in m['vertices']:
        if v in m['leaves']:
            if deg[v]!=1:return False
        elif deg[v]!=3:return False
        if incoming[v] not in (0,2):return False
    return True


def canonical_mixed(m):
    """Exact individualization-refinement code for a labelled mixed graph."""
    deg,incoming,outgoing,und=mixed_stats(m)
    colors={}
    for v in m['vertices']:
        if v in m['leaves']:
            colors[v]='L:'+v
        elif incoming[v]==2:
            colors[v]='R'
        else:
            colors[v]='I'
    neigh={v:[] for v in m['vertices']}
    for e in m['edges']:
        if not e.heads:
            neigh[e.u].append(('U',e.v));neigh[e.v].append(('U',e.u))
        elif len(e.heads)==1:
            h=e.heads[0];t=e.v if h==e.u else e.u
            neigh[t].append(('D+',h));neigh[h].append(('D-',t))
        else:
            neigh[e.u].append(('H',e.v));neigh[e.v].append(('H',e.u))
    groups=defaultdict(list)
    for v,c in colors.items():groups[c].append(v)
    part=tuple(tuple(sorted(groups[c])) for c in sorted(groups))
    def refine(partition):
        while True:
            ci={v:i for i,cell in enumerate(partition) for v in cell}
            ans=[];changed=False
            for cell in partition:
                blocks=defaultdict(list)
                for v in cell:
                    cnt=Counter((r,ci[w]) for r,w in neigh[v])
                    sig=tuple(sorted(cnt.items()))
                    blocks[sig].append(v)
                if len(blocks)>1:changed=True
                ans.extend(tuple(sorted(blocks[k])) for k in sorted(blocks,key=repr))
            partition=tuple(ans)
            if not changed:return partition
    def leaf_code(partition):
        order=tuple(cell[0] for cell in partition);mp={v:i for i,v in enumerate(order)}
        rows=[]
        for e in m['edges']:
            a,b=mp[e.u],mp[e.v]
            if not e.heads:
                if a>b:a,b=b,a
                rows.append(('U',a,b))
            elif len(e.heads)==1:
                h=mp[e.heads[0]];t=b if e.heads[0]==e.u else a
                rows.append(('D',t,h))
            else:
                if a>b:a,b=b,a
                rows.append(('H',a,b))
        return (tuple(colors[v] for v in order),tuple(sorted(rows))),mp
    def search(partition):
        partition=refine(partition)
        if all(len(c)==1 for c in partition):return leaf_code(partition)
        i=next(i for i,c in enumerate(partition) if len(c)>1);cell=partition[i]
        best=None;bestmap=None
        for v in cell:
            rem=tuple(x for x in cell if x!=v)
            cand=search(partition[:i]+((v,),rem)+partition[i+1:])
            if best is None or cand[0]<best:best,bestmap=cand
        return best,bestmap
    code,mp=search(part)
    return {'code':repr(code),'sha256':sha256(repr(code).encode()).hexdigest(),
            'vertex_map':mp}


def same_labeled_mixed(first,second):
    if first['vertices']!=second['vertices'] or first['leaves']!=second['leaves']:
        return False
    def rows(m):
        return sorted((e.u,e.v,tuple(e.heads)) for e in m['edges'])
    return rows(first)==rows(second)


def root_orientations(m, root_edge):
    """Enumerate binary rooted orientations by exact degree-constrained backtracking."""
    root='ROOT'; E=m['edges']
    deg,incount,_out,_und=mixed_stats(m)
    target={}
    for v in m['vertices']:
        if v in m['leaves']: target[v]=(1,0)
        elif incount[v]==2: target[v]=(2,1)
        else: target[v]=(1,2)
    fixed=[]; free=[]
    re=E[root_edge]
    if len(re.heads)>1:return []
    # The root replaces the selected edge and sends one arc to each endpoint.
    fixed.extend([(root,re.u),(root,re.v)])
    for i,e in enumerate(E):
        if i==root_edge:continue
        if len(e.heads)==1:
            h=e.heads[0];t=e.v if h==e.u else e.u;fixed.append((t,h))
        elif not e.heads:free.append((e.u,e.v))
        else:return []
    indeg=Counter(v for _,v in fixed);outdeg=Counter(u for u,_ in fixed)
    rem_in={v:target[v][0]-indeg[v] for v in m['vertices']}
    rem_out={v:target[v][1]-outdeg[v] for v in m['vertices']}
    if any(rem_in[v]<0 or rem_out[v]<0 for v in m['vertices']):return []
    incidence=Counter(x for e in free for x in e)
    if any(rem_in[v]+rem_out[v]!=incidence[v] for v in m['vertices']):return []
    results=[]
    def rec(left,chosen):
        if not left:
            if any(rem_in[v] or rem_out[v] for v in m['vertices']):return
            directed=tuple(fixed+chosen); V=set(m['vertices'])|{root}
            info=classify_rooted(V,directed,root,m['leaves'])
            if not info:return
            red=sd0_reduce(V,directed,root,m['leaves'])
            if red is None or not same_labeled_mixed(red,m):return
            results.append((directed,info));return
        # Pick the most constrained edge.
        best_i=0;best_opts=None
        for i,(a,b) in enumerate(left):
            opts=[]
            if rem_out[a]>0 and rem_in[b]>0:opts.append((a,b))
            if rem_out[b]>0 and rem_in[a]>0:opts.append((b,a))
            if best_opts is None or len(opts)<len(best_opts):
                best_i=i;best_opts=opts
                if len(opts)<=1:break
        if not best_opts:return
        a,b=left[best_i];rest=left[:best_i]+left[best_i+1:]
        for u,v in best_opts:
            rem_out[u]-=1;rem_in[v]-=1
            rec(rest,chosen+[(u,v)])
            rem_out[u]+=1;rem_in[v]+=1
    rec(list(free),[])
    # Deduplicate identical arc sets (can arise only from symmetric branch order).
    uniq={tuple(sorted(d)):info for d,info in results}
    return [(d,uniq[d]) for d in sorted(uniq)]


def rooting_census(m):
    rec=[]
    for i,_e in enumerate(m['edges']):
        for directed,info in root_orientations(m,i):
            rec.append({'edge_index':i,'arc_sha256':sha256(repr(directed).encode()).hexdigest(),
                        'tree_child':info['tree_child']})
    return {'valid':len(rec),'tree_child':sum(r['tree_child'] for r in rec),
            'weak':any(r['tree_child'] for r in rec),
            'strong':bool(rec) and all(r['tree_child'] for r in rec),
            'records':rec}


def parallel_theta_family(L):
    """Root children p,q are adjacent and also joined by a path of L edges."""
    internal=[f'v{i}' for i in range(1,L)]
    leaves={f'L{i}' for i in range(1,L)}
    vertices={'rho','p','q',*internal,*leaves}
    path=['p',*internal,'q'];segments=list(zip(path,path[1:]))
    fixed=[('rho','p'),('rho','q')]+[(v,f'L{i}') for i,v in enumerate(internal,1)]
    out=[]
    for direct in (("p","q"),("q","p")):
        for bits in product((0,1),repeat=L):
            oriented=[(u,v) if b==0 else (v,u) for (u,v),b in zip(segments,bits)]
            E=tuple(fixed+[direct]+oriented)
            info=classify_rooted(vertices,E,'rho',leaves)
            if not info or info['level']>2:continue
            try:clean=clean_reduce(vertices,E,'rho',leaves,trace=True)
            except ValueError:continue
            canon=canonical_mixed(clean);rc=rooting_census(clean)
            out.append({'L':L,'direct':list(direct),'bits':''.join(map(str,bits)),
                        'rooted_tree_child':info['tree_child'],'rooted_retics':info['retics'],
                        'clean_code':canon['sha256'],'clean_vertices':len(clean['vertices']),
                        'clean_edges':len(clean['edges']),'clean_weak':rc['weak'],
                        'clean_strong':rc['strong'],'clean_rootings':rc['valid'],
                        'cleanup_trace':clean['cleanup_trace']})
    return out


def strict_fibre_witness():
    V={'rho','p','q','a','b','d','L1','L2','L3'};L={'L1','L2','L3'}
    E=(('rho','p'),('rho','q'),('p','q'),('p','a'),('q','b'),
       ('b','d'),('d','a'),('a','L1'),('b','L2'),('d','L3'))
    info=classify_rooted(V,E,'rho',L)
    assert info and info['level']==2 and not info['tree_child']
    assert sd0_reduce(V,E,'rho',L) is None
    clean=clean_reduce(V,E,'rho',L,trace=True);rc=rooting_census(clean)
    assert rc['strong'] and rc['valid']==5
    return {'vertices':sorted(V),'leaves':sorted(L),'arcs':[list(x) for x in E],
            'rooting_tree_child':False,'level':2,'clean_code':canonical_mixed(clean),
            'clean_rooting_census':rc,'cleanup_trace':clean['cleanup_trace']}


def triangle_leaf_status(m,leaf):
    adj=defaultdict(set)
    for e in m['edges']:adj[e.u].add(e.v);adj[e.v].add(e.u)
    internal=sorted(set(m['vertices'])-set(m['leaves']))
    tris=[]
    for i,a in enumerate(internal):
        for j in range(i+1,len(internal)):
            b=internal[j]
            for k in range(j+1,len(internal)):
                c=internal[k]
                if b in adj[a] and c in adj[a] and c in adj[b]:tris.append({a,b,c})
    parent=next(v for v in adj[leaf])
    return {'triangle_count':len(tris),'leaf_parent':parent,
            'leaf_parent_in_triangle':any(parent in T for T in tris)}


def theta_sharpness_pair():
    V={'rho','A','B','C','D','E','F','L1','L2','L3','L4'};L={'L1','L2','L3','L4'}
    common=(('rho','A'),('rho','C'),('A','B'),('B','C'),('C','D'),('D','E'),
       ('A','F'),('E','F'))
    source=common+(('B','L1'),('D','L2'),('F','L3'),('E','L4'))
    target=common+(('E','L1'),('D','L2'),('F','L3'),('B','L4'))
    rows=[]
    for name,E in [('source',source),('target',target)]:
        info=classify_rooted(V,E,'rho',L);assert info and info['tree_child'] and info['level']==2
        sd=sd0_reduce(V,E,'rho',L);cl=clean_reduce(V,E,'rho',L)
        assert sd and canonical_mixed(sd)['code']==canonical_mixed(cl)['code']
        rc=rooting_census(cl);assert rc['valid']==5 and rc['tree_child']==2 and rc['weak'] and not rc['strong']
        rows.append({'name':name,'arcs':[list(x) for x in E],'sd0_equals_clean':True,
            'code':canonical_mixed(cl),'rooting_census':rc,
            'leaf1_status':triangle_leaf_status(cl,'L1')})
    assert rows[0]['code']['code']!=rows[1]['code']['code']
    assert rows[0]['leaf1_status']['leaf_parent_in_triangle'] is True
    assert rows[1]['leaf1_status']['leaf_parent_in_triangle'] is False
    return {'vertices':sorted(V),'leaves':sorted(L),'topologies':rows,
            'nonisomorphic':True,'non_T_equivalent':True,
            'reason':'Leaf 1 is adjacent to a triangle vertex only in the source; T preserves the labelled underlying graph.'}


def main():
    families={str(L):parallel_theta_family(L) for L in range(2,10)}
    summary={};fibres={}
    for L,rec in families.items():
        by=defaultdict(list)
        for r in rec:by[r['clean_code']].append(r)
        fibre_rows=[]
        for code,rows in sorted(by.items()):
            # Every sd0 rooting is also a cleanup rooting; the raw rows here are
            # additional root-created-parallel presentations.
            sd0_weak=rows[0]['clean_weak'];sd0_strong=rows[0]['clean_strong']
            extra_tc=sum(x['rooted_tree_child'] for x in rows)
            fibre_rows.append({'clean_graph_code':code,'raw_artifact_rootings':len(rows),
                'raw_artifact_tree_child_rootings':extra_tc,
                'sd0_weak':sd0_weak,'sd0_strong':sd0_strong,
                'cleanup_weak_in_this_fibre':sd0_weak or extra_tc>0,
                'cleanup_strong_in_this_fibre':sd0_strong and all(x['rooted_tree_child'] for x in rows)})
        fibres[L]=fibre_rows
        summary[L]={'valid_raw_artifact_presentations':len(rec),
                    'tree_child_raw_artifact_presentations':sum(r['rooted_tree_child'] for r in rec),
                    'canonical_clean_target_graphs':len(by),
                    'cleanup_weak_targets_in_frontier':sum(x['cleanup_weak_in_this_fibre'] for x in fibre_rows),
                    'cleanup_strong_targets_in_frontier':sum(x['cleanup_strong_in_this_fibre'] for x in fibre_rows)}
    assert summary['2']['valid_raw_artifact_presentations']==0
    assert summary['3']['tree_child_raw_artifact_presentations']==0
    assert [summary[str(L)]['tree_child_raw_artifact_presentations'] for L in range(4,10)]==[2,4,6,8,10,12]
    cert={'status':'EXACTLY COMPUTED','scope':'binary LSA-valid level-2 root-created cleanup frontier',
          'path_length_frontier':summary,'cleanup_fibres':fibres,'records':families,
          'strict_rooting_fibre_witness':strict_fibre_witness(),
          'theta_sharpness_pair':theta_sharpness_pair(),
          'structural_conclusions':{
              'SD0_subset_SDclean':True,
              'cleanup_graphs_have_canonical_sd0_refinement_on_binary_LSA_inputs':True,
              'W_clean_equals_W_sd0':True,
              'S_clean_subset_S_sd0':True,
              'strict_rooting_fibre_witness_proves_subset_strict':True,
              'parallel_theta_112_valid_rooting':False,
              'parallel_theta_113_tree_child_rooting':False,
              'parallel_theta_first_tree_child_L':4}}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'frontier':summary,'strict_witness':cert['strict_rooting_fibre_witness']['clean_rooting_census'],
                      'theta':cert['theta_sharpness_pair']['topologies'][0]['rooting_census']},indent=2,sort_keys=True))
    print('PASS primary convention frontier')

if __name__=='__main__':main()
