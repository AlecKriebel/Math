#!/usr/bin/env python3
"""Fresh read-only prepared PR/main/queue/body/test-merge gate."""
import base64,hashlib,json,pathlib
from capture import ROOT,PRIVATE,run,now
REPO=pathlib.Path('/Users/alec/Documents/Math');A=ROOT.parent
HEAD='47dbe2c144a77f590faf144b950f1e759db92e75'
BASE='728b48109a11e83769b24ec5b30978c1c5ed7ec9'
ORIGINAL='4245f1af53840a07f43c05c928c4783bc6c3a467'
TREE='c95a909fed27e9af7954f82ce216d34f305d91a2'
P='unsolved_math_prioritization/attempts/2303002/'
Q='unsolved_math_prioritization/QUEUE.md'
API='repos/AlecKriebel/Math/'
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
expected_body=(A/'accepted_pr_body.txt').read_bytes();(ROOT/'accepted_body.md').write_bytes(expected_body)

def call(name,args):
    p=run('prepared_'+name,args,REPO)
    assert p.returncode==0 and not p.stderr,(name,p.returncode,p.stderr)
    return p.stdout
def git(name,*args):return call(name,['git',*args])
def api(name,path):return json.loads(call(name,['gh','api',API+path]))
def tree(name,ref):
    raw=git(name,'ls-tree','-rz','--full-tree',ref);rows={}
    for line in raw.split(b'\0'):
        if line:
            left,p=line.split(b'\t',1);mode,kind,oid=left.decode().split();rows[p.decode()]=[mode,kind,oid]
    return rows
def api_tree(name,oid):
    obj=api(name,'git/trees/'+oid+'?recursive=1');assert not obj['truncated']
    return {r['path']:[r['mode'],r['type'],r['sha']] for r in obj['tree'] if r['type']!='tree'}
def index_digest(name):
    p=pathlib.Path(git(name,'rev-parse','--git-path','index').decode().strip())
    if not p.is_absolute():p=REPO/p
    return sha(p.read_bytes())

beg_branch=git('begin_branch','symbolic-ref','--short','HEAD').decode().strip()
beg_main=git('begin_main','rev-parse','HEAD').decode().strip();beg_index=index_digest('begin_index_path')
assert beg_branch=='main' and beg_main==BASE
pr=api('begin_pr','pulls/365')
main=api('begin_main_ref','git/ref/heads/main')
head=api('begin_head_commit','git/commits/'+HEAD)
base=api('begin_base_commit','git/commits/'+BASE)
merge=api('begin_testmerge','commits/refs/pull/365/merge')
assert pr['head']['sha']==HEAD and pr['base']['sha']==BASE and pr['draft'] is True and pr['state']=='open'
assert pr['body'].encode()==expected_body
assert main['object']['sha']==BASE and head['sha']==HEAD and base['sha']==BASE
assert [x['sha'] for x in head['parents']]==[ORIGINAL,BASE]
assert head['tree']['sha']==TREE
merge_sha=merge['sha'];merge_tree=merge['commit']['tree']['sha']
assert [x['sha'] for x in merge['parents']]==[BASE,HEAD]
base_tree=tree('base_tree',BASE);head_tree=tree('head_tree',HEAD)
assert api_tree('base_api_tree',base['tree']['sha'])==base_tree
assert api_tree('head_api_tree',TREE)==head_tree
assert api_tree('testmerge_api_tree',merge_tree)==head_tree
assert merge_tree==TREE
assert git('head_tree_oid','rev-parse',HEAD+'^{tree}').decode().strip()==TREE
assert git('head_parents','show','-s','--format=%P',HEAD).decode().split()==[ORIGINAL,BASE]
changes={p for p in set(base_tree)|set(head_tree) if base_tree.get(p)!=head_tree.get(p)}
orig=json.loads((ROOT/'03_reproduction_bindings.json').read_bytes())
assert changes=={b['path'] for b in orig['original_bindings']} and len(changes)==19
assert {p for p in head_tree if p.startswith(P)}==changes-{Q}
api_files=api('files','pulls/365/files?per_page=100')
assert len(api_files)==19 and {f['filename'] for f in api_files}==changes
byfile={f['filename']:f for f in api_files}
bindings=[]
for i,p in enumerate(sorted(changes)):
    mode,kind,oid=head_tree[p];assert mode=='100644' and kind=='blob'
    d=git('blob_'+str(i).zfill(2),'cat-file','blob',oid)
    assert blob(d)==oid
    if p!=Q:assert d==(A/'snapshot'/p).read_bytes() and p not in base_tree
    assert byfile[p]['sha']==oid and byfile[p]['status']==('modified' if p==Q else 'added')
    for ref_name,ref in [('head',HEAD),('testmerge',merge_sha)]:
        remote=api(ref_name+'_content_'+str(i).zfill(2),'contents/'+p+'?ref='+ref)
        content=base64.b64decode(remote['content'])
        assert remote['path']==p and remote['type']=='file' and remote['size']==len(d) and remote['sha']==oid and content==d
    bindings.append(dict(path=p,mode=mode,kind=kind,git_blob=oid,bytes=len(d),sha256=sha(d)))
    if p==Q:queue_head=d
