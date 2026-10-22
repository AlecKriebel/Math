#!/usr/bin/env python3
"""Independent consumer of every deterministic ideal-seed derivation.
The supplied checker supplies trace candidates only. None of its arithmetic is
used by this consumer; literal group/linear formulas are recomputed below.
All guards are explicit and survive optimization. Run from this folder.
"""
from pathlib import Path
import copy, hashlib, importlib.util, itertools, json
A=Path(__file__).resolve().parent
E=A/'tmp/extracted/audit/reviews/finite_01'
def need(v,msg):
 if not v:raise ValueError(msg)
def coeff(r):return [(r//5**j)%5 for j in range(4)]
def encode(r):return sum((r[j]%5)*5**j for j in range(4))
def rp(a,b):return encode([x+y for x,y in zip(coeff(a),coeff(b))])
def rm(a,b):
 c=[0]*4
 for i,x in enumerate(coeff(a),1):
  for j,y in enumerate(coeff(b),1):
   if i+j<=4:c[i+j-1]+=x*y
 return encode(c)
def rs(n,a):return encode([n*c for c in coeff(a)])
def plus(a,b):return (rp(a[0],b[0]),a[1]^b[1],a[2]^b[2])
def minus(a,b):return plus(a,(rs(-1,b[0]),b[1],b[2]))
def rotate(w,s):
 s%=5
 return ((w<<s)|(w>>(5-s)))&31
def circle(a,b):
 r,v,z=a;u,w,Z=b
 e=z^((v.bit_count()//2)%2)
 h=encode([(-1)**(j+1)*c for j,c in enumerate(coeff(u))]) if e else u
 r2=rm(r,r);r3=rm(r2,r);r4=rm(r3,r)
 ell=rp(rp(r,rs(2,r2)),rp(rs(2,r3),r4))
 s=coeff(ell)[3]; mw=rotate(w,s)
 return (rp(rp(r,h),rm(r,h)),v^mw,z^Z^((v&mw).bit_count()%2))
def star(a,b):return minus(minus(circle(a,b),a),b)
V=tuple(v for v in range(32) if v.bit_count()%2==0)
BASIS=tuple((5**j,0,0) for j in range(4))+tuple((0,v,0) for v in (17,18,20,24))+((0,0,1),)
step_total=0
def consume(seed,records):
 global step_total
 need(records[0]==['seed',list(seed)],'seed mismatch')
 known=[seed]
 for record in records[1:]:
  kind,refs,actor,out=record
  need(len(refs)==1 and isinstance(refs[0],int) and 0<=refs[0]<len(known),'invalid prior reference')
  i=known[refs[0]]
  if kind=='integer_multiple':
   need(isinstance(actor,int) and actor>=0,'invalid scalar')
   value=(0,0,0)
   for _ in range(actor):value=plus(value,i)
  elif kind=='lambda_difference':value=star(tuple(actor),i)
  elif kind=='star':value=star(i,tuple(actor))
  else:raise ValueError('invalid inference')
  need(value==tuple(out),'incorrect mathematical inference')
  known.append(value);step_total+=1
 need(set(BASIS)<=set(known),'generators not derived')
 return True
receipts=[json.loads(line) for line in (E/'ideal_seed_derivations.jsonl').read_text().splitlines()]
expected={(r,v,z) for r,v,z in itertools.product(range(625),V,range(2))}-{(0,0,0)}
seeds=[tuple(row['seed']) for row in receipts]
need(len(seeds)==19999 and len(set(seeds))==19999 and set(seeds)==expected,'receipt seed coverage')
loader=importlib.util.spec_from_file_location('frozen_trace_supplier',E/'check.py')
mod=importlib.util.module_from_spec(loader);loader.loader.exec_module(mod);mod.setup()
stream=hashlib.sha256()
for row in receipts:
 seed=tuple(row['seed']);trace=mod.replay_one(seed);records=trace['records']
 raw=json.dumps(records,separators=(',',':')).encode()
 need(hashlib.sha256(raw).hexdigest()==row['trace_sha256'],'stored trace commitment mismatch')
 need(len(records)-1==row['steps'],'step count mismatch')
 consume(seed,records)
 stream.update(raw+b'\n')
# Adversarial consumer checks: these corruptions must each be rejected.
sample=mod.replay_one((1,3,1))['records']
controls=[]
for name in ('future_reference','falsified_output','changed_actor'):
 bad=copy.deepcopy(sample)
 if name=='future_reference':bad[1][1]=[999]
 elif name=='falsified_output':bad[1][-1][0]=(bad[1][-1][0]+1)%625
 else:
  idx=next(i for i,rec in enumerate(bad[1:],1) if rec[0]=='star')
  bad[idx][2]=[0,0,0]
 try:consume((1,3,1),bad)
 except ValueError as err:controls.append({'mutation':name,'rejected':True,'reason':str(err)})
 else:raise ValueError('mutation accepted '+name)
result={'status':'PASS','seeds':len(seeds),'independently_checked_derivation_steps':sum(row['steps'] for row in receipts),'all_seed_receipt_hashes_rederived':True,'all_traces_independently_consumed':True,'all_nine_generators_derived_per_seed':True,'trace_stream_sha256':stream.hexdigest(),'negative_controls':controls,'scope':'Independent arithmetic verifies supplied traces; quotient/ideal closure inference remains a proved mathematical implication, not software evidence.'}
(A/'INDEPENDENT_SEED_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
