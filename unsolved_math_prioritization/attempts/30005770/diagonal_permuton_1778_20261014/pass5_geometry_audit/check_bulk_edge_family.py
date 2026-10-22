#!/usr/bin/env python3
"""Independent all-shuffle diagnostics for the internal bulk-edge family."""
from itertools import combinations
from pathlib import Path
from math import comb
import json
P=Path(__file__).resolve().parent

def avoids1324(p):return not any(p[a]<p[c]<p[b]<p[d] for a,b,c,d in combinations(range(len(p)),4))
rows=[]
for n in range(4,11):
 for p in range(2,n-1):
  q=n-p
  A=(1,)+tuple(range(p,1,-1));B=tuple(range(q-1,0,-1))+(q,)
  count=cross=words=0
  for U in combinations(range(n),p):
   us=set(U);word=tuple(i in us for i in range(n));ui=li=0;v=[]
   for isupper in word:
    if isupper:v.append(q+A[ui]);ui+=1
    else:v.append(B[li]);li+=1
   lowermax=v.index(q)
   greedy=any(v[i]<v[j] for i in range(lowermax) for j in range(lowermax+1,n) if word[i] and word[j])
   valid=greedy and avoids1324(v)
   if valid!=(word[0] and word[-1]):raise RuntimeError(('word characterization',p,q,word,v))
   words+=1
   if valid:
    count+=1;cross+=sum(1 for i in range(n) for j in range(i+1,n) if not word[i] and word[j])
  if count!=comb(n-2,q) or 2*cross!=p*q*count:raise RuntimeError(('count or mean',p,q,count,cross))
  rows.append({'p':p,'q':q,'all_words_checked':words,'K':count,'K_inc':cross})
r={'scope':'Finite diagnostics only; the all-size proof uses the exact word characterization','all_checks_passed':True,'checks':rows}
(P/'BULK_EDGE_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'state_pairs':len(rows),'all_words_checked':sum(x['all_words_checked'] for x in rows),'all_checks_passed':True}))
