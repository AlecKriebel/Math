"""MIT licensed. Administrative evidence checks only; no ROOT helper imports/runs."""
import ast, base64, datetime, hashlib, json, os, pathlib, stat, sys
R=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((R/n).read_bytes())
assert __debug__ and sys.flags.optimize==0 and sys.flags.ignore_environment==1
A=load('ORIGINAL_AUTHENTICATION.json');H='98cc2821e9376507caf2d2c57414f7c7e7719c1b';B='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
assert A['head']==H and A['base']==B and A['science_count']==17 and A['diff_count']==18
assert A['whole_scientific_tree_authenticated'] is True
original=R/'original';entries=A['scientific_files'];paths={e['relative_path'] for e in entries}
assert len(paths)==17 and paths=={p.relative_to(original).as_posix() for p in original.rglob('*') if p.is_file()}
for e in entries:
    p=original/e['relative_path'];b=p.read_bytes();s=p.stat()
    assert str(p)==e['path'] and e['git_mode']=='100644'
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha1']
    assert stat.S_IMODE(s.st_mode)==int(e['full_mode_07777'],8)==0o444 and s.st_nlink==1
P=load('PR_METADATA.json');assert P['head']['sha']==H and P['base']['sha']==B and P['state']=='open' and P['draft'] is True
prefix='unsolved_math_prioritization/attempts/2715/'
D=load('CHANGED_FILES.json');assert len(D)==18
assert {x['filename'] for x in D}=={prefix+p for p in paths}|{'unsolved_math_prioritization/QUEUE.md'}
C=load('COMPARE_AUTHENTICATION.json');assert C['base_commit']==B and C['merge_base_commit']==B and C['ahead_by']==4 and C['behind_by']==0
S=load('RETRIEVAL_FULL_COMMAND_STREAMS.json');assert len(S)==28
api={}
for c in S:
    out=base64.b64decode(c['stdout_base64'],validate=True);err=base64.b64decode(c['stderr_base64'],validate=True)
    assert c['exit_code']==0 and c['actual_pid']>0
    assert len(out)==c['stdout_bytes'] and sha(out)==c['stdout_sha256']
    assert len(err)==c['stderr_bytes'] and sha(err)==c['stderr_sha256']
    assert c['label'] not in api;api[c['label']]=json.loads(out)
assert api['PR_start']==P and api['diff_files']==D
assert api['PR_end']['head']['sha']==H and api['PR_end']['base']['sha']==B
for e in entries:
    j=api['blob_'+e['relative_path']];assert j['sha']==e['git_blob_sha1']
    assert base64.b64decode(j['content'])==(original/e['relative_path']).read_bytes()
qbody=base64.b64decode(api['QUEUE_blob']['content']);Q=load('PR_QUEUE_SELECTED.json')
assert len(qbody)==Q['body_bytes'] and sha(qbody)==Q['body_sha256']
assert '| unsolved | 1/5 |' in Q['selected'][0]['text']
for c in load('ACCOUNTING_FULL_GIT_STREAMS.json'):
    assert c['argv'][0]=='git' and c['pid']>0
    base64.b64decode(c['stdout_base64'],validate=True);base64.b64decode(c['stderr_base64'],validate=True)
account=load('SOURCE_ACCOUNTING.json');prior=account['raw_prior']
assert account['native_branch']=='main' and account['head']==H
assert account['raw_problem_equals_SQL_payload_equals_original_record'] is True
assert prior['key_present'] is False and prior['selected_value_type']=='NoneType' and prior['selected_value_is_NULL'] is True
assert prior['classification'] is None and prior['object_keys'] is None and prior['direct_dict_no_report_wrapper'] is False
assert prior['SQL_storage_type']=='text' and prior['SQL_literal_is_NULL'] is False and prior['SQL_literal_empty_object'] is True
assert prior['SQL_decoded_matches_raw'] is False
assert (R/'RAW_PRIOR_SQL_TEXT.txt').read_bytes()==b'{}' and load('SELECTED_RAW_PRIOR.json') is None
assert account['original_substantive_attempts']==1 and account['budget']==5 and account['new_attempts']==account['audit_increment']==0
turn=load('original/turns.json');assert turn['substantive_proof_attempts']==1 and turn['budget']==5 and turn['turns'][0]['outcome']=='unsolved'
assert account['primary_problem']['text']['sha256']=='3f42d6ebef41f9c4112638f001f16f1bc45e720231b18bc3a8b4f936a51ff790'
assert account['primary_problem']['LF_lines_1_based']==[2867,2893] and account['primary_problem']['visual_read_claimed'] is False
E=load('EXTERNAL_INPUT_PINS.json');assert E['SQL_missing_report_fallback']['LF_line_1_based']==56
assert E['SQL_missing_report_fallback']['queue_generator_executed'] is False
ops={'retrieval':'retrieve_original.py','accounting':'account_original.py',
 'submitted_replay':'original/verify.py','historical_replay':'reproduction/historical/independent_checks.py',
 'submitted_guarded':'original/verify.py','historical_guarded':'reproduction/historical/independent_checks.py',
 'notes':'prepare_source_notes.py'}
