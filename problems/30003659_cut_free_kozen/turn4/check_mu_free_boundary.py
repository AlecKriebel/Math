#!/usr/bin/env python3
"""Exact syntax controls for the 19-formula predecessor invariant.
This is a restricted-fragment obstruction, not general Kozen incompleteness.
"""
import importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('t1',Path(__file__).parents[1]/'turn1/proof_certificate.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
P,NP,U,W=t.P,t.NP,t.U,t.W;X=t.Box(U);Y=t.Dia(W);H=t.Or(X,Y)
S={P,NP,U,W,X,Y,H}
for h in (X,Y,H):
 S|={t.And(P,h),t.And(NP,h),t.Box(t.And(P,h)),t.Dia(t.And(NP,h))}
checks=0
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
def replace(a,b,c):
 if a==b:return c
 if a[0] in ('lit','var'):return a
 if a[0] in ('box','dia'):return(a[0],replace(a[1],b,c))
 if a[0] in ('and','or'):return(a[0],replace(a[1],b,c),replace(a[2],b,c))
 return(a[0],a[1],replace(a[2],b,c))
check(len(S)==19);check(all(not t.free(a) for a in S))
closed_or_counts={}
for a in S:
 check(not any(b[0]=='mu' for b in walk(a)))
 check({b for b in walk(a) if b[0] in ('mu','nu') and not t.free(b)}<={U,W})
 if a[0] in ('and','or'):check(a[1] in S and a[2] in S)
 if a[0] in ('box','dia'):check(a[1] in S)
 if a[0]=='nu':check(t.subst(a[2],a[1],a) in S)
 ors=[b for b in walk(a) if b[0]=='or' and not t.free(b)]
 check(len(ors)<=1);check(all(b==H for b in ors))
 for b in ors:
  check(replace(a,b,b[1]) in S);check(replace(a,b,b[2]) in S)
 closed_or_counts[repr(a)]=len(ors)
check({a for a in S if not any(b[0] in ('mu','nu') for b in walk(a))}=={P,NP})
# A ν-principal U/W uses its argument, so substituting a negated side
# formula with a binder introduces a μ occurrence literally.
for f in (U,W):
 for a in S-{P,NP}:
  premise=t.subst(f[2],f[1],t.neg(a));check(any(b[0]=='mu' for b in walk(premise)))
# Independent direct semantics on finite frames for six non-tautological
# singleton/empty side contexts. General validity equivalences are proved in turn1.
def ev(a,R,lab,env=None):
 env={} if env is None else env;worlds=set(range(len(R)));tag=a[0]
 if tag=='lit':return set(lab) if a[2] else worlds-set(lab)
 if tag=='var':return env[a[1]]
 if tag=='and':return ev(a[1],R,lab,env)&ev(a[2],R,lab,env)
 if tag=='or':return ev(a[1],R,lab,env)|ev(a[2],R,lab,env)
 if tag=='box':
  z=ev(a[1],R,lab,env);return{u for u in worlds if set(R[u])<=z}
 if tag=='dia':
  z=ev(a[1],R,lab,env);return{u for u in worlds if set(R[u])&z}
 z=worlds if tag=='nu' else set()
 for _ in range(len(R)+1):
  zz=ev(a[2],R,lab,{**env,a[1]:z})
  if zz==z:return z
  z=zz
 raise AssertionError('fixed point not reached')
cases=[('U_empty',U,[],[[0]],{0}),('W_empty',W,[],[[0]],set()),('U_p',U,[P],[[]],set()),('W_p',W,[P],[[0]],set()),('U_notp',U,[NP],[[0]],{0}),('W_notp',W,[NP],[[1],[1]],{0})]
for name,f,G,R,lab in cases:
 truth=ev(f,R,lab)
 for a in G:truth|=ev(a,R,lab)
 check(0 not in truth)
# The actual one-cut proof from turn1 is ν-only; the separate reverse-
# implication certificate roots do contain μ and are not used here.
used=t.ancestors(t.roots['Phi_with_one_box_p_cut'])
for i in used:
 for a in t.nodes[i]['conclusion']:check(not any(b[0]=='mu' for b in walk(a)))
check(sum(t.nodes[i]['rule']=='cut' for i in used)==1)
print(json.dumps({'status':'PASS','exact_assertions':checks,'predecessor_formula_count':len(S),'fixed_point_free_members':['p','not p'],'non_tautological_induction_context_countermodels':len(cases),'nu_only_one_cut_ancestor_nodes':len(used),'claim':'The pinned2016 cut-free Koz-minus has no entirely mu-free proof of Phi. A full proof with mu-bearing intermediate formulas remains possible and unresolved.','scope':'Exact syntax and finite countermodels support the written minimal-induction proof; no general incompleteness claim.'},indent=2))
