"""Once-intent failure controls against unchanged frozen source functions."""
import probes as H
import compact_fixtures
import json,types,subprocess,sys,traceback
D,B,I,P=H.D,H.B,H.I,H.P
ROWS=[]
def check(name,fn,fixture):
 start=H.utc()
 try:result=fn();row=dict(name=name,start_utc=start,end_utc=H.utc(),PASS=True,result=result)
 except Exception as e:row=dict(name=name,start_utc=start,end_utc=H.utc(),PASS=False,error=repr(e),traceback=traceback.format_exc())
 ROWS.append(row);H.js(D/'FAILURE_PATH_RESULTS.json',ROWS);print(json.dumps(row),flush=True)
 if (D/'fixtures'/fixture).exists():compact_fixtures.main([fixture])
def unknown_stage():
 r,pub,p=H.make_case('stage_unknown');p.lose_stage=True
 first=H.rejects(lambda:P.publish_once(r,pub,ROOT=pub.parent.parent));second=H.rejects(lambda:P.publish_once(r,pub,ROOT=pub.parent.parent),'Prior stage')
 assert (pub/'STAGE_ATTEMPT.json').exists() and not (pub/'PUBLISH_ATTEMPT.json').exists()
 assert sum(x.get('provider')=='zenodo' and x.get('operation')=='stage' for x in p.calls)==1
 raw=list((pub/'private_transport/zenodo_stage').rglob('02-stage-stdout.json'))[0].read_bytes();assert raw==b'partial-stage\xff'
 p.save('stage_unknown');return dict(first=first,second=second,stage_calls=1,partial_bytes_retained=raw.hex())
def unknown_native_object():
 r,pub,p=H.make_case('native_object_unknown');H.stage_and_append(r,pub,p);orig=p.api
 def api(method,path,payload=None):
  result=orig(method,path,payload)
  if method=='POST' and path=='git/blobs':
   assert (pub/'NATIVE_OBJECT_BUILD_INTENT.json').exists()
   raise subprocess.TimeoutExpired('SYNTHETIC_BLOB_CREATED_RESPONSE_LOST',1,output=b'\x00\xffpartial-blob',stderr=b'blob-stderr')
  return result
 p.api=api
 first=H.rejects(lambda:I.main([]),'unknown');writes=sum(x.get('method')in ['PATCH','POST'] for x in p.calls)
 second=H.rejects(lambda:I.main([]),'Prior native');assert sum(x.get('method')in ['PATCH','POST'] for x in p.calls)==writes==1
 raw=list((pub/'private_transport').rglob('*partial-stdout.bin'))[0].read_bytes();assert raw==b'\x00\xffpartial-blob'
 assert not (pub/'PR_PREPARED.json').exists() and not (pub/'NATIVE_PREPARE_ATTEMPT.json').exists()
 p.save('native_object_unknown');return dict(first=first,second=second,object_writes=1,intent_precedes_first_post=True,binary_partial_retained=raw.hex())
if __name__=='__main__':
 check('unknown_stage_never_stages_twice',unknown_stage,'stage_unknown')
 check('unknown_first_native_object_durable_intent_no_second_write',unknown_native_object,'native_object_unknown')
 H.js(D/'FAILURE_PATH_SUMMARY.json',dict(utc=H.utc(),groups=len(ROWS),passed=sum(x['PASS'] for x in ROWS),all_expected_outcomes=all(x['PASS'] for x in ROWS),synthetic_only=True,no_release_authority=True))
 sys.exit(0 if all(x['PASS'] for x in ROWS) else 1)
