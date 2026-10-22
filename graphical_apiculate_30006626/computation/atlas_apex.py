"""Exhaustive unlabeled graph atlas check (NetworkX atlas, orders 1--7).
Canonical adjacency is forced by a(x,y,z)=z iff z lies in I(x,y).
All subsets, not just induced subgraphs, are checked for ternary closure.
"""
import sys,json,itertools,collections,time
import networkx as nx

def apex_table(G):
    V=list(G); d=dict(nx.all_pairs_shortest_path_length(G))
    if any(len(d[x])!=len(V) for x in V):return None,{'disconnected':True}
    I={(x,y):{z for z in V if d[x][z]+d[z][y]==d[x][y]} for x in V for y in V}
    a={}
    for u,v,w in itertools.product(V,repeat=3):
        C=I[u,v]&I[u,w]
        maximal=[x for x in C if not any(x!=y and x in I[u,y] for y in C)]
        if len(maximal)!=1:return None,{'triple':[u,v,w],'maximal':maximal}
        a[u,v,w]=maximal[0]
    return a,None

def test_subset(S,a):
    H=nx.Graph();H.add_nodes_from(S)
    H.add_edges_from((x,y) for x,y in itertools.combinations(S,2) if not any(a[x,y,z]==z for z in S if z!=x and z!=y))
    b,err=apex_table(H)
    if err:return H,{'realization_not_apiculate':err}
    for t in itertools.product(S,repeat=3):
        if a[t]!=b[t]:return H,{'operation_mismatch':{'triple':t,'original':a[t],'canonical':b[t]}}
    return H,None

def main():
    stats=collections.defaultdict(collections.Counter);failures=[];graphical=[];start=time.time()
    for idx,G in enumerate(nx.graph_atlas_g()):
        n=len(G)
        if not n or not nx.is_connected(G):continue
        stats[n]['connected']+=1
        a,err=apex_table(G)
        if err:continue
        stats[n]['apiculate']+=1
        bad=[];closed=0
        for mask in range(1,1<<n):
            S=[x for x in G if (mask>>x)&1];ss=set(S)
            if any(a[t] not in ss for t in itertools.product(S,repeat=3)):continue
            closed+=1;stats[n]['closed_subsets']+=1
            H,err=test_subset(S,a)
            if err:
                stats[n]['bad_closed_subsets']+=1
                bad.append({'subset':S,'canonical_edges':sorted(H.edges()),'failure':err})
        if bad:
            stats[n]['nongraphical']+=1
            failures.append({'atlas_index':idx,'order':n,'edges':sorted(G.edges()),'closed_subsets':closed,'witnesses':bad})
            if len(failures)==1:print('FIRST FAILURE',json.dumps(failures[-1]),flush=True)
        else:stats[n]['graphical']+=1;graphical.append(idx)
    result={'method':'All connected graph atlas entries of orders 1 through 7; every nonempty ternary-closed subset; forced canonical realization tested','networkx_version':nx.__version__,'elapsed_seconds':time.time()-start,'counts':dict(stats),'failures':failures,'graphical_atlas_indices':graphical}
    path=__file__.replace('atlas_apex.py','atlas_apex_results.json')
    with open(path,'w') as f:json.dump(result,f,indent=2)
    print(json.dumps(dict(stats),indent=2));print('Failures',len(failures),'seconds',result['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
