#!/usr/bin/env python3
import ast
import datetime
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

root = Path(__file__).resolve().parent
python = '/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
script = root / 'independent_ideal_controls.py'
body = script.read_bytes()
if any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(body))):
    raise RuntimeError('Independent checker contains optimization-sensitive assertions')
env = {'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'}
records = []
outputs = []
for optimized, filename in ((False,'INDEPENDENT_CONTROLS_NORMAL.json'),
                            (True,'INDEPENDENT_CONTROLS_OPTIMIZED.json')):
    argv = [python] + (['-O'] if optimized else []) + ['-E','-S','-B','-P',str(script),str(root/filename)]
    start_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    started = time.monotonic()
    child = subprocess.Popen(argv,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = child.communicate(timeout=30)
    if child.returncode != 0 or stderr:
        raise RuntimeError('Independent child failed or emitted stderr')
    data = json.loads(stdout)
    if (root/filename).read_bytes() != stdout:
        raise RuntimeError('Printed and saved independent result differ')
    if data['result'] != 'PASS' or not data['exception_guards_active']:
        raise RuntimeError('Checker did not pass its explicit runtime guard')
    if data['script_sha256'] != hashlib.sha256(body).hexdigest():
        raise RuntimeError('Checker body pin changed')
    if data['python_optimization_level'] != int(optimized):
        raise RuntimeError('Optimization mode not authenticated')
    outputs.append(data)
    records.append({'pid':child.pid,'argv':argv,'start_utc':start_utc,
                    'elapsed_seconds':time.monotonic()-started,
                    'returncode':child.returncode,'process_completed_and_waited':True,
                    'stdout_bytes':len(stdout),'stdout_sha256':hashlib.sha256(stdout).hexdigest(),
                    'stderr_bytes':len(stderr),'output_file':filename})
if {k:v for k,v in outputs[0].items() if k!='python_optimization_level'} != {k:v for k,v in outputs[1].items() if k!='python_optimization_level'}:
    raise RuntimeError('Normal and optimized controls diverge')
receipt = {'root_pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'physical_python':python,'exception_guards_active_under_optimization':True,
           'script_sha256':hashlib.sha256(body).hexdigest(),
           'ast_assert_statements':0,'records':records,
           'same_logical_result_except_mode':True,
           'no_original_or_shared_file_writes':True}
(root/'EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
