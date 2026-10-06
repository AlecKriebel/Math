import datetime, hashlib, json, os, pathlib, shutil, subprocess, sys

BASE = pathlib.Path(__file__).resolve().parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    p = pathlib.Path(p)
    b = p.read_bytes()
    return {'path':str(p), 'resolved_path':str(p.resolve()), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest(), 'mode':oct(p.stat().st_mode & 0o7777)}

def main():
    label, *argv = sys.argv[1:]
    if not label or not argv or '/' in label: raise ValueError('literal unique label and argv required')
    out = BASE/'native_captures'/label
    out.mkdir()
    source = pathlib.Path(__file__).resolve()
    saved = out/'launcher_source.py'
    saved.write_bytes(source.read_bytes()); saved.chmod(0o444)
    executable = pathlib.Path(shutil.which(argv[0]) or argv[0]).resolve()
    before = {'capture_version':1, 'launcher_pid':os.getpid(), 'launcher_argv':sys.argv, 'launcher_source':pin(source), 'retained_launcher_source':pin(saved), 'launcher_python':pin(pathlib.Path(sys.executable).resolve()), 'runtime':{'version':sys.version, 'optimization':sys.flags.optimize, 'stdlib_modules':[pin(pathlib.Path(m.__file__)) for m in (json,subprocess,hashlib,shutil) if getattr(m,'__file__',None)]}, 'child_executable':pin(executable), 'argv':argv, 'cwd':str(BASE), 'started_utc':now()}
    try:
        child = subprocess.Popen(argv, cwd=BASE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        before['actual_child_pid'] = child.pid
        stdout, stderr = child.communicate()
        before['exit_code'] = child.returncode
    except Exception as exc:
        before.update({'pre_Popen_failure':repr(exc), 'actual_child_pid':None, 'exit_code':None})
        stdout, stderr = b'', repr(exc).encode()
    (out/'stdout.bin').write_bytes(stdout); (out/'stderr.bin').write_bytes(stderr)
    before['completed_utc'] = now()
    before['stdout'] = pin(out/'stdout.bin'); before['stderr'] = pin(out/'stderr.bin')
    (out/'execution.json').write_text(json.dumps(before,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'label':label,'pid':before.get('actual_child_pid'),'exit_code':before['exit_code'],'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),'capture':str(out/'execution.json')}))
    return 0 if before['exit_code']==0 else 1
if __name__ == '__main__': sys.exit(main())
