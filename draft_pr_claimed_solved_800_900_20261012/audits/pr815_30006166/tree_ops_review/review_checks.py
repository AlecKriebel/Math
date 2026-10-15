#!/usr/bin/env python3
"""Isolated adversarial fixtures plus read-only examination of the sealed preview."""
import datetime
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
sys.dont_write_bytecode = True
OUT = pathlib.Path(__file__).resolve().parent
ROOT = OUT.parents[2]
REPO = ROOT.parent
spec = importlib.util.spec_from_file_location('scoped_git_tree_under_review', ROOT / 'scoped_git_tree.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
PRIVATE = OUT / 'private_sources'
PRIVATE.mkdir(exist_ok=True)
FIXTURE = PRIVATE / 'fixture.git'
if not FIXTURE.exists():
    subprocess.run(['git', 'init', '--bare', '--quiet', str(FIXTURE)], check=True)
def g(*args, raw=None, repo=FIXTURE):
    return subprocess.check_output(['git', *args], cwd=repo, input=raw)
def blob(raw):
    return g('hash-object', '-w', '--stdin', raw=raw).decode().strip()
def tree(entries):
    return g('mktree', '-z', raw=b''.join(m+b' '+k+b' '+o.encode()+b'\t'+n+b'\0' for n,m,k,o in entries)).decode().strip()
a=blob(b'A\n'); b=blob(b'B\n'); link=blob(b'foreign/exec\n')
empty=tree([])
commit=g('-c','user.name=Tree audit fixture','-c','user.email=fixture@example.invalid','commit-tree',empty,raw=b'fixture-only\n').decode().strip()
foreign=tree([(b'exec',b'100755',b'blob',a),(b'link',b'120000',b'blob',link),(b'module',b'160000',b'commit',commit),(b'bad-utf8-\xff',b'100644',b'blob',a),(b'name\nnewline\twith tab',b'100644',b'blob',b)])
owned=tree([(b'replace',b'100644',b'blob',a),(b'leave-executable',b'100755',b'blob',b),(b'leave-link',b'120000',b'blob',link)])
base=tree([(b'foreign',b'040000',b'tree',foreign),(b'owned',b'040000',b'tree',owned),(b'plain',b'100644',b'blob',a),(b'root-link',b'120000',b'blob',link)])
def inventory(oid):
    result={}
    for row in g('ls-tree','-r','-z',oid).split(b'\0'):
        if row:
            meta,name=row.split(b'\t',1)
            result[name]=meta
    return result
checks=[]
def check(label,predicate):
    assert predicate,label
    checks.append(label)
check('no-op reconstructs exact base root tree',mod.patch_tree(FIXTURE,base,{})==base)
updates={'owned/replace':b,'owned/new/space and ü.txt':a,'newdir/child':b}
patched=mod.patch_tree(FIXTURE,base,updates)
old,new=inventory(base),inventory(patched)
for name,meta in old.items():
    if name!=b'owned/replace':
        check('unchanged exact mode/type/OID: '+repr(name),new[name]==meta)
check('updated leaf regular mode and exact blob',new[b'owned/replace']==b'100644 blob '+b.encode())
check('new nested unicode leaf',new['owned/new/space and ü.txt'.encode()]==b'100644 blob '+a.encode())
check('only explicit leaf additions or replacement',set(new)==set(old)|{n.encode() for n in updates})
rejections=[]
invalid_paths=['','.','..','/absolute','owned//x','owned/./x','owned/../x','owned/x/','owned\\x','owned/x\0suffix']
for path in invalid_paths:
    try:
        mod.patch_tree(FIXTURE,base,{path:a})
    except (RuntimeError,ValueError,TypeError,subprocess.CalledProcessError):
        rejections.append(repr(path))
    else:
        raise AssertionError('Unsafe path accepted: '+repr(path))
for label,edits in [
    ('file then child',{'new':a,'new/child':b}),
    ('child then file',{'new/child':a,'new':b}),
    ('replace directory',{'owned':a}),
    ('traverse regular leaf',{'plain/child':a}),
    ('traverse symlink',{'root-link/child':a}),
    ('wrong object kind',{'owned/new':base}),
    ('bad oid uppercase',{'owned/new':'A'*40}),
    ('bad oid length',{'owned/new':a[:-1]}),
]:
    try:
        mod.patch_tree(FIXTURE,base,edits)
    except (RuntimeError,ValueError,TypeError,subprocess.CalledProcessError):
        rejections.append(label)
    else:
        raise AssertionError('Collision or bad object accepted: '+label)
# Scope, exact bytes, modes, full non-target queue, and ancestry: reads only.
audit=ROOT/'audits/pr815_30006166'
mapping=json.loads((audit/'FINAL_PR_MAPPING.json').read_text())
receipt=json.loads((audit/'FINAL_PR_REVISION_RECEIPT.json').read_text())
head,main=receipt['prepared_commit'],receipt['main_base']
prefix='unsolved_math_prioritization/attempts/30006166'
raw_file_checks=[]
for f in mapping['files']:
    raw=g('show',head+':'+f['repo_path'],repo=REPO)
    digest=hashlib.sha256(raw).hexdigest()
    check('reviewed Git bytes '+f['repo_path'],digest==f['sha256'])
    raw_file_checks.append({'repo_path':f['repo_path'],'sha256':digest})
expected_target='10b95122c72fb715d21fb5567d95959c39e95ec0'
target_tree=g('rev-parse',head+':'+prefix,repo=REPO).decode().strip()
check('sealed target tree exact',target_tree==expected_target)
q='unsolved_math_prioritization/QUEUE.md'
oldq=g('show',main+':'+q,repo=REPO);newq=g('show',head+':'+q,repo=REPO)
before,after=receipt['queue_before'].encode(),receipt['queue_after'].encode()
check('unique base target queue row',oldq.count(before)==1)
check('unique revised target queue row',newq.count(after)==1)
check('non-target queue byte equality',oldq.replace(before,b'')==newq.replace(after,b''))
changes=g('diff-tree','-r','--no-commit-id','--name-only',main,head,repo=REPO).decode().splitlines()
check('exact receipt diff list',changes==receipt['changed_paths_vs_main'])
check('diff restricted to queue and target',all(p==q or p.startswith(prefix+'/') for p in changes))
check('prepared parents retain old head and fresh main',g('show','-s','--format=%P',head,repo=REPO).decode().strip().split()==[receipt['old_head'],main])
check('preview did not claim a push',receipt['pushed'] is False)
# Full recursive inventories prove foreign paths retain exact modes/types/OIDs.
def repo_inventory(rev):
    out={}
    for row in g('ls-tree','-r','-z',rev,repo=REPO).split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);out[path]=meta
    return out
base_inv=repo_inventory(main);head_inv=repo_inventory(head)
foreign_keys={p for p in set(base_inv)|set(head_inv) if p!=q.encode() and not p.startswith((prefix+'/').encode())}
check('all foreign recursive entries exactly preserved',all(base_inv.get(p)==head_inv.get(p) for p in foreign_keys))
result={
 'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'checked_files':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['scoped_git_tree.py','prepare_pr_revision.py','record_publication_main.py','checkpoint_main.py']},
 'prepared_commit':head,'main_base':main,'mapped_files':len(raw_file_checks),'mapped_file_hashes':raw_file_checks,
 'target_tree':target_tree,'expected_target_tree':expected_target,'non_target_queue_bytes_equal':True,
 'all_foreign_entries_equal':True,'foreign_entry_count':len(foreign_keys),
 'positive_check_count':len(checks),'fixture_rejections':rejections,
 'preview_changed_paths_count':len(changes),'private_fixture':str(FIXTURE),
 'remote_writes':False,'shared_ref_index_writes':False,'completion_percent':100,
}
(OUT/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['mapped_file_hashes']},indent=2))
