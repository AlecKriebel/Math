"""Nonsearch independent verifier of the order<=15 witness certificates.
Uses coordinate tuples, rather than searcher's addition tables/color bitsets.
All checks remain active in optimized Python.
"""
from pathlib import Path
from math import prod,comb
import json,hashlib,datetime
P=Path(__file__).resolve().parents[1]
GROUPS={'C3':(3,),'C5':(5,),'C7':(7,),'C9':(9,), 'C3xC3':(3,3),'C11':(11,),'C13':(13,),'C15':(15,)}
def require(cond,msg):
 if not cond:raise ValueError(msg)
def decode(x,mods):
 out=[]
 for m in mods:out.append(x%m);x//=m
 require(x==0,'out of group range')
 return tuple(out)
def audit():
 reports=[]
 for name,mods in GROUPS.items():
  q=prod(mods);path=P/'finite_search/exhaustive_order15'/f'{name}.jsonl'
  rows=path.read_text().splitlines();header=json.loads(rows[0])
  require(tuple(header['moduli'])==mods and header['order']==q,'header mismatch')
  seen=set();by_size={}
  for line in rows[1:]:
   row=json.loads(line);mask=row['mask'];c=row['cycle'];n=len(c)
   require(type(mask)is int and 0<=mask<2**q and mask&1,'invalid mask')
   require(mask not in seen,'duplicate subset');seen.add(mask)
   want={x for x in range(q) if mask>>x&1}
   require(n==len(want)>2 and set(c)==want and len(set(c))==n,'not a vertex permutation')
   require(c[0]==0 and all(type(x)is int for x in c),'invalid vertex')
   coords=[decode(x,mods) for x in c]
   sums=[tuple((a+b)%m for a,b,m in zip(coords[i],coords[(i+1)%n],mods)) for i in range(n)]
   require(len(set(sums))==n,'repeated adjacent sum')
   by_size[n]=by_size.get(n,0)+1
  want_masks={mask for mask in range(1,2**q,2) if mask.bit_count()>2}
  require(seen==want_masks,'incomplete subset coverage')
  require(all(by_size[n]==comb(q-1,n-1) for n in range(3,q+1)),'wrong size distribution')
  reports.append({'group':name,'moduli':mods,'all_normalized_subsets_checked':len(seen),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 trap=json.loads((P/'switching/local_landscape_result.json').read_text())['strict_improvement_trap']
 c=trap['cycle'];n=len(c)
 def score(d):return len({(d[i]+d[(i+1)%n])%7 for i in range(n)})
 moves=[]
 # Independently construct cyclic 2-opt paths by cutting each pair of disjoint edges.
 for i in range(n):
  for j in range(i+1,n):
   if (j-i)%n in (1,n-1):continue
   d=c[:i+1]+list(reversed(c[i+1:j+1]))+c[j+1:]
   moves.append(d)
 require(len(moves)==n*(n-3)//2==9,'incorrect neighbor count')
 require(score(c)==5 and all(score(d)<=5 for d in moves),'not an improvement trap')
 require(set(trap['rainbow_witness'])==set(c) and score(trap['rainbow_witness'])==n,'invalid rainbow witness')
 return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verifier':'independent tuple arithmetic, no search imports','passed':True,'groups':reports,'total_certificate_witnesses':sum(x['all_normalized_subsets_checked'] for x in reports),'strict_2opt_trap_all_nine_moves_verified':True,'scope':'Every subset of each odd abelian group of order<=15, via translation. No assertion for larger groups.'}
if __name__=='__main__':
 r=audit();Path(__file__).with_name('root_certificate_audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
