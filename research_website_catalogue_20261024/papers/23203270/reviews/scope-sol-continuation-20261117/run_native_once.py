"""One ordinary unmodified native stabilization route in an isolated folder."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import subprocess
import time

LANE=Path(__file__).resolve().parent
SOURCE=LANE.parents[1]/'sources/archives/01-source-and-verification.zip.extracted'
RUN=LANE/'native-route'
assert not RUN.exists(), 'No second native attempt is authorized'
RUN.mkdir()
native=SOURCE/'check_stabilization.py'
target=RUN/native.name
shutil.copyfile(native,target)
assert target.read_bytes()==native.read_bytes()
native_sha=hashlib.sha256(native.read_bytes()).hexdigest()
before=subprocess.run(['python3',str(LANE/'guard_sources.py'),'native_before'],capture_output=True)
assert before.returncode==0,before.stderr.decode()
command=['python3',str(target)]
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
started=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
with (RUN/'stdout.txt').open('wb') as out, (RUN/'stderr.txt').open('wb') as err:
    completed=subprocess.run(command,cwd=RUN,env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
elapsed=time.perf_counter()-clock;finished=datetime.now(timezone.utc).isoformat()
after=subprocess.run(['python3',str(LANE/'guard_sources.py'),'native_after'],capture_output=True)
assert after.returncode==0,after.stderr.decode()
receipt={'schema':'single-unmodified-native-route-v1','started_utc':started,'finished_utc':finished,
         'elapsed_seconds':elapsed,'command':command,'cwd':str(RUN),'resolved_python3':shutil.which('python3'),
         'exit_code':completed.returncode,'stdout_file':'stdout.txt','stderr_file':'stderr.txt',
         'source_program_sha256':native_sha,'copy_program_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
         'source_and_initial_guards_before_after_exact':True,'native_route_attempts':1,
         'dependencies_installed':False,'interpreter_switches_or_retries':0,
         'entrypoint_and_all_own_called_bodies_personally_read_before_execution':True,
         'scope':'Published stabilization identities and rational regression points only; no nonpolynomiality proof by finite testing'}
(RUN/'EXECUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
