"""Read-only verification of this independent review's custody and receipts."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;S=E.parents[1]/'sources';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,tag):
    if not ok:raise ValueError(tag)
def verify(rows,root,key='sha256'):
    for row in rows:
        p=root/row['path'];require(p.resolve().is_relative_to(root.resolve()) and not p.is_symlink() and p.is_file() and p.stat().st_size==row['bytes'] and H(p)==row[key],'binding '+str(p))
seal=json.loads((E/'SEAL.json').read_bytes());require(H(E/'MANIFEST.json')==seal['manifest_sha256'],'own manifest seal')
manifest=json.loads((E/'MANIFEST.json').read_bytes());verify(manifest['files'],E)
actual={str(p.relative_to(E)) for p in E.rglob('*') if p.is_file()}-{'MANIFEST.json','SEAL.json'}
require(actual=={r['path'] for r in manifest['files']},'exact owned file set')
early=json.loads((E/'EARLY_SEAL.json').read_bytes());require(H(E/'EARLY_MANIFEST.json')==early['manifest_sha256'],'early seal');verify(json.loads((E/'EARLY_MANIFEST.json').read_bytes())['files'],E)
require(H(S/'SOURCE_READY.json')=='b9a6b2f5d848fd924682faf33ad39c74f80d6d849e1a0081abbc5d5bfdc0bf4d','source-ready original')
require(H(S/'SOURCE_READY_MANIFEST.json')=='6c0e7a2de9e057d850fc61addd2c493c6f2feacc6c5aa57bd0875df41fbd2924','source manifest original')
source=json.loads((S/'SOURCE_READY_MANIFEST.json').read_bytes());verify(source['files'],S,'SHA256')
sourcesseal=json.loads((S/'SOURCE_READY_SEAL.json').read_bytes());require(sourcesseal['SOURCE_READY_SHA256']==H(S/'SOURCE_READY.json') and sourcesseal['SOURCE_READY_MANIFEST_SHA256']==H(S/'SOURCE_READY_MANIFEST.json'),'native ready seal')
a=json.loads((E/'INDEPENDENT_CONTROLS_NORMAL.json').read_bytes());b=json.loads((E/'INDEPENDENT_CONTROLS_OPTIMIZED.json').read_bytes());require(a==b and a['all_passed'] and a['check_count']==33057 and a['exact_check_count']==2584 and a['wrong_order_cases_detected']==500,'own finite controls')
execution=json.loads((E/'INDEPENDENT_EXECUTION_LEDGER.json').read_bytes());require(execution['code_sha256']==H(E/'independent_controls.py') and execution['normal_exit']==execution['optimized_exit']==0,'own code/execution binding')
exact=json.loads((E/'SUPPLIED_REPLAY_exact.json').read_bytes());numeric=json.loads((E/'SUPPLIED_REPLAY_numeric.json').read_bytes());require(exact['passed'] and len(exact['checks'])==10 and numeric['passed'] and numeric['check_count']==7679 and numeric['failures']==[],'optional source diagnostics')
for item in json.loads((E/'SUPPLIED_EXECUTION_LEDGER.json').read_bytes()):require(item['exit']==0,'supplied executable exit')
verdict=json.loads((E/'VERDICT.json').read_bytes());require(verdict['publication_authority'] is False and verdict['follow_up'] is None and verdict['source_repair_required'] is False,'scope and authority')
print(json.dumps({'status':'PASS_READ_ONLY_REVIEW_CUSTODY','owned_bindings':len(manifest['files']),'source_original_bindings':len(source['files']),'early_reconstruction_seal_unchanged':True,'own_controls':33057,'own_exact_controls':2584,'normal_optimized_identical':True,'supplied_exact':10,'supplied_numeric':7679,'universal_scope_evidence':'Written analytic reconstruction; finite controls are not a universal proof.','publication_authority':False},indent=2))
