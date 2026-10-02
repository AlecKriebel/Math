#!/usr/bin/env python3
"""Exact certificate and frame controls for a failed local context permutation.
This does not prove cut nonadmissibility in any calculus.
"""
import json
from itertools import product
p=('lit','p',1);np=('lit','p',0);q=('lit','q',1);nq=('lit','q',0)
T=('or',q,nq);D=('and',nq,q);Z=('nu','x',('box',('var','x')))
def neg(a):
 if a[0]=='lit':return('lit',a[1],1-a[2])
 if a[0]=='var':return a
 if a[0] in ('box','dia'):return({'box':'dia','dia':'box'}[a[0]],neg(a[1]))
 if a[0] in ('and','or'):return({'and':'or','or':'and'}[a[0]],neg(a[1]),neg(a[2]))
 return({'nu':'mu','mu':'nu'}[a[0]],a[1],neg(a[2]))
def subst(a,x,b):
 if a[0]=='var':return b if a[1]==x else a
 if a[0]=='lit':return a
 if a[0] in ('box','dia'):return(a[0],subst(a[1],x,b))
 if a[0] in ('and','or'):return(a[0],subst(a[1],x,b),subst(a[2],x,b))
 return a if a[1]==x else(a[0],a[1],subst(a[2],x,b))
def dual_context(G):
 G=sorted(G,key=repr)
 if not G:return T
 out=neg(G[-1])
 for a in reversed(G[:-1]):out=('and',neg(a),out)
 return out
nodes=[]
def node(rule,G,parents=(),**kw):
 nodes.append({'rule':rule,'sequent':tuple(sorted(set(G),key=repr)),'parents':parents,**kw});return len(nodes)-1
def S(i):return set(nodes[i]['sequent'])
def weak(i,a):return node('weak',S(i)|{a},(i,),added=a)
n0=node('ax',[q,nq]);n1=node('or',[T],(n0,),context=(),left=q,right=nq)
n2=node('modal',[('box',T)],(n1,),principal=T)
n3=node('ind',[Z],(n2,),context=(),principal=Z)
cut_free=weak(n3,p)
l0=weak(n2,D);l1=node('ind',[D,Z],(l0,),context=(D,),principal=Z)
l2=weak(l1,p);r0=weak(n1,p);r1=weak(r0,Z)
with_cut=node('cut',[p,Z],(l2,r1),context=(p,Z),cut_formula=D)
checks=0
def check(v):
 global checks
 assert v;checks+=1
for i,n in enumerate(nodes):
 G=set(n['sequent']);ps=n['parents'];check(all(j<i for j in ps));get=lambda j:S(ps[j]);r=n['rule']
 if r=='ax':check(len(ps)==0 and any(a[0]=='lit' and neg(a) in G for a in G))
 elif r=='weak':check(len(ps)==1 and G==get(0)|{n['added']})
 elif r=='or':
  C=set(n['context']);a=n['left'];b=n['right'];check(get(0)==C|{a,b});check(G==C|{('or',a,b)})
 elif r=='modal':
  a=n['principal'];check(a in get(0));check(G=={('box',a)}|{('dia',b) for b in get(0)-{a}})
 elif r=='ind':
  C=set(n['context']);f=n['principal'];check(f[0]=='nu');check(G==C|{f});check(get(0)==C|{subst(f[2],f[1],dual_context(C))})
 elif r=='cut':
  C=set(n['context']);f=n['cut_formula'];check(G==C);check(get(0)==C|{f} and get(1)==C|{neg(f)})
 else:raise AssertionError(r)
# The direct transformed induction premise is p,box(not p).
direct=(p,('box',np));check(subst(Z[2],Z[1],dual_context([p]))==direct[1])
frames=0;validframes=0
for n in (1,2):
 edges=list(product(range(n),repeat=2))
 for mask in range(1<<len(edges)):
  R={e for j,e in enumerate(edges) if mask>>j&1};valid=True
  for lab in range(1<<n):
   value={u for u in range(n) if lab>>u&1}
   truth={u for u in range(n) if u in value or all(v not in value for x,v in R if x==u)}
   valid &= len(truth)==n;checks+=1
  check(valid==all(u==v for u,v in R));frames+=1;validframes+=valid
# Concrete serial two-state witness.
R={(0,1),(1,1)};value={1}
check(0 not in value and not all(v not in value for u,v in R if u==0))
# Retaining the principal is a DIFFERENT allowed context, not the invalid premise.
kept=dual_context([p,Z]);check(kept!=np)
print(json.dumps({'status':'PASS','exact_assertions':checks,'proof_nodes':len(nodes),'cut_free_root':cut_free,'one_cut_root':with_cut,'same_endsequent':S(cut_free)==S(with_cut),'cut_formula':'not(q or not q)','frames_checked':frames,'all_valuation_valid_frames':validframes,'serial_witness':{'states':[0,1],'edges':sorted(R),'p_true_at':[1],'failed_at':0},'scope':'The irredundant-context direct permutation fails; both final endsequents nevertheless have cut-free proofs. No general incompleteness or cut nonadmissibility claim.'},indent=2))
