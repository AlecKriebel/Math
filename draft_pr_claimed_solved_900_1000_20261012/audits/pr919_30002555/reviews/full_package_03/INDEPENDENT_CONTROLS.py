#!/usr/bin/env python3
"""Third-round distinct finite falsification controls; never universal proof."""
import argparse,copy,hashlib,importlib.util,json,os,pathlib,shutil,stat,tempfile
from fractions import Fraction as F
from itertools import permutations
R=pathlib.Path(__file__).resolve().parent
def need(x,s):
 if not x:raise RuntimeError(s)
def load(p):
 spec=importlib.util.spec_from_file_location('review03_tested_verifier',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def perform(bundle):
 m=load(bundle/'verify_package.py');pin=hashlib.sha256((bundle/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest();m.validate(bundle,pin)
 rejected=[]
 def reject(fn,name):
  try:fn()
  except (RuntimeError,ValueError,TypeError,KeyError,FileNotFoundError,NotADirectoryError):rejected.append(name);return
  raise RuntimeError('accepted '+name)
 model={'a':[{'integer':1,'boolean':True,'nested':[None,'x',2.0]}]}
 for name,obj in [('bool_for_integer',{'integer':True}),('float_for_integer',{'integer':1.0}),('integer_for_boolean',{'boolean':1}),('int_for_float',{'nested':[None,'x',2]}),('changed_value',{'integer':2}),('changed_null',{'nested':[False,'x',2.0]})]:
  got=copy.deepcopy(model);got['a'][0].update(obj);reject(lambda got=got:m.equivalent(got,model),'recursive_'+name)
 for name,got in [('missing',{}),('extra',dict(model,b=0)),('tuple',{'a':tuple(model['a'])}),('listlength',{'a':[]})]:reject(lambda got=got:m.equivalent(got,model),'recursive_'+name)
 for name,b in [('nested_duplicate',b'{"a":{"x":1,"x":1}}'),('negative_infinity',b'{"x":-Infinity}'),('positive_infinity',b'[Infinity]')]:reject(lambda b=b:m.strict_json(b),'json_'+name)
 mutations=[('float_PR',lambda d:d.update(pr=919.0)),('float_schema',lambda d:d.update(schema_version=1.0)),('scope_list',lambda d:d.update(scope=['claimed'])),('empty_inventory',lambda d:d.update(files={})),('null_inventory',lambda d:d.update(files=None)),('float_bytes',lambda d:d['files']['note.tex'].update(bytes=12146.0)),('normalized_dot',lambda d:d['files'].update({'./note.tex':d['files'].pop('note.tex')})),('double_slash',lambda d:d['files'].update({'reviews//bad':d['files'].pop('note.tex')})),('backslash',lambda d:d['files'].update({'bad\\name':d['files'].pop('note.tex')})),('array_record',lambda d:d['files'].update({'note.tex':[]}))]
 work=R/'private/independent';work.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(dir=work) as td:
  root=pathlib.Path(td)/'bundle';shutil.copytree(bundle,root);original=(root/'PACKAGE_MANIFEST.json').read_bytes()
  for name,change in mutations:
   d=json.loads(original);change(d);raw=json.dumps(d).encode();(root/'PACKAGE_MANIFEST.json').write_bytes(raw)
   reject(lambda:m.validate(root,hashlib.sha256(raw).hexdigest()),'reanchored_'+name)
  (root/'PACKAGE_MANIFEST.json').write_bytes(original)
  proof=root/'original_packet/public/PROOF.md';raw=proof.read_bytes();proof.write_bytes(raw+b' altered')
  reject(lambda:m.validate(root,pin),'fixed_anchor_proof_change');proof.write_bytes(raw)
  alias=pathlib.Path(td)/'ancestor';alias.symlink_to(root.parent,target_is_directory=True)
  reject(lambda:m.validate(alias/root.name,pin),'symlink_ancestor')
  reject(lambda:m.validate(root/'..'/root.name,pin),'lexical_parent')
  m.validate(root,pin)
 # Fast binary Gaussian powers, distinct selected exponents including negatives.
 def product(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
 def power(n):
  b=(3,4);a=(1,0)
  while n:
   if n&1:a=product(a,b)
   b=product(b,b);n//=2
  return a
 arithmetic=[]
 for n in [13,257,2039,8191]:
  a,b=power(n);need(a*a+b*b==25**n and a%5==3 and b%5==4 and b!=0,'Gaussian fast power')
  need(product((a,b),(a,-b))==(25**n,0),'inverse Gaussian');arithmetic.append(n)
 # Exact quadratic-form check and explicit inner disk radius for transformed cone.
 T=((F(3),F(1)),(F(0),F(2)));Ti=((F(1,3),F(-1,6)),(0,F(1,2)));A=((F(3,5),F(-4,5)),(F(4,5),F(3,5)))
 def mm(x,y):return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(2)) for j in range(2)) for i in range(2))
 def tr(x):return tuple(zip(*x))
 Q=mm(tr(Ti),Ti);C=mm(mm(T,A),Ti);need(mm(mm(tr(C),Q),C)==Q and mm(tr(C),C)!=((1,0),(0,1)),'conjugate Q')
 need(sum(x*x for row in Ti for x in row)<1,'unit round disk fits transformed unit ellipse via inverse Frobenius bound')
 # C8->C4 has kernel C2 and admits no homomorphic section; full preimage works.
 need([x for x in range(8) if x%4==1]==[1,5] and all(4*x%8!=0 for x in [1,5]),'nonsplitting quotient')
 permutation_count=0
 for n in range(1,7):
  for pi in permutations(range(n)):
   for arm in range(n):
    inherited={pi[j] for j in range(n) if j!=arm};need(len(inherited)==n-1 and (len(inherited)>1)==(n>=3),'ambient ends permutation');permutation_count+=1
 # Finite groups must not be swept into the infinite-order claim.
 need(product((0,1),(0,1))==(-1,0) and product((-1,0),(-1,0))==(1,0),'finite rotation')
 m.validate(bundle,pin)
 return {'status':'PASS','independent_rejections':len(rejected),'rejections':rejected,'gaussian_fast_exponents':arithmetic,'end_permutation_receiving_arm_cases':permutation_count,'nonorthogonal_conjugate_Q_and_inner_disk_bound':True,'nonsplit_C8_to_C4':True,'unchanged_positive_validations':3,'limits':'Finite exact falsification controls only; no samples prove conformal properness, topology, all exponents, priority or security.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--bundle',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path);a=p.parse_args();out=perform(a.bundle)
 if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,sort_keys=True))
