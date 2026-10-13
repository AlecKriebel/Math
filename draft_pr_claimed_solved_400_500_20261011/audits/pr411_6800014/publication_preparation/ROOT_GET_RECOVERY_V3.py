#!/usr/bin/env python3
"""Preliminary root read-only recovery; independent final software review remains.

The production transport rejects every non-GET and every Sheet operation.
This invokes recover only and records an actual method call, not a CLI run.
"""
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
CASE = HERE.parent
HELPER = HERE / 'admin_helper_v3/publication_admin_v3.py'
HELPER_SHA = 'def419151e2a2e63f11081baaba5a845f259b9b89679bca274894cb358e0543c'
ADOPTION_SHA = '8edb48b705627c97e6390e05e63879924920fb2d1d590e83a61d18542f44155b'
WHOLE_SHA = '01fe1ab553f8f17a78f222863cb6afa173323c7bd63ed32b55879ca3db4299fe'

def main():
    fd = os.open(HELPER, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f: raw = f.read()
    if hashlib.sha256(raw).hexdigest() != HELPER_SHA: raise RuntimeError('source changed')
    sp = importlib.util.spec_from_file_location('root_readonly_v3', HELPER)
    m = importlib.util.module_from_spec(sp); exec(compile(raw,str(HELPER),'exec'),m.__dict__)
    whole_raw,_ = m.g.read_regular(CASE/'ROOT_WHOLE_REVIEW_2_ACCEPTANCE.json')
    whole = json.loads(whole_raw)
    m.need(m.sha(whole_raw) == WHOLE_SHA and whole['result'] == 'PASS_WHOLE_PACKAGE_ZERO_FINDINGS'
           and whole['scientific_head'] == m.HEAD, 'whole acceptance changed')
    m.need(not m.STATE.exists(), 'V3 state already exists; no repeated recovery')
    root = CASE/'private_sources/root_publication_runs/get_recovery_v3_20261013T0527'
    root.mkdir(parents=True,exist_ok=False)
    gate = m.g.Engine(m.g.Native(),root/'scope_native')
    pr=gate.call('GET','pulls/411'); ref=gate.call('GET','git/ref/heads/research/ricci-pinching-6800014')
    q=gate.call('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+m.HEAD)
    qb=base64.b64decode(q['content'],validate=False)
    m.need(pr['state']=='open' and pr['draft'] is True and pr['merged'] is False
           and pr['head']['sha']==ref['object']['sha']==m.HEAD and q['sha']==m.g.QBLOB and m.sha(qb)==m.g.QHASH
           and m.sha(pr['body'].encode())=='959f075e0bfff3fccc2411235000bbefd491177ba078878265182806ca0500a0'
           and whole['queue_status']=='claimed_solved' and whole['turns']=='2/5','fresh eligible case changed')
    class ReadOnlyProduction(m.v1.Production):
        def zenodo(self, method, endpoint, *args, **kwargs):
            m.need(method=='GET','root transport prohibits Zenodo mutation')
            return super().zenodo(method,endpoint,*args,**kwargs)
        def sheet(self,*args,**kwargs):
            raise m.Stop('root recovery transport prohibits every Sheet operation')
    e=m.Admin(ReadOnlyProduction(),m.PRIVATE/'ROOT_ACTUAL_GET_RECOVERY_20261013T0527')
    try:
        os.environ['ZENODO_TOKEN']=m.z.token_for('production')
        result=e.recover(HERE/'admin_helper_v3/PROPOSED_RECOVERY_ADOPTION.json',ADOPTION_SHA,m.SPEC_SHA,m.NATIVE_SHA)
        m.need(e.count==8 and result['status']=='known_publication_get_verified_adopted','eight GET recovery differs')
        result.update(evidence_kind=e.kind,revision=3)
        m.v1.save(e.evidence/'RESULT.json',result,True)
        native={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'evidence_kind':'actual_root_python_method_capture',
                'method':'Admin.recover','helper_sha256':HELPER_SHA,'adoption_sha256':ADOPTION_SHA,'whole_acceptance_sha256':WHOLE_SHA,
                'fresh_scope_GETs':3,'publication_GETs':8,'remote_mutations':0,'all_sheet_calls_prohibited':True,
                'independent_final_software_review_pending':True,'result':result,
                'evidence_directory':str(e.evidence.relative_to(CASE)),
                'new_state_sha256':m.sha(m.g.read_regular(m.STATE,private=True)[0])}
        m.g.durable(root/'ROOT_METHOD_NATIVE.json',native,exclusive=True,private=True)
        print(json.dumps({'result':result['status'],'doi':result['doi'],'remote_mutations':0,'publication_GETs':8,
                          'evidence_directory':native['evidence_directory'],'new_state_sha256':native['new_state_sha256']}))
    finally:
        os.environ.pop('ZENODO_TOKEN',None)
        e.check_original()

if __name__=='__main__':main()
