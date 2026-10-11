"""Reviewer 02's independent exact checks; no candidate-program imports.

Inputs are a released expected-data directory. Source tables are mathematical
facts credited to GL Lemma 5.2, KS Example 6.5 and GMS Examples 7 and 8.
Finite checks supplement personal proof review and do not prove an all-graph claim.
"""
import argparse, collections, fractions, itertools, json, math, pathlib, random
Q=fractions.Fraction
def cube(n): return list(itertools.product((0,1),repeat=n))
def mtp(w):
 return all(w[tuple(a&b for a,b in zip(x,y))]*w[tuple(a|b for a,b in zip(x,y))]>=w[x]*w[y] for x in w for y in w)
def projection(x,indices): return tuple(x[i] for i in indices)
def components(n,edges,removed):
 remain=set(range(n))-set(removed); parts=[]
 while remain:
  part={min(remain)}; changed=True
  while changed:
   changed=False
   for a,b in edges:
    if a in part and b in remain and b not in part: part.add(b);changed=True
    if b in part and a in remain and a not in part: part.add(a);changed=True
  remain-=part;parts.append(part)
 return parts
def check_law(record):
 n=record['n']; edges=[tuple(i-1 for i in e) for e in record['edges']]
 w={tuple(map(int,x)):v for x,v in record['integer_weights'].items()};states=cube(n)
 assert set(w)==set(states) and all(type(a) is int and a>=0 for a in w.values())
 assert sum(w.values())==record['normalizer']>0 and mtp(w)
 assert record['support_closed_meet_join'] and record['mtp2_failure_count']==record['global_markov_failure_count']==0
 assert record['mtp2_ordered_pairs']==4**n
 assert all(record[k]==[] for k in ['lattice_failures','first_mtp2_failures','first_global_markov_failures'])
 separations=[];evaluations=0;rank_cells=0
 for label in itertools.product(range(4),repeat=n):
  A=tuple(i for i,a in enumerate(label) if a==0);B=tuple(i for i,a in enumerate(label) if a==1);C=tuple(i for i,a in enumerate(label) if a==2)
  if not A or not B or any(p.intersection(A) and p.intersection(B) for p in components(n,edges,C)): continue
  separations.append({'A':[i+1 for i in A],'B':[i+1 for i in B],'C':[i+1 for i in C]})
  for c in cube(len(C)):
   table=collections.Counter()
   for x in states:
    if projection(x,C)==c:table[projection(x,A),projection(x,B)]+=w[x]
   rows=collections.Counter();cols=collections.Counter();total=sum(table.values())
   for (a,b),v in table.items():rows[a]+=v;cols[b]+=v
   for a in cube(len(A)):
    for b in cube(len(B)):
     assert table[a,b]*total==rows[a]*cols[b];rank_cells+=1
   evaluations+=math.comb(2**len(A),2)*math.comb(2**len(B),2)
 assert separations==record['all_separations']
 assert len(separations)==record['ordered_nontrivial_separations']
 assert evaluations==record['ordered_conditioning_2x2_minor_evaluations']
 assert evaluations//2==record['distinct_structural_minor_labels_up_to_A_B_transpose']
 inv=record['invariant'];L=[tuple(x) for x in inv['left_states']];R=[tuple(x) for x in inv['right_states']]
 for e,balance in zip(edges,inv['edge_balances']):
  lc=collections.Counter(''.join(map(str,projection(x,e))) for x in L);rc=collections.Counter(''.join(map(str,projection(x,e))) for x in R)
  assert lc==rc and balance['equal'] and dict(lc)==balance['left'] and dict(rc)==balance['right'] and balance['edge']==[i+1 for i in e]
 products=[math.prod(w[x] for x in side) for side in [L,R]]
 assert products==inv['integer_products'] and products[0]!=products[1]
 normalized=[Q(p,sum(w.values())**len(side)) for p,side in zip(products,[L,R])]
 assert [str(a) for a in normalized]==inv['normalized_products'] and str(normalized[0]-normalized[1])==inv['normalized_difference']
 return {'rank_one_table_cells_checked':rank_cells,'ordered_separations':len(separations),'minor_evaluation_count':evaluations,'structural_count':evaluations//2,'exact_products':products}
def solve(matrix,values):
 a=[[Q(x) for x in row]+[Q(v)] for row,v in zip(matrix,values)];n=len(matrix[0]);r=0;pivots=[]
 for col in range(n):
  k=next((k for k in range(r,len(a)) if a[k][col]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];d=a[r][col];a[r]=[x/d for x in a[r]]
  for k in range(len(a)):
   if k!=r and a[k][col]:
    d=a[k][col];a[k]=[u-d*v for u,v in zip(a[k],a[r])]
  pivots.append(col);r+=1
 assert all(any(row[:-1]) or row[-1]==0 for row in a)
 solution=[Q(0)]*n
 for k,col in enumerate(pivots):solution[col]=a[k][-1]
 assert all(sum(Q(u)*v for u,v in zip(row,solution))==value for row,value in zip(matrix,values))
 return solution
def density_by_interpolation(n,edges,w,logvalues):
 states=cube(n);S=[x for x in states if w[x]>0];assert S and mtp(w)
 projections={e:{projection(x,e) for x in S} for e in edges};unary=[{x[i] for x in S} for i in range(n)]
 assert {x for x in states if all(x[i] in unary[i] for i in range(n)) and all(projection(x,e) in projections[e] for e in edges)}==set(S)
 pins={i:next(iter(a)) for i,a in enumerate(unary) if len(a)==1};active=[i for i in range(n) if i not in pins]
 groups=collections.defaultdict(list)
 for i in active:groups[tuple(x[i] for x in S)].append(i)
 classes=sorted(groups.values(),key=lambda a:a[0]);reps=[a[0] for a in classes]
 forces={(a,b) for a in active for b in active if all(x[a]<=x[b] for x in S)}
 pairs=[(k,l) for k in range(len(classes)) for l in range(k+1,len(classes)) if (reps[k],reps[l]) not in forces and (reps[l],reps[k]) not in forces and any(a in classes[k] and b in classes[l] or b in classes[k] and a in classes[l] for a,b in edges)]
 matrix=[[1]+[x[i] for i in reps]+[x[reps[k]]*x[reps[l]] for k,l in pairs] for x in S]
 coeff=solve(matrix,[logvalues[x] for x in S]);B=coeff[1+len(reps):];assert all(b>=0 for b in B)
 chosen=[next(e for e in edges if e[0] in classes[k] and e[1] in classes[l] or e[1] in classes[k] and e[0] in classes[l]) for k,l in pairs]
 def L(x):return coeff[0]+sum(h*x[i] for h,i in zip(coeff[1:1+len(reps)],reps))+sum(b*x[a]*x[c] for b,(a,c) in zip(B,chosen))
 arcs=[(a,b) for a,b in itertools.permutations(active,2) if tuple(sorted((a,b))) in {tuple(sorted(e)) for e in edges} and (a,b) in forces]
 def D(x):return sum(x[i]!=a for i,a in pins.items())+sum(x[a]*(1-x[b]) for a,b in arcs)
 assert {x for x in states if D(x)==0}==set(S)
 assert all(L(x)==logvalues[x] for x in S)
 target={x:Q(w[x],sum(w.values())) for x in states};errors=[]
 for penalty in [0,4,8,16]:
  weights={}
  for x in states:
   power=L(x)-penalty*D(x);assert power.denominator==1
   k=int(power);weights[x]=Q(2**k) if k>=0 else Q(1,2**(-k))
  assert mtp(weights);Z=sum(weights.values());errors.append(sum(abs(weights[x]/Z-target[x]) for x in states))
 assert all(a>=b for a,b in zip(errors,errors[1:]))
 return {'support_size':len(S),'classes':classes,'aggregate_couplings':{str(k):int(b) if b.denominator==1 else str(b) for k,b in zip(pairs,B)},'l1_errors_exact':[str(a) for a in errors]}
def powtwo(k):return Q(2**k) if k>=0 else Q(1,2**(-k))
def boundary_independent(expected):
 examples=[(3,[(0,1),(0,2),(1,2)],{},[(0,1),(1,0)],[-2,1,0],[0,-3,5]),(4,[(0,1),(1,2),(2,3)],{0:1},[(1,2)],[-1,2,0,-2],[-4,-7,3]),(5,[(0,1),(1,2),(0,3)],{3:1},[(0,1),(1,0),(2,1)],[1,-2,3,0,0],[-5,-4,2]),(1,[],{0:0},[],[3],[]),(0,[],{},[],[],[])]
 rows=[]
 for n,edges,pins,arcs,h,j in examples:
  logs={x:sum(x[i]*h[i] for i in range(n))+sum(q*x[a]*x[b] for (a,b),q in zip(edges,j)) for x in cube(n)}
  w={x:powtwo(logs[x]) if all(x[i]==a for i,a in pins.items()) and all(x[a]<=x[b] for a,b in arcs) else Q(0) for x in cube(n)}
  rows.append(density_by_interpolation(n,edges,w,logs))
 assert rows==expected['density_examples']
 graphs=sum(2**math.comb(n,2) for n in range(5));assignments=5*sum(2**math.comb(n,2)*2**n for n in range(5))
 assert graphs==76 and expected['networks']==graphs*5==380 and expected['cut_assignments_checked']==assignments==5495
 psi=[1,1,1,0];pinned={(a,b):Q((1-a)*psi[2*a+b],2) for a,b in cube(2)}
 smoothed={(a,b):(1 if a==0 else Q(1,10))*(psi[2*a+b] or Q(1,10)) for a,b in cube(2)}
 assert mtp(pinned) and psi[0]*psi[3]-psi[1]*psi[2]==-1 and not mtp(smoothed)
 assert expected['invalid_given_potential_and_naive_smoothing_shortcuts_falsified']
 return {'graphs':graphs,'networks':graphs*5,'cut_assignments':assignments,'density_examples_exactly_equal':True}
def rational_gauges():
 rng=random.Random(291711);networks=assignments=0
 for n in range(7):
  for sample in range(24):
   pairs=list(itertools.combinations(range(n),2));edges=[e if rng.randrange(2) else e[::-1] for e in pairs if rng.randrange(3)]
   h=[Q(rng.randrange(-40,41),rng.choice([1,3,7])) for _ in range(n)];j=[Q(rng.randrange(0,80),rng.choice([1,3,7])) for _ in edges]
   size=n+2;s=n;t=n+1;c=[[Q(0) for _ in range(size)] for _ in range(size)];b=[-a for a in h]
   for (a,d),q in zip(edges,j):c[a][d]+=q;b[a]-=q
   for a,q in enumerate(b):
    if q>=0:c[a][t]+=q
    else:c[s][a]-=q
   r=[a[:] for a in c];value=Q(0)
   def dfs(u,seen,path):
    if u==t:return path
    for v in range(size-1,-1,-1):
     if v not in seen and r[u][v]>0:
      ans=dfs(v,seen|{v},path+[(u,v)])
      if ans is not None:return ans
    return None
   while (path:=dfs(s,{s},[])) is not None:
    d=min(r[a][b] for a,b in path)
    for a,b in path:r[a][b]-=d;r[b][a]+=d
    value+=d
   energy={x:-sum(a*b for a,b in zip(h,x))-sum(q*x[a]*x[b] for (a,b),q in zip(edges,j)) for x in cube(n)};minimum=min(energy.values());cuts=[]
   for x,e in energy.items():
    U={s}|{i for i,v in enumerate(x) if v};cut=sum(c[a][b] for a in U for b in range(size) if b not in U);res=sum(r[a][b] for a in U for b in range(size) if b not in U)
    assert res==cut-value==e-minimum and res>=0;cuts.append(cut);assignments+=1
   assert min(cuts)==value
   undirected={frozenset(e) for e in edges}
   assert all(r[a][b]>=0 and (not r[a][b] or a>=n or b>=n or frozenset((a,b)) in undirected) for a in range(size) for b in range(size))
   networks+=1
 return {'networks':networks,'assignments':assignments,'vertices':'0 through 6','capacities':'exact rationals, variable orientation, DFS augmentations','all_residual_cut_energy_identities_passed':True}
def random_factors():
 rng=random.Random(801613);accepted=empty=nonmtp=0
 for n in range(5):
  pairs=list(itertools.combinations(range(n),2))
  for sample in range(180):
   edges=[e for e in pairs if rng.randrange(2)];unary=[[rng.choice([0,1,2,4]) for _ in range(2)] for _ in range(n)];edge=[[rng.choice([0,1,2,4]) for _ in range(4)] for _ in edges]
   w={x:math.prod(unary[i][x[i]] for i in range(n))*math.prod(a[2*x[u]+x[v]] for (u,v),a in zip(edges,edge)) for x in cube(n)}
   if not sum(w.values()):empty+=1;continue
   if not mtp(w):nonmtp+=1;continue
   logs={x:v.bit_length()-1 for x,v in w.items() if v};density_by_interpolation(n,edges,w,logs);accepted+=1
 return {'attempted':900,'accepted_MTP2_nonempty':accepted,'empty_rejected':empty,'nonMTP2_rejected':nonmtp,'entries':'0,1,2,4','scope':'Deterministic finite samples, not exhaustive over local potentials.'}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--expected',type=pathlib.Path,required=True);parser.add_argument('--output',type=pathlib.Path,required=True);args=parser.parse_args()
 expected=json.loads((args.expected/'priority_laws.json').read_text());boundary=json.loads((args.expected/'boundary.json').read_text())
 laws=expected['laws'];expected_weights={}
 for label,record in laws.items():
  n=record['n']
  if label=='gandolfi_lenarda_lemma5_2':w={x:(2 if all(x) else 1) if x[2]==x[3] else 0 for x in cube(n)}
  elif label=='kahle_sullivant_example6_5':w={x:(7 if not any(x) else 1) if x[0]==x[1] else 0 for x in cube(n)}
  elif label=='released_candidate_C4':w={x:(2 if all(x) else 1) if x[0]==x[1] else 0 for x in cube(n)}
  else:assert label=='released_candidate_C6';w={x:(2 if all(x) else 1) if all(x[i]==x[i+1] for i in [0,2,4]) else 0 for x in cube(n)}
  assert w=={tuple(map(int,x)):v for x,v in record['integer_weights'].items()};expected_weights[label]=w
 checks={label:check_law(record) for label,record in laws.items()}
 gl=expected_weights['gandolfi_lenarda_lemma5_2'];c4=expected_weights['released_candidate_C4'];c6=expected_weights['released_candidate_C6']
 assert all(gl[x]==c4[(x[2],x[3],x[0],x[1])] for x in gl)
 assert all(c4[(a,a,b,c)]==c6[(a,a,b,b,c,c)]==gl[(b,c,a,a)] for a,b,c in cube(3))
 assert expected['gandolfi_to_candidate_rotation']['verified_all16_states'] and expected['gandolfi_to_candidate_rotation']['graph_edges_preserved'] and expected['C6_core_lift_verified_all8_core_states']
 recoding={}
 for name,supp in [('gms_example7',['0000','0001','1000','0011','1100','0111','1110','1111']),('gms_example8',['0100','0111','1001','1010'])]:
  support={int(x,2) for x in supp};counts={}
  for flip in range(16):
   moved={x^flip for x in support};counts[format(flip,'04b')]=sum(((a&b) not in moved or (a|b) not in moved) for a in moved for b in moved)
  assert counts==expected['recoding_controls'][name]['all_16_coordinate_flips_mtp2_failure_counts'] and all(counts.values()) and not expected['recoding_controls'][name]['some_orientation_mtp2'];recoding[name]=counts
 results={'status':'PASS_INDEPENDENT_EXACT_FINITE_CHECKS','laws':checks,'boundary':boundary_independent(boundary),'rational_gauges':rational_gauges(),'random_local_factors':random_factors(),'recoding_counts':recoding,'limitations':'No all-graph theorem or historical-priority certificate is inferred from these finite checks. Historical authorship/provenance prose is not mechanically authenticated by this program.'}
 assert not args.output.exists();args.output.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n');print(json.dumps(results,indent=2,sort_keys=True))
if __name__=='__main__':main()