controllers={'retrieval':'capture_retrieval.py','accounting':'capture_step.py',
 'submitted_replay':'capture_step.py','historical_replay':'capture_step.py',
 'submitted_guarded':'guarded_capture_replay.py','historical_guarded':'guarded_capture_replay.py',
 'notes':'capture_preparation.py'}
for step,op in ops.items():
    p=R/'captures'/step;c=json.loads((p/'CAPTURE.json').read_bytes())
    assert c['actual_execution'] is True and c['exit_code']==0 and c['ROOT_helper_run'] is False
    assert c['pid']>0 and c['controller_pid']>0 and c['operator_unchanged'] is True
    for n,field,source in [('operator_prelaunch.py','operator_prelaunch_sha256',op),('controller_prelaunch.py','controller_prelaunch_sha256',controllers[step])]:
        b=(p/n).read_bytes();assert sha(b)==c[field] and b==(R/source).read_bytes()
    for st in ['stdout','stderr']:
        b=(p/c[st]['path']).read_bytes();assert len(b)==c[st]['bytes'] and sha(b)==c[st]['sha256']
    assert c['stderr']['bytes']==0
    if step.startswith('submitted'):
        assert (p/'stdout.bin').read_bytes()==(R/'original/verification.json').read_bytes()
        assert (p/'OBSTRUCTION_prelaunch.md').read_bytes()==(R/'original/OBSTRUCTION.md').read_bytes()
        assert json.loads((p/'stdout.bin').read_bytes())['assertions']==564
    if step.startswith('historical'):
        assert (p/'stdout.bin').read_bytes()==(R/'original/independent_review/independent_results.json').read_bytes()
        assert json.loads((p/'stdout.bin').read_bytes())['assertions_passed']==20223
    if step.endswith('_guarded'):
        assert c['argv'][1:3]==['-E','-B'] and '-O' not in c['argv']
        pr=c['runtime_probe'];assert pr['exit_code']==0 and pr['argv'][1:3]==['-E','-B']
        for st in ['stdout','stderr']:
            b=(p/('probe_'+st+'.bin')).read_bytes()
            assert len(b)==pr[st+'_bytes'] and sha(b)==pr[st+'_sha256']
        assert json.loads((p/'probe_stdout.bin').read_bytes())=={'debug':True,'ignore_environment':1,'optimize':0}
assert (R/'reproduction/historical/independent_checks.py').read_bytes()==(R/'original/independent_review/independent_checks.py').read_bytes()
assert (R/'reproduction/historical/independent_results.json').read_bytes()==(R/'original/independent_review/independent_results.json').read_bytes()
RR=load('REPRODUCTION_RECEIPT.json');assert RR['ROOT_helpers_executed'] is False and RR['new_proof_attempts']==RR['new_audit_credit']==0
assert 'not measured' in RR['first_successful_replay_environment_qualification']
W=load('PRIMARY_READING_RECEIPT.json');assert W['owned_web_PID_or_local_download_or_body_hash_or_visual_read_claimed'] is False
assert len(W['access_failures_or_limits'])==2
qualification=(R/'SOURCE_PRECISION_QUALIFICATION.md').read_text()
for literal in ['endpoint','81-95','not measured','SQL','1/5']:assert literal in qualification
python_sources=[]
for p in sorted(R.rglob('*.py')):
    b=p.read_bytes();compile(b,str(p),'exec');python_sources.append(p.relative_to(R).as_posix())
    assert not p.is_symlink() and p.stat().st_nlink==1
helpers=['ROOT_verify_original.py','ROOT_close_original.py','ROOT_readback_original.py']
assert all(n in python_sources for n in helpers)
report={'schema':'pr62-owned-administrative-evidence-check/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'pid':os.getpid(),'status':'PASS_AUTHENTICATED_ORIGINAL_AND_ACTUAL_CONTROL_EVIDENCE',
 'original17_whole_bytes_git_blobs_full_modes':True,'diff18_head_base_fullstream_authentication':True,
 'original564_and_historical20223_exact_replays':True,'guarded_replay_environment_checked':True,
 'typed_raw_absent_SQL_text_empty_object_and_unsolved1of5_preserved':True,
 'ROOT_helpers_syntax_read_only':helpers,'ROOT_helpers_imported_or_executed':False,
 'compiled_source_count':len(python_sources),'self_debug':__debug__,'self_optimize':sys.flags.optimize,
 'scientific_approval':False,'new_math_attempts':0,'new_audit_credit':0,
 'mode_chronology':'Original17 already0444. Other prepared files may still0644 here; final fixed SOURCE separately requires all files0444/directories0755.'}
with (R/'ADMIN_VERIFICATION.json').open('x') as f:f.write(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':report['status'],'pid':os.getpid(),'original_files':17,
 'guarded_controls':[564,20223],'compiled_source_count':len(python_sources),
 'ROOT_helpers_executed':False,'scientific_approval':False},sort_keys=True))
