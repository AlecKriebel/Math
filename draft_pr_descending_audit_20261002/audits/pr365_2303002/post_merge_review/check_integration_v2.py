#!/usr/bin/env python3
"""Independent postmerge scope/bytes/API/replay check; writes this review only."""
import base64,gzip,hashlib,json,pathlib,shutil,sys
from capture import ROOT,PRIVATE,run,now,sha
A=ROOT.parent;REPO=pathlib.Path('/Users/alec/Documents/Math')
BASE='728b48109a11e83769b24ec5b30978c1c5ed7ec9';HEAD='47dbe2c144a77f590faf144b950f1e759db92e75';MERGE='904d63bba0651c8f7364144c617e2b66f5d14256';TREE='c95a909fed27e9af7954f82ce216d34f305d91a2'
P='unsolved_math_prioritization/attempts/2303002/';Q='unsolved_math_prioritization/QUEUE.md';API='repos/AlecKriebel/Math/'
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
CURRENT='08adf9cb444d365fd148a2bb3e2951a7f49c6808'
checks=[]
def check(n,c):
    assert c,n;checks.append(n)
def command(n,argv):
    p=run('v2_'+n,argv,REPO);check(n+' exit/stderr',p.returncode==0 and not p.stderr);return p.stdout
def git(n,*args):return command(n,['git',*args])
def api(n,path):return json.loads(command(n,['gh','api',API+path]))
def tree(n,oid,recursive=True):
    data=git(n,'ls-tree','-rz' if recursive else '-z','--full-tree',oid)
    return {p.decode():h.decode().split() for line in data.split(b'\0') if line for h,p in [line.split(b'\t',1)]}
def index(n):
    p=pathlib.Path(git(n,'rev-parse','--git-path','index').decode().strip())
    if not p.is_absolute():p=REPO/p
    return sha(p.read_bytes())

before_branch=git('begin_branch','symbolic-ref','--short','HEAD').decode().strip()
before_main=git('begin_main','rev-parse','HEAD').decode().strip();before_index=index('begin_index_path')
check('begin main exact',before_branch=='main' and before_main==CURRENT)
git('remote_url','remote','get-url','origin')
git('actual_merge_in_current_main','merge-base','--is-ancestor',MERGE,CURRENT)
remote=git('begin_remote_main','ls-remote','--heads','origin','refs/heads/main').decode().split()[0]
check('remote main exact',remote==CURRENT)
git('base_ancestor','merge-base','--is-ancestor',BASE,MERGE);git('head_ancestor','merge-base','--is-ancestor',HEAD,MERGE)
git('actual_commit_raw','cat-file','-p',MERGE)
parents=git('actual_parents','show','-s','--format=%P',MERGE).decode().split();check('actual parents',parents==[BASE,HEAD])
check('actual tree',git('actual_tree_oid','rev-parse',MERGE+'^{tree}').decode().strip()==TREE)
main_ref=api('begin_main_api','git/ref/heads/main');pr=api('begin_pr_api','pulls/365');mc=api('merge_api','git/commits/'+MERGE);hc=api('head_api','git/commits/'+HEAD)
check('merged exact state',pr['merged'] is True and pr['state']=='closed' and pr['merge_commit_sha']==MERGE and pr['merged_at']=='2026-10-03T19:39:40Z' and pr['draft'] is False)
check('merged body and head',pr['head']['sha']==HEAD and pr['body'].encode()==(A/'clean_final_adversary/accepted_body.md').read_bytes())
check('main exact API',main_ref['object']['sha']==CURRENT)
check('merge API parents/tree',[e['sha'] for e in mc['parents']]==[BASE,HEAD] and mc['tree']['sha']==TREE)
check('head API tree',hc['tree']['sha']==TREE)
bt=tree('base_tree',BASE);ht=tree('head_tree',HEAD);mt=tree('merge_tree',MERGE)
current=tree('current_main_tree',CURRENT)
check('current main accepted19 modes/blob IDs',all(current.get(b['path'])==mt.get(b['path']) for b in json.loads((A/'clean_final_adversary/03_reproduction_bindings.json').read_bytes())['original_bindings']))
check('head equals actual merge all repository',mt==ht)
root_tree=tree('merge_root_tree',MERGE,False)
remote_tree=api('merge_root_api','git/trees/'+TREE)
check('complete root tree',not remote_tree['truncated'] and remote_tree['sha']==TREE and {r['path']:[r['mode'],r['type'],r['sha']] for r in remote_tree['tree']}==root_tree)
delta={p for p in set(bt)|set(mt) if bt.get(p)!=mt.get(p)}
original=json.loads((A/'clean_final_adversary/03_reproduction_bindings.json').read_bytes())
check('whole exactly19delta',delta=={b['path'] for b in original['original_bindings']} and len(delta)==19)
check('exact target namespace18',{p for p in mt if p.startswith(P)}==delta-{Q})
files=api('merged_pr_files','pulls/365/files?per_page=100');check('API19scope',len(files)==19 and {f['filename'] for f in files}==delta)
by_api={f['filename']:f for f in files};bindings=[]
for i,p in enumerate(sorted(delta)):
    mode,kind,oid=mt[p];check(p+' actualmode',mode=='100644' and kind=='blob')
    d=git('actual_blob_'+str(i).zfill(2),'cat-file','blob',oid)
    check(p+' Git blob',blob(d)==oid)
    check(p+' worktree bytes',d==(REPO/p).read_bytes())
    if p!=Q:check(p+' immutable math',d==(A/'snapshot'/p).read_bytes() and p not in bt)
    check(p+' APIlistbinding',by_api[p]['sha']==oid and by_api[p]['status']==('modified' if p==Q else 'added'))
    for name,ref in [('head',HEAD),('merge',MERGE)]:
        o=api(name+'_remote_content_'+str(i).zfill(2),'contents/'+p+'?ref='+ref)
        check(p+' '+name+' fullAPI',o['path']==p and o['type']=='file' and o['size']==len(d) and o['sha']==oid and base64.b64decode(o['content'])==d)
    bindings.append(dict(path=p,mode=mode,kind=kind,git_blob=oid,bytes=len(d),sha256=sha(d)))
    if p==Q:queue=d
