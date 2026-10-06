"""Log actual processes and store output only in corrected_v2 private custody."""
from pathlib import Path
import sys,subprocess,os,datetime,json,hashlib
B=Path(__file__).resolve().parent
label=sys.argv[1];argv=sys.argv[2:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate()
(B/'_private'/(label+'.stdout')).write_bytes(out)
(B/'_private'/(label+'.stderr')).write_bytes(err)
c={'label':label,'UTC_started':start,'UTC_finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'child_PID':p.pid,'argv':argv,'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()}
with (B/'CLI_LEDGER.jsonl').open('a') as f:f.write(json.dumps(c)+'\n')
print(json.dumps(c))
raise SystemExit(p.returncode)
