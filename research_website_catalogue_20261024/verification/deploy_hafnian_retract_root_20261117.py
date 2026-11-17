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

assert not E.exists()
E.mkdir()
before=state()
assert before['public']['regular_files']==790 and before['public']['child_directories']==381
assert before['W']['controls']['index']['SHA256']=='25494ed68b5d5612ae64ac01f2897c77b26024a994b66167426203d5620de4b7'
assert (W/'.git/refs/heads/master').read_text()==COMMIT+'\n'
assert before['M']['controls']['index']['SHA256']=='91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11'
assert before['firebase']['firebase.json']['SHA256']=='47bc3e4c1a61d99890ef108a28e7504eeafe2aa1c81bbfd51c20f62d808852a4'
assert before['firebase']['.firebaserc']['SHA256']=='a0c6d74d33098b189fa74ba069059310fc4b293d76a1c4674e9686c4fef1e01d'
save('LOCAL_BEFORE.json',before)
command=['/opt/homebrew/bin/firebase','hosting:channel:list','--project','aleckriebel-bd92e','--json','--non-interactive']
old=live(call('HOSTING_BEFORE',command))
assert old['name'].endswith('/versions/474f691fb1557456') and old['status']=='FINALIZED'
assert state()==before
save('ROOT_DEPLOYMENT_DECISION.json',dict(UTC=now(),authorization='User persistent goal expressly authorizes routine website deployment; root separately adopts this actual verified scoped commit for hosting.',
    commit=COMMIT,whole_local_before_exact=True,only_hosting=True,project='aleckriebel-bd92e',
    previous_live_version=old['name'],automatic_rollback_or_retry=False,
    on_failure='Preserve literal results and state; root review before any recovery.',AA=None,actual_UI_verification=False))
deployed=call('DEPLOY',['/opt/homebrew/bin/firebase','deploy','--only','hosting','--project','aleckriebel-bd92e','--json','--non-interactive'])
new=live(call('HOSTING_AFTER',command))
assert new['status']=='FINALIZED' and new['name']!=old['name']
assert int(new['fileCount'])==int(old['fileCount'])+9
after=state()
save('LOCAL_AFTER.json',after)
assert after==before
result=dict(UTC=now(),status='HOSTING_DEPLOYED_LOCAL_GUARDS_EXACT',commit=COMMIT,
    old_live_version=old['name'],new_live_version=new['name'],hosting_file_count=int(new['fileCount']),
    all_native_M_W_controls_localheads_and_public_bytes_modes_exact=True,
    deployment_exit=0,live_HTTP_and_actual_UI_verification_pending=True,AA=None)
save('DEPLOYMENT_FINAL.json',result)
print(json.dumps(result))
