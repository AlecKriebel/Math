#!/usr/bin/env python3
"""Independent finite syntax and powerset semantics audit, without importing author modules."""
from pathlib import Path
from itertools import combinations
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--author',required=True);args=p.parse_args();base=Path(args.author)
def imm(a):return tuple(imm(x) for x in a) if isinstance(a,list) else a
obj=imm(json.loads((base/'turn1/certificate.json').read_text()))
# imm intentionally leaves dicts alone; normalize its payload recursively.
def tree(a):
 if isinstance(a,list):return tuple(tree(x) for x in a)
 if isinstance(a,dict):return {k:tree(v) for k,v in a.items()}
 return a
obj=tree(obj);nodes=obj['nodes'];N=0
def ck(v):
 global N
 assert v;N+=1

def dual(f):
 tag=f[0]
 if tag=='lit':return(tag,f[1],1-f[2])
 if tag=='var':return f
 if tag in ('box','dia'):return(('dia' if tag=='box' else 'box'),dual(f[1]))
 if tag in ('and','or'):return(('or' if tag=='and' else 'and'),dual(f[1]),dual(f[2]))
 return(('nu' if tag=='mu' else 'mu'),f[1],dual(f[2]))
def fv(f):
 if f[0]=='var':return {f[1]}
 if f[0]=='lit':return set()
 if f[0] in ('box','dia'):return fv(f[1])
 if f[0] in ('and','or'):return fv(f[1])|fv(f[2])
 return fv(f[2])-{f[1]}
def replace(f,x,g):
 if f[0]=='var':return g if f[1]==x else f
 if f[0]=='lit':return f
 if f[0] in ('box','dia'):return(f[0],replace(f[1],x,g))
 if f[0] in ('and','or'):return(f[0],replace(f[1],x,g),replace(f[2],x,g))
 if f[1]==x:return f
 ck(not fv(g))
 return(f[0],f[1],replace(f[2],x,g))
def negcontext(G):
 gs=sorted(G,key=repr);ck(bool(gs));v=dual(gs[-1])
 for f in gs[-2::-1]:v=('and',dual(f),v)
 return v
def validate(ns):
 nodes=ns
 for i,node in enumerate(nodes):
  seq=set(node['conclusion']);pr=node['premises'];ck(all(j<i for j in pr));ck(all(not fv(f) for f in seq));prem=[set(nodes[j]['conclusion']) for j in pr];rule=node['rule']
  if rule=='ax':ck(not pr and len(seq)==2 and any(dual(f) in seq and f[0]=='lit' for f in seq))
  elif rule=='weak':ck(len(pr)==1 and seq==prem[0]|{node['added']})
  elif rule=='modal':
   a=node['principal'];ck(len(pr)==1 and a in prem[0]);ck(seq=={('box',a)}|{('dia',f) for f in prem[0]-{a}})
  elif rule in ('and','or'):
   G=set(node['context']);a=node['left'];b=node['right'];ck(seq==G|{(rule,a,b)})
   ck(prem==[G|{a},G|{b}] if rule=='and' else prem==[G|{a,b}])
  elif rule in ('ind','unfold'):
   G=set(node['context']);f=node['principal'];ck(seq==G|{f});ck(f[0]=='nu' if rule=='ind' else f[0]=='mu')
   g=negcontext(G) if rule=='ind' else f;ck(prem==[G|{replace(f[2],f[1],g)}])
  elif rule=='cut':
   G=set(node['context']);f=node['cut_formula'];ck(seq==G and prem==[G|{f},G|{dual(f)}])
  else:raise AssertionError(rule)
validate(nodes)
control=tree(json.loads((base/'turn5/found_certificates.json').read_text()))['positive_control']
validate(control['nodes'])
ck(set(control['nodes'][control['root']]['conclusion'])=={obj['formulas']['B'],obj['formulas']['U']})
# Independently reconstruct the exact non-induction predecessor invariant.
U0=obj['formulas']['U'];W0=obj['formulas']['V_U'];P0=('lit','p',1);NP0=('lit','p',0)
X=('box',U0);Y=('dia',W0);H=('or',X,Y)
S={P0,NP0,U0,W0,X,Y,H}
for z in (X,Y,H):S.update({('and',P0,z),('and',NP0,z),('box',('and',P0,z)),('dia',('and',NP0,z))})
ck(len(S)==19)
def contains(f,tag):
 if f[0]==tag:return True
 if f[0] in ('lit','var'):return False
 if f[0] in ('box','dia'):return contains(f[1],tag)
 if f[0] in ('and','or'):return contains(f[1],tag) or contains(f[2],tag)
 return contains(f[2],tag)
