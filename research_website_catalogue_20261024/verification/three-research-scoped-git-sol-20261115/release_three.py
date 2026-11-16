#!/usr/bin/env python3
"""Offline installed-state preflight by default. --commit needs exact root authorization.
No imports/execution of project code. Never use status/add/reset/clean/force.
"""
from pathlib import Path
import base64, datetime, hashlib, json, os, stat, struct, subprocess, sys

A = Path(__file__).absolute().parent
S = A.parent / 'three-research-private-stage-sol-20261115'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PARENT = '2b78e689e571e658daa859f29b97a61b9ec479ed'
OLD_TREE = '4392815cea2aab48096a321869e0e30ae616ecbc'
OLD_INDEX = '5f9c24f576cca18c466163a9572120f118698ead90eca728199030ba346e8244'
STAGE = '4f9cb2f5c8779a586bbfa34efc6f498d677bcd15826f28f7c4f4ecf33cd43b11'
ADOPTION = 'd0f165bf8e35935684b2580489a341587a376421e6838790d3c07c9e1472be4c'
BRANCH, MESSAGE = 'refs/heads/master', 'Publish three reviewed Zenodo research pages'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_OPTIONAL_LOCKS='0', GIT_INDEX_VERSION='2', GIT_TERMINAL_PROMPT='0')
OPTIONS = ['-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false', '-c', 'core.untrackedCache=false', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', '-c', 'commit.gpgsign=false', '-c', 'core.splitIndex=false', '-c', 'index.version=2', '-c', 'remote.origin.mirror=false']
LOG = None

def need(ok, why):
    if not ok: raise ValueError(why)

def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def packed(x): return (json.dumps(x, sort_keys=True, separators=(',', ':')) + '\n').encode()
def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)
def read(p):
    need(p.is_absolute() and '..' not in p.parts, 'absolute input')
    need(all(stat.S_ISDIR(q.lstat().st_mode) for q in p.parents), 'ordinary ancestors')
    before = p.lstat(); need(stat.S_ISREG(before.st_mode), 'ordinary file')
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        held = os.fstat(fd); need((held.st_dev, held.st_ino) == (before.st_dev, before.st_ino), 'opened identity')
        chunks = []
        while part := os.read(fd, 1048576): chunks.append(part)
        after, final = os.fstat(fd), p.lstat()
        need((held.st_size, held.st_mtime_ns, held.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns) and (held.st_dev, held.st_ino) == (final.st_dev, final.st_ino), 'stable read')
        body = b''.join(chunks); need(len(body) == held.st_size, 'complete buffer'); return body
    finally: os.close(fd)

