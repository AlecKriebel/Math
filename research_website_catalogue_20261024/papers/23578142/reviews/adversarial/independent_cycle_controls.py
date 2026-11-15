"""Independent integer-prefix / cycle-chain falsifiers; stdlib only.
No deposited code imports, rank-count extrapolation, or source writes.
"""
from itertools import product,combinations
from collections import Counter
from math import prod
import json,sys

def need(ok,label):
 if not ok:raise ValueError(label)
def parts(n,cap=None):
 if n==0:return [()]
 cap=n if cap is None else min(n,cap);out=[]
 for a in range(cap,0,-1):out.extend((a,)+tail for tail in parts(n-a,a))
 return out
def compositions(n,r):
 if r==1:return [(n,)]
 return [(a,)+tail for a in range(n+1) for tail in compositions(n-a,r-1)]
def lower_partition(lam):
 out=[]
 for i,a in enumerate(lam):
  if i==len(lam)-1 or a>lam[i+1]:
   q=list(lam);q[i]-=1;out.append(tuple(x for x in q if x))
 return out
def young_product(r,N):
 labels=[];layers=[]
 for n in range(N+1):
  vals=sorted(x for sizes in compositions(n,r) for x in product(*(parts(k) for k in sizes)));labels.append(vals)
  if n==0:layers.append([frozenset()]);continue
  previous={x:i for i,x in enumerate(labels[-2])};row=[]
  for x in vals:
   pred=set()
   for j,lam in enumerate(x):
    for lower in lower_partition(lam):y=list(x);y[j]=lower;pred.add(previous[tuple(y)])
   row.append(frozenset(pred))
  layers.append(row)
 return layers
def reflection(P,r):
 if len(P)==1:return P+[[frozenset({0}) for _ in range(r)]]
 previous,current=P[-2],P[-1];new=[frozenset(x for x,p in enumerate(current) if z in p) for z in range(len(previous))]
 new.extend(frozenset({x}) for x in range(len(current)) for _ in range(r));return P+[new]
def validate(P,r,start=0):
 need(len(P[0])==1 and not P[0][0],'unique_rank_zero')
 for n,row in enumerate(P):
  if n:need(all(q and all(type(x) is int and 0<=x<len(P[n-1]) for x in q) for q in row),'ordinary_nonempty_predecessor_sets')
 for j in range(start,len(P)-1):
  for x,pred in enumerate(P[j]):
   upper=sum(x in q for q in P[j+1]);need(upper-len(pred)==r,'integer_diagonal_commutator_rank'+str(j))
  for x,y in combinations(range(len(P[j])),2):
   lo=len(P[j][x]&P[j][y]);hi=sum(x in q and y in q for q in P[j+1]);need(lo==hi and hi<=1,'integer_offdiagonal_and_unique_common_covers_rank'+str(j))
 return True
