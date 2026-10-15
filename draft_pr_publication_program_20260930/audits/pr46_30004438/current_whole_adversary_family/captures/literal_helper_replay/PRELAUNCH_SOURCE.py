"""Rerun byte-literal helpers only in owned private output directories."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
F=Path(__file__).absolute().parent;A=F.parent;C=A/'reviewed_candidate'
assert __debug__ and not sys.flags.optimize
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(x):return (json.dumps(x,indent=2,allow_nan=False)+'\n').encode()
def equal(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 return a==b
captures=[]
for label,source_name,result_name,count in [('author','verify.py','verification.json',51),('historical_independent','independent_review/independent_checks.py','independent_review/independent_results.json',848)]:
 d=F/'private_original_replay'/label;d.mkdir(parents=True,exist_ok=False)
 original=(C/source_name).read_bytes();src=d/Path(source_name).name;src.write_bytes(original)
 (d/'PRELAUNCH_SOURCE.py').write_bytes(original)
 record={'schema':'pr46-whole-independent-literal-helper-actual-capture/v1','operator_pid':os.getpid(),
  'argv':['/usr/bin/python3','-B',str(src)],'cwd':str(F),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
  'source_sha256':sha(original),'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False}
 (d/'PRELAUNCH.json').write_bytes(dump(record))
 with (d/'stdout.bin').open('xb') as so,(d/'stderr.bin').open('xb') as se:
  child=subprocess.Popen(record['argv'],cwd=F,stdin=subprocess.DEVNULL,stdout=so,stderr=se)
  record.update(actual_execution=True,pid=child.pid);record['exit_code']=child.wait(timeout=120);record['completed']=True
 record['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
 for channel in ['stdout','stderr']:
  b=(d/(channel+'.bin')).read_bytes();record[channel]={'path':(d/(channel+'.bin')).relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)}
 record['source_unchanged']=src.read_bytes()==original and (C/source_name).read_bytes()==original
 (d/'CAPTURE.json').write_bytes(dump(record));captures.append(record)
 assert record['exit_code']==0 and record['source_unchanged'] is True and (d/'stderr.bin').read_bytes()==b''
 result=(d/Path(result_name).name).read_bytes();saved=(C/result_name).read_bytes()
 assert result==saved and equal(json.loads(result),json.loads(saved))
 o=json.loads(result);assert type(o['passed']) is int and o['passed']==count and type(o['failed']) is int and o['failed']==0 and len(o['checks'])==count
out={'schema':'pr46-whole-independent-literal-helper-reproduction/v1','actual_pid':os.getpid(),'status':'PASS_COMPLETE_BYTE_AND_RECURSIVE_TYPE_IDENTITY','author_checks':51,'historical_independent_checks':848,'captures':captures,'entire_author_result':json.loads((F/'private_original_replay/author/verification.json').read_bytes()),'entire_historical_independent_result':json.loads((F/'private_original_replay/historical_independent/independent_results.json').read_bytes()),'future_acceptance_approved':False}
(F/'ORIGINAL_REPLAY_RESULT.json').write_bytes(dump(out))
print(json.dumps({k:out[k] for k in ['schema','actual_pid','status','author_checks','historical_independent_checks','future_acceptance_approved']},indent=2))
