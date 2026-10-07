#!/usr/bin/env python3
"""Reproduce only pinned family-129 sources. Not yet successfully run to completion."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
root=Path(__file__).resolve().parent
receipts=root/'receipts';receipts.mkdir(exist_ok=True)
env=os.environ.copy();env['MATHLIB_CACHE_DIR']=str(root/'.lake/cache')
def run(name,argv):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic()
    with (receipts/(name+'.log')).open('w') as log:
        proc=subprocess.Popen(argv,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
        for line in proc.stdout:
            log.write(line);log.flush();print(line,end='',flush=True)
        rc=proc.wait()
    receipt={'argv':argv,'cwd':str(root),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-clock,'exit_code':rc,'log_sha256':hashlib.sha256((receipts/(name+'.log')).read_bytes()).hexdigest()}
    (receipts/(name+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    if rc:sys.exit(rc)
manifest=json.loads((root/'source_manifest.json').read_text())
for m,d in manifest['modules'].items():
    if hashlib.sha256((root/d['path']).read_bytes()).hexdigest()!=d['sha256']:
        sys.exit('Pinned OAI source hash mismatch: '+m)
run('lean_version',['lean','--version'])
run('lake_version',['lake','--version'])
# Populate packages at the already resolved exact manifest pins. Avoid lake update,
# whose tag-fetch would fetch unrelated history and change the resolved manifest.
for dep in json.loads((root/'lake-manifest.json').read_text())['packages']:
    q=root/'.lake/packages'/dep['name'];q.mkdir(parents=True,exist_ok=True)
    if not (q/'.git').exists():
        run('init_'+dep['name'],['git','init',str(q)])
        run('remote_'+dep['name'],['git','-C',str(q),'remote','add','origin',dep['url']])
    current=subprocess.run(['git','-C',str(q),'rev-parse','HEAD'],capture_output=True,text=True)
    if current.returncode or current.stdout.strip()!=dep['rev']:
        run('fetch_'+dep['name'],['git','-C',str(q),'fetch','--depth=1','origin',dep['rev']])
        run('checkout_'+dep['name'],['git','-C',str(q),'checkout','--detach',dep['rev']])
run('cache_get',['lake','exe','cache','get','Mathlib'])
run('family129_build',['lake','build',*manifest['entrypoints']])
run('axioms',['lake','env','lean','-DautoImplicit=false','AuditAxioms.lean'])
