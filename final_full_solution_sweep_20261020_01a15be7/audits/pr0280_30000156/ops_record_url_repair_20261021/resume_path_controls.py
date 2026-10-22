#!/usr/bin/env python3
"""Existing-pushed-head read-only verification path, actual tree/queue guards, synthetic."""
from contextlib import ExitStack,redirect_stdout
import copy
import io
import json
import shutil
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import types
from unittest.mock import patch
import controls_support as S


def main():
    B,P,G,V,D=S.implementation(False)
    I=types.ModuleType('repository_integration');I.__file__=str(S.AUDIT/'repository_integration.py')
    exec(compile((S.AUDIT/'repository_integration.py').read_bytes(),I.__file__,'exec'),I.__dict__)
    H='8aebb819bfac9c12340d2f1469408943549ab530';M='b'*40;T='c'*40;cases=[]
    originals=I.originals();selected=I.selection()
    def leaf(signature):return {'mode':signature[0],'type':signature[1],'sha':signature[2]}
    def tree():return {'mode':'040000','type':'tree','sha':'synthetic-tree'}
    trees={M:{'previous.txt':leaf(('100644','blob','old')),'keepempty':tree()},
           B.ORIGINAL:{**{n:leaf(v) for n,v in originals.items()},'checks':tree(),'independent_review':tree()}}
    trees[T]={**trees[M],**trees[B.ORIGINAL],**{n:leaf(('100644','blob',I.blob_sha(v))) for n,v in selected.items()},'preprint':tree()}
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',S.forbidden));guards.enter_context(patch.object(socket,'socket',S.forbidden))
        with tempfile.TemporaryDirectory(dir=S.HERE,prefix='resume_synthetic_') as tmp:
            root=Path(tmp)
            # Preserve actual snapshot validation in the synthetic receipt destination.
            snapshot=json.loads((S.AUDIT/'SOURCE_SNAPSHOT.json').read_text())
            shutil.copyfile(S.AUDIT/'SOURCE_SNAPSHOT.json',root/'SOURCE_SNAPSHOT.json')
            for entry in snapshot['files']:
                destination=root/entry['snapshot'];destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(S.AUDIT/entry['snapshot'],destination)
            for label,expected,stale,accept in [('already_pushed_head_resume',H,False,True),
                    ('wrong_expected_head',B.ORIGINAL,False,False),('stale_test_merge',H,True,False)]:
                calls=[]
                def api(endpoint,method='GET',body=None):
                    S.check(method=='GET','resume must never call a provider mutation');calls.append(endpoint)
                    if endpoint=='pulls/280':return {'number':280,'state':'open','merged':False,'draft':True,'mergeable':True,'merge_commit_sha':T,
                        'head':{'sha':H,'repo':{'full_name':'AlecKriebel/Math'}},'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
                    if endpoint=='git/ref/heads/main':return {'object':{'sha':M}}
                    if endpoint=='git/commits/'+T:return {'sha':T,'parents':[{'sha':'d'*40 if stale else M},{'sha':H}]}
                    if endpoint=='git/commits/'+B.ORIGINAL:return {'parents':[{'sha':B.ORIGINAL_PARENT}]}
                    raise RuntimeError('Unexpected synthetic read')
                with patch.object(I,'AUDIT',root),patch.object(I,'verify_destination',lambda:True),\
                     patch.object(I,'require_release_clearance',lambda:True),patch.object(I,'api',api),\
                     patch.object(I,'subtree',lambda c,p,recursive=True:copy.deepcopy(trees[c]) if p==B.PROBLEM else {}),\
                     patch.object(I,'blob',lambda c,p:I.BASELINE_ROW if c in {M,B.ORIGINAL_PARENT} else I.DESIRED_ROW),\
                     patch.object(sys,'argv',['repository_integration.py','verify-test-merge','--expected-pr-head',expected]):
                    try:
                        with redirect_stdout(io.StringIO()):I.main()
                    except RuntimeError as error:S.check(not accept,label+' should pass');actual='reject'
                    else:S.check(accept,label+' should reject');actual='accept'
                cases.append({'case':label,'actual':actual,'provider_methods':['GET'] if calls else [],'no_commit_action_invoked':True})
    S.check(not S.ATTEMPTS,'no actual providers')
    result={'optimization':sys.flags.optimize,'controls':len(cases),'all_controls_passed':True,'actual_provider_access_attempts':0,'cases':cases}
    S.write(S.HERE/('RESUME_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'RESUME_CONTROLS.json'),result);print(result)


if __name__=='__main__':main()
