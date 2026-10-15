from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent;D=A/'priority_modern_invariant_mechanism_20261006'
def require(c,m):
    if not c:raise RuntimeError(m)
def check(p,r):
    require(p.is_file() and not p.is_symlink(),'regular body '+str(p));b=p.read_bytes()
    require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'body pin '+str(p));return b
b=(D/'OUTPUT_MANIFEST.json').read_bytes();require(hashlib.sha256(b).hexdigest()=='070552d43ff08757eb0275ee952f5c49e235efeb0c7f6a6e6f951ca8841e3e6e','manifest')
m=json.loads(b);seen=set()
for r in m['public_payload_bodies']:
    p=D/r['path'];require(p.resolve().is_relative_to(D) and r['path'] not in seen,'path');seen.add(r['path'])
    require(not any(r['path'].startswith(x+'/') for x in m['private_folders_excluded']),'private payload');check(p,r)
require(len(seen)==m['public_payload_count']==185 and sum(x['bytes'] for x in m['public_payload_bodies'])==m['public_payload_bytes']==232171,'counts')
s=json.loads((D/'SEAL_RECEIPT.json').read_text())
for k in ['manifest_body_pin','private_metadata_pin','report_body_pin','verdict_body_pin']:check(D/s[k]['path'],s[k])
v=json.loads((D/'VERDICT.json').read_text());require(not v['combined_priority_clearance'] and not v['publication_clearance'] and v['bounded_novelty_support_within_read_modern_corpus'] and not v['full_covering_prior_located'],'bounded verdict')
require([x['id'] for x in v['required_findings']]==['M1'],'required gap')
i=json.loads((D/'INPUT_PINS.json').read_text());inputs=i['inputs']+i['reused_readonly_primary_sourcepins']
for r in inputs:check(Path(r['path']),r)
private=json.loads((D/'PRIVATE_MATERIAL_PINS.json').read_text())['private_complete_body_metadata_only']
for r in private:
    p=D/r['path'];require(p.resolve().is_relative_to(D),'private path');check(p,r)
ops=[]
for p in sorted((D/'actual_operations').glob('*/execution.json')):
    r=json.loads(p.read_text())
    for k in ('stdout','stderr'):check(p.parent/r[k]['path'],r[k])
    require(isinstance(r['child_PID'],int) and r['UTC_start']<=r['UTC_end'],'process metadata')
    ops.append({'label':p.parent.name,'child_PID':r['child_PID'],'exit_code':r['exit_code'],'argv':r['argv']})
close=json.loads((D/'actual_operations/seal_public_payload/execution.json').read_text());require(close['child_PID']==s['actual_sealer_PID']==36119 and close['exit_code']==0,'sealer')
for name,opt in [('TRANSFER_NORMAL.json',0),('TRANSFER_OPTIMIZED.json',1)]:
    r=json.loads((D/name).read_text());require(r['explicit_checks']==49 and r['optimization']==opt and r['status']=='passed','control')
    receipt=json.loads((D/'actual_operations'/('transfer_normal' if opt==0 else 'transfer_optimized')/'execution.json').read_text());require(receipt['child_PID']==r['actual_PID'] and receipt['exit_code']==0 and receipt['stderr']['bytes']==0,'control execution')
pins={}
for name in ['REPORT.md','VERDICT.json','OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','SOURCE_READ_LEDGER.json']:
    b=(D/name).read_bytes();pins[name]={'path':str((D/name).relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
result={'schema':'pr110-root-modern-priority-custody/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'root_complete_REPORT_VERDICT_read':True,'public_payload_count':185,'private_source_pins_authenticated':len(private),'input_pins_authenticated':len(inputs),'actual_operations_authenticated':ops,'nonzero_actual_operations_retained':[x for x in ops if x['exit_code']!=0],'pins':pins,'full_covering_prior_found':False,'bounded_modern_corpus_novelty_support':True,'priority_or_publication_clearance':False,'required_findings':v['required_findings'],'optional_findings':v['optional_findings'],'new_central_proof_search_turns':0,'workflow_estimate_percent':30}
(A/'ROOT_MODERN_PRIORITY_FAMILY_AUTHENTICATION_20261006.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['actual_operations_authenticated','pins','required_findings','optional_findings']}))
