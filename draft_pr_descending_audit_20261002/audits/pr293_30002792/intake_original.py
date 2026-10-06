"""Preserve the submitted PR293 artifact; readonly GitHub access only."""
from pathlib import Path
from datetime import datetime,timezone
import base64,gzip,hashlib,json,os,signal,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];HEAD='6e717193f93c8a321cce1ce35a00eed1ecfb56e7';PREFIX='unsolved_math_prioritization/attempts/30002792/';Q='unsolved_math_prioritization/QUEUE.md'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def need(x,m):
    if not x:raise RuntimeError(m)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=p.stat().st_mode&511)
def main():
    need(not sys.flags.optimize,'unoptimized');C=A/'intake_native';C.mkdir(exist_ok=False);(C/'SOURCE_PRELAUNCH.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0));count=0
    def run(argv):
        nonlocal count
        count+=1;c=C/str(count);c.mkdir();q=dict(argv=argv,cwd=str(R),UTC=utc(),actual_recorder_PID=os.getpid(),source=pin(Path(__file__)),read_only=True);(c/'request.json').write_text(json.dumps(q,indent=2)+'\n')
        proc=None;out=err=b'';failure=None;complete=False
        try:
            proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            try:
                (c/'started.json').write_text(json.dumps(dict(UTC=utc(),actual_PID=proc.pid),indent=2)+'\n');out,err=proc.communicate(timeout=55);complete=True
            except BaseException:
                try:os.killpg(proc.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                out,err=proc.communicate(timeout=5);complete=True;raise
        except BaseException as ex:failure=dict(type=type(ex).__name__,message=str(ex))
        streams={}
        for n,b in [('stdout',out),('stderr',err)]:
            z=c/(n+'.gz');z.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(z),bytes=len(b),sha256=sha(b))
        (c/'execution.json').write_text(json.dumps(dict(**q,end_UTC=utc(),actual_PID=proc.pid if proc else None,exit_code=proc.returncode if proc else None,parent_reaped=proc is not None and proc.poll() is not None,complete_streams=complete,failure=failure,streams=streams),indent=2)+'\n')
        need(failure is None and complete and proc.returncode==0,'complete actual readonly request');return json.loads(out),c
    pr,pc=run(['/opt/homebrew/bin/gh','pr','view','293','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefName,headRefOid,title,url,body,files'])
    need(pr['number']==293 and pr['state']=='OPEN' and pr['isDraft'] and pr['headRefOid']==HEAD,'exact eligible original draft')
    paths=[x['path'] for x in pr['files']];need(len(paths)==19 and len(set(paths))==19 and all(x==Q or x.startswith(PREFIX) for x in paths),'all19 exact scoped submitted changes')
    snap=A/'snapshot';snap.mkdir();files=[]
    for rel in paths:
        data,c=run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/contents/'+rel+'?ref='+HEAD]);need(data['encoding']=='base64','complete contents response');b=base64.b64decode(data['content']);need(len(b)==data['size'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==data['sha'],'native complete body size/blob')
        p=snap/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o444);files.append(dict(path=rel,snapshot=pin(p),git_blob=data['sha'],native_capture=str(c)))
    queue=(snap/Q).read_bytes();rows=[b for b in queue.splitlines() if len(b.split(b'|'))>11 and b.split(b'|')[2].strip().split(b' / ')[0]==b'30002792'];need(len(rows)==1 and rows[0].split(b'|')[8].strip()==b'claimed_solved' and rows[0].split(b'|')[9].strip()==b'2/5','submitted exact claimed_solved2/5')
    record=dict(status='PRESERVED_ELIGIBLE_ORIGINAL_PR293_SUBMISSION',UTC=utc(),actual_ROOT_PID=os.getpid(),source=pin(Path(__file__)),PR=293,problem_id='30002792',head=HEAD,original_submitted_status='claimed_solved',original_author_budget='2/5',native_PR=pr,native_PR_capture=str(pc),exact_original_QUEUE_row=rows[0].decode(),files=files,mathematical_acceptance=False,priority_acceptance=False,paper=False,DOI=None,tracker=False,merged=False,closed=False,estimates_percent=dict(mathematical_review=0,priority_audit=0,PR293_workflow=5),overall_goal_complete=False)
    p=A/'snapshot_manifest.json';p.write_text(json.dumps(record,indent=2)+'\n');p.chmod(0o444)
    (A/'RESEARCH_LOG.md').write_text(f"# PR293: gap-one line configurations\n\n{utc()} — Mathematics0%, priority0%, workflow5%: Preserved exact original draft head{HEAD}, all19 native submitted changed-file bodies and complete original QUEUE row claimed_solved2/5. Original target is arbitrary characteristic non-ACM gap-one line configurations. The submitted full-resolution claim remains a hypothesis requiring source-statement validation, independent proof audits and fresh adversarial reproduction. No acceptance or external publication action.\n")
    print(json.dumps(dict(status=record['status'],manifest=pin(p),files=len(files)),indent=2))
if __name__=='__main__':main()
