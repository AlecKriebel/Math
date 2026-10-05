"""Prepare exact public-safe checkpoint bodies and an exclusive local scope."""
import ast,copy,datetime,hashlib,json,os,pathlib,stat,sys,uuid
A=pathlib.Path(__file__).resolve().parent;P=A.parent.parent;R=P.parent
D=P/'audits/pr305_5100034/root_during_peer_pause_20261005'
W=A/'math_checkpoint_036_preparation';assert not W.exists();W.mkdir()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(p.stat().st_mode)))
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
assert not sys.flags.optimize
gate=json.loads((A/'ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json').read_bytes())
assert gate['status']=='PASS_ROOT_PR302_PRECISE_MATHEMATICAL_GATE' and gate['mandatory_mathematical_findings']==0 and gate['priority_unestablished']
intake=json.loads((P/'intake_after_pr305_20261005/INTAKE.json').read_bytes())
assert [x['number'] for x in intake['records']]==[304,303,302] and intake['eligible']['original_head']==gate['original_head']
token=str(uuid.uuid4());stamp=utc()
status=dict(UTC=stamp,PR=302,original_head=gate['original_head'],original_submitted_status='claimed_solved',original_author_turn_count='2/5',mathematics_percent=100,priority_percent=0,workflow_percent=30,mathematical_gate='ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json',mandatory_mathematical_findings=0,strongest_verified_result=gate['strongest_verified_result'],priority_audit_started=True,priority_families=['/root/pr302_priority_target_01','/root/pr302_priority_mechanism_01'],historical_firstness_certified=False,preprint_ready=False,publication_ready=False,merged=False,remaining_gap=gate['remaining_gap'])
write(A/'CURRENT_AUDIT_STATUS.json',status)
(A/'README.md').write_text('''# PR302: smooth fixed-lag diffusion tensor consistency

Original submitted PR head `eb6e0e999521d84a65f9857d338cad76b84d30db`, original
status `claimed_solved`, author history2/5. The immutable original packet is
under `snapshot/`. The current ROOT mathematical gate accepts the explicitly
stated smooth stationary reversible conormal model after three independently
frozen adversarial families and original-control reproduction. Mathematics100%,
priority0%, workflow30%. Historical priority, preprint, publication and merge
are still unaccepted.

The result is almost-sure local uniform recovery of S and separately fitted
div S, plus global L2 recovery of the clipped tensor, from exact fixed-positive-
lag observations with unknown density on a known connected smooth domain and
known positive class bounds. It is not a rate theorem or a rough-model,
sensor-noise or approximate numerical implementation result. Finite controls
supplement the analytic proof and do not prove its infinite-dimensional or
probabilistic steps. ROOT_MATHEMATICAL_RECONSTRUCTION.md records the independent
analytic reconstruction; ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json closes its
previously pending review gate.

The committed review subset includes reports, proof/control programs, output
receipts and whole-body inventories. Those inventories intentionally also
bind local-only primary PDFs, extracted text, runtime inputs and complete
native tapes; their presence in an inventory does not assert redistribution.
Third-party primary PDFs and text extractions stay private. Historical failed
helper runs and metadata corrections remain disclosed; no historical proof
or closed review body is rewritten.
''')
x=json.loads((P/'inventory.json').read_bytes());original=copy.deepcopy(x)
for rec in intake['records']:
 e=next(v for v in x['items'] if v['number']==rec['number'])
 e.update(submitted_status=rec['original_status'],original_submitted_status=rec['original_status'],eligibility_checked_head=rec['original_head'],eligibility_checked_utc=rec['eligibility_checked_UTC'])
 if rec['number']!=302:e.update(disposition='skipped_original_status_without_processing',no_mathematical_or_priority_or_other_processing=True)
 else:e.update(original_author_turn_count='2/5',audit='draft_pr_descending_audit_20261002/audits/pr302_30003508/',mathematical_acceptance=True,mathematical_verification_percent=100,bounded_priority_percent=0,workflow_percent=30,audit_workflow_percent=30,disposition='mathematics_verified_precise_smooth_class_priority_pending',priority_acceptance=False,preprint_ready=False,publication_ready=False,current_audit_status='audits/pr302_30003508/CURRENT_AUDIT_STATUS.json',historical_first_priority_certified=False)
