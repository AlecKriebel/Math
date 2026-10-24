#!/usr/bin/env python3
"""Finite candidate-word visibility, exact; no universal invisibility conclusion."""
from check_iterated_covers import analyze
from fractions import Fraction as Q
from pathlib import Path
import argparse,json

def inv(w): return [-x for x in w[::-1]]
def comm(u,v): return u+v+inv(u)+inv(v)

p=argparse.ArgumentParser(); p.add_argument('--input',type=Path,required=True); p.add_argument('--output',type=Path,required=True); args=p.parse_args()
source=json.loads(args.input.read_text()); frozen=source['found']['result']; m=frozen['m']; perms=frozen['permutations']; q=len(perms[0]); r=frozen['stable_letter_power']
analysis=analyze(m,perms,r,characters=True)
chars=[{int(k):Q(v) for k,v in d.items()} for d in analysis['invariant_characters']]
ind={tuple(e):j for j,e in enumerate(analysis['basis_edges'])}
inverse=[]
for perm in perms:
 back=[0]*q
 for x,y in enumerate(perm): back[y]=x
 inverse.append(back)
def walk(word,start=0):
 v=start; chain={}
 for x in word:
  if x>0: i=x-1; edge=(v,i); sign=1; v=perms[i][v]
  else: i=-x-1; v=inverse[i][v]; edge=(v,i); sign=-1
  j=ind.get(edge)
  if j is not None: chain[j]=chain.get(j,0)+sign
 return v,chain
candidates=[('a'+str(i),[i]) for i in range(1,m+1)]
for i in range(1,m+1):
 for j in range(i+1,m+1): candidates.append(('[a'+str(i)+',a'+str(j)+']',comm([i],[j])))
u=[1]
for i in range(2,m+1):
 u=comm(u,[i]); candidates.append(('left_nested_through_a'+str(i),u))
results=[]
for label,w in candidates:
 v,chain=walk(w); power=1
 while v:
  v,increment=walk(w,v); power+=1
  for j,n in increment.items(): chain[j]=chain.get(j,0)+n
  assert power<=q
 values=[sum(n*ell.get(j,0) for j,n in chain.items()) for ell in chars]
 nonzero=next((j for j,x in enumerate(values) if x),None)
 results.append({'label':label,'word':w,'power_closing_in_fiber_cover':power,'visible':nonzero is not None,'character_index':nonzero,'character_value':None if nonzero is None else str(values[nonzero])})
args.output.write_text(json.dumps({'scope':'Only this single explicit finite-index subgroup; zero means no rational character of this subgroup detects the specified power, not every finite-index subgroup','m':m,'index':analysis['subgroup_index'],'H1_dimension':analysis['H1_subgroup_Q_dimension'],'results':results},indent=2)+'\n')
print(json.dumps(results))
