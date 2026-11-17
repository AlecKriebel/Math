"""Invoke exactly one ordered checkpoint step and retain its literal streams."""
import datetime,json,subprocess,sys,time
from pathlib import Path
if not __debug__:
    raise RuntimeError('Checkpoint assertions must be enabled')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/checkpoint-native145-fanoINITIAL-20261117')
steps=[('GUARDS_BEFORE','capture_guards.py','before'),('DRY_HELPER_WRAPPER','run_helper_once.py','dry-run'),('DRY_TREE_AUDIT','inspect_checkpoint.py','dry'),('PUSH_HELPER_WRAPPER','run_helper_once.py','push'),('POST_TREE_AUDIT','inspect_checkpoint.py','post'),('GUARDS_AFTER','capture_guards.py','after')]
assert len(sys.argv)==2 and sys.argv[1] in [x[0] for x in steps]
name=sys.argv[1];index=[x[0] for x in steps].index(name)
runfile=OWN/'RUNS.json'
runs=json.loads(runfile.read_bytes()) if runfile.exists() else []
assert len(runs)==index and all(x['exit_code']==0 for x in runs)
for ext in ['stdout','stderr']:assert not (OWN/(name+'.'+ext)).exists()
argv=[sys.executable,'-B',str(OWN/steps[index][1]),steps[index][2]]
started=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for ext,raw in [('stdout',r.stdout),('stderr',r.stderr)]:
    with (OWN/(name+'.'+ext)).open('xb') as f:f.write(raw)
row=dict(name=name,argv=argv,started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-tick,exit_code=r.returncode)
runs.append(row)
runfile.write_text(json.dumps(runs,indent=2)+'\n')
print(json.dumps(row));print('literal_stdout_bytes',len(r.stdout),'literal_stderr_bytes',len(r.stderr))
if r.returncode:print(r.stderr.decode(errors='replace'),file=sys.stderr)
raise SystemExit(r.returncode)
