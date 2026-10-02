#!/usr/bin/env python3
"""Exact syntactic/one-state controls for the stated two-induction lower bound.
The universal metaproof is in TURN_2.md, not inferred from finite enumeration.
"""
import importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('turn1',Path(__file__).parents[1]/'turn1/proof_certificate.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
U,W=t.U,t.W;checks=0
def check(b):
 global checks
 assert b;checks+=1
def walk(a):
 yield a
 if a[0] in ('lit','var'):return
 if a[0] in ('box','dia'):yield from walk(a[1])
 elif a[0] in ('and','or'):
  yield from walk(a[1]);yield from walk(a[2])
 else:yield from walk(a[2])
def bound_forms(a):return {b for b in walk(a) if b[0] in ('mu','nu') and not t.free(b)}
for a in (U,W):
 check(bound_forms(a)<={U,W})
 check(not any(b[0]=='mu' for b in walk(a)))
 check(not any(b[0]=='or' and not t.free(b) for b in walk(a)))
 unfolded=t.subst(a[2],a[1],a)
 check(bound_forms(unfolded)<={U,W})
# Minimal-context ordinary-induction obligations. Set-sequent rules also permit
# retaining the principal formula in the side context; include both cases.
PU=(W,t.subst(U[2],U[1],t.neg(W)))
PW=(U,t.subst(W[2],W[1],t.neg(U)))
DU=t.dual_context([U,W])
PUkeep=(U,W,t.subst(U[2],U[1],DU))
PWkeep=(U,W,t.subst(W[2],W[1],DU))
def eval_formula(a,p,swapped,env=None):
 env={} if env is None else env
 tag=a[0]
 if tag=='lit':return p if a[2] else not p
 if tag=='var':return env[a[1]]
 if tag in ('box','dia'):return eval_formula(a[1],p,swapped,env) # one state with self-loop
 if tag in ('and','or'):
  x=eval_formula(a[1],p,swapped,env);y=eval_formula(a[2],p,swapped,env)
  return (x and y) if tag=='and' else (x or y)
 least=(tag=='mu')!=swapped;x=not least
 for _ in range(3):
  y=eval_formula(a[2],p,swapped,{**env,a[1]:x})
  if x==y:return x
  x=y
 raise AssertionError('not monotone Boolean fixed point')
rows=[]
for p in (False,True):
 check(not eval_formula(U,p,True));check(not eval_formula(W,p,True))
 # The ordinary semantics also verifies the exact component equivalences here.
 check(eval_formula(U,p,False)==(not p));check(eval_formula(W,p,False)==p)
 principal=U if p else W
 for z in (False,True):
  body=eval_formula(principal[2],p,True,{principal[1]:z});check(not body)
 for gamma in (False,True):
  body=eval_formula(principal[2],p,True,{principal[1]:not gamma})
  check((gamma or body)==(gamma or eval_formula(principal,p,True)))
 rows.append({'p':p,'swapped_U':False,'swapped_W':False,'induction_locally_sound_for':'U' if p else 'W'})
check(not any(eval_formula(a,True,True) for a in PU));check(not any(eval_formula(a,False,True) for a in PW))
check(not any(eval_formula(a,True,True) for a in PUkeep));check(not any(eval_formula(a,False,True) for a in PWkeep))
# Ordinary countermodels to the singleton premises needed for final weakening.
# On a dead-end world U is false since its outer body is diamond(...).
# On a self-loop world with p false, W is false by its outer box(p and ...).
check(not eval_formula(W,False,False))
# Bound duality check on all closed subformulas of the displayed obligations,
# under both singleton labelings and the swapped interpretation.
fs={b for a in (U,W,*PU,*PW,*PUkeep,*PWkeep) for b in walk(a) if not t.free(b)}
for a in fs:
 for p in (False,True):check(eval_formula(t.neg(a),p,True)==(not eval_formula(a,p,True)))
print(json.dumps({'status':'PASS','exact_assertions':checks,'closed_formulas_in_duality_controls':len(fs),'core_final_induction_context_options':4,'one_state_rows':rows,'claim':'Any finite cut-free proof of Phi in the pinned2016 Koz-minus requires at least two ordinary-induction occurrences. Existence or nonexistence of such a proof remains unresolved.','scope':'Finite controls support the written syntactic preservation and swapped-semantics metaproof, not proof-search exhaustiveness.'},indent=2))
