"""Only literal copies in owned directories; duplicates remain duplicates."""
from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, sys, traceback
F=Path(__file__).absolute().parent; C=F.parent/'reviewed_candidate'
assert __debug__ and not sys.flags.optimize
def sha(b): return hashlib.sha256(b).hexdigest()
def enc(x): return (json.dumps(x,indent=2,allow_nan=False)+'\n').encode()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
caps=[]; results={}
spec=[('author','verify.py','verification.json',114),('duplicate','review/submitted_verify.py','review/submitted_results.json',114),('historical_independent','review/independent_checks.py','review/independent_results.json',100)]
for label,sn,rn,count in spec:
    d=F/'private_literal_replay'/label; d.mkdir(parents=True,exist_ok=False)
    original=(C/sn).read_bytes(); src=d/Path(sn).name; src.write_bytes(original)
    (d/'PRELAUNCH_SOURCE.py').write_bytes(original)
    (d/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
    rec={'schema':'pr47-whole-independent-literal-helper-actual-capture/v1','operator_pid':os.getpid(),'argv':['/usr/bin/python3','-B',str(src)],'cwd':str(F),'started_utc':utc(),'source_sha256':sha(original),'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False}
    (d/'PRELAUNCH.json').write_bytes(enc(rec))
    try:
        with (d/'stdout.bin').open('xb') as out,(d/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(rec['argv'],cwd=F,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,PYTHONOPTIMIZE='0',GIT_OPTIONAL_LOCKS='0'))
            rec.update(actual_execution=True,pid=child.pid)
            try: rec['exit_code']=child.wait(timeout=120); rec['completed']=True
            except BaseException: child.kill(); rec['exit_code']=child.wait(); raise
    except BaseException: rec['failure']=traceback.format_exc(); raise
    finally:
        rec['finished_utc']=utc()
        for k in ['stdout','stderr']:
            p=d/(k+'.bin')
            if p.exists(): b=p.read_bytes(); rec[k]={'path':p.relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)}
        rec['source_unchanged']=src.read_bytes()==original and (C/sn).read_bytes()==original
        (d/'CAPTURE.json').write_bytes(enc(rec)); caps.append(rec)
    assert rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code']==0 and rec['source_unchanged'] is True and (d/'stderr.bin').read_bytes()==b''
    body=(d/Path(rn).name).read_bytes(); saved=(C/rn).read_bytes()
    assert body==saved and equal(json.loads(body),json.loads(saved))
    o=json.loads(body)
    if label!='historical_independent': assert o['passed'] is True and type(o['assertions']) is int and o['assertions']==count and len(o['checks'])==count
    else: assert type(o['passed']) is int and o['passed']==100 and type(o['failed']) is int and o['failed']==0 and len(o['checks'])==100
    results[label]=o
assert (C/'verify.py').read_bytes()==(C/'review/submitted_verify.py').read_bytes()
assert equal(results['author'],results['duplicate'])
result={'schema':'pr47-whole-independent-literal-helper-replay/v1','actual_pid':os.getpid(),'utc':utc(),'status':'PASS_COMPLETE_BYTE_AND_RECURSIVE_TYPE_IDENTITY','author_checks':114,'duplicate_checks':114,'historical_independent_checks':100,'duplicate_is_independent':False,'complete_actual_captures':caps,'entire_results':results,'target_solved':False,'future_acceptance_approved':False}
(F/'ORIGINAL_REPLAY_RESULT.json').write_bytes(enc(result))
print(json.dumps({k:result[k] for k in ['status','actual_pid','author_checks','duplicate_checks','historical_independent_checks','duplicate_is_independent']}))
