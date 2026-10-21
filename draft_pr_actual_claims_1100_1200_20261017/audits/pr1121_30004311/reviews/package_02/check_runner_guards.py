#!/usr/bin/env python3
"""Negative integrity/optimization controls, performed solely in ignored mirrors."""
from pathlib import Path
import importlib.util,shutil,hashlib,json,copy
BASE=Path(__file__).resolve().parent
SRC=BASE/'tmp/extracted'
M=BASE/'tmp/runner-mutations'
if M.exists():shutil.rmtree(M)
shutil.copytree(SRC/'verification',M/'verification')
shutil.copytree(SRC/'audit',M/'audit')
spec=importlib.util.spec_from_file_location('mirror_verifier',M/'verification/verify_all.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
plan=json.loads((M/'verification/CONTROL_PLAN.json').read_text())
rows=[]
def digest(raw):return hashlib.sha256(raw).hexdigest()
def reject(name,job,needle):
 try:mod.run_control((job,False))
 except RuntimeError as e:
  if needle not in str(e):raise RuntimeError('wrong rejection '+str(e))
  rows.append({'case':name,'rejected':str(e)});return
 raise RuntimeError('Bad mutation accepted '+name)
job=copy.deepcopy(plan[3]);file=M/'audit'/job['file'];original=file.read_bytes()
file.write_bytes(original+b'\n# corruption\n');reject('checker altered',job,'fingerprint')
file.write_bytes(original)
p=M/'audit/inputs/PROOF.md';raw=p.read_bytes();p.write_bytes(raw+b' ');reject('original proof altered',job,'proof changed');p.write_bytes(raw)
p=M/'audit'/job['expected'];raw=p.read_bytes();p.write_bytes(raw+b' ');reject('expected receipt altered',job,'Expected result fingerprint');p.write_bytes(raw)
file.write_bytes(original+b'\nassert True\n');j=copy.deepcopy(job);j['sha256']=digest(file.read_bytes());reject('assert inserted with matching checker hash',j,'Optimization-sensitive');file.write_bytes(original)
# Mutate a true mathematical output while resealing the expected receipt hash.
p=M/'audit'/job['expected'];raw=p.read_bytes();j=copy.deepcopy(job);wrapper=json.loads(raw);wrapper['runs'][0]['result']['binary_vectors']=15;p.write_text(json.dumps(wrapper));j['expected_sha256']=digest(p.read_bytes());reject('false expected mathematics with resealed receipt hash',j,'Mathematical result mismatch');p.write_bytes(raw)
# A nominal successful receipt cannot erase historical failure.
wrapper=json.loads(raw);wrapper['runs'][0]['exit_code']=1;p.write_text(json.dumps(wrapper));j=copy.deepcopy(job);j['expected_sha256']=digest(p.read_bytes());reject('historical failed symbolic run',j,'Invalid historical');p.write_bytes(raw)
result={'status':'PASS','negative_controls':rows,'operative_assets_edited':False}
(BASE/'RUNNER_GUARDS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
