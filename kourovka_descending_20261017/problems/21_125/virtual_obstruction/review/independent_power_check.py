#!/usr/bin/env python3
"""Signed-word reproduction of powered second-Engel failure."""
import json
from pathlib import Path

def reduce(word):
 stack=[]
 for letter in word:
  if stack and stack[-1]==-letter:stack.pop()
  else:stack.append(letter)
 return stack

def inverse(w):return [-x for x in w[::-1]]
def image(w,q):
 out=[]
 for x in w:
  base=[1] if abs(x)==1 else [2]+[1]*q
  out+=base if x>0 else inverse(base)
 return reduce(out)

out=[]
for p in range(1,26):
 for q in range(1,26):
  c=reduce([-2]*p+image([2]*p,q))
  transformed=image(c,q)
  second=reduce(inverse(c)+transformed)
  assert bool(second)==(p>1)
  if p>1:assert c[0]==-2 and transformed[0]==-1
  out.append({'p':p,'q':q,'length_second_engel':len(second)})
Path(__file__).with_name('independent_power_results.json').write_text(json.dumps({'pairs':625,'result':'PASS','checks':out},indent=2)+'\n')
print('PASS625')
