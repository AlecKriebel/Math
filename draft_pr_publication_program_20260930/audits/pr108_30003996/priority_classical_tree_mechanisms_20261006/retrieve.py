from pathlib import Path
import subprocess,datetime,hashlib,json,os,sys
BASE=Path(__file__).resolve().parent
PRIV=BASE/'_private'; PRIV.mkdir(exist_ok=True); PRIV.chmod(0o700)
def run(label,argv):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    (PRIV/(label+'.stdout')).write_bytes(out)
    (PRIV/(label+'.stderr')).write_bytes(err)
    rec={'label':label,'UTC_started':start,'UTC_finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'child_PID':p.pid,'argv':argv,'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest()}
    with (BASE/'CLI_LEDGER.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
    print(json.dumps(rec))
    if p.returncode:sys.exit(p.returncode)
if __name__=='__main__':run(sys.argv[1],sys.argv[2:])
