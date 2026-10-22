#!/usr/bin/env python3
"""Independent read-only archive binding validator; no service calls."""
import hashlib,json,stat
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'adversary_01'
OLD_MANIFEST_PIN='aded476e358ec7fbbc02bda6c48f8dbdee2518d0475b3a8ee861ad11a80ad86d'
SOURCE_PIN='fc8ef5d6493c0088d94441e3a1876b9dc99bbaef84a98320647b84d15d5d048e'
def require(ok,label):
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
old_manifest_bytes=(OLD/'MANIFEST.json').read_bytes()
require(sha(old_manifest_bytes)==OLD_MANIFEST_PIN,'Original external manifest changed')
old_manifest=json.loads(old_manifest_bytes)
require(len(old_manifest['files'])==458,'Original member count changed')
require(set(old_manifest['explicit_public_allowlist'])==set(old_manifest['files']),'Original allowlist mismatch')
for filename,record in old_manifest['files'].items():
 b=(OLD/filename).read_bytes()
 require(sha(b)==record['sha256'] and len(b)==record['bytes'],'Original sealed member changed: '+filename)
require(set(x.relative_to(OLD).as_posix() for x in OLD.rglob('*') if x.is_file())==set(old_manifest['files'])|{'MANIFEST.json'},'Original directory inventory changed')
require(sha((HERE/'resweep_draft_statuses_900_1000.py').read_bytes())==SOURCE_PIN,'Supplement source pin mismatch')
require(sha((HERE.parents[1]/'resweep_draft_statuses_900_1000.py').read_bytes())==SOURCE_PIN,'Current source pin mismatch')
require(sha((HERE/'INDEPENDENT_HARNESS_BEFORE_REPAIR.py').read_bytes())==old_manifest['files']['independent_controls.py']['sha256'],'Pre-repair harness copy differs from sealed input')
old_names=[x['name'] for x in json.loads((OLD/'own_bound_actual0/INDEPENDENT_RESULTS.json').read_bytes())['tests']]
old_losses=[]
for prefix in ['actual','own_bound_actual']:
 for mode in range(3):
  folder=OLD/f'{prefix}{mode}'/'raw_receipts';raw=list(folder.iterdir())
  require(len(raw)==71,'Unexpected original raw file count')
  lost=json.loads((folder/'legacy_fresh_status_claimed_solved.json').read_bytes())
  require(lost['control']=='legacy_fresh_status_CLAIMED_SOLVED','Original collision evidence differs')
  old_losses.append({'run':f'{prefix}{mode}','retained_raw_files':71,'actual_controller_invocations':72,'lost_case':'legacy_fresh_status_claimed_solved','overwriting_case':'legacy_fresh_status_CLAIMED_SOLVED'})
