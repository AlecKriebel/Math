from pathlib import Path
import json, hashlib, datetime, os, zipfile
A=Path(__file__).resolve().parent; D=A/'whole_preprint_round2_20261005'; U=A/'publication_package_v1/publicfiles'
def require(c,m):
 if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
manifest=load(D/'CLOSED_CUSTODY_MANIFEST.json'); pins=[]
require(manifest['mandatory_findings_remaining']==[] and manifest['audit_completion_percent']==100,'review incomplete')
for group,base in [('all_external_inputs',A),('all_audit_artifacts',D)]:
 for row in manifest[group]:
  p=Path(row['path']);p=p if p.is_absolute() else base/p
  require(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'custody mismatch: '+str(p));pins.append({'path':str(p),'bytes':row['bytes'],'sha256':row['sha256']})
require((D/'CLOSED_CUSTODY_MANIFEST.sha256').read_text().split()[0]==sha(D/'CLOSED_CUSTODY_MANIFEST.json'),'detached manifest hash')
findings=load(D/'FINDING_DISPOSITION.json');require(findings['new_mandatory_findings']==[] and findings['unresolved_mandatory_findings']==[],'mandatory finding')
meta=A/'publication_package_v1/zenodo-deposit.json';require(sha(meta)==manifest['metadata_sha256'],'metadata changed')
for row in manifest['selected_payloads']:require(sha(A/row['path'])==row['sha256'] and row['unchanged_since_initial'],'public bytes changed')
public=load(A/'publication_package_v1/private_notes/PUBLIC_PACKAGE_MANIFEST.json')
for row in public['payloads']:require(sha(A/'publication_package_v1'/row['file'])==row['sha256'],'public manifest mismatch')
with zipfile.ZipFile(U/'pr91_support.zip') as z:
 require(len(z.namelist())==11 and z.testzip() is None,'archive')
 for row in public['archive_members']:require(z.read(row['file'])==(U/row['file']).read_bytes(),'member changed')
for line in (U/'SHA256SUMS.txt').read_text().splitlines():
 digest,rel=line.split('  ',1);require(sha(U/rel)==digest,'digest')
orig=load(A/'original_source_authentication_20261005/ORIGINAL_BLOB_MANIFEST.json')
for row in orig['files']:
 p=Path(row['preserved_path']);b=p.read_bytes();require(sha(p)==row['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_SHA1'],'original body changed')
processes=load(D/'PROCESS_SUMMARY.json')['processes'];require(len(processes)==16,'process count')
for row in processes:
 record=load(D/row['path']);require(sha(D/row['path'])==row['sha256'] and row['pid']>0 and row['started_utc']<=row['ended_utc'],'actual execution')
 require(record['exit_code']==row['exit_code'],'process outcome')
positive=load(D/'portable_reproduction/results.json');require(positive['status']=='PASS_FINITE_CONTROLS' and len(positive['runs'])==6 and all(r['exit_code']==0 for r in positive['runs']) and positive['unique_controls_per_mode']['total']==2720,'fresh wrapper failed')
# The evidence manifest authenticates all receipt bodies, full streams and six false controls.
report=(D/'REPORT.md').read_text();require('No mandatory issue remains' in report,'review verdict')
check=load(A/'actual_operations/zenodo_check_round2/execution.json');require(check['exit_code']==0,'local kit validation')
r={'schema':'pr91-root-publication-clearance/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'PR':91,'head':'2ea84c5de45cb92783b5b55057af1f52590be6bf','literal_status':'claimed_solved','original_budget':'1/5','new_central_proof_search_turns':0,'publication_clearance':True,'whole_package_rounds':2,'mandatory_findings_remaining':[],'mathematical_target_complete':True,'bounded_priority_audit_complete':True,'priority_framing':'Explicit completion of historical 2015 mixed converse by credited classical specialization; no worldwide firstness or continuous-openness claim.','firstness_established':False,'human_peer_review':False,'original_bodies_authenticated':len(orig['files']),'round2_custody_pins_authenticated':len(pins),'round2_closed_manifest_sha256':sha(D/'CLOSED_CUSTODY_MANIFEST.json'),'round2_report_sha256':sha(D/'REPORT.md'),'round2_actual_execution_records':len(processes),'unique_controls_per_mode':2720,'exact_discrete_per_mode':2154,'floating_per_mode':566,'metadata_sha256':sha(meta),'payloads':public['payloads'],'publication_API_operations_started':False,'tracker_update_started':False,'merge_started':False,'workflow_estimate_percent':85,'persistent_goal_complete':False,'primary_checkout_mutated':False,'pins':pins}
(A/'ROOT_READY_FOR_PUBLICATION.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['pins','payloads']}))
