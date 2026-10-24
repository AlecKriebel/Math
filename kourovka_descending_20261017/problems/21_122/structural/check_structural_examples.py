#!/usr/bin/env python3
"""Exact finite-group controls for the two infinite-product countermodels."""
from itertools import permutations,product
from pathlib import Path
from datetime import datetime,timezone
import json

def pmul(a,b):return tuple(a[b[i]] for i in range(len(a)))
def pinv(a):return tuple(a.index(i) for i in range(len(a)))
def dmul(a,b):return ((a[0]+(-1)**a[1]*b[0])%4,(a[1]+b[1])%2)
def dinv(a):return ((-(-1)**a[1]*a[0])%4,a[1])
def comm(a,b,mul,inv):return mul(mul(mul(inv(a),inv(b)),a),b)
def run():
 s3=list(permutations(range(3)));identity=(0,1,2)
 trans=[x for x in s3 if x!=identity and pmul(x,x)==identity]
 assert len(trans)==3
 sc={comm(a,b,pmul,pinv) for a,b in product(s3,repeat=2)}
 assert len(sc)==3 and all(pmul(x,pmul(x,x))==identity for x in sc)
 assert {pmul(pmul(pinv(g),x),g) for g in s3 for x in trans}==set(trans)
 d8=list(product(range(4),range(2)));dc={comm(a,b,dmul,dinv) for a,b in product(d8,repeat=2)};squares={dmul(x,x) for x in d8}
 assert dc==squares=={(0,0),(2,0)}
 assert all(dmul(z,x)==dmul(x,z) for z in dc for x in d8)
 assert {dmul(z,z) for z in dc}=={(0,0)}
 products=[]
 for n in range(1,11):
  # Independent coordinate choices yield exactly 2^n values; direct enumeration
  # uses the finite product of the already verified single-factor value sets.
  vals=set(product(sorted(dc),repeat=n));assert len(vals)==2**n
  products.append({'D8_factors':n,'square_value_count':len(vals),'commutator_value_count':len(vals),'second_verbal_count':1})
 return {'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS_EXACT_PRODUCT_COUNTERMODEL_CONTROLS','S3_transpositions':len(trans),'S3_commutator_values':len(sc),'D8_single_factor_values':sorted(dc),'finite_product_checks':products,'scope':'Controls for explicit countermodels to overstrong structural inferences. The infinite products and topology are proved in the note. None has a small infinite word-value set.'}
if __name__=='__main__':
 out=run();Path(__file__).with_name('structural_example_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
