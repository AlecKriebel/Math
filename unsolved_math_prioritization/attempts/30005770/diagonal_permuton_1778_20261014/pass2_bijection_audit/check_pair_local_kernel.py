#!/usr/bin/env python3
"""Independent exact finite enumeration of the proposed local greedy kernel."""
from itertools import permutations,combinations
from functools import lru_cache
from collections import defaultdict
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def avoids213(p):return not any(p[b]<p[a]<p[c] for a,b,c in combinations(range(len(p)),3))
def avoids1324(p):return not any(p[a]<p[c]<p[b]<p[d] for a,b,c,d in combinations(range(len(p)),4))
def S(p):
 n=len(p);inv=[0]*n
 for i,v in enumerate(p,1):inv[v-1]=i
 return tuple(n+1-v for v in inv[::-1])
@lru_cache(None)
def kernel(top,normbottom):
 a=len(top);b=len(normbottom);bottom=S(normbottom);total=0
 for topinds in combinations(range(a+b),a):
  ts=set(topinds);botinds=[i for i in range(a+b) if i not in ts];p=[None]*(a+b)
  for i,v in zip(topinds,top):p[i]=b+v
  for i,v in zip(botinds,bottom):p[i]=v
  e=p.index(b)
  if not any(i<e<j and p[i]<p[j] for i,j in combinations(topinds,2)):continue
  if avoids1324(p):total+=1
 return total

N=8;states={n:[p for p in permutations(range(1,n+1)) if avoids213(p)] for n in range(1,N+1)}
dp=[defaultdict(int) for _ in range(N+1)]
for n in range(1,N+1):
 for p in states[n]:dp[n][p]+=1
for n in range(1,N):
 for top,count in list(dp[n].items()):
  for b in range(1,N-n+1):
   for bottom in states[b]:
    k=kernel(top,bottom)
    if k:dp[n+b][bottom]+=count*k
expected=[1,1,2,6,23,103,513,2762,15793]
rows=[]
for n in range(1,N+1):
 got=sum(dp[n].values())
 brute=sum(avoids1324(p) for p in permutations(range(1,n+1)))
 if got!=brute or got!=expected[n]:raise RuntimeError(('kernel count mismatch',n,got,brute,expected[n]))
 rows.append({'n':n,'single_cell_states':len(states[n]),'kernel_chain_count':got,'direct_1324_count':brute})
result={'scope':'Finite diagnostic only; no asymptotic or tail conclusion','kernel_definition':'Vertical shuffles of top Av213 and S(normalized bottom), requiring1324 avoidance and max bottom witnessing213 with top','verified_counts':rows,'kernel_pairs_evaluated':kernel.cache_info().currsize,'all_checks_passed':True}
(P/'PAIR_LOCAL_KERNEL_FINITE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
