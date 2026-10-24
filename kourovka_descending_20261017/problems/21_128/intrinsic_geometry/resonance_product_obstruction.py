#!/usr/bin/env python3
"""Three local resonant subspaces with pairwise nonzero cross products.
Certificate is in degree-two Orlik--Solomon algebra, with exact integer arithmetic.
"""
from pathlib import Path
from itertools import combinations, product
import json, argparse

def vector(N,i,j):
 v=[0]*N;v[i]=1;v[j]=-1;return v

def cup(a,b,flats):
 out=[]
 for f in flats:
  s=f['members'];A=sum(a[i] for i in s);B=sum(b[i] for i in s)
  for j in s[1:]:
   c=A*b[j]-B*a[j]
   if c:out.append({'flat':s,'anchor':s[0],'basis_mirror':j,'coefficient':c})
 return out

def find(d):
 N=len(d['hyperplanes']);flats=d['rank2_flats'];locals=[f['members'] for f in flats if len(f['members'])>=3]
 for ss in combinations(locals,3):
  witnesses=[]
  for i,j in combinations(range(3),2):
   s,t=ss[i],ss[j];found=None
   for u in s[1:]:
    for v in t[1:]:
     a=vector(N,s[0],u);b=vector(N,t[0],v);c=cup(a,b,flats)
     if c:found={'subspace_pair':[i,j],'left_vector':a,'right_vector':b,'nonzero_cup_coordinate':c[0]};break
    if found:break
   if found is None:break
   witnesses.append(found)
  if len(witnesses)==3:
   # Every pair of basis vectors within each local sum-zero space has zero cup.
   for s in ss:
    vs=[vector(N,s[0],u) for u in s[1:]]
    assert all(not cup(a,b,flats) for a,b in product(vs,repeat=2))
   return {'ambient_type':d['ambient_type'],'planes':N,'local_subspaces':list(ss),'dimensions':[len(s)-1 for s in ss], 'cross_cup_witnesses':witnesses,'all_local_basis_cups_zero':True}
 raise RuntimeError('No triangle found')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',default=str(Path(__file__).with_name('restriction_certificate.json')));p.add_argument('--output',required=True);args=p.parse_args();out=[find(d) for d in json.loads(Path(args.input).read_text())];Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
