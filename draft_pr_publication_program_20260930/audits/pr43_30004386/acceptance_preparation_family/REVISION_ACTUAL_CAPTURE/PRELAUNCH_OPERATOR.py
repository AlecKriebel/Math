"""Capture only this family's own authoring, private controls and closure reads."""
from pathlib import Path
import subprocess, sys, datetime, json, hashlib, os
H = Path(__file__).resolve().parent
name, member = sys.argv[1:3]
allowed = {'SOURCE_READING_ACTUAL_CAPTURE':'inspect_source_inputs.py',
           'AUTHORING_ACTUAL_CAPTURE':'author_sources.py',
           'REVISION_ACTUAL_CAPTURE':'repair_sources.py',
           'CONTROLS_ACTUAL_CAPTURE':'independent_source_controls.py',
           'CLOSURE_ACTUAL_CAPTURE':'close_owned_source.py'}
if name not in allowed or member != allowed[name]:
    raise ValueError('Own author/control/closure sources only')
source = H / member
if source.is_symlink() or not source.is_file(): raise ValueError('Regular own source required')
C = H/name; C.mkdir(exist_ok=False)
raw = source.read_bytes()
(C/'PRELAUNCH_SOURCE.py').write_bytes(raw)
(C/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
argv = [sys.executable, '-B', str(source)]; started = stamp()
with (C/'stdout.bin').open('xb') as out, (C/'stderr.bin').open('xb') as err:
    child = subprocess.Popen(argv, cwd=H, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
    code = child.wait()
finished = stamp(); streams = []
for n in ['stdout.bin', 'stderr.bin']:
    b = (C/n).read_bytes(); streams.append({'path':n,'bytes':len(b),'sha256':sha(b)})
record = {'schema':'pr43-own-source-operation-capture/v1','actual_execution':True,
          'completed':True,'parent_pid':os.getpid(),'pid':child.pid,'argv':argv,'cwd':str(H),
          'started_utc':started,'finished_utc':finished,'exit_code':code,
          'status':'PASS' if code==0 else 'FAIL','stdin_supplied':False,
          'source_sha256':sha(raw),'source_unchanged':source.read_bytes()==raw,
          'prelaunch_operator_sha256':sha((C/'PRELAUNCH_OPERATOR.py').read_bytes()),
          'stdout':streams[0],'stderr':streams[1],
          'proposed_acceptance_helpers_executed':False,'science_helpers_executed':False,
          'native_Git_remote_people_mutations':False}
(C/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record)); sys.exit(code)
