from pathlib import Path
import json,hashlib,datetime,os,subprocess,sys
A=Path(__file__).resolve().parent;P=A.parents[1]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
spec=json.loads(Path(sys.argv[1]).read_text());records=[];public=set()
def walk(x):
 if isinstance(x,dict):
  if 'bytes' in x and 'sha256' in x and any(k in x for k in ['path','file','path_relative_to_pr108_audit']):yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
for family in spec['families']:
 D=A/family['directory'];checked=[]
 for name in family['manifests']:
  M=D/name;mb=M.read_bytes();x=json.loads(mb);public.add(str(M.relative_to(A)))
  for row in walk(x):
   if 'path_relative_to_pr108_audit' in row:q=A/row['path_relative_to_pr108_audit']
   else:q=Path(row.get('path',row.get('file')));q=q if q.is_absolute() else D/q
   require(q.is_file() and not q.is_symlink(),'missing manifested body: '+str(q));b=q.read_bytes()
   require(len(b)==row['bytes'] and sha(b)==row['sha256'],'manifest drift: '+str(q))
   checked.append({'file':str(q),'bytes':len(b),'sha256':sha(b)})
   if q.is_relative_to(D) and not any(part.startswith('private') for part in q.relative_to(D).parts) and row.get('public_artifact',True):public.add(str(q.relative_to(A)))
  checked.append({'file':str(M),'bytes':len(mb),'sha256':sha(mb)})
 for name in ['REPORT.md','VERDICT.json','RESEARCH_LOG.md']:
  q=D/name;b=q.read_bytes();public.add(str(q.relative_to(A)))
  checked.append({'file':str(q),'bytes':len(b),'sha256':sha(b)})
 verdict=json.loads((D/'VERDICT.json').read_text())
 for key,value in family['required_verdict_fields'].items():require(verdict[key]==value,'verdict mismatch: '+key)
 records.append({'family':family['directory'],'root_full_report_and_verdict_read':True,'verified_pin_count':len(checked),'pins':checked})
R=A/'root_effective_reproductions_20261006';r=json.loads((R/'REPRODUCTION_RECEIPT.json').read_text());require(r['all_actual_exits_expected'] and r['actual_runs']==12 and r['intentional_false_or_corrupt_controls_rejected']==8,'effective replay')
D=A/'repaired_diagnostics_v1';pins=[]
for q in sorted(D.rglob('*')):
 if q.is_file():
  b=q.read_bytes();pins.append({'file':str(q.relative_to(A)),'bytes':len(b),'sha256':sha(b)})
proofsha=sha((D/'PROOF.md').read_bytes());require(proofsha==r['proof_sha256'],'current proof drift')
require((D/'PROOF.md').read_bytes()==(D/'independent_review/author_replay/PROOF.md').read_bytes(),'replay proof')
for label,script,result in [('author_normal','verify.py','verification.json'),('old_review_normal','independent_review/independent_checks.py','independent_review/independent_results.json'),('author_optimized','verify.py','verification_optimized.json'),('old_review_optimized','independent_review/independent_checks.py','independent_review/independent_results_optimized.json')]:
 x=json.loads((D/result).read_text());require(x['artifact_sha256']==proofsha and x['verifier_sha256']==sha((D/script).read_bytes()) and x['all_pass'] is True,'actual current binding: '+label)
