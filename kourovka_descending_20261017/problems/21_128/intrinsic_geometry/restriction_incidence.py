#!/usr/bin/env python3
"""Exact incidence of the arrangement restricted to a selected mirror."""
import arrangement_incidence as a
from itertools import combinations
from collections import Counter
from pathlib import Path
import json, argparse

def dot(v,w):
 t=a.Z
 for x,y in zip(v,w):t=a.add(t,a.mul(x,y))
 return t

def census(typ):
 r=a.roots(typ);h=r[0];p=next(i for i,x in enumerate(h) if x!=a.Z)
 basis=[]
 for j in range(4):
  if j==p:continue
  v=[a.Z]*4;v[j]=a.ONE;v[p]=a.neg(a.div(h[j],h[p]));basis.append(tuple(v))
 rr=set()
 for v in r:
  w=tuple(dot(v,b) for b in basis)
  if any(x!=a.Z for x in w):rr.add(a.norm(w))
 rr=sorted(rr);flats={}
 for i,j in combinations(range(len(rr)),2):
  w=tuple(a.sub(a.mul(rr[i][k],rr[j][l]),a.mul(rr[i][l],rr[j][k])) for k,l in combinations(range(3),2))
  flats.setdefault(a.norm(w),set()).update((i,j))
 counts=Counter(len(s) for s in flats.values());N=len(rr);b2=sum((m-1)*c for m,c in counts.items());b3=1-N+b2
 return {'ambient_type':typ,'selected_mirror_normal':a.encode(h),'mirror_basis':[a.encode(v) for v in basis], 'hyperplanes':[a.encode(v) for v in rr], 'rank2_flats':[{'members':sorted(s),'wedge':a.encode(w)} for w,s in sorted(flats.items())], 'rank2_multiplicity_counts':dict(sorted(counts.items())), 'central_betti':[1,N,b2,b3], 'projective_betti':[1,N-1,b3], 'projective_euler':1-(N-1)+b3}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();out=[census(t) for t in ('F4','H4')];Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
 for v in out:print(v['ambient_type'],len(v['hyperplanes']),v['rank2_multiplicity_counts'],v['central_betti'],v['projective_euler'])
