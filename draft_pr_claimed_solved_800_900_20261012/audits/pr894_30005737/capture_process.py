#!/usr/bin/env python3
"""Capture actual process evidence before interpreting outcomes; no acceptance supplied."""
import argparse,base64,datetime,hashlib,json,os
from pathlib import Path
import stat,subprocess,sys,time,zlib

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(raw): return {"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
def save(path,raw):
    with path.open("xb") as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())
def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("--stem",type=Path,required=True);ap.add_argument("--cwd",type=Path,required=True)
    ap.add_argument("--timeout",type=int,default=180);ap.add_argument("command",nargs=argparse.REMAINDER)
    a=ap.parse_args();cmd=a.command[1:] if a.command[:1]==["--"] else a.command
    if not cmd or a.timeout<=0:raise ValueError("command and positive timeout required")
    parent=a.stem.absolute().parent
    for p in (parent,*parent.parents):
        if not stat.S_ISDIR(p.lstat().st_mode):raise ValueError("ordinary nonsymlink capture parent required")
    paths={kind:Path(str(a.stem)+"."+suffix) for kind,suffix in [("stdout","stdout.bin"),("stderr","stderr.bin"),("meta","json")]}
    if any(p.exists() or p.is_symlink() for p in paths.values()):raise ValueError("capture outputs must be fresh")
    env=os.environ.copy();removed=sorted(k for k in env if k.startswith("PYTHON") or k=="__PYVENV_LAUNCHER__")
    for k in removed:env.pop(k,None)
    if cmd[0]=="__SELECTED_PYTHON__":cmd[0]=sys.executable
    meta={"started_utc":now(),"command":cmd,"cwd":str(a.cwd),"removed_environment_keys":removed}
    t=time.monotonic_ns();proc=None;expired=False
    try:
        proc=subprocess.Popen(cmd,cwd=a.cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        meta["launched_utc"]=now()
        try:out,err=proc.communicate(timeout=a.timeout)
        except subprocess.TimeoutExpired:
            expired=True;proc.kill();out,err=proc.communicate()
        meta.update(pid=proc.pid,returncode=proc.returncode)
    except OSError as exc:
        if proc is not None:
            proc.kill();out,err=proc.communicate();meta.update(pid=proc.pid,returncode=proc.returncode,postlaunch_error=repr(exc))
        else:
            out=b"";err=str(exc).encode();meta.update(pid=None,returncode=None,launched_utc=None,launch_error=repr(exc))
    meta.update(ended_utc=now(),elapsed_monotonic_ns=time.monotonic_ns()-t,timeout=expired,stdout=pin(out),stderr=pin(err))
    raw=(json.dumps(meta,indent=2,sort_keys=True)+"\n").encode()
    try:
        save(paths["stdout"],out);save(paths["stderr"],err);save(paths["meta"],raw)
    except OSError as exc:
        fallback=json.dumps({"metadata":meta,"stdout_base64":base64.b64encode(out).decode(),"stderr_base64":base64.b64encode(err).decode()},sort_keys=True).encode()
        print(json.dumps({"status":"CAPTURE_PERSISTENCE_FAILED","error":repr(exc),"actual_returncode":meta["returncode"],"lossless_evidence_zlib_base64":base64.b64encode(zlib.compress(fallback,9)).decode()}));return 3
    print(json.dumps({"status":"ACTUAL_PROCESS_CAPTURED","pid":meta["pid"],"returncode":meta["returncode"],"timeout":expired,"stdout":meta["stdout"],"stderr":meta["stderr"]},sort_keys=True))
    return 124 if expired else (meta["returncode"] if meta["returncode"] is not None else 127)
if __name__=="__main__":sys.exit(main())
