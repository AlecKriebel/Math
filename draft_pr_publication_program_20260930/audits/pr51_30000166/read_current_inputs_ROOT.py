from pathlib import Path
import hashlib,json,stat,subprocess,datetime
A=Path(__file__).absolute().parent
F=A/'current_preparation_family'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(F/'EXTERNAL_BINDINGS.json')=='863e49e8546efdc01069ff1ffdf80d82591ab276ee448e05da296e7ca7f56166'
d=json.loads((F/'EXTERNAL_BINDINGS.json').read_bytes())
assert d['schema']=='pr51-current-external-normalized-bindings/v1' and d['future_authority'] is False
rows=[]
for group in d['closed_inputs']:
    for z in group['directories']:
        p=Path(z['path']);assert p.is_dir() and not p.is_symlink()
        assert stat.S_IMODE(p.stat().st_mode)==int(z['full_mode'],8)
    rows.extend(group['rows'])
for group in d['actual_root_capture_references']:rows.extend(group['rows'])
assert len(rows)==d['rows_count']==273
seen=set()
for z in rows:
    p=Path(z['path']);assert p.is_absolute() and p.is_file() and not p.is_symlink()
    assert all(not q.is_symlink() for q in p.parents)
    assert str(p) not in seen;seen.add(str(p))
    b=p.read_bytes();assert type(z['bytes']) is int and len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256']
    assert stat.S_IMODE(p.stat().st_mode)==int(z['full_mode'],8)
for z in d['actual_root_capture_references']:
    rr=[x for x in z['rows'] if x['path'].endswith('/CAPTURE.json')];assert len(rr)==1
    c=json.loads(Path(rr[0]['path']).read_bytes())
    assert c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and c['status']=='PASS'
    assert c['pid']==z['actual_child_pid'] and c['argv']==z['actual_argv'] and c['cwd']==z['actual_cwd']
    assert c['started_utc']==z['started_utc'] and c['finished_utc']==z['finished_utc']
cmd=['/usr/bin/python3','-B',str(F/'verify_closed_family.py'),'--expected-index-sha256','b158dc5bbb0c583d8e29f67af3defce91a8850cd2a586c1dc8908bd662805f1a','--expected-ready-sha256','0d2cfe38d254db586a3b35c36b108ace6f8800489b05a8eac6cdf15ff4be3f29','--expected-manifest-sha256','7ece84cf8366514b959b867aa95b690931a94ae3e8e1ce1ef14089a399f70844']
p=subprocess.run(cmd,capture_output=True,check=True)
assert p.stderr==b''
print(p.stdout.decode(),end='')
print(json.dumps({'status':'PASS_ROOT_CURRENT_SCIENCE_AND_ALL_EXTERNAL_ROWS','external_rows':273,'root_actual_capture_references':6,'science_files':31,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'new_mathematical_approval_created':False,'native_mutations':False}))
