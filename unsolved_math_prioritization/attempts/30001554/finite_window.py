import json,hashlib
from itertools import chain

def search(t):
 n=3*t; nodes=[0]*(n+1); leaves=0; bad=[]; w=[];th=[];types=[]; digest=hashlib.sha256(); nonperiodic=[0]*(n+1)
 def extend(a):
  w.append(a);m=len(w)
  ok=True
  for l in range(t+1,m+1):
   i=m-l
   if not any(all(w[m-k+j]==th[w[i+j]] for j in range(k)) for k in range(1,l)):
    ok=False;break
  if ok:go()
  w.pop()
 def go():
  nonlocal leaves
  m=len(w);nodes[m]+=1
  if m>=t and not any(all(w[i+p]==th[w[i]] for i in range(m-p)) for p in range(1,t+1)):nonperiodic[m]+=1
  if m==n:
   leaves+=1
   digest.update((json.dumps([types,w],separators=(',',':'))+'\n').encode())
   p=next(p for p in range(1,n+1) if all(w[i+p]==th[w[i]] for i in range(n-p)))
   if p>t:bad.append(dict(w=w.copy(),theta=th.copy(),p=p));print('BAD',bad[-1],flush=True);raise RuntimeError
   return
  for j,ispaired in enumerate(types):
   extend(2*j)
   if ispaired:extend(2*j+1)
  if m<t:
   j=len(types);types.append(False);th.extend((2*j,2*j+1));extend(2*j);th[-2:]=[2*j+1,2*j];types[-1]=True;extend(2*j);th[-2:]=[];types.pop()
 go();return dict(t=t,length=n,nodes=nodes,leaves=leaves,bad=bad,nonperiodic_by_length=nonperiodic,leaf_sha256=digest.hexdigest())
if __name__=="__main__":
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument("--max-t",type=int,default=6);a=ap.parse_args()
 print(json.dumps([search(t) for t in range(1,a.max_t+1)],indent=2,sort_keys=True))
