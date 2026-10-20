"""Independent direct unique quasi-median checks for apiculate atlas graphs."""
from atlas_apex import *

def quasi_median_check(G):
    V=list(G);d=dict(nx.all_pairs_shortest_path_length(G))
    I={(u,v):{w for w in V if d[u][w]+d[w][v]==d[u][v]} for u in V for v in V}
    triangles=[t for t in itertools.product(V,repeat=3) if all(I[t[i],t[j]]&I[t[i],t[k]]=={t[i]} for i,j,k in ((0,1,2),(1,0,2),(2,0,1)))]
    for x in itertools.combinations(V,3):
        Q=[y for y in triangles if all(d[x[i]][y[i]]+d[y[i]][y[j]]+d[y[j]][x[j]]==d[x[i]][x[j]] for i,j in ((0,1),(0,2),(1,2)))]
        if len(Q)!=1:return False,{'triple':x,'quasi_medians':Q}
    return True,None
if __name__=='__main__':
    old=json.load(open(__file__.replace('generalized_median_check.py','atlas_apex_results.json')))
    bad={x['atlas_index'] for x in old['failures']};counts=collections.defaultdict(collections.Counter);detail=[]
    for idx,G in enumerate(nx.graph_atlas_g()):
        if not len(G) or not nx.is_connected(G):continue
        a,e=apex_table(G)
        if e:continue
        yes,w=quasi_median_check(G)
        counts[len(G)]['generalized_median' if yes else 'not_generalized_median']+=1
        if yes:counts[len(G)]['nongraphical_generalized_median' if idx in bad else 'graphical_generalized_median']+=1
        detail.append({'atlas_index':idx,'generalized_median':yes,'failure_witness':w})
    result={'counts':dict(counts),'details':detail}
    with open(__file__.replace('generalized_median_check.py','generalized_median_results.json'),'w') as f:json.dump(result,f,indent=2)
    print(json.dumps(dict(counts),indent=2))
