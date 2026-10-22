#!/usr/bin/env python3
"""Finite proof certificate in an explicitly pinned ordinary-induction core.
No deep disjunction, strong induction, cyclic closure or semantic oracle.
One separately marked final cut is fixed-point-free, on box(p).
"""
import json,hashlib
P=('lit','p',1);NP=('lit','p',0)
def Var(x):return('var',x)
def Box(a):return('box',a)
def Dia(a):return('dia',a)
def And(a,b):return('and',a,b)
def Or(a,b):return('or',a,b)
def Nu(x,a):return('nu',x,a)
def Mu(x,a):return('mu',x,a)
def neg(a):
 t=a[0]
 if t=='lit':return('lit',a[1],1-a[2])
 if t=='var':return a
 if t in ('box','dia'):return({'box':'dia','dia':'box'}[t],neg(a[1]))
 if t in ('and','or'):return({'and':'or','or':'and'}[t],neg(a[1]),neg(a[2]))
 return({'mu':'nu','nu':'mu'}[t],a[1],neg(a[2]))
def subst(a,x,b):
 t=a[0]
 if t=='var':return b if a[1]==x else a
 if t=='lit':return a
 if t in ('box','dia'):return(t,subst(a[1],x,b))
 if t in ('and','or'):return(t,subst(a[1],x,b),subst(a[2],x,b))
 return a if a[1]==x else(t,a[1],subst(a[2],x,b))
def free(a):
 if a[0]=='var':return{a[1]}
 if a[0]=='lit':return set()
 if a[0] in ('box','dia'):return free(a[1])
 if a[0] in ('and','or'):return free(a[1])|free(a[2])
 return free(a[2])-{a[1]}
def canonical(G):return tuple(sorted(set(G),key=repr))
def dual_context(G):
 G=canonical(G)
 if not G:raise ValueError('The present certificate uses no empty induction context')
 a=neg(G[-1])
 for b in reversed(G[:-1]):a=And(neg(b),a)
 return a
nodes=[]
def add(rule,G,prem=(),**data):
 n={'rule':rule,'conclusion':canonical(G),'premises':tuple(prem),**data};nodes.append(n);return len(nodes)-1
def seq(i):return set(nodes[i]['conclusion'])
def ax():return add('ax',[P,NP])
def weak(i,a):return add('weak',seq(i)|{a},[i],added=a)
def modal(i,a):
 G=seq(i)-{a};return add('modal',[Box(a)]+[Dia(b) for b in G],[i],principal=a)
def disj(i,G,a,b):return add('or',set(G)|{Or(a,b)},[i],context=canonical(G),left=a,right=b)
def conj(i,j,G,a,b):return add('and',set(G)|{And(a,b)},[i,j],context=canonical(G),left=a,right=b)
def ind(i,G,f):return add('ind',set(G)|{f},[i],context=canonical(G),principal=f)
def unfold(i,G,f):return add('unfold',set(G)|{f},[i],context=canonical(G),principal=f)
A=Dia(NP);B=Box(P)
def R(x,y):return Or(Box(x),Dia(y))
def V(x):return Nu('y',Box(And(P,R(x,Var('y')))))
U=Nu('x',Dia(And(NP,R(Var('x'),V(Var('x'))))));W=V(U)
# T_X: from a closed proof of X,B to a closed proof of A,V(X).
def T(X,pi):
 n=modal(pi,X);n=disj(n,[],Box(X),Dia(B));n=weak(n,NP)
 n=conj(ax(),n,[NP],P,R(X,B));n=modal(n,And(P,R(X,B)))
 return ind(n,[A],V(X))
