#!/usr/bin/env python3
"""Standard-library exact identities, elementary interval checks and mutations."""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
from tempfile import TemporaryDirectory
import json,random,sys
sys.dont_write_bytecode=True
import verify_independent as v
root=Path(__file__).resolve().parent
q=6479
u=(-Q(1),Q(0));a=(-Q(289,300),Q(1,300));b=(-Q(161,180),-Q(1,180))
phases=(u,a,b);weights=(Q(1,2),Q(1,3),Q(1,5))
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):return (x[0]*y[0]-q*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(c,x):return (c*x[0],c*x[1])
def conj(x):return (x[0],-x[1])
def summ(ps,ws):
 z=(Q(1),Q(0))
 for p,w in zip(ps,ws):z=add(z,scale(w,p))
 return z
for p in phases:assert mul(p,conj(p))==(1,0)
assert summ(phases,weights)==(0,0)
for perm in permutations(range(3)):
 U,V,W=[phases[j] for j in perm];A,B,C=[weights[j] for j in perm]
 aa=add((1,0),scale(A,U));bb=add((1,0),scale(A,conj(U)))
 residual=add(add(mul(scale(B,bb),mul(V,V)),mul(add(mul(aa,bb),(B*B-C*C,0)),V)),scale(B,aa))
 assert residual==(0,0) and bb!=(0,0)
sign_mutants=[];denominator_mutants=[]
for j in range(3):
 ps=list(phases);ps[j]=scale(-1,ps[j]);r=summ(ps,weights);assert r!=(0,0);sign_mutants.append(list(map(str,r)))
 ws=list(weights);ws[j]=Q(1,(2,3,5)[j]+1);r=summ(phases,ws);assert r!=(0,0);denominator_mutants.append(list(map(str,r)))
det=scale(Q(1,15),mul(conj(a),b))[1];assert det!=0
# Rational endpoint arithmetic tests cover every sign pattern.
rng=random.Random(30003644)
for _ in range(200):
 p=sorted(Q(rng.randrange(-100,101),rng.randrange(1,101)) for _ in range(2))
 r=sorted(Q(rng.randrange(-100,101),rng.randrange(1,101)) for _ in range(2))
 X=v.bounds(*p);Y=v.bounds(*r)
 for Z,values in [(X+Y,[i+j for i in p for j in r]),(X-Y,[i-j for i in p for j in r]),(X*Y,[i*j for i in p for j in r])]:
  assert Q(Z.lo,v.S)<=min(values)<=max(values)<=Q(Z.hi,v.S)
 if not Y.lo<=0<=Y.hi:
  Z=X/Y;values=[i/j for i in p for j in r]
  assert Q(Z.lo,v.S)<=min(values)<=max(values)<=Q(Z.hi,v.S)
assert v.trig(v.PI/2)[1].hi==v.S
assert v.trig(v.PI)[0].lo==-v.S
assert v.trig(2*v.PI)[0].hi==v.S
rejected=[]
rows=[json.loads(s) for s in (root/'target_leaves.jsonl').read_text().splitlines()]
neg=[json.loads(s) for s in (root/'negative_leaves.jsonl').read_text().splitlines()]
with TemporaryDirectory() as t:
 def reject(name,data,height,co):
  p=Path(t)/'mutant.jsonl';p.write_text(''.join(json.dumps(x)+'\n' for x in data))
  try:v.scan(p,height,co)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Mutation incorrectly accepted: '+name)
 reject('missing initial leaf',rows[1:],10000,(1,1,1))
 reject('duplicated initial leaf',rows[:1]+rows,10000,(1,1,1))
 mutant=[dict(x) for x in neg]
 for x in mutant:x['accepted']=True
 reject('known zero falsely marked certified',mutant,8,(2,0,0))
print(json.dumps({'six_permuted_elimination_identities':'PASS','unit_norms_and_cancellation':'PASS','sign_mutants_rejected':sign_mutants,'denominator_mutants_rejected':denominator_mutants,'torus_jacobian_determinant_sqrt6479_coefficient':str(det),'rational_interval_arithmetic_tests':200,'critical_point_inclusion':'PASS','coverage_and_false_success_mutants_rejected':rejected},indent=2,sort_keys=True))
