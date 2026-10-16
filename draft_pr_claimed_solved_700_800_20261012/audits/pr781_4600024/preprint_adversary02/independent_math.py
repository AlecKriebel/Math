"""Independent finite-state falsification controls; no reviewed-code imports or writes."""
from collections import deque
from itertools import product
import json
checks=0
def need(x,m):
 global checks
 checks+=1
 if not x: raise ValueError(m)
def words(n):return [''.join(t) for t in product('01',repeat=n)]
def step(E,Q,a):return frozenset(v for u,b,v in E if u in Q and a==b)
def vs(E):return frozenset(v for u,a,w in E for v in (u,w))
def accept(E,w):
 Q=vs(E)
 for a in w:Q=step(E,Q,a)
 return bool(Q)
def profile(w,k):
 l=k//2;r=k-l
 return frozenset((w[max(0,i-l):i],w[i:i+r]) for i in range(len(w)))
def sig(w,k):
 if len(w)<k:return ('s',w)
 return ('l',w[:k-1],w[-(k-1):],frozenset(w[i:i+k] for i in range(len(w)-k+1)))
def sigstep(s,a,k):
 if s[0]=='s':return sig(s[1]+a,k)
 _,p,t,f=s
 return ('l',p,(t+a)[-(k-1):],f|{t+a})
def output(w,ell,table):return ''.join(table[w[i:i+ell]] for i in range(len(w)-ell+1))
def approximation(E,n):return tuple((w[:-1],w[-1],w[1:]) for w in words(n) if accept(E,w))
def exact_collision(E,ell,table,k):
 # Finite closure of original-language state x transducer state x LT sufficient signature.
 initial=(vs(E),vs(E),'',('s',''))
 queue=deque([initial]);reps={initial:''};good={};bad={}
 while queue:
  state=queue.popleft();Q,R,tail,s=state;w=reps[state];p=profile(w,k)
  if Q:good.setdefault(p,w)
  if not R:bad.setdefault(p,w)
  if p in good and p in bad:
   x,y=good[p],bad[p]
   need(accept(E,x) and not accept(E,output(y,ell,table)) and profile(x,k)==profile(y,k),'collision certificate')
   return {'collision':True,'states':len(reps),'good':x,'bad':y}
  for a in '01':
   pending=tail+a
   RR=step(E,R,table[pending]) if len(pending)==ell else R
   tt=pending[1:] if len(pending)==ell else pending
   nxt=(step(E,Q,a),RR,tt,sigstep(s,a,k))
   if nxt not in reps:reps[nxt]=w+a;queue.append(nxt)
 return {'collision':False,'states':len(reps)}
def exact_bad(D,E,ell,table):
 initial=[(v,vs(E),'') for v in vs(D)];q=deque(initial);reps={s:'' for s in initial}
 while q:
  v,R,t=s=q.popleft()
  for u,a,z in D:
   if u!=v:continue
   pending=t+a;RR=step(E,R,table[pending]) if len(pending)==ell else R
   tt=pending[1:] if len(pending)==ell else pending;w=reps[s]+a
   if not RR:
    need(accept(D,w) and not accept(E,output(w,ell,table)),'bad input witness')
    return w
   nxt=(z,RR,tt)
   if nxt not in reps:reps[nxt]=w;q.append(nxt)
 return None
def main():
 graphs={'even':((0,'0',0),(0,'1',1),(1,'1',0)),'golden':((0,'0',0),(0,'1',1),(1,'0',0)),'period2':((0,'0',1),(1,'1',0)),'singleton':((0,'0',0),),'full':((0,'0',0),(0,'1',0))}
 # Exact all-word comparison of profile collisions and canonical bad-word reachability.
 # Not inferred from bounded enumeration: both closures are finite automata.
 results=[]
 for name,E in graphs.items():
  for bits in product('01',repeat=4):
   table=dict(zip(words(2),bits))
   for k in (2,3):
    c=exact_collision(E,2,table,k);bad=exact_bad(approximation(E,k),E,2,table)
    need(c['collision']==(bad is not None),'saturation versus exact profile closure')
    results.append({'shift':name,'table':''.join(bits),'k':k,**c,'canonical_bad':bad})
 # All width-three completions for three different widened projections, including
 # asymmetric memory/anticipation; finite windows check actual normalization.
 completion_cases=0
 for name in ('even','golden','period2','singleton'):
  E=graphs[name];absent=[w for w in words(3) if not accept(E,w)]
  for index in (0,1,2):
   for bits in product('01',repeat=len(absent)):
    table={w:w[index] for w in words(3)};table.update(zip(absent,bits))
    bad=exact_bad(approximation(E,3),E,3,table)
    need((bad is not None)==(name=='even'),'all projection completions on T[3]')
    completion_cases+=1
 # Finite output and ideal property, exhaust all width-two rules and words <=6,
 # all single-letter left/right paddings. This includes empty/short outputs.
 ideal_cases=0
 for name,E in graphs.items():
  for bits in product('01',repeat=4):
   table=dict(zip(words(2),bits))
   for n in range(7):
    for w in words(n):
     bad=not accept(E,output(w,2,table))
     if bad:
      for a,b in product('01',repeat=2):
       need(not accept(E,output(a+w+b,2,table)),'ideal under padding')
       ideal_cases+=1
 # Independent endpoint controls. Same factors alone do not imply profiles.
 need(profile('00100',3)!=profile('001001',3),'endpoint-sensitive negative control')
 need(profile('010',2)==profile('0101',2),'actual PRZ convention at k=2')
 print(json.dumps({'result':'PASS','checks':checks,'exact_profile_vs_approximation_cases':len(results),'exact_states_total':sum(r['states'] for r in results),'projection_completion_cases':completion_cases,'ideal_padding_cases':ideal_cases,'cases':results,'scope':'Finite all-word closure controls and finite sweeps; does not prove general PRZ theorem or universal mathematical theorem.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
