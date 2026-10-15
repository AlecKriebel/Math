"""One bounded exact existing-branch correction phase capture; never retry or relabel failure.

Retain native raw streams on every catchable postlaunch error. Host loss,
SIGKILL and unwritable storage may prevent a final record; started/request/raw
files then constitute uncertain recovery evidence, never success evidence.
"""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,signal,stat,subprocess,sys,time,traceback
W=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math')
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(p):
    p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def contain(child,d):
    # Inner children have separate sessions. Inventory before stopping root,
    # retain observed descendants, and explicitly qualify unobserved groups.
    seen={child.pid};groups={child.pid};errors=[];captures=[]
    for attempt in range(2):
        p=None
        try:
            p=subprocess.Popen(['/bin/ps','-axo','pid=,ppid=,pgid='],stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            try:out,err=p.communicate(timeout=3)
            except BaseException:
                os.killpg(p.pid,signal.SIGKILL);out,err=p.communicate(timeout=3);raise
            (d/('containment_ps_'+str(attempt)+'.stdout')).write_bytes(out)
            (d/('containment_ps_'+str(attempt)+'.stderr')).write_bytes(err)
            captures.append(dict(actual_PID=p.pid,exit_code=p.returncode,stdout_bytes=len(out),stdout_sha256=sha(out),stderr_bytes=len(err),stderr_sha256=sha(err)))
            need(p.returncode==0,'process inventory failed')
            rows=[tuple(map(int,line.split())) for line in out.splitlines() if line.strip()]
            changed=True
            while changed:
                before=len(seen);seen.update(pid for pid,ppid,pgid in rows if ppid in seen);changed=len(seen)!=before
            groups.update(pgid for pid,ppid,pgid in rows if pid in seen and pgid>0 and pgid!=os.getpgrp())
        except BaseException as e:errors.append('inventory: '+type(e).__name__+': '+str(e))
        for group in sorted(groups,reverse=True):
            try:os.killpg(group,signal.SIGTERM if attempt==0 else signal.SIGKILL)
            except ProcessLookupError:pass
            except BaseException as e:errors.append('contain group: '+type(e).__name__+': '+str(e))
        try:child.wait(timeout=3)
        except subprocess.TimeoutExpired:pass
        except BaseException as e:errors.append('reap: '+type(e).__name__+': '+str(e))
    if child.poll() is None:
        try:child.kill();child.wait(timeout=3)
        except BaseException as e:errors.append('final reap: '+type(e).__name__+': '+str(e))
    alive=[]
    for group in sorted(groups):
        try:os.killpg(group,0);alive.append(group)
        except ProcessLookupError:pass
        except BaseException as e:errors.append('verify group: '+type(e).__name__+': '+str(e))
    return dict(observed_descendant_PIDs=sorted(seen),observed_process_groups=sorted(groups),remaining_observed_process_groups=alive,errors=errors,inventory_captures=captures,parent_reaped=child.poll() is not None,unobserved_descendant_absence_certified=False)
def main():
    need(not sys.flags.optimize,'unoptimized launcher')
    need(sys.argv[1:]==['finish_metadata'],'explicit correction phase');phase='metadata_completion'
    operator=W/'integrate_correction.py';plan=W/'PLAN.json';clear=W/'ROOT_BRANCH_CORRECTION_CLEARANCE.json'
    need(pin(operator)['sha256']=='7f52beff29b3e11336b7e95d7b5bebe1394c5338826662abe78c238d4fd3024e' and pin(operator)['mode']==0o444,'exact immutable operator')
    need(pin(plan)['mode']==0o444,'immutable plan; exact body is bound by frozen ROOT clearance below')
    c=json.loads(clear.read_bytes());need(c['status']=='ROOT_CLEARS_EXACT_PR301_STALE_API_METADATA_COMPLETION' and c['source']==pin(operator) and c['plan']==pin(plan) and c['unresolved_issues']==[] and pin(clear)['mode']==0o444,'frozen ROOT grant')
    need(c['launcher']==pin(__file__),'exact launcher bound by ROOT')
    d=W/('actual_correction_'+phase+'_outer');d.mkdir(exist_ok=False)
    inputs=[]
    for p in [Path(__file__),operator,plan,clear]:
        q=d/(p.name+'.prelaunch.gz');q.write_bytes(gzip.compress(p.read_bytes(),mtime=0));inputs.append(dict(input=pin(p),stored=pin(q)))
    request=dict(argv=['/opt/homebrew/bin/python3','-E','-B',str(operator),'finish_metadata'],cwd=str(R),UTC=utc(),
                 actual_launcher_PID=os.getpid(),launcher=pin(__file__),full_prelaunch_inputs=inputs,automatic_retry=False,total_operator_timeout_seconds=900,native_raw_streams_retained=True)
    (d/'request.json').write_text(json.dumps(request,indent=2)+'\n')
    child=None;started=None;failure=None;containment=None;streams={};errors=[];interrupt=[]
    previous={s:signal.getsignal(s) for s in (signal.SIGINT,signal.SIGTERM)}
    def interrupted(signum,frame):interrupt.append(dict(signal=signum,UTC=utc()))
    for s in previous:signal.signal(s,interrupted)
    try:
        with (d/'stdout.native').open('xb',buffering=0) as outfd,(d/'stderr.native').open('xb',buffering=0) as errfd:
            try:
                child=subprocess.Popen(request['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=outfd,stderr=errfd,start_new_session=True)
                started=dict(actual_operator_PID=child.pid,start_UTC=utc());(d/'started.json').write_text(json.dumps(started,indent=2)+'\n')
                deadline=time.monotonic()+request['total_operator_timeout_seconds']
                while child.poll() is None:
                    if interrupt:raise RuntimeError('capture interrupted; outcome uncertain')
                    if time.monotonic()>=deadline:raise TimeoutError('bounded correction-phase wait expired')
                    try:child.wait(timeout=min(1,max(0.01,deadline-time.monotonic())))
                    except subprocess.TimeoutExpired:pass
            except BaseException as e:failure=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc(),UTC=utc())
            finally:
                if child is not None and (failure is not None or child.poll() is None or child.poll()!=0):
                    try:containment=contain(child,d)
                    except BaseException as e:errors.append('containment: '+type(e).__name__+': '+str(e))
                for fd in (outfd,errfd):
                    try:os.fsync(fd.fileno())
                    except BaseException as e:errors.append('raw fsync: '+type(e).__name__+': '+str(e))
    except BaseException as e:
        if failure is None:failure=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc(),UTC=utc())
        if child is not None and child.poll() is None:
            try:containment=contain(child,d)
            except BaseException as e:errors.append('outer containment: '+type(e).__name__+': '+str(e))
    finally:
        for label in ('stdout','stderr'):
            try:
                raw=d/(label+'.native');b=raw.read_bytes();row=dict(raw=pin(raw),logical_bytes=len(b),logical_sha256=sha(b),complete_through_operator_exit=child is not None and child.poll() is not None,unobserved_descendant_stream_closure_certified=False)
                streams[label]=row
                try:q=d/(label+'.gz');q.write_bytes(gzip.compress(b,mtime=0));row['stored']=pin(q)
                except BaseException as e:errors.append(label+' compression: '+type(e).__name__+': '+str(e))
            except BaseException as e:errors.append(label+' raw read: '+type(e).__name__+': '+str(e))
        record=dict(**request,actual_operator_PID=child.pid if child is not None else None,start_UTC=started['start_UTC'] if started else None,end_UTC=utc(),exit_code=child.poll() if child is not None else None,parent_reaped=child is not None and child.poll() is not None,streams=streams,failure=failure,interruptions=interrupt,containment=containment,capture_errors=errors,failed_or_uncertain_execution_not_reclassified=bool(failure or interrupt or errors or child is None or child.poll()!=0))
        record['status']='ACTUAL_BRANCH_CORRECTION_OUTER_FAILED_OR_UNCERTAIN' if record['failed_or_uncertain_execution_not_reclassified'] else 'ACTUAL_BRANCH_CORRECTION_OUTER_COMPLETED'
        try:(d/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
        except BaseException as e:
            record['status']='ACTUAL_BRANCH_CORRECTION_OUTER_FAILED_OR_UNCERTAIN';record['failed_or_uncertain_execution_not_reclassified']=True;record['final_record_persistence_error']=type(e).__name__+': '+str(e)
        print(json.dumps(record,indent=2))
        for s,handler in previous.items():signal.signal(s,handler)
    if record['failed_or_uncertain_execution_not_reclassified']:return child.returncode if child is not None and child.returncode not in (None,0) else 1
    return 0
if __name__=='__main__':sys.exit(main())
