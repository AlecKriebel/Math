#!/usr/bin/env python3
"""Exact, standard-library-only replay of the binary grandparent-square certificate."""
import gzip, json, hashlib, sys
from pathlib import Path
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('square_flow_certificate.json.gz')
data=path.read_bytes();c=json.loads(gzip.decompress(data))
def require(ok,message):
 if not ok:raise ValueError(message)
require(c['q']==2 and c['radius']==10,'unexpected graph')
R=c['radius'];words=[()]
for w in words:
 if len(w)<R:
  words.extend(w+(i,) for i in range(3 if not w else 2))
index={w:i for i,w in enumerate(words)}
p={}
for w in words:
 toward=w+(0,) if all(x==0 for x in w) else w[:-1]
 p[w]=toward if toward in index else None
E=set()
for w in words:
 for v in [p[w],p[p[w]] if p[w] is not None else None]:
  if v is not None:E.add(tuple(sorted((index[w],index[v]))))
adj=[set() for w in words]
for a,b in E:adj[a].add(b);adj[b].add(a)
S=set(E)
for ns in adj:
 for a in ns:
  for b in ns:
   if a<b:S.add((a,b))
require(c['vertices']==len(words)==3070,'vertex count')
require(c['edge_order']==[list(e) for e in sorted(S)],'edge list mismatch')
neigh=sorted(b if a==0 else a for a,b in S if a==0 or b==0)
require(c['root_neighbors']==neigh and len(neigh)==40,'root neighborhood')
require(all(len(words[v])<=4 for v in neigh),'root neighbor range')
require(len(c['flows'])==40,'missing unit flow')
D=c['denominator'];require(isinstance(D,int) and D>0,'denominator');nums=[]
for sink,flow in zip(neigh,c['flows']):
 require(len(flow)==len(S),'flow length')
 div=[0]*len(words)
 for (a,b),f in zip(c['edge_order'],flow):
  require(type(f) is int,'noninteger flow')
  div[a]+=f;div[b]-=f
 target=[0]*len(words);target[sink]=D;target[0]=-D
 require(div==target,'unit divergence failure')
 nums.append(sum(f*f for f in flow))
require(nums==c['energy_numerators'],'energy mismatch')
N=sum(nums)
require(c['total_energy_numerator']==N and c['total_energy_denominator']==D*D,'total mismatch')
require(100*N<321*D*D,'upper bound failed')
print(json.dumps({'verdict':'PASS','certificate_sha256':hashlib.sha256(data).hexdigest(),'vertices':len(words),'edges':len(S),'root_neighbors':len(neigh),'energy_numerator':N,'energy_denominator':D*D,'strict_upper_bound':'321/100'},indent=2))
