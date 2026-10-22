#!/usr/bin/env python3
import itertools,json,sys,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'turn1'))
from surface_gluing import surface

def family(bits):
 k=len(bits);arrows=[];rel=set()
 for j,x in enumerate(bits):
  v=4*j;a=5*j;arrows.extend([(v,v+1),(v,v+2),(v+1,v+2),(v+1,v+3),(v+2,v+3)])
  rel|={(a,a+2),(a+(2 if x else 1),a+4)}
 for j in range(k-1):
  z=len(arrows);arrows.append((4*j+3,4*j+4));rel|={(5*j+4,z),(z,5*(j+1)+1)}
 return 4*k,arrows,rel

def ribbon(n,a,r):
 nxt={i:j for i,(u,v) in enumerate(a) for j,(w,z) in enumerate(a) if v==w and (i,j) not in r};prev=set(nxt.values());threads=[]
 for i in range(len(a)):
  if i in prev:continue
  vertices=[a[i][0]];path=[]
  while True:
   path.append(i);vertices.append(a[i][1])
   if i not in nxt:break
   i=nxt[i]
  threads.append((path,vertices))
 occ=collections.defaultdict(list);sigma={};d=0
 for path,vs in threads:
  ds=list(range(d,d+len(vs)));d+=len(vs)
  for i,v in enumerate(vs):occ[v].append(ds[i]);sigma[ds[i]]=ds[(i+1)%len(ds)]
 assert len(occ)==n and all(len(ds)==2 for ds in occ.values())
 alpha={}
 for x,y in occ.values():alpha[x]=y;alpha[y]=x
 phi={i:sigma[alpha[i]] for i in sigma};todo=set(phi);boundaries=[]
 while todo:
  start=min(todo);cur=start;cy=[]
  while cur in todo:todo.remove(cur);cy.append(cur);cur=phi[cur]
  assert cur==start;boundaries.append(cy)
 return {'threads':[{'arrows':p,'vertices':v} for p,v in threads],'boundaries':boundaries,'genus':(2-len(boundaries)-(len(threads)-n))//2,'dimension':n+sum(len(p)*(len(p)+1)//2 for p,v in threads)}
checks=0;tested=0;summ=[]
def ck(x):
 global checks
 assert x;checks+=1
for k in range(1,9):
 counts=collections.Counter()
 for bits in itertools.product((0,1),repeat=k):
  n,a,r=family(bits);rr=ribbon(n,a,r);h=sum(bits);tested+=1
  ck(n==4*k and len(a)==6*k-1);ck(rr['genus']==h);ck(len(rr['boundaries'])==2*k+1-2*h);ck(rr['dimension']==(9*k*k+13*k)//2)
  ck(len(rr['threads'])==2*k+1)
  counts[str(h)]+=1
  if k<=5:
   s=surface(n,a,r);ck((s['genus'],s['boundaries'])==(h,2*k+1-2*h));ck(s['white_punctures']==s['black_punctures']==0)
 summ.append({'k':k,'by_genus':dict(counts)})
print(json.dumps({'assertions':checks,'covers_tested':tested,'summaries':summ,'sample_k2':[{ 'bits':bits,'ribbon':ribbon(*family(bits))} for bits in itertools.product((0,1),repeat=2)],'scope':'Exact controls supplement the proof for every positive integer k.'},indent=2))
