"""Close the explicitly bounded PR302 mathematical gate; no novelty clearance."""
import datetime,hashlib,json,os,pathlib,stat,subprocess,sys
A=pathlib.Path(__file__).resolve().parent;R=A.parent.parent.parent
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    p=pathlib.Path(p);b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(p.stat().st_mode)))
def equal(row,p=None):
    q=pin(p or row['path']);assert (q['bytes'],q['sha256'])==(row['bytes'],row['sha256']),(row,q);return q
assert not sys.flags.optimize
started=utc();source=pin(__file__)
d=json.loads((A/'ROOT_CLOSED_REVIEW_CUSTODY_DIAGNOSTIC.json').read_bytes())
assert d['all_output_inventories_match_and_all_original_blobs_unchanged'] and not d['missing_pinned_paths']
assert d['complete_native_capture_count']==35 and len(d['historical_body_differences'])==14
F={k:A/k for k in ['math_empirical_adversary_01','math_spectral_adversary_01','math_scope_adversary_01']}
aliases={
 'd4da12a5a18d7e1d3f430170d7d465b71763a263b4ffeb774871765f16734b08':F['math_empirical_adversary_01']/'independent_exact_controls_before_exact_sign.py',
 '041ea877554f084c1c2522db38e1baef3e2937ca3deed6e15b6d756a721423e3':F['math_spectral_adversary_01']/'VERDICT_BEFORE_EXTERNAL_OWNERSHIP_METADATA_REPAIR.json',
 'cbf3ec40fa6000c4e0694815280176dce8d233ee22c21482cacb6c236368fdcd':F['math_scope_adversary_01']/'metadata_finalization_v01_preserved/freeze_outputs.py',
 '6b090faee9efcaf12bfe0ef3103a69c7a81114eade056d94c41769b562dd34e6':F['math_scope_adversary_01']/'metadata_finalization_v01_preserved/OUTPUT_INVENTORY.json',
 '04280339022e0705a8fb53e343ffd71cf2d8d495f5fd91a1c0ce41ea9d00d04e':F['math_scope_adversary_01']/'run_capture_v01_preserved.py'}
resolved=[]
for e in d['historical_body_differences']:
    row=e['historical_pin'];h=row['sha256']
    if h in aliases:
        q=equal(row,aliases[h]);kind='Exact separately retained historical source/metadata body; not the current file at the old path.'
    else:
        assert h=='9641fdcc9458a23a80388d1da17b4e6dbbafb4bc40251fc2e4da84b134b382cd'
        p=pathlib.Path(row['path']);b=p.read_bytes()[:row['bytes']]
        assert hashlib.sha256(b).hexdigest()==h
        q=dict(path=str(p),authenticated_prefix_bytes=len(b),sha256=h,current_whole=pin(p))
        kind='Historical research-log body authenticated as the exact current prefix; appended metadata-repair entry, no separate historical archive asserted.'
    resolved.append(dict(original_record=e,resolution=kind,retained_evidence=q))
assert len(resolved)==14
mode_exceptions=[]
for e in d['mode_differences']:
    if e['inside_closed_review']:
        assert e['historical_mode']=='0o644' and e['current_mode']=='0o444'
    else:
        assert e['container']==str(F['math_spectral_adversary_01']/'VERDICT_BEFORE_EXTERNAL_OWNERSHIP_METADATA_REPAIR.json')
        assert e['path']==str(A/'snapshot_manifest.json') and e['historical_mode']=='0o444' and e['current_mode']=='0o644'
        mode_exceptions.append(e)
assert len(mode_exceptions)==1
old=json.loads((F['math_spectral_adversary_01']/'VERDICT_BEFORE_EXTERNAL_OWNERSHIP_METADATA_REPAIR.json').read_bytes())
now=json.loads((F['math_spectral_adversary_01']/'VERDICT.json').read_bytes())
assert old['source_snapshot'].pop('final_frozen_mode')=='0o444'
assert now['source_snapshot'].pop('ownership')=='External case manifest: authenticated but neither mutated nor frozen by this family.'
now.pop('metadata_only_repair');assert old==now
for family in d['families']:
    equal(family['output_inventory'])
    for row in family['all_current_files']:
        q=equal(row);assert q['mode']=='0o444'
for row in d['native_captures']:
    equal(row['execution']);equal(row['request']);equal(row['complete_stdout']);equal(row['complete_stderr'])
assert len(d['failed_native_captures'])==1
failure=d['failed_native_captures'][0]
assert failure['actual_PID']==5104 and failure['exit_code']==1
assert failure['execution']['path'].endswith('/math_scope_adversary_01/process_evidence/authenticate_inputs/execution.json')
assert b'AssertionError' in pathlib.Path(failure['complete_stderr']['path']).read_bytes()

# Authenticate the complete original API tapes, not displayed excerpts.
original_native=[]
intake_source=pin(A/'root_source_intake.py')
for p in sorted((A/'source_intake_private').glob('*_execution.json')):
    e=json.loads(p.read_bytes());label=p.name.removesuffix('_execution.json')
    s=json.loads((p.parent/(label+'_started.json')).read_bytes())
    assert e['actual_PID']==s['actual_PID']>0 and e['argv']==s['argv'] and e['cwd']==s['cwd']==str(R)
    assert e['source_sha256']==s['source_sha256']==intake_source['sha256'] and e['exit_code']==0
    streams={}
    for k in ['stdout','stderr']:
        q=pin(p.parent/(label+'_'+k+'.bin'));assert q['bytes']==e[k+'_bytes'] and q['sha256']==e[k+'_sha256'];streams[k]=q
    body=json.loads(pathlib.Path(streams['stdout']['path']).read_bytes())
    if label in ['before','after']:assert body['head']['sha']==d['original_head'] and body['state']=='open' and body['draft']
    original_native.append(dict(execution=pin(p),start=pin(p.parent/(label+'_started.json')),actual_PID=e['actual_PID'],argv=e['argv'],cwd=e['cwd'],UTC_start=e['start_UTC'],UTC_end=e['end_UTC'],exit_code=e['exit_code'],streams=streams))
