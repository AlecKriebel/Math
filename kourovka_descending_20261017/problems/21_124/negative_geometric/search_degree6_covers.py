#!/usr/bin/env python3
from check_covers import inv,cover
from itertools import permutations
from pathlib import Path
import json,datetime

def mul(p,q):return tuple(p[q[i]] for i in range(len(p)))
def power(p,k):
 q=tuple(range(len(p)))
 for _ in range(k):q=mul(q,p)
 return q

def parts(n,lo=1):
 if not n:yield []
 for i in range(lo,n+1):
  for p in parts(n-i,i):yield [i]+p

def cyc(part):
 out=[];start=0
 for d in part:out.extend(start+(i+1)%d for i in range(d));start+=d
 return tuple(out)

def trans(ps):
 seen={0};todo=[0]
 while todo:
  x=todo.pop()
  for p in ps:
   if p[x] not in seen:seen.add(p[x]);todo.append(p[x])
 return len(seen)==len(ps[0])

def main():
 counts=[];examples=[]
 for k in [3,5]:
  for n in [6]:
   pp=list(permutations(range(n)));one=tuple(range(n));raw=checked=0
   for part in parts(n):
    t=cyc(part);ti=inv(t)
    conj={}
    for b in pp:conj.setdefault(mul(inv(b),mul(t,b)),[]).append(b)
    cent=conj[t]
    if t==one:
     aa=[cyc(pt) for pt in parts(n)]
    else:
     remaining=set(cent);aa=[]
     while remaining:
      a=min(remaining);aa.append(a)
      remaining.difference_update(mul(inv(s),mul(a,s)) for s in cent)
    for a in aa:
     if a==one:continue
     bs=conj.get(mul(t,power(a,k)),[])
     for b in bs:
      w=mul(a,mul(b,mul(inv(a),inv(b))))
      cs=conj.get(mul(t,w),[])
      for c in cs:
       if not trans([a,b,c,t]):continue
       raw+=1
       # Only one c per identical a,b,t? Every c affects homology, so check all.
       r=cover(k,{'a':inv(a),'b':inv(b),'c':inv(c),'t':inv(t)});checked+=1
       if r['a_visible']:
        examples.append({'k':k,'n':n,'left_action':{g:list(p) for g,p in zip('abct',[a,b,c,t])},'homology':r})
        break
      if examples:break
     if examples:break
    if examples:break
   counts.append({'k':k,'degree':n,'transitive_actions_checked':checked})
   if examples:break
  if examples:break
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'canonical t conjugacy types, all a commuting t, all compatible b,c, transitive left permutation actions, a nontrivial; stops at first rational visibility witness','counts':counts,'witnesses':examples}
 Path(__file__).with_name('degree6_cover_search.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
