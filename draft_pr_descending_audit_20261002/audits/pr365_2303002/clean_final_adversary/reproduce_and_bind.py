#!/usr/bin/env python3
"""Read-only original Git/API binding plus exact private-copy replay."""
import gzip, hashlib, json, pathlib, shutil
from capture import ROOT, PRIVATE, now, run

REPO=pathlib.Path('/Users/alec/Documents/Math')
SNAP=ROOT.parent/'snapshot'
TARGET=pathlib.Path('unsolved_math_prioritization/attempts/2303002')
HEAD='4245f1af53840a07f43c05c928c4783bc6c3a467'
BASE='efd29c05204703acca9a0860812f54b94fae54b1'
CHECKPOINT='a3ac55761d2301fbfe30e07a266da4a039cbfaba'
PY='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'

def command(name,args):
    p=run(name,args,REPO)
    if p.returncode: raise RuntimeError((name,p.returncode,p.stderr.decode(errors='replace')))
    return p.stdout

before={}
for name,args in [('branch',['git','symbolic-ref','--short','HEAD']),('repo_head',['git','rev-parse','HEAD']),('remote',['git','remote','-v']),('original_head',['git','cat-file','-p',HEAD]),('original_base',['git','cat-file','-p',BASE]),('source_checkpoint',['git','cat-file','-p',CHECKPOINT]),('original_changes',['git','diff','--name-status',BASE,HEAD]),('original_raw',['git','diff','--raw','--full-index','--abbrev=40',BASE,HEAD]),('source_changes',['git','diff','--name-status',BASE,CHECKPOINT]),('original_tree',['git','ls-tree','-r',HEAD,'--',str(TARGET),'unsolved_math_prioritization/QUEUE.md'])]:
    before[name]=command(name,args).decode()
assert before['branch'].strip()=='main'
assert [s.split()[1] for s in before['original_head'].splitlines() if s.startswith('parent ')]==[BASE,CHECKPOINT]
assert [s.split()[1] for s in before['source_checkpoint'].splitlines() if s.startswith('parent ')]==[BASE]
changes=[line.split('\t') for line in before['original_changes'].splitlines()]
assert len(changes)==19
assert len([x for x in changes if x[1].startswith(str(TARGET)+'/')])==18
assert len([x for x in changes if x[1]=='unsolved_math_prioritization/QUEUE.md'])==1
bindings=[]
for i,line in enumerate(before['original_tree'].splitlines()):
    left,path=line.split('\t');mode,kind,oid=left.split()
    blob=command(f'original_blob_{i:02d}',['git','cat-file','blob',oid])
    actual=(SNAP/path).read_bytes()
    assert blob==actual,(path,'snapshot mismatch')
    bindings.append(dict(path=path,mode=mode,kind=kind,git_blob=oid,bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest()))
assert len(bindings)==19
checkpoint_tree=command('checkpoint_tree',['git','ls-tree','-r',CHECKPOINT,'--',str(TARGET)]).decode()
assert len(checkpoint_tree.splitlines())==10
for i,line in enumerate(checkpoint_tree.splitlines()):
    left,path=line.split('\t'); mode,kind,oid=left.split()
    b=command(f'checkpoint_blob_{i:02d}',['git','cat-file','blob',oid])
    assert b==(SNAP/path).read_bytes()

remote=command('origin_url',['git','remote','get-url','origin']).decode().strip()
if remote.startswith('git@github.com:'): slug=remote.split(':',1)[1].removesuffix('.git')
elif remote.startswith('https://github.com/'): slug=remote.removeprefix('https://github.com/').removesuffix('.git')
else: raise ValueError(remote)
api=json.loads(command('original_pr_api',['gh','api','repos/'+slug+'/pulls/365']))
api_files=json.loads(command('original_pr_files_api',['gh','api','--paginate','repos/'+slug+'/pulls/365/files?per_page=100']))
assert api['head']['sha']==HEAD and api['base']['sha']==BASE
assert len(api_files)==19
by_path={x['filename']:x for x in api_files}
assert set(by_path)=={x['path'] for x in bindings}
for b in bindings: assert by_path[b['path']]['sha']==b['git_blob']

target=SNAP/TARGET
nested=[]
for mf in ['FINAL_FROZEN_MANIFEST.json','final_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
    data=json.loads((target/mf).read_text())
    fs=data.get('files') if 'files' in data else [dict(path='final_review/'+k,sha256=v) for k,v in data.items()]
    for entry in fs:
        p=entry['path']; d=(target/p).read_bytes()
        assert hashlib.sha256(d).hexdigest()==entry['sha256']
        if 'bytes' in entry: assert len(d)==entry['bytes']
        nested.append(dict(manifest=mf,path=p,sha256=entry['sha256'],bytes=len(d)))
assert len(nested)==29
pub=json.loads((target/'PUBLICATION_MANIFEST.json').read_text())
assert pub['author_manifest_sha256']==hashlib.sha256((target/'FINAL_FROZEN_MANIFEST.json').read_bytes()).hexdigest()
assert pub['review_manifest_sha256']==hashlib.sha256((target/'final_review/REVIEW_MANIFEST.json').read_bytes()).hexdigest()

copy=PRIVATE/'execution_source'
if copy.exists(): raise RuntimeError('private execution copy already exists; do not overwrite')
shutil.copytree(target,copy)
for p in target.rglob('*'):
    if p.is_file(): assert p.read_bytes()==(copy/p.relative_to(target)).read_bytes()
author=command('author_replay',[PY,str(copy/'verify_source_alignment.py')])
assert author==(target/'SOURCE_CHECKS.json').read_bytes()
sources=PRIVATE/'portable_sources';sources.mkdir()
for original,logical in [('hayman_lingham_2018.pdf','hayman_lingham_2018.pdf'),('carleson_1976.pdf','carleson_1976.pdf')]:
    (sources/logical).symlink_to(PRIVATE/original)
historical=command('historical_review_replay',[PY,str(copy/'final_review/run_portable.py'),'--sources',str(sources)])
assert historical==(target/'final_review/INDEPENDENT_CHECKS.json').read_bytes()
math_only=command('math_only_review_replay',[PY,str(copy/'final_review/run_portable.py'),'--math-only'])
math=json.loads(math_only)
assert math['independent_assertions']==1665 and math['status']=='PASS'
expected=json.loads(historical);expected['independent_assertions']=1665
assert math_only==(json.dumps(expected,indent=2)+'\n').encode()
assert all(p.read_bytes()==(copy/p.relative_to(target)).read_bytes() for p in target.rglob('*') if p.is_file())
after_branch=command('end_branch',['git','symbolic-ref','--short','HEAD']).decode().strip()
after_head=command('end_repo_head',['git','rev-parse','HEAD']).decode().strip()
assert after_branch=='main' and after_head==before['repo_head'].strip()
out=dict(completed_utc=now(),frozen_head=HEAD,frozen_base=BASE,source_checkpoint=CHECKPOINT,source_checkpoint_files=10,
         branch=after_branch,repo_head=after_head,original_bindings=bindings,nested_manifest_bindings=nested,
         author_assertions=json.loads(author)['assertions'],historical_independent_assertions=json.loads(historical)['independent_assertions'],math_only_assertions=math['independent_assertions'],
         exact_full_receipts=True,source_copy_byte_identical_before_and_after=True,api_pr_number=api['number'],api_files_count=len(api_files),
         no_global_historical_negative_certification=True)
(ROOT/'03_reproduction_bindings.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
