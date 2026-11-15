from pathlib import Path
import itertools,json,datetime,hashlib

def partitions(n,cap=None):
 if not n:return[()]
 return[(i,)+q for i in range(min(n,cap or n),0,-1)for q in partitions(n-i,i)]
def young(top):
 names=[partitions(k)for k in range(top+1)];layers=[[frozenset()]]
 for k in range(1,top+1):
  lookup={q:i for i,q in enumerate(names[k-1])};row=[]
  for q in names[k]:
   ps=set()
   for i in range(len(q)):
    z=list(q);z[i]-=1;z=tuple(sorted((v for v in z if v),reverse=True))
    if z in lookup:ps.add(lookup[z])
   row.append(frozenset(ps))
  layers.append(row)
 return layers
def reflect(layers,r):
 lower=layers[-1];zcount=len(layers[-2]);new=[frozenset(i for i,ps in enumerate(lower)if z in ps)for z in range(zcount)]
 new.extend(frozenset([i])for i in range(len(lower))for _ in range(r))
 return layers+[new]
def gram_differences(layers):
 out=[]
 for j in range(len(layers)-1):
  low=layers[j];up=layers[j+1];out.append([[sum(i in ps and k in ps for ps in up)-len(low[i]&low[k])for k in range(len(low))]for i in range(len(low))])
 return out
def ordinary(layers,r):
 return all(a[i][j]==(r if i==j else 0)for a in gram_differences(layers)for i in range(len(a))for j in range(len(a)))
def graph(v,e):
 v=set(v);e={tuple(sorted(q))for q in e};adj={x:set()for x in v}
 for x,y in e:adj[x].add(y);adj[y].add(x)
 unseen=set(v);components=[]
 while unseen:
  root=min(unseen);stack=[root];seen=set()
  while stack:
   x=stack.pop()
   if x in seen:continue
   seen.add(x);stack.extend(adj[x]-seen)
  unseen-=seen;components.append(sorted(seen))
 # Independent GF(2) edge-incidence column rank.
 ix={x:i for i,x in enumerate(sorted(v))};basis={}
 for x,y in sorted(e):
  col=(1<<ix[x])^(1<<ix[y])
  while col:
   k=col.bit_length()-1
   if k in basis:col^=basis[k]
   else:basis[k]=col;break
 beta=len(e)-len(v)+len(components);cycle_dim=len(e)-len(basis)
 assert beta==cycle_dim and beta>=0
 return {'vertices':sorted(v),'edges':sorted(e),'components':components,'beta':beta,'GF2_cycle_dimension':cycle_dim}
def bip(lower,upper):
 return graph([f'L{i}'for i in range(lower)]+[f'X{i}'for i in range(len(upper))],[(f'L{z}',f'X{x}')for x,ps in enumerate(upper)for z in ps])
def controls(name,layers,r):
 assert ordinary(layers,r)
 n=len(layers)-1;X=layers[-2];top=layers[-1];zcount=len(layers[-3]);S=[z for z in range(zcount)if any(ps=={z}for ps in X)]
 N={z:{x for x,ps in enumerate(X)if z in ps}for z in S};opts={z:[x for x,ps in enumerate(X)if ps=={z}]for z in S}
 H=graph([f'X{x}'for x in range(len(X))]+[f'Z{z}'for z in S],[(f'Z{z}',f'X{x}')for z in S for x in N[z]])
 prev=bip(zcount,X);nxt=bip(len(X),top);q=H['beta'];records=[]
 for choice in itertools.product(*(opts[z]for z in S)):
  witness=dict(zip(S,choice));assigned={};ke=set();kv={f'X{x}'for x in range(len(X))};minor=set()
  for z,a in witness.items():
   for y in N[z]-{a}:minor.add(tuple(sorted((f'X{a}',f'X{y}'))))
   for t,ps in enumerate(top):
    if a in ps and len(ps)>1:
     assert ps<=N[z]and t not in assigned
     assigned[t]=z;kv.add(f'T{t}');ke.update((f'T{t}',f'X{x}')for x in ps)
  K=graph(kv,ke);M=graph([f'X{x}'for x in range(len(X))],minor)
  # Contract t--a_z directly from the actual selected upper stars.
  contracted={tuple(sorted((f'X{witness[z]}',f'X{x}')))for t,z in assigned.items()for x in top[t]if x!=witness[z]}
  assert contracted==minor and M['beta']==K['beta']==q<=nxt['beta']and q<=prev['beta']
  records.append({'witnesses':witness,'K':K,'common_contracted_minor':M})
 p=[len(x)for x in layers];U=1+r*sum(p[:-2])+(r-1)*p[-2];local=r*p[-2]+p[-3]
 assert p[-1]==U-nxt['beta']and U-local==prev['beta']and p[-1]<=U-q
 return {'case':name,'r':r,'n':n,'rank_sizes':p,'whole_predecessor_layers':[[sorted(x)for x in row]for row in layers],'supported_z':S,'q':q,'b_previous':prev['beta'],'b_next':nxt['beta'],'U':U,'local_RHS':local,'refined_RHS':U-q,'residual_allowance':prev['beta']-q,'all_witness_products_checked':len(records),'witness_records':records,'all_z_two_singletons':all(len(opts.get(z,[]))>=2 for z in range(zcount))}