def closed_disj(f):
 z={f} if f[0]=='or' and not fv(f) else set()
 if f[0] in ('box','dia'):return z|closed_disj(f[1])
 if f[0] in ('and','or'):return z|closed_disj(f[1])|closed_disj(f[2])
 if f[0] in ('mu','nu'):return z|closed_disj(f[2])
 return z
def replace_H(f,z):
 if f==H:return z
 if f[0] in ('lit','var'):return f
 if f[0] in ('box','dia'):return(f[0],replace_H(f[1],z))
 if f[0] in ('and','or'):return(f[0],replace_H(f[1],z),replace_H(f[2],z))
 return(f[0],f[1],replace_H(f[2],z))
ck(not closed_disj(U0) and not closed_disj(W0))
ck({f for f in S if not contains(f,'nu') and not contains(f,'mu')}=={P0,NP0})
for f in S:
 ck(not fv(f) and not contains(f,'mu'));ck(closed_disj(f)<={H})
 if f[0] in ('and','or'):ck(f[1] in S and f[2] in S)
 if f[0] in ('box','dia'):ck(f[1] in S)
 if f[0]=='nu':ck(replace(f[2],f[1],f) in S)
 if H in closed_disj(f):
  for z in (X,Y):ck(replace_H(f,z) in S)
 if contains(f,'nu'):
  for g in (U0,W0):ck(contains(replace(g[2],g[1],dual(f)),'mu'))
# Separate explicit finite semantics for U,V; no certificate evaluator reused.
models=0
for n in range(1,4):
 allmask=(1<<n)-1
 for em in range(1<<(n*n)):
  succ=[sum(((em>>(i*n+j))&1)<<j for j in range(n)) for i in range(n)]
  def box(S):return sum((not bool(t & (allmask^S)))<<i for i,t in enumerate(succ))
  def dia(S):return sum(bool(t&S)<<i for i,t in enumerate(succ))
  def fixed(F,greatest):
   a=allmask if greatest else 0
   for _ in range(n+1):
    b=F(a)
    if b==a:return a
    a=b
   raise AssertionError('fixed point did not stabilize')
  for pval in range(1<<n):
   def V(X,greatest=True):return fixed(lambda Y:box(pval&(box(X)|dia(Y))),greatest)
   U=fixed(lambda X:dia((allmask^pval)&(box(X)|dia(V(X)))),True);W=V(U)
   ck(U==dia(allmask^pval));ck(W==box(pval));ck((U|W)==allmask);models+=1
   A=dia(allmask^pval);Bv=box(pval);ck(V(A)==Bv)
   FU=lambda Z:dia((allmask^pval)&(box(Z)|dia(V(Z))))
   FW=lambda Z:box(pval&(box(U)|dia(Z)))
   ck((W|FU(allmask^W))==allmask);ck((U|FW(allmask^U))==allmask)
   inv=(allmask^U)&(allmask^W)
   ck((U|W|FU(inv))==allmask);ck((U|W|FW(inv))==allmask)
   # Reproduce context-permutation frame criterion independently.
   valid=((pval|box(allmask^pval))==allmask)
   if succ==[0]*n:ck(valid)
  schema=all((pval|box(allmask^pval))==allmask for pval in range(1<<n))
  ck(schema==all(t&~(1<<i)==0 for i,t in enumerate(succ)))
# Both auxiliary truth assignments in the one-state loop refute Phi.
for pval in (0,1):
 def fp(F):
  a=0
  for _ in range(2):
   b=F(a)
   if a==b:return a
   a=b
  raise AssertionError
 def V(X):return fp(lambda Y:pval&(X|Y))
 U=fp(lambda X:(1-pval)&(X|V(X)));W=V(U)
 ck(U==W==0)
 if pval:ck(all((1-pval)&(Z|V(Z))==0 for Z in (0,1)))
 else:ck(all(pval&(U|Z)==0 for Z in (0,1)))
print(json.dumps({'status':'PASS','exact_assertions':N,'independently_checked_certificate_nodes':len(nodes),'independently_checked_search_control_nodes':len(control['nodes']),'ordinary_finite_models_through_three_states':models,'scope':'Exact finite syntax and model controls only; structural lower bounds and the proof-fragment theorem require separate metaproof review.'},indent=2,sort_keys=True))