assert all(e==next(v for v in original['items'] if v['number']==e['number']) for e in x['items'] if e['number'] not in [304,303,302])
assert x['completed_by_descending']==27 and len(x['claimed_solved_published_by_descending'])==8
write(W/'inventory.json',x)
(W/'RESEARCH_LOG.md').write_bytes((P/'RESEARCH_LOG.md').read_bytes()+('\n'+stamp+' — PR305 exact completion checkpoint8b59507d997563baa58dbf6c6579b26e239ea005 verified and closed; peer PR85 exact55-path checkpoint2e0162fbb5773d0c1b41bfaa9f461bc474338902 and explicit release independently verified operationally only. Descending status-only intake skips304 unsolved and303 already_solved without processing. PR302 original claimed_solved2/5 is the next eligible head. Three NEW independently frozen mathematical families close with zero mandatory findings; ROOT reconstructs the proof and authenticates29 original blobs,35 complete new native captures,32 original API captures and4 author/historical reproductions. Full theorem retains known smooth connected domain, known positive bounds, stationary exact fixed-lag reversible conormal observations and local/clipped-L2 losses. Math100%,priority0%,workflow30%; two independent primary-source priority families now active. No preprint/novelty/publication/merge clearance, DOI/tracker/nativeQUEUE mutation or future commit/push completion claimed here.\n').encode())
scope=json.loads((P/'CURRENT_SCOPE.json').read_bytes());scope.update(utc=stamp,scope='Process only submitted QUEUE.md status exactly claimed_solved; skip all others entirely and PR8; descending current302.',current_eligible_pr=302,current_original_head=gate['original_head'],current_original_status='claimed_solved',last_completed_pr=305,last_completed_disposition='merged_claimed_solved_published_zenodo_tracker_verified',next_descending_filter_pending=False,mathematical_verification_percent=100,priority_percent=0,workflow_percent=30)
write(W/'CURRENT_SCOPE.json',scope)
selected=[]
for row in json.loads((A/'snapshot_manifest.json').read_bytes())['files']:selected.append(A/'snapshot'/row['path'])
for name in ['snapshot_manifest.json','RESEARCH_LOG.md','README.md','CURRENT_AUDIT_STATUS.json','ROOT_MATHEMATICAL_RECONSTRUCTION.md','ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json','ROOT_CLOSED_REVIEW_CUSTODY_DIAGNOSTIC.json','ROOT_ORIGINAL_CONTROL_REPRODUCTION.json','root_source_intake.py','root_reproduce_original_checks.py','root_authenticate_closed_math_reviews.py','root_close_math_review_gate.py','root_prepare_math_checkpoint_036.py','root_checkpoint_math_036.py']:selected.append(A/name)
for name in ['verify_turn1.py','verify_turn2.py','independent_controls.py','TURN_1_CHECKS.json','TURN_2_CHECKS.json']:selected.append(A/'root_reproduction'/name)
fams={
 'math_empirical_adversary_01':['FROZEN_CRITERIA.md','CRITERIA_FREEZE.json','REPORT.md','VERDICT.json','RESEARCH_LOG.md','INPUT_AND_CUSTODY_INVENTORY.json','OUTPUT_INVENTORY.json','INDEPENDENT_CONTROLS_RESULT.json','independent_exact_controls.py','independent_exact_controls_before_exact_sign.py'],
 'math_spectral_adversary_01':['FROZEN_CRITERIA.md','REVIEW_REPORT.md','INDEPENDENT_DERIVATION.md','VERDICT.json','RESEARCH_LOG.md','INPUT_CUSTODY.json','OUTPUT_INVENTORY.json','INDEPENDENT_CONTROLS_RESULT.json','RUNTIME_MODULE_INVENTORY.json','independent_controls.py'],
 'math_scope_adversary_01':['CRITERIA.md','REPORT.md','VERDICT.json','RESEARCH_LOG.md','INPUT_INVENTORY_V02.json','REVIEW_CUSTODY.json','OUTPUT_INVENTORY.json','CLOSURE.json','INDEPENDENT_SCOPE_CONTROLS.json','independent_scope_controls.py']}
