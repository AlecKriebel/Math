from pathlib import Path
import datetime,hashlib,json,os,shutil
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(c,m):
 if not c:raise RuntimeError(m)
families=[('reduction_all_trees_adversary_20261006','MANIFEST.json'),('source_objective_complexity_adversary_20261006','SHA256_BYTES_MANIFEST.json'),('independent_reproduction_adversary_20261006','MANIFEST.json')]
records=[];public_outputs=[]
for name,mfile in families:
 F=A/name;manifest=load(F/mfile);checked=[]
 for kind in ['inputs','outputs','input_files','output_files']:
  for pin in manifest.get(kind,[]):
   path=Path(pin.get('path',pin.get('file','')))
   if not path.is_absolute():path=F/path
   require(path.is_file() and not path.is_symlink(),'missing/nonregular pin: '+str(path))
   require(path.stat().st_size==pin['bytes'] and sha(path)==pin['sha256'],'family pin mismatch: '+str(path))
   checked.append({'path':str(path),'bytes':pin['bytes'],'sha256':pin['sha256'],'kind':kind})
   if kind in ['outputs','output_files']:
    require(path.is_relative_to(F),'foreign output')
    if path.suffix.lower() not in ['.png','.pdf'] and path.name not in ['source_kaibel_full.txt'] and '__pycache__' not in path.parts:public_outputs.append(str(path.relative_to(C)))
 require(any(x['path'].endswith('/original_attempt/PROOF.md') and x['sha256']=='2c219bf80ad4bbba75f8c70169b26b7e9b11b6f5e1742543f25d9cb0d0c5ebe8' for x in checked),'candidate was not pinned')
 public_outputs.append(str((F/mfile).relative_to(C)))
 records.append({'family':name,'manifest_file':mfile,'manifest_sha256':sha(F/mfile),'checked_pins':checked,'report_sha256':sha(F/'REPORT.md'),'verdict':load(F/'VERDICT.json')})
validation=load(A/'repaired_diagnostics_validation_v2_20261006/VERDICT.json');require(validation['status']=='PASS' and validation['actual_runs']==8,'root repair validation')
R=A/'repaired_diagnostics_v1';D=A/'repaired_diagnostics_validation_v2_20261006'
for name,i in [('verification.json',0),('independent_results.json',4)]:
 raw=(D/(str(i)+'.stdout.bin')).read_bytes();require(raw==(D/(str(i+2)+'.stdout.bin')).read_bytes(),'normal/optimized byte drift');(R/name).write_bytes(raw)
require(load(R/'verification.json')['checker_sha256']==sha(R/'verify.py') and load(R/'verification.json')['artifact_sha256']==sha(R/'PROOF.md'),'current diagnostic metadata')
require(sha(R/'PROOF.md')=='0c2783ca865108ad7abb31eda65f60cb997840b1dd42a0bc98cee3f08a406132','clarified proof changed')
old=A/'original_source_authentication_20261006/original_attempt';require(sha(old/'PROOF.md')=='2c219bf80ad4bbba75f8c70169b26b7e9b11b6f5e1742543f25d9cb0d0c5ebe8','original proof mutation')
require([json.loads(s)['turn'] for s in (old/'turns.jsonl').read_text().splitlines()]==[1],'original effort ledger')
resolved={'all_tree_minor_boundary_presentation':{'status':'resolved','artifact':'repaired_diagnostics_v1/PROOF.md','diff':'repaired_diagnostics_v1/preprocessing_clarification.diff','central_mechanism_changed':False},
 'C1_optimized_assert_bypass':{'status':'resolved_in_effective_audit_package','author_sites':2,'old_independent_sites':1,'root_actual_normal_and_optimized_runs':8,'regenerated_current_receipts':True,'candidate_proof_mechanism_changed':False},
 'stale_background_problem1_description':{'status':'literal_source_controls_current_scope','immutable_original_source_preserved':True,'future_publication_must_describe_Problem2_only':True}}
