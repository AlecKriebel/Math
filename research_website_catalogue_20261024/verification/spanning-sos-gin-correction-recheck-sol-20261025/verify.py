"""Read-only packet/original preservation verifier, with no test replay."""
from pathlib import Path
import hashlib,json
O=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,tag):
    if not x:raise ValueError('sg_correction_verify:'+tag)
seal=json.loads((O/'FINAL_SEAL.json').read_text());mf=O/'FINAL_MANIFEST.json';need(sha(mf)==seal['manifest_SHA256'],'manifest_seal');items=json.loads(mf.read_text())['files']
for x in items:
    p=O/x['path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==x['bytes'] and sha(p)==x['SHA256'],'owned:'+x['path'])
actual={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']};need(actual=={x['path'] for x in items},'complete_owned_inventory')
count=0
for n,k in [('protected-before.json','files'),('AUDITOR_INPUT_CUSTODY.json','original_files')]:
    for x in json.loads((O/n).read_text())[k]:
        p=Path(x['path']);need(p.is_file() and p.stat().st_size==x['bytes'] and sha(p)==x['SHA256'],'original:'+str(p));count+=1
early=json.loads((O/'EARLY_MECHANISM_SEAL.json').read_text());need(sha(O/'EARLY_MECHANISM.json')==early['EARLY_MECHANISM_SHA256'],'early_seal')
prior=json.loads((O/'PRIOR_RESULTS.json').read_text());auditor=json.loads((O/'AUDITOR_REPLAY_RESULTS.json').read_text())
need(prior['status']==auditor['status']=='PASS' and len(prior['faults'])==70 and len(auditor['cases'])==62,'all_negative_results')
for mode in ['normal','optimized']:
    a=[x for x in prior['faults'] if x['mode']==mode];b=[x for x in auditor['cases'] if x['mode']==mode];need(len(a)==35 and len(b)==31 and all(x['rejected'] for x in a+b) and sum(x['former_false_accept'] for x in b)==7,'per_mode_results')
    positive=next(x for x in prior['pristine'] if x['mode']==mode);need(positive['status']=='PASS' and len(positive['record_ids'])==3 and positive['checks']==194,'pristine3')
need(sha(O/'inputs/final-content-check.proposed.py')=='aceef187f34f5d1029a19e4e2e9b2b15472535a07cf224134adbd2ddb16fd6c4','root_input')
print(json.dumps({'status':'PASS_READ_ONLY_CORRECTION_RECHECK_VERIFICATION','owned_bindings':len(items),'preserved_original_bindings':count,'pristine_records_each_mode':3,'prior_faults_rejected_each_mode':35,'auditor_faults_rejected_each_mode':31,'former_seven_rejected_each_mode':True,'negative_checker_dispatches':132,'total_checker_subprocesses':134,'old61_suite_rerun':False,'renderer_rerun':False,'production_installed':False,'writes':0},indent=2))
