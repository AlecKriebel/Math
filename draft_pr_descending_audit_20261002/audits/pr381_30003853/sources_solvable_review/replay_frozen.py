#!/usr/bin/env python3
"""Replay an exact private copy of frozen PR381, recording full stdout/stderr."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
REPO=next(p for p in ROOT.parents if (p/'.git').exists())
manifest=json.loads((AUDIT/'snapshot_manifest.json').read_text())
HEAD=manifest['head']
out=ROOT/'private_replay'/'candidate'
out.mkdir(exist_ok=True)
bindings=[]
for e in manifest['files']:
 b=(AUDIT/'snapshot'/e['path']).read_bytes()
 assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
 object_bytes=subprocess.check_output(['git','show',HEAD+':'+e['path']],cwd=REPO)
 assert object_bytes==b,e['path']
 blob=subprocess.check_output(['git','rev-parse',HEAD+':'+e['path']],cwd=REPO,text=True).strip()
 bindings.append(dict(e,git_blob_sha=blob))
 path=out/e['path']; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(b)
p=out/'problems'/'30003853_thompson_subgroup_abelianization'
commands=[('turn3',[sys.executable,str(p/'verify_turn3.py')]),
 ('author_all',[sys.executable,str(p/'REPLAY_ALL.py')]),
 ('publication',[sys.executable,str(p/'verify_publication.py')])]
runs=[]
for name,cmd in commands:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 done=subprocess.run(cmd,cwd=p,capture_output=True)
 for stream in ['stdout','stderr']:
  data=getattr(done,stream);(ROOT/'private_replay'/(name+'.'+stream)).write_bytes(data)
 runs.append({'name':name,'argv':cmd,'cwd':str(p),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':done.returncode,
  'stdout_sha256':hashlib.sha256(done.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(done.stderr).hexdigest(),'stdout_bytes':len(done.stdout),'stderr_bytes':len(done.stderr)})
 print(name,done.returncode,done.stdout.decode().strip(),done.stderr.decode().strip())
 assert done.returncode==0,name
receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_head':HEAD,'frozen_base':manifest['base'],'workspace_main_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
 'snapshot_manifest_sha256':hashlib.sha256((AUDIT/'snapshot_manifest.json').read_bytes()).hexdigest(),'exact_git_snapshot_bindings':bindings,'commands':runs,
 'source_replay':'Public author replay passes with 0/20 optional local source bindings. Fresh PDF inputs checked separately in SOURCE_RECEIPT; regenerated text/page images are not asserted byte-identical to author local outputs.'}
(ROOT/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