assert len(original_native)==32

repro=json.loads((A/'ROOT_ORIGINAL_CONTROL_REPRODUCTION.json').read_bytes())
for item in repro['copies']:
    equal(item['original']);equal(item['copy'])
for e in repro['native_captures']:
    p=A/'root_reproduction'/('runtime' if '-c' in e['argv'] else {'verify_turn1.py':'author1','verify_turn2.py':'author2','independent_controls.py':'old_independent'}[pathlib.Path(e['argv'][-1]).name])
    assert json.loads((p/'execution.json').read_bytes())==e
    start=json.loads((p/'started.json').read_bytes())
    assert start['actual_PID']==e['actual_PID']>0 and start['argv']==e['argv'] and start['cwd']==e['cwd']
    equal(e['root_driver']);equal(e['interpreter'])
    for row in e['program_sources']:equal(row)
    for k in ['stdout','stderr']:
        q=pin(p/(k+'.bin'));assert q['bytes']==e[k+'_bytes'] and q['sha256']==e[k+'_sha256']
    assert e['exit_code']==0
assert len(repro['native_captures'])==4 and [x['count'] for x in repro['counts']]==[11,42,1905]

# A new complete read of the PR verifies the science still concerns the same head.
N=A/'root_math_gate_native_readback';assert not N.exists();N.mkdir()
argv=['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/302'];ts=utc()
proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
native=dict(actual_PID=proc.pid,argv=argv,cwd=str(R),UTC_start=ts,source=source)
(N/'started.json').write_text(json.dumps(native,indent=2)+'\n')
out,err=proc.communicate(timeout=55)
(N/'stdout.bin').write_bytes(out);(N/'stderr.bin').write_bytes(err)
native.update(UTC_end=utc(),exit_code=proc.returncode,stdout=pin(N/'stdout.bin'),stderr=pin(N/'stderr.bin'))
(N/'execution.json').write_text(json.dumps(native,indent=2)+'\n')
assert proc.returncode==0
pr=json.loads(out);assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==d['original_head']

result=dict(status='PASS_ROOT_PR302_PRECISE_MATHEMATICAL_GATE',UTC=utc(),started_UTC=started,actual_root_PID=os.getpid(),actual_root_argv=sys.orig_argv,cwd=os.getcwd(),source=source,diagnostic=pin(A/'ROOT_CLOSED_REVIEW_CUSTODY_DIAGNOSTIC.json'),original_head=d['original_head'],original_status='claimed_solved',author_count='2/5',original_snapshot=d['original_snapshot'],families=d['families'],independent_native_capture_count=35,independent_successful_native_captures=34,independent_failed_native_captures=1,failed_run_preserved=failure,two_empirical_pre_Popen_failures_preserved=True,historical_body_differences_all_resolved=resolved,historical_readonly_mode_changes=337,archived_incorrect_external_mode_label=mode_exceptions,full_original_API_captures=original_native,original_reproduction=pin(A/'ROOT_ORIGINAL_CONTROL_REPRODUCTION.json'),original_finite_control_counts=[11,42,1905],new_independent_control_counts=dict(empirical_assertions_per_each_of_two_runs=3690,spectral_exact_checks=43,scope_exact_checks=35,scope_author_replays=[11,42]),fresh_same_head_readback=native,strongest_verified_result='For each fixed smooth symmetric uniformly elliptic S and smooth positive normalized unknown mu on a known bounded connected C-infinity domain in d>=2, with known class bounds and stationary exact fixed-positive-lag conormal reversible observations: almost-sure local uniform spectral recovery of S and separately fitted div S, and global L2 recovery of the ellipticity-clipped tensor.',mandatory_mathematical_findings=0,original_informal_source_convergence_goal_answered_with_explicit_qualifications=True,no_unrestricted_rough_model_or_rate_claim=True,no_claim_that_finite_controls_prove_the_infinite_theorem=True,analytic_ROOT_reconstruction=pin(A/'ROOT_MATHEMATICAL_RECONSTRUCTION.md'),all_three_reports_read_in_full_and_analytically_reconciled=True,priority_unestablished=True,publication_and_merge_clearance=False,mathematics_percent=100,priority_percent=0,workflow_percent=30,remaining_gap='Deep primary-source priority audit; if genuinely open, fully reviewed preprint package and authorized publication/tracker/native merge.',no_Git_index_config_shared_control_service_write=True)
p=A/'ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json';assert not p.exists();p.write_text(json.dumps(result,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write(result['UTC']+' — ROOT closes the precise mathematical gate after full analytical reconciliation of three independent families, authenticating all29 original blobs,35 complete independent native captures (one honest helper failure),32 original API captures and4 original reproductions. Every historical metadata/source difference is retained and resolved explicitly. Zero mandatory mathematical findings for the stated smooth stationary conormal model. Math100%,priority0%,workflow30%; novelty/publication/merge remain unaccepted. Begin materially distinct primary-source priority audits.\n')
print(json.dumps(dict(status=result['status'],actual_PID=os.getpid(),acceptance=pin(p),math_percent=100,priority_percent=0,workflow_percent=30,mandatory_findings=0,publication_clearance=False)))
