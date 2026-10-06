from pathlib import Path
import json,hashlib,datetime,os
A=Path(__file__).resolve().parent;D=A/'priority_classical_confocal_mechanism_20261006'
def require(c,m):
 if not c:raise RuntimeError(m)
def check(p,row):
 b=p.read_bytes();require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'bodypin '+str(p));return b
manifest=json.loads((D/'OUTPUT_MANIFEST.json').read_text())
require(hashlib.sha256((D/'OUTPUT_MANIFEST.json').read_bytes()).hexdigest()=='c31ff3476ba625f91b7d15bea8a2097ec8d9c7aaf26f449fecafe0e7c6ce7869','sealedmanifest')
seen=set()
for row in manifest['payload']:
 p=D/row['path'];require(p.resolve().is_relative_to(D) and not p.is_symlink(),'path')
 require(row['path'] not in seen,'duplicate');seen.add(row['path'])
 require(not any(row['path'].startswith(prefix) for prefix in manifest['excluded_private_prefixes']),'privatebody')
 check(p,row)
require(len(seen)==115 and sum(r['bytes'] for r in manifest['payload'])==107208,'count')
seal=json.loads((D/'SEAL_RECEIPT.json').read_text())
for name in ['REPORT','VERDICT','OUTPUT_MANIFEST']:check(D/seal[name]['path'],seal[name])
v=json.loads((D/'VERDICT.json').read_text());require(not v['required_findings'] and not v['optional_findings'],'findings')
require(not v['covering_prior_found'] and v['classical_family_clearance'] and not v['combined_priority_clearance'] and not v['novelty_established'] and not v['publication_ready'],'boundedstatus')
inputs=json.loads((D/'INPUT_AUTHENTICATION.json').read_text())
for row in inputs['inputs']:check(Path(row['path']),row)
private=json.loads((D/'PRIVATE_SOURCE_CUSTODY.json').read_text())
for row in private['private_files']:check(Path(row['path']),row)
ops=json.loads((D/'ACTUAL_PROCESS_AUTHENTICATION.json').read_text())
for row in ops['actual_completed_operations']:
 p=D/row['receipt'];r=json.loads(p.read_text());require(r['child_PID']==row['actual_PID'] and r['exit_code']==row['exit_code']==0,'process')
 for name in ['stdout','stderr']:check(p.parent/r[name]['path'],r[name])
closing=D/'actual_operations/final_seal/execution.json';r=json.loads(closing.read_text());require(r['child_PID']==seal['actual_sealer_PID']==24461 and r['exit_code']==0,'sealer')
for name in ['stdout','stderr']:check(closing.parent/r[name]['path'],r[name])
for label,pid,opt in [('quantity_controls_normal',21078,0),('quantity_controls_optimized',21077,1)]:
 d=D/'actual_operations'/label;r=json.loads((d/'execution.json').read_text());v0=json.loads(check(d/r['stdout']['path'],r['stdout']))
 require(r['child_PID']==pid and v0['actual_operator_PID']==pid and v0['checks']==41 and v0['optimization']==opt and r['exit_code']==0 and r['stderr']['bytes']==0,'controls')
pins={}
for name in ['REPORT.md','VERDICT.json','OUTPUT_MANIFEST.json','SEAL_RECEIPT.json']:
 b=(D/name).read_bytes();pins[name]={'file':(D/name).relative_to(A.parents[2]).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
result={'schema':'pr110-root-classical-priority-complete-custody/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'root_complete_REPORT_VERDICT_read':True,'payload_count':115,'private_source_body_pins_authenticated':len(private['private_files']),'read_input_pins_authenticated':len(inputs['inputs']),'completed_actual_operations_authenticated':len(ops['actual_completed_operations']),'actual_normal_PID':21078,'actual_optimized_PID':21077,'explicit_checks_each':41,'actual_sealer_PID':24461,'required_findings':[],'optional_findings':[],'covering_prior_found':False,'bounded_classical_family_clearance':True,'priority_or_publication_clearance':False,'pins':pins,'new_central_proof_search_turns':0,'workflow_estimate_percent':30}
(A/'ROOT_CLASSICAL_PRIORITY_FAMILY_AUTHENTICATION_20261006.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='pins'}))