queue_base=git('base_queue','show',BASE+':'+Q)
remote_base=api('base_queue_api','contents/'+Q+'?ref='+BASE)
assert base64.b64decode(remote_base['content'])==queue_base
before=queue_base.splitlines(keepends=True);after=queue_head.splitlines(keepends=True)
assert len(before)==len(after)==1966
diff=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b]
assert diff==[404]
bc=before[404].split(b'|');ac=after[404].split(b'|')
assert len(bc)==len(ac) and b'2303002 / AMR-022-3002' in bc[2]
assert [i for i,(x,y) in enumerate(zip(bc,ac)) if x!=y]==[8]
assert bc[8].strip()==b'queued' and ac[8].strip()==b'already_solved'
assert bc[9].strip()==ac[9].strip()==b'0/5'
expected=list(before);cells=bc.copy();cells[8]=b' already_solved ';expected[404]=b'|'.join(cells)
assert b''.join(expected)==queue_head
nested=orig['nested_manifest_bindings'];assert len(nested)==29
for r in nested:
    d=(A/'snapshot'/P/r['path']).read_bytes();assert sha(d)==r['sha256'] and len(d)==r['bytes']
    assert next(b for b in bindings if b['path']==P+r['path'])['sha256']==r['sha256']

end_branch=git('end_branch','symbolic-ref','--short','HEAD').decode().strip()
end_main=git('end_main','rev-parse','HEAD').decode().strip();end_index=index_digest('end_index_path')
end_pr=api('end_pr','pulls/365');end_ref=api('end_main_ref','git/ref/heads/main')
end_head=api('end_head_commit','git/commits/'+HEAD);end_base=api('end_base_commit','git/commits/'+BASE)
end_merge=api('end_testmerge','commits/refs/pull/365/merge')
assert end_branch==beg_branch=='main' and end_main==beg_main==BASE and end_index==beg_index
assert end_ref['object']['sha']==BASE and end_head==head and end_base==base
assert end_pr['head']['sha']==HEAD and end_pr['base']['sha']==BASE and end_pr['draft'] is True and end_pr['state']=='open'
assert end_pr['body'].encode()==expected_body and end_pr['changed_files']==19
assert end_merge['sha']==merge_sha and end_merge['commit']['tree']['sha']==TREE
assert [x['sha'] for x in end_merge['parents']]==[BASE,HEAD]
report=dict(completed_utc=now(),complete=True,prepared_head=HEAD,prepared_base=BASE,prepared_head_parents=[ORIGINAL,BASE],prepared_tree=TREE,
    testmerge=merge_sha,testmerge_tree=TREE,testmerge_parents=[BASE,HEAD],scope_files=19,unchanged_mathematical_files=18,
    bindings=bindings,queue_lines=1966,queue_physical_line=405,queue_changed_pipe_cells=[8],queue_turns_preserved='0/5',
    queue_base_sha256=sha(queue_base),queue_head_sha256=sha(queue_head),accepted_body_sha256=sha(expected_body),accepted_body_bytes=len(expected_body),
    branch_at_both_ends='main',repository_head_at_both_ends=BASE,private_git_index_unchanged=True,index_sha256_at_both_ends=beg_index,
    whole_api_git_body_main_merge_gate=True,all29_nested_bindings=True,kept_draft=True,raw_api_private=True,
    mathematical_verdict='credited already_solved0/5; entire harmonic and continuous case only',novel_theorems=0)
(ROOT/'05_prepared_gate.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
