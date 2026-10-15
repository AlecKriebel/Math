"""Independent exact finite-model controls; no author module imported.
Usage: python independent_check.py [attempt_directory]
Default: parent of this file's published independent_review directory.
Only the saved declarative two-date formula is read from the author packet.
"""
from fractions import Fraction as F
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import ast,copy,json,sys
import sympy as S
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1

def bary_support(points,target):
 # Independent support enumeration rather than the author's nullspace pruning.
 d=len(target);A=S.Matrix([[1]*len(points)]+[[p[j] for p in points] for j in range(d)])
 rhs=S.Matrix([1]+target)
 for size in range(1,d+2):
  for inds in combinations(range(len(points)),size):
   B=A[:,list(inds)]
   if B.rank()!=size:continue
   try:sol,par=B.gauss_jordan_solve(rhs)
   except ValueError:continue
   if par.rows or any(w<=0 for w in sol):continue
   ck(B*sol==rhs,'independent_convex_support_identity')
   return list(inds),[F(w) for w in sol]
 raise AssertionError('Caratheodory support absent')
def payoff(r,t):return max(F(0),r-[F(1),F(11,10)][t-1])
def make(t,code):
 # Every shadow history is identically one, while reference paths vary.
 d={'z':F(1),'t':t,'children':[]}
 if t:d['r']=F(3,5)+F((code*7)%9,10)
 if t<2:
  raw=[F(j+1+(code%3)) for j in range(5)];total=sum(raw)
  d['children']=[(w/total,make(t+1,5*code+j+1)) for j,w in enumerate(raw)]
 return d
def enrich(d,hist):
 if d['t']:hist=hist+[payoff(d['r'],d['t'])]
 if not d['children']:d['V']=hist
 else:
  for _,ch in d['children']:enrich(ch,hist)
  d['V']=[sum(w*ch['V'][j] for w,ch in d['children']) for j in range(2)]
def reduce(d):
 o={k:copy.deepcopy(v) for k,v in d.items() if k!='children'}
 if not d['children']:o['children']=[];return o
 reduced=[(w,reduce(ch)) for w,ch in d['children']]
 points=[[ch['z']]+ch['V'] for _,ch in reduced]
 ids,weights=bary_support(points,[d['z']]+d['V'])
 o['children']=[(w,reduced[i][1]) for i,w in zip(ids,weights)]
 return o
def pad(d,b=4):
 d=copy.deepcopy(d)
 if not d['children']:return d
 old=d['children'];first_mult=b-len(old)+1;new=[]
 for j,(w,ch) in enumerate(old):
  mult=first_mult if j==0 else 1
  for _ in range(mult):new.append((w/mult,pad(ch,b)))
 d['children']=new;return d
def audit(d,hist,full=False):
 if d['t']:
  ck(d['r']>=F(1,2) and d['r']>0 and d['z']>0 and abs(d['r']-d['z'])<=F(1,2),'adapted_auxiliary_domain')
  hist=hist+[payoff(d['r'],d['t'])]
 if not d['children']:
  ck(d['V']==hist,'leaf_history_payoffs')
  return d['V'],1
 ck(len(d['children'])==4 if full else len(d['children'])<=4,'conditional_support_bound')
 ck(all(w>0 for w,_ in d['children']) and sum(w for w,_ in d['children'])==1,'strict_conditional_weights')
 ck(sum(w*ch['z'] for w,ch in d['children'])==d['z'],'every_local_martingale')
 out=[(w,audit(ch,hist,full)) for w,ch in d['children']]
 vec=[sum(w*v[j] for w,(v,n) in out) for j in range(2)]
 ck(vec==d['V'],'all_history_and_future_quotes_preserved')
 return vec,sum(n for _,(v,n) in out)
examples=[]
for seed in range(1,13):
 original=make(0,seed);enrich(original,[]);red=reduce(original);v,n=audit(red,[])
 ck(v==original['V'] and n<=16,'root_payoffs_and_leaf_count')
 padded=pad(red);v2,n2=audit(padded,[],True)
 ck(n2==16 and v2==v,'full_positive_padding')
 ck(len({ch['r'] for _,ch in original['children']})>1,'reference_not_function_of_shadow_history')
 examples.append(padded)
