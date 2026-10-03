#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,os,stat
f=Path(__file__).resolve().parent
s=f.parent/'original_preparation_family/source_snapshot'
p=s/'verify.py'; saved=s/'verification.json'
c=f/'original_helper_capture';c.mkdir(exist_ok=False)
def bind(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':oct(stat.S_IMODE(p.stat().st_mode))}
source=bind(p);before=p.read_bytes();argv=['/usr/bin/python3','-B',str(p)];start=datetime.now(timezone.utc).isoformat()
(c/'PRELAUNCH.json').write_text(json.dumps({'argv':argv,'cwd':str(f),'started_utc':start,'operator_pid':os.getpid(),'source':source,'expected_saved_result':bind(saved)},indent=2)+'\n')
with (c/'stdout.bin').open('wb') as out,(c/'stderr.bin').open('wb') as err:
 child=subprocess.Popen(argv,cwd=f,stdout=out,stderr=err);rc=child.wait()
end=datetime.now(timezone.utc).isoformat();raw=(c/'stdout.bin').read_bytes()
def unique_pairs(pairs):
 result={}
 for k,v in pairs:
  if k in result:raise ValueError('duplicate JSON key')
  result[k]=v
 return result
live=json.loads(raw,object_pairs_hook=unique_pairs);old=json.loads(saved.read_bytes(),object_pairs_hook=unique_pairs)
assert rc==0 and p.read_bytes()==before and raw==saved.read_bytes() and live==old
assert type(live['assertions']) is int and live['assertions']==2837 and live['status']=='PASS'
result={'status':'PASS','started_utc':start,'ended_utc':end,'operator_pid':os.getpid(),'child_pid':child.pid,'exit_code':rc,'argv':argv,'cwd':str(f),'source_unchanged':p.read_bytes()==before,'source':source,'byte_identical_saved_result':True,'decoded_equal_saved_result':True,'stdout':bind(c/'stdout.bin'),'stderr':bind(c/'stderr.bin'),'assertions':live['assertions']}
(c/'CAPTURE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
