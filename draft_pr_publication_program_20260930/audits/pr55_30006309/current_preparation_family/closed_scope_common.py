"""Current SOURCE custody only. Full body/mode/topology verification; no acceptance authority."""
import datetime,hashlib,json,pathlib,stat
F=pathlib.Path(__file__).absolute().parent
EXPECTED=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr55_30006309/current_preparation_family')
assert F==EXPECTED
R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
def js(rel):return json.loads((F/rel).read_bytes())
def topology(base=F):
    assert all(not p.is_symlink() for p in [base,*base.parents,*base.rglob('*')])
    files=[];dirs=[]
    for p in [base,*base.rglob('*')]:
        if p.is_dir():dirs.append('.' if p==base else p.relative_to(base).as_posix())
        else:assert p.is_file();files.append(p.relative_to(base).as_posix())
    return sorted(files),sorted(dirs)
def check(row,external=False):
    p=R/row['repo_path'] if external else F/row['path'];b=p.read_bytes()
    assert not p.is_symlink() and p.is_file() and len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['mode']
def verify_capture(name,child,current_author=False):
    d=F/name;c=json.loads((d/'CAPTURE.json').read_bytes())
    assert c['actual_execution'] is True and c['root_execution'] is False and c['exit_code']==0 and c['completed'] is True
    assert type(c['pid']) is int and c['pid']>0 and c['cwd']==str(R)
    assert c['argv']==['/usr/bin/python3','-B',str(F/child)]
    assert datetime.datetime.fromisoformat(c['started_utc'])<=datetime.datetime.fromisoformat(c['finished_utc'])
    assert c['operator_unchanged'] and c['sources_unchanged']
    assert sha((d/'prelaunch_operator.py').read_bytes())==c['operator_sha256']==sha((F/'capture_command.py').read_bytes())
    for row in c['sources']:
        b=(d/row['prelaunch_copy']).read_bytes()
        assert len(b)==row['bytes'] and sha(b)==row['sha256'] and b==pathlib.Path(row['path']).read_bytes()
    for key in ['stdout','stderr']:
        row=c[key];b=(d/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
    out=json.loads((d/'stdout.bin').read_bytes())
    if current_author:
        assert out['status']=='PASS' and out['exact_assertions']==1227 and out['case_count']==8
        assert (d/'stdout.bin').read_bytes()==(F/'original_archive/product_verification.json').read_bytes()
        assert c['candidate_context_bound_by_operator_not_read_by_checker'] is True
    else:assert out['status']=='PASS_SOURCE_PREPARATION_ONLY' and out['root_approval'] is False
    return c,out
def verify_prepared(closed=False):
    idx=js('FIXED_PAYLOAD_INDEX.json');ready=js('READY.json')
    assert idx['schema']=='pr55-current-prepared-index/v1' and ready['schema']=='pr55-current-source-ready/v1'
    assert ready['manifest_absent_at_handoff'] is True and ready['root_approval'] is False
    assert ready['fixed_index_sha256']==sha((F/'FIXED_PAYLOAD_INDEX.json').read_bytes())
    for key,name in [('report_sha256','REPORT.md'),('verdict_sha256','VERDICT.json'),('external_references_sha256','EXTERNAL_REFERENCES.json'),('science_index_sha256','SCIENCE_INDEX.json'),('source_accounting_sha256','SOURCE_ACCOUNTING_CURRENT.json'),('current_reproduction_sha256','CURRENT_REPRODUCTION.json')]:
        assert ready[key]==sha((F/name).read_bytes())
    assert ready['current_source_status']=='already_solved' and ready['original_substantive_attempts']==1 and ready['new_proof_search_turns']==0
    assert ready['original_JSONL_turn_entry_count']==1 and ready['new_paper'] is False
    assert ready['mandatory_math_corrections']==[] and ready['payload_files']<=70 and ready['total_payload_bytes']<1000000
    assert ready['source_correction_completion_percent']==100 and ready['original_target_novel_discovery_percent']==0
    expected={x['path'] for x in idx['files']}|{'FIXED_PAYLOAD_INDEX.json','READY.json'}
    if closed:expected.add('MANIFEST.json')
    files,dirs=topology();assert set(files)==expected and len(files)==len(expected) and dirs==idx['directories']
    assert len(idx['files'])==ready['payload_files'] and sum(x['bytes'] for x in idx['files'])==ready['total_payload_bytes']
    for row in idx['files']:check(row)
    for name in ['FIXED_PAYLOAD_INDEX.json','READY.json']:assert mode(F/name)=='0444'
    for rel in dirs:assert mode(F if rel=='.' else F/rel)=='0755'
    ext=js('EXTERNAL_REFERENCES.json');n=0
    for g in ext['closed_families']+ext['actual_root_captures']+ext['frozen_source_notes']:
        base=R/g['repo_path'];fs,ds=topology(base)
        assert {str((base/x).relative_to(R)) for x in fs}=={row['repo_path'] for row in g['rows']}
        assert {str((base if x=='.' else base/x).relative_to(R)) for x in ds}=={row['repo_path'] for row in g['directories']}
        for row in g['rows']:check(row,True);n+=1
        for row in g['directories']:assert mode(R/row['repo_path'])==row['mode']
    for g in ext['closed_families']:assert sha((R/g['manifest_repo_path']).read_bytes())==g['manifest_sha256']
    for g in ext['actual_root_captures']:
        base=R/g['repo_path'];c=json.loads((base/'CAPTURE.json').read_bytes())
        assert c['pid']==g['pid'] and c['argv']==g['argv'] and c['exit_code']==0 and c['actual_execution'] is True
        assert c['started_utc']==g['started_utc'] and c['finished_utc']==g['finished_utc']
        assert c['operator_unchanged'] and sha((base/'prelaunch_operator.py').read_bytes())==c['operator_sha256']
        for key in ['stdout','stderr']:
            row=c[key];b=(base/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
    science=js('SCIENCE_INDEX.json');assert science['original_archive_files']==16 and science['operative_science_files']==20
    for row in science['files']:
        b=(F/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
    c,out=verify_capture('actual_current_author_replay','science/verify_product_vectors.py',True)
    q=js('CURRENT_REPRODUCTION.json');assert q['actual_child_pid']==c['pid'] and q['new_independence'] is False and q['root_approval'] is False
    assert q['current_candidate_sha256']==sha((F/'science/CANDIDATE.md').read_bytes())
    c,out=verify_capture('actual_preparation_check','verify_current.py')
    assert out['external_whole_body_rows']==n
    return idx,ready,n
