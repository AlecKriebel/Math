#!/usr/bin/env python3
"""A deliberately bounded, non-exhaustive backward attempt in the core C.
Success is checked as a finite proof. Failure has no unprovability meaning.
The search permits μ-bearing invariants and μ unfolding; it has no cut,
no strong induction, no deep disjunction and no cyclic closing rule.
"""
import importlib.util,json
from pathlib import Path
from functools import lru_cache
spec=importlib.util.spec_from_file_location('t1',Path(__file__).parents[1]/'turn1/proof_certificate.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
P,NP,U,W=t.P,t.NP,t.U,t.W
@lru_cache(None)
def weight(a):
 if a[0] in ('lit','var'):return 1
 if a[0] in ('box','dia'):return 1+weight(a[1])
 if a[0] in ('and','or'):return 1+weight(a[1])+weight(a[2])
 return 1+weight(a[2])
@lru_cache(None)
def hasmu(a):
 if a[0]=='mu':return True
 if a[0] in ('lit','var'):return False
 if a[0] in ('box','dia'):return hasmu(a[1])
 if a[0] in ('and','or'):return hasmu(a[1]) or hasmu(a[2])
 return hasmu(a[2])
def dual(G):return t.dual_context(G) if G else t.Or(P,NP)
def pr(rule,G,children=(),**kw):return{'rule':rule,'G':t.canonical(G),'children':children,'params':kw}
def weaken_to(proof,G):
 for a in sorted(set(G)-set(proof['G']),key=repr):proof=pr('weak',set(proof['G'])|{a},(proof,),added=a)
 return proof
class Attempt:
 def __init__(self,cap=300):
  self.cap=cap;self.memo={};self.stats={'expanded_states':0,'mu_bearing_states':0,'mu_unfolding_attempts':0,'ordinary_induction_attempts':0,'max_formula_occurrences_in_state':0,'state_cap_hits':0,'size_prunes':0,'depth_prunes':0};self.frontier=[]
 def search(self,G,ib=2,ub=3,depth=22):
  G=t.canonical(G);key=(G,ib,ub,depth)
  if key in self.memo:return self.memo[key]
  size=sum(weight(a) for a in G);self.stats['max_formula_occurrences_in_state']=max(size,self.stats['max_formula_occurrences_in_state'])
  if size>600:self.stats['size_prunes']+=1;return None
  if depth<=0:self.stats['depth_prunes']+=1;return None
  if self.stats['expanded_states']>=self.cap:self.stats['state_cap_hits']+=1;return None
  self.stats['expanded_states']+=1;self.stats['mu_bearing_states']+=any(hasmu(a) for a in G)
  S=set(G)
  if P in S and NP in S:
   ans=weaken_to(pr('ax',[P,NP]),G);self.memo[key]=ans;return ans
  # Only the first eager Boolean decomposition is used. Its failure is not
  # treated as invertibility of every Kozen derivation or as a full search.
  for f in G:
   if f[0] in ('or','and'):
    C=S-{f};a,b=f[1:]
    if f[0]=='or':
     child=self.search(C|{a,b},ib,ub,depth-1)
     ans=pr('or',G,(child,),context=t.canonical(C),left=a,right=b) if child else None
    else:
     x=self.search(C|{a},ib,ub,depth-1);y=self.search(C|{b},ib,ub,depth-1) if x else None
     ans=pr('and',G,(x,y),context=t.canonical(C),left=a,right=b) if x and y else None
    self.memo[key]=ans;return ans
  # Choose one box, retain all available diamonds, discard other side formulas
  # by explicit weakening after a successful modal step.
  for f in G:
   if f[0]=='box':
    dias={a for a in G if a[0]=='dia'};C={a[1] for a in dias};child=self.search(C|{f[1]},ib,ub,depth-1)
    if child:
     ans=weaken_to(pr('modal',dias|{f},(child,),principal=f[1]),G);self.memo[key]=ans;return ans
  if ub:
   for f in G:
    if f[0]=='mu':
     self.stats['mu_unfolding_attempts']+=1;C=S-{f};child=self.search(C|{t.subst(f[2],f[1],f)},ib,ub-1,depth-1)
     if child:
      ans=pr('unfold',G,(child,),context=t.canonical(C),principal=f);self.memo[key]=ans;return ans
  if ib:
   for f in G:
    if f[0]=='nu':
     for C in (S-{f},S):
      self.stats['ordinary_induction_attempts']+=1;prem=C|{t.subst(f[2],f[1],dual(C))};child=self.search(prem,ib-1,ub,depth-1)
      if child:
       ans=pr('ind',G,(child,),context=t.canonical(C),principal=f);self.memo[key]=ans;return ans
  if len(self.frontier)<6:self.frontier.append({'top_connectives':[a[0] for a in G],'induction_budget_left':ib,'mu_unfolding_budget_left':ub,'depth_left':depth,'formula_occurrences':size})
  self.memo[key]=None;return None

def checked_nodes(proof):
 ns=[];ids={}
 def rec(p):
  if id(p) in ids:return ids[id(p)]
  parents=tuple(rec(q) for q in p['children']);n={'rule':p['rule'],'conclusion':p['G'],'premises':parents,**p['params']};ids[id(p)]=len(ns);ns.append(n);return len(ns)-1
 root=rec(proof)
 old=t.dual_context;t.dual_context=dual_checker
 try:t.verify(ns)
 finally:t.dual_context=old
 return ns,root
def dual_checker(G):
 G=t.canonical(G)
 if not G:return t.Or(P,NP)
 out=t.neg(G[-1])
 for a in reversed(G[:-1]):out=t.And(t.neg(a),out)
 return out
rows=[];certs={}
control=Attempt(500);proof=control.search([t.B,U],ib=3,ub=3,depth=26)
assert proof is not None,'Positive control not found'
ns,root=checked_nodes(proof);certs['positive_control']={'nodes':ns,'root':root};rows.append({'name':'positive_control_B_U','found':True,'checked_proof_nodes':len(ns),'stats':control.stats})
for label,f,C in [('U_minimal',U,{W}),('W_minimal',W,{U}),('U_retained',U,{U,W}),('W_retained',W,{U,W})]:
 goal=C|{t.subst(f[2],f[1],dual(C))};attempt=Attempt(300);proof=attempt.search(goal)
 row={'name':label,'found':bool(proof),'stats':attempt.stats,'representative_frontier':attempt.frontier}
 if proof:
  full=pr('ind',[U,W],(proof,),context=t.canonical(C),principal=f);ns,root=checked_nodes(full);certs[label]={'nodes':ns,'root':root};row['checked_proof_nodes']=len(ns)
 rows.append(row)
base=Path(__file__).parent
(base/'found_certificates.json').write_text(json.dumps(certs,indent=2)+'\n')
print(json.dumps({'status':'COMPLETED_BOUNDED_ATTEMPT','limits_per_target':{'expanded_states':300,'depth':22,'ordinary_inductions_per_branch_below_forced_root':2,'mu_unfoldings_per_branch':3,'formula_occurrences_per_state':600},'heuristic_restrictions':['first eager Boolean decomposition only','modal rule keeps all diamonds and drops other side formulas','no general weakening branching','no deep disjunction or nu unfolding','no cyclic closure'],'results':rows,'inference':'Only found proofs are certified. Failure is not unprovability, not completeness evidence, and not an exhaustive search of2016 Koz-minus.'},indent=2))