t=now();auth={'schema':'pr107-root-math-family-authentication/v1','UTC':t,'actual_operator_PID':os.getpid(),'families':records,'all_pins_match':True,'public_family_outputs':sorted(set(public_outputs))};dump(A/'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json',auth)
gate={'schema':'pr107-root-mathematical-gate/v1','UTC':t,'actual_operator_PID':os.getpid(),'PR':107,'problem_id':30003997,'original_head':'cc2ae01897135b35bee135917819e782a220f2c1',
 'source_authentication_complete':True,'original_literal_status':'claimed_solved','original_budget':'1/5','new_central_proof_search_turns':0,
 'three_independent_math_families_authenticated':True,'full_reports_read_by_root':True,'mathematical_audit_percent':100,'mathematical_clearance':True,
 'exact_claim':'Literal fixed-root destination-specific path-cost arborescence Problem2: NP-complete zero-threshold binary-cost subclass on simple reachable depth-three consecutive-layer DAGs of nonroot indegree at most3; strongly NP-hard optimization, also strictly positive costs1/2 with polynomial threshold.',
 'current_clarified_proof_sha256':sha(R/'PROOF.md'),'original_immutable_proof_sha256':sha(old/'PROOF.md'),'current_author_checker_sha256':sha(R/'verify.py'),'current_independent_checker_sha256':sha(R/'independent_checks.py'),
 'resolved_corrections':resolved,'unresolved_mathematical_concerns':[], 'priority_clearance':False,'priority_audit_percent':0,'publication_clearance':False,'human_peer_review':False,
 'strongest_verified_scope':'Full literal source Problem2 with stated graph/numeric restrictions. No new result for duplicate30003998, distinct Problem1, a Wong polyhedral equivalence or approximation threshold.',
 'bounded_computations_do_not_replace_arbitrary_size_proof':True,'PR_source_branch_repair_or_later_native_integration_pending':True,'workflow_estimate_percent':25,'program_completion_percent':15/99*100}
dump(A/'ROOT_MATHEMATICAL_GATE_20261006.json',gate)
progress=load(P/'CURRENT_PROGRESS.json');require(progress['current_PR']==107 and progress['fully_completed_count']==15,'progress cursor')
progress.update(UTC=t,updated_UTC=t,current_mathematical_audit_percent=100,current_mathematical_clearance=True,current_mathematical_gate='audits/pr107_30003997/ROOT_MATHEMATICAL_GATE_20261006.json',current_math_family_evidence_readback_complete=True,current_repaired_diagnostics='audits/pr107_30003997/repaired_diagnostics_v1',
 current_source_authentication_checkpoint='f0fcafb70260b672d0a050dc945effb04867f020',current_source_authentication_checkpoint_remote_verified=True,current_PR_workflow_percent=25,current_workflow_estimate_percent=25,
 current_priority_audit_percent=0,current_priority_clearance=False,current_publication_ready=False,next_step='Launch deep independent priority families for the verified PR107 result.',remaining_current_step='Historical novelty and prior-resolution audit; no publication or merge clearance.')
dump(P/'CURRENT_PROGRESS.json',progress)
line=t+' — PR107 source and mathematical gate complete after three independent fully authenticated families. All-tree reduction, real/rational decision distinctions, dense encoding, numerical strong hardness and every graph restriction verified. Required minor total-input presentation clarified in current proof; optimized assert bypass repaired at3 sites; current code/proof receipts regenerated and8 ROOT normal/optimized positive/false-control runs passed. Immutable original proof/head/1-of5 ledger preserved; added proof-search0. Mathematics100%, priority0%, PR107workflow25%; program15/99=15.15%. Deep priority audit next; no novel-resolution publication/merge clearance.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+line)
paths=set(public_outputs)
for name in ['ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json','ROOT_MATHEMATICAL_GATE_20261006.json','authenticate_math_gate.py','propagate_diagnostic_repair.py','validate_repaired_diagnostics.py','validate_repaired_diagnostics_v2.py','DIAGNOSTIC_REPAIR_PROPAGATION_20261006.json','RESEARCH_LOG.md','INTAKE_CHECKPOINT_SELECTION_20261006.json']:paths.add(str((A/name).relative_to(C)))
for folder in [R,A/'repaired_diagnostics_validation_20261006',D]:
 for p in folder.rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:paths.add(str(p.relative_to(C)))
for label in ['record_intake','intake_release','diagnostic_repair_propagation','diagnostic_repair_validation','diagnostic_repair_validation_v2']:
 for p in (A/'actual_operations'/label).iterdir():
  if p.is_file():paths.add(str(p.relative_to(C)))
for name in ['RECEIPT.json','PROCESS_JOURNAL.json']:paths.add(str((A/'actual_checkpoints/intake_release'/name).relative_to(C)))
oldA=P/'audits/pr104_600008'
for name in ['cleanup_private_backend.py','PRIVATE_BACKEND_CLEANUP_RECEIPT_20261006.json']:paths.add(str((oldA/name).relative_to(C)))
for p in (oldA/'actual_operations/cleanup_private_backend').iterdir():
 if p.is_file():paths.add(str(p.relative_to(C)))
paths.update([str((P/'CURRENT_PROGRESS.json').relative_to(C)),str((P/'RESEARCH_LOG.md').relative_to(C))])
dump(A/'MATH_CHECKPOINT_SELECTION_20261006.json',{'UTC':t,'paths':sorted(paths),'expected_main_parent':'f0fcafb70260b672d0a050dc945effb04867f020','private_primary_PDF_images_and_full_extracts_excluded':True})
print(json.dumps({'mathematical_clearance':True,'all_pin_authentication_complete':True,'math_percent':100,'workflow_percent':25,'selected_paths':len(paths),'public_checkpoint_bytes':sum((C/p).stat().st_size for p in paths),'priority_clearance':False}))
