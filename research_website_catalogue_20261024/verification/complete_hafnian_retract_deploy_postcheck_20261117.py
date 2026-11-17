from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, stat, subprocess, time

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M=P.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
E=P/'verification/hafnian-retract-live-root-20261117'
COMMIT='217d41c0a9344aed9caacee7aed31d4f23b77e47'

def now(): return datetime.now(timezone.utc).isoformat()
def pin(path):
    s=path.lstat()
    assert stat.S_ISREG(s.st_mode)
    return dict(bytes=s.st_size,SHA256=sha256(path.read_bytes()).hexdigest(),mode=oct(stat.S_IMODE(s.st_mode)))
def tree(root):
    files,dirs={}, {'.':oct(stat.S_IMODE(root.stat().st_mode))}
    for path in sorted(root.rglob('*')):
        assert not path.is_symlink()
        name=path.relative_to(root).as_posix()
        if path.is_file(): files[name]=pin(path)
        else:
            assert path.is_dir()
            dirs[name]=oct(stat.S_IMODE(path.stat().st_mode))
    return dict(root=str(root),files=files,directories=dirs,regular_files=len(files),child_directories=len(dirs)-1)
def native(root):
    packed=root/'.git/packed-refs'
    local=[line for line in packed.read_text().splitlines() if ' refs/heads/' in line] if packed.exists() else []
    return dict(root=str(root),controls={name:pin(root/'.git'/name) for name in ['HEAD','index','config']},
                loose_heads=tree(root/'.git/refs/heads'),packed_local_lines=local,
                packed_mode=oct(stat.S_IMODE(packed.stat().st_mode)) if packed.exists() else None)
def state():
    return dict(M=native(M),W=native(W),public=tree(W/'public'),
                firebase={name:pin(W/name) for name in ['firebase.json','.firebaserc']})
def save(name,value):
    path=E/name
    assert not path.exists()
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def call(name,args):
    started=now();clock=time.monotonic()
    r=subprocess.run(args,cwd=W,capture_output=True)
    (E/(name+'.stdout')).write_bytes(r.stdout)
    (E/(name+'.stderr')).write_bytes(r.stderr)
    receipt=dict(startUTC=started,endUTC=now(),elapsed_seconds=time.monotonic()-clock,
        argv=args,cwd=str(W),exit=r.returncode,stdout_bytes=len(r.stdout),stderr_bytes=len(r.stderr),
        stdout_SHA256=sha256(r.stdout).hexdigest(),stderr_SHA256=sha256(r.stderr).hexdigest())
    save(name+'.execution.json',receipt)
    assert r.returncode==0,(name,r.returncode)
    data=json.loads(r.stdout)
    assert data['status']=='success',name
    return data
def live(data):
    rows=[c for c in data['result']['channels'] if c['name']=='projects/aleckriebel-bd92e/sites/aleckriebel-bd92e/channels/live']
    assert len(rows)==1
    return rows[0]['release']['version']

assert E.is_dir()
before=json.loads((E/'LOCAL_BEFORE.json').read_text())
execution=json.loads((E/'DEPLOY.execution.json').read_text())
deployed=json.loads((E/'DEPLOY.stdout').read_text())
old=live(json.loads((E/'HOSTING_BEFORE.stdout').read_text()))
new=live(json.loads((E/'HOSTING_AFTER.stdout').read_text()))
assert execution['exit']==0 and deployed['status']=='success'
assert new['status']=='FINALIZED' and new['name'].endswith('/versions/9d7f8c6526f4153b')
assert deployed['result']['hosting'].endswith('/versions/9d7f8c6526f4153b')
assert old['name'].endswith('/versions/474f691fb1557456')
after=state()
save('LOCAL_AFTER.json',after)
assert after==before
failure=dict(UTC=now(),old_root_script_exit=1,actual_deployment_exit=0,
 exact_diagnosis='Optional fileCount absent in actual finalized version object. The original postcondition wrongly indexed it. This happened after one successful deployment and after new live version/status were verified.',
 original_script_unchanged=True,deployment_not_repeated=True,
 original_failure_not_retroactively_passed=True,
 remaining_native_and_whole_public_checks_completed_here=True,
 stream_limit='Original root traceback is retained in the tool result, not claimed as separately binary-captured stderr.')
save('POSTCONDITION_SCHEMA_FAILURE.json',failure)
result=dict(UTC=now(),status='HOSTING_DEPLOYED_LOCAL_GUARDS_EXACT',commit=COMMIT,
 old_live_version=old['name'],new_live_version=new['name'],
 actual_hosting_fileCount_if_reported=new.get('fileCount'),
 expected_served_files_from_unchanged_ignore_and_nine_additions=int(old['fileCount'])+9,
 optional_metric_not_used_as_publication_certificate=True,
 all_native_M_W_controls_localheads_and_public_bytes_modes_exact=True,
 deployment_attempts=1,deployment_exit=0,root_old_postcondition_failed_retained=True,
 continuation_data_checks_exit=0,live_HTTP_and_actual_UI_verification_pending=True,AA=None)
save('DEPLOYMENT_FINAL.json',result)
print(json.dumps(result))
