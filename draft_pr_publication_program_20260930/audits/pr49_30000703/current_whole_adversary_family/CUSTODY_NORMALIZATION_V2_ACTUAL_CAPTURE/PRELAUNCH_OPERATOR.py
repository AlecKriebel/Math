"""Capture only explicitly selected private review programs; no production entrypoints."""
import sys, json, subprocess, os, hashlib
from pathlib import Path
from datetime import datetime, timezone
F = Path(__file__).resolve().parent
R = F.parents[3]
def now(): return datetime.now(timezone.utc).isoformat()
def ref(p):
    b=p.read_bytes()
    return {'path':str(p.relative_to(R)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest(), 'full_mode':p.stat().st_mode & 0o7777}
label, source = sys.argv[1:3]
assert label.isidentifier()
p = Path(source).resolve()
assert p.is_relative_to(F) and p.suffix == '.py' and not p.is_symlink()
d = F / label
d.mkdir(exist_ok=False)
operator = Path(__file__).read_bytes()
(d/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
(d/'PRELAUNCH_SOURCE.py').write_bytes(p.read_bytes())
argv=['/usr/bin/python3','-B',str(p),*sys.argv[3:]]
q={'schema':'pr49-whole-private-actual-capture/v1','operator_pid':os.getpid(), 'argv':argv,'cwd':str(R),'started_utc':now(),'source':ref(p),'operator':ref(Path(__file__)), 'stdin_supplied':False, 'actual_execution':True}
if 'from review_common import' in p.read_text():
    common=F/'review_common.py'
    (d/'PRELAUNCH_COMMON.py').write_bytes(common.read_bytes())
    q['prelaunch_dependencies']=[ref(common)]
(d/'PRELAUNCH.json').write_text(json.dumps(q,indent=2)+'\n')
with (d/'stdout.bin').open('wb') as out, (d/'stderr.bin').open('wb') as err:
    child = subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
    q['pid']=child.pid
    q['exit_code']=child.wait()
q.update(completed=True,finished_utc=now(),source_unchanged=(ref(p)==q['source']),operator_unchanged=(Path(__file__).read_bytes()==operator),stdout=ref(d/'stdout.bin'),stderr=ref(d/'stderr.bin'))
(d/'CAPTURE.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps({'capture':str(d.relative_to(R)), 'pid':child.pid,'exit_code':q['exit_code']}))
sys.exit(q['exit_code'])
