from fractions import Fraction as Q
from pathlib import Path
import json,random,math,datetime
# Independent exact augmenting-path implementation, not candidate code.
def maxflow(D):
 k=len(D); n=2*k+2; s=2*k; t=s+1; cap=[[Q(0) for _ in range(n)] for _ in range(n)]
 for i in range(k):
  cap[s][i]=2*k; cap[k+i][t]=2*k
  for j in range(k): cap[i][k+j]=D[i][j]
 res=[r[:] for r in cap]; flow=Q(0)
 while True:
  parent={s:None}; queue=[s]
  for u in queue:
   for v in range(n):
    if v not in parent and res[u][v]>0: parent[v]=u;queue.append(v)
  if t not in parent:break
  v=t; amount=None
  while parent[v] is not None:
   u=parent[v];amount=res[u][v] if amount is None else min(amount,res[u][v]);v=u
  v=t
  while parent[v] is not None:
   u=parent[v];res[u][v]-=amount;res[v][u]+=amount;v=u
  flow+=amount
 return flow,[[cap[i][k+j]-res[i][k+j] for j in range(k)] for i in range(k)]
def cuts(X,t):
 k=len(X); out=[]
 for A in range(1<<k):
  for B in range(1<<k):
   a=bin(A).count('1'); b=bin(B).count('1'); slope=sum((X[i][j] for i in range(k) for j in range(k) if A>>i&1 and not(B>>j&1)),Q(0)); intercept=Q(2*k*(k-a+b)+a*(k-b));out.append((intercept+(t-1)*slope,slope))
 value=min(x[0] for x in out); slope=min(x[1] for x in out if x[0]==value);return value,slope,out
rng=random.Random(397003); cases=0; edges=0; slopechecks=0
for k in [2,4]:
 for trial in range(70):
  X=[[Q(rng.randint(1,80),rng.randint(1,12)) for j in range(k)] for i in range(k)]; t=Q(rng.randint(10,80),10); D=[[1+(t-1)*x for x in row] for row in X]
  flow,y=maxflow(D); expected,slope,lines=cuts(X,t); assert flow==expected
  # Choose a right increment smaller than all nonactive crossing distances.
  distances=[(v-flow)/(slope-w) for v,w in lines if v>flow and w<slope]; h=min([Q(1,97)]+[v/2 for v in distances]); assert cuts(X,t+h)[0]==flow+h*slope; slopechecks+=1
  rows=[sum(r) for r in y]; cols=[sum(y[i][j] for i in range(k)) for j in range(k)]
  # Every physical edge groups a complete dyadic block of terminal loads.
  for loads in [rows,cols]:
   for size in [2**h for h in range(int(math.log2(k))+1)]:
    for a in range(0,k,size):
     load=sum(loads[a:a+size]); assert load<=2*k*size
     if flow==2*k*k: assert load==2*k*size
     if all(sum(D[i])<2*k for i in range(k)) and all(sum(D[i][j] for i in range(k))<2*k for j in range(k)): assert load<2*k*size
     edges+=1
  cases+=1
# Exact mixed Hall obstruction with strictly positive slopes, k=4.
D=[[Q(11,10) if i<3 and j<2 else Q(10) for j in range(4)] for i in range(4)]; assert min(map(sum,D))>8 and min(sum(D[i][j] for i in range(4)) for j in range(4))>8
v,_=maxflow(D); assert v==Q(153,5)<32
# At a kink, the right derivative is the smaller active slope.
v,slope,_=cuts([[Q(1)]*4 for _ in range(4)],Q(2)); assert v==32 and slope==0
# Exhaustively challenge cut area/count inequalities independently by integer arithmetic.
pairs=0;counts=0
for k in range(2,301):
 for a in range(1,k+1):
  for d in range(max(1,k-a+1),k+1):
   q=min(a,d);ell=k-max(a,d);assert 0<=ell<q;assert a*d-k*(a+d-k)==(k-a)*(k-d);assert a*d==q*(k-ell)
   if q<=k//2: assert 2*a*d>=q*k
   else: assert 4*a*d>k*k
   pairs+=1
 if k<=40:
  for q in range(1,k//2+1):
   exact=sum((1 if q==k-ell else 2)*math.comb(k,q)*math.comb(k,ell) for ell in range(q)); assert exact<=2*q*k**(2*q);counts+=1
first=next(2**h for h in range(1,30) if 8*math.sqrt(math.log(2**h)/(2**h))<1); assert first==512
rates=0
for i in range(1,10000):
 delta=i/10000; Iplus=1/(1-delta)-1+math.log(1-delta);Iminus=1/(1+delta)-1+math.log(1+delta); assert Iplus+1e-15>=delta**2/2 and Iminus+1e-15>=delta**2/8;rates+=1
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_assertions_passed':True,'rational_flow_cut_instances':cases,'physical_edges_checked':edges,'exact_right_slope_checks':slopechecks,'positive_cut_size_pairs':pairs,'small_class_exact_counts':counts,'rate_grid_points':rates,'first_admissible_binary_k':first,'terminal_only_shortcut_counterexample':{'k':4,'full_capacity':32,'exact_flow':str(v) if False else '153/5','all_offered_terminal_totals_exceed_capacity':True},'critical_tie_right_slope':0,'scope':'Supplementary finite independent falsification; analytic proof remains required.'}
Path(__file__).with_name('INDEPENDENT_MATH_CONTROLS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
