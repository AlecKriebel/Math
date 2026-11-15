"""Read-only custody/result checks for the independent analytic packet."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;S=E.parents[1]/'sources';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,tag):
    if not ok:raise ValueError(tag)
def verify(rows,root):
    for x in rows:
        p=root/x['path'];require(p.resolve().is_relative_to(root.resolve()) and p.is_file() and not p.is_symlink() and p.stat().st_size==x['bytes'] and H(p)==x['sha256'],'binding '+str(p))
seal=json.loads((E/'SEAL.json').read_bytes());require(H(E/'MANIFEST.json')==seal['manifest_sha256'],'own seal')
manifest=json.loads((E/'MANIFEST.json').read_bytes());verify(manifest['files'],E)
require({str(p.relative_to(E)) for p in E.rglob('*') if p.is_file()}-{'MANIFEST.json','SEAL.json'}=={x['path'] for x in manifest['files']},'owned file set')
early=json.loads((E/'EARLY_SEAL.json').read_bytes());require(H(E/'EARLY_MANIFEST.json')==early['manifest_sha256'],'early seal');verify(json.loads((E/'EARLY_MANIFEST.json').read_bytes())['files'],E)
require(H(S/'SOURCE_READY.json')=='b9f69bfea594378f8cd69a00d214ce14c894fd33e850047a915327432d96ae20','native source ready')
native_seal=json.loads((S/'SOURCE_READY_SEAL.json').read_bytes());require(H(S/'SOURCE_READY.json')==native_seal['source_ready_sha256'] and H(S/'SOURCE_READY_MANIFEST.json')==native_seal['manifest_sha256'],'native manifest seal')
native=json.loads((S/'SOURCE_READY_MANIFEST.json').read_bytes());verify(native['files'],S)
a=json.loads((E/'INDEPENDENT_CONTROLS_NORMAL.json').read_bytes());b=json.loads((E/'INDEPENDENT_CONTROLS_OPTIMIZED.json').read_bytes())
require(a==b and a['status']=='PASS' and a['checks_total']==181983 and a['floating_point_decisions'] is False,'independent controls')
require(sum(x['certified_all_pairs'] for x in a['chord_records'])==6292 and all(x['unique_exact_witnesses']==[[0,1]] for x in a['chord_records']),'direct validated pair certificates')
execution=json.loads((E/'INDEPENDENT_EXECUTION_LEDGER.json').read_bytes());require(H(E/'independent_controls.py')==execution['code_sha256'] and len(execution['runs'])==2 and all(x['exit']==0 for x in execution['runs']),'independent execution')
replay=json.loads((E/'supplied-replay/RESULT.json').read_bytes());require(replay['status']=='PASS_PAYLOAD_INTEGRITY_AND_FINITE_CONTROLS' and replay['successful_controls']==4 and replay['expected_mathematical_rejections']==5,'original programme replay')
expected=json.loads((S/'published-source/EXPECTED_SCIENTIFIC_OUTPUTS.json').read_bytes())
for label,values in expected['positive'].items():
    data=json.loads((E/'supplied-replay'/label/'stdout.bin').read_bytes());require(all(data[k]==v for k,v in values.items()),'source positive '+label)
for label,reason in expected['mathematical_rejections'].items():
    result=json.loads((E/'supplied-replay'/label/'execution.json').read_bytes());err=(E/'supplied-replay'/label/'stderr.bin').read_text();require(result['exit']==1 and reason in err and 'AssertionError' in err and (E/'supplied-replay'/label/'stdout.bin').stat().st_size==0,'genuine source rejection '+label)
v=json.loads((E/'VERDICT.json').read_bytes());require(v['source_repair_required'] is False and v['publication_authority'] is False and v['follow_up'] is None,'scope')
print(json.dumps({'status':'PASS_INDEPENDENT_ANALYTIC_CUSTODY','owned_bindings':len(manifest['files']),'source_original_bindings':len(native['files']),'early_seal_unchanged':True,'own_exact_checks_each_mode':181983,'normal_optimized_identical':True,'direct_interval_pairs':6292,'supplied_positive_processes':4,'genuine_negative_processes':5,'all_n_proof':'Written independent reconstruction; finite controls are supplementary.','publication_authority':False},indent=2))
