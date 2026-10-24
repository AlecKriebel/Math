#!/usr/bin/env python3
"""Necessary minimal-block partition tests and exponent-lattice ranks."""
from pathlib import Path
from math import gcd
from itertools import combinations
import json

def parts(items):
 if not items:yield [];return
 first,*rest=items
 for p in parts(rest):
  yield [[first]]+[b[:] for b in p]
  for i in range(len(p)):
   out=[b[:] for b in p];out[i]=[first]+out[i];yield out

def possible(block,terms):
 cs=[abs(terms[i]['coefficient']) for i in block];n=len(cs)
 if n<2:return False
 if max(cs)>sum(cs)-max(cs):return False
 if n==2:return cs[0]==cs[1]
 if n==3:return len(set(cs))==1 or 2*max(cs)==sum(cs)
 return True

def lattice(blocks,terms):
 ds=[]
 for b in blocks:
  e=terms[b[0]]['exponent']
  ds.extend(tuple(x-y for x,y in zip(terms[i]['exponent'],e)) for i in b[1:])
 minors=[abs(a[0]*b[1]-a[1]*b[0]) for a,b in combinations(ds,2)]
 nonzero=[x for x in minors if x]
 if not nonzero:return (1 if any(any(x) for x in ds) else 0),0
 d=0
 for x in nonzero:d=gcd(d,x)
 return 2,d

def run():
 out=[]
 for row in json.loads(Path(__file__).with_name('dihedral_determinants.json').read_text()):
  terms=row['terms'];counts={};ranklow=[];ds=set();survivors=0
  for p in parts(list(range(len(terms)))):
   if not all(possible(b,terms) for b in p):continue
   survivors+=1;r,d=lattice(p,terms);counts[str((r,d))]=counts.get(str((r,d)),0)+1
   if r<2:ranklow.append(p)
   else:ds.add(d)
  out.append({'types':row['types'],'necessary_partition_survivors':survivors,'rank_index_counts':counts,'rank_low_partitions':ranklow,'possible_fullrank_indices':sorted(ds)})
 return out
if __name__=='__main__':
 out=run();Path(__file__).with_name('dihedral_partition_bounds.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