iAB=modal(ax(),P)
iAVA=T(A,iAB)
# S: construct B,U from A,V(A).
n=modal(iAVA,A);n=disj(n,[],Box(A),Dia(V(A)));n=weak(n,P)
n=conj(ax(),n,[P],NP,R(A,V(A)));n=modal(n,P)
iBU=ind(n,[B],U)
iAW=T(U,iBU)
# Reverse implications: unfold each least-fixed-point dual once, then
# use only an atomic identity, weakening, disjunction and modal K.
def reverse(Uf,context):
 f=neg(Uf);body=subst(f[2],f[1],f);modalbody=body[1]
 assert modalbody[0]=='or'
 left,right=modalbody[1:]
 i=weak(ax(),right)
 opposite=neg(left)
 i=disj(i,[opposite],left,right)
 principal=modalbody if body[0]=='box' else opposite
 i=modal(i,principal)
 assert seq(i)=={context,body}
 return unfold(i,[context],f)
iUA=reverse(U,A);iWB=reverse(W,B)
# Final source sequent U,W, with exactly one explicit cut on B.
i1=weak(iBU,W);i2=weak(iAW,U)
iPhi=add('cut',[U,W],[i1,i2],context=canonical([U,W]),cut_formula=B)
checks=0
def check(ok):
 global checks
 assert ok;checks+=1
def verify(ns):
 for idx,n in enumerate(ns):
  G=set(n['conclusion']);ps=n['premises'];check(all(i<idx for i in ps));check(all(not free(a) for a in G));r=n['rule']
  get=lambda j:set(ns[ps[j]]['conclusion'])
  if r=='ax':check(len(ps)==0);check(G=={P,NP})
  elif r=='weak':check(len(ps)==1);check(G==get(0)|{n['added']})
  elif r=='modal':
   a=n['principal'];check(len(ps)==1 and a in get(0));check(G=={Box(a)}|{Dia(b) for b in get(0)-{a}})
  elif r in ('or','and'):
   C=set(n['context']);a=n['left'];b=n['right'];check(G==C|{(r,a,b)})
   if r=='or':check(len(ps)==1 and get(0)==C|{a,b})
   else:check(len(ps)==2 and get(0)==C|{a} and get(1)==C|{b})
  elif r in ('ind','unfold'):
   C=set(n['context']);f=n['principal'];check(len(ps)==1 and G==C|{f});check(f[0] in ('mu','nu'))
   if r=='ind':check(f[0]=='nu');body=subst(f[2],f[1],dual_context(C))
   else:body=subst(f[2],f[1],f)
   check(get(0)==C|{body})
  elif r=='cut':
   C=set(n['context']);f=n['cut_formula'];check(len(ps)==2 and G==C);check(get(0)==C|{f} and get(1)==C|{neg(f)})
  else:raise ValueError(r)
verify(nodes)
def ancestors(i):
 seen=set();todo=[i]
 while todo:
  j=todo.pop()
  if j not in seen:seen.add(j);todo.extend(nodes[j]['premises'])
 return seen
roots={'A_implies_U':iBU,'U_implies_A':iUA,'B_implies_VU':iAW,'VU_implies_B':iWB,'Phi_with_one_box_p_cut':iPhi}
for k,i in roots.items():
 cuts=[j for j in ancestors(i) if nodes[j]['rule']=='cut'];check(len(cuts)==int(k=='Phi_with_one_box_p_cut'))
check(neg(A)==B and neg(B)==A)
# Verify one deliberately corrupt inference is rejected by the syntactic checker.
import copy
bad=copy.deepcopy(nodes);bad[iBU]['principal']=W
try:verify(bad)
except AssertionError:rejected=True
else:rejected=False
check(rejected)
payload={'formulas':{'A':A,'B':B,'U':U,'V_U':W},'nodes':nodes,'roots':roots}
receipt={'status':'PASS','nodes':len(nodes),'root_node_ids':roots,'root_ancestral_nodes':{k:len(ancestors(i)) for k,i in roots.items()},'rules_used':sorted({n['rule'] for n in nodes}),'cut_free_roots':4,'final_cut_formula':'box(p)','final_cut_has_fixed_points':False,'assertions_including_negative_control':checks,'scope':'Finite author proof certificate only. No assertion that the final source sequent lacks a cut-free proof; no general completeness or incompleteness claim.'}
if __name__=='__main__':
 from pathlib import Path
 base=Path(__file__).parent
 (base/'certificate.json').write_text(json.dumps(payload,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
