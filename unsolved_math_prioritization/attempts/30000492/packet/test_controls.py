#!/usr/bin/env python3
"""Deterministic positive/negative controls for the arithmetic checker."""
import json
from fractions import Fraction
import verify as v

checks=[]
def check(name,b):
 assert b,name
 checks.append(name)
check('F2 irreducible quadratic',v.irreducible([1,1,1],2))
check('F2 reducible square',not v.irreducible([1,0,1],2))
check('F7 irreducible x2+1',v.irreducible([1,0,1],7))
check('F7 reducible x2-1',not v.irreducible([6,0,1],7))
check('F7 repeated square rejected',not v.irreducible(v.mul([1,0,1],[1,0,1],7),7))
check('constant rejected',not v.irreducible([1],7))
# Exhaustive low-degree control only: all monic degrees 1..4 over F2, F3.
count=0
import itertools
for p in [2,3]:
 for degree in range(1,5):
  for cs in itertools.product(range(p),repeat=degree):
   h=list(cs)+[1]
   expected=bool(v.sp.Poly.from_list(list(reversed(h)),v.x,modulus=p).is_irreducible)
   check('Rabin-control-'+str(count),v.irreducible(h,p)==expected);count+=1
# The proposed missing support must use tail length 2 for f=x2+1/F7.
w=v.markov_witness()
check('actual iterate factor',w['occurs_at_iterate']==4 and w['g'] in w['fourth_iterate_factors'])
check('correct old support',w['old_model_grandchild_types']==['nnn','nss','snn','sss'])
check('history excludes unequal first two digits',w['theorem_excludes']==['nss','snn'])
check('actual terminal types stable',all(h['type']=='nnn' for h in w['levels'][-1]))
# Values from written conclusions must exactly agree with saved certificate.
saved=json.load(open(v.Path(__file__).with_name('EXACT_RESULTS.json')))
expected=[Fraction(85,128),Fraction(11,32),Fraction(13,16),Fraction(1,8),Fraction(3,16)]
check('written finite masses',all(Fraction(P['rows'][-1]['stable_mass'])==r for P,r in zip(saved['odd_profiles'],expected)))
check('degree doubling threshold at p31',next(P['proved_stable_threshold'] for P in saved['fixed_critical_point_family'] if P['p']==31)==5)
print(json.dumps({'status':'passed','control_count':len(checks),'low_degree_comparisons':count,'controls':checks},indent=2))
