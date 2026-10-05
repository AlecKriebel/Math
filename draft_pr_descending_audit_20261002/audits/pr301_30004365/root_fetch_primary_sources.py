"""Actual read-only primary PDF fetches with full source/request/PID/streams."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,subprocess,sys
A=Path(__file__).parent;D=A/'source_evidence';R=Path('/Users/alec/Documents/Math');sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def main():
 assert not sys.flags.optimize;D.mkdir(exist_ok=False);rows=[]
 for label,url in [('owr2020-3','https://ems.press/content/serial-article-files/46842'),('aps2023-final','https://link.springer.com/content/pdf/10.1007/s00029-022-00822-x.pdf'),('ppp-arxiv','https://arxiv.org/pdf/1807.04730')]:
  q=D/label;q.mkdir();headers=q/'headers.raw';argv=['/usr/bin/curl','--fail','--location','--max-time','45','--silent','--show-error','--dump-header',str(headers),url];request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),source=pin(__file__),read_only=True,automatic_retry=False);(q/'request.json').write_text(json.dumps(request,indent=2)+'\n');(q/'source.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0));proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);start=dict(**request,actual_PID=proc.pid,start_UTC=utc());(q/'started.json').write_text(json.dumps(start,indent=2)+'\n');out,err=proc.communicate(timeout=50);streams={}
  for n,b in [('stdout',out),('stderr',err)]:
   p=q/(n+'.gz');p.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(p),logical_bytes=len(b),logical_sha256=sha(b))
  success=proc.returncode==0 and not err and out.startswith(b'%PDF-');record=dict(**start,end_UTC=utc(),exit_code=proc.returncode,parent_reaped=True,streams=streams,headers=pin(headers) if headers.exists() else None,complete_PDF_retrieved=success,failed_fetch_not_reclassified=not success);(q/'execution.json').write_text(json.dumps(record,indent=2)+'\n');p=None
  if success:p=q/(label+'.pdf');p.write_bytes(out);p.chmod(0o444)
  rows.append(dict(label=label,url=url,actual_PID=proc.pid,exit_code=proc.returncode,complete_PDF_retrieved=success,PDF=pin(p) if p else None,execution=pin(q/'execution.json')))
 result=dict(status='ACTUAL_PRIMARY_PDF_ACCESS_READBACK',UTC=utc(),actual_recorder_PID=os.getpid(),source=pin(__file__),results=rows,no_failed_fetch_claimed_complete=True);p=D/'FETCH_RESULTS.json';p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
