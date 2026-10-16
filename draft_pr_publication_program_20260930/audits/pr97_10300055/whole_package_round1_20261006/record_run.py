#!/usr/bin/env python3
import datetime,json,subprocess,time,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run(label,argv,cwd=None,expected=None):
 outdir=ROOT/'runs';outdir.mkdir(exist_ok=True)
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 p=subprocess.Popen(argv,cwd=cwd or ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 stdout,stderr=p.communicate()
 (outdir/(label+'.stdout.bin')).write_bytes(stdout);(outdir/(label+'.stderr.bin')).write_bytes(stderr)
 x={'label':label,'argv':argv,'cwd':str(cwd or ROOT),'PID':p.pid,'started_UTC':start,'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'exit_code':p.returncode,'expected_exit_code':expected,'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest()}
 f=outdir/'PROCESS_RECEIPTS.json';rows=json.loads(f.read_text()) if f.exists() else [];rows.append(x);f.write_text(json.dumps(rows,indent=2)+'\n')
 print(json.dumps(x));return p.returncode,stdout,stderr
if __name__=='__main__':run(sys.argv[1],sys.argv[2:])
