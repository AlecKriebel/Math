"""Additional independent probes. The initial program remains unmodified."""
import adversarial_controls as H
from pathlib import Path
import json,copy,contextlib,io,types,subprocess
D=H.D;RESULTS=[]
def record(label,fn):
 start=H.utc()
 try:r=dict(label=label,start_utc=start,PASS=True,result=fn())
 except Exception as e:
  import traceback
  r=dict(label=label,start_utc=start,PASS=False,error=repr(e),traceback=traceback.format_exc())
 r['completed_utc']=H.utc();RESULTS.append(r);print(json.dumps(r),flush=True);H.dump(D/'ADDITIONAL_RESULTS.json',RESULTS)

class BindingFixture(H.Fixture):
 def __init__(self,label):
  self.root=H.b.RUNS/label
  H.b.Fixture.__init__(self,label)


def lock_control():
 folder=D/'lock_control';folder.mkdir();rb=H.L.b.Fixture.module
 # Import actual binding bytes directly through inert module loading.
 import importlib.util
 spec=importlib.util.spec_from_file_location('lock_binding',D/'release_binding.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 with m.acquire(folder):r=H.reject(lambda:m.acquire(folder))
 assert 'Another release stage is active' in r['error'];return r

def once_paths():
 out={}
 for kind in ['stage','publish','append']:
  label='once_'+kind;f=BindingFixture(label);normal=f.run
  if kind=='stage':
   def lost(cmd,**kw):
    r=normal(cmd,**kw)
    if len(cmd)>3 and cmd[3]=='stage':raise subprocess.TimeoutExpired('synthetic stage',1,output=b'stage\x00\xff',stderr=b'stageerr\xfe')
    return r
   f.run=lost;out[kind]=H.reject(f.publish);assert f.stages==1 and f.publishes==0
   second=H.reject(f.publish);assert f.stages==1
  elif kind=='publish':
   f.lose_publish=True;out[kind]=H.reject(f.publish);assert f.stages==f.publishes==1
   second=H.reject(f.publish);f.lose_publish=False
   z=f.module('verify_published_readonly.py').verify_existing(f.r,f.pub,f.ctx);assert z['submitted'] and f.stages==f.publishes==1
  else:
   f.publish();f.lose_append=True;out[kind]=H.reject(f.append);assert f.appends==1
   f.lose_append=False;t=f.append();assert t['append_count']==0 and f.appends==1;second=dict(readonly_append_count=t['append_count'])
  out[kind]['second']=second;f.trace();H.compact(label)
 return out


def retained_completion_corruption():
 f=H.Fixture('retained_receipt');H.quiet(f.prepare);H.quiet(f.merge)
 path=f.pub/'PR_MERGED.json';original=path.read_bytes();receipt=json.loads(original);fixed=len(f.mutations)
 outcomes={}
 for key,value in [('doi_url','https://doi.org/10.5281/zenodo.999999999'),('tracker_range',"'Wrong tab'!Z999:AC999"),('case_completion_percent',1),('actual_publication_tracker_native_merge_complete',False),('exact_native_body_readbacks',[]),('merged',False)]:
  changed=copy.deepcopy(receipt);changed[key]=value;H.dump(path,changed)
  try:
   H.quiet(lambda:f.merge(True));returned=json.loads(path.read_bytes());accepted=returned[key]==value
   outcomes[key]=dict(accepted=accepted,corrupted_value=value,mutations_unchanged=len(f.mutations)==fixed)
  except Exception as e:outcomes[key]=dict(accepted=False,error=repr(e))
  H.dump(f.base/('CORRUPT_'+key+'.json'),dict(changed_receipt=changed,outcome=outcomes[key]));path.write_bytes(original)
 f.trace();H.dump(f.base/'CORRUPTION_OUTCOMES.json',outcomes);H.compact('retained_receipt')
 return outcomes

if __name__=='__main__':
 record('actual_second_lock_acquisition_rejected',lock_control)
 record('stage_publish_append_unknown_outcome_once_paths',once_paths)
 record('existing_completion_receipt_static_field_corruption',retained_completion_corruption)
 H.dump(D/'ADDITIONAL_SUMMARY.json',dict(completed_utc=H.utc(),groups=len(RESULTS),all_expected_execution_completed=all(r['PASS'] for r in RESULTS),case_completion_percent=65))
 raise SystemExit(0 if all(r['PASS'] for r in RESULTS) else 1)
