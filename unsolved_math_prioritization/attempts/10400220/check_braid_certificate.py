#!/usr/bin/env python3
"""Exact separate verifier for the saved three-change certificate."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent
x=json.loads((p/'braid_upper_certificate.json').read_text());count=0

def ck(t):
 global count
 assert t
 count+=1

def reduce(w):
 out=[]
 for a in w:
  if out and out[-1]==-a:out.pop()
  else:out.append(a)
 return tuple(out)

def inv(w):return tuple(-a for a in w[::-1])

def substitute(w,images):
 return reduce(a for k in w for a in (images[k-1] if k>0 else inv(images[-k-1])))

def artin_action(n,w):
 images=tuple((i+1,) for i in range(n))
 for a in w:
  i=abs(a)-1;gen=[(j+1,) for j in range(n)]
  if a>0:gen[i]=(i+1,i+2,-i-1);gen[i+1]=(i+1,)
  else:gen[i]=(i+2,);gen[i+1]=(-i-2,i+1,i+2)
  images=tuple(substitute(v,gen) for v in images)
 return images

cert=x['certificate'];W=x['source_word'];changes=cert['changes_zero_based'];ck(len(set(changes))==3)
initial=[x['strand_count'],[-a if i in changes else a for i,a in enumerate(W)]];ck(initial==cert['initial'])
state=initial
for step in cert['moves']:
 ck(step['before']==state);n,w=state;nn,v=step['after'];op=step['move']
 ck(all(0<abs(a)<n for a in w));ck(all(0<abs(a)<nn for a in v))
 if op[0]=='destabilize_end':
  _,end,i=op;ck(end in (1,n-1));ck(nn==n-1 and sum(abs(a)==end for a in w)==1 and abs(w[i])==end)
  expect=w[:i]+w[i+1:]
  if end==1:expect=[(1 if a>0 else -1)*(abs(a)-1) for a in expect]
  ck(v==expect)
 elif op[0]=='cyclic_left':ck(nn==n and v==w[1:]+w[:1])
 else:
  ck(nn==n);ck(artin_action(n,w)==artin_action(n,v))
 state=step['after']
ck(state==[1,[]])
# Generator/inverse and all local rewrite identities used by the search, tested
# independently by Artin's free-group action rather than the search's rewrite function.
for n in range(2,7):
 identity=artin_action(n,[])
 for i in range(1,n):
  ck(artin_action(n,[i,-i])==identity)
  ck(artin_action(n,[-i,i])==identity)
 for i in range(1,n-1):
  for sign in (-1,1):
   a,b=sign*i,sign*(i+1)
   for a,b in [(a,b),(b,a)]:
    ck(artin_action(n,[a,b,a])==artin_action(n,[b,a,b]))
    ck(artin_action(n,[a,b,-a])==artin_action(n,[-b,a,b]))
print(json.dumps({'status':'PASS','exact_assertions':count,'crossing_changes':3,'isotopy_moves':len(cert['moves']),'final_braid':[1,[]],'scope':'An exact upper certificate for the specified source braid closure. The database label is sourced separately; no u>=3 or mutation gap is claimed.'},indent=2))
