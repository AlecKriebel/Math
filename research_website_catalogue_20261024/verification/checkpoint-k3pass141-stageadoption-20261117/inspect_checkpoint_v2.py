"""Read-only actual tree/path/blob/ignore inspection, never write-tree or index mutation."""
import base64, collections, datetime, hashlib, json, os
from pathlib import Path
import stat, subprocess, sys

M = Path('/Users/alec/Documents/Math')
P = M/'research_website_catalogue_20261024'
OWN = P/'verification/checkpoint-k3pass141-stageadoption-20261117'
assert sys.argv[1:] in (['dry'],['post'])
phase = sys.argv[1]
prefix = P.name+'/'
invocation = json.loads((OWN/('DRY_RUN.invocation.json' if phase=='dry' else 'PUSH.invocation.json')).read_bytes())
receipt = json.loads((OWN/('DRY_RUN.receipt.json' if phase=='dry' else 'PUSH.receipt.json')).read_bytes())
assert invocation['exit_code'] == 0 and receipt['parent'] == '736c42d516805462cec410ce5ae8366962e38bbe'
parent,tree = receipt['parent'],receipt['tree']
env = dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='core.hooksPath',GIT_CONFIG_VALUE_0='/dev/null',GIT_CONFIG_KEY_1='core.fsmonitor',GIT_CONFIG_VALUE_1='false')
for k in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):
    env.pop(k,None)
calls = []
def git(*args,data=None,allow=(0,)):
    argv = ['/usr/bin/git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','gc.auto=0',*args]
    r = subprocess.run(argv,cwd=M,env=env,input=data,capture_output=True,check=False)
    calls.append(dict(argv=argv,exit_code=r.returncode,stdout_bytes=len(r.stdout),stdout_SHA256=hashlib.sha256(r.stdout).hexdigest(),stderr_base64=base64.b64encode(r.stderr).decode()))
    assert r.returncode in allow,r.stderr.decode(errors='replace')
    return r.stdout

def entries(ref,*paths,recursive=False):
    args = ['ls-tree']+(['-r'] if recursive else [])+['-z','--full-tree',ref]
    if paths:
        args += ['--',*paths]
    result = {}
    for row in git(*args).split(b'\0'):
        if not row:
            continue
        header,name = row.split(b'\t',1)
        mode,kind,oid = header.decode().split()
        name = name.decode()
        assert name not in result
        result[name] = dict(mode=mode,type=kind,OID=oid)
    return result

oldroot,newroot = entries(parent),entries(tree)
assert set(oldroot) == set(newroot)
assert len(oldroot)-1 == receipt['sibling_root_entries_preserved'] == 159
assert {k:v for k,v in oldroot.items() if k != P.name} == {k:v for k,v in newroot.items() if k != P.name}
assert oldroot['docs'] == newroot['docs']
diff = git('diff-tree','-r','--no-commit-id','--no-renames','--name-status','-z',parent,tree)
parts = diff.split(b'\0')
assert parts[-1] == b'' and (len(parts)-1)%2 == 0
changes = [dict(status=parts[i].decode(),path=parts[i+1].decode()) for i in range(0,len(parts)-1,2)]
assert len(changes) == receipt['files'] and all(x['path'].startswith(prefix) for x in changes)
excluded = invocation['excluded_actual_directories']
assert all(not any(x['path'].startswith(prefix+p+'/') for p in excluded) for x in changes)
excluded_paths = [prefix+p for p in excluded]
assert entries(parent,*excluded_paths,recursive=True) == entries(tree,*excluded_paths,recursive=True)
leaves = entries(tree,P.name,recursive=True)
cache_candidates = [
 'verification/hafnian-retract-stage-sol-20261117/baseline-public',
 'verification/hafnian-retract-stage-sol-20261117/candidate-public',
 'verification/hafnian-retract-stage-corrected-sol-20261117/baseline-public',
 'verification/hafnian-retract-stage-corrected-sol-20261117/candidate-public',
 'papers/23204176/reviews/root-continuation-20261117/primary',
 'papers/23204176/reviews/scope-sol-continuation-20261117/primary',
 'papers/23204176/reviews/scope-sol-continuation-20261117/tectonic-cache',
 'papers/23204176/reviews/adversarial-sol-continuation-20261117/primary-pinned',
]
cache_data = []
for p in cache_candidates:
    exists = (P/p).exists()
    committed = [n for n in leaves if n == prefix+p or n.startswith(prefix+p+'/')]
    cache_data.append(dict(path=p,exists=exists,committed_leaves=len(committed)))
    assert not committed,p
