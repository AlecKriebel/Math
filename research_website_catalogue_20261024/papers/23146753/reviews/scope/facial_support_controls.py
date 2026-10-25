"""Exact facial obstructions, independent of supplied support scripts and numerical LP."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,datetime
E=Path(__file__).resolve().parent

def bit(x,i):return (x>>i)&1
def ck(v,msg):
 if not v:raise RuntimeError(msg)
def islat(S):return all(x&y in S and x|y in S for x in S for y in S)
def feat(xs,G):return Counter((e,bit(x,e[0]),bit(x,e[1])) for x in xs for e in G)
counts=Counter();samples=[]
for n in range(2,5):
 O=list(range(1<<n));ES=list(combinations(range(n),2));lats=[{x for x in O if m>>x&1} for m in range(1,1<<len(O))];lats=[S for S in lats if islat(S)]
 for gm in range(1,1<<len(ES)):
  G=[e for k,e in enumerate(ES) if gm>>k&1];isolated=[i for i in range(n) if not any(i in e for e in G)]
  for S in lats:
   proj={e:{(bit(x,e[0]),bit(x,e[1])) for x in S} for e in G};R={x for x in O if all((bit(x,i),bit(x,j)) in proj[i,j] for i,j in G)};counts['lattice_graph_pairs_nonempty_E']+=1
   if R==S:counts['edge_A_feasible']+=1;continue
   counts['not_edge_A_feasible']+=1;cert=None
   for i in isolated:
    for a in S:
     u=a^(1<<i)
     if u not in S:cert=('invisible_isolate',[u],[a]);break
    if cert:break
   active=[i for i in range(n) if len({bit(x,i) for x in S})==2];classes=[];which={}
   for i in active:
    if i in which:continue
    C=[j for j in active if all(bit(x,i)==bit(x,j) for x in S)];k=len(classes);classes.append(C)
    for j in C:which[j]=k
   if not cert:
    for C in classes:
     reached={C[0]}
     while True:
      more=reached|{v for u,v in G if u in reached and v in C}|{u for u,v in G if v in reached and u in C}
      if more==reached:break
      reached=more
     if reached==set(C):continue
     mask=sum(1<<i for i in C);d=sum(1<<i for i in reached);f=mask^d
     for a in S:
      if a&mask:continue
      b=a|mask
      if b not in S:continue
      u=a|d;v=a|f
      if u not in S and v not in S:cert=('disconnected_tie_class',[u,v],[a,b]);break
     if cert:break
   if not cert:
    order={(K,L):all(bit(x,C[0])<=bit(x,D[0]) for x in S) for K,C in enumerate(classes) for L,D in enumerate(classes) if K!=L}
    for K,C in enumerate(classes):
     for L,D in enumerate(classes):
      if K==L or not order[K,L] or any(M not in [K,L] and order.get((K,M)) and order.get((M,L)) for M in range(len(classes))):continue
      if any((i in C and j in D) or (i in D and j in C) for i,j in G):continue
      cm=sum(1<<i for i in C);dm=sum(1<<i for i in D)
      for a in S:
       if a&(cm|dm):continue
       b=a|dm;c=a|cm|dm;u=a|cm
       if b in S and c in S and u not in S:cert=('missing_cover_edge',[u,b],[a,c]);break
      if cert:break
     if cert:break
   ck(cert is not None,('missing_facial_obstruction',n,G,sorted(S)))
   kind,left,right=cert;ck(all(x in S for x in right),'RHS_support');ck(any(x not in S for x in left),'LHS_forbidden');ck(feat(left,G)==feat(right,G),'exact_original_edge_column_sum_certificate');counts[kind]+=1
   if sum(x['kind']==kind for x in samples)<2:samples.append({'n':n,'edges':G,'support':sorted(S),'kind':kind,'left':left,'right':right,'same_sum_original_edge_feature_columns':True,'interpretation':'A facial nonnegative exposure would be zero on RHS and positive on at least one LHS term, contradiction.'})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','exact_integer_no_LP_tolerance':True,'counts':dict(counts),'samples':samples,'scope':'All nonempty-edge simple graphs with2–4vertices and all nonemptyBoolean sublattice supports; finite check of universal proof mechanisms, not a finite proof of the theorem.'};(E/'FACIAL_SUPPORT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'counts':result['counts'],'samples':len(samples)},indent=2))
