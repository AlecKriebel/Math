"""Bind the already reviewed exact package to actual staging and fresh PR intake."""
from pathlib import Path
import base64
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]
C=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'
def sha(b): return hashlib.sha256(b).hexdigest()
def bind(p): return {'path':p.relative_to(R).as_posix(),'sha256':sha(p.read_bytes())}
def load(p): return json.loads(p.read_bytes())
if sys.flags.optimize: raise RuntimeError('Optimization forbidden')
(F/'PREPUBLICATION_SOURCE.py').write_bytes(Path(__file__).read_bytes())
ready=load(F/'EXACT_READY_PACKAGE_READBACK.json')
assert ready['reviewed_head']=='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29'
assert ready['existing_two_independent_review_rounds_retained'] is True
assert ready['new_independent_review_claimed'] is False
for pin in [ready['old_ROOT_final_adjudication'],ready['old_ROOT_priority_adjudication'],ready['zenodo_manifest'],*ready['operative_publication_files']]:
    p=R/pin['path']; assert p.is_file() and not p.is_symlink()
    assert len(p.read_bytes())==pin['bytes'] and sha(p.read_bytes())==pin['sha256']
commands=[]
def run(name,argv):
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=60)
    (F/(name+'.stdout')).write_bytes(out); (F/(name+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
    assert child.returncode==0
    return json.loads(out)
pr=run('prepublish_PR',['gh','pr','view','57','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName'])
assert pr=={'number':57,'state':'OPEN','isDraft':True,'headRefOid':ready['reviewed_head'],'baseRefName':'main'}
q=run('prepublish_QUEUE',['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid']])
body=base64.b64decode(q['content']); blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
assert blob==q['sha']=='ff7925a66537e55c8bc9e6398ed2df94c4faddd7'
rows=[s for s in body.decode().splitlines() if '| 30003354 /' in s]
assert len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and rows[0].split('|')[9].strip()=='1/5'
receipts=[]
for name in ['root_pr57_zenodo_check_20261004_actual_capture','root_pr57_zenodo_stage_20261004_actual_capture','root_pr57_zenodo_staged_inspection_20261004_actual_capture']:
    cap=C/name; rec=load(cap/'CAPTURE.json'); output=load(cap/'stdout.bin')
    assert rec['status']=='PASS' and rec['completed'] and rec['exit_code']==0
    assert rec['stdout']['sha256']==sha((cap/'stdout.bin').read_bytes())
    assert output['environment']=='production'
    if 'check' not in name: assert output['id']==23131374 and output['state']=='ready_to_publish'
    receipts.append({'capture':bind(cap/'CAPTURE.json'),'output':bind(cap/'stdout.bin')})
record={'schema':'pr57-actual-staged-prepublication-gate/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'reviewed_head':pr['headRefOid'],'literal_status':'claimed_solved','original_budget':'1/5','QUEUE_blob_SHA1':blob,'ready_package':bind(F/'EXACT_READY_PACKAGE_READBACK.json'),'zenodo_manifest':ready['zenodo_manifest'],'actual_stage_receipts':receipts,'record_id':23131374,'publication_authorized':True,'original_priority_rule_applied':True,'PR50_priority_exception_extended':False,'actual_commands':commands,'published':False,'PR57_ordered_workflow_percent':85,'dated_completed_program_fraction_percent':5/99*100,'new_central_proof_attempts':0,'goal_complete':False}
with (F/'ACTUAL_PREPUBLICATION_GATE.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
print(json.dumps(record,indent=2))
