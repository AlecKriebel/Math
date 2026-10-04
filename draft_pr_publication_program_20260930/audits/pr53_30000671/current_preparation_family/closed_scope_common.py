"""Current SOURCE custody only: no native operations or mathematical approval."""
import datetime,hashlib,json,pathlib,stat
F=pathlib.Path(__file__).absolute().parent
EXPECTED=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr53_30000671/current_preparation_family')
assert F==EXPECTED
R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
def js(rel):return json.loads((F/rel).read_bytes())
def topology():
    assert all(not p.is_symlink() for p in [F,*F.parents,*F.rglob('*')])
    files=[];dirs=[]
    for p in [F,*F.rglob('*')]:
        if p.is_dir():dirs.append('.' if p==F else p.relative_to(F).as_posix())
        else:assert p.is_file();files.append(p.relative_to(F).as_posix())
    return sorted(files),sorted(dirs)
def check(row,external=False):
    p=(R/row['repo_path']) if external else F/row['path'];b=p.read_bytes()
    assert not p.is_symlink() and len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['mode']
def verify_prepared(closed=False):
    idx=js('FIXED_PAYLOAD_INDEX.json');ready=js('READY.json')
    assert idx['schema']=='pr53-current-prepared-index/v1' and ready['schema']=='pr53-current-source-ready/v1'
    assert ready['manifest_absent_at_handoff'] is True and ready['root_approval'] is False
    assert ready['fixed_index_sha256']==sha((F/'FIXED_PAYLOAD_INDEX.json').read_bytes())
    for key,name in [('report_sha256','REPORT.md'),('verdict_sha256','VERDICT.json'),('external_references_sha256','EXTERNAL_REFERENCES.json'),('science_index_sha256','SCIENCE_INDEX.json')]:assert ready[key]==sha((F/name).read_bytes())
    assert ready['original_substantive_attempts']==0 and ready['new_proof_search_turns']==0 and ready['new_paper'] is False
    assert ready['required_math_corrections']==[] and ready['payload_files']<=45
    expected={x['path'] for x in idx['files']}|{'FIXED_PAYLOAD_INDEX.json','READY.json'}
    if closed:expected.add('MANIFEST.json')
    files,dirs=topology();assert set(files)==expected and len(files)==len(expected) and dirs==idx['directories']
    for row in idx['files']:check(row)
    for name in ['FIXED_PAYLOAD_INDEX.json','READY.json']:assert mode(F/name)=='0444'
    for rel in dirs:assert mode(F if rel=='.' else F/rel)=='0755'
    ext=js('EXTERNAL_REFERENCES.json');n=0
    for g in ext['closed_families']+ext['actual_root_captures']:
        for row in g['rows']:check(row,True);n+=1
        for row in g.get('directories',[]):assert mode(R/row['repo_path'])==row['mode']
    c=js('actual_preparation_check/CAPTURE.json');d=F/'actual_preparation_check'
    assert c['exit_code']==0 and type(c['pid']) is int and c['pid']>0 and c['cwd']==str(R)
    assert c['argv']==['/usr/bin/python3','-B',str(F/'verify_current.py')]
    assert datetime.datetime.fromisoformat(c['started_at'])<=datetime.datetime.fromisoformat(c['completed_at'])
    assert c['operator_unchanged'] and c['child_unchanged']
    assert sha((d/'prelaunch_operator.py').read_bytes())==c['operator_sha256']
    assert sha((d/'prelaunch_child.py').read_bytes())==c['child_sha256']==sha((F/'verify_current.py').read_bytes())
    for key in ['stdout','stderr']:
        r=c[key];b=(d/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
    out=json.loads((d/'stdout.bin').read_bytes());assert out['status']=='PASS_SOURCE_PREPARATION_ONLY' and out['root_approval'] is False
    return idx,ready,n
