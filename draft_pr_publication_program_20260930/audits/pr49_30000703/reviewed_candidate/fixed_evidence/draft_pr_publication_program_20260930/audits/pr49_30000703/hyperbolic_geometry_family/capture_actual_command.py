#!/usr/bin/python3
"""First-party actual capture. Never manufactures a child PID or receipts."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys, time

def identity(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--capture',required=True)
    a.add_argument('--cwd',required=True)
    a.add_argument('--source',action='append',default=[])
    a.add_argument('argv',nargs=argparse.REMAINDER)
    args=a.parse_args()
    argv=args.argv
    if argv and argv[0]=='--': argv=argv[1:]
    if not argv: raise ValueError('No command')
    out=pathlib.Path(args.capture).resolve()
    out.mkdir(parents=True,exist_ok=False)
    cwd=pathlib.Path(args.cwd).resolve()
    op=pathlib.Path(__file__).resolve()
    opcopy=out/'prelaunch_operator.py';opcopy.write_bytes(op.read_bytes());opcopy.chmod(0o444)
    sources=[]
    for i,name in enumerate(args.source):
        p=pathlib.Path(name).resolve()
        q=out/('prelaunch_source_%02d%s'%(i,p.suffix))
        q.write_bytes(p.read_bytes());q.chmod(0o444)
        sources.append({'original':identity(p),'copied':identity(q),'byte_identical':p.read_bytes()==q.read_bytes()})
    pre={'schema':'actual_command_prelaunch_v1','operator_pid':os.getpid(),'operator_parent_pid':os.getppid(),'prelaunch_utc':utc(),'argv':argv,'cwd':str(cwd),'operator':identity(op),'operator_copy':identity(opcopy),'sources':sources,'environment_policy':'Inherited; no environment values are dumped','streams':'Separate full raw bytes via PIPE.communicate'}
    (out/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
    started=utc();t=time.monotonic_ns()
    proc=subprocess.Popen(argv,cwd=str(cwd),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=proc.communicate()
    ended=utc();elapsed=time.monotonic_ns()-t
    (out/'stdout.bin').write_bytes(stdout);(out/'stderr.bin').write_bytes(stderr)
    cap={'schema':'actual_command_completed_v1','child_pid':proc.pid,'operator_pid':os.getpid(),'started_utc':started,'completed_utc':ended,'elapsed_monotonic_ns':elapsed,'argv':argv,'cwd':str(cwd),'returncode':proc.returncode,'capture_completed':True,'stdout':identity(out/'stdout.bin'),'stderr':identity(out/'stderr.bin'),'prelaunch':identity(out/'PRELAUNCH.json')}
    (out/'CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n')
    print(json.dumps({'capture':str(out),'child_pid':proc.pid,'returncode':proc.returncode,'stdout_bytes':len(stdout),'stderr_bytes':len(stderr)}))
    return proc.returncode

if __name__=='__main__': sys.exit(main())
