#!/usr/bin/env python3
"""Actual revision functions with synthetic GitHub/tree methods; zero providers."""
from contextlib import ExitStack
import copy
import hashlib
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
sys.path.insert(0,str(AUDIT))
import ops_binding as B
import repository_integration as I
CASES=[];ATTEMPTS=[]


def ck(value,message):
    if not value:raise RuntimeError('REVISION CONTROL FAILED: '+message)
def forbidden(*args,**kwargs):
    ATTEMPTS.append(True);raise RuntimeError('ACTUAL PROVIDER FORBIDDEN')
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')
def leaf(identity):return {'mode':identity[0],'type':identity[1],'sha':identity[2]}
def tree(identity='directory'):return {'mode':'040000','type':'tree','sha':identity}
def dirs(files):
    result={}
    for name in files:
        parts=name.split('/')
        for end in range(1,len(parts)):result['/'.join(parts[:end])]=tree()
    return result


class Fixture:
    def __init__(self,root,mode='normal'):
        self.root=root;root.mkdir();self.mode=mode;self.calls=[];self.gates=0;self.ref=I.REVISION_BASE
        self.child='c'*40;self.posts=[];self.patches=[];self.gate_heads=[];self.lag=0;self.branch='codex/synthetic-pr280'
        snapshot=json.loads((AUDIT/'SOURCE_SNAPSHOT.json').read_text());write(root/'SOURCE_SNAPSHOT.json',snapshot)
        for e in snapshot['files']:
            d=root/e['snapshot'];d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(AUDIT/e['snapshot'],d)
        history=root/I.OLD_RELEASE_HISTORY;history.mkdir(parents=True)
        for p in (AUDIT/I.OLD_RELEASE_HISTORY).iterdir():
            if p.is_file():shutil.copyfile(p,history/p.name)
        self.originals=I.originals();self.prior={}
        for e in json.loads((history/'RELEASE_FILES.json').read_text())['files']:
            self.prior['preprint/'+e['path']]=(history/e['path']).read_bytes()
        self.publication=root/'current_publication';self.publication.mkdir()
        for name in B.NAMES|{'RELEASE_FILES.json'}:shutil.copyfile(B.PUBLICATION/name,self.publication/name)
        self.current=I.selection()
        original={n:leaf(v) for n,v in self.originals.items()};original.update(dirs(original))
        old={**original,**{n:leaf(('100644','blob',I.blob_sha(b))) for n,b in self.prior.items()}};old.update(dirs(old))
        child={**original,**{n:leaf(('100644','blob',I.blob_sha(b))) for n,b in self.current.items()}};child.update(dirs(child))
        self.trees={B.ORIGINAL:original,I.REVISION_BASE:old,self.child:child}
        self.parents={B.ORIGINAL:[B.ORIGINAL_PARENT],I.REVISION_BASE:[B.ORIGINAL],self.child:[I.REVISION_BASE]}
        self.queues={B.ORIGINAL_PARENT:b'prefix\n'+I.BASELINE_ROW+b'suffix\n',
                     B.ORIGINAL:b'prefix\n'+I.DESIRED_ROW+b'suffix\n',
                     I.REVISION_BASE:b'prefix\n'+I.DESIRED_ROW+b'suffix\n',
                     self.child:b'prefix\n'+I.DESIRED_ROW+b'suffix\n'}
        self.outer={}
        for c in [B.ORIGINAL,I.REVISION_BASE,self.child]:
            self.outer[c,'']={'README.md':leaf(('100644','blob','same-root')),'unsolved_math_prioritization':tree(c)}
            self.outer[c,'unsolved_math_prioritization']={'attempts':tree(c),'QUEUE.md':leaf(('100644','blob','same-queue')),'keep':tree('nested-unchanged')}
            self.outer[c,'unsolved_math_prioritization/attempts']={'30000156':tree(c),'other-problem':tree('unchanged-empty-and-nested')}
        if mode=='wrong_parent':self.parents[I.REVISION_BASE]=['e'*40]
        if mode=='old_file_tamper':self.trees[I.REVISION_BASE][next(iter(self.prior))]['sha']='tampered'
        if mode=='original_file_tamper':self.trees[I.REVISION_BASE][next(iter(self.originals))]['sha']='tampered'
        if mode=='old_extra_file':self.trees[I.REVISION_BASE]['unselected.txt']=leaf(('100644','blob','extra'))
        if mode=='old_extra_empty_directory':self.trees[I.REVISION_BASE]['extraempty']=tree()
        if mode=='old_missing_directory':self.trees[I.REVISION_BASE].pop('checks')
        if mode=='old_queue_other_bytes':self.queues[I.REVISION_BASE]+=b'concurrent-other-row\n'
        if mode=='old_own_queue':self.queues[I.REVISION_BASE]=b'prefix\n'+I.BASELINE_ROW+b'suffix\n'
        if mode=='old_root_sibling':self.outer[I.REVISION_BASE,'']['README.md']['sha']='changed'
        if mode=='old_attempt_sibling':self.outer[I.REVISION_BASE,'unsolved_math_prioritization/attempts']['other-problem']['sha']='changed'
        if mode=='child_file_tamper':self.trees[self.child][next(iter(self.current))]['sha']='changed'
        if mode=='child_original_tamper':self.trees[self.child][next(iter(self.originals))]['sha']='changed'
        if mode=='child_extra_empty_directory':self.trees[self.child]['extraempty']=tree()
        if mode=='child_missing_directory':self.trees[self.child].pop('preprint')
        if mode=='child_queue':self.queues[self.child]+=b'changed-unrelated-row\n'
        if mode=='child_root_sibling':self.outer[self.child,'']['README.md']['sha']='changed'
        if mode=='child_attempt_sibling':self.outer[self.child,'unsolved_math_prioritization/attempts']['other-problem']['sha']='changed'
        if mode=='main_as_head_ref':self.branch='main'
        if mode=='wrong_pr_head':self.ref='e'*40
        if mode=='new_parent_get':self.parents[self.child]=['e'*40]
        if mode=='local_snapshot_tamper':(root/snapshot['files'][0]['snapshot']).write_text('changed')
        if mode=='history_manifest_tamper':(history/'RELEASE_FILES.json').write_text('{}')
        if mode=='history_payload_tamper':(history/next(iter(B.NAMES))).write_text('changed')

    def api(self,endpoint,method='GET',body=None):
        self.calls.append((method,endpoint))
        if method=='GET':
            if endpoint=='pulls/280':
                shown=self.ref
                if self.lag:shown=I.REVISION_BASE;self.lag-=1
                return {'number':280,'state':'open','merged':False,'draft':True,'mergeable':True,
                'head':{'sha':shown,'ref':self.branch,'repo':{'full_name':'AlecKriebel/Math'}},
                'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
            if endpoint.startswith('git/ref/heads/'):return {'object':{'sha':self.ref}}
            if endpoint.startswith('git/commits/'):
                c=endpoint.rsplit('/',1)[1];return {'sha':c,'parents':[{'sha':p} for p in self.parents[c]],'tree':{'sha':'tree-'+c}}
            raise RuntimeError('Unexpected synthetic GET '+endpoint)
        ck((self.root/'PUBLICATION_REVISION_INTENT.json').exists(),'durable revision intent before any provider mutation')
        if method=='POST':
            self.posts.append(endpoint)
            if endpoint=='git/blobs':
                import base64
                return {'sha':I.blob_sha(base64.b64decode(body['content']))}
            if endpoint=='git/trees':
                ck(body['base_tree']=='tree-'+I.REVISION_BASE,'tree starts from exact pushed head')
                ck({e['path'] for e in body['tree']}=={B.PROBLEM+'/'+n for n in self.current},'only current five overlay entries')
                return {'sha':'new-tree'}
            if endpoint=='git/commits':
                ck(body['parents']==[I.REVISION_BASE],'sole-parent revision child request')
                return {'sha':self.child,'parents':[{'sha':('e'*40 if self.mode=='new_parent_response' else I.REVISION_BASE)}],
                        'tree':{'sha':'new-tree'}}
        if method=='PATCH':
            self.patches.append(endpoint)
            ck((self.root/'PUBLICATION_REVISION_PUSH_INTENT.json').exists(),'durable push intent before branch update')
            ck(body=={'sha':self.child,'force':False},'non-force exact child ref update')
            if self.mode=='uncertain_push_old':raise RuntimeError('Synthetic lost response before push')
            self.ref=self.child
            if self.mode=='rest_lag':self.lag=1
            if self.mode=='uncertain_push_new':raise RuntimeError('Synthetic lost response after push')
            return {'object':{'sha':self.child}}
        raise RuntimeError('Unexpected synthetic provider boundary')

    def gate(self,phase,head):
        self.gates+=1;self.gate_heads.append(head)
        ck(phase=='before_integration','fresh integration phase')
        if self.mode=='branch_name_before_objects' and self.gates==1:self.branch='codex/different-pr280'
        if self.mode=='branch_name_before_push' and self.gates==2:self.branch='codex/different-pr280'
        if self.mode=='concurrent_branch_before_objects' and self.gates==1:self.ref='e'*40
        if self.mode=='concurrent_branch_before_push' and self.gates==2:self.ref='e'*40
        if ((self.mode=='local_release_before_objects' and self.gates==1) or (self.mode=='local_release_before_push' and self.gates==2)):
            with (self.publication/'README.md').open('ab') as stream:stream.write(b'concurrent change')
        if self.mode=='expired_or_failed_gate':raise RuntimeError('Synthetic live gate expired')
        return {'receipt':'synthetic-gate-'+str(self.gates)},{}

    def contexts(self):
        stack=ExitStack();stack.enter_context(patch.object(I,'AUDIT',self.root));stack.enter_context(patch.object(I,'api',self.api))
        stack.enter_context(patch.object(I,'require_release_clearance',lambda:True));stack.enter_context(patch.object(I,'collect',self.gate))
        stack.enter_context(patch.object(I,'subtree',lambda c,p,recursive=True:copy.deepcopy(self.trees[c]) if p==B.PROBLEM else copy.deepcopy(self.outer[c,p])))
        stack.enter_context(patch.object(I,'blob',lambda c,p:self.queues[c]))
        stack.enter_context(patch.object(I,'PUBLICATION',self.publication));stack.enter_context(patch.object(B,'PUBLICATION',self.publication))
        return stack


def main():
    modes=['normal','wrong_parent','old_file_tamper','original_file_tamper','old_extra_file','old_extra_empty_directory','old_missing_directory',
      'old_queue_other_bytes','old_own_queue','old_root_sibling','old_attempt_sibling','child_file_tamper','child_original_tamper',
      'child_extra_empty_directory','child_missing_directory','child_queue','child_root_sibling','child_attempt_sibling','wrong_pr_head',
      'history_manifest_tamper','history_payload_tamper','new_parent_response','concurrent_branch_before_objects','concurrent_branch_before_push','expired_or_failed_gate','new_parent_get','local_snapshot_tamper','local_release_before_objects','local_release_before_push','main_as_head_ref','branch_name_before_objects','branch_name_before_push']
    with ExitStack() as guard:
        guard.enter_context(patch.object(subprocess,'run',forbidden));guard.enter_context(patch.object(socket,'socket',forbidden))
        with tempfile.TemporaryDirectory(dir=HERE,prefix='revision_synthetic_') as temp:
            root=Path(temp)
            for mode in modes:
                f=Fixture(root/mode,mode)
                # Preserve old receipt names; actual revision must never touch them.
                old_names=['PUBLICATION_BRANCH_PUSH_INTENT.json','PUBLICATION_BRANCH_COMMIT.json','PUBLICATION_BRANCH_RECONCILIATION.json']
                for n in old_names:(f.root/n).write_text('historical-'+n)
                with f.contexts():
                    try:value=I.revise(I.REVISION_BASE)
                    except RuntimeError as error:ck(mode!='normal','valid revision rejected '+str(error));actual='reject'
                    else:ck(mode=='normal' and value['status']=='pushed_and_verified','hostile revision accepted');actual='accept'
                ck(all((f.root/n).read_text()=='historical-'+n for n in old_names),'old push receipts unchanged')
                if mode!='normal':ck(not f.patches,'hostile case reached ref update')
                CASES.append({'case':mode,'actual':actual,'synthetic_posts':len(f.posts),'synthetic_patches':len(f.patches),'actual_provider_attempts':0})
            for mode in ['uncertain_push_old','uncertain_push_new','rest_lag']:
                f=Fixture(root/mode,mode)
                with f.contexts():
                    try:I.revise(I.REVISION_BASE)
                    except RuntimeError:pass
                    else:raise RuntimeError('Uncertain push must require reconciliation')
                    ck((f.root/'PUBLICATION_REVISION_UNCERTAIN.json').exists(),'uncertain outcome retained')
                    posts=len(f.posts);patches=len(f.patches)
                    try:value=I.revise(I.REVISION_BASE)
                    except RuntimeError:ck(mode=='uncertain_push_old','known new ref should reconcile');result='blocked_no_retry'
                    else:ck(mode in {'uncertain_push_new','rest_lag'} and value['read_only_reconciliation'],'wrong read-only reconciliation');result='verified_read_only'
                    ck(len(f.posts)==posts and len(f.patches)==patches,'no blind mutation retry')
                CASES.append({'case':mode,'actual':result,'additional_synthetic_mutations':0})
            f=Fixture(root/'verified_outcome_idempotence')
            with f.contexts():
                first=I.revise(I.REVISION_BASE);posts=len(f.posts);patches=len(f.patches)
                old=(f.root/'PUBLICATION_REVISION_OUTCOME.json').read_bytes();second=I.revise(I.REVISION_BASE)
                ck(first==second and (f.root/'PUBLICATION_REVISION_OUTCOME.json').read_bytes()==old,'verified outcome immutable idempotence')
                ck(len(f.posts)==posts and len(f.patches)==patches,'idempotent reconciliation has no additional mutation')
            CASES.append({'case':'verified_outcome_idempotence','actual':'verified_read_only','additional_synthetic_mutations':0})
            f=Fixture(root/'wrong_expected')
            with f.contexts():
                try:I.revise(B.ORIGINAL)
                except RuntimeError:pass
                else:raise RuntimeError('Revision accepted original head argument')
                ck(not f.calls,'wrong explicit head rejected before providers')
            CASES.append({'case':'wrong_expected_head','actual':'reject','synthetic_mutations':0})
            f=Fixture(root/'immutable_receipt')
            with f.contexts():
                I.revision_write('PUBLICATION_REVISION_INTENT.json',{'first':True})
                before=(f.root/'PUBLICATION_REVISION_INTENT.json').read_bytes()
                try:I.revision_write('PUBLICATION_REVISION_INTENT.json',{'first':False})
                except RuntimeError:pass
                else:raise RuntimeError('Receipt overwrite accepted')
                ck((f.root/'PUBLICATION_REVISION_INTENT.json').read_bytes()==before,'exclusive immutable receipt')
                try:I.revise(I.REVISION_BASE)
                except RuntimeError:pass
                else:raise RuntimeError('Conflicting prior intent accepted')
                ck(not f.posts and not f.patches,'conflicting intent prevents mutations')
            CASES.append({'case':'immutable_conflicting_receipt','actual':'reject','synthetic_mutations':0})
    ck(not ATTEMPTS,'zero actual providers')
    result={'timestamp':B.stamp(),'optimization':sys.flags.optimize,'controls':len(CASES),'all_passed':True,
      'actual_provider_attempts':0,'scope':'Actual current revision functions; synthetic API methods and fresh gates only; current root clearance remains false',
      'helper_sha256':hashlib.sha256((AUDIT/'repository_integration.py').read_bytes()).hexdigest(),'cases':CASES}
    write(HERE/('REVISION_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'REVISION_CONTROLS.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
