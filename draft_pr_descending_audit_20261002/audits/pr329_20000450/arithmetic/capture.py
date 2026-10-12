#!/usr/bin/env python3
"""Native subprocess capture; writes only in this audit namespace."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--name',required=True)
parser.add_argument('--input',action='append',default=[])
parser.add_argument('--output',action='append',default=[])
parser.add_argument('command',nargs=argparse.REMAINDER)
args = parser.parse_args()
base = Path(__file__).resolve().parent
destination = base/'executions'/args.name
destination.mkdir(parents=True,exist_ok=False)
command = args.command[1:] if args.command[:1]==['--'] else args.command
def utc(): return datetime.now(timezone.utc).isoformat()
def pin(name):
    path = Path(name).resolve()
    data = path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
environment = {'PATH':'/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
               'LANG':'C','LC_ALL':'C','TZ':'UTC','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'}
before = [pin(name) for name in args.input]
record = {'actual_argv':command,'actual_env':environment,'actual_cwd':str(base),
          'capture_argv':sys.argv,'capture_interpreter':sys.executable,
          'capture_version':sys.version,'capture_program':pin(__file__),
          'start_utc':utc(),'input_before':before}
try:
    child = subprocess.run(command,cwd=base,env=environment,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr,code = child.stdout,child.stderr,child.returncode
    record['child_launched'] = True
except OSError as error:
    stdout,stderr,code = b'',str(error).encode()+b'\n',None
    record['child_launched'] = False
    record['launch_error'] = repr(error)
after = [pin(name) for name in args.input]
record.update({'end_utc':utc(),'actual_child_exit_code':code,'input_after':after,
               'unchanged_inputs':before==after,
               'output_pins':[pin(name) for name in args.output if Path(name).exists()]})
(destination/'stdout.txt').write_bytes(stdout)
(destination/'stderr.txt').write_bytes(stderr)
(destination/'metadata.json').write_text(json.dumps(record,indent=2)+'\n')
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
print(json.dumps({'receipt':str(destination),'actual_child_exit_code':code,
                  'child_launched':record['child_launched'],'unchanged_inputs':before==after}))
sys.exit(90 if before!=after else (code if code is not None else 91))
