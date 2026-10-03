#!/usr/bin/env python3
"""Root's actual private unchanged-program reproduction; no proof by assertion count."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr41_9700035'
S=A/'source_snapshot'
O=A/'root_original_actual_reproduction'
O.mkdir(exist_ok=False)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def pin(p):
 raw=p.read_bytes();return dict(path=p.relative_to(O).as_posix(),bytes=len(raw),sha256=sha(raw))
def write_new(p,raw):
 with p.open('xb') as f:f.write(raw)
def run(label,source,cwd,arguments):
 cap=O/(label+'_capture');cap.mkdir()
 raw=source.read_bytes();write_new(cap/'prelaunch_source.py',raw)
 argv=['/usr/bin/python3','-B',str(source),*arguments]
 record=dict(label=label,source_sha256=sha(raw),argv=argv,cwd=str(cwd),started_utc=now(),actual_execution=True,stdin_supplied=False)
 child=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);record['pid']=child.pid
 try:
  out,err=child.communicate(timeout=180);timed_out=False
 except subprocess.TimeoutExpired:
  child.kill();out,err=child.communicate();timed_out=True
 write_new(cap/'stdout.bin',out);write_new(cap/'stderr.bin',err)
 record.update(finished_utc=now(),completed=True,exit_code=child.returncode,timed_out=timed_out,
  status='PASS' if child.returncode==0 and not timed_out else 'FAIL',stdout=pin(cap/'stdout.bin'),stderr=pin(cap/'stderr.bin'))
 write_new(cap/'CAPTURE.json',(json.dumps(record,indent=2)+'\n').encode())
 assert child.returncode==0 and not timed_out, record
 assert sha(source.read_bytes())==sha(raw)
 return record
snapshot=json.loads((A/'snapshot_manifest.json').read_bytes())
before={row['path']:sha((S/row['path']).read_bytes()) for row in snapshot['files']}
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
native=R/'unsolved_math_prioritization'
paths=[native/n for n in ('QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json')]+[R/'draft_pr_publication_program_20260930/inventory.json']
inputs=[dict(path=p.relative_to(R).as_posix(),bytes=len(p.read_bytes()),sha256=sha(p.read_bytes())) for p in paths]
write_new(O/'ACTUAL_FRESH_INPUTS_BEFORE.json',(json.dumps(dict(utc=now(),head=head,files=inputs),indent=2)+'\n').encode())
runs=[]
for label,source_rel,output_rel,expected in (
 ('author','verify.py','verification.json',211),
 ('original_independent','review/independent_checks.py','review/independent_results.json',3809)):
 private=O/(label+'_private');private.mkdir()
 for row in snapshot['files']:
  target=private/row['path'];target.parent.mkdir(parents=True,exist_ok=True);write_new(target,(S/row['path']).read_bytes())
 source=private/source_rel
 runs.append(run(label,source,private,[]))
 old=json.loads((S/output_rel).read_bytes());new=json.loads((private/output_rel).read_bytes())
 assert type(new['passed']) is int and new['passed']==len(new['checks'])==expected and new['failed']==0
 assert old==new, (label,'Complete saved and actual result objects differ')
 assert all(type(v) is str and v=='PASS' for v in new['checks'].values())
 assert source.read_bytes()==(S/source_rel).read_bytes()
 write_new(O/(label+'_WHOLE_OBJECT_COMPARISON.json'),(json.dumps(dict(utc=now(),status='PASS',saved=old,actual=new,whole_objects_equal=True,actual_result=pin(private/output_rel)),indent=2)+'\n').encode())
data_source=A/'primary_scope_family/audit_original_data.py'
runs.append(run('original_data',data_source,R,['--repo',str(R),'--output',str(O/'original_data')]))
after=[dict(path=p.relative_to(R).as_posix(),bytes=len(p.read_bytes()),sha256=sha(p.read_bytes())) for p in paths]
assert after==inputs and subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==head
assert {row['path']:sha((S/row['path']).read_bytes()) for row in snapshot['files']}==before
result=dict(utc=now(),status='PASS',pr=41,actual_outer_runs=runs,author_assertions=211,original_independent_assertions=3809,
 whole_saved_and_actual_JSON_objects_equal=True,original16_byte_unchanged=True,native13_and_main_unchanged=True,
 input_preimages=inputs,head_before=head,original_substantive_attempts=2,new_substantive_attempts=0,audit_turns=0,
 full_problem_solved=False,scope='Actual unchanged diagnostic and full original-data replays. Assertions do not establish measure exhaustion or the missing unconditional exterior estimate.')
write_new(O/'ROOT_REPRODUCTION.json',(json.dumps(result,indent=2)+'\n').encode())
files=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
write_new(O/'MANIFEST.json',(json.dumps(dict(self_excluded=['MANIFEST.json'],files_count=len(files),files=files),indent=2)+'\n').encode())
print(json.dumps(dict(status='PASS',outer_runs=len(runs),author_assertions=211,independent_assertions=3809,
 authored_members=len(files),manifest_sha256=sha((O/'MANIFEST.json').read_bytes()))))
