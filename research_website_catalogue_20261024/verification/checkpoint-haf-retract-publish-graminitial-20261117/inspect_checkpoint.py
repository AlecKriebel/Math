"""Metadata-only tree/byte/mode/closure audit; no scientific source execution."""
import base64, collections, datetime, hashlib, json, os, stat, subprocess, sys
from pathlib import Path

if not __debug__:
    raise RuntimeError('Checkpoint guards require Python assertions enabled')

M = Path('/Users/alec/Documents/Math')
P = M/'research_website_catalogue_20261024'
OWN = P/'verification/checkpoint-haf-retract-publish-graminitial-20261117'
assert sys.argv[1:] in (['dry'], ['post'])
phase = sys.argv[1]
release = json.loads((OWN/'WRITEHOLD_RELEASE.json').read_bytes())
assert release['authorization'] == 'WRITEHOLD_RELEASE_TO_CHECKPOINT'
prefix = P.name+'/'
name = 'DRY_RUN' if phase == 'dry' else 'PUSH'
invocation = json.loads((OWN/(name+'.invocation.json')).read_bytes())
receipt = json.loads((OWN/(name+'.receipt.json')).read_bytes())
assert invocation['exit_code'] == 0
assert receipt['parent'] == release['expected_parent'] == '15482acd0ef864af280a864758b2ac6aa24dfbe8'
parent, tree = receipt['parent'], receipt['tree']
env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_COUNT='2', GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null', GIT_CONFIG_KEY_1='core.fsmonitor', GIT_CONFIG_VALUE_1='false')
for k in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):
    env.pop(k, None)
calls = []
def git(*args, data=None, allow=(0,)):
    argv = ['/usr/bin/git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','gc.auto=0',*args]
    r = subprocess.run(argv, cwd=M, env=env, input=data, capture_output=True, check=False)
    calls.append(dict(argv=argv, exit_code=r.returncode, stdout_bytes=len(r.stdout), stdout_SHA256=hashlib.sha256(r.stdout).hexdigest(), stderr_base64=base64.b64encode(r.stderr).decode()))
    assert r.returncode in allow, r.stderr.decode(errors='replace')
    return r.stdout

def entries(ref, *paths, recursive=False):
    args = ['ls-tree']+(['-r'] if recursive else [])+['-z','--full-tree',ref]
    if paths:
        args += ['--',*paths]
    result = {}
    for row in git(*args).split(b'\0'):
        if row:
            header, name = row.split(b'\t',1)
            mode, kind, oid = header.decode().split()
            name = name.decode()
            assert name not in result
            result[name] = dict(mode=mode, type=kind, OID=oid)
    return result

