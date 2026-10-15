"""Capture actual serial source-only builder invocation; never runs integration."""
import datetime as dt,hashlib,json,subprocess,sys
from pathlib import Path
own=Path(__file__).resolve().parent;repo=own.parents[3];p=own/'private/source_build_capture_v2'
p.mkdir(parents=True,exist_ok=False)
script=own/'build_source_packet.py';(p/'PRELAUNCH_SOURCE.py').write_bytes(script.read_bytes())
argv=[sys.executable,'-B',str(script)];start=dt.datetime.now(dt.timezone.utc).isoformat()
child=subprocess.Popen(argv,cwd=repo,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
(p/'stdout.bin').write_bytes(out);(p/'stderr.bin').write_bytes(err)
x={'schema':'pr57-actual-source-builder-command-capture/v1','argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest(),'integration_helper_executed':False}
(p/'CAPTURE.json').write_text(json.dumps(x,indent=2)+'\n');print(out.decode(),end='');print(err.decode(),end='',file=sys.stderr);raise SystemExit(child.returncode)
