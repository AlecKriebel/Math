#!/usr/bin/env python3
"""Root independent packet verification and unchanged fresh-exact replays.
No provider operations, prior helper imports, or source mutations.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal
B=Path(__file__).resolve().parent
F=B/'fresh_whole_math_adversary'
O=B/'root_fresh_whole_verification_v01'
assert not O.exists(), 'One-shot evidence folder already exists'
O.mkdir()
checks=[]
def check(value,name):
    assert value,name
    checks.append(name)
def pin(path,p):
    b=Path(path).read_bytes()
    check(len(b)==p['bytes'],str(path)+' size')
    check(hashlib.sha256(b).hexdigest()==p['sha256'],str(path)+' sha256')
    if 'git_blob_oid' in p:
        check(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==p['git_blob_oid'],str(path)+' native blob')
    return b
manifest=json.loads((F/'MANIFEST.json').read_bytes())
for name,p in manifest['output_pins'].items():pin(F/name,p)
for name,p in manifest['runtime_entrypoint_pins'].items():pin(name,p)
freeze=json.loads((F/'PRECOMPARISON_FREEZE.json').read_bytes())
for name,p in freeze['pins'].items():
    if name=='RESEARCH_LOG.md':
        b=(F/name).read_bytes()[:p['bytes']]
        check(len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256'],'frozen research log exact prefix preserved')
    else:pin(F/name,p)
inputs=json.loads((F/'POSTCOMPARISON_INPUT_PINS.json').read_bytes())
check(len(inputs['submitted'])==26,'26 independently authenticated original bodies')
for p in inputs['submitted']:pin(p['path'],p)
for p in inputs['primary_pdf_full_hashes']:pin(p['path'],p)
for name,p in inputs['cross_comparison_inputs'].items():pin(name,p)
for r in json.loads((F/'ORIGINAL_REPLAY_RECEIPTS.json').read_bytes()):
    check(r['exit_code']==0 and r['byte_identical_to_frozen_output'] is True,r['name']+' recorded replay pass')
    pin(r['source'],r['source_pin']);pin(r['copy'],r['copy_pin'])
    d=F/'replays'/r['name']
    pin(d/'stdout.json',r['stdout']);pin(d/'stderr.txt',r['stderr'])
    check(r['stdout']['sha256']==r['expected_frozen_output_sha256'],r['name']+' frozen output byte equality')
N=json.loads((F/'INDEPENDENT_NUMERIC.json').read_bytes(),parse_float=Decimal)
check(Decimal(N['max_phase_and_symmetry_error'])<Decimal('1e-65'),'fresh sampled centroid/symmetry residual')
check(Decimal(N['min_actual_real_antipedal_determinant'])>0,'fresh sampled normal determinants positive')
check(Decimal(N['max_raw_tangent_vs_closed_outer_error'])<Decimal('1e-65'),'fresh actual tangent constructions')
check(Decimal(N['max_confocal_segment_tangency_residual'])<Decimal('1e-60'),'fresh sampled caustic tangency')
import math
for r in N['primitive_even_cases']:
    check(r['N']%2==0 and math.gcd(r['N'],r['tau'])==1 and 0<2*r['tau']<r['N'],'primitive even case '+str((r['k'],r['N'],r['tau'])))
    check(Decimal(r['phase_and_symmetry_max_error'])<Decimal('1e-65'),'sampled cell residual '+str((r['k'],r['N'],r['tau'])))
check(len(N['all_class_local_probes'])==20,'all twenty translated local probes')
for r in N['all_class_local_probes']:
    check(len(r['values'])==3,'three local approach probes '+r['class'])
    key='eps2_U_max' if r['class']=='endpoint_pole' else 'eps_U_max'
    check(Decimal(r['values'][-1][key])<Decimal('1e-23'),'local pole-order probe '+r['class'])
    if r['focal_root_error'] is not None:check(Decimal(r['focal_root_error'])<Decimal('1e-65'),'explicit focal root probe')
check(len(N['all_translate_actual_four_edge_residues'])==4,'all four common Jacobi-pole translates')
for r in N['all_translate_actual_four_edge_residues']:
    check(len(set(r['edge_indices']))==4,'four distinct actual incident edges')
    for component in r['sum_scaled']:
        check(abs(Decimal(component['re']))+abs(Decimal(component['im']))<Decimal('2e-22'),'sampled actual quartet residue cancellation')
py='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
replays=[]
for name,outname in [('independent_exact.py','INDEPENDENT_EXACT.json'),('supplementary_exact_witness.py','SUPPLEMENTARY_EXACT_WITNESS.json')]:
    d=O/name.removesuffix('.py');d.mkdir()
    b=(F/name).read_bytes();(d/name).write_bytes(b)
    start=datetime.now(timezone.utc).isoformat()
    r=subprocess.run([py,'-I','-B',str(d/name)],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (d/'stdout.txt').write_bytes(r.stdout);(d/'stderr.txt').write_bytes(r.stderr)
    check(r.returncode==0,name+' actual fresh replay exit0')
    actual=json.loads((d/outname).read_bytes());expected=json.loads((F/outname).read_bytes())
    actual.pop('utc',None);expected.pop('utc',None)
    # Supplementary receipt's self-relative historical path is provenance, not mathematical data.
    actual.pop('earlier_independent_freeze',None);expected.pop('earlier_independent_freeze',None)
    check(actual==expected,name+' unchanged mathematical replay content')
    replays.append({'program':name,'script_sha256':hashlib.sha256(b).hexdigest(),'start_utc':start,'finish_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,'comparison_exclusions':['utc','earlier_independent_freeze'],'mathematical_content_identical':True})
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':len(checks),'check_names':checks,'fresh_manifest_sha256':hashlib.sha256((F/'MANIFEST.json').read_bytes()).hexdigest(),'original_head':'0524ed734ee8185681d030af98088259134a6af7','replays':replays,'sampled_numeric_cases':len(N['primitive_even_cases']),'scope':'Artifact authenticity, unchanged fresh exact replays and finite numerical-result consistency only. Root separately reads and checks full proof/divisor argument. Numerical diagnostics are not interval proofs. Priority unaudited.','provider_writes':0,'shared_git_mutations':0}
(O/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('utc','status','checks','sampled_numeric_cases','provider_writes','shared_git_mutations')},indent=2))