for family,files in fams.items():selected.extend(A/family/name for name in files)
I=P/'intake_after_pr305_20261005'
selected.extend(I/name for name in ['INTAKE.json','check_next.py','check_next_v02.py','FAILED_V01_LOCATOR.json'])
selected.extend([P/'checkpoint_305_publication_completion_035_receipt.json',D/'ROOT_PR305_CHECKPOINT035_VERIFICATION.json',D/'ROOT_PR305_COMPLETED_100_SCOPE_CLOSED.json',D/'root_verify_pr305_checkpoint035_readonly.py',D/'ROOT_PR85_MATH_CHECKPOINT_RELEASE_VERIFICATION.json',D/'ROOT_PR85_MATH_CHECKPOINT_SCOPE_CLOSED.json'])
targets=[]
for p in selected:
 q=pin(p);q['path']=str(p.relative_to(R));targets.append(dict(target=q['path'],input=q,original_target=pin(p)))
for name in ['inventory.json','RESEARCH_LOG.md','CURRENT_SCOPE.json']:
 q=pin(W/name);q['path']=str((W/name).relative_to(R));targets.append(dict(target=str((P/name).relative_to(R)),input=q,original_target=pin(P/name)))
assert len({x['target'] for x in targets})==len(targets)
path=W/'CONTENT_PLAN.json';allowed=sorted([e['target'] for e in targets]+[str(path.relative_to(R))])
plan=dict(status='EXACT_PR302_PUBLIC_SAFE_MATHEMATICAL_CHECKPOINT036_PLAN',UTC=stamp,preparation_actual_PID=os.getpid(),preparation_argv=sys.orig_argv,starting_main='2e0162fbb5773d0c1b41bfaa9f461bc474338902',targets=targets,allowed_paths=allowed,mathematics_percent=100,priority_percent=0,workflow_percent=30,unresolved_mandatory_mathematical_findings=0,no_PR_native_QUEUE_Zenodo_tracker_mutation=True,closed_inventories_bind_private_evidence_beyond_committed_subset=True,third_party_PDFs_and_extracts_not_selected=True,source=pin(__file__),operator=pin(A/'root_checkpoint_math_036.py'))
write(path,plan)
ast.parse((A/'root_checkpoint_math_036.py').read_bytes());ast.parse(pathlib.Path(__file__).read_bytes())
s=json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes());assert s['shared_git_writes_paused'] and s['descending_writer_window_released'] and s['ascending_pr85_math_checkpoint_complete_and_released'] and not s['ascending_pr85_math_checkpoint_window_granted']
write(W/'PREVIOUS_CLOSED_SHARED_CONTROL_EPOCH.json',s)
s.update(utc=utc(),shared_git_writes_paused=False,descending_writer_window_released=False,descending_shared_git_writes_abstained=False,descending_active_pr=302,descending_302_math_review_percent=100,descending_302_priority_percent=0,descending_302_workflow_percent=30,reason='ROOT exact PR302 mathematics checkpoint036; original PR/nativeQUEUE/publication/tracker are outside scope; peer last writer scope closed',local_main_at_resume=plan['starting_main'],remote_main_at_resume=plan['starting_main'])
s['descending_302_math_checkpoint_lease']=dict(token=token,active=True,scope='PR302 exact mathematical checkpoint only',plan=pin(path),source=pin(A/'root_checkpoint_math_036.py'),allowed_paths=allowed,starting_main=plan['starting_main'],endpoint='https://github.com/AlecKriebel/Math.git',expires_UTC=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=15)).isoformat(),no_PR_native_QUEUE_Zenodo_tracker_authority=True,postcheckpoint_shared_control_closure_authorized=True)
write(P/'SHARED_GIT_WINDOW_STATUS.json',s)
print(json.dumps(dict(status=plan['status'],allowed_paths=len(allowed),token=token,plan=pin(path),syntax_parses=True,actual_writer_not_yet_run=True)))
