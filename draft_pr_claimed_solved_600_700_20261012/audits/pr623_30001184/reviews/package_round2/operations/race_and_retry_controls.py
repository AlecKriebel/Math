#!/usr/bin/env python3
"""Additional integration controls with all service/Git calls mocked."""
import contextlib,datetime,importlib.util,io,json,pathlib,sys,tempfile
from unittest.mock import patch
sys.dont_write_bytecode=True
OUT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('local_independent_runner',OUT/'run_review.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
p=r.p;results=[]

def run(mode,root,prior=None,prior_files=None):
    base,tree='c'*40,'d'*40
    head=p.ORIGINAL if prior is None else prior['integration_commit']
    commit='e'*40 if prior is None else 'f'*40
    newqueue,_=p.patch_queue(r.QUEUE,r.DOI)
    current={};calls=[];real_build=p.build_current_files
    def build(*args):
        answer=real_build(*args);current.update(answer);return answer
    def git(*args,env=None,input=None):
        calls.append(args)
        if args[0]=='show':
            if args[:3]==('show','-s','--format=%P'):return (prior['main_base']+' '+prior['existing_pr_head']+'\n').encode()
            if args[1]==head+':'+p.QPATH:return newqueue
            if args[1]==base+':'+p.QPATH:
                return r.QUEUE.replace(b' 0/5 ',b' 1/5 ') if mode=='main_turn_drift' else r.QUEUE
            if prior and args[1].startswith(head+':'+p.PREFIX):return prior_files[args[1].split(':'+p.PREFIX,1)[1]]
            return r.ORIGINAL[args[1].split(':'+p.PREFIX,1)[1]]
        if args[0]=='ls-tree':
            return ('\n'.join(sorted(p.PREFIX+n for n in prior_files))+'\n').encode() if prior and args[3]==head else b''
        if args[0] in ['fetch','read-tree','update-index','push']:return b''
        if args[0]=='rev-parse':return (base+'\n').encode()
        if args[0]=='hash-object':return ('f'*40+'\n').encode()
        if args[0]=='write-tree':return (tree+'\n').encode()
        if args[0]=='diff':
            if args[1]=='--numstat':return b'1\t1\tqueue\n'
            if prior and args[-1]==head:return ('\n'.join(prior['changed_paths'])+'\n').encode()
            return ('\n'.join(sorted({p.QPATH}|{p.PREFIX+n for n in current}))+'\n').encode()
        if args[0]=='commit-tree':return (commit+'\n').encode()
        if args[0]=='ls-remote':return (base+'\trefs/heads/main\n').encode()
        raise AssertionError('unexpected mocked Git call '+repr(args))
    if prior:(root/'pushed.json').write_bytes(p.json_bytes(prior))
    src=root/'source.md';src.write_bytes(r.SOURCE)
    states=[{'head':'main','index_sha256':'stable'}]*3
    if mode=='local_drift_after_tree':states[1]={'head':'main','index_sha256':'changed'}
    if mode=='local_drift_before_push':states[2]={'head':'main','index_sha256':'changed'}
    metas=[r.META|{'headRefOid':head},r.META|{'headRefOid':head},r.META|{'headRefOid':commit}]
    with patch.object(p,'A',root),patch.object(p,'PUSHED_RECEIPT',root/'pushed.json'), \
         patch.object(p,'local_state',side_effect=states),patch.object(p,'pr_metadata',side_effect=metas), \
         patch.object(p,'git',side_effect=git),patch.object(p,'load_snapshot',return_value=(r.ORIGINAL,r.FROZEN)), \
         patch.object(p,'publication_inputs',return_value=(r.PUB,{})),patch.object(p,'build_current_files',side_effect=build), \
         patch.object(sys,'argv',['helper','--doi',r.DOI,'--push','--source-audit',str(src)]),contextlib.redirect_stdout(io.StringIO()):
        if mode=='success':p.main();outcome='PUSHED_MOCK'
        else:outcome=r.reject(p.main)
    pushes=[x for x in calls if x[0]=='push'];commits=[x for x in calls if x[0]=='commit-tree']
    p.require(len(pushes)==(1 if mode=='success' else 0),'push escaped expected control')
    if pushes:p.require(pushes[0]==('push','origin',commit+':refs/heads/'+p.BRANCH),'force or wrong target push')
    if commits:p.require(commits[0]==('commit-tree',tree,'-p',base,'-p',head),'wrong integration parents')
    result={'mode':mode,'outcome':outcome,'push_calls':len(pushes),'second_parent':head,
            'prepared_receipt_exists':(root/'INTEGRATION_PREPARED_RECEIPT.json').exists(),
            'pushed_receipt_exists':(root/'pushed.json').exists()}
    receipt=p.parse_json((root/'pushed.json').read_bytes()) if mode=='success' else None
    return result,receipt,current

for mode in ['main_turn_drift','local_drift_after_tree','local_drift_before_push']:
    with tempfile.TemporaryDirectory(dir=OUT) as td:
        result,_,_=run(mode,pathlib.Path(td));results.append(result)
with tempfile.TemporaryDirectory(dir=OUT) as td:
    root=pathlib.Path(td)
    first,receipt,current=run('success',root);results.append(first)
    second,retry,_=run('success',root,receipt,current);results.append(second)
    p.require(retry['existing_pr_head']==receipt['integration_commit'],'retry did not retain own successful parent')
obj={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','results':results,
     'remote_mutations':0,'git_mutations':0,'writes_outside_review_folder':0}
(OUT/'RACE_AND_RETRY_RESULTS.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(obj,indent=2))
