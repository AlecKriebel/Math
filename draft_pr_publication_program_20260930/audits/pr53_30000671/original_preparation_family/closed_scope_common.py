"""Small exact closure verifier; original-only custody, never mathematical approval."""
import datetime,hashlib,json,pathlib,stat
F=pathlib.Path(__file__).absolute().parent
EXPECTED=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr53_30000671/original_preparation_family')
assert F==EXPECTED
def sha(b):return hashlib.sha256(b).hexdigest()
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
def js(rel):return json.loads((F/rel).read_bytes())
def regular_paths():
    assert all(not p.is_symlink() for p in [F,*F.parents])
    files=[];dirs=[]
    for p in [F,*F.rglob('*')]:
        assert not p.is_symlink(),str(p)
        rel='.' if p==F else p.relative_to(F).as_posix()
        if p.is_dir():dirs.append(rel)
        else:assert p.is_file(),str(p);files.append(rel)
    return sorted(files),sorted(dirs)
def check_row(row):
    p=F/row['path'];b=p.read_bytes()
    assert len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['mode'],row['path']
def validate_captures():
    count=0
    for p in sorted(F.rglob('CAPTURE.json')):
        c=json.loads(p.read_bytes());d=p.parent
        assert type(c['pid']) is int and c['pid']>0
        assert isinstance(c['argv'],list) and c['argv'] and all(type(x) is str for x in c['argv'])
        assert c['cwd']=='/Users/alec/Documents/Math'
        start=datetime.datetime.fromisoformat(c['started_at'].replace('Z','+00:00'))
        end=datetime.datetime.fromisoformat(c['completed_at'].replace('Z','+00:00'))
        assert start.tzinfo and end.tzinfo and start<=end and type(c['exit_code']) is int
        assert sha((d/'prelaunch_operator.py').read_bytes())==c['operator_sha256']
        for key in ['stdout','stderr']:
            row=c[key];b=(d/row['path']).read_bytes()
            assert len(b)==row['bytes'] and sha(b)==row['sha256']
        if c.get('prelaunch_child_source'):
            row=c['prelaunch_child_source'];b=(d/row['path']).read_bytes()
            assert len(b)==row['bytes'] and sha(b)==row['sha256']
        count+=1
    return count
def verify_prepared(closed=False):
    idx=js('FIXED_PAYLOAD_INDEX.json');ready=js('READY.json')
    assert idx['schema']=='pr53-original-prepared-index/v1'
    assert ready['root_approval'] is False and ready['manifest_absent_at_handoff'] is True
    assert ready['fixed_index_sha256']==sha((F/'FIXED_PAYLOAD_INDEX.json').read_bytes())
    assert ready['report_sha256']==sha((F/'REPORT.md').read_bytes())
    assert ready['source_qualifications_sha256']==sha((F/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes())
    expected={r['path'] for r in idx['files']}|{'FIXED_PAYLOAD_INDEX.json','READY.json'}
    if closed:expected.add('MANIFEST.json')
    files,dirs=regular_paths()
    assert set(files)==expected and dirs==idx['directories']
    assert len({r['path'] for r in idx['files']})==len(idx['files'])
    for row in idx['files']:check_row(row)
    for rel in ['FIXED_PAYLOAD_INDEX.json','READY.json']:assert mode(F/rel)=='0444'
    for rel in dirs:assert mode(F if rel=='.' else F/rel)=='0755'
    count=validate_captures()
    auth=js('GITHUB_AUTHENTICATION.json')
    assert auth['head']=='d49a1bd56d8cc268159331e5ce868e258a32bb58' and len(auth['files'])==11
    for row in auth['files']:
        b=(F/row['archive_path']).read_bytes()
        assert len(b)==row['bytes'] and sha(b)==row['sha256']
        assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==row['git_blob_sha1']
    scope=js('ORIGINAL_SCOPE_CHECKS.json')
    assert scope['status']=='PASS' and scope['counterexample_construction_independently_verified'] is False
    assert js('RAW_PRIOR_REPORT_JOIN.json')['raw_research_results_key_present'] is False
    assert js('RAW_PRIOR_REPORT_JOIN.json')['sql_report_literal']=='{}'
    return idx,ready,count