base_queue=git('base_queue','show',BASE+':'+Q)
old=base_queue.splitlines(keepends=True);new=queue.splitlines(keepends=True)
check('whole queue1966',len(old)==len(new)==1966)
check('only physical405',[i for i,(x,y) in enumerate(zip(old,new)) if x!=y]==[404])
cells=old[404].split(b'|');accepted=new[404].split(b'|')
check('exact ID',cells[2].strip()==b'2303002 / AMR-022-3002')
check('only statuscell8',[i for i,(x,y) in enumerate(zip(cells,accepted)) if x!=y]==[8])
check('queued to solved',cells[8].strip()==b'queued' and accepted[8].strip()==b'already_solved')
check('zero turns',cells[9].strip()==accepted[9].strip()==b'0/5')
expected=old.copy();edited=cells.copy();edited[8]=b' already_solved ';expected[404]=b'|'.join(edited)
check('entire exact onecell bytes',b''.join(expected)==queue)
nested=original['nested_manifest_bindings'];check('29instances',len(nested)==29)
for e in nested:
    d=(REPO/P/e['path']).read_bytes();check(e['manifest']+'/'+e['path'],sha(d)==e['sha256'] and len(d)==e['bytes'])

# Preserve byte-identical replay inputs privately; no raw source redistribution.
copy=PRIVATE/'candidate';shutil.copytree(REPO/P,copy)
src=PRIVATE/'sources';src.mkdir()
for e in json.loads((copy/'SOURCE_MANIFEST.json').read_bytes())['primary_pdfs']:
    d=(A/'clean_final_adversary/private'/e['file']).read_bytes()
    check(e['file']+' exact primary',len(d)==e['bytes'] and sha(d)==e['sha256']);(src/e['file']).write_bytes(d)
for name,argv,expected in [
    ('author_replay',[sys.executable,str(copy/'verify_source_alignment.py')],(copy/'SOURCE_CHECKS.json').read_bytes()),
    ('source_review_replay',[sys.executable,str(copy/'final_review/run_portable.py'),'--sources',str(src)],(copy/'final_review/INDEPENDENT_CHECKS.json').read_bytes()),
    ('math_only_replay',[sys.executable,str(copy/'final_review/run_portable.py'),'--math-only'],(copy/'final_review/INDEPENDENT_CHECKS.json').read_bytes().replace(b'1667',b'1665'))]:
    check(name+' whole receipt',command(name,argv)==expected)
check('private replay inputs unchanged',all(p.read_bytes()==(REPO/P/p.relative_to(copy)).read_bytes() for p in copy.rglob('*') if p.is_file()))

end_branch=git('end_branch','symbolic-ref','--short','HEAD').decode().strip();end_main=git('end_main','rev-parse','HEAD').decode().strip();end_index=index('end_index_path')
end_remote=git('end_remote_main','ls-remote','--heads','origin','refs/heads/main').decode().split()[0]
end_pr=api('end_pr_api','pulls/365');end_ref=api('end_main_api','git/ref/heads/main')
check('end local branch/main/index',end_branch==before_branch=='main' and end_main==before_main==CURRENT and end_index==before_index)
check('end remote/API main',end_remote==CURRENT and end_ref['object']['sha']==CURRENT)
check('end merged exact',end_pr['merged'] is True and end_pr['merge_commit_sha']==MERGE and end_pr['head']['sha']==HEAD and end_pr['body']==pr['body'] and end_pr['draft'] is False)
out=dict(completed_utc=now(),actual_merge=MERGE,base=BASE,reviewed_head=HEAD,tree=TREE,parents=parents,merged_at=pr['merged_at'],branch='main',remote_and_local_main=CURRENT,
    bindings=bindings,scope_files=19,unchanged_math_files=18,nested_bindings=29,queue_lines=1966,queue_line=405,queue_changed_cells=[8],turns='0/5',
    queue_base_sha256=sha(base_queue),queue_merge_sha256=sha(queue),index_sha256_unchanged=before_index,receipts=[3675,1667,1665],checks=checks,
    proof_reaudited=False,mathematical_credited_resolution_percent=100,novel_theorems=0,postmerge_workflow_percent=65)
(ROOT/'INTEGRATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['bindings','checks']},indent=2))
