"""Execute only this family's newly authored inspector, saving actual evidence."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, subprocess, sys

D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def main():
    p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('script');a=p.parse_args()
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    assert a.name and '/' not in a.name and a.name not in ('.','..')
    s=D/a.script;assert s.parent==D and s.is_file() and not s.is_symlink()
    dest=D/a.name;dest.mkdir()
    source=s.read_bytes();operator=Path(__file__).read_bytes()
    (dest/'PRELAUNCH_SOURCE.py').write_bytes(source)
    (dest/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    argv=['/usr/bin/python3','-B',str(s)]
    rec={'schema':'PR43_V2_SOURCE_ADVERSARY_ACTUAL_OWN_CAPTURE_v1','argv':argv,
         'cwd':str(D),'actual_parent_pid':os.getpid(),'started_utc':utc(),
         'prelaunch_source_sha256':sha(source),'prelaunch_operator_sha256':sha(operator),
         'proposed_foreign_helpers_imported_compiled_executed':False}
    proc=subprocess.Popen(argv,cwd=D,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=proc.communicate()
    rec.update(actual_child_pid=proc.pid,actual_execution=True,completed_after_child_exit=True,
               exit_code=proc.returncode,finished_utc=utc(),source_unchanged=s.read_bytes()==source)
    for channel,raw in [('stdout',out),('stderr',err)]:
        name=channel+'.bin'
        with (dest/name).open('xb') as stream:
            stream.write(raw);stream.flush();os.fsync(stream.fileno())
        rec[channel]={'path':name,'bytes':len(raw),'sha256':sha(raw)}
    with (dest/'CAPTURE.json').open('x') as stream:
        json.dump(rec,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    print(json.dumps(rec,indent=2))
    return proc.returncode if rec['source_unchanged'] else 1
if __name__=='__main__':sys.exit(main())
