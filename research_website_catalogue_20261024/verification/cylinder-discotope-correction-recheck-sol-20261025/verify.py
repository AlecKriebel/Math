"""Read-only final packet and original preservation recheck; writes nothing."""
from pathlib import Path
import hashlib,json
O=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,tag):
    if not x:raise ValueError('correction_verify:'+tag)
seal=json.loads((O/'FINAL_SEAL.json').read_text());mf=O/'FINAL_MANIFEST.json';need(sha(mf)==seal['manifest_SHA256'],'manifest_seal')
files=json.loads(mf.read_text())['files']
for item in files:
    p=O/item['path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'owned:'+item['path'])
present={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']}
need(present=={x['path'] for x in files},'complete_owned_inventory')
preserved=0
for name,key in [('protected-before.json','files'),('AUDITOR_INPUT_CUSTODY.json','original_files')]:
    for item in json.loads((O/name).read_text())[key]:
        p=Path(item['path']);need(p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'original:'+str(p));preserved+=1
early=json.loads((O/'EARLY_MECHANISM_SEAL.json').read_text());need(sha(O/'EARLY_MECHANISM.json')==early['EARLY_MECHANISM_SHA256'],'early_mechanism_immutable')
r=json.loads((O/'RECHECK_RESULTS.json').read_text());need(r['executions']==44 and r['per_mode_former_false_accepts_now_rejected']==7 and not r['full_old59_suite_rerun'],'bounded_results')
for mode in ['normal','optimized']:
    cases=[x for x in r['cases'] if x['mode']==mode];need(len(cases)==22 and sum(x['accepted'] for x in cases)==2 and all(x['accepted']==x['expected_pristine'] for x in cases),'mode_outcomes')
    need(sum(x['former_false_accept'] for x in cases)==7,'seven_former_faults')
print(json.dumps({'status':'PASS_READ_ONLY_CORRECTION_RECHECK_VERIFICATION','owned_bindings':len(files),'preserved_original_bindings':preserved,'executions':44,'pristine_accepted_each_mode':2,'faults_rejected_each_mode':20,'former_seven_rejected_each_mode':True,'old59_suite_rerun':False,'writes':0,'production_installed':False},indent=2))
