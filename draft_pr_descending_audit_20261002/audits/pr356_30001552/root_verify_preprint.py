#!/usr/bin/env python3
"""Capture actual full public package verification outside the extracted package."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, subprocess, sys, zipfile

A=Path(__file__).resolve().parent
P=A/'preprint'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def bind(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
label=sys.argv[1]
reuse=sys.argv[2] if len(sys.argv)>2 else None
assert label.isalnum() or all(x.isalnum() or x=='_' for x in label)
out=A/'root_replay_private'/('preprint_'+label)
out.mkdir(parents=True,exist_ok=False)
names=['alternating-antimorphic-fine-wilf.tex','alternating-antimorphic-fine-wilf.pdf','alternating-antimorphic-verification.zip','zenodo-deposit.json']
pins={name:bind(P/name) for name in names}
dump(out/'PREEXECUTION.json',{'utc':now(),'files':pins,'orchestrator':bind(Path(__file__))})
(out/'orchestrator.executed.py').write_bytes(Path(__file__).read_bytes())
with zipfile.ZipFile(P/names[2]) as z:
 infos=z.infolist();members=[x.filename for x in infos]
 assert len(members)==len(set(members))
 for x in infos:
  rel=PurePosixPath(x.filename)
  assert rel.parts[0]=='alternating-antimorphic-verification' and '..' not in rel.parts and not rel.is_absolute()
  assert x.external_attr>>16==0o100644 and not x.is_dir()
 z.extractall(out/'extracted')
root=out/'extracted/alternating-antimorphic-verification'
assert (root/names[0]).read_bytes()==(P/names[0]).read_bytes()
assert (root/names[3]).read_bytes()==(P/names[3]).read_bytes()
meta=json.loads((P/names[3]).read_text())
assert len(meta['metadata'])==10
assert meta['files']==[{'path':names[1]},{'path':names[2]}]
assert meta['metadata']['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
runs={}
for label,flags in [('integrity',[])]+([] if reuse else [('full',['--full'])]):
 code=root/'verify_supplement.py';(out/(label+'.executed.py')).write_bytes(code.read_bytes())
 argv=['/opt/homebrew/bin/python3.11','-B',str(code),*flags]
 started=now();p=subprocess.run(argv,cwd=root,env=env,capture_output=True);finished=now()
 (out/(label+'.stdout')).write_bytes(p.stdout);(out/(label+'.stderr')).write_bytes(p.stderr)
 receipt={'argv':argv,'started_utc':started,'finished_utc':finished,'exit_code':p.returncode,
 'code':bind(code),'stdout':bind(out/(label+'.stdout')),'stderr':bind(out/(label+'.stderr'))}
 dump(out/(label+'.receipt.json'),receipt)
 assert p.returncode==0 and p.stderr==b'',receipt
 result=json.loads(p.stdout);assert result['status']=='PASS' and result['payload_files_checked']==68 and result['submitted_files_checked']==16
 assert len(result['runs'])==(4 if label=='integrity' else 10)
 runs[label]=receipt
if reuse:
 prior=A/'root_replay_private'/('preprint_'+reuse)
 pre=json.loads((prior/'PREEXECUTION.json').read_text())
 for name in names:
  if name.endswith('.pdf'):continue
  assert pre['files'][name]==pins[name]
 old=json.loads((prior/'full.receipt.json').read_text())
 assert old['exit_code']==0 and old['stderr']['bytes']==0
 assert bind(prior/'full.stdout')==old['stdout'] and bind(prior/'full.stderr')==old['stderr']
 assert old['code']==bind(root/'verify_supplement.py')
 result=json.loads((prior/'full.stdout').read_bytes())
 assert result['status']=='PASS' and result['payload_files_checked']==68 and len(result['runs'])==10
 runs['full']={'genuine_prior_capture_reused':True,'capture':str(prior.relative_to(A)),
  'reason':'Exact current ZIP, source and metadata match prior native full run; finished PDF export does not change supplement programs or payload.',
  'receipt':bind(prior/'full.receipt.json'),'stdout':old['stdout'],'stderr':old['stderr'],'exit_code':0}
assert {name:bind(P/name) for name in names}==pins
r={'utc':now(),'status':'PASS_EXACT_PDF_SOURCE_METADATA_AND_WHOLE_PUBLIC_PACKAGE','files':pins,'runs':runs,
   'zip_members':69,'payload_files':68,'capture':str(out.relative_to(A)),
   'math_completion_percent':100,'publication_workflow_percent':50,'fresh_sequential_preprint_reviews_pending':True}
dump(A/'ROOT_PREPRINT_PACKAGE_VERIFICATION.json',r)
print(json.dumps({k:v for k,v in r.items() if k not in ('files','runs')},indent=2))
