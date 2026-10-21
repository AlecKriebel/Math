#!/usr/bin/env python3
"""Retain complete actual streams and exact program bodies for audit replay."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

out=Path(__file__).resolve().parent
source=out.parent/'snapshot/unsolved_math_prioritization/attempts/9900002'
utc=lambda:datetime.now(timezone.utc).isoformat()
programs=[('fresh_probability',out/'probability_controls.py',None),
          ('author_replay',source/'verify_turn1.py',source/'TURN_1_CHECKS.json'),
          ('inherited_checker_replay',source/'review/independent_checks.py',
           source/'review/independent_output.json')]
receipt={'started_utc':utc(),'python_executable':sys.executable,
         'python_version':sys.version,'runs':[]}
for name,program,expected in programs:
    body=program.read_text()
    argv=[sys.executable,'-B',str(program)]
    started=utc()
    try:
        r=subprocess.run(argv,cwd=str(out),capture_output=True,text=True,timeout=60)
        entry={'name':name,'started_utc':started,'ended_utc':utc(),'argv':argv,
               'cwd':str(out),'program_sha256':hashlib.sha256(program.read_bytes()).hexdigest(),
               'program_body':body,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
        if expected is not None:
            entry['expected_output_path']=str(expected)
            entry['byte_identical_to_expected']=r.stdout.encode()==expected.read_bytes()
    except Exception as e:
        entry={'name':name,'started_utc':started,'ended_utc':utc(),'argv':argv,
               'cwd':str(out),'program_sha256':hashlib.sha256(program.read_bytes()).hexdigest(),
               'program_body':body,'exception':repr(e),'stdout':getattr(e,'stdout',None),
               'stderr':getattr(e,'stderr',None)}
    receipt['runs'].append(entry)
    (out/'CONTROL_EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in entry.items() if k in ('name','exit_code','exception','byte_identical_to_expected')}))
    if entry.get('exit_code')==0 and name=='fresh_probability':
        (out/'CONTROL_OUTPUT.json').write_text(entry['stdout'])
    if entry.get('exit_code') != 0:
        with (out/'FAILED_EXECUTIONS.jsonl').open('a') as f:
            f.write(json.dumps(entry)+'\n')
receipt['ended_utc']=utc()
receipt['all_exit_zero']=all(e.get('exit_code')==0 for e in receipt['runs'])
(out/'CONTROL_EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('all_exit_zero',receipt['all_exit_zero'])
