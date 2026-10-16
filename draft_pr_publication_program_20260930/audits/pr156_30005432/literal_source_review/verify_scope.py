#!/usr/bin/env python3
"""Independent finite-coefficient controls; the infinite-index proof is in REVIEW.md."""
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import json
import argparse
import sys
parser=argparse.ArgumentParser()
parser.add_argument("--receipt",default="CHECKS.json")
parser.add_argument("--corrupt-annihilator",action="store_true",help="Intentional negative control: falsely require r in Ann(B3)")
args=parser.parse_args()
C=range(4)
eps=lambda c: 1 if c in (0,1) else -1
q=lambda c,d:(c+d+2*c*d)%4
eta=lambda c: 1 if c%2==0 else -1
checks=0
def check(cond):
 global checks
 checks+=1
 if not cond:
  raise RuntimeError(f"Mathematical check {checks} failed")
for c,d in product(C,repeat=2):
 check(q(c,d)==q(d,c))
 check(eps(q(c,d))==eps(c)*eps(d))
 check(eta(q(c,d))==eta(c)*eta(d))
 check(q(c,d)%2==(c+d)%2)
 check((q(c,d)//2)%2==((c//2)+(d//2))%2)
for c,d,e in product(C,repeat=3):
 # Universal integer coefficients of n,m,p in (a circle b) circle e and a circle (b circle e).
 check((1,eps(c),eps(q(c,d)))==(1,eps(c),eps(c)*eps(d)))
 check(q(q(c,d),e)==q(c,q(d,e)))
 # Second-coordinate left distributivity; universal integer coefficients coincide as (1,eps(c),eps(c)).
 check(q(c,(d+e)%4)==(q(c,d)-c+q(c,e))%4)
for c in C:
 check(q(0,c)==c==q(c,0))
 check(q(c,c)==0)
 check(1+eps(c)*(-eps(c))==0) # n + eps(c)*inverse first coordinate
 check(-eps(c)+eps(c)==0)   # inverse first coordinate + eps(c)*n
 for d in C:
  check((q(c,d)-c-d)%4==(2*c*d)%4)
  check((q(c,d)-c)%4==(eta(c)*d)%4)
# Exact rightfixed conditions depend on the universal m coefficient and d residue.
right_kernel_records=[]
for c in C:
 coefficient=eps(c)-1
 residues=[d for d in C if 2*c*d%4==0]
 right_kernel_records.append({'c':c,'m_coefficient':coefficient,'d_residues':residues,'m_unrestricted':coefficient==0})
check(right_kernel_records[1]['m_coefficient']==0)
check(right_kernel_records[1]['d_residues']==[0,2])
check(right_kernel_records[2]['m_coefficient']==-2)
check(right_kernel_records[2]['d_residues']==[0,1,2,3])
# Parameter n=0 vs n !=0 is exact: (eps(d)-1)n vanishes iff coefficient=0 for nonzero integer n.
indices=[]
for c,n_nonzero in product((0,1),(False,True)):
 D=[d for d in C if (not n_nonzero or eps(d)==1) and (2*d*c)%4==0]
 check(all(q(d,e) in D for d,e in product(D,repeat=2)))
 indices.append({'c':c,'n_nonzero':n_nonzero,'first_index':1 if c==0 else 2,'second_projection_kernel_residues':D,'second_index':4//len(D)})
# Finite quotient B3 controls have full hypotheses of the cited converse but a noninjective f.
P=list(product(range(3),C))
def plus(a,b):return ((a[0]+b[0])%3,(a[1]+b[1])%4)
def neg(a):return ((-a[0])%3,(-a[1])%4)
def circ(a,b):return ((a[0]+eps(a[1])*b[0])%3,q(a[1],b[1]))
def star(a,b):return plus(plus(neg(a),circ(a,b)),neg(b))
zero=(0,0);r=(1,0);x=(0,1)
for a,b,c in product(P,repeat=3):
 check(circ(circ(a,b),c)==circ(a,circ(b,c)))
 check(circ(a,plus(b,c))==plus(plus(circ(a,b),neg(a)),circ(a,c)))
ann=[a for a in P if all(star(a,b)==zero and star(b,a)==zero and circ(a,b)==circ(b,a) for b in P)]
check(ann==([zero,r] if args.corrupt_annihilator else [zero]))
def fmap(a):return (star(a,r),star(a,x),star(r,a),star(x,a),zero,zero)
check(fmap(zero)==fmap(r))
check(r not in ann)
check(star(r,r)==zero and star(x,r)==zero and star((0,2),r)==(1,0))
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','python_optimization_level':sys.flags.optimize,'negative_control_requested':args.corrupt_annihilator,'exact_controls':checks,'scope':'Coefficient identities certify universal integer formulas; B3 finite quotient checks certify source proof-map collision. Infinite index rests on written distinct-coset proof, not bounded tests.','right_fixed_kernel_records':right_kernel_records,'property_s_indices_for_c0_c1':indices,'B3':{'cardinality':len(P),'annihilator':ann,'f_zero':fmap(zero),'f_r':fmap(r),'collision_distinct_ann_cosets':True,'all_converse_premises_satisfied':True,'theorem_conclusion_false':False}}
Path(args.receipt).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