actual_caches = [prefix+r['path']+'/' for r in cache_data if r['exists']]
ignored = git('check-ignore','--no-index','-v','-z','--stdin',data=('\0'.join(actual_caches)+'\0').encode(),allow=(0,1))
ig = ignored.split(b'\0')
assert ig[-1] == b'' and (len(ig)-1)%4 == 0
ignore_rows = [dict(source=ig[i].decode(),line=ig[i+1].decode(),pattern=ig[i+2].decode(),path=ig[i+3].decode()) for i in range(0,len(ig)-1,4)]
assert {x['path'] for x in ignore_rows} == set(actual_caches)
live_changes = [x for x in changes if x['status'] != 'D']
queries = [tree+':'+x['path'] for x in live_changes]
raw = git('cat-file','--batch',data=('\n'.join(queries)+'\n').encode())
cursor = 0
blob_rows = []
allowed_metadata_drift = {prefix+'verification/PUSH_RECEIPT.json',prefix+'verification/checkpoint-subtree-dry-run-20261025.json'}
for item in live_changes:
    end = raw.index(b'\n',cursor)
    oid,kind,size = raw[cursor:end].decode().split()
    cursor = end+1
    size = int(size)
    blob = raw[cursor:cursor+size]
    assert raw[cursor+size:cursor+size+1] == b'\n' and len(blob) == size
    cursor += size+1
    assert kind == 'blob' and leaves[item['path']]['OID'] == oid
    local = M/item['path']
    assert local.is_file() and not local.is_symlink()
    current = local.read_bytes()
    same = current == blob
    assert same or item['path'] in allowed_metadata_drift,item['path']
    expected_mode = '100755' if local.stat().st_mode & stat.S_IXUSR else '100644'
    assert leaves[item['path']]['mode'] == expected_mode
    blob_rows.append(dict(**item,OID=oid,bytes=size,SHA256=hashlib.sha256(blob).hexdigest(),current_file_whole_bytes_equal=same,mode=expected_mode,known_helper_receipt_drift=not same))
assert cursor == len(raw)
expected_counts = {'verification/hafnian-retract-stage-corrected-audit-sol-20261117/':12,'verification/hafnian-retract-stage-audit-continuation-sol-20261117/':12,'verification/hafnian-retract-production-prepare-sol-20261117/':11,'verification/acquire-rows192-194-sol-20261117/':11}
packet_counts = {}
for p,count in expected_counts.items():
    names = [n for n in leaves if n.startswith(prefix+p)]
    assert len(names) == count,(p,len(names),count)
    packet_counts[p] = len(names)
