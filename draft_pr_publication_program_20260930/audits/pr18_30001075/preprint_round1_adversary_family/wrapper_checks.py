#!/usr/bin/env python3
"""Independently inspect actual executions of the kit's capture controller."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

here=Path(__file__).resolve().parent
kit=here/'private/extracted'
program=kit/'run_capture.py'
records=[]
for name,label,mode,expected in [('positive','independent-positive','verify',0),('optimized','independent-optimized','optimized',0),('negative','independent-negative','negative',0),('duplicate_label','independent-positive','verify',1)]:
    folder=here/'capture_wrapper_actual_captures'/name;folder.mkdir(parents=True,exist_ok=False)
    source=program.read_bytes();(folder/'PRELAUNCH_SOURCE.py').write_bytes(source)
    argv=[sys.executable,'-B',str(program),label,mode]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen(argv,cwd=here,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=p.communicate()
    (folder/'stdout.bin').write_bytes(stdout);(folder/'stderr.bin').write_bytes(stderr)
    record={'argv':argv,'controller_pid':os.getpid(),'actual_outer_pid':p.pid,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'expected_exit_code':expected,'source_sha256':hashlib.sha256(source).hexdigest(),'source_unchanged':program.read_bytes()==source,'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest(),'stdout_bytes':len(stdout),'stderr_bytes':len(stderr)}
    if p.returncode!=expected or not record['source_unchanged']:raise RuntimeError('Unexpected wrapper result')
    if expected==0:
        returned=json.loads(stdout);actual=json.loads((kit/'captures'/label/'CAPTURE.json').read_bytes())
        if returned!=actual or actual['controller_pid']!=p.pid or not actual['child_launched'] or not actual['source_unchanged'] or not actual['outcome_as_expected']:raise RuntimeError('Wrapper returned a false or mismatched actual receipt')
        childout=(kit/'captures'/label/'stdout.txt').read_bytes();childerr=(kit/'captures'/label/'stderr.txt').read_bytes()
        for field,data in [('stdout.txt',childout),('stderr.txt',childerr)]:
            if actual[field]['bytes']!=len(data) or actual[field]['sha256']!=hashlib.sha256(data).hexdigest():raise RuntimeError('Wrapper stream hash mismatch')
            (folder/('nested_'+field)).write_bytes(data)
        if actual['returncode']!=(0 if mode=='verify' else 1):raise RuntimeError('Unexpected nested mode exit')
        (folder/'NESTED_CAPTURE.json').write_text(json.dumps(actual,indent=2,sort_keys=True)+'\n')
        record['actual_nested_child_pid']=actual['child_pid'];record['nested_exit_code']=actual['returncode']
    elif b'FileExistsError' not in stderr:raise RuntimeError('Duplicate label refused for an unexpected reason')
    (folder/'CAPTURE.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');records.append(record)
(here/'CAPTURE_WRAPPER_REPRODUCTION.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
print('Capture wrapper positive and deliberate fail modes preserve real child receipts; duplicate label cannot overwrite prior evidence.')
