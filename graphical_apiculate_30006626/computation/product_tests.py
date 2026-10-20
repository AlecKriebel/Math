from atlas_apex import *
def audit(G,label):
 G=nx.convert_node_labels_to_integers(G);V=list(G);a,e=apex_table(G);start=time.time()
 result={'name':label,'order':len(V),'edges':sorted(G.edges()),'apiculate':a is not None,'apex_failure':e,'closed_count':0,'subsets_tested':0,'bad_count':0,'first_failure':None}
 if e:return result
 # Closure only requires distinct triples: repeats always return an input.
 trip=[(sum(1<<x for x in t),1<<a[t]) for t in itertools.permutations(V,3)]
 for mask in range(1,1<<len(V)):
  result['subsets_tested']+=1
  if any(mask&inputs==inputs and not mask&output for inputs,output in trip):continue
  result['closed_count']+=1;S=[x for x in V if mask>>x&1];H,err=test_subset(S,a)
  if err:
   result['bad_count']+=1
   if result['first_failure'] is None:result['first_failure']={'subset':S,'canonical_edges':sorted(H.edges()),'failure':err}
 result['elapsed_seconds']=time.time()-start
 return result
if __name__=='__main__':
 house=nx.graph_atlas_g()[43]
 cases=[(nx.cartesian_product(house,nx.path_graph(2)),'house Cartesian K2'),(nx.cartesian_product(nx.cycle_graph(5),nx.path_graph(2)),'C5 Cartesian K2'),(nx.cartesian_product(house,nx.path_graph(3)),'house Cartesian P3')]
 results=[]
 for G,label in cases:
  r=audit(G,label);results.append(r);print(json.dumps(r),flush=True)
  with open(__file__.replace('product_tests.py','product_results.json'),'w') as f:json.dump(results,f,indent=2)
