"""Bounded actual read-only command/private-replay capture for PR50 preparation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys
H = Path(__file__).resolve().parent
R = H.parents[2]
def stamp(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def put(p, b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
def enc(o): return (json.dumps(o, sort_keys=True, indent=2)+'\n').encode()
def capture(name, argv, cwd=R, source=None):
    assert name and '/' not in name and name not in {'.','..'}
    assert type(argv) is list and argv and all(type(x) is str for x in argv)
    d=H/'captures'/name;d.mkdir(parents=True)
    operator=Path(__file__).read_bytes();put(d/'prelaunch_operator.py',operator)
    pre={'schema':'pr50-bounded-prelaunch/v1','created_utc':stamp(),'operator_pid':os.getpid(),'cwd':str(cwd),'argv':argv,'operator_sha256':sha(operator),'child_source':None,'stdin_supplied':False}
    if source is not None:
        b=Path(source).read_bytes();put(d/'prelaunch_child_source.py',b);pre['child_source']={'path':str(source),'bytes':len(b),'sha256':sha(b)}
    put(d/'PRELAUNCH.json',enc(pre));start=stamp()
    child=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate();end=stamp()
    c={'schema':'pr50-bounded-actual-capture/v1','actual_execution':True,'completed':True,'operator_pid':os.getpid(),'child_pid':child.pid,'started_utc':start,'finished_utc':end,'cwd':str(cwd),'argv':argv,'exit_code':child.returncode,'status':'PASS' if child.returncode==0 else 'FAIL','operator_sha256':sha(operator),'operator_unchanged':Path(__file__).read_bytes()==operator,'child_source':pre['child_source']}
    for k,b in [('stdout',out),('stderr',err)]:
        put(d/(k+'.bin'),b);c[k]={'path':k+'.bin','bytes':len(b),'sha256':sha(b)}
    if source is not None: c['source_unchanged']=Path(source).read_bytes()==(d/'prelaunch_child_source.py').read_bytes()
    put(d/'CAPTURE.json',enc(c));return c,out,err
if __name__=='__main__':
    name=sys.argv[1];argv=sys.argv[2:];source=None
    if argv[0].endswith('gh') or argv[0]=='gh':
        assert (argv[1:3] in [['pr','view'],['pr','diff']] and argv[3]=='50') or (argv[1]=='api' and 'repos/AlecKriebel/Math/' in argv[2] and not any(x in argv for x in ['--method','-X','--input','--field','-f','-F']))
    else:
        assert argv[0].endswith('python3') and argv[1]=='-B'
        source=Path(argv[2]).resolve();assert H in source.parents
        assert source.name in {'snapshot_original.py','reproduce_original.py','selected_source_inventory.py','independent_math_checks.py'}
    c,out,err=capture(name,argv,source=source)
    print(json.dumps({'capture':name,'child_pid':c['child_pid'],'status':c['status'],'exit_code':c['exit_code'],'stdout_bytes':len(out),'stderr_bytes':len(err)},sort_keys=True))
    sys.exit(c['exit_code'])
