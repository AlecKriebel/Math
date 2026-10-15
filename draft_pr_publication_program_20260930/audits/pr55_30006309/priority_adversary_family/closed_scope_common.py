"""Fixed priority SOURCE custody only; no mathematical or native approval."""
import datetime,hashlib,json,pathlib,stat
from verify_priority import check_sources
F=pathlib.Path(__file__).absolute().parent
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
def check(row):
    p=F/row['path'];b=p.read_bytes()
    assert len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['mode']
def verify_prepared(closed=False):
    idx=js('FIXED_PAYLOAD_INDEX.json');ready=js('READY.json')
    assert idx['schema']=='pr55-priority-prepared-index/v1' and ready['schema']=='pr55-priority-source-ready/v1'
    assert ready['fixed_index_sha256']==sha((F/'FIXED_PAYLOAD_INDEX.json').read_bytes())
    assert ready['manifest_absent_at_handoff'] is True and ready['root_acceptance'] is False and ready['priority_cleared'] is False
    for key,name in [('report_sha256','REPORT.md'),('verdict_sha256','VERDICT.json'),('external_references_sha256','EXTERNAL_REFERENCES.json'),('specialization_sha256','ESTEROV_SPECIALIZATION.md')]:
        assert ready[key]==sha((F/name).read_bytes())
    expected={x['path'] for x in idx['files']}|{'FIXED_PAYLOAD_INDEX.json','READY.json'}
    if closed:expected.add('MANIFEST.json')
    files,dirs=topology();assert set(files)==expected and len(files)==len(expected) and dirs==idx['directories']
    for row in idx['files']:check(row)
    for name in ['FIXED_PAYLOAD_INDEX.json','READY.json']:assert mode(F/name)=='0444'
    for rel in dirs:assert mode(F if rel=='.' else F/rel)=='0755'
    n=check_sources()
    c=js('actual_preparation_check/CAPTURE.json')
    assert c['exit_code']==0 and c['root_authority'] is False and c['is_root_closure'] is False
    assert type(c['pid']) is int and c['pid']>0 and c['cwd']==str(R)
    assert c['argv']==['/usr/bin/python3','-B',str(F/'verify_priority.py')]
    assert datetime.datetime.fromisoformat(c['started_at'])<=datetime.datetime.fromisoformat(c['completed_at'])
    assert c['operator_unchanged'] and c['child_unchanged']
    assert c['operator_sha256']==sha((F/'capture_preparation.py').read_bytes())==sha((F/'actual_preparation_check/prelaunch_operator.py').read_bytes())
    for key in ['stdout','stderr']:
        b=(F/'actual_preparation_check'/f'{key}.bin').read_bytes()
        assert len(b)==c[key]['bytes'] and sha(b)==c[key]['sha256']
    assert js('actual_preparation_check/stdout.bin')['status']=='PASS_SOURCE_PRIORITY_PREPARATION_ONLY'
    assert c['child_sha256']==sha((F/'verify_priority.py').read_bytes())==sha((F/'actual_preparation_check/prelaunch_child.py').read_bytes())
    return idx,ready,n