def event(phase, **fields):
    if LOG is not None:
        LOG.write(packed({'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'phase': phase, **fields})); LOG.flush(); os.fsync(LOG.fileno())

def git(*args, data=None, index=None, identity=None):
    env = dict(ENV)
    if index is not None: env['GIT_INDEX_FILE'] = str(index)
    if identity is not None: env.update(identity)
    cmd = ['git', *OPTIONS, *args]
    r = subprocess.run(cmd, cwd=W, env=env, input=data, capture_output=True)
    if LOG is None and r.stderr: sys.stderr.buffer.write(r.stderr)
    event('git', argv=cmd, input_SHA256=None if data is None else sha(data), exit_code=r.returncode, stdout_base64=base64.b64encode(r.stdout).decode(), stderr_base64=base64.b64encode(r.stderr).decode())
    need(r.returncode == 0, 'Git command failed: ' + args[0])
    return r.stdout

def entries(body):
    need(body[:12] == b'DIRC' + struct.pack('>II', 2, struct.unpack('>I', body[8:12])[0]) and hashlib.sha1(body[:-20]).digest() == body[-20:], 'v2 index/checksum')
    result, pos, previous = {}, 12, None
    for unused in range(struct.unpack('>I', body[8:12])[0]):
        start = pos; flags = struct.unpack('>H', body[pos+60:pos+62])[0]
        need(not flags & 0x7000, 'ordinary stage-zero v2 record')
        end = body.index(b'\0', pos+62); name = body[pos+62:end]
        pos = start + ((end + 1 - start + 7) // 8) * 8
        need(name and (previous is None or previous < name) and not any(body[end+1:pos]) and flags & 0xfff == min(len(name), 0xfff), 'sorted unique padded record')
        result[name] = (body[start:pos], body[start+24:start+28], body[start+40:start+60]); previous = name
    while pos < len(body)-20:
        kind, size = body[pos:pos+4], struct.unpack('>I', body[pos+4:pos+8])[0]
        need(kind == b'TREE' and pos+8+size <= len(body)-20, 'only optional Git cache-tree extension')
        pos += 8 + size
    need(pos == len(body)-20, 'complete index extent')
    return result

def census(root):
    files, dirs = {}, set()
    for directory, names, leaves in os.walk(root, followlinks=False):
        for name in names:
            p = Path(directory)/name; need(stat.S_ISDIR(p.lstat().st_mode), 'ordinary public directory'); dirs.add(p.relative_to(root).as_posix())
        for name in leaves:
            p = Path(directory)/name; b = read(p); files[p.relative_to(root).as_posix()] = (len(b), sha(b))
    return files, dirs

def preflight(owned_lock=None):
    need(sha(read(S/'FINAL_SEAL.json')) == STAGE and sha(read(A.parent/'root-three-private-stage-adoption-20261115.json')) == ADOPTION, 'root adoption and frozen stage')
    seal = json.loads(read(S/'FINAL_SEAL.json')); mb = read(S/'OWNED_MANIFEST.json')
    need({'bytes': len(mb), 'SHA256': sha(mb)} == seal['manifest'], 'whole stage manifest')
    rows = [x for x in json.loads(mb)['files'] if x['path'].startswith('candidate/')]
    need(len(rows) == 19, 'exact candidate19')
    buffers = {}
    for row in rows:
        name = row['path'][10:]; b = read(S/row['path'])
        need(len(b) == row['bytes'] and sha(b) == row['SHA256'] and not any(p in ['', '.', '..'] for p in name.split('/')), 'candidate buffer/path')
        buffers[name] = b; need(read(W/name) == b and not (W/name).stat().st_mode & 0o111, 'installed candidate exact/nonexecutable')
    baseline = read(S/'WEBSITE_BASELINE.json'); br = next(x for x in json.loads(mb)['files'] if x['path'] == 'WEBSITE_BASELINE.json')
    need(len(baseline) == br['bytes'] and sha(baseline) == br['SHA256'], 'same-buffer frozen baseline'); base = json.loads(baseline)
    expected = {x['path']: (x['bytes'], x['SHA256']) for x in base['public_files']}; directories = set(base['public_directories'])
    for name, b in buffers.items():
        if name.startswith('public/'):
            rel = name[7:]; expected[rel] = (len(b), sha(b)); directories.update(str(p) for p in Path(rel).parents if str(p) != '.')
    need(len(expected) == 647 and census(W/'public') == (expected, directories), 'entire installed647 public namespace')
    for row in base['site_and_Git_controls']:
        if row['relative_path'] != 'firebase.json': need(sha(read(Path(row['path']))) == row['SHA256'], 'unchanged site/Git control')
    old = read(W/'.git/index'); need(sha(old) == OLD_INDEX and stat.S_IMODE((W/'.git/index').stat().st_mode) == 0o600, 'original58571 shared index0600')
    need(old == read(S/'raw/shared-index.before') and len(entries(old)) == 58571, 'original opaque index reference')
    lock = W/'.git/index.lock'
    need(not os.path.lexists(lock) if owned_lock is None else (lock.lstat().st_dev, lock.lstat().st_ino) == owned_lock, 'exclusive index lock state')
    need(git('symbolic-ref', 'HEAD').strip().decode() == BRANCH and git('rev-parse', 'HEAD').strip().decode() == PARENT and git('rev-parse', 'HEAD^{tree}').strip().decode() == OLD_TREE and git('rev-parse', '--show-object-format').strip() == b'sha1', 'existing master/parent/tree/SHA1')
    state = {'parent': PARENT, 'tree': OLD_TREE, 'branch': BRANCH, 'index': OLD_INDEX, 'installed647': sorted(expected.items()), 'installed_directories': sorted(directories), 'scope': [(n, len(b), sha(b)) for n, b in sorted(buffers.items())]}
    return buffers, old, sha(packed(state)), state

def main():
    global LOG
    need(sys.argv[1:] in [[], ['--commit']], 'default or explicit --commit only')
    buffers, old, fingerprint, state = preflight()
    if not sys.argv[1:]:
        print(json.dumps({'status': 'OFFLINE_INSTALLED_PREFLIGHT_PASS', 'preflight_SHA256': fingerprint, 'helper_SHA256': sha(read(A/'release_three.py')), 'candidate_files': state['scope'], 'expected_public_files': 647, 'expected_public_manifest_SHA256': sha(packed(state['installed647'])), 'expected_public_directories_SHA256': sha(packed(state['installed_directories'])), 'index_SHA256': OLD_INDEX, 'index_mode': '0600', 'HEAD': PARENT, 'tree': OLD_TREE, 'branch': BRANCH, 'remote_checked': False, 'writes': 0})); return
    auth_raw = read(A/'AUTHORIZATION.json'); auth = json.loads(auth_raw)
    fixed = {'schema': 'three-scoped-git-release-v1', 'action': 'COMMIT_AND_FAST_FORWARD_PUSH_19_PATHS', 'helper_SHA256': sha(read(A/'release_three.py')), 'preflight_SHA256': fingerprint, 'stage_FINAL_SHA256': STAGE, 'adoption_SHA256': ADOPTION, 'parent': PARENT, 'remote_parent': PARENT, 'branch': BRANCH, 'commit_message': MESSAGE}
    need(set(auth) == set(fixed) | {'author_name', 'author_email', 'commit_date', 'expires_UTC'} and all(auth[k] == v for k, v in fixed.items()), 'exact current root authorization')
    need(all(isinstance(auth[k], str) and auth[k] and '\n' not in auth[k] and '\0' not in auth[k] for k in ['author_name', 'author_email', 'commit_date', 'expires_UTC']), 'literal identity/dates')
    expiry = datetime.datetime.fromisoformat(auth['expires_UTC'])
    need(datetime.datetime.fromisoformat(auth['commit_date']).utcoffset() is not None and expiry.utcoffset() is not None and datetime.datetime.now(datetime.timezone.utc) < expiry, 'current timezone-qualified authorization')
    raw = A/'raw'; need(stat.S_ISDIR(raw.lstat().st_mode), 'preignored ordinary owned raw directory')
    fd = os.open(raw/'events.jsonl', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600); os.fchmod(fd, 0o600); LOG = os.fdopen(fd, 'wb')
    event('authorized', authorization_SHA256=sha(auth_raw), preflight_SHA256=fingerprint)
    sync_dir(raw)
    need(git('ls-remote', '--exit-code', 'origin', BRANCH) == (PARENT+'\t'+BRANCH+'\n').encode(), 'remote parent unchanged')
    temp = raw/'scoped.index'; fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600); os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'wb') as stream: stream.write(old); stream.flush(); os.fsync(stream.fileno())
    sync_dir(raw)
    oids = {n: blob(b) for n, b in buffers.items()}
    for name, b in sorted(buffers.items()): need(git('hash-object', '--no-filters', '-w', '--stdin', data=b).strip().decode() == oids[name], 'raw unfiltered blob')
    git('update-index', '--add', '-z', '--index-info', data=b''.join(('100644 '+oids[n]+'\t'+n).encode()+b'\0' for n in sorted(buffers)), index=temp)
    tree = git('write-tree', index=temp).strip().decode(); staged = read(temp); before, after = entries(old), entries(staged); targets = {n.encode() for n in buffers}
    need(len(after) == 58587 and set(after) == set(before) | targets and sum(n not in targets for n in before) == 58568, 'exact58587 / protected58568')
    need(all(after[n] == record for n, record in before.items() if n not in targets), 'every untargeted raw record unchanged')
    need(all(after[n.encode()][1:] == (struct.pack('>I', 0o100644), bytes.fromhex(oids[n])) for n in buffers), 'all19 staged raw blob IDs/modes')
    diff = git('diff-tree', '--raw', '-r', '--no-commit-id', '--no-abbrev', '--no-renames', '--no-ext-diff', '-z', OLD_TREE, tree).split(b'\0'); need(diff.pop() == b'' and len(diff) == 38, 'exact19 tree delta')
    need({diff[i+1] for i in range(0, len(diff), 2)} == targets and all(diff[i].split()[1] == b'100644' and diff[i].split()[3].decode() == oids[diff[i+1].decode()] and diff[i].split()[4] in [b'A', b'M'] for i in range(0, len(diff), 2)), 'scope-only tree delta')
    need(sum(diff[i].split()[4] == b'A' for i in range(0, len(diff), 2)) == 16 and sum(diff[i].split()[4] == b'M' for i in range(0, len(diff), 2)) == 3, '16 additions and3 replacements')
    lock = W/'.git/index.lock'; fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600); os.fchmod(fd, 0o600); held = os.fstat(fd); owner = (held.st_dev, held.st_ino); ref_attempted = False; event('shared_index_lock_acquired', device=held.st_dev, inode=held.st_ino)
    try:
        with os.fdopen(fd, 'wb') as stream: stream.write(staged); stream.flush(); os.fsync(stream.fileno())
        need(preflight(owner)[2] == fingerprint, 'final installed/HEAD/index fence under owned lock')
        need(read(A/'AUTHORIZATION.json') == auth_raw and datetime.datetime.now(datetime.timezone.utc) < expiry, 'same current authorization before commit object')
        identity = {f'GIT_{role}_{key}': auth[value] for role in ['AUTHOR', 'COMMITTER'] for key, value in [('NAME', 'author_name'), ('EMAIL', 'author_email'), ('DATE', 'commit_date')]}
        commit = git('commit-tree', tree, '-p', PARENT, data=(MESSAGE+'\n').encode(), identity=identity).strip().decode(); event('commit_object', commit=commit, tree=tree)
        need(read(A/'AUTHORIZATION.json') == auth_raw and datetime.datetime.now(datetime.timezone.utc) < expiry, 'same current authorization before CAS')
        event('CAS_REF_ATTEMPT', commit=commit); ref_attempted = True; git('update-ref', BRANCH, commit, PARENT); event('local_ref_advanced', commit=commit)
        need((lock.lstat().st_dev, lock.lstat().st_ino) == owner, 'own lock before atomic replacement'); os.replace(lock, W/'.git/index'); sync_dir(W/'.git'); event('shared_index_replaced', SHA256=sha(staged))
    except BaseException:
        if not ref_attempted and os.path.lexists(lock) and (lock.lstat().st_dev, lock.lstat().st_ino) == owner: lock.unlink(); event('own_pre_ref_lock_removed')
        raise
    need(read(W/'.git/index') == staged and stat.S_IMODE((W/'.git/index').stat().st_mode) == 0o600 and git('rev-parse', BRANCH).strip().decode() == commit, 'local committed state exact')
    git('push', '--no-follow-tags', '--recurse-submodules=no', 'origin', commit+':'+BRANCH)
    need(git('ls-remote', '--exit-code', 'origin', BRANCH) == (commit+'\t'+BRANCH+'\n').encode(), 'remote commit verified')
    need(read(W/'.git/index') == staged and stat.S_IMODE((W/'.git/index').stat().st_mode) == 0o600 and git('rev-parse', BRANCH).strip().decode() == commit, 'local index/ref preserved through push')
    event('release_verified', commit=commit, tree=tree); print(json.dumps({'status': 'SCOPED_COMMIT_AND_PUSH_VERIFIED', 'commit': commit, 'tree': tree, 'paths': 19, 'protected_raw_records': 58568}))

if __name__ == '__main__':
    try: main()
    except BaseException as error:
        event('FAILED_HISTORY_RETAINED', error=repr(error)); raise
