#!/usr/bin/env python3
"""Private read-only retrieval/replay capture. No stdin or shell execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent
def utc():return datetime.now(timezone.utc).isoformat()
def info(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(name,argv,cwd=None,sources=()):
    root=HERE/'captures'/name;root.mkdir(parents=True,exist_ok=False)
    operator=Path(__file__).resolve().read_bytes()
    (root/'operator_prelaunch.py').write_bytes(operator)
    inputs=[]
    for i,p in enumerate(sources):
        p=Path(p);b=p.read_bytes();saved=root/('source_prelaunch_'+str(i)+p.suffix)
        saved.write_bytes(b);inputs.append({'original':str(p),'saved':str(saved),**info(b),
                                         'mode_at_prelaunch':format(p.stat().st_mode&0o7777,'04o')})
    cwd=str(cwd or HERE);start=utc()
    with (root/'stdout.bin').open('wb') as out,(root/'stderr.bin').open('wb') as err:
        p=subprocess.Popen(argv,cwd=cwd,stdout=out,stderr=err)
        pid=p.pid;code=p.wait()
    end=utc();stdout=(root/'stdout.bin').read_bytes();stderr=(root/'stderr.bin').read_bytes()
    cap={'schema':'pr54-private-command-capture/v1','argv':argv,'cwd':cwd,
         'operator_pid':os.getpid(),'child_pid':pid,'utc_start':start,'utc_end':end,
         'exit_code':code,'operator':info(operator),'operator_unchanged_after':Path(__file__).resolve().read_bytes()==operator,
         'sources':inputs,'sources_unchanged_after':all(Path(q['original']).read_bytes()==Path(q['saved']).read_bytes() for q in inputs),
         'stdout':info(stdout),'stderr':info(stderr),'ROOT_approval':False,
         'native_Git_ref_or_remote_mutation':False}
    (root/'CAPTURE.json').write_text(json.dumps(cap,indent=2,sort_keys=True)+'\n')
    return cap,stdout,stderr
if __name__=='__main__':
    name=sys.argv[1];argv=sys.argv[2:]
    if not argv:raise SystemExit('literal command argv required')
    cap,out,err=run(name,argv)
    print(json.dumps(cap,indent=2,sort_keys=True))
    sys.exit(cap['exit_code'])
