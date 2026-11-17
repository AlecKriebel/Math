"""Passive complete native/local-head/public guards for the scoped checkpoint."""
import base64, datetime, hashlib, json, os
from pathlib import Path

if not __debug__:
    raise RuntimeError('Checkpoint guards require Python assertions enabled')
import stat, subprocess, sys

M = Path('/Users/alec/Documents/Math')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
P = M/'research_website_catalogue_20261024'
OWN = P/'verification/checkpoint-d4-pass144-20261117'
assert sys.argv[1:] in (['before'],['after'])
phase = sys.argv[1]
release = json.loads((OWN/'ROOT_RELEASE.json').read_bytes())
assert release['authorization'] == 'ROOT_RELEASE_TO_CHECKPOINT'

def record(path):
    a = path.lstat()
    assert stat.S_ISREG(a.st_mode) and not path.is_symlink()
    fd = os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        assert (a.st_dev,a.st_ino) == (opened.st_dev,opened.st_ino)
        chunks = []
        while True:
            b = os.read(fd,1048576)
            if not b:
                break
            chunks.append(b)
        z = os.fstat(fd)
        assert (opened.st_dev,opened.st_ino,opened.st_size,opened.st_mode,opened.st_mtime_ns,opened.st_ctime_ns) == (z.st_dev,z.st_ino,z.st_size,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
        raw = b''.join(chunks)
        assert len(raw) == z.st_size
        return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),mode=oct(stat.S_IMODE(z.st_mode))), raw
    finally:
        os.close(fd)

def census(root):
    files,dirs = {},{}
    pending = [root]
    while pending:
        here = pending.pop()
        a = here.lstat()
        assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for path in sorted(here.iterdir()):
            rel = path.relative_to(root).as_posix()
            z = path.lstat()
            if stat.S_ISDIR(z.st_mode):
                assert not path.is_symlink()
                dirs[rel] = oct(stat.S_IMODE(z.st_mode))
                pending.append(path)
            else:
                files[rel] = record(path)[0]
        z = here.lstat()
        assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns) == (z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(root=str(root),root_mode=oct(stat.S_IMODE(root.lstat().st_mode)),files=files,directories=dirs)

env = dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='core.hooksPath',GIT_CONFIG_VALUE_0='/dev/null',GIT_CONFIG_KEY_1='core.fsmonitor',GIT_CONFIG_VALUE_1='false')
for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):
    env.pop(key,None)
calls = []
def git(root,*args):
    argv = ['/usr/bin/git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','gc.auto=0',*args]
    r = subprocess.run(argv,cwd=root,env=env,capture_output=True,check=False)
    calls.append(dict(cwd=str(root),argv=argv,exit_code=r.returncode,stdout_base64=base64.b64encode(r.stdout).decode(),stderr_base64=base64.b64encode(r.stderr).decode()))
    assert r.returncode == 0, r.stderr.decode(errors='replace')
    return r.stdout

repos = {}
for label,root in [('M',M),('W',W)]:
    paths = {}
    for name in ('HEAD','index','config','config.worktree'):
        p = Path(git(root,'rev-parse','--git-path',name).decode().strip())
        if not p.is_absolute():
            p = root/p
        paths[name] = dict(path=str(p),exists=p.exists())
        if p.exists():
            pin,raw = record(p)
            paths[name].update(pin)
            if name == 'HEAD':
                paths[name]['raw_base64'] = base64.b64encode(raw).decode()
    heads = Path(git(root,'rev-parse','--git-path','refs/heads').decode().strip())
    if not heads.is_absolute():
        heads = root/heads
    refs = git(root,'for-each-ref','--format=%(refname)%00%(objectname)%00%(objecttype)','refs/heads').decode()
    packed = Path(git(root,'rev-parse','--git-path','packed-refs').decode().strip())
    if not packed.is_absolute():
        packed = root/packed
    packed_pin,packed_raw = record(packed)
    local_raw_lines = [line for line in packed_raw.splitlines(keepends=True) if len(line.split())==2 and line.split()[1].startswith(b'refs/heads/')]
    assert len(local_raw_lines) == len({line.split()[1] for line in local_raw_lines})
    repos[label] = dict(root=str(root),HEAD=git(root,'rev-parse','HEAD').decode().strip(),branch=git(root,'branch','--show-current').decode().strip(),native_files=paths,logical_local_heads=refs,loose_local_heads=census(heads),packed_local_heads=dict(path=str(packed),mode=packed_pin['mode'],raw_lines_base64=[base64.b64encode(line).decode() for line in local_raw_lines]))
assert repos['M']['native_files']['index']['bytes'] == 25854746
assert repos['W']['native_files']['index']['bytes'] == 9062142
assert git(W,'rev-parse','HEAD^{tree}').decode().strip() == 'a9c5a4f3e30eb976bbe4f9c1872e14a92e22cc7e'
assert repos['M']['native_files']['config']['SHA256']=='2c083de0f0839443ce1ed062a8c1f2be83cbc30f838e5350e567a8153b7b3a47'
immutable_packets = {relative:census(P/relative) for relative in release['immutable_packet_paths']}
public = census(W/'public')
active_paths = release['authorized_active_verification_paths'] + ['verification/'+OWN.name]
active = []
for relative in active_paths:
    path = P/relative
    active.append(dict(path=relative,exists=path.exists(),regular_directory=path.is_dir() and not path.is_symlink()))
result = dict(schema='checkpoint-native-localheads-public-guards-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),phase=phase,repositories=repos,public=public,immutable_packets=immutable_packets,active_exclusion_discovery=active,protected_boundary='Exact native HEAD/index/config/config.worktree and logical/loose local branch heads; complete W/public bytes/modes/topology. FETCH_HEAD, remote-tracking refs and Git object additions are outside equality by root clarification.',helper=record(P/'scripts/checkpoint_subtree.py')[0],git_calls=calls)
assert repos['M']['HEAD']=='a4ce3c37dad209339e490d18dcced6c48cf912d2' and repos['M']['branch']=='main'
assert repos['M']['native_files']['index']['SHA256']=='91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11'
assert repos['W']['HEAD']=='4cc09d6bbbad61aa11077c5002cf84a1e93b1344' and repos['W']['branch']=='master'
assert repos['W']['native_files']['index']['SHA256']=='6b76dc0a4e7a631587aec1c081057479883573f7ff284dfc88b5adad02317179'
assert len(public['files'])==803 and len(public['directories'])==387 and public['root_mode']=='0o750'
with (OWN/('GUARDS_'+phase.upper()+'.json')).open('x') as stream:
    json.dump(result,stream,indent=2)
    stream.write('\n')
if phase == 'after':
    old = json.loads((OWN/'GUARDS_BEFORE.json').read_bytes())
    assert result['repositories'] == old['repositories'] and result['public'] == old['public']
    assert result['immutable_packets'] == old['immutable_packets']
print(json.dumps(dict(phase=phase,M_HEAD=repos['M']['HEAD'],W_HEAD=repos['W']['HEAD'],M_index= repos['M']['native_files']['index'],W_index=repos['W']['native_files']['index'],public_files=len(public['files']),public_dirs=len(public['directories']),active_exclusions=active,protected_exact=True if phase=='after' else None)))
