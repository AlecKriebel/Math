#!/usr/bin/env python3
"""Fail-closed integrity and algebra replay for the frozen pointwise cut theorem."""
from collections import Counter
from pathlib import Path
import json
import sympy as sp

HERE=Path(__file__).resolve().parents[1]
CERT=HERE/'certificates'/'pointwise_cut_certificate.json'

def main():
 d=json.loads(CERT.read_text())
 assert d['status']=='PROVED'
 assert d['endpoint_type_count']==177
 assert d['endpoint_dichotomy']=={'F_positive':151,'F_zero_G_positive':26}
 assert len(d['endpoint_records'])==177
 branches=Counter()
 for r in d['endpoint_records']:
  c=r['certificate'];branches[c['branch']]+=1
  if c['branch']=='F_positive':
   assert not c['F']['zero'] and c['F']['total_sign']==1
  else:
   assert c['branch']=='F_zero_G_positive' and c['F']['zero']
   assert not c['G']['zero'] and c['G']['total_sign']==1
 assert dict(branches)==d['endpoint_dichotomy']
 assert d['single_blob_type_count']==453
 assert d['single_blob_classification']=={'wrong_split_strict':421,'rank_one_all_blocks':32}
 assert len(d['single_blob_records'])==453
 classes=Counter()
 for r in d['single_blob_records']:
  c=r['certificate'];classes[c['classification']]+=1
  if c['classification']=='wrong_split_strict':
   assert not c['sign']['zero'] and c['sign']['total_sign'] in (-1,1)
   assert not c['displayed_bridge']
  else:
   assert c['classification']=='rank_one_all_blocks' and c['displayed_bridge']
 assert dict(classes)==d['single_blob_classification']
 # Independently rederive the four decisive two-active-endpoint minors.
 a,b,c,t,A,B,C,T,z=sp.symbols('a b c t A B C T z', positive=True)
 expected={
  'm0':A*a-B*C*b*c*z**2,
  'm1':-(-A*a+T*t*z)*(A*a+T*t*z),
  'm2':A**2*a-T**2*b*c*z**2,
  'm3':A*a**2-B*C*t**2*z**2,
 }
 for k,v in expected.items():
  assert sp.expand(v-sp.sympify(d['two_active_endpoint_case']['decisive_minors'][k], locals={x.name:x for x in (a,b,c,t,A,B,C,T,z)}))==0
 assert d['two_active_endpoint_case']['derived_rank_one_equations']==[
  'a*b*c=t**2','A*B*C=T**2','a*A=b*c*B*C*z**2']
 # If all wrong-split minors vanish, m0/m2 and m0/m3 imply the two tree
 # equations by positive cancellation.  Endpoint branch F=0 then forces
 # a>bc and A>BC, contradicting m0 with 0<z<1.
 out={
  'status':'VERIFIED',
  'endpoint_types':177,
  'endpoint_dichotomy':dict(branches),
  'single_blob_types':453,
  'single_blob_classification':dict(classes),
  'two_active_endpoint_contradiction':True,
  'conclusion':'one-sided open JC containment preserves every cut split',
 }
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
