"""Verify complete replay data before recording the mathematical gate and intake."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,os,stat,subprocess,fcntl
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(p.read_bytes())
def pin(p):
    assert p.is_file() and not p.is_symlink(),p
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
S=P/'SHARED_GIT_WINDOW_STATUS.json';s=load(S)
assert not s['shared_git_writes_paused'] and s['descending_active_pr']==s['descending_acceptance_pr']==305
lease=s['descending_shared_write_lease'];assert lease['pr']==305 and lease['owner_thread']=='01a0ff30-7e80-7053-abb4-4a9c45f2fd62'
assert lease['token']=='dd8a3816-588a-4873-a0c5-daf812b24b07' and lease['peer_readonly_release_verified'] and lease['cooperative_exclusive_window']
assert pin(P/lease['release_verification_path'])==lease['release_verification']
fd=os.open(P/'audits/pr311_30005303/root_integration_private/SHARED_WRITE_LEASE.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
hold=os.fdopen(fd,'r+b');fcntl.flock(hold,fcntl.LOCK_EX|fcntl.LOCK_NB)
head=git('rev-parse','HEAD').decode().strip();assert git('branch','--show-current')==b'main\n'
assert head=='f203c604c8db564423fbd3f6b5f367580745b9f2' and git('ls-remote','origin','refs/heads/main').decode().split()[0]==head
assert not git('diff','--cached','--raw','-z')
index=git('ls-files','--stage','-z');owned={str(x.relative_to(R)) for x in [P/'inventory.json',P/'RESEARCH_LOG.md',S,A/'RESEARCH_LOG.md']}
foreign={}
for name in git('diff','--name-only','-z').split(b'\0'):
    if name and name.decode() not in owned:
        p=R/name.decode();foreign[name.decode()]=(p.exists(),p.read_bytes() if p.is_file() else None,stat.S_IMODE(p.stat().st_mode) if p.exists() else None)
original=load(A/'snapshot_manifest.json');assert original['head']=='cc083024dbd00de06ad444cd4070f51f60d209eb' and len(original['files'])==30
for e in original['files']:
    p=A/'snapshot'/e['path'];b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'] and format(p.stat().st_mode&0o777,'04o')==e['mode']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha']
T=A/'snapshot/problems/5100034_focal_pedal_equality';public=load(T/'PUBLIC_MANIFEST.json')
assert len(public['files'])==28
for e in public['files']:assert {k:pin(T/e['path'])[k] for k in ['bytes','sha256']}=={k:e[k] for k in ['bytes','sha256']}
auth=load(A/'ROOT_FAMILY_SEAL_AUTHENTICATION.json');assert auth['status']=='PASS_THREE_CLOSED_FAMILY_SEALS_AND_FOUR_FRESH_NATIVE_REPLAYS'
for folder,e in auth['families'].items():
    D=A/folder;report='FINAL_REPORT.md' if folder.startswith('source') else 'REPORT.md';manifest='MANIFEST.json' if folder.startswith('geometric') else 'ARTIFACT_SEAL.json'
    assert pin(D/report)==e['report'] and pin(D/manifest)==e['seal'] and stat.S_IMODE(D.stat().st_mode)==0o555
    for entry in load(D/manifest)['files']:assert pin(D/entry['path'])=={k:entry[k] for k in ['bytes','sha256','mode']}
    for name,expected in e['terminal_envelopes'].items():assert pin(D/name)==expected
jobs=['pr305_original_exact_checks_actual001','pr305_original_numeric_checks_actual001','root_inherited_triangle_actual001','root_inherited_diagnostics_actual001','root_replay_meromorphic_rational_actual001','root_replay_meromorphic_full_actual001','root_replay_source_symbolic_actual001','root_replay_source_decimal_actual001','root_geometric_multiquadratic_actual001','root_geometric_candidate_symbolic_actual001','root_geometric_direct_reflection_actual001','root_geometric_canonical_compare_actual001','root_geometric_stored_crosschecks_actual001']
runs={}
for label in jobs:
    D=A/'root_runs_private'/label;j=load(D/'execution.json');assert j['exit_code']==0
    for key in ['stdout','stderr']:
        b=(D/(key+'.bin')).read_bytes();assert len(b)==j[key+'_bytes'] and sha(b)==j[key+'_sha256']
    assert j['stderr_bytes']==0
    for e in j['programs']:assert {k:pin(Path(e['path']))[k] for k in ['bytes','sha256']}=={k:e[k] for k in ['bytes','sha256']}
    runs[label]=j
for label,expected in [('pr305_original_exact_checks_actual001',T/'EXACT_CONTROLS.json'),('pr305_original_numeric_checks_actual001',T/'NUMERICAL_DIAGNOSTICS.json'),('root_inherited_triangle_actual001',T/'review/INDEPENDENT_TRIANGLE_CHECK.json'),('root_inherited_diagnostics_actual001',T/'review/INDEPENDENT_GEOMETRY_DIAGNOSTICS.json')]:
    assert (A/'root_runs_private'/label/'stdout.bin').read_bytes()==expected.read_bytes()
G=A/'geometric_family_20261004';D=A/'root_geometric_reproduction_private'
for e in load(D/'INPUT_PROGRAMS.json')['files']:
    assert (D/e['name']).read_bytes()==(G/e['name']).read_bytes()
    assert {k:pin(D/e['name'])[k] for k in ['bytes','sha256']}=={k:e[k] for k in ['bytes','sha256']}
for name in ['exact_triangle_results.json','candidate_exact_and_symbolic_results.json','independent_billiard_results.json','canonical_vs_direct_results.json','stored_geometry_crosschecks_results.json']:
    assert (D/name).read_bytes()==(G/name).read_bytes(),name
rows=load(D/'independent_billiard_results.json')['results'];assert len(rows)==117
assert len({(x['a'],x['N'],x['winding']) for x in rows})==39
for row in rows:
    assert row['primitive'] and Decimal(row['beta_squared'])>0
    assert all(Decimal(v)>0 for v in row['signed_areas_Aplus_Aprimeplus_Aminus_Aprimeminus'])
    assert Decimal(row['checks']['min_outer_det'])>0
    assert all(abs(Decimal(v))<Decimal('1e-65') for k,v in row['checks'].items() if k!='min_outer_det')
cross=load(D/'stored_geometry_crosschecks_results.json');assert cross['samples']==117
for row in cross['results']:
    assert Decimal(row['actual_chord_reflection_max_residual'])<Decimal('1e-65')
    assert all(Decimal(row[k])>0 for k in ['min_incoming_normal','min_outgoing_normal','min_consecutive_focal_determinant'])
    assert all(Decimal(v[k])<Decimal('1e-80') for v in row['areas'] for k in ['reversal_residual','repetition_residual'])
canonical=load(D/'canonical_vs_direct_results.json');assert canonical['rows']==117 and all(Decimal(x)<Decimal('1e-60') for x in canonical['global_maxima'].values())
raw=load(A/'ROOT_IMPORTED_RECORD_AUTHENTICATION.json');assert raw['status']=='PASS_TARGET_IMPORTED_RECORD_EXACT_HASH_AND_CACHED_REVISION_CHAIN' and raw['explicit_phase_constancy_present']
for name,e in raw['target_raw_files'].items():assert pin(A/'root_imported_record_private'/name)==e
report=A/'ROOT_MATHEMATICAL_AUDIT.md';assert 'Mathematical verdict: E proved, C disproved' in report.read_text()
j={'utc':utc(),'status':'PASS_CORRECTED_DISPLAYED_EQUALITY_PROVED_AND_PHASE_CONSTANCY_DISPROVED',
   'original_head':original['head'],'original_status':'claimed_solved','original_author_turn_count':'1/5',
   'proof':pin(T/'TURN_1.md'),'root_report':pin(report),'three_closed_family_reports_authenticated':auth['families'],
   'scientific_native_runs':runs,'all_five_fresh_geometric_result_files_byte_equal_to_sealed_results':True,
   'all_117_direct_reflection_data_rows_checked':True,'entire_submitted_30_file_snapshot_and_28_public_manifest_entries_authenticated':True,
   'imported_record_authenticated':pin(A/'ROOT_IMPORTED_RECORD_AUTHENTICATION.json'),
   'strongest_verified_result':'For every permitted phase and both foci, B_j=C0*A_j with the same positive phase-independent C0. All four signed real areas are nonzero. The displayed ratio equality follows; common focal-ratio phase constancy is false by exact counterexample.',
   'unresolved_mathematical_findings':0,'phase_constancy_affirmatively_solved':False,
   'mathematical_verification_percent':100,'bounded_priority_percent':0,'workflow_percent':30,
   'bounded_priority_audit_required':True,'preprint_ready':False,'merge_ready':False,'publishing_clearance':False,
   'unrefereed':True,'extensive_AI_use':True,'human_peer_review_claimed':False,
   'numeric_evidence':'Finite high-precision NONINTERVAL diagnostics; universal result rests on the checked analytic proof.'}
(A/'ROOT_MATHEMATICAL_ACCEPTANCE.json').write_text(json.dumps(j,indent=2)+'\n')
inventory=load(P/'inventory.json');before_items={x['number']:json.loads(json.dumps(x)) for x in inventory['items']};counter=inventory['completed_by_descending']
E=P/'audits/pr311_30005303/root_coordination_private/pr73_final_acceptance_20261004';eligible={}
for folder in ['remote_eligibility_prefetch','remote_eligibility_prefetch_v02','remote_eligibility_prefetch_v03']:
    receipt=load(E/folder/'ELIGIBILITY_ONLY.json')
    for row in receipt['rows']:
        if row.get('submitted_QUEUE_status')=='unsolved' and row['pr'] in range(306,311):
            b=(E/folder/('pr'+str(row['pr'])+'_QUEUE.bin')).read_bytes()
            assert len(b)==row['queue_bytes'] and sha(b)==row['queue_sha256']
            assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['queue_git_blob']
            eligible[row['pr']]={**row,'eligibility_checked_utc':receipt['recorded_utc']}
assert set(eligible)==set(range(306,311))
for item in inventory['items']:
    if item['number'] in eligible:
        e=eligible[item['number']];assert item['headRefOid']==e['original_inventory_head']
        item.update(submitted_status='unsolved',eligibility_checked_head=e['original_inventory_head'],eligibility_checked_utc=e['eligibility_checked_utc'],disposition='skipped_excluded_status_without_processing')
    elif item['number']==305:
        assert item['headRefOid']==original['head']
        item.update(submitted_status='claimed_solved',eligibility_checked_head=original['head'],eligibility_checked_utc=original['utc'],disposition='mathematics_accepted_corrected_equality_and_negative_constancy_priority_pending',mathematical_verification_percent=100,bounded_priority_percent=0,workflow_percent=30,original_author_turn_count='1/5',audit='draft_pr_descending_audit_20261002/audits/pr305_5100034/')
    else:assert item==before_items[item['number']]
assert inventory['completed_by_descending']==counter
(P/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
entry='\n- '+utc()+': PR305 three independent closed mathematical/source families authenticated; all13 scientific programs reproduced, all117 direct-reflection rows and complete fresh result files checked. Exact imported wording recovered and authenticated. Strongest verified result: displayed focal-pedal equality proved, phase-constancy reading disproved. No mathematical gap identified; priority remains unassessed. PR310–306 skipped by original unsolved status only; no other PR processing. Completion estimate: math100%, bounded priority0%, PR workflow30%; persistent goal active.\n'
for log in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with log.open('a') as f:f.write(entry)
s.update(utc=utc(),reason='PR311 completed and PR80 scoped checkpoint released and verified. ROOT owns the PR305 mathematics/priority window.',descending_checkpoint_scope='PR305 corrected equality proved and constancy disproved; three closed independent families authenticated and all13 scientific programs replayed. Priority and preprint gates remain pending.',descending_305_mathematical_verification_percent=100,descending_305_bounded_priority_percent=0,descending_305_workflow_percent=30,local_main_at_resume=head,remote_main_at_resume=head)
S.write_text(json.dumps(s,indent=2)+'\n')
assert git('ls-files','--stage','-z')==index and git('rev-parse','HEAD').decode().strip()==head
for name,e in foreign.items():
    p=R/name;assert (p.exists(),p.read_bytes() if p.is_file() else None,stat.S_IMODE(p.stat().st_mode) if p.exists() else None)==e
print(json.dumps({'utc':utc(),'status':j['status'],'root_acceptance':pin(A/'ROOT_MATHEMATICAL_ACCEPTANCE.json'),'scientific_runs_verified':len(runs),'family_payloads_verified':sum(x['payload_files_verified'] for x in auth['families'].values()),'foreign_index_body_modes_and_main_preserved':True,'math_percent':100,'bounded_priority_percent':0,'workflow_percent':30},indent=2))
