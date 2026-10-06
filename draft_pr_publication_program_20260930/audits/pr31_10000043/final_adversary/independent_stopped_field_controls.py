#!/usr/bin/env python3
"""Independent exact finite-stop controls. No submitted module imported."""
from pathlib import Path
from collections import Counter,deque,defaultdict
from itertools import product
from fractions import Fraction
import json,hashlib,datetime
HERE=Path(__file__).resolve().parent
V=[(u,h) for u in (0,1) for h in range(3)]
edge=lambda a,b:tuple(sorted((a,b)))
VE=sorted(edge((u,h),(u,h+1)) for u in (0,1) for h in range(2))
HE=[edge((0,h),(1,h)) for h in range(3)]
E=sorted(VE+HE);adj={v:sorted(w for w in V if w!=v and edge(v,w) in E) for v in V}
N=len(E);checks=0

def expect(cond):
 global checks
 checks+=1
 assert cond

def trace(cap,root,reverse,primitive,mutant=None):
 accepted={root};counts=Counter({root[0]:1});q=deque([root]);states={};snap=[{}];j=0;labels=[]
 while q:
  v=q.popleft()
  for w in adj[v][::-1] if reverse else adj[v]:
   e=edge(v,w)
   if e in states:continue
   if e in VE:state=primitive[VE.index(e)];label=('V',e)
   else:
    state=primitive[len(VE)+j];label=('H',j);j+=1
    if mutant=='anticipating_horizontal_OR' and j==1:state=max(primitive[len(VE)],primitive[len(VE)+1])
   states[e]=state;labels.append(label);snap.append(states.copy())
   if state and w not in accepted and counts[w[0]]<cap:accepted.add(w);counts[w[0]]+=1;q.append(w)
 expect(j<=2*cap);expect(len(labels)==len(set(labels)))
 expect(all(c<=cap for c in counts.values()))
 return snap,accepted

def distribution(cap,root,reverse,mutant=None):
 K=len(VE)+2*cap;hist=[defaultdict(Counter) for i in range(N+1)];configuration_count=0;terminal_clusters=Counter();joint=defaultdict(Counter)
 for primitive in product((0,1),repeat=K):
  snapshots,accepted=trace(cap,root,reverse,primitive,mutant)
  y=int(any(primitive[len(VE):]));
  for fallback in product((0,1),repeat=N):
   ones=sum(primitive)+sum(fallback);configuration_count+=1
   for n in range(N+1):
    states=snapshots[min(n,len(snapshots)-1)]
    bits=tuple(states.get(e,fallback[k]) for k,e in enumerate(E))
    if mutant=='fallback_reuses_first_reservoir':
     bits=tuple(states.get(e,primitive[len(VE)] if e in HE else fallback[k]) for k,e in enumerate(E))
    hist[n][bits][ones]+=1
    if n==N:joint[(bits[E.index(HE[0])],y)][ones]+=1
 return hist,configuration_count,K+N,joint

def evaluate(counter,total,p):return sum(Fraction(c)*p**k*(1-p)**(total-k) for k,c in counter.items())
reports=[]
for cap,root,reverse in product((1,2),((0,0),(1,2)),(False,True)):
 hist,count,total,joint=distribution(cap,root,reverse)
 for p in [Fraction(4,9),Fraction(1,11),Fraction(0),Fraction(1)]:
  for n in range(N+1):
   expect(sum(evaluate(c,total,p) for c in hist[n].values())==1)
   for bits in product((0,1),repeat=N):
    actual=evaluate(hist[n][bits],total,p);expected=p**sum(bits)*(1-p)**(N-sum(bits));expect(actual==expected)
  q=1-(1-p)**(2*cap);expect(sum(evaluate(c,total,p) for (w,y),c in joint.items() if y)==q)
 reports.append({'cap':cap,'root':root,'reverse_order':reverse,'primitive_and_fallback_assignments':count,'stop_indices':list(range(N+1)),'physical_atoms':2**N,'exact_p':['4/9','1/11','0','1'],'all_stopped_completed_fields_iid':True})
mutants=[]
for mutant in ['anticipating_horizontal_OR','fallback_reuses_first_reservoir']:
 hist,count,total,joint=distribution(2,(0,0),False,mutant);p=Fraction(4,9);witness=None;bad=0
 for n in range(N+1):
  for bits in product((0,1),repeat=N):
   actual=evaluate(hist[n][bits],total,p);expected=p**sum(bits)*(1-p)**(N-sum(bits))
   if actual!=expected:
    bad+=1
    if witness is None:witness={'stop':n,'bits':bits,'actual':str(actual),'iid_expected':str(expected)}
 expect(bad>0);mutants.append({'mutation':mutant,'detected':True,'bad_stop_atoms':bad,'witness':witness})
# The necessary W and Y marginals do not imply their independence.
hist,count,total,joint=distribution(1,(0,0),False);p=Fraction(4,9)
wy=sum(evaluate(c,total,p) for (w,y),c in joint.items() if w and y);q=1-(1-p)**2
expect(wy!=p*q)
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'positive_cases':reports,'broken_variants':mutants,'W_Y_independence_false_control':{'P_Wcrossing_and_Yopen':str(wy),'independent_expected':str(p*q),'actual_covariance':str(wy-p*q)},'checks':checks,'all_passed':True,'scope':'Exact finite primitive/fallback enumeration on K2×P3 at every stop. This supplements the written countable-cylinder proof and does not prove infinite-volume assertions.'}
(HERE/'STOPPED_FIELD_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
