"""Portable full-payload and finite-control reproduction, never a novelty certificate."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,signal,subprocess,sys,threading,time
R=Path(__file__).resolve().parent
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
    assert not sys.flags.optimize and sys.flags.ignore_environment and sys.flags.dont_write_bytecode
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',required=True);args=parser.parse_args()
    outdir=Path(args.output_dir).absolute()
    assert outdir==outdir.resolve() and not outdir.is_relative_to(R),'New output directory must be outside the package'
    assert not outdir.exists(),'Existing output directory is not adopted or overwritten'
    manifest=json.loads((R/'MANIFEST.json').read_bytes())
    for name,w in manifest['payload'].items():
        p=R/name;assert p.is_file() and not p.is_symlink() and p.parent==R
        b=p.read_bytes();assert len(b)==w['bytes'] and sha(b)==w['sha256'],name
    expected=json.loads((R/'EXPECTED_SCIENTIFIC_OUTPUTS.json').read_bytes())
    outdir.mkdir(parents=True,exist_ok=False);results=[]
    cases=[('author','author_verify.py',[],0),('direct_chord','historical_independent.py',[],0),('self_contained_proof','proof_controls.py',[],0),('conventions','identity_controls.py',['positive'],0)]
    cases += [(case,'identity_controls.py',[case],1) for case in expected['mathematical_rejections']]
    for label,program,arguments,wanted in cases:
        d=outdir/label;d.mkdir();source=(R/program).read_bytes()
        command=[sys.executable,'-E','-B',str(R/program),*arguments]
        request=dict(actual_prelaunch_utc=utc(),actual_recorder_pid=os.getpid(),argv=command,cwd=str(R),source={'bytes':len(source),'sha256':sha(source)},timeout_seconds=30,expected_exit=wanted)
        save(d/'request.json',request)
        p=None;timer=None;out=err=b'';error=None;cleanup_errors=[];communicated=False;expired=threading.Event();started=time.monotonic()
        def kill():
            if p is not None:
                try:os.killpg(p.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                except BaseException as e:cleanup_errors.append('signal:'+repr(e))
        def timeout():expired.set();kill()
        try:
            p=subprocess.Popen(command,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
            timer=threading.Timer(30,timeout);timer.daemon=True;timer.start()
            save(d/'started.json',dict(actual_post_popen_utc=utc(),actual_pid=p.pid,process_group=p.pid))
            out,err=p.communicate(timeout=30)
            communicated=True
        except BaseException as e:
            error=repr(e)
            if isinstance(e,subprocess.TimeoutExpired):
                expired.set();out=e.output or out;err=e.stderr or err
        finally:
            if timer:timer.cancel()
            if p is not None:
                kill()
                if not communicated:
                    try:
                        out,err=p.communicate(timeout=5);communicated=True
                    except BaseException as e:
                        error=str(error)+';cleanup:'+repr(e)
                        if isinstance(e,subprocess.TimeoutExpired):
                            out=e.output or out;err=e.stderr or err
                        try:p.kill()
                        except BaseException as e:cleanup_errors.append('kill:'+repr(e))
                        try:p.wait(timeout=2)
                        except BaseException as e:error+=';reap:'+repr(e)
        if cleanup_errors:error=(error+';' if error else '')+';'.join(cleanup_errors)
        (d/'stdout.bin').write_bytes(out);(d/'stderr.bin').write_bytes(err)
        result={**request,'actual_reaped_utc':utc(),'actual_pid':None if p is None else p.pid,'exit':None if p is None else p.returncode,'reaped':p is not None and p.returncode is not None,'timed_out':expired.is_set(),'error':error,'cleanup_errors':cleanup_errors,'elapsed_seconds':time.monotonic()-started,'stdout':{'bytes':len(out),'sha256':sha(out)},'stderr':{'bytes':len(err),'sha256':sha(err)}}
        save(d/'execution.json',result);results.append(result)
        assert error is None and not expired.is_set() and p is not None and p.returncode==wanted,label
        if wanted==0:
            data=json.loads(out)
            for k,v in expected['positive'][label].items():assert data[k]==v,(label,k,data[k],v)
        else:
            assert not out and expected['mathematical_rejections'][label].encode() in err and b'AssertionError' in err,label
        assert source==(R/program).read_bytes(),'Control source changed'
    for name,w in manifest['payload'].items():
        b=(R/name).read_bytes();assert len(b)==w['bytes'] and sha(b)==w['sha256'],name
    summary=dict(status='PASS_PAYLOAD_INTEGRITY_AND_FINITE_CONTROLS',actual_completed_utc=utc(),actual_runner_pid=os.getpid(),successful_controls=4,expected_mathematical_rejections=5,full_process_results=results,infinite_theorem_proved_by_computation=False,novelty_certified=False,human_peer_review=False)
    save(outdir/'RESULT.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='full_process_results'},indent=2))
if __name__=='__main__':main()