def incidence(P,j):return [('L'+str(x),'R'+str(y)) for y,p in enumerate(P[j]) for x in sorted(p)]
def beta(vertices,edges):
 parent={v:v for v in vertices}
 def root(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for x,y in edges:
  need(x in parent and y in parent,'edge_endpoints_present');a,b=root(x),root(y)
  if a!=b:parent[a]=b
 components=len({root(x) for x in vertices});return len(edges)-len(vertices)+components,components
def graph(P,j):
 vertices=['L'+str(x) for x in range(len(P[j-1]))]+['R'+str(x) for x in range(len(P[j]))];e=incidence(P,j);b,c=beta(vertices,e);need(c==1,'full_consecutive_graph_connected');return b
def boundary(vertices,edges,p):
 index={v:i for i,v in enumerate(vertices)};A=[[0]*len(edges) for _ in vertices]
 for j,(a,b) in enumerate(edges):A[index[a]][j]=-1%p;A[index[b]][j]=1
 return A
def kernel(A,p):
 if not A:return []
 A=[row[:] for row in A];nr=len(A);nc=len(A[0]);r=0;piv=[]
 for c in range(nc):
  q=next((i for i in range(r,nr) if A[i][c]%p),None)
  if q is None:continue
  A[r],A[q]=A[q],A[r];inv=pow(A[r][c],-1,p);A[r]=[x*inv%p for x in A[r]]
  for i in range(nr):
   if i!=r and A[i][c]:v=A[i][c];A[i]=[(x-v*y)%p for x,y in zip(A[i],A[r])]
  piv.append(c);r+=1
  if r==nr:break
 out=[]
 for free in [x for x in range(nc) if x not in piv]:
  v=[0]*nc;v[free]=1
  for i,c in enumerate(piv):v[c]=-A[i][free]%p
  out.append(v)
 return out
def matrix_rank(columns,p):
 if not columns:return 0
 A=[list(r) for r in zip(*columns)];return len(columns)-len(kernel(A,p))
def zero_boundary(A,v,p):return all(sum(x*y for x,y in zip(row,v))%p==0 for row in A)
def is_reflection(P,n,r):
 Z,X=P[n-2:n];wanted=[frozenset(x for x,pr in enumerate(X) if z in pr) for z in range(len(Z))]+[frozenset({x}) for x in range(len(X)) for _ in range(r)];return Counter(P[n])==Counter(wanted)
def check_rank(P,n,r,selector_cap=32):
 Z,X,Y=P[n-2:n+1];S=[z for z in range(len(Z)) if any(pr==frozenset({z}) for pr in X)];choices=[[x for x,pr in enumerate(X) if pr==frozenset({z})] for z in S];hsvertices=[('z',z) for z in S]+[('x',x) for x in range(len(X))];hsedges=[(('z',z),('x',x)) for z in S for x,pr in enumerate(X) if z in pr];q,c=beta(hsvertices,hsedges);previous=graph(P,n-1);bn=graph(P,n);sizes=[len(a) for a in P];edges=sum(len(a) for a in Y);U=1+r*sum(sizes[:n-1])+(r-1)*sizes[n-1];need(edges==r*sum(sizes[:n]) and sizes[n]==U-bn and bn-previous==r*sizes[n-1]+sizes[n-2]-sizes[n],'exact_slack_not_only_bounds');need(0<=q<=previous and bn>=q,'full_supported_bound');need(q==sum(sum(z in pr for pr in X)-1 for z in S)-len(X)+c,'all_isolates_component_formula')
 twowitnesses=len(S)==len(Z) and all(len(v)>=2 for v in choices);equal=sizes[n]==r*sizes[n-1]+sizes[n-2]
 if n>=3 and twowitnesses:need(equal==is_reflection(P,n,r),'two_witness_equality_exact_predecessor_multiset')
 if len(S)==len(Z):need(equal or sizes[n]<r*sizes[n-1]+sizes[n-2],'all_supported_local_bound')
 total=prod(len(v) for v in choices);selections=list(product(*choices)) if total<=selector_cap else [tuple(v[0] for v in choices),tuple(v[-1] for v in choices),tuple(v[i%len(v)] for i,v in enumerate(choices))];checked=0;wrong_sign_detected=False
 targetvertices=[('x',x) for x in range(len(X))]+[('t',t) for t in range(len(Y))];targetedges=[(('x',x),('t',t)) for t,pr in enumerate(Y) for x in sorted(pr)];targetindex={e:i for i,e in enumerate(targetedges)};pair_top={}
 for t,pr in enumerate(Y):
  for a,b in combinations(sorted(pr),2):need((a,b) not in pair_top,'unique_upper_pair');pair_top[a,b]=t
 for witnesses in selections:
  chosen=dict(zip(S,witnesses));internal={};union_internal=set();Kedges=set();common=[]
  for z,a in chosen.items():
   Nz={x for x,pr in enumerate(X) if z in pr};tops={t for t,pr in enumerate(Y) if a in pr and len(pr)>1};need(not(union_internal&tops),'disjoint_witness_internals');union_internal|=tops;internal[z]=tops;Tv=[('x',x) for x in Nz]+[('t',t) for t in tops];Te=[(('x',x),('t',t)) for t in tops for x in sorted(Y[t])];need(all(Y[t]<=Nz for t in tops),'no_external_terminal');need(beta(Tv,Te)==(0,1),'actual_witness_tree');Kedges.update(Te)
   for y in Nz-{a}:
    t=pair_top[tuple(sorted((a,y)))];need(t in tops and all((y in Y[k])==(k==t) for k in tops),'unique_actual_witness_path');common.append((z,a,y,t))
  Kv=[('x',x) for x in range(len(X))]+[('t',t) for t in sorted(union_internal)];need(beta(Kv,list(Kedges))==(q,c),'whole_simultaneous_tree_union_cycle_components');need(Kedges<=set(targetedges),'actual_subgraph_edges');need(Counter((z,a,y) for z,a,y,t in common)==Counter((z,chosen[z],x) for z in S for x,pr in enumerate(X) if z in pr and x!=chosen[z]),'common_forest_contraction_edge_model')
  for p in [2,3]:
   sourceA=boundary(hsvertices,hsedges,p);basis=kernel(sourceA,p);need(len(basis)==q,'independent_boundary_kernel_dimension');targetA=boundary(targetvertices,targetedges,p);images=[]
   for v in basis:
    image=[0]*len(targetedges);wrong=[0]*len(targetedges)
    for coefficient,(zz,xx) in zip(v,hsedges):
     z,x=zz[1],xx[1];a=chosen[z]
     if x==a:need(coefficient==0,'witness_leaf_cycle_coefficient');continue
     t=pair_top[tuple(sorted((a,x)))];i=targetindex[(('x',a),('t',t))];j=targetindex[(('x',x),('t',t))];image[i]=(image[i]+coefficient)%p;image[j]=(image[j]-coefficient)%p;wrong[i]=(wrong[i]+coefficient)%p;wrong[j]=(wrong[j]+coefficient)%p
    need(zero_boundary(targetA,image,p),'actual_cycle_chain_map_boundary_zero');images.append(image)
    if p==3 and not zero_boundary(targetA,wrong,p):wrong_sign_detected=True
   need(matrix_rank(images,p)==q,'actual_cycle_chain_map_injective');checked+=1
 return {'rank':n,'rank_sizes':sizes[:n+1],'supported_centers':len(S),'q':q,'b_previous':previous,'b_next':bn,'residual':previous-q,'singleton_witness_products':total,'selections_checked':len(selections),'all_choices_exhausted':total<=selector_cap,'cycle_field_maps_checked':checked,'two_witness_hypothesis':twowitnesses,'local_equality':equal,'exact_reflection_extension':is_reflection(P,n,r),'wrong_path_sign_detected_in_F3':wrong_sign_detected,'Byrnes':U,'refined':U-q}
def run():
 fixtures=[]
 for r,N in [(1,8),(2,3),(3,3),(4,3)]:fixtures.append(('Young-product-r'+str(r),r,young_product(r,N)))
 for r in [1,3,4]:
  base=young_product(r,5 if r==1 else 2);P=reflection(base,r);P=reflection(P,r) if r==1 else P;fixtures.append(('Young-prefix-then-reflection-r'+str(r),r,P))
 results=[];wrong_sign=False
 for label,r,P in fixtures:
  validate(P,r)
  for n in range(2,len(P)):
   row=check_rank(P,n,r);row['fixture']=label;results.append(row);wrong_sign|=row['wrong_path_sign_detected_in_F3']
 need(wrong_sign,'wrong_signed_cycle_path_is_a_nonvacuous_fault')
 sharp3=next(x for x in results if x['fixture']=='Young-prefix-then-reflection-r3' and x['rank']==3);sharp1=next(x for x in results if x['fixture']=='Young-prefix-then-reflection-r1' and x['rank']==7);need(sharp3['rank_sizes']==[1,3,9,30] and sharp3['q']==1 and sharp3['refined']==30,'independent_r3_attained_positive_correction');need(sharp1['rank_sizes']==[1,1,2,3,5,7,12,19] and sharp1['q']==1 and sharp1['refined']==19,'independent_r1_attained_positive_correction');need(all(s['rank_sizes'][-1]>s['Byrnes']-2*s['q'] for s in [sharp3,sharp1]),'coefficient_two_refuted_by_actual_attained_examples');young6=next(x for x in results if x['fixture']=='Young-product-r1' and x['rank']==6);need((young6['b_previous'],young6['q'],young6['residual'],young6['Byrnes'],young6['refined'],young6['rank_sizes'][-1])==(1,0,1,13,13,11),'strict_residual_not_erased_or_misreported_as_recurrence_failure')
 faults=[]
 def rejects(label,fn):
  try:fn()
  except ValueError as e:faults.append({'fault':label,'rejection':str(e)});return
  raise RuntimeError('bad_prefix_accepted:'+label)
 relaxed=[[frozenset()],[frozenset({0}) for _ in range(3)],[frozenset({0,1}),frozenset({0,2}),frozenset({1,2})],[frozenset({0,1,2})]+[frozenset({x}) for x in range(3) for _ in range(2)]];validate(relaxed,1,start=1);rejects('middle_commutators_do_not_replace_rank_zero',lambda:validate(relaxed,1));P=reflection(young_product(3,2),3);damaged=[row[:] for row in P];damaged[-1]=damaged[-1][:-1];rejects('deleted_top_vertex',lambda:validate(damaged,3));rejects('false_r_parameter',lambda:validate(P,2));bad=[row[:] for row in P];bad[-1]=bad[-1][:];a=next(x for x,pr in enumerate(P[-2]) if pr==frozenset({0}));w=next(x for x,pr in enumerate(P[-2]) if pr==frozenset({1}));t=next(i for i,pr in enumerate(bad[-1]) if a in pr and len(pr)>1);bad[-1][t]=bad[-1][t]|{w};rejects('colliding_internals_force_disjoint_witness_common_upper',lambda:validate(bad,3));need(min(len(pr) for pr in P[1])==1,'false_minimum_incidence_degree_two_is_not_assumed')
 return {'literal_custom_status':'INDEPENDENT_INTEGER_PREFIX_AND_EXPLICIT_CYCLE_CHAIN_DIAGNOSTICS_AGREE','optimization':sys.flags.optimize,'fixtures':len(fixtures),'rank_interfaces':len(results),'cycle_maps_over_F2_F3':sum(r['cycle_field_maps_checked'] for r in results),'positive_q_interfaces':sum(r['q']>0 for r in results),'results':results,'invalid_prefix_faults_rejected':faults,'wrong_signed_path_fault_rejected':True,'coefficient2_refuted_by_both_sharp_examples':True,'unrestricted_local_recurrence_proved_by_samples':False,'all_witness_choice_proof':'INITIAL_RECONSTRUCTION.md families4-6','native_code_import_execution_network_or_writes':False}
if __name__=='__main__':print(json.dumps(run(),indent=2))
