#!/usr/bin/env python3
"""Adversarial controls against a separately trusted bootstrap; no input edits."""
from pathlib import Path
import argparse,copy,hashlib,json,os,runpy,shutil,subprocess,sys,tempfile

def need(x,m):
 if not x:raise RuntimeError(m)
def mutable(root):
 for p in [root,*root.rglob('*')]:
  if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('bootstrap',type=Path);ap.add_argument('delivery',type=Path);ap.add_argument('queue',type=Path);a=ap.parse_args();bootstrap=a.bootstrap.absolute();root=a.delivery.absolute();queue=a.queue.absolute()
 trusted=runpy.run_path(str(bootstrap));files,_=trusted['authenticate'](root,queue);m=trusted['load'](files['DELIVERY_MANIFEST.json'])
 rows=[]
 def rejected(fn,label):
  try:fn()
  except (trusted['Reject'],ValueError,TypeError,KeyError):return
  raise RuntimeError('malformed value accepted: '+label)
 for raw in ['{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}','{"a":-Infinity}','{"a":1e999}']:rejected(lambda raw=raw:trusted['load'](raw),'JSON '+raw)
 schema_tests=[]
 for field,value in [('problem_id',3800015.0),('rank',1060.0),('turns',True),('full_target_resolved',0),('status','solved'),('files',{}),('excluded_anchor_files',{})]:
  x=copy.deepcopy(m);x[field]=value;schema_tests.append((field,x))
 for field,value in [('bytes',True),('bytes',-1),('bytes',1.0),('bytes',2000001),('sha256',123),('sha256','g'*64),('path','../escape'),('path','/absolute'),('path','a//b'),('path','a/./b'),('path','a\\b'),('path','')]:
  x=copy.deepcopy(m);x['files'][0][field]=value;schema_tests.append(('entry '+field+' '+str(value),x))
 x=copy.deepcopy(m);x['files'][1]=copy.deepcopy(x['files'][0]);schema_tests.append(('duplicate entries',x))
 x=copy.deepcopy(m);x['queue']['bytes']=True;schema_tests.append(('queue bool size',x))
 x=copy.deepcopy(m);x['queue']['repository_path']='another.md';schema_tests.append(('queue path',x))
 x=copy.deepcopy(m);x['unexpected']=1;schema_tests.append(('extra manifest field',x))
 for label,x in schema_tests:rejected(lambda x=x:trusted['manifest_schema'](x),label)
 replayer=runpy.run_path(str(root/'REPLAY.py'));same=replayer['same'];expected=json.loads(files['EXPECTED_OUTPUTS.json'])
 need(not same(True,1) and not same(1,1.0) and not same({'a':1},{'a':1,'b':2}),'typed output controls')
 for section in ['native','independent','original_mutations','complete_mutations']:
  baseline=expected['modes']['0'];x=copy.deepcopy(baseline);x[section]['stdout']+=' ';need(not same(x,baseline),'full output byte comparison: '+section)
 baseline=expected['modes']['0'];x=copy.deepcopy(baseline);x['independent']['result']['independent_ordered_distance_queries']=True;need(not same(x,baseline),'recursive output type')
 before={n:hashlib.sha256(b).hexdigest() for n,b in files.items()}
 with tempfile.TemporaryDirectory(prefix='delivery-tamper-controls-') as td:
  temp=Path(td);candidate=temp/'candidate';q=temp/'QUEUE.md'
  def reset():
   if candidate.exists():mutable(candidate);shutil.rmtree(candidate)
   shutil.copytree(root,candidate);mutable(candidate);q.write_bytes(queue.read_bytes())
  def command(mode):
   flags=[] if mode==0 else ['-O' if mode==1 else '-OO']
   return [sys.executable,'-I','-S','-B',*flags,str(bootstrap),str(candidate),'--queue',str(q),'--integrity-only']
  def check(label,change,needle):
   reset();change()
   for mode in range(3):
    p=subprocess.run(command(mode),capture_output=True,timeout=20)
    need(p.returncode==1 and p.stdout==b'' and p.stderr.startswith(b'REJECT: ') and needle.encode() in p.stderr,label+' wrong rejection')
    rows.append({'test':label,'mode':mode,'exit_code':1,'rejection':p.stderr.decode().strip()})
  for name in sorted(files):
   needle='manifest trust anchor' if name=='DELIVERY_MANIFEST.json' else 'bootstrap differs' if name=='BOOTSTRAP.py' else 'payload binding'
   check('alter '+name,lambda name=name:(candidate/name).write_bytes(files[name]+b'\n'),needle)
  check('missing report',lambda:(candidate/'author/REPORT.md').unlink(),'file inventory')
  check('extra file',lambda:(candidate/'extra.txt').write_text('extra'),'file inventory')
  check('extra empty directory',lambda:(candidate/'extra').mkdir(),'directory inventory')
  def symlink():
   p=candidate/'author/REPORT.md';p.unlink();p.symlink_to(root/'author/REPORT.md')
  check('payload symlink',symlink,'symlink:')
  check('special FIFO',lambda:os.mkfifo(candidate/'pipe'),'nonregular member:')
  check('wrong queue bytes',lambda:q.write_bytes(b'changed'),'queue size')
  check('queue same size corrupt',lambda:q.write_bytes(bytes([q.read_bytes()[0]^1])+q.read_bytes()[1:]),'queue hash')
  def symlink_queue():q.unlink();q.symlink_to(queue)
  check('queue symlink',symlink_queue,'queue regular file')
  # Restore after link control without following a link when resetting.
  q.unlink();q.write_bytes(queue.read_bytes());reset()
  for mode in range(3):
   p=subprocess.run(command(mode),capture_output=True,timeout=20);need(p.returncode==0 and p.stderr==b'' and json.loads(p.stdout)['status']=='PASS_ENTIRE_DELIVERY_INTEGRITY','positive control')
  source=files['REPLAY_MUTATIONS.py'].decode()
  need("observed['last_error_line'] == expected_errors[label]" in source and "observed['exit_code'] == 1" in source,'semantic rejection exact checks absent')
 need(trusted['authenticate'](root,queue)[0]==files,'source delivery changed')
 return {'schema':'line-arrangement-hostile-controls-v1','status':'PASS','optimization':sys.flags.optimize,'all_three_modes_for_each_tamper':True,'bound_files_tested':len(files),'tamper_rejections':len(rows),'schema_rejections':len(schema_tests),'malformed_json_rejections':5,'typed_and_complete_output_negative_controls':8,'positive_integrity_modes':3,'input_unchanged':True,'controls':rows}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
