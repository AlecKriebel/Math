#!/usr/bin/env python3
"""Actual rejection processes plus explicitly mocked JSON-comparison layer tests."""
from pathlib import Path
import contextlib,copy,hashlib,importlib.util,io,json,os,shutil,subprocess,sys,types,tempfile
H=Path(__file__).resolve().parent;C=H/'.cache'/'tamper';C.mkdir(exist_ok=True);ROOT=H/'.cache/extract/weighted_centers_verification';rows=[]
def reseal(d):
 p=d/'MANIFEST.json';m=json.loads(p.read_text())
 for n in list(m['files']):
  if (d/n).is_file():b=(d/n).read_bytes();m['files'][n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 p.write_text(json.dumps(m,indent=2)+'\n')
def actual(name,mutate,reason,opt=False):
 d=C/name
 if d.exists():shutil.rmtree(d)
 shutil.copytree(ROOT,d);mutate(d)
 p=subprocess.run([sys.executable,*(['-O'] if opt else []),str(d/'run_all.py')],cwd=d,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 assert p.returncode and reason in p.stderr,(name,p.returncode,p.stdout,p.stderr)
 rows.append({'case':name,'method':'actual driver process','status':'REJECTED_AS_REQUIRED','reason':reason})
actual('changed_payload',lambda d:(d/'weighted_centers.tex').write_bytes((d/'weighted_centers.tex').read_bytes()+b'X'),'Outer payload mismatch')
actual('extra_payload',lambda d:(d/'unregistered.txt').write_text('X'),'Outer payload inventory mismatch')
actual('missing_payload',lambda d:(d/'reviews/search01/SOURCE_CHECKS.md').unlink(),'Outer payload inventory mismatch')
def original(d):
 p=d/'original/unsolved_math_prioritization/attempts/30006605/bundle/PROOF.md';p.write_bytes(p.read_bytes()+b'X');reseal(d)
actual('outer_resealed_changed_original',original,'Nested hash mismatch')
def nested_hash(d):
 p=d/'reviews/search01/SHA256SUMS';s=p.read_text();p.write_text(('0' if s[0]!='0' else '1')+s[1:]);reseal(d)
actual('outer_resealed_nested_hash',nested_hash,'Nested hash mismatch')
def registry(d):
 p=d/'SEALS.json';x=json.loads(p.read_text());x.pop();p.write_text(json.dumps(x));reseal(d)
actual('outer_resealed_registry',registry,'Seal registry mismatch')
def missing_nested(d):
 p=d/'reviews/search01/SOURCE_CHECKS.md';p.unlink();m=json.loads((d/'MANIFEST.json').read_text());del m['files']['reviews/search01/SOURCE_CHECKS.md'];(d/'MANIFEST.json').write_text(json.dumps(m))
actual('outer_resealed_missing_nested',missing_nested,'Nested hash mismatch or missing payload')
def symlink(d):
 p=d/'weighted_centers.tex';p.unlink();p.symlink_to(d/'README.md')
actual('symlink_payload',symlink,'Unexpected symlink')
actual('assertions_disabled',lambda d:None,'Run with assertions enabled',opt=True)
# Unit-isolate the comparison policy. These outputs are mocks, not real controls.
sys.path.insert(0,str(ROOT));spec=importlib.util.spec_from_file_location('review_replay',ROOT/'run_all.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
baseline={p.relative_to(ROOT).as_posix():p.read_bytes() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
tempfile.tempdir=str(C)
jobs=json.loads(baseline['JOBS.json']);records={j['script']:json.loads(baseline[j['record']]) for j in jobs}
real_run=subprocess.run

def layer(name,change_actual=lambda x:None,change_jobs=lambda x:None,should_pass=False,changed_after=False):
 payload=copy.deepcopy(baseline);js=json.loads(payload['JOBS.json']);change_jobs(js);payload['JOBS.json']=(json.dumps(js,indent=2)+'\n').encode();m=json.loads(payload['MANIFEST.json']);b=payload['JOBS.json'];m['files']['JOBS.json']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};payload['MANIFEST.json']=json.dumps(m).encode()
 actuals=copy.deepcopy(records);change_actual(actuals);calls=[0]
 def inv():
  calls[0]+=1
  if changed_after and calls[0]>1:return dict(payload,extra=b'changed')
  return copy.deepcopy(payload)
 def fake_run(cmd,**kwargs):
  s=Path(cmd[1]);key=next(k for k in actuals if s.as_posix().endswith(k));return types.SimpleNamespace(returncode=0,stdout=json.dumps(actuals[key]),stderr='')
 mod.inventory=inv;mod.subprocess.run=fake_run
 try:
  with contextlib.redirect_stdout(io.StringIO()):mod.main()
 except RuntimeError as e:
  assert not should_pass,(name,str(e));reason=str(e)
 else:assert should_pass,name;reason='complete equality accepted'
 finally:mod.subprocess.run=real_run
 rows.append({'case':name,'method':'explicit mocked-output comparison-policy unit control','status':'PASS' if should_pass else 'REJECTED_AS_REQUIRED','reason':reason})
layer('complete_baseline',should_pass=True)
key='reviews/oracle01/controls.py'
def clocks(x):
 for n in ('started_at_utc','completed_at_utc','elapsed_seconds'):x[key][n]='changed execution clock'
layer('three_top_level_clocks_only',clocks,should_pass=True)
def mathchange(x):x[key]['fresh_bad_math']=1
layer('mathematical_field_changed',mathchange)
def nestedclock(x):x[key]['nested']={'elapsed_seconds':'mathematical field'}
layer('nested_clock_named_field_changed',nestedclock)
layer('extra_clock_normalization',change_jobs=lambda js:js[2]['ignored_clock_fields'].append('fresh_bad_math'))
layer('normalization_on_wrong_job',change_jobs=lambda js:js[0].update(ignored_clock_fields=['started_at_utc','completed_at_utc','elapsed_seconds']))
layer('payload_changed_after_jobs',changed_after=True)
(H/'PACKAGE_NEGATIVE_RESULTS.json').write_text(json.dumps({'status':'PASS','actual_rejection_processes':9,'mocked_policy_unit_controls':7,'cases':rows},indent=2)+'\n');print('PASS:9 actual tamper rejection processes and7 explicitly mocked policy unit controls')
