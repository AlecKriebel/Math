"""Exact obstruction search for strict 2-opt color-improvement arguments.
Finite diagnostics only; this script is not a verifier of the full conjecture.
"""
from itertools import combinations,permutations
import json,datetime
from pathlib import Path

def colors(cycle,mod):return [(cycle[i]+cycle[(i+1)%len(cycle)])%mod for i in range(len(cycle))]
def switches(c):
 n=len(c)
 for i in range(n):
  for j in range(i+2,n):
   if i==0 and j==n-1:continue
   yield c[:i+1]+c[i+1:j+1][::-1]+c[j+1:]
def run():
 tested=0
 for mod in (5,7,9,11):
  for n in range(4,min(mod,8)+1):
   for tailset in combinations(range(1,mod),n-1):
    for tail in permutations(tailset):
     if tail[0]>tail[-1]:continue
     c=(0,)+tail;s=colors(c,mod);score=len(set(s))
     if score==n:continue
     tested+=1
     ns=[(len(set(colors(d,mod))),d) for d in switches(c)]
     if max(k for k,d in ns)<=score:
      found={'group':'Z/'+str(mod),'subset':sorted(c),'cycle':c,'edge_sums':s,'score':score,'maximum_2opt_score':max(k for k,d in ns),'moves':[{'cycle':d,'edge_sums':colors(d,mod),'score':k} for k,d in ns]}
      # Independent positive witness in same finite subset, to avoid calling trap a counterexample.
      found['rainbow_witness']=next((0,)+t for t in permutations(tailset) if len(set(colors((0,)+t,mod)))==n)
      return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'nonrainbow_cycles_examined':tested,'strict_improvement_trap':found,'interpretation':'Strict 2-opt improvement alone can stop short of a rainbow cycle. This is not a counterexample to Kourovka21.130.'}
 raise RuntimeError('No trap within enumerated range')
if __name__=='__main__':
 result=run();Path(__file__).with_name('local_landscape_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
