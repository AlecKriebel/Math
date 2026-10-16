#!/usr/bin/env python3
"""Replay the frozen package in both Python modes; do not prove the infinite theorem."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,time
root=Path(__file__).resolve().parent
source=root/'source'
manifest=source/'PUBLICATION_MANIFEST.json'
pin=hashlib.sha256(manifest.read_bytes()).hexdigest()
runs=[]
for optimized in (False,True):
 flags=['-I','-B']+(['-O'] if optimized else [])
 command=[sys.executable,*flags,str(source/'verify_publication.py'),pin,'--full']
 started=time.monotonic()
 result=subprocess.run(command,cwd='/',capture_output=True,text=True,timeout=900)
 if result.returncode:raise RuntimeError(result.stderr)
 value=json.loads(result.stdout)
 runs.append({'mode':'optimized' if optimized else 'normal','exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-started,3),'stdout_sha256':hashlib.sha256(result.stdout.encode()).hexdigest(),'result':value})
if runs[0]['result']!=runs[1]['result']:raise RuntimeError('normal/optimized results differ')
record={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_sha256':pin,'runs':runs,'normal_optimized_semantics_identical':True,'infinite_theorem_verified_by_program':False,'scope':'Closed 61-file inventory, three ZIP/extracted identity bindings, historical finite diagnostics and 68 integrity rejections; manual proofs and priority are separate.'}
(root/'ROOT_REPLAY_RESULTS.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','manifest_sha256':pin,'files':runs[0]['result']['files'],'archive_members':runs[0]['result']['archive_members_verified'],'runs':len(runs),'infinite_theorem_verified_by_program':False}))
