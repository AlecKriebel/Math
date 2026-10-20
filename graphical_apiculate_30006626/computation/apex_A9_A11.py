from atlas_apex import *
def identities(a,V):
 for u,v,w,x in itertools.product(V,repeat=4):
  lhs=a[a[u,w,x],a[a[u,v,x],w,x],u];rhs=a[u,w,x]
  if lhs!=rhs:return False,{'identity':'A9','u':u,'v':v,'w':w,'x':x,'lhs':lhs,'rhs':rhs}
  lhs=a[a[w,u,x],a[u,v,w],v];rhs=a[w,a[u,v,w],a[v,u,a[w,u,x]]]
  if lhs!=rhs:return False,{'identity':'A11','u':u,'v':v,'w':w,'x':x,'lhs':lhs,'rhs':rhs}
 return True,None
if __name__=='__main__':
 r=json.load(open(__file__.replace('apex_A9_A11.py','atlas_apex_results.json')));graphical=set(r['graphical_atlas_indices']);counts=collections.defaultdict(collections.Counter);differences=[]
 for idx,G in enumerate(nx.graph_atlas_g()):
  if not len(G) or not nx.is_connected(G):continue
  a,e=apex_table(G)
  if e:continue
  yes,w=identities(a,list(G));graph=idx in graphical
  counts[len(G)]['identities_true' if yes else 'identities_false']+=1
  if yes!=graph:differences.append({'atlas_index':idx,'order':len(G),'edges':sorted(G.edges()),'graphical':graph,'identities_true':yes,'failure_witness':w})
 result={'counts':dict(counts),'differences':differences}
 with open(__file__.replace('apex_A9_A11.py','apex_A9_A11_results.json'),'w') as f:json.dump(result,f,indent=2)
 print(json.dumps(dict(counts)));print('differences',len(differences));print(json.dumps(differences[:2]))