important_names = [
 'PROGRESS.json','RESEARCH_LOG.md',
 'verification/root-hafnian-retract-corrected-stage-adoption-20261117.json',
 'verification/root-hafnian-retract-newhelper-reading-20261117.json',
 'verification/hafnian-retract-stage-corrected-audit-sol-20261117/FINAL.json',
 'verification/hafnian-retract-stage-corrected-audit-sol-20261117/OWNED_MANIFEST.json',
 'verification/hafnian-retract-stage-audit-continuation-sol-20261117/FINAL.json',
 'verification/hafnian-retract-stage-audit-continuation-sol-20261117/OWNED_MANIFEST.json',
 'verification/hafnian-retract-stage-audit-continuation-sol-20261117/CRITERIA.json',
 'verification/hafnian-retract-production-prepare-sol-20261117/FINAL.json',
 'verification/hafnian-retract-production-prepare-sol-20261117/OWNED_MANIFEST.json',
 'papers/23204176/reviews/root-continuation-20261117/ROOT_REVIEW.md',
 'verification/root-clearance-23204176-20261117.json',
 'papers/23204212/sources/SOURCE_FINAL.json',
 'papers/23204212/sources/SOURCE_MANIFEST.json',
 'papers/23204810/sources/SOURCE_FINAL.json',
 'papers/23204810/sources/SOURCE_MANIFEST.json',
 'papers/23318851/sources/SOURCE_FINAL.json',
 'papers/23318851/sources/SOURCE_MANIFEST.json',
 'verification/acquire-rows192-194-sol-20261117/FINAL.json',
 'verification/acquire-rows192-194-sol-20261117/OWNED_MANIFEST.json',
]
by_path = {x['path']:x for x in blob_rows}
important = []
for n in important_names:
    path = prefix+n
    if path in by_path:
        important.append(by_path[path])
    else:
        leaf = leaves[path]
        assert leaf['type'] == 'blob'
        blob = git('cat-file','blob',tree+':'+path)
        local = M/path
        assert local.is_file() and not local.is_symlink() and local.read_bytes() == blob
        expected_mode = '100755' if local.stat().st_mode & stat.S_IXUSR else '100644'
        assert leaf['mode'] == expected_mode
        important.append(dict(status='UNCHANGED_FROM_PARENT',path=path,OID=leaf['OID'],bytes=len(blob),SHA256=hashlib.sha256(blob).hexdigest(),current_file_whole_bytes_equal=True,mode=expected_mode,known_helper_receipt_drift=False))
remote = None
commit_data = None
if phase == 'post':
    commit = receipt['commit']
    commit_raw = git('cat-file','commit',commit)
    commit_data = commit_raw.decode()
    header = commit_data.split('\n\n',1)[0].splitlines()
    assert header[0] == 'tree '+tree and [x for x in header if x.startswith('parent ')] == ['parent '+parent]
    assert any(x.startswith('author Alec Kriebel <me@aleckriebel.com> ') for x in header)
    assert any(x.startswith('committer Alec Kriebel <me@aleckriebel.com> ') for x in header)
    remote = git('ls-remote','origin','refs/heads/main').decode().strip()
    assert remote.split()[0] == commit
groups = collections.Counter('/'.join(x['path'][len(prefix):].split('/')[:2]) for x in changes)
result = dict(schema='actual-checkpoint-tree-path-blob-audit-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),phase=phase,parent=parent,tree=tree,commit=receipt.get('commit'),changed_paths=len(changes),changes=changes,status_counts=dict(collections.Counter(x['status'] for x in changes)),all_changes_in_programme=True,sibling_root_entries_preserved=159,old_root_entries=oldroot,new_root_entries=newroot,docs_entry=oldroot['docs'],excluded_subtree_leaves_exact_at_parent=True,excluded_paths=excluded,private_caches=cache_data,actual_ignore_rules=ignore_rows,all_changed_blob_whole_bytes_verified=blob_rows,packet_committed_leaf_counts=packet_counts,important_committed_blob_identities=important,group_counts=dict(groups),ordinary_commit_headers=commit_data,fresh_remote_main=remote,git_calls=calls,scope='Checkpoint integrity only; no scientific claims or website release')
with (OWN/(phase.upper()+'_V2_TREE_AUDIT.json')).open('x') as stream:
    json.dump(result,stream,indent=2)
    stream.write('\n')
with (OWN/(phase.upper()+'_V2_PATHS.txt')).open('x') as stream:
    stream.write(''.join(x['status']+'\t'+x['path']+'\n' for x in changes))
print(json.dumps(dict(phase=phase,parent=parent,tree=tree,commit=receipt.get('commit'),paths=len(changes),status_counts=result['status_counts'],siblings=159,docs=oldroot['docs'],packet_counts=packet_counts,caches=cache_data,groups=dict(groups),important=important)))