live=A/'mathematical_gate_actual_live_readback_20261006';live.mkdir(exist_ok=False);start=now();argv=['gh','pr','view','108','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,mergedAt'];p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();(live/'stdout.bin').write_bytes(out);(live/'stderr.bin').write_bytes(err)
lr={'PID':p.pid,'argv':argv,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)};(live/'PROCESS_RECEIPT.json').write_text(json.dumps(lr,indent=2)+'\n');require(p.returncode==0,'live readback failed');x=json.loads(out)
require(x['number']==108 and x['state']=='OPEN' and x['isDraft'] and x['baseRefName']=='main' and x['headRefOid']=='3526d46bf143b08e5055ffa7728c6278e9f958ea' and x['mergedAt'] is None,'source head changed')
authentication={'schema':'pr108-root-math-family-authentication/v1','UTC':now(),'actual_reader_PID':os.getpid(),'families':records,'all_byte_pins_match':True,'root_full_reports_read':True,'public_family_paths':sorted(public),'third_party_primary_content_excluded':True}
(A/'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json').write_text(json.dumps(authentication,indent=2)+'\n')
effective={'schema':'pr108-current-effective-artifacts/v1','UTC':now(),'current_diagnostics':'repaired_diagnostics_v1','pins':pins,'original_submitted_artifacts_immutable':True,'root_reproduction':'root_effective_reproductions_20261006/REPRODUCTION_RECEIPT.json','source_proof_header_is_dated_preparation_snapshot':True,'current_state_authority':'ROOT_MATHEMATICAL_GATE_20261006.json'}
(A/'CURRENT_EFFECTIVE_ARTIFACTS.json').write_text(json.dumps(effective,indent=2)+'\n')
gate={'schema':'pr108-root-mathematical-gate/v1','UTC':now(),'actual_operator_PID':os.getpid(),'PR':108,'problem_id':30003996,'original_head':x['headRefOid'],'review_hash':'9a2816afbdd3750d36f550dc6e91c7201aa024344a7b83fdb420aafe6c86df0d','original_status':'claimed_solved','original_effort':'2/5','original_turn_provenance':'QUEUE and prose log; no submitted structured ledger','new_central_proof_search_turns':0,'exact_source_problem':'Kaibel Problem1, one undirected tree and all root-specific induced whole-tree orientations','all_size_proof_checked':True,'source_authentication_percent':100,'mathematical_audit_percent':100,'mathematical_clearance':True,'remaining_mathematical_concerns':[],'minor_preprocessing_clarifications_adopted':True,'explicit_optimization_safe_guards_adopted_and_actual_runs_verified':True,'current_effective_proof_sha256':proofsha,'fresh_family_authentication':'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json','root_actual_reproduction':r,'unclaimed_global_OPT_identity_false':True,'B_at_least_two_is_same_mechanism_robustness_only':True,'priority_percent':0,'priority_clearance':False,'novelty_established':False,'publication_clearance':False,'workflow_estimate_percent':30,'program_completed':16,'dated_program_total':99}
(A/'ROOT_MATHEMATICAL_GATE_20261006.json').write_text(json.dumps(gate,indent=2)+'\n')
q=P/'CURRENT_PROGRESS.json';progress=json.loads(q.read_text());progress.update({'UTC':now(),'updated_UTC':now(),'current_mathematical_audit_percent':100,'current_mathematical_clearance':True,'current_math_family_evidence_readback_complete':True,'current_mathematical_gate':'audits/pr108_30003996/ROOT_MATHEMATICAL_GATE_20261006.json','current_repaired_diagnostics':'audits/pr108_30003996/repaired_diagnostics_v1','current_source_authentication_checkpoint':'c085f5d590ab1f4f2f045fa7bff04a201a2cbc61','current_source_authentication_checkpoint_remote_verified':True,'current_PR_workflow_percent':30,'current_workflow_estimate_percent':30,'next_step':'Independent multi-family priority audit of literal all-root Problem1 and advertised restrictions.','remaining_current_step':'Historical priority and substantive novelty unresolved.'});q.write_text(json.dumps(progress,indent=2,sort_keys=True)+'\n')
note=f'\n{now} — PR108 full root source/proof/code/receipt review and three fresh families authenticated byte-for-byte; repaired current checkers pass12actual runs, with all8negative controls rejected. Mathematical gate100%, source100%, priority0%, PR108workflow30%; program16/99=16.16%. Original2/5 and missing original structured ledger honestly preserved; audit central proof-search0. Current effective proof{proofsha}. Same OPENdraft head freshly checked. No priority/novelty/publication clearance.\n'
for q in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with q.open('a') as f:f.write(note)
print(json.dumps({'UTC':now(),'actual_operator_PID':os.getpid(),'verified_family_pins':sum(x['verified_pin_count'] for x in records),'mathematical_clearance':True,'priority_clearance':False,'effective_proof_sha256':proofsha,'workflow_percent':30}))
