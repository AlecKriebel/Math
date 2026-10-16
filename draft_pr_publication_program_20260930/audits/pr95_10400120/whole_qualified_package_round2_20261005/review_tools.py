from pathlib import Path
import hashlib, json, os, subprocess, datetime, time
A=Path(__file__).resolve().parent
Q=A.parent/'qualified_publication_package_v2'
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def run(label,argv,cwd,inputs=()):
    folder=A/'processes'/label;folder.mkdir(parents=True)
    record={'label':label,'recorder_pid':os.getpid(),'argv':list(map(str,argv)), 'cwd':str(cwd),'started_utc':utc(),'inputs':[{'path':str(p),'sha256':sha(p),'bytes':Path(p).stat().st_size}for p in inputs]}
    began=time.monotonic()
    with (folder/'stdout.bin').open('wb')as out,(folder/'stderr.bin').open('wb')as err:
        child=subprocess.Popen(record['argv'],cwd=cwd,stdout=out,stderr=err,env={k:v for k,v in os.environ.items()if not k.startswith('PYTHON')})
        record['pid']=child.pid;dump(folder/'process.json',record)
        record['exit_code']=child.wait()
    record.update(ended_utc=utc(),elapsed_seconds=time.monotonic()-began)
    for name in ['stdout.bin','stderr.bin']:record[name]={'sha256':sha(folder/name),'bytes':(folder/name).stat().st_size}
    dump(folder/'process.json',record)
    print(label,record['pid'],record['exit_code'],flush=True)
    return record
