"""Fresh checks derived only from the four-page paper before packaged helpers."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import gcd
import json, datetime
R=Path(__file__).resolve().parent
M=[[1,0,1,1,1,0,0],[0,1,1,1,1,0,0],[0,0,1,0,0,1,1],[0,0,0,1,0,1,1],[0,0,0,0,1,1,1],[1,1,0,0,0,1,0],[1,1,0,0,0,0,1]]
b=[F(x,27) for x in (5,5,3,3,3,4,4)];q=[F(x,27) for x in (4,4,3,3,3,5,5)]
def require(p,msg):
 if not p:raise AssertionError(msg)
def validate(A,b,q,theta):
 m=len(A);n=len(A[0]);require(len(b)==m and len(q)==n,'shape')
 require(all(x in (0,1) for row in A for x in row),'binary')
 require(all(x>0 for x in b+q) and sum(b)==sum(q)==1,'positive probability vectors')
 require(len({tuple(A[v][i] for v in range(m)) for i in range(n)})==n,'distinct columns')
 require(all(sum(F(A[v][i])*q[i] for i in range(n))==theta for v in range(m)),'row regularity')
 require(all(sum(F(A[v][i])*b[v] for v in range(m))==theta for i in range(n)),'column regularity')
 return max(map(sum,A))
def lcm(a,b):return a*b//gcd(a,b)
def integer_sizes(w):
 den=1
 for x in w:den=lcm(den,x.denominator)
 z=[int(x*den) for x in w];require(min(z)>0 and sum(z)==den,'blowup positive and normalized');return z

def construct(A,b,q,theta,literal=False):
 d=validate(A,b,q,theta);m=len(A);n=len(A[0]);t=theta/d;delta=1-n*t
 require(delta>=0,'residual')
 av=[t]*n+([delta] if delta else [])
 # Weighted primal LP solution and exact dual certificate. For a max-degree row,
 # average its d constraints p_i >= t and combine with sum_{row}p_i <= theta.
 require(all(sum(av[i] for i in range(n) if A[v][i])<=theta for v in range(m)),'primal LP row constraints')
 v=max(range(m),key=lambda v:sum(A[v]));support=[i for i in range(n) if A[v][i]]
 dual_objective=theta*F(1,d)
 require(sum(F(1,d) for i in support)==1 and dual_objective==t,'exact matching primal/dual LP bound')
 for i,j in product(range(n),repeat=2):
  if i!=j:require(any(A[v][i] and not A[v][j] for v in range(m)),'incomparable support witness')
 out={'theta':str(theta),'rows':m,'columns':n,'degree':d,'t':str(t),'residual':str(delta),'primal_dual_optimum':str(t),'literal_graph_checked':literal}
 if literal:
  aa=integer_sizes(av);bb=integer_sizes(b);cc=integer_sizes(q)
  at=[i for i,size in enumerate(aa) for _ in range(size)]
  bt=[i for i,size in enumerate(bb) for _ in range(size)]
  ct=[i for i,size in enumerate(cc) for _ in range(size)]
  # Literal unweighted adjacency sets, no weighted reachability shortcuts.
  nb_a=[{v for v,typ in enumerate(bt) if i==n or not A[typ][i]} for i in at]
  nb_c=[{v for v,typ in enumerate(bt) if A[typ][i]} for i in ct]
  a_deg=[len(x) for x in nb_a];c_deg=[len(x) for x in nb_c]
  ba_deg=[sum(v in x for x in nb_a) for v in range(len(bt))]
  bc_deg=[sum(v in x for x in nb_c) for v in range(len(bt))]
  require(min(F(x,len(bt)) for x in a_deg)>=1-theta,'A-to-B')
  require(min(F(x,len(at)) for x in ba_deg)>=1-theta,'B-to-A')
  require(min(F(x,len(ct)) for x in bc_deg)>=theta,'B-to-C')
  require(min(F(x,len(bt)) for x in c_deg)>=theta,'C-to-B')
  reach=[sum(bool(ta&tc) for ta in nb_a) for tc in nb_c]
  require(all(F(k,len(at))==1-t for k in reach),'literal reached-vertex fractions')
  out.update({'part_sizes':[len(at),len(bt),len(ct)],'A_type_sizes':aa,'reach_counts':sorted(set(reach)),'minimum_four_degree_fractions':[str(min(F(x,len(bt)) for x in a_deg)),str(min(F(x,len(at)) for x in ba_deg)),str(min(F(x,len(ct)) for x in bc_deg)),str(min(F(x,len(bt)) for x in c_deg))]})
 return out
results=[]
results.append(construct(M,b,q,F(13,27),True));results.append(construct([[1-x for x in row] for row in M],b,q,F(14,27),True))
for den in range(2,11):
 for num in range(1,den):
  if gcd(num,den)==1:
   A=[[int((v-i)%den<num) for i in range(den)] for v in range(den)]
   results.append(construct(A,[F(1,den)]*den,[F(1,den)]*den,F(num,den),True))
# Duplicated rows are allowed and preserve graph/template values.
Ms=[M[0],M[0],*M[1:]];bs=[b[0]/3,2*b[0]/3,*b[1:]]
results.append(construct(Ms,bs,q,F(13,27),True))
# Invalid-domain controls must actually reject.
rejects=[]
for name,A,bb,qq in [
 ('duplicate column',[row+[row[0]] for row in M],b,[q[0]/2,*q[1:],q[0]/2]),
 ('zero row weight',M,[F(0),*b[1:]],q),
 ('incorrect normalization',M,b,[q[0]+F(1,27),*q[1:]])]:
 try:validate(A,bb,qq,F(13,27))
 except AssertionError:rejects.append(name)
 else:raise AssertionError('invalid template accepted: '+name)
gaps=[]
for d,e in product(range(1,5),repeat=2):
 gap=abs(F(13,27*d)-F(14,27*e));require(gap>=F(1,108),'integer gap')
 gaps.append({'d':d,'e':e,'gap':str(gap)})
require(min(F(x['gap']) for x in gaps)==F(1,108),'minimum gap exact')
# Exhaust all labeled adjacent-pair edge sets on (3,3,3) for theta=1/3,2/3.
# Validate the universal lower-bound reduction itself, without assuming unknown d(theta).
exhaust=[]
m=a=c=3
masks=list(range(1<<m))
pairs=list(product(masks,repeat=3))
for theta in [F(1,3),F(2,3)]:
 feasible=0;saturated=0;leftover_examples=0;full=0
 minA=int(3*(1-theta));minC=int(3*theta)
 As=[arr for arr in pairs if min(x.bit_count() for x in arr)>=minA and all(sum((x>>v)&1 for x in arr)>=minA for v in range(m))]
 Cs=[arr for arr in pairs if min(x.bit_count() for x in arr)>=minC and all(sum((x>>v)&1 for x in arr)>=minC for v in range(m))]
 for na,nc in product(As,Cs):
  feasible+=1;rc=[sum(bool(x&y) for x in na) for y in nc];Fmax=F(max(rc),a)
  if Fmax==1:full+=1;continue
  saturated+=1
  require(all(y.bit_count()==minC for y in nc),'lower saturation C degrees')
  require(all(sum((y>>v)&1 for y in nc)==minC for v in range(m)),'lower saturation B degrees')
  types=sorted(set(nc));Aclasses=[sum(x==((1<<m)-1)^y for x in na) for y in types]
  require(min(Aclasses)>0,'each missed class positive')
  leftover=a-sum(Aclasses);require(leftover>=0,'disjoint missed classes');leftover_examples+=int(leftover>0)
  t=F(min(Aclasses),a);degree=max(sum((y>>v)&1 for y in types) for v in range(m))
  require(Fmax==1-t and t*degree<=theta,'lower-bound reduction')
  for v in range(m):require(sum(F(Aclasses[i],a) for i,y in enumerate(types) if (y>>v)&1)<=theta,'row complement constraint')
 exhaust.append({'theta':str(theta),'all_labeled_pair_choices':len(pairs)**2,'biconstrained_graphs':feasible,'F_equals_1':full,'F_below_1':saturated,'F_below_1_with_leftover_A':leftover_examples})
# Explicit leftover-A construction is already present in the seven-type examples.
# Distinct upper bounds alone are not a separation certificate.
require(F(4,5)<=min(F(95,108),F(47,54)),'shared value permitted by both upper bounds')
out={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','mechanism':'Independent exact Fractions, literal adjacency sets, explicit primal/dual LP certificates, exhaustive small graph reduction. No packaged helper imported.','template_cases':results,'invalid_template_controls':rejects,'integer_gap_cases':gaps,'exhaustive_graph_reductions':exhaust,'upper_bound_only_control':'The common hypothetical value 4/5 satisfies both displayed upper bounds, confirming that those inequalities alone cannot prove separation.','limits':'Finite controls corroborate the universal argument; they do not prove it, determine d(13/27) or d(14/27), or determine the ordering.'}
(R/'independent-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','templates':len(results),'gap_cases':len(gaps),'exhaustive':exhaust,'invalid_controls':len(rejects)},indent=2))
