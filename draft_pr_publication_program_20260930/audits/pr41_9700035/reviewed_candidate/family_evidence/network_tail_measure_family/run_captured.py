#!/usr/bin/env python3
"""Capture only our independently authored diagnostics, never reviewed helpers."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import traceback

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--label',required=True)
parser.add_argument('--program',type=Path,required=True)
parser.add_argument('--expected',type=int,default=0)
args=parser.parse_args()
assert args.label and '/' not in args.label and args.program.resolve().is_relative_to(HERE)
capture=HERE/'executions'/args.label
capture.mkdir(parents=True,exist_ok=False)
source=args.program.read_bytes()
(capture/'source.py').write_bytes(source)
command=['/usr/bin/python3',str(args.program.resolve())]
row={'argv':command,'cwd':str(HERE),'stdin_supplied':False,'source_sha256':hashlib.sha256(source).hexdigest(),
     'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_execution':False,'launch_attempted':False,'exit_code':None,'timeout_seconds':60}
for channel in ['stdout','stderr']:(capture/channel).write_bytes(b'')
(capture/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
error=error_tb=None
try:
    row['launch_attempted']=True
    (capture/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
    result=subprocess.run(command,cwd=HERE,capture_output=True,timeout=60)
    row.update(actual_execution=True,exit_code=result.returncode,stdio_kind='complete')
    stdout,stderr=result.stdout,result.stderr
except subprocess.TimeoutExpired as caught:
    error,error_tb=caught,caught.__traceback__;row.update(actual_execution=True,stdio_kind='partial_timeout');stdout,stderr=caught.stdout or b'',caught.stderr or b''
except OSError as caught:
    error,error_tb=caught,caught.__traceback__;row['stdio_kind']='no_child_launched';stdout=stderr=b''
finally:
    if error:row['failure']={'type':type(error).__name__,'message':str(error),'traceback':''.join(traceback.format_exception(type(error),error,error_tb))}
    for channel,data in [('stdout',stdout),('stderr',stderr)]:
        if isinstance(data,str):data=data.encode()
        (capture/channel).write_bytes(data);row[channel]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    row['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    row['observed_expected']=error is None and row['exit_code']==args.expected
    (capture/'receipt.json').write_text(json.dumps(row,indent=2)+'\n')
print(json.dumps(row,indent=2))
assert row['observed_expected'],'Captured diagnostic failed; failure retained'
