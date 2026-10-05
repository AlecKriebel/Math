import pathlib,json,itertools,collections,math,random,datetime,hashlib
from fractions import Fraction as Q
R=pathlib.Path(__file__).resolve().parent
P=R/'private/fresh_external_copy'
E=json.loads((P/'expected/priority_laws.json').read_text())
def states(n): return list(itertools.product((0,1),repeat=n))
def mtp(w):
 bad=[]
 for a,b in itertools.product(w,repeat=2):
  lo=tuple(x&y for x,y in zip(a,b));hi=tuple(x|y for x,y in zip(a,b))
  if w[lo]*w[hi]<w[a]*w[b]:bad.append((a,b))
 return bad
def separation(n,edges,A,B,C):
 # Independent transitive-closure test, instead of candidate DFS.
 reach=[[i==j for j in range(n)] for i in range(n)]
 for i,j in edges:
  if i not in C and j not in C:reach[i][j]=reach[j][i]=True
 for k in range(n):
  for i in range(n):
   for j in range(n):reach[i][j]=reach[i][j] or (reach[i][k] and reach[k][j])
 return all(not reach[i][j] for i in A for j in B)
def checks(n,edges,w):
 X=states(n);sep=[];bad=[];count=0;canonical=set();cipoly=0
 for assign in itertools.product(range(4),repeat=n):
  A=tuple(i for i,v in enumerate(assign) if v==0);B=tuple(i for i,v in enumerate(assign) if v==1);C=tuple(i for i,v in enumerate(assign) if v==2)
  if not A or not B or not separation(n,edges,A,B,C):continue
  sep.append({'A':[i+1 for i in A],'B':[i+1 for i in B],'C':[i+1 for i in C]})
  for c in states(len(C)):
   fiber=[x for x in X if tuple(x[i] for i in C)==c]
   pc=sum(w[x] for x in fiber)
   rows=states(len(A));cols=states(len(B))
   cells={(a,b):[x for x in fiber if tuple(x[i] for i in A)==a and tuple(x[i] for i in B)==b] for a in rows for b in cols}
   sums={key:sum(w[x] for x in xx) for key,xx in cells.items()}
   for a,b in itertools.product(rows,cols):
    pac=sum(v for (ar,br),v in sums.items() if ar==a);pbc=sum(v for (ar,br),v in sums.items() if br==b)
    cipoly+=1
    if sums[a,b]*pc!=pac*pbc:bad.append((A,B,C,c,a,b))
   for a1,a2 in itertools.combinations(rows,2):
    for b1,b2 in itertools.combinations(cols,2):
     count+=1
     polynomial=collections.Counter()
     for x,y in itertools.product(cells[a1,b1],cells[a2,b2]):polynomial[tuple(sorted((x,y)))]+=1
     for x,y in itertools.product(cells[a1,b2],cells[a2,b1]):polynomial[tuple(sorted((x,y)))]-=1
     terms=sorted((xy,v) for xy,v in polynomial.items() if v)
     sign=1 if terms[0][1]>0 else -1
     canonical.add(tuple((xy,sign*v) for xy,v in terms))
 return sep,bad,count,len(canonical),cipoly
result={}
for name,r in E['laws'].items():
 n=r['n'];edges=[tuple(i-1 for i in edge) for edge in r['edges']]
 w={tuple(map(int,k)):v for k,v in r['integer_weights'].items()}
 assert len(w)==2**n and set(w)==set(states(n))
 sep,bad,count,unique,polycount=checks(n,edges,w)
 assert sep==r['all_separations'] and not bad
 assert not mtp(w) and r['mtp2_failure_count']==0
 assert sum(w.values())==r['normalizer']
 assert count==r['unique_conditioning_2x2_minors_checked']
 inv=r['invariant'];left=[tuple(x) for x in inv['left_states']];right=[tuple(x) for x in inv['right_states']]
 products=[math.prod(w[x] for x in xx) for xx in [left,right]]
 assert products==inv['integer_products']
 actualfrac=[str(Q(v,sum(w.values())**len(xx))) for v,xx in zip(products,[left,right])]
 assert actualfrac==inv['normalized_products']
 assert str(Q(products[0]-products[1],sum(w.values())**len(left)))==inv['normalized_difference']
 for edge,record in zip(edges,inv['edge_balances']):
  counts=[dict(collections.Counter(''.join(str(x[i]) for i in edge) for x in xx)) for xx in [left,right]]
  assert counts[0]==record['left'] and counts[1]==record['right'] and counts[0]==counts[1]
 result[name]={'all_source_weights_read':True,'global_markov_polynomial_equations_checked':polycount,'ordered_separations':len(sep),'ordered_minors_evaluated':count,'distinct_formal_minor_polynomials_up_to_sign':unique,'mtp2_all_pairs':len(w)**2,'invariant_products':products,'PASS':True}
# Fully independently re-evaluate all recoding outputs.
controls={}
supports={'gms_example7':['0000','0001','1000','0011','1100','0111','1110','1111'],'gms_example8':['0100','0111','1001','1010']}
for name,supp in supports.items():
 counts={}
 for flip in states(4):
  transformed={tuple(int(a)^b for a,b in zip(x,flip)) for x in supp}
  w={x:int(x in transformed) for x in states(4)}
  counts[''.join(map(str,flip))]=len(mtp(w))
 assert counts==E['recoding_controls'][name]['all_16_coordinate_flips_mtp2_failure_counts']
 controls[name]=counts
