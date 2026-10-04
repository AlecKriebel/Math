"""Capture only the fixed own read-only operator; no compressor invocation."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
N=Path(__file__).absolute().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(q,b):
 with q.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
def ref(q):
 b=q.read_bytes();return dict(path=str(q),bytes=len(b),sha256=sha(b),full_mode_07777=oct(stat.S_IMODE(q.stat().st_mode)))
def main():
 if not __debug__:raise RuntimeError('No optimized SOURCE capture')
 capdir=N/'actual_readback_capture';capdir.mkdir(exist_ok=False)
 operator=N/'readback_only.py';save(capdir/'prelaunch_operator.py',operator.read_bytes())
 helpers=[]
 for name,q in [('prelaunch_reviewed_V3.py',N.parent/'compress_completed_v3.py'),('prelaunch_reviewed_V4.py',N.parent/'v4_preparation/compress_completed_v4.py')]:
  save(capdir/name,q.read_bytes());helpers.append(ref(capdir/name))
 argv=[sys.executable,'-B',str(operator)];start=now()
 child=subprocess.Popen(argv,cwd=N.parents[2],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=child.communicate();end=now();save(capdir/'stdout.bin',out);save(capdir/'stderr.bin',err)
 record=dict(schema='storage-preparer-actual-readonly-readback-capture/v1',operator_role='SOURCE_PREPARER_NOT_ROOT',actual_execution=True,
  actual_controller_pid=os.getpid(),pid=child.pid,argv=argv,cwd=str(N.parents[2]),started_utc=start,finished_utc=end,
  completed=True,exit_code=child.returncode,prelaunch_operator=ref(capdir/'prelaunch_operator.py'),reviewed_helper_prelaunch_copies=helpers,
  stdout=ref(capdir/'stdout.bin'),stderr=ref(capdir/'stderr.bin'),operator_unchanged=sha(operator.read_bytes())==sha((capdir/'prelaunch_operator.py').read_bytes()),
  ROOT_personal_readback_or_approval=False,compression_native_Git_or_remote_mutation=False)
 save(capdir/'CAPTURE.json',(json.dumps(record,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(record,sort_keys=True,indent=2))
 if child.returncode:raise RuntimeError('Actual readonly child failed; complete streams retained')
if __name__=='__main__':main()
