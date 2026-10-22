from pathlib import Path
"""Produce an integer-only deletion branching certificate, then independently check it."""
import itertools,json,gzip,sys

def require(condition, message="Certificate validation failed"):
 if not condition: raise ValueError(message)
from exact_finite_search import instance

def produce(d,n,K):
 points,edges=instance(d,n); target=n**d-K; nodes={}
 def rec(D):
  key=str(D)
  if key in nodes:return key
  unmet=[e for e in edges if not e&D]; packing=[]; occupied=0
  for e in unmet:
   if not e&occupied: packing.append(e);occupied|=e
  if D.bit_count()+len(packing)>=target:
   nodes[key]={'packing':packing};return key
  require(bool(unmet),'Claimed upper bound is false')
  freq={i:sum(bool(e>>i&1) for e in unmet) for i in range(len(points))}
  edge=min(unmet,key=lambda e:(e.bit_count(),-sum(freq[i] for i in freq if e>>i&1)))
  children=[rec(D|(1<<i)) for i in freq if edge>>i&1]
  nodes[key]={'edge':edge,'children':children};return key
 rec(0)
 return dict(d=d,n=n,K=K,nodes=nodes)

def check(c):
 d,n,K=c['d'],c['n'],c['K']; p=list(itertools.product(range(1,n+1),repeat=d)); index={v:i for i,v in enumerate(p)}
 # Independently reconstruct all x+y=z constraints, including x=y.
 forbidden=set()
 for a in p:
  for b in p:
   z=tuple(a[j]+b[j] for j in range(d))
   if z in index: forbidden.add(sum(1<<i for i in {index[a],index[b],index[z]}))
 seen=set()
 def visit(key):
  if key in seen:return
  seen.add(key);D=int(key);node=c['nodes'][key]
  require(D>=0 and D < (1<<len(p)))
  if 'packing' in node:
   occupied=D
   for e in node['packing']:
    require(e in forbidden and not occupied&e)
    occupied|=e
   require(D.bit_count()+len(node['packing'])>=len(p)-K)
  else:
   e=node['edge'];require(e in forbidden and not D&e)
   expected={str(D|1<<i) for i in range(len(p)) if e>>i&1}
   require(set(node['children'])==expected)
   for child in expected:visit(child)
 visit('0')
 # Lower bound is independently recounted from an actual sum-free slice.
 counts=[sum(t<=sum(x)<2*t for x in p) for t in range(1,d*n+1)]
 require(max(counts)==K)
 return len(seen)
if __name__=='__main__':
 for spec in sys.argv[1:]:
  d,n,K=map(int,spec.split(','));c=produce(d,n,K);num=check(c)
  path=Path(__file__).with_name(f'finite_certificate_d{d}_n{n}.json.gz')
  with gzip.open(path,'wt') as f:json.dump(c,f,separators=(',',':'))
  with gzip.open(path,'rt') as f:require(check(json.load(f))==num)
  print(d,n,K,num,path,flush=True)
