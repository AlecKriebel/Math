"""Independent finite diagnostics. No supplied verification code is imported or run."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from collections import deque,Counter
import json,datetime
E=Path(__file__).resolve().parent

def check(v,tag):
 if not v:raise RuntimeError(tag)
def states(n):return list(range(1<<n))
def bit(x,i):return (x>>i)&1
def lattice(S):return all((x&y) in S and (x|y) in S for x in S for y in S)
def mtp_log(Q,S):return all(Q[x&y]+Q[x|y]>=Q[x]+Q[y] for x in S for y in S)
def mtp(W):return all(W[x&y]*W[x|y]>=W[x]*W[y] for x in range(len(W)) for y in range(len(W)))
def two(k):return F(2)**k
struct={'lattices_by_n':{},'graph_support_pairs':0,'finite_local_support_pairs':0,'class_connectivity_checks':0};density={'sampled_quadratics':0,'aggregate_sign_equivalences':0,'MTP2_sampled_laws':0,'penalized_laws':0,'all_cell_comparisons':0}
for n in range(5):
 O=states(n);edges=list(combinations(range(n),2));supports=[]
 for mask in range(1,1<<len(O)):
  S={x for x in O if (mask>>x)&1}
  if lattice(S):supports.append(S)
 struct['lattices_by_n'][str(n)]=len(supports)
 for gm in range(1<<len(edges)):
  G=[e for k,e in enumerate(edges) if (gm>>k)&1]
  for S in supports:
   struct['graph_support_pairs']+=1;unary=[{bit(x,i) for x in S} for i in range(n)];proj={e:{(bit(x,e[0]),bit(x,e[1])) for x in S} for e in G}
   R={x for x in O if all(bit(x,i) in unary[i] for i in range(n)) and all((bit(x,i),bit(x,j)) in proj[i,j] for i,j in G)}
   if R!=S:continue
   struct['finite_local_support_pairs']+=1;pins={i:next(iter(v)) for i,v in enumerate(unary) if len(v)==1};active=[i for i in range(n) if i not in pins]
   rules=[]
   for i,j in G:
    if i not in active or j not in active:continue
    if (1,0) not in proj[i,j]:rules.append((i,j))
    if (0,1) not in proj[i,j]:rules.append((j,i))
   D=lambda x:sum(bit(x,i)!=v for i,v in pins.items())+sum(bit(x,i)*(1-bit(x,j)) for i,j in rules)
   check({x for x in O if D(x)==0}==S,'original_edge_implication_support')
   reach={(i,j):(i==j or (i,j) in rules) for i in active for j in active}
   for k in active:
    for i in active:
     for j in active:reach[i,j]|=reach[i,k] and reach[k,j]
   classes=[];which={}
   for i in active:
    if i in which:continue
    C=[j for j in active if reach[i,j] and reach[j,i]];k=len(classes);classes.append(C)
    for j in C:which[j]=k
    seen={i}
    while True:
     newer=seen|{v for u,v in G if u in seen and v in C}|{u for u,v in G if v in seen and u in C}
     if newer==seen:break
     seen=newer
    check(seen==set(C),'original_graph_connected_tie_class');struct['class_connectivity_checks']+=1
   if n>3:continue
   h=[(i+1)*(-1 if (i+gm)%2 else 1) for i in range(n)];J={e:((k+sum(S)+gm)%5)-2 for k,e in enumerate(G)};Q={x:sum(h[i]*bit(x,i) for i in range(n))+sum(j*bit(x,i)*bit(x,k) for (i,k),j in J.items()) for x in O};H=[0]*len(classes);B={};constant=sum(h[i]*v for i,v in pins.items())
   for i in active:H[which[i]]+=h[i]
   for (i,j),w in J.items():
    if i in pins and j in pins:constant+=w*pins[i]*pins[j]
    elif i in pins:H[which[j]]+=w*pins[i]
    elif j in pins:H[which[i]]+=w*pins[j]
    elif which[i]==which[j]:H[which[i]]+=w
    else:
     K,L=which[i],which[j]
     if reach[i,j]:H[K]+=w
     elif reach[j,i]:H[L]+=w
     else:key=tuple(sorted((K,L)));B[key]=B.get(key,0)+w
   sign=all(w>=0 for w in B.values());good=mtp_log(Q,S);check(sign==good,'aggregate_incomparable_sign_iff_MTP2');density['sampled_quadratics']+=1;density['aggregate_sign_equivalences']+=1
   if not good:continue
   density['MTP2_sampled_laws']+=1;lift={}
   for (K,L),w in B.items():
    es=[(i,j) for i,j in G if {which.get(i),which.get(j)}=={K,L}];check(bool(es),'lift_requires_original_joining_edge');lift[es[0]]=w
   LQ=lambda x:sum(H[k]*bit(x,C[0]) for k,C in enumerate(classes))+sum(w*bit(x,i)*bit(x,j) for (i,j),w in lift.items())
   check(all(LQ(x)+constant==Q[x] for x in S),'lifted_log_on_every_support_cell');density['all_cell_comparisons']+=len(S)
   original=[two(Q[x]) if x in S else F(0) for x in O];Z=sum(original);original=[w/Z for w in original];errors=[]
   for t in [1,3,8]:
    W=[two(LQ(x)-t*D(x)) for x in O];Zt=sum(W);p=[w/Zt for w in W];check(mtp(p),'positive_penalty_law_MTP2');errors.append(sum(abs(p[x]-original[x]) for x in O));density['penalized_laws']+=1
   check(errors[0]>=errors[1]>=errors[2],'monotone_finite_penalty_L1_error')

def maxflow(c):
 N=len(c);r=[row[:] for row in c];v=F(0)
 while True:
  prev={0:None};q=deque([0])
  while q and N-1 not in prev:
   u=q.popleft()
   for w in range(N):
    if w not in prev and r[u][w]>0:prev[w]=u;q.append(w)
  if N-1 not in prev:return v,r
  x=N-1;d=None
  while prev[x] is not None:u=prev[x];d=r[u][x] if d is None else min(d,r[u][x]);x=u
  x=N-1
  while prev[x] is not None:u=prev[x];r[u][x]-=d;r[x][u]+=d;x=u
  v+=d
flow={'networks':0,'all_cut_identities':0,'rational_capacity_networks':0,'base2_normalizers_checked':0}
for n in range(5):
 O=states(n);edges=list(combinations(range(n),2))
 for gm in range(1<<len(edges)):
  G=[e for k,e in enumerate(edges) if (gm>>k)&1]
  for seed in range(4):
   h=[F(((i+seed*2+gm)%9)-4,3 if seed==3 else 1) for i in range(n)];J={e:F((k+seed+gm)%5,3 if seed==3 else 1) for k,e in enumerate(G)};b=[-v for v in h];N=n+2;c=[[F(0) for j in range(N)] for i in range(N)]
   for (i,j),w in J.items():c[i+1][j+1]+=w;b[i]-=w
   for i,w in enumerate(b):
    if w>=0:c[i+1][-1]+=w
    else:c[0][i+1]+=-w
   energy={x:-sum(h[i]*bit(x,i) for i in range(n))-sum(w*bit(x,i)*bit(x,j) for (i,j),w in J.items()) for x in O};mn=min(energy.values());v,r=maxflow(c);res=[]
   for x in O:
    U={0}|{i+1 for i in range(n) if bit(x,i)};C=sum(c[u][w] for u in U for w in range(N) if w not in U);R=sum(r[u][w] for u in U for w in range(N) if w not in U);check(R==C-v==energy[x]-mn,'every_cut_residual_energy_identity');check(R>=0,'residual_nonnegative');res.append(R);flow['all_cut_identities']+=1
   check(min(res)==0,'nonvanishing_weight_at_actual_minimum')
   if seed<3:Z=sum(two(-int(x)) for x in res);check(1<=Z<=1<<n,'exact_normalizer_bound');flow['base2_normalizers_checked']+=1
   else:flow['rational_capacity_networks']+=1
   flow['networks']+=1
# Falsify the tempting original-potential-attractiveness and smoothing shortcuts.
n=3;O=states(n);S={x for x in O if bit(x,0)==bit(x,1)};W=[two(-bit(x,0)*bit(x,2)+2*bit(x,1)*bit(x,2)) if x in S else F(0) for x in O];check(mtp(W),'tied_aggregate_example_MTP2')
eps=F(1,10);smooth=[(F(1) if bit(x,0)==bit(x,1) else eps)*two(-bit(x,0)*bit(x,2)+2*bit(x,1)*bit(x,2)) for x in O];badpairs=[(x,y) for x in O for y in O if smooth[x&y]*smooth[x|y]<smooth[x]*smooth[y]];check(bool(badpairs),'naive_zero_factor_smoothing_must_fail')
# A wrong gauge omitting reverse flow must fail for a path with an entering cut flow.
c=[[F(0)]*4 for _ in range(4)];c[0][1]=3;c[1][2]=2;c[2][3]=3;v,r=maxflow(c);f=[[max(F(0),c[i][j]-r[i][j]) for j in range(4)] for i in range(4)];U={0,2};wrong=sum(c[u][w]-f[u][w] for u in U for w in range(4) if w not in U);correct=sum(c[u][w] for u in U for w in range(4) if w not in U)-v;check(wrong!=correct,'omit_reverse_flow_control')
collapse=[{'t':t,'naive_normalizer':str(F(4)*two(-t))} for t in [1,4,12]];check(F(collapse[-1]['naive_normalizer'])<F(collapse[0]['naive_normalizer']),'naive_bounded_factor_normalizer_collapse')
# Exact existing C4 law; all global separations, including marginal leftovers.
G=[(0,1),(1,2),(2,3),(0,3)];O=states(4);p={x:(F(2,9) if x==15 else F(1,9)) if bit(x,2)==bit(x,3) else F(0) for x in O};check(sum(p.values())==1 and mtp([p[x] for x in O]),'C4_MTP2_and_normalization');seps=0;minors=0
for lab in product(range(4),repeat=4):
 A={i for i in range(4) if lab[i]==1};B={i for i in range(4) if lab[i]==2};C={i for i in range(4) if lab[i]==3}
 if not A or not B:continue
 seen=set(A)
 while True:
  newer=seen|{j for i,j in G if i in seen and j not in C}|{i for i,j in G if j in seen and i not in C}
  if newer==seen:break
  seen=newer
 if seen&B:continue
 seps+=1;AA=sorted(A);BB=sorted(B);CC=sorted(C);key=lambda x,idx:tuple(bit(x,i) for i in idx);table={}
 for x in O:k=(key(x,AA),key(x,BB),key(x,CC));table[k]=table.get(k,F(0))+p[x]
 for z in product([0,1],repeat=len(C)):
  for a,a2 in combinations(list(product([0,1],repeat=len(A))),2):
   for b,b2 in combinations(list(product([0,1],repeat=len(B))),2):check(table[a,b,z]*table[a2,b2,z]==table[a,b2,z]*table[a2,b,z],'all_global_conditioning_minor');minors+=1
# Paper's bit-string subscripts are converted to the integer-coordinate convention.
def idx(s):return sum(int(v)<<i for i,v in enumerate(s))
left=list(map(idx,['0000','0111','1011','1100']));right=list(map(idx,['0011','0100','1000','1111']))
for i,j in G:check(Counter((bit(x,i),bit(x,j)) for x in left)==Counter((bit(x,i),bit(x,j)) for x in right),'quartic_original_edge_multiplicities')
prod=lambda xs:__import__('functools').reduce(lambda a,x:a*p[x],xs,F(1));check(prod(left)!=prod(right),'C4_finite_factor_binomial_violated')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','independently_authored_no_supplied_program_import_or_execution':True,'finite_limits_not_universal_proof':True,'support_diagnostics':struct,'density_diagnostics':density,'residual_flow_diagnostics':flow,'failure_controls':{'tied_example_raw_negative_pair_exponent':-1,'aggregate_pair_exponent':1,'naive_smoothing_violating_pairs':badpairs,'reverse_flow_omission_wrong':str(wrong),'reverse_flow_correct':str(correct),'naive_bounded_factor_collapse':collapse},'C4_exact':{'MTP2_pairs':256,'ordered_global_separations':seps,'conditioning_minors':minors,'left_product':str(prod(left)),'right_product':str(prod(right)),'edge_cell_balances':len(G)}}
(E/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,indent=2))
