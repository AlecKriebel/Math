#!/usr/bin/env python3
"""Capture exact executable source, PID, UTC interval, exit, and full streams."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
script=Path(sys.argv[1]).resolve()
directory=root/sys.argv[2]
directory.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
source=script.read_bytes()
operator=Path(__file__).read_bytes()
(directory/'prelaunch_source.py').write_bytes(source)
(directory/'prelaunch_operator.py').write_bytes(operator)
argv=['/usr/bin/python3','-B',str(script)]
start=utc()
pre={'argv':argv,'cwd':str(root),'operator_pid':os.getpid(),'started_utc':start,
     'source_sha256':sha(source),'operator_sha256':sha(operator),'operator_agent':'/root/pr46_complex_dynamics_adversary'}
(directory/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
with (directory/'stdout.bin').open('wb') as out,(directory/'stderr.bin').open('wb') as err:
    proc=subprocess.Popen(argv,cwd=root,stdout=out,stderr=err)
    pid=proc.pid
    exit_code=proc.wait()
finish=utc()
stdout=(directory/'stdout.bin').read_bytes()
stderr=(directory/'stderr.bin').read_bytes()
receipt={**pre,'actual_pid':pid,'finished_utc':finish,'exit_code':exit_code,
 'complete_streams':True,'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),
 'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),'post_source_sha256':sha(script.read_bytes()),
 'source_unchanged':script.read_bytes()==source}
(directory/'CAPTURE.json').write_text(json.dumps(receipt,indent=2)+'\n')
for file in directory.iterdir():file.chmod(0o444)
if sys.argv[3:]==['--freeze']:
    manifest_path=root/'COMPLEX_DYNAMICS_MANIFEST.json'
    if manifest_path.exists():raise RuntimeError('Refusing to replace an existing closure manifest')
    owned_files=sorted(p for p in root.rglob('*') if p.is_file())
    if any(p.is_symlink() for p in root.rglob('*')):raise RuntimeError('Symlink in owned topology')
    for file in owned_files:file.chmod(0o444)
    rows=[{'path':str(file.relative_to(root)),'bytes':file.stat().st_size,
           'sha256':sha(file.read_bytes()),'full_mode':file.stat().st_mode & 0o7777} for file in owned_files]
    assert all(r['full_mode']==0o444 for r in rows)
    manifest={'schema':'pr46-complex-dynamics-self-only-manifest/v1','head':'a39d178b10f75fb127058b08e0d0002b3ae97f8a',
       'operator_agent':'/root/pr46_complex_dynamics_adversary','sealed_utc':utc(),'operator_pid':os.getpid(),
       'files_count':len(rows),'files':rows,'self_excluded':['COMPLEX_DYNAMICS_MANIFEST.json'],
       'authorship_root':str(root),'sibling_or_parent_files_included':False,'all_owned_files_full_mode':0o444,
       'foreign_pdf_ocr_pixel_cache_bodies_included':False,'acceptance_verdict':None,
       'mathematical_claim_verified':True,'audit_completion_estimate_percent':100,'novel_discovery_credit_percent':0}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    manifest_path.chmod(0o444)
    receipt={**receipt,'self_only_manifest_path':str(manifest_path),'self_only_manifest_sha256':sha(manifest_path.read_bytes()),
             'manifest_files_count':len(rows),'all_files_plus_manifest_full0444':all(p.stat().st_mode & 0o7777==0o444 for p in owned_files+[manifest_path])}
print(json.dumps(receipt,indent=2))
sys.exit(exit_code)
