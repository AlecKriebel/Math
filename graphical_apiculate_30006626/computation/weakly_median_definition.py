"""Direct weak modularity T,Q + no unconnected common-neighbor triplet.
Unlike TQ! shortcut, this uses defining conditions independently.
"""
from atlas_apex import *
def weak_median(G):
 V=list(G);d=dict(nx.all_pairs_shortest_path_length(G));N={x:set(G[x]) for x in V}
 for u in V:
  for v,w in itertools.combinations(V,2):
   if d[u][v]!=d[u][w]:continue
   k=d[u][v];C=N[v]&N[w]
   if d[v][w]==1 and k>1 and not any(d[u][x]==k-1 for x in C):return False,{'condition':'T','u':u,'v':v,'w':w}
   if d[v][w]==2 and k>=2 and any(d[u][z]==k+1 for z in C) and not any(d[u][x]==k-1 for x in C):return False,{'condition':'Q','u':u,'v':v,'w':w}
 for x,y in itertools.combinations(V,2):
  for t in itertools.combinations(N[x]&N[y],3):
   if not nx.is_connected(G.subgraph(t)):return False,{'condition':'unconnected_common_neighbor_triplet','x':x,'y':y,'triplet':t}
 return True,None
if __name__=='__main__':
 r=json.load(open(__file__.replace('weakly_median_definition.py','atlas_apex_results.json')));graphical=set(r['graphical_atlas_indices']);counts=collections.defaultdict(collections.Counter);differences=[]
 for idx,G in enumerate(nx.graph_atlas_g()):
  if not len(G) or not nx.is_connected(G):continue
  wm,w=weak_median(G);graph=idx in graphical
  counts[len(G)]['weakly_median' if wm else 'not_weakly_median']+=1
  if wm!=graph:differences.append({'atlas_index':idx,'order':len(G),'edges':sorted(G.edges()),'graphical':graph,'weakly_median':wm,'failure_witness':w})
 result={'counts':dict(counts),'differences':differences}
 with open(__file__.replace('weakly_median_definition.py','weakly_median_definition_results.json'),'w') as f:json.dump(result,f,indent=2)
 print(json.dumps(dict(counts)));print('differences',len(differences));print(json.dumps(differences[:2]))
