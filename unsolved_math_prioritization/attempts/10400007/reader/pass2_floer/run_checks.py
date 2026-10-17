#!/usr/bin/env python3
import json
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('pl_markov_test',Path(__file__).with_name('pl_markov_test.py'))
pl=importlib.util.module_from_spec(spec);spec.loader.exec_module(pl)
experiment=pl.experiment;quantum_grade_experiment=pl.quantum_grade_experiment;inverse_generator_count=pl.inverse_generator_count
D=Path(__file__).parent
out=[]
for n,word,expected_count,expected_poly in [
 (1,[1],3,{(0,1):1,(1,1):-1,(1,2):1}),
 (2,[1,2],5,{(0,1):1,(1,1):-1,(1,3):1,(2,3):-1,(2,4):1})]:
 result=experiment(n,word);rows=quantum_grade_experiment(n,word)
 poly={(r['A'],r['Q']):r['Euler_coefficient'] for r in rows}
 if result['generator_count']!=expected_count or poly!=expected_poly:raise AssertionError((result,poly))
 for r in rows:
  r['W']=sum(3*(n-i)+1 for i in r['S']);r['R0']=sum(n-i for i in r['S']);r['B']=r['Q']-r['W']+r['R0'];r['C']=r['R0']-r['W']
 arrows=[]
 for a in sorted({r['A'] for r in rows}):
  same=[r for r in rows if r['A']==a]
  if a==0:
   if len(same)!=1:raise AssertionError('Expected one A0 generator')
   continue
  if len(same)!=2:raise AssertionError('Expected two generators in nonzero Alexander degree')
  source,target=sorted(same,key=lambda r:r['W'])
  if source['W']==target['W']:raise AssertionError('Cannot fix direction by W')
  arrows.append({'A':a,'source_Q':source['Q'],'target_Q':target['Q'],'U_exponent':source['B']-target['B'],'V_exponent':source['C']-target['C']})
 result.update({'generators':rows,'forced_Rees_arrows':arrows,'derivation':'The knot Floer homology of the unknot is one-dimensional in A=0. Each nonzero-A block has exactly two generators; positivity implies W cannot decrease, fixing the nonzero arrow direction. Exponents are B and C differences.'})
 out.append(result)
if out[0]['forced_Rees_arrows']!=[{'A':1,'source_Q':1,'target_Q':2,'U_exponent':0,'V_exponent':1}]:raise AssertionError('First arrows')
if out[1]['forced_Rees_arrows']!=[{'A':1,'source_Q':1,'target_Q':3,'U_exponent':1,'V_exponent':3},{'A':2,'source_Q':3,'target_Q':4,'U_exponent':0,'V_exponent':1}]:raise AssertionError('Second arrows')
inverse_count=inverse_generator_count()
if inverse_count!=1:raise AssertionError('Inverse orientation calibration')
report={'status':'PASS','inverse_half_twist_generator_count':inverse_count,'arithmetic':'fractions.Fraction; all predicates rational and exact','models':out,'qHFB_dimensions':[3,5],'one_parameter_fiber_dimensions':{'U=0,V=1':[1,3],'U=1,V=0':[3,5],'U=1,V=1':[1,1]},'analytic_inputs':'Published v4 invariance for same-braid representative, relation to knot Floer and positivity, plus standard unknot HFK; no independent pseudoholomorphic-disc enumeration.'}
(D/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