summaries=[]
for mode in range(3):
 folder=HERE/f'actual{mode}';result=json.loads((folder/'INDEPENDENT_RESULTS.json').read_bytes())
 require(result['actual_python_optimization_level']==mode and result['source_sha256']==SOURCE_PIN,'Actual mode/source mismatch')
 require(result['passed']==84 and result['failed']==0 and result['actual_live_service_calls']==0 and result['unexpected_live_operation_attempts']==0,'Execution failure or live operation')
 tests=result['tests'];invocations=result['controller_invocations']
 require([x['name'] for x in tests]==old_names,'Subject testcase sequence changed')
 require(len(invocations)==result['actual_controller_invocations']==result['retained_raw_receipt_count']==72,'Invocation/raw count mismatch')
 require([x['index'] for x in invocations]==list(range(1,73)),'Invocation indices not contiguous')
 files=list((folder/'raw_receipts').iterdir());names=[x.name for x in files]
 require(len(files)==72 and len({x.casefold() for x in names})==72,'Case-insensitive raw collision')
 require(set(names)=={x['raw_filename'] for x in invocations},'Extra/missing raw receipt')
 bound=[]
 for test in tests:
  require(test['status']=='PASS','Named testcase did not pass')
  require(len(test['controller_invocation_indices']) in (0,1),'Expected one controller invocation or direct parser control')
  for index in test['controller_invocation_indices']:
   inv=invocations[index-1]
   require(inv['testcase']==test['name']==inv['control_label'],'Named test/invocation binding differs')
   bound.append(index)
 require(sorted(bound)==list(range(1,73)),'Testcase-to-invocation mapping not bijective')
 for inv in invocations:
  name=inv['raw_filename'];require(name.startswith(f"{inv['index']:04d}--") and '/' not in name and '\\' not in name,'Noncanonical indexed raw filename')
  path=folder/'raw_receipts'/name;st=path.lstat()
  require(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'Raw must be own regular copy')
  b=path.read_bytes();raw=json.loads(b)
  require(inv['retained'] and sha(b)==inv['raw_sha256'] and len(b)==inv['raw_bytes'],'Raw fingerprint mismatch')
  require(raw['control']==raw['actual_named_testcase']==inv['testcase'],'Exact case-sensitive raw testcase binding differs')
  require(raw['controller_invocation_index']==inv['index'] and raw['raw_receipt_filename']==name,'Raw index/name differs')
  require(raw['source_sha256']==SOURCE_PIN and raw['actual_python_optimization_level']==mode,'Raw source/mode differs')
  require(raw['actual_live_service_calls']==0 and raw['provenance'].startswith('OFFLINE SYNTHETIC'),'Raw provenance differs')
  receipt=raw['synthetic_controller_receipt'];require(receipt['pr_count']==101 and len(receipt['rows'])==101,'Not a complete synthetic controller receipt')
  require([x['pr'] for x in receipt['rows']]==list(range(900,1001)),'Synthetic numbered range differs')
  require(sum(x['kind']=='metadata' for x in raw['requests_to_synthetic_callable'])==2,'Two metadata snapshots not retained')
  require(all(not x['math_or_source_or_artifact_read'] and not x['remote_mutation'] for x in receipt['rows']),'Unexpected processing markers')
 case_records=[]
 for label,status,action in [('legacy_fresh_status_claimed_solved','claimed_solved','ELIGIBLE_REQUIRES_PROCESSING'),('legacy_fresh_status_CLAIMED_SOLVED','CLAIMED_SOLVED','SKIP_STATUS_ONLY')]:
  inv=next(x for x in invocations if x['testcase']==label)
  raw=json.loads((folder/'raw_receipts'/inv['raw_filename']).read_bytes())
  record=next(x for x in raw['synthetic_controller_receipt']['rows'] if x['pr']==952)
  require(record['status']==status and record['action']==action,'Distinct lower/upper status receipt invalid')
  case_records.append({'testcase':label,'index':inv['index'],'raw_filename':inv['raw_filename'],'status':record['status'],'action':record['action']})
 require(case_records[0]['raw_filename'].casefold()!=case_records[1]['raw_filename'].casefold(),'Case-distinct statuses still alias')
 summaries.append({'actual_optimization_mode':mode,'passed':84,'controller_invocations':72,'direct_parser_controls':12,'raw_receipts':72,'casefold_unique_raw_names':True,'bijective_testcase_invocation_raw_binding':True,'lower_and_upper_status_records':case_records})
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','original_manifest_sha256':OLD_MANIFEST_PIN,'all_original458_members_and_original_directory_inventory_unchanged':True,'source_sha256':SOURCE_PIN,'old_raw_evidence_loss':old_losses,'repaired_modes':summaries,'total_new_controller_invocations':216,'total_new_retained_raw_receipts':216,'total_new_passing_control_executions':252,'actual_live_service_calls':0}
with (HERE/'VERIFICATION.json').open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['utc','status','all_original458_members_and_original_directory_inventory_unchanged','total_new_controller_invocations','total_new_retained_raw_receipts','total_new_passing_control_executions','actual_live_service_calls']}))
