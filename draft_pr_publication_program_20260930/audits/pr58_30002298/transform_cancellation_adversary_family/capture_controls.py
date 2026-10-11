"""Capture this family's single exact-control program, with full streams."""
import datetime,hashlib,json,os,subprocess
from pathlib import Path

base=Path(__file__).resolve().parent
script=base/'controls.py'
before=script.read_bytes()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
command=['/Users/alec/Documents/Math/discotope_irreducibility_30005473/verification/.venv/bin/python','-B',str(script)]
child=subprocess.Popen(command,cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
out,err=child.communicate()
finish=datetime.datetime.now(datetime.timezone.utc).isoformat()
after=script.read_bytes()
(base/'controls.stdout.bin').write_bytes(out)
(base/'controls.stderr.bin').write_bytes(err)
receipt={'schema':'pr58-own-controls-capture/v1','operator':'transform_cancellation_adversary','capture_pid':os.getpid(),'child_pid':child.pid,'started_utc':start,'finished_utc':finish,'command':command,'cwd':str(base),'exit_code':child.returncode,'source_sha256_before':hashlib.sha256(before).hexdigest(),'source_sha256_after':hashlib.sha256(after).hexdigest(),'source_bytes':len(before),'source_unchanged':before==after,'stdout_bytes':len(out),'stderr_bytes':len(err),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest(),'ROOT_or_math_acceptance':False}
(base/'controls.CAPTURE.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'capture_pid':os.getpid(),'child_pid':child.pid,'exit_code':child.returncode,'stdout_bytes':len(out),'stderr_bytes':len(err)}))
raise SystemExit(child.returncode)