root=[[frozenset()]]
r3=root+[[frozenset([0])for _ in range(3)]]
r3.append([frozenset([0,1]),frozenset([0,2]),frozenset([1,2])]+[frozenset([i])for i in range(3)for _ in range(2)])
r3=reflect(r3,3)
y5=young(5);y7=reflect(reflect(y5,1),1)
cases=[controls('r3 sharp reflected Y^3 prefix',r3,3),controls('r1 sharp reflected Young prefix',y7,1),controls('Young n6 residual',young(6),1),controls('n2 r1 sole-terminal boundary',young(2),1),controls('n3 r1 two-singleton equality',young(3),1)]
assert cases[0]['rank_sizes']==[1,3,9,30]and cases[0]['q']==cases[0]['b_next']==1
assert cases[1]['rank_sizes']==[1,1,2,3,5,7,12,19]and cases[1]['q']==cases[1]['b_next']==1
assert cases[2]['q']==0 and cases[2]['b_previous']==1 and cases[2]['refined_RHS']==13 and cases[2]['local_RHS']==12 and cases[2]['rank_sizes'][-1]==11
assert cases[3]['q']==0 and cases[3]['all_witness_products_checked']==1
for c in cases[:2]:assert c['rank_sizes'][-1]>c['U']-2*c['q']
relaxed=root+[[frozenset([0])for _ in range(3)],[frozenset([0,1]),frozenset([0,2]),frozenset([1,2])],[frozenset([0,1,2])]+[frozenset([i])for i in range(3)for _ in range(2)]]
g=gram_differences(relaxed);assert g[0]==[[3]]and all(a[i][j]==(1 if i==j else 0)for a in g[1:]for i in range(len(a))for j in range(len(a)))and not ordinary(relaxed,1)
assert all(a[i][j]%2==(1 if i==j else 0)for a in g for i in range(len(a))for j in range(len(a)))
rel={'whole_predecessor_layers':[[sorted(x)for x in row]for row in relaxed],'rank_sizes':[len(x)for x in relaxed],'all_integer_Gram_differences':g,'ordinary_r1_prefix':False,'mod2_r1_commutator_holds_at_all_completed_ranks':True,'beta2':bip(3,relaxed[2])['beta'],'beta3':bip(3,relaxed[3])['beta'],'outside_category_failure':'p2=3 exceeds r1 cumulative RHS2; root discrepancy3−1 is zero only modulo2.'}
assert rel['beta2']==1 and rel['beta3']==0
out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','mechanism':'Own direct predecessor constructions, ordinary integer Gram differences, dual contractions to a common minor, independent GF2 incidence ranks; no source modules/results imported or run.','cases':cases,'outside_integer_category_control':rel,'negative_controls':{'coefficient2_rejected_in_both_sharp_examples':True,'Young_refined_RHS_equals_local_RHS_rejected':True,'relaxed_middle_layers_not_ordinary_prefix':True,'mod2_integer_substitution_rejected':True},'limits':'Five bounded hand-selected examples, not exhaustive differential-poset enumeration or proof of any unclaimed general recurrence.'}
p=Path(__file__).resolve().parent;(p/'INDEPENDENT_MINOR_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':len(cases),'witness_products':sum(c['all_witness_products_checked']for c in cases),'r3_q':cases[0]['q'],'r1_q':cases[1]['q'],'Young_residual':cases[2]['residual_allowance']}))