def local_pin(path):
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode) and not path.is_symlink(), str(path)
    h = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576), b''):
            h.update(block)
            size += len(block)
    after = path.lstat()
    assert (before.st_dev,before.st_ino,before.st_mode,before.st_size,before.st_mtime_ns,before.st_ctime_ns) == (after.st_dev,after.st_ino,after.st_mode,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
    assert size == after.st_size
    return dict(bytes=size,SHA256=h.hexdigest(),mode='100755' if after.st_mode & stat.S_IXUSR else '100644',filesystem_mode=oct(stat.S_IMODE(after.st_mode)))

def blob_pins(paths, leaves):
    if not paths:
        return {}
    raw = git('cat-file','--batch',data=('\n'.join(tree+':'+n for n in paths)+'\n').encode())
    result, cursor = {}, 0
    for path in paths:
        end = raw.index(b'\n',cursor)
        oid, kind, size = raw[cursor:end].decode().split()
        cursor = end+1
        size = int(size)
        blob = raw[cursor:cursor+size]
        assert raw[cursor+size:cursor+size+1] == b'\n' and len(blob) == size
        cursor += size+1
        assert kind == 'blob' and leaves[path]['OID'] == oid
        result[path] = dict(OID=oid,bytes=size,SHA256=hashlib.sha256(blob).hexdigest(),mode=leaves[path]['mode'])
    assert cursor == len(raw)
    return result

def ignore_rows(paths):
    if not paths:
        return []
    raw = git('check-ignore','--no-index','-v','-z','--stdin',data=('\0'.join(paths)+'\0').encode(),allow=(0,1))
    parts = raw.split(b'\0')
    assert parts[-1] == b'' and (len(parts)-1)%4 == 0
    return [dict(source=parts[i].decode(),line=parts[i+1].decode(),pattern=parts[i+2].decode(),path=parts[i+3].decode()) for i in range(0,len(parts)-1,4)]

oldroot, newroot = entries(parent), entries(tree)
assert set(oldroot) == set(newroot) and len(oldroot)-1 == receipt['sibling_root_entries_preserved'] == 159
assert {k:v for k,v in oldroot.items() if k != P.name} == {k:v for k,v in newroot.items() if k != P.name}
assert oldroot['docs'] == newroot['docs']
rawdiff = git('diff-tree','-r','--no-commit-id','--no-renames','--name-status','-z',parent,tree)
parts = rawdiff.split(b'\0')
assert parts[-1] == b'' and (len(parts)-1)%2 == 0
changes = [dict(status=parts[i].decode(),path=parts[i+1].decode()) for i in range(0,len(parts)-1,2)]
assert len(changes) == receipt['files'] and all(x['path'].startswith(prefix) for x in changes)
excluded = invocation['excluded_actual_directories']
assert all(not any(x['path'] == prefix+p or x['path'].startswith(prefix+p+'/') for p in excluded) for x in changes)
assert entries(parent,*[prefix+p for p in excluded],recursive=True) == entries(tree,*[prefix+p for p in excluded],recursive=True)
assert entries(parent,*[prefix+p for p in excluded]) == entries(tree,*[prefix+p for p in excluded])
leaves = entries(tree,P.name,recursive=True)
live = [x['path'] for x in changes if x['status'] != 'D']
blobrows = blob_pins(live,leaves)
allowed_drift = {prefix+'verification/PUSH_RECEIPT.json',prefix+'verification/checkpoint-subtree-dry-run-20261025.json'}
changed_evidence = []
for item in changes:
    path = item['path']
    if item['status'] == 'D':
        assert not os.path.lexists(M/path)
        changed_evidence.append(dict(**item,absent_from_current_filesystem=True))
        continue
    pin = local_pin(M/path)
    committed = blobrows[path]
    same = (pin['bytes'],pin['SHA256']) == (committed['bytes'],committed['SHA256'])
    assert same or path in allowed_drift, path
    assert pin['mode'] == committed['mode']
    changed_evidence.append(dict(**item,**committed,current_file_whole_bytes_equal=same,current_filesystem_mode=pin['filesystem_mode'],known_helper_receipt_drift=not same))

caches = []
actual_caches = []
for relative in release.get('private_cache_paths',[]):
    rel = Path(relative)
    assert not rel.is_absolute() and '..' not in rel.parts
    path = P/rel
    exists = os.path.lexists(path)
    committed = [n for n in leaves if n == prefix+relative or n.startswith(prefix+relative+'/')]
    assert not committed, relative
    caches.append(dict(path=relative,exists=exists,committed_leaves=0))
    if exists:
        assert path.is_dir() and not path.is_symlink()
        actual_caches.append(prefix+relative+'/')
cache_ignore = ignore_rows(actual_caches)
assert {x['path'] for x in cache_ignore if not x['pattern'].startswith('!')} == set(actual_caches)

closures = []
for spec in release['durable_tree_roots']:
    relative = spec['path'].rstrip('/')
    rel = Path(relative)
    assert not rel.is_absolute() and '..' not in rel.parts
    root = P/relative
    assert root.is_dir() and not root.is_symlink() and root.resolve().is_relative_to(P)
    local_files, directories = {}, {}
    pending = [root]
    while pending:
        here = pending.pop()
        before = here.lstat()
        assert stat.S_ISDIR(before.st_mode) and not here.is_symlink()
        for path in sorted(here.iterdir()):
            rel = path.relative_to(root).as_posix()
            pin = path.lstat()
            if stat.S_ISDIR(pin.st_mode):
                assert not path.is_symlink()
                directories[rel] = oct(stat.S_IMODE(pin.st_mode))
                pending.append(path)
            else:
                local_files[prefix+relative+'/'+rel] = local_pin(path)
        after = here.lstat()
        assert (before.st_dev,before.st_ino,before.st_mode,before.st_mtime_ns,before.st_ctime_ns) == (after.st_dev,after.st_ino,after.st_mode,after.st_mtime_ns,after.st_ctime_ns)
    if 'files' in spec:
        assert len(local_files) == spec['files'], (relative,len(local_files),spec['files'])
    if 'directories' in spec:
        assert len(directories) == spec['directories'], (relative,len(directories),spec['directories'])
    ignored_rows = ignore_rows(sorted(local_files))
    ignored = {x['path'] for x in ignored_rows if not x['pattern'].startswith('!')}
    expected = {n for n in local_files if n not in ignored}
    committed = {n for n in leaves if n.startswith(prefix+relative+'/')}
    assert expected == committed, dict(root=relative,missing=sorted(expected-committed),unexpected=sorted(committed-expected))
    pins = blob_pins(sorted(committed),leaves)
    for path in sorted(committed):
        a,b = local_files[path],pins[path]
        assert (a['bytes'],a['SHA256'],a['mode']) == (b['bytes'],b['SHA256'],b['mode']),path
    closures.append(dict(path=relative,root_mode=oct(stat.S_IMODE(root.lstat().st_mode)),all_local_regular_files=len(local_files),child_directories=directories,committed_regular_files=len(committed),ignored_regular_files=len(ignored),actual_ignore_rules=ignored_rows,all_committed_blob_metadata=pins,complete_current_nonignored_local_files_equal_committed_tree=True))

important = []
for relative in release['important_paths']:
    path = prefix+relative
    assert path in leaves
    pin = local_pin(M/path)
    if relative in release['expected_key_file_SHA256']:
        assert pin['SHA256'] == release['expected_key_file_SHA256'][relative],relative
    committed = blobrows[path] if path in blobrows else blob_pins([path],leaves)[path]
    assert (pin['bytes'],pin['SHA256'],pin['mode']) == (committed['bytes'],committed['SHA256'],committed['mode'])
    important.append(dict(path=path,**committed,filesystem_mode=pin['filesystem_mode'],current_whole_bytes_equal=True))

remote, commit_data, tree_delta = None, None, None
if phase == 'post':
    commit = receipt['commit']
    commit_data = git('cat-file','commit',commit).decode()
    header = commit_data.split('\n\n',1)[0].splitlines()
    assert header[0] == 'tree '+tree and [x for x in header if x.startswith('parent ')] == ['parent '+parent]
    assert any(x.startswith('author Alec Kriebel <me@aleckriebel.com> ') for x in header)
    assert any(x.startswith('committer Alec Kriebel <me@aleckriebel.com> ') for x in header)
    remote = git('ls-remote','origin','refs/heads/main').decode().strip()
    assert remote.split()[0] == commit
    dry = json.loads((OWN/'DRY_RUN.receipt.json').read_bytes())
    delta = git('diff-tree','-r','--no-commit-id','--no-renames','--name-only','-z',dry['tree'],tree)
    tree_delta = [x.decode() for x in delta.split(b'\0') if x]
    assert tree_delta == [prefix+'verification/checkpoint-subtree-dry-run-20261025.json'],tree_delta
result = dict(schema='actual-scoped-checkpoint-tree-closure-audit-v2',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),phase=phase,parent=parent,tree=tree,commit=receipt.get('commit'),changed_paths=len(changes),changes=changes,status_counts=dict(collections.Counter(x['status'] for x in changes)),all_changes_in_programme=True,sibling_root_entries_preserved=159,old_root_entries=oldroot,new_root_entries=newroot,docs_entry=oldroot['docs'],excluded_subtrees_exactly_at_parent=True,excluded_actual_paths=excluded,private_caches=caches,actual_cache_ignore_rules=cache_ignore,changed_whole_blob_byte_mode_metadata=changed_evidence,durable_packet_and_source_closures=closures,key_actual_committed_files=important,ordinary_commit_data=commit_data,fresh_actual_remote_main=remote,dry_to_push_tree_delta=tree_delta,git_calls=calls,scientific_report_contents_never_interpreted=True,scope='Checkpoint integrity only; no scientific promotion, source execution, website/deploy/Sheet action or release')
with (OWN/(phase.upper()+'_TREE_AUDIT.json')).open('x') as stream:
    json.dump(result,stream,indent=2)
    stream.write('\n')
with (OWN/(phase.upper()+'_PATHS.txt')).open('x') as stream:
    stream.write(''.join(x['status']+'\t'+x['path']+'\n' for x in changes))
print(json.dumps(dict(phase=phase,parent=parent,tree=tree,commit=receipt.get('commit'),changed_paths=len(changes),status_counts=result['status_counts'],siblings=159,docs=oldroot['docs'],closures=[dict(path=x['path'],files=x['all_local_regular_files'],directories=len(x['child_directories']),committed=x['committed_regular_files'],ignored=x['ignored_regular_files']) for x in closures],important_paths=len(important),dry_to_push_tree_delta=tree_delta)))
