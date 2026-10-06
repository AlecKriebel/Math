#!/usr/bin/env python3
"""R2 complete JSON/custody semantic audit, distinct from copied runner checks."""
from pathlib import Path
import hashlib,json,os,datetime
O=Path(__file__).resolve().parent;A=O.parent;D=A/'publication_ready_package_v2';N=0
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ck(x,msg):
 global N
 if not x:raise RuntimeError(msg)
 N+=1
def load(p):return json.loads(p.read_text())
read=[]
for p in sorted(D.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();kind=p.suffix
 if kind=='.json':load(p)
 elif kind not in ('.pdf','.zip'):b.decode('utf-8')
 read.append(dict(path=p.relative_to(D).as_posix(),bytes=len(b),sha256=H(p),scope='complete parsed JSON plus semantic audit' if kind=='.json' else 'complete decoded text/code content' if kind not in ('.pdf','.zip') else 'complete archive byte/member checks' if kind=='.zip' else 'all4 actual rendered pages visually read, full PDF byte hash; object inspection'))
# All provenance copies retain exact authenticated authored bodies.
for dst,src in [('source_preparation/provenance/R1_REPORT.md','whole_publication_package_round1_20261006/REPORT.md'),('source_preparation/provenance/R1_VERDICT.json','whole_publication_package_round1_20261006/VERDICT.json'),('source_preparation/provenance/R1_REVIEW_MANIFEST.json','whole_publication_package_round1_20261006/REVIEW_MANIFEST.json'),('source_preparation/provenance/ROOT_MATHEMATICAL_GATE_20261006.json','ROOT_MATHEMATICAL_GATE_20261006.json'),('source_preparation/provenance/ROOT_PRIORITY_GATE_20261006.json','ROOT_PRIORITY_GATE_20261006.json'),('source_preparation/provenance/V1_SOURCE_PREPARATION_MANIFEST.json','publication_package_v1/SOURCE_PREPARATION_MANIFEST.json'),('source_preparation/provenance/V1_SEAL.json','publication_package_v1/SEAL.json')]:ck((D/dst).read_bytes()==(A/src).read_bytes(),'preserved_provenance_copy_'+dst)
ck((D/'source_preparation/historical/PROOF.md').read_bytes()==(D/'source_preparation/historical/independent_review/author_replay/PROOF.md').read_bytes(),'identical_historical_proof_duplicate')
binding=load(D/'source_preparation/PROOF_BINDING.json')
for key,pathkey in [('paper_sha256','paper_relative_path'),('historical_proof_sha256','historical_proof_relative_path')]:ck(binding[key]==H(D/'source_preparation'/binding[pathkey]),'portable_binding_'+key)
for k,p in [('current_verifier_sha256','verify_exact.py'),('current_runner_sha256','run_checks.py')]:ck(binding[k]==H(D/'source_preparation'/p),'code_binding_'+k)
old=load(D/'source_preparation/provenance/V1_SOURCE_PREPARATION_MANIFEST.json');ck(len(old['files'])==26 and sum(r['bytes'] for r in old['files'])==129509,'historical_V1_manifest_arithmetic')
for r in old['files']:ck(H(A/'publication_package_v1'/r['relative_path'])==r['sha256'] and (A/'publication_package_v1'/r['relative_path']).stat().st_size==r['bytes'],'historical_V1_retained_pin')
corr=load(D/'source_preparation/CORRECTION_LEDGER.json')
for row in corr['R1_bindings']:ck(H(A/row['relative_to_audit'])==row['sha256'] and (A/row['relative_to_audit']).stat().st_size==row['bytes'],'correction_R1_exact_pin')
for r in corr['paper_and_metadata_historical_preserved_exact']:ck(H(D/'source_preparation'/r['relative_path'])==r['sha256'],'correction_unchanged_pin')
ck(corr['current_checks_per_valid_mode']==2727845 and corr['current_formula_parameter_cases']==397 and corr['current_tree_formula_parameter_cases']==74997,'current_correction_counts')
ck(corr['actual_run_receipt_sha256']==H(D/'source_preparation/verification_results/actual_run_receipt.json'),'correction_receipt_pin')
# Complete original and fresh run-receipt objects are checked, and all process
# positive stdout hashes can be reconstructed exactly from included report objects.
summary=[]
for p in [D/'source_preparation/verification_results/actual_run_receipt.json',D/'root_verified_reproduction.json',O/'receipts/runner_normal_internal.json',O/'receipts/runner_optimized_internal.json']:
 r=load(p);ck(r['all_pass'] and r['normal_and_optimized_counts_identical'],'run_status');ck(r['runner_sha256']==binding['current_runner_sha256'],'runner_current');s=r['actual_subprocesses'];ck(len(s)==18 and len({x['actual_PID'] for x in s})==18,'18_distinct_actual_processes');ck(r['intentional_controls_rejected']==12,'12_controls')
 positive=[x for x in s if x['actual_exit']==0];negative=[x for x in s if x['actual_exit']==1];ck(len(positive)==6 and len(negative)==12,'6_positive_12_negative')
 for j,x in enumerate(s):
  ck(x['actual_exit']==x['expected_exit'],'actual_exit_matches');ck(isinstance(x['actual_PID'],int) and x['actual_PID']>0 and len(x['argv'])>=2,'process_PID_argv');ck(datetime.datetime.fromisoformat(x['start_UTC'])<=datetime.datetime.fromisoformat(x['end_UTC']),'process_time_order')
  if j:ck(datetime.datetime.fromisoformat(s[j-1]['end_UTC'])<=datetime.datetime.fromisoformat(x['start_UTC']),'sequential_process_order')
  if x['actual_exit']==1:ck(x['expected_guard_present'] and x['stdout_bytes']==0 and x['stderr_bytes']>0,'negative_control_actual_semantics')
  else:ck(x['stderr_bytes']==0,'positive_no_stderr')
 reports=r['verification_reports'];ck(len(reports)==2,'two_positive_verifier_reports')
 for mode,rep in enumerate(reports):
  ck(rep['python_optimization_level']==mode and rep['total_checks']==sum(rep['checks'].values())==2727845,'metric_count_and_optimization');ck(rep['formula_parameter_cases']==397 and rep['tree_formula_parameter_cases']==74997,'formula_tree_case_counts');ck(rep['paper_sha256']==binding['paper_sha256'] and rep['historical_proof_sha256']==binding['historical_proof_sha256'] and rep['verifier_sha256']==binding['current_verifier_sha256'],'positive_report_bound');x=positive[mode];ck(rep['actual_operator_PID']==x['actual_PID'],'child_report_PID_corresponds');b=(json.dumps(rep,sort_keys=True)+'\n').encode();ck(len(b)==x['stdout_bytes'] and hashlib.sha256(b).hexdigest()==x['stdout_sha256'],'positive_stdout_exact_reconstruction')
 trim=lambda t:{k:v for k,v in t.items() if k not in ['UTC','actual_operator_PID','python_optimization_level']}
 ck(trim(reports[0])==trim(reports[1]),'normal_optimized_full_equal')
 hs=r['historical_scratch_replays'];ck(len(hs)==4 and [x['assertions'] for x in hs]==[78056,600122,78056,600122],'historical_counts')
 for i,h in enumerate(hs):
  ck(h['all_pass'] and h['artifact_sha256']==binding['historical_proof_sha256'],'historical_proof_binding'); ck(h['verifier_sha256']==H(D/'source_preparation/historical'/('verify.py' if i%2==0 else 'independent_review/independent_checks.py')),'historical_code_binding')
  if i%2:ck(h['assertions']==sum(h['checks'].values()) and h['statistics']['tree_formula_cases']==h['statistics']['canonical_trees']+h['statistics']['noncanonical_trees'],'historical_metric_arithmetic')
  b=((json.dumps(h) if i%2==0 else json.dumps(h,indent=2))+'\n').encode();x=positive[2+i];ck(len(b)==x['stdout_bytes'] and hashlib.sha256(b).hexdigest()==x['stdout_sha256'],'historical_stdout_exact_reconstruction')
 summary.append(dict(path=str(p),bytes=p.stat().st_size,sha256=H(p),processes=[{k:v for k,v in x.items() if k!='argv'}|{'argv_script':next((Path(a).name for a in x['argv'] if a.endswith('.py')),None),'optimization':'-O' in x['argv'],'control':x['argv'][-1] if '--negative-control' in x['argv'] else None} for x in s],metrics=trim(reports[0])))
rootreceipt=A/'ROOT_READY_PACKAGE_REPRODUCTION_V2_20261006.json';ck(rootreceipt.read_bytes()==(D/'root_verified_reproduction.json').read_bytes(),'root_reproduction_exact_copy')
wrapper=A/'actual_operations/publication_ready_package_reproduction_v2';w=load(wrapper/'execution.json');ck(w['exit_code']==0 and w['child_PID']==load(rootreceipt)['actual_operator_PID'],'root_wrapper_exact_PID_exit')
for k in ['stdout','stderr']:ck((wrapper/w[k]['path']).stat().st_size==w[k]['bytes'] and H(wrapper/w[k]['path'])==w[k]['sha256'],'root_wrapper_'+k+'_bytes')
w=load(D/'source_preparation/verification_results/runner_execution.json');ck(w['exit']==0 and w['actual_runner_PID']==load(D/'source_preparation/verification_results/actual_run_receipt.json')['actual_operator_PID'],'source_wrapper_PID_exit')
for k in ['stdout','stderr']:
 p=D/'source_preparation'/w[k+'_relative_path'];ck(p.stat().st_size==w[k+'_bytes'] and H(p)==w[k+'_sha256'],'source_wrapper_'+k+'_bytes')
for r in load(D/'source_preparation/provenance/INPUT_READ_BINDINGS.json')['records']:
 p=A/r['path_relative_to_audit'];ck(p.stat().st_size==r['bytes'] and H(p)==r['sha256'],'recorded_read_binding_'+r['path_relative_to_audit'])
# Historical R1 review manifest inventory refers to its own outputs, not the
# current package; check all retained report artifacts named by its schema.
r1=load(D/'source_preparation/provenance/R1_REVIEW_MANIFEST.json')
for r in r1['files']:
 name=r.get('relative_path',r.get('path'));p=A/'whole_publication_package_round1_20261006'/name;ck(p.stat().st_size==r['bytes'] and H(p)==r['sha256'],'R1_review_manifest_retained_bytes')
result=dict(schema='pr108-fresh-r2-provenance-diagnostics/v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_PID=os.getpid(),checks=N,all_pass=True,complete_payload_read=read,complete_run_receipts=summary,custody_limit='Negative subprocess raw stderr not separately retained by portable runner; its actual guard checks and hashes are inspected and freshly reproduced. Included positive stdout is independently reconstructed exactly. Early read tool PIDs were unexposed and are not invented.')
(O/'PROVENANCE_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(all_pass=True,checks=N,complete_payload_files=len(read),run_receipts=len(summary))))
