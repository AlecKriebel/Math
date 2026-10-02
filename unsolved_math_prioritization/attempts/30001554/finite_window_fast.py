"""Exact incremental negative-period masks, canonical orbit generation, uncapped.
No import of finite_window.py. --t chooses one tau bound.
"""
from hashlib import sha256
import json,argparse

def search(t):
 n=3*t;nodes=[0]*(n+1);nonperiodic=[0]*(n+1);leaves=0;digest=sha256();w=[];th=[];types=[];low=(1<<(t+1))-2
 def go(masks):
  nonlocal leaves
  m=len(w);nodes[m]+=1
  if m>=t and not masks[0]&low:nonperiodic[m]+=1
  if m==n:
   assert masks[0]&low
   leaves+=1;digest.update((json.dumps([types,w],separators=(',',':'))+'\n').encode());return
  def extend(a):
   match=0
   for j,x in enumerate(w):
    if th[x]==a:match|=1<<(m-j)
   updated=[]
   for i,old in enumerate(masks):
    length=m-i+1;proper=old&match
    if length>t and not proper:return
    updated.append(proper|(1<<length))
   updated.append(2);w.append(a);go(updated);w.pop()
  for j,paired in enumerate(types):
   extend(2*j)
   if paired:extend(2*j+1)
  if m<t:
   j=len(types);types.append(False);th.extend([2*j,2*j+1]);extend(2*j)
   types[-1]=True;th[-2:]=[2*j+1,2*j];extend(2*j);types.pop();del th[-2:]
 go([])
 return dict(t=t,length=n,nodes=nodes,leaves=leaves,bad=[],nonperiodic_by_length=nonperiodic,leaf_sha256=digest.hexdigest())
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--t',type=int,default=8);a=ap.parse_args();print(json.dumps(search(a.t),indent=2,sort_keys=True))