# The marginal-law shortcut would not enforce the necessary node conditions.
ck((F(1)+F(3))/2==(F(1,2)+F(7,2))/2,'bad_coupling_equal_global_means')
ck(F(7,2)!=1 and F(1,2)!=3,'bad_coupling_fails_local_martingale')
# A genuinely nontrivial initial sigma field can be made trivial by averaging.
ck(F(1,3)*F(3,4)+F(2,3)*F(9,8)==1,'initial_root_average_in_interval')
# Strict-positive boundary example: rational identities and butterfly regions.
ks=[F(1,4),F(1,2),F(3,4)];quotes=[F(13,16),F(5,8),F(7,16)]
for e in [F(j,4*m) for m in range(2,25) for j in range(1,m)]:
 rs=[e,F(4,3)];zs=[e,F(4,3)-e/3];ps=[F(1,4),F(3,4)]
 ck(sum(p*z for p,z in zip(ps,zs))==1,'boundary_shadow_mean')
 ck(all(r>=e and z>0 and r>0 and abs(r-z)<=e for r,z in zip(rs,zs)),'boundary_all_pathwise_constraints')
 ck([sum(p*max(0,r-k) for p,r in zip(ps,rs)) for k in ks]==quotes,'boundary_exact_quotes')
ck(quotes[0]-2*quotes[1]+quotes[2]==0,'butterfly_price_zero')
ck((quotes[0]-quotes[2])/(ks[2]-ks[0])==F(3,4),'forced_tail_mass')
ck(quotes[2]+ks[2]*F(3,4)==1,'forced_tail_first_moment')
for x in [F(j,40) for j in range(0,81)]:
 b=max(0,x-ks[0])-2*max(0,x-ks[1])+max(0,x-ks[2])
 ck((b>0)==(ks[0]<x<ks[2]) and b>=0,'butterfly_exact_support')
 if x<=ks[0] or x>=ks[2]:ck(max(0,x-ks[0])-max(0,x-ks[2])==(ks[2]-ks[0])*(x>=ks[2]),'tail_indicator_difference')
for r,k,c in product([F(j,4) for j in range(-2,7)],repeat=3):
 ck((c>=0 and c>=r-k and c*(c-r+k)==0)==(c==max(0,r-k)),'positive_part_both_directions')
# Independent AST evaluator; no author code execution/import.
def eval_poly(text,vals):
 def rec(n):
  if isinstance(n,ast.Expression):return rec(n.body)
  if isinstance(n,ast.Constant):return F(n.value)
  if isinstance(n,ast.Name):return vals[n.id]
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -rec(n.operand)
  if isinstance(n,ast.BinOp):
   a,b=rec(n.left),rec(n.right)
   if isinstance(n.op,ast.Add):return a+b
   if isinstance(n.op,ast.Sub):return a-b
   if isinstance(n.op,ast.Mult):return a*b
  raise AssertionError(ast.dump(n))
 return rec(ast.parse(text,mode='eval'))
def valid(pr,vals):
 l,o,r=pr;a,b=eval_poly(l,vals),eval_poly(r,vals)
 return {'=':a==b,'>':a>b,'>=':a>=b,'<=':a<=b}[o]
A=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
encoded=json.loads((A/'example_system.json').read_text())
ck(encoded['shape']==[1,1] and encoded['nodes']==21 and encoded['leaves']==16,'formula_size')
for tree in examples:
 vals={'epsilon':F(1,2),'s_bid':F(1),'s_ask':F(1),'k_1_0':F(1),'k_2_0':F(11,10)}
 for t in [1,2]:vals[f'bid_{t}_0']=vals[f'ask_{t}_0']=tree['V'][t-1]
 def fill(d,path,weight):
  tag='root' if not path else '_'.join(map(str,path))
  vals['z_'+tag]=d['z'];vals['w_'+tag]=weight
  if path:vals['r_'+tag]=d['r'];vals['c0_'+tag]=payoff(d['r'],len(path))
  for j,(p,ch) in enumerate(d['children']):vals[f'p{j}_'+tag]=p;fill(ch,path+(j,),weight*p)
 fill(tree,(),F(1))
 ck(set(vals)==set(encoded['free_parameters']+encoded['existential_variables']),'formula_variable_coverage')
 for pred in encoded['conjunction']+encoded['input_conditions']:ck(valid(pred,vals),'independent_tree_satisfies_every_generated_predicate')
 for name,bad in [('p0_root',F(-1)),('r_0',F(-1)),('c0_0',F(-1)),('z_root',F(7)),('w_0',F(9)),('epsilon',F(-1))]:
  modified=dict(vals);modified[name]=bad
  ck(not all(valid(p,modified) for p in encoded['conjunction']),'negative_constraint_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Independent support enumeration, adapted-reference and padding controls, exact formula evaluation and strict-positive boundary controls. No general QE execution.'},indent=2,sort_keys=True))
