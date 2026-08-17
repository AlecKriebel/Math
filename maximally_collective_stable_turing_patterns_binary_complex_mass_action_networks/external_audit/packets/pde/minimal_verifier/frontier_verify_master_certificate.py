#!/usr/bin/env python3
from __future__ import annotations

if not __debug__:
 raise SystemExit('Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O')

import argparse,json
from pathlib import Path
import sympy as sp

def parse(s,local): return sp.sympify(s,locals=local)
def verify(path:Path):
 d=json.loads(path.read_text());assert d['schema_version']==1 and d['outcome']=='STABLE-PARETO'
 m,r,L=sp.symbols('m r L',positive=True)
 loc={'m':m,'r':r,'L':L,'sqrt':sp.sqrt}
 assert parse(d['linear_tradeoff']['factor'],loc)==8
 family=d['pareto_family']
 chiD=parse(family['chi_D'],loc);chiH=parse(family['chi_H'],loc);prod=parse(family['product'],loc)
 assert sp.factor(chiD*chiH-prod)==0
 assert sp.factor(prod.subs(r,m-2)-sp.Rational(23,63)*(91*m-183))==0
 L0=family['L0']
 assert parse(L0['r_eq_1'],loc)==1/sp.sqrt(3)
 assert sp.factor(r*parse(L0['r_ge_2'],loc)**2-sp.Rational(5,4))==0
 for key,rv in [('L0_chi_D',chiD),('L0_chi_H',chiH)]:
  endpoint=family[key]
  assert sp.factor(parse(endpoint['r_eq_1'],loc).subs(r,1)-rv.subs({r:1,L:parse(L0['r_eq_1'],loc)}))==0
  assert sp.factor(parse(endpoint['r_ge_2'],loc)-rv.subs(L,parse(L0['r_ge_2'],loc)))==0
 assert d['mode_certificate']=={
  'homogeneous_terms':22,'spatial_terms':84,
  'homogeneous_B':'5/4','spatial_B':'1/3',
  'homogeneous_coefficient_shift':'U=A-1/4'}
 nf=d['normal_form'];assert nf['zero_mode_rhs_factor']=='-1/4' and nf['second_mode_rhs_factor']=='-1/4' and nf['cubic_second_harmonic_factor']=='1/2'
 assert sp.Rational(nf['N0_lower'])-sp.Rational(nf['tau_upper'])*sp.Rational(nf['S_abs_upper'])==sp.Rational(nf['N_lower'])
 assert d['near_threshold']['prescribed_m3_limit']=='6/1379'

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('certificate',nargs='?',default=str(Path(__file__).resolve().parent/'frontier_certificate.json'));a=p.parse_args();verify(Path(a.certificate));print('VERIFY_MASTER_CERTIFICATE_PASS')
