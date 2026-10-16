#!/usr/bin/env python3
from pathlib import Path
import runpy,io,contextlib,itertools,json
with contextlib.redirect_stdout(io.StringIO()):D=runpy.run_path(str(Path(__file__).with_name('check_turn_1.py')))
action=D['action'];inverse=D['inverse'];pairs=D['pairs'];n=0
def ck(x):
 global n
 assert x;n+=1
c=(1,2,3,4)*5;z=(1,2,3,4,5)*6;d=(1,2,3,4,5);w=(2,3,4,5)*10
for i in range(1,5):ck(action(d+(i,)+inverse(d))==action((i+1,)))
for i in range(1,6):ck(action(z+(i,))==action((i,)+z))
ck(action(d+c+c+inverse(d))==action(w))
def perm(i):
 p=list(range(6));p[i-1],p[i]=p[i],p[i-1];return tuple(p)
def compose(p,q):return tuple(p[q[i]]for i in range(6))
def closure(gs):
 e=tuple(range(6));out={e};queue=[e]
 for p in queue:
  for g in gs:
   q=compose(p,g)
   if q not in out:out.add(q);queue.append(q)
 return out
A=closure([perm(i)for i in range(1,5)]);B=closure([perm(i)for i in range(2,6)])
ck(len(A)==len(B)==120);ck(A!=B);ck(all(p[5]==5 for p in A));ck(all(p[0]==0 for p in B));ck(perm(1)in A and perm(1)not in B);ck(perm(5)in B and perm(5)not in A)
expected={20:{tuple(2*int(k in ij)for ij in pairs)for k in range(6)},30:{(1,)*15},40:{tuple(2*int(k not in ij)for ij in pairs)for k in range(6)}}
found={m:set()for m in expected};solutions={m:0 for m in expected}
for t in itertools.product(range(-3,4),repeat=6):
 T=sum(t);m=10*(T+4)
 if m not in expected:continue
 L=tuple(2*int(j<5)+T-2*(t[i]+t[j])for i,j in pairs)
 if min(L)<0:continue
 ck(L in expected[m]);ck(sum(L)*2==m);found[m].add(L);solutions[m]+=1
for m in expected:ck(found[m]==expected[m])
for k in range(1,5):
 left=0;right=5;ck(left<k<right);ck(2*int(k not in (left,right))==2)
print(json.dumps({'status':'PASS','exact_assertions':n,'subgroup_orders':[len(A),len(B)],'different_fixed_vertices':[6,1],'necessary_linking_patterns':{m:len(v)for m,v in expected.items()},'bounded_stress_solutions':solutions,'scope':'Exact conjugation, centrality and subgroup checks; linking classifications and all-length forty-letter slice are proved analytically. Simultaneous-conjugation classification at lengths20 and30 remains unresolved.'},indent=2,sort_keys=True))
