#!/usr/bin/env python3
"""Separate exploratory binary-dihedral complex 2D determinant family."""
from pathlib import Path
from itertools import product
import json
from dihedral_determinant import add,det
from dihedral_partition_bounds import parts,possible,lattice
from check_dihedral_torsion import cyclo,powers
PAIRS=((3,2),(20,14),(119,84))
def matrix(types):
 j0=types.index(1);others=[i for i in range(3) if i!=j0];phases=[(0,0)]*3
 for j,k in enumerate(others):phases[k]=tuple(int(i==j) for i in range(2))
 a=[[{} for _ in range(6)] for _ in range(6)]
 def ins(r,c,e,v):a[r][c]=add(a[r][c],{e:v})
 for i,((p,q),refl,phase) in enumerate(zip(PAIRS,types,phases)):
  neg=tuple(-x for x in phase)
  if refl:
   ins(2*i,1,phase,p);ins(2*i,2,(0,0),-q);ins(2*i,5,phase,1);ins(2*i,4,(0,0),-1)
   ins(2*i+1,0,neg,-p);ins(2*i+1,3,(0,0),-q);ins(2*i+1,4,neg,-1);ins(2*i+1,5,(0,0),-1)
  else:
   ins(2*i,0,phase,p);ins(2*i,2,(0,0),-q);ins(2*i,4,phase,1);ins(2*i,4,(0,0),-1)
   ins(2*i+1,1,neg,p);ins(2*i+1,3,(0,0),-q);ins(2*i+1,5,neg,1);ins(2*i+1,5,(0,0),-1)
 return a

def run():
 out=[]
 for ts in product((0,1),repeat=3):
  if not any(ts):continue
  d=det(matrix(ts));terms=[{'exponent':e,'coefficient':v} for e,v in sorted(d.items())]
  survivor=0;indices=set();low=[]
  for part in parts(list(range(len(terms)))):
   if not all(possible(b,terms) for b in part):continue
   survivor+=1;r,index=lattice(part,terms)
   if r<2:low.append(part)
   else:indices.add(index)
  row={'types':ts,'terms':terms,'partition_survivors':survivor,'full_rank_indices':sorted(indices),'low_rank_partitions':low};out.append(row)
  print(ts,'terms',len(terms),'partitions',survivor,'indices',indices,'low',len(low),flush=True)
 Path(__file__).with_name('quaternionic_probe_results.json').write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