# Negative and limiting laws: void V; arbitrary independent isolates; bad implication/smoothing;
# correlated disconnected coordinates violate global Markov; a heavy bottom violates MTP2.
negative={}
wempty={():Q(1)};assert not mtp(wempty)
isolate={x:Q(1,3) if x[0]==0 else Q(2,3) for x in states(1)};assert sum(isolate.values())==1 and not mtp(isolate)
correlated={x:Q(1,2) if x[0]==x[1] else Q(0) for x in states(2)}
assert checks(2,[],correlated)[1]
negative['disconnected_equality_is_MTP2_but_not_global_Markov']=True
w={tuple(map(int,x)):v for x,v in E['laws']['released_candidate_C4']['integer_weights'].items()}
w[(1,1,1,1)]=0;assert mtp(w)
negative['missing_join_zero_rejected_by_whole_lattice_MTP2']=True
smooth={(0,0):Q(1),(0,1):Q(1),(1,0):Q(1,10),(1,1):Q(1,100)}
assert mtp(smooth);negative['naive_smoothing_rejected']=True
# Fraction-capacity residual identity, arbitrary edge orientations, up to six vertices.
rng=random.Random(2026100417);flow_cases=flow_assignments=0
for n in range(7):
 for sample in range(30):
  edges=[(i,j) if rng.randrange(2) else (j,i) for i,j in itertools.combinations(range(n),2) if rng.randrange(2)]
  h=[Q(rng.randrange(-14,15),rng.randrange(1,8)) for i in range(n)]
  J=[Q(rng.randrange(0,15),rng.randrange(1,8)) for e in edges]
  s=n;t=n+1;cap=collections.defaultdict(Q);unary=[-v for v in h]
  for (i,j),v in zip(edges,J):cap[i,j]+=v;unary[i]-=v
  for i,v in enumerate(unary):
   if v>=0:cap[i,t]+=v
   else:cap[s,i]-=v
  res=collections.defaultdict(Q,cap);flow=Q(0)
  while True:
   paths=[[s]];path=None
   while paths and path is None:
    walk=paths.pop(0);i=walk[-1]
    for j in range(n+2):
     if j not in walk and res[i,j]>0:
      if j==t:path=walk+[j];break
      paths.append(walk+[j])
   if path is None:break
   arcs=list(zip(path,path[1:]));amount=min(res[e] for e in arcs)
   for i,j in arcs:res[i,j]-=amount;res[j,i]+=amount
   flow+=amount
  energy={x:-sum(v*x[i] for i,v in enumerate(h))-sum(v*x[i]*x[j] for (i,j),v in zip(edges,J)) for x in states(n)}
  minimum=min(energy.values());costs=[]
  for x,en in energy.items():
   U={s}|{i for i,v in enumerate(x) if v}
   cut=sum(v for (i,j),v in cap.items() if i in U and j not in U)
   rcost=sum(v for (i,j),v in res.items() if i in U and j not in U)
   assert rcost==cut-flow==en-minimum and rcost>=0
   costs.append(cut)
   # Exact unary/edge local residual product exponents are the whole residual cut.
   local=sum(res[s,i]*(1-x[i])+res[i,t]*x[i] for i in range(n))
   local+=sum(res[i,j]*x[i]*(1-x[j])+res[j,i]*x[j]*(1-x[i]) for i,j in edges)
   assert local==rcost
  assert flow==min(costs) and min(en-minimum for en in energy.values())==0
  allowed={frozenset(e) for e in edges}
  assert all(i>=n or j>=n or frozenset((i,j)) in allowed or v==0 for (i,j),v in res.items())
  flow_cases+=1;flow_assignments+=len(energy)
# Facial-support lemma independent brute sampling from original-edge energies.
facial=facial_lattice=0
for n in range(2,5):
 for mask in range(1,2**(n*(n-1)//2)):
  possible=list(itertools.combinations(range(n),2));edges=[e for k,e in enumerate(possible) if mask>>k&1]
  for sample in range(20):
   tables={e:[rng.randrange(-3,4) for k in range(4)] for e in edges}
   energy={x:sum(tables[e][2*x[e[0]]+x[e[1]]] for e in edges) for x in states(n)}
   minimum=min(energy.values());S={x for x,v in energy.items() if v==minimum};facial+=1
   uniform={x:int(x in S) for x in energy}
   if mtp(uniform):continue
   facial_lattice+=1
   projections={e:{tuple(x[i] for i in e) for x in S} for e in edges}
   recovered={x for x in energy if all(tuple(x[i] for i in e) in projections[e] for e in edges)}
   assert S==recovered
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_FINITE_CROSS_CHECKS','priority_laws':result,'recoding_controls':controls,'negative_limiting_checks':negative,
 'fraction_capacity_residual_cases':flow_cases,'fraction_capacity_cut_assignments':flow_assignments,
 'sampled_original_edge_facial_energies':facial,'lattice_facial_supports_tested_for_A_feasibility':facial_lattice,
 'limitations':'Finite controls supplement personal adjudication of arbitrary-graph proofs; do not establish novelty, all-graph truth, or historical authorship metadata.'}
(R/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

