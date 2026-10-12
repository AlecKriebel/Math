#!/usr/bin/env python3
"""Capture only the repository deposit tool's read-only local `check` branch."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

here=Path(__file__).resolve().parent
repository=here.parents[3]
program=repository/'zenodo_deposit_tool/zenodo.py'
manifest=here.parent/'root_final_package_20261003/zenodo-deposit.json'
folder=here/'production_tool_check_actual_capture';folder.mkdir(exist_ok=False)
source=program.read_bytes();(folder/'PRELAUNCH_SOURCE.py').write_bytes(source)
argv=[sys.executable,'-B',str(program),'check',str(manifest)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen(argv,cwd=here,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr=p.communicate()
(folder/'stdout.bin').write_bytes(stdout);(folder/'stderr.bin').write_bytes(stderr)
record={'argv':argv,'controller_pid':os.getpid(),'actual_child_pid':p.pid,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'source_sha256':hashlib.sha256(source).hexdigest(),'source_unchanged':source==program.read_bytes(),'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest(),'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),'operation':'local check only; no credential read/network/draft/deposit/publication branch executed'}
(folder/'CAPTURE.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
if p.returncode or not record['source_unchanged']:raise RuntimeError('Local production mapping check failed')
result=json.loads(stdout)
expected={'common_tangent_nullness.pdf':(92307,'80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327'),'common_tangents_null_locus_v1.zip':(182613,'1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5')}
if len(result['files'])!=2 or {f['name']:(f['size'],f['sha256']) for f in result['files']}!=expected:raise RuntimeError('Tool file mapping differs from reviewed pair')
print('Actual local production-tool check passes and returns the exact two reviewed artifacts.')
