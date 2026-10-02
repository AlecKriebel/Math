#!/usr/bin/env python3
"""Genuine root current freeze capture after complete source and science reading."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess
import sys

R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr40_2814'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def encoded(o):return (json.dumps(o,indent=2)+'\n').encode()
def git(*args):return subprocess.run(['git',*args],cwd=R,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def write_new(p,b):
    with p.open('xb') as f:f.write(b)

assert git('branch','--show-current').strip()==b'main'
head=git('rev-parse','HEAD').decode().strip()
assert head=='c7da3726e31648bf854f92d7fe1ea83b34a420d5'
assert not git('diff','--cached','--name-only').strip()
native=['unsolved_math_prioritization/'+n for n in (
    'QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json',
    'manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json')]
native.append('draft_pr_publication_program_20260930/inventory.json')
rows=[]
for n in sorted(native):
    p=R/n;assert p.is_file() and not p.is_symlink()
    b=p.read_bytes();rows.append({'path':n,'size':len(b),'sha256':sha(b)})
state=json.loads((R/'unsolved_math_prioritization/state.json').read_bytes())
assert not {'2814','20001896'}.intersection(state)
for line in (R/'unsolved_math_prioritization/history.jsonl').read_bytes().splitlines():
    if line.strip():assert str(json.loads(line).get('id')) not in {'2814','20001896'}
preimage={'schema':'pr40-root-approved-dated-current-preimages/v1','utc':now(),'approved_by_root':True,
    'reason':'2026-10-02: root authorizes a current administrative freeze after complete primary/proof/source and actual evidence inspection; new whole-current review remains pending.',
    'current_head':head,'files':rows,'new_substantive_attempts':0,'audit_turns':0}
card={'schema':'pr40-root-current-science-card/v1','utc':now(),'status':'UNSOLVED','full_problem_solved':False,
    'partial_valid':True,'novelty_claimed':False,'source_hold':True,'original_substantive_attempts':0,'turn_limit':5,
    'new_substantive_attempts':0,'audit_attempts_added':0,'current_model':None,'current_reasoning_effort':None,
    'current_deadline_utc':None,'new_whole_current_gate':'PENDING',
    'scope_certificate_sha256':'c8f4ff0c373073e313de3c9ead16937117134d384560dbacfb499e1333561ac4',
    'read_ledger_sha256':'0a2da801b4f214435be7fea1ec55b5d47124bc6bcadcafd8b16a9d76839a1bd6',
    'root_actual_guard_sha256':'b7ddba101a11683a1aa6a5a32eee8b1d4897fc1d2f66acf1bdc5898e26935b5e',
    'qualified_claim':'Existing theorem statements cover the literal closed/cusped and orientability cases. The project retains a valid conservative source-status partial; it asserts no new proof or recursively certified external theorem.',
    'paper_or_new_DOI_or_tracker':False}
write_new(A/'ROOT_CURRENT_INPUT_PREIMAGES.json',encoded(preimage))
write_new(A/'ROOT_SCIENCE_CARD.json',encoded(card))
source=A/'current_preparation_family/prepare_current_packet.py'
source_bytes=source.read_bytes()
assert sha(source_bytes)=='7ff0c70ff46e7ab3feec38f6434bc24a0f6dd5d90f7da7dabc99eb4167cba4a9'
source_review={'utc':now(),'root_complete_source_lines_read':271,'root_complete_contract_read':True,
    'root_current_overview_read':True,'source_sha256':sha(source_bytes),'source_only_before_this_actual_capture':True,
    'live_HEAD_independently_checked_by_root':head,'scientific_reading_and_actual_reproduction_separately_retained':True,
    'new_whole_current_verdict':'PENDING','qualification':'Builder makes no Git query; genuine root outer independently checks HEAD and all13 native preimages before/after its actual invocation.'}
write_new(A/'ROOT_CURRENT_SOURCE_REVIEW.json',encoded(source_review))
capture=A/'root_current_freeze_actual_capture';capture.mkdir(exist_ok=False)
write_new(capture/'prelaunch_source.py',source_bytes)
argv=['/usr/bin/python3','-B',str(source),'--execute']
for label,n in [('root-guard','ROOT_ACTUAL_EVIDENCE_INSPECTION.json'),('root-preimage','ROOT_CURRENT_INPUT_PREIMAGES.json'),
                ('science-card','ROOT_SCIENCE_CARD.json'),('sql-qualification','root_audit_SQL_qualification_family/BINDINGS.json')]:
    argv.extend(['--'+label+'-json',n,'--'+label+'-sha256',sha((A/n).read_bytes())])
def check():
    assert git('rev-parse','HEAD').decode().strip()==head
    for row in rows:
        b=(R/row['path']).read_bytes();assert len(b)==row['size'] and sha(b)==row['sha256']
check()
record={'schema':'pr40-root-actual-current-freeze-capture/v1','started_utc':now(),'argv':argv,'cwd':str(A),
    'source_sha256':sha(source_bytes),'native_preimages':rows,'current_head_before':head,'actual_execution':True}
child=subprocess.Popen(argv,cwd=A,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
record['pid']=child.pid
out,err=child.communicate(timeout=90)
write_new(capture/'stdout.bin',out);write_new(capture/'stderr.bin',err)
record.update(finished_utc=now(),completed=True,exit_code=child.returncode,
    stdout={'path':'stdout.bin','size':len(out),'sha256':sha(out)},stderr={'path':'stderr.bin','size':len(err),'sha256':sha(err)},
    status='PASS' if child.returncode==0 else 'FAIL')
write_new(capture/'CAPTURE.json',encoded(record))
check()
assert source.read_bytes()==source_bytes
print(json.dumps({'status':record['status'],'pid':child.pid,'exit_code':child.returncode,
    'capture_sha256':sha((capture/'CAPTURE.json').read_bytes()),'stdout':out.decode(),'stderr':err.decode()}))
sys.exit(child.returncode)
