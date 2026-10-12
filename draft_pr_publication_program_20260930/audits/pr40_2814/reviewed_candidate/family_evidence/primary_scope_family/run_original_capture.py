#!/usr/bin/env python3
"""Capture the complete real original-audit process, preserving failed attempts."""
import argparse,datetime,hashlib,json,pathlib,subprocess,sys
AUDITOR_SHA = "5b4f6e0bfd5be4381057899d17dd7310b5957742b87ddfeecd57e9d97bd8489f"
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 a=argparse.ArgumentParser();a.add_argument('--repository-root',type=pathlib.Path,required=True);a.add_argument('--capture-root',type=pathlib.Path,required=True);x=a.parse_args();repo=x.repository_root.resolve();cap=x.capture_root.resolve();program=pathlib.Path(__file__).parent/'audit_original.py';b=program.read_bytes()
 if hashlib.sha256(b).hexdigest()!=AUDITOR_SHA:raise ValueError('auditor source pin mismatch')
 if cap.exists():raise FileExistsError(cap)
 cap.mkdir(parents=True,exist_ok=False);argv=['/usr/bin/python3',str(program.resolve()),'--repository-root',str(repo),'--output-root',str(cap/'results')];d={'schema':'pr40-original-audit-outer-capture/v1','started_utc':utc(),'argv':argv,'cwd':str(repo),'program':{'sha256':AUDITOR_SHA,'size':len(b)},'attempted':True,'timeout_seconds':90,'returncode':None}
 try:
  r=subprocess.run(argv,cwd=repo,capture_output=True,timeout=90);stdout,stderr=r.stdout,r.stderr;d.update(returncode=r.returncode,status='PASS' if r.returncode==0 else 'FAILED')
 except subprocess.TimeoutExpired as e:
  stdout,stderr=e.stdout or b'',e.stderr or b'';d.update(status='TIMEOUT',error_type=type(e).__name__,error=str(e))
 except OSError as e:
  stdout,stderr=b'',b'';d.update(status='LAUNCH_FAILED',attempted=False,error_type=type(e).__name__,error=str(e))
 for name,b in [('stdout',stdout),('stderr',stderr)]:
  (cap/(name+'.bin')).write_bytes(b);d[name]={'path':name+'.bin','size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 d['finished_utc']=utc();d['capture_runtime']={'executable':sys.executable,'version':sys.version};(cap/'CAPTURE.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({'status':d['status'],'returncode':d['returncode'],'capture':str(cap/'CAPTURE.json')}));return 0 if d['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
