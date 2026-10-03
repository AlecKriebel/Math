#!/usr/bin/env python3
"""Own finite/source/receipt controls; no candidate helper imports or execution."""
from pathlib import Path,PurePosixPath
import collections,datetime,difflib,hashlib,json,math,re,subprocess,os
R=Path(__file__).resolve().parent;A=R.parent;REPO=R.parents[3];C=A/'reviewed_candidate'

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def H(b):return hashlib.sha256(b).hexdigest()
def ck(v,s):
 if not v:raise ValueError(s)
def pairs(xs):
 d={}
 for k,v in xs:ck(k not in d,'Duplicate key');d[k]=v
 return d
def floating(s):
 n=float(s);ck(math.isfinite(n),'Nonfinite float');return n
def constant(s):raise ValueError(s)
def J(b):return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=constant)
def entry(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':H(b)}

def main():
 begin=now();g=R/'independent_git_reads';g.mkdir(exist_ok=False);commands=[]
 def git(*args):
  ck(args[0] in ('show','ls-tree','diff'),'Read-only original Git query')
  i=len(commands);out=g/f'{i}.stdout';err=g/f'{i}.stderr';start=now();argv=['git',*args]
  with out.open('wb') as o,err.open('wb') as e:
   p=subprocess.Popen(argv,cwd=REPO,stdin=subprocess.DEVNULL,stdout=o,stderr=e,env=None);pid=p.pid;code=p.wait(timeout=60)
  row={'argv':argv,'cwd':str(REPO),'pid':pid,'started_utc':start,'finished_utc':now(),'actual_execution':True,'completed':True,'stdin_supplied':False,'returncode':code,'stdout':entry(out),'stderr':entry(err)};commands.append(row)
  (R/'INDEPENDENT_ORIGINAL_GIT_READ_RECEIPTS.json').write_text(json.dumps(commands,indent=2)+'\n');ck(code==0,'Original Git read failed');return out.read_bytes()
 snapshot=J((C/'original_snapshot_manifest.json').read_bytes());head=snapshot['head'];base=snapshot['base']
 for row in snapshot['files']:
  name=snapshot['prefix']+row['path'];b=(C/'original_archive'/row['path']).read_bytes()
  ck(git('show',head+':'+name)==b,'Whole original Git object differs')
  ck(git('ls-tree',head,'--',name).decode().strip()==row['mode']+' blob '+row['git_blob']+'\t'+name,'Original100644 blob differs')
 diff=(C/'original_diff.patch').read_bytes();ck(diff==git('diff',base,head),'Complete original diff differs')
 ck(git('diff','--name-only',base,head).decode().splitlines()==snapshot['changed_paths'],'Original17path set/order')
 blocks=[x for x in re.split(rb'(?m)(?=^diff --git )',diff) if x];ck(len(blocks)==17,'Full diff17sections');sections=[]
 for block in blocks:
  lines=block.splitlines(keepends=True);names=lines[0].decode().strip().split(' ')[2:];ck(len(names)==2 and names[0][2:]==names[1][2:],'Diff path pair')
  path=names[1][2:]
  if path.endswith('/QUEUE.md'):
   old=[x[1:].decode() for x in lines if x.startswith(b'-') and not x.startswith(b'---')];new=[x[1:].decode() for x in lines if x.startswith(b'+') and not x.startswith(b'+++')]
   ck(len(old)==len(new)==1,'Only target queue line changed in original');left=old[0].split('|');right=new[0].split('|')
   ck(len(left)==len(right)==14 and [i for i,(x,y) in enumerate(zip(left,right)) if x!=y]==[8,9,11] and left[2].strip()=='9700035 / AMR-096-0035','Original named queue columns only')
   sections.append({'path':path,'bytes':len(block),'sha256':H(block),'removed_whole_line':old[0],'added_whole_line':new[0]})
  else:
   name=path[len(snapshot['prefix']):];ck(b'new file mode 100644\n' in lines and b'--- /dev/null\n' in lines,'New100644 file')
   reconstructed=b''.join(x[1:] for x in lines if x.startswith(b'+') and not x.startswith(b'+++'))
   ck(reconstructed==(C/'original_archive'/name).read_bytes(),'Whole added original diff payload');sections.append({'path':path,'bytes':len(block),'sha256':H(block),'added_payload_exact_original':True})
 (R/'INDEPENDENT_COMPLETE_ORIGINAL_DIFF_SECTIONS.json').write_text(json.dumps({'bytes':len(diff),'lines':len(diff.splitlines()),'sections':sections},indent=2)+'\n')
 # Genuine outer current builder receipt plus complete inner read-only Git channels.
 cap=A/'root_current_freeze_actual_capture';receipt=J((cap/'CAPTURE.json').read_bytes())
 ck(H((cap/'CAPTURE.json').read_bytes())=='68a9cc23f0b5fedd6624d4e7474b707d8f2727b4ac78193232ff16b4cc376d34','Frozen root capture SHA')
 ck(receipt['actual_execution'] is True and receipt['completed'] is True and type(receipt['pid']) is int and receipt['pid']==36236 and type(receipt['exit_code']) is int and receipt['exit_code']==0 and receipt['stdin_supplied'] is False,'Genuine builder actual record')
 ck(receipt['fresh_native13_before']==receipt['fresh_native13_after'] and receipt['head_before']==receipt['head_after']=='6f7cdb80ac4ed9d7e1179380de540a4eb5d9a534','Freeze dated13/main before/after')
 source=(cap/'PRELAUNCH_SOURCE.py').read_bytes();ck(H(source)==receipt['source_sha256']==H((C/'build/prepare_current_packet.py').read_bytes()),'Actual full builder source exact')
 for channel in ('stdout','stderr'):
  row=receipt[channel];b=(cap/row['path']).read_bytes();ck(type(row['bytes']) is int and len(b)==row['bytes'] and H(b)==row['sha256'],'Full actual builder channel')
 out=J((cap/receipt['stdout']['path']).read_bytes());ck(out['status']=='CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING' and out['members']==547 and out['manifest_sha256']==H((C/'MANIFEST.json').read_bytes()),'Builder full output exact current')
 for row in receipt['complete_reviewed_prerequisites']:
  b=(A/row['path']).read_bytes();ck(len(b)==row['bytes'] and H(b)==row['sha256'],'Actual root prerequisite byte pin')
 inner=J((C/'build/actual_builder_attempt/GIT_COMMANDS.json').read_bytes())
 for run in inner:
  ck(run['argv'][0]=='git' and run['argv'][1] in ('branch','show','ls-tree','diff','rev-parse'),'Builder read-only commands')
  ck(run['actual_execution'] is True and run['completed'] is True and type(run['exit_code']) is int and run['exit_code']==0 and run['stdin_supplied'] is False and not run['retention_errors'],'Actual retained child success')
  for channel in ('stdout','stderr'):
   row=run[channel];b=(C/'build/actual_builder_attempt'/row['path']).read_bytes();ck(len(b)==row['bytes'] and H(b)==row['sha256'] and row['available'] is True,'Inner full actual channel')
 # Independent source-variant reading ledger: every source byte, full baseline
 # bodies and every semantic delta, without execution of any of those sources.
 grouped=collections.defaultdict(list)
 for p in C.rglob('*.py'):grouped[H(p.read_bytes())].append(p)
 source_groups=[{'sha256':h,'bytes':ps[0].stat().st_size,'paths':[p.relative_to(C).as_posix() for p in ps]} for h,ps in grouped.items()]
 (R/'WHOLE_CURRENT_UNIQUE_SOURCE_COVERAGE.json').write_text(json.dumps({'source_groups':source_groups,'unique_sources':len(source_groups),'all_sources_imported_or_executed':False,'coverage':'Full baseline source reading plus exact whole unified deltas for corruptions, V1 controls, historic closure and reconstructed stopped builder.'},indent=2)+'\n')
 variants=[]
 pairs_to_read=[('build/prepare_current_packet.py','build/HISTORICAL_STOPPED_BUILDER_SOURCE.py'),('family_evidence/primary_scope_family/finite_controls.py','family_evidence/primary_scope_family/finite_controls_actual_capture/PRELAUNCH_SOURCE.py'),('family_evidence/primary_scope_family/closure_check.py','family_evidence/primary_scope_family/closure_check_actual_capture/PRELAUNCH_SOURCE.py')]
 for p in sorted((C/'family_evidence/network_tail_measure_family/controls').glob('*.py')):pairs_to_read.append(('family_evidence/network_tail_measure_family/network_measure_controls.py',p.relative_to(C).as_posix()))
 for first,second in pairs_to_read:
  d=''.join(difflib.unified_diff((C/first).read_text().splitlines(True),(C/second).read_text().splitlines(True),fromfile=first,tofile=second));variants.append({'baseline':first,'variant':second,'complete_delta':d})
 (R/'WHOLE_CURRENT_COMPLETE_SOURCE_VARIANT_DELTAS.json').write_text(json.dumps(variants,indent=2)+'\n')
 # Pure independently implemented finite guard controls: no candidate loader.
 controls=[]
 def rejected(label,fn):
  try:fn()
  except (ValueError,TypeError):controls.append({'label':label,'expected_rejection_observed':True})
  else:raise ValueError('Bad control accepted '+label)
 for label,b in [('duplicate_key',b'{"a":0,"a":1}'),('nonfinite_NaN',b'{"a":NaN}'),('overflow',b'{"a":1e9999}')]:rejected(label,lambda b=b:J(b))
 def typed_size(v):ck(type(v) is int and v>=0,'Exact nonnegative integer')
 for value in [False,True,-1,'0',0.0]:rejected('typed_size_'+repr(value),lambda value=value:typed_size(value))
 for value in [0,1,15458]:typed_size(value);controls.append({'label':'valid_typed_size_'+str(value),'positive_acceptance_observed':True})
 # Type-sensitive canonical identity rather than Python bool/int equality.
 ck(json.dumps({'v':True})!=json.dumps({'v':1}),'Boolean identity must not equal integer identity')
 record={'path':'same','bytes':3,'sha256':H(b'abc'),'roles':['one']}
 def merge(b,role):
  ck(record['bytes']==len(b) and record['sha256']==H(b),'Immutable repeated read');record['roles']=sorted(set(record['roles']+[role]))
 merge(b'abc','two');merge(b'abc','one');ck(record['roles']==['one','two'],'Multiple roles retained');controls.append({'label':'same_bytes_multiple_roles','positive_acceptance_observed':True})
 rejected('same_size_changed_bytes',lambda:merge(b'abd','three'))
 rejected('changed_size',lambda:merge(b'abcd','three'))
 # Missing and present-null are distinct states, enforced independently.
 def runtime(o):ck(all(k in o and o[k] is None for k in ('model','verdict')),'Present runtime nulls')
 runtime({'model':None,'verdict':None});controls.append({'label':'present_null','positive_acceptance_observed':True})
 rejected('missing_null_key',lambda:runtime({'verdict':None}));rejected('false_not_null',lambda:runtime({'model':False,'verdict':None}))
 (R/'INDEPENDENT_FINITE_GUARD_CONTROL_RESULTS.json').write_text(json.dumps({'finite_controls':controls,'count':len(controls),'candidate_guard_import_or_execution':False,'scope':'Finite own representation/byte/type controls only; actual candidate guard source was separately read.'},indent=2)+'\n')
 result={'status':'PASS_OWN_SUPPLEMENTAL_READONLY_SOURCE_RECEIPT_FINITE_CONTROLS','started_utc':begin,'finished_utc':now(),'pid':os.getpid(),'independent_original_Git_queries':len(commands),'original16_all_bytes_modes_blobs_exact':True,'full_original17_diff_payloads_queue_exact':True,'original_diff_bytes':len(diff),'current_root_builder_capture_full_source_channels_exact':True,'root_builder_inner_readonly_query_count':len(inner),'root_builder_native13_HEAD_unchanged_at_freeze':True,'later_live_native_changes_are_not_reinterpreted_as_freeze_failure':True,'unique_current_python_sources':len(source_groups),'source_variant_deltas':len(variants),'independent_finite_guard_controls':len(controls),'candidate_helper_imports_or_execution':False,'shared_native_Git_remote_writes':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0}
 (R/'SUPPLEMENTAL_READONLY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
