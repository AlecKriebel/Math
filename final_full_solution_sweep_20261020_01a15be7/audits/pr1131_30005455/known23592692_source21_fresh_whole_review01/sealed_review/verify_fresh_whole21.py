"""Readonly independent whole21 closure/replay; prehash caller and supply manifest SHA."""
from pathlib import Path
import sys,os,stat,json,hashlib,gzip,base64,argparse
if sys.flags.optimize or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('Use isolated-I-S-B optimize0')
E=Path(__file__).resolve().parent;W=E.parent;P=W.parent
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'Duplicate JSON key');out[k]=v
  return out
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda v:need(False,'Nonfinite JSON'))
def audit(e,a):
 if e.startswith('socket.')or e in {'subprocess.Popen','os.system','os.posix_spawn'}:raise RuntimeError('Cold forbids network/process')
 if e=='open'and(isinstance(a[1],str)and any(x in a[1]for x in'wax+')or a[2]is not None and a[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):raise RuntimeError('Cold readonly')
 if e in {'os.mkdir','os.remove','os.rename','os.rmdir','os.link','os.symlink','os.chmod','os.utime','os.truncate'}:raise RuntimeError('Cold readonly')
sys.addaudithook(audit)
def meta(p):
 s=p.lstat();return {'mode':s.st_mode,'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink,'inode':s.st_ino,'device':s.st_dev}
def record(p):
 out={'physical':meta(p)}
 if p.is_symlink():out['symlink_target']=os.readlink(p)
 elif p.is_file():
  b=p.read_bytes();out.update(bytes=len(b),sha256=sha(b))
 else:need(p.is_dir(),'Unsupported external type');out['directory']=True
 return out
def original_native(path,expected=None,pass_required=True):
 raw=path.read_bytes()
 if expected:need(sha(raw)==expected,'Externally selected native changed')
 v=strict(raw);need(v['argv'][1:4]==['-I','-S','-B'],'Actual isolated native argv')
 if 'caller_source_path'in v:need(sha(Path(v['caller_source_path']).read_bytes())==v['caller_source_sha256'],'Exact executed native caller buffer')
 elif 'source_sha256'in v:need(sha(Path(v['argv'][-1]).read_bytes())==v['source_sha256'],'Exact framework caller buffer')
 need(v.get('complete_original_binary_before_parsing')is True or path.parent.name.startswith('native_parent03_')or path.parent.name=='native_fixture_intake02','Original native custody flag')
 for name in ['stdout','stderr']:
  part=v['streams'][name];b=base64.b64decode(part['base64'],validate=True);need(sha(b)==part['sha256']and len(b)==part['bytes']and b==(path.parent/(name+'.bin')).read_bytes(),'Full native binary equality')
 if pass_required:need(v['returncode']==0 and v.get('error')is None and v['streams']['stderr']['bytes']==0,'Selected actual native success')
 return v
def world(v):
 need(v['status']=='PASS'and v['error']is None,'Full fresh lifecycle success')
 need(v['source21_sha256']=='c64fae35c2ea0ebd7213e0791559f3cb5eba9f87a5b6fa8a0fc2038af2da9670'and v['entry21_sha256']=='694fb1692a0d30c5f4d7ea3e782887a88070ec3a980869717a8f5f025d8663ea','Fresh original final source/entry identity')
 need([x['action']for x in v['answers']]==['resume-stage','publish','verify-public','ledger'],'All four parsed actual lifecycle actions')
 need([(x['native_delta'],x['append_delta'])for x in v['phase_facts']]==[(3,0),(1,0),(0,0),(0,1)],'Exact individual phase transitions')
 need(v['native_calls']==['upload:finite-warm-thresholds.pdf','upload:finite-warm-thresholds-source-and-verification.zip','update','publish']and v['appends']==1,'Only reviewed modeled writes, no create')
 need(v['Git_writes']==[]and v['blocked_external_attempts']==[]and v['actual_service_effects']==0 and v['actual_AUTH_STATE_runtime_changes']is False and v['readiness']is False and v['action_authority']is False,'No actual actions or inferred authority')
 controls=v['negative_controls'];need(all(x['effect_delta']==0 for x in controls),'Every negative zero delegated effect')
 names={x['name']for x in controls}
 for name in ['new_class_initializer_alias','new_callback_sources_wrapper_alias','new_instance_attach_guard_shadow','new_unknown_UI_field_transition','new_expired_grant_replay_create','new_late_state_corruption','new_historical_create_intent_byte_drift','new_formula_only_full43_drift','new_foreign_owned_missing','new_ledger_same_runtime_reentry']:need(name in names,'Required fresh boundary control '+name)
 need(len([n for n in names if n.startswith('exact_wire_reentry_')])==4 and len([n for n in names if n.startswith('different_client_same_wire_')])==4,'Every actual wire capability rejects exact replay and foreign receiver')
def captures(path,v):
 raw=path.read_bytes();need(sha(raw)==v['complete_capture_carrier_sha256'],'Own full capture carrier')
 c=strict(gzip.decompress(raw));need(c['format']=='independent21-lossless-lines-v1','Known exact line carrier')
 pin=c['base_carrier'];b=Path(pin['path']).read_bytes();need(len(b)==pin['bytes']and sha(b)==pin['sha256']=='a87f37cfb5035da690a5bf3853851e55ff63aff48c67abaed76c7f1af9224987','Exact reference storage carrier')
 base=strict(gzip.decompress(b));bodies={h:base64.b64decode(v,validate=True)for h,v in base['bodies_base64'].items()};need(all(sha(b)==h for h,b in bodies.items()),'Every original base body complete')
 out={}
 for h,parts in c['bodies'].items():
  chunks=[]
  for p in parts:
   if p[0]=='ref':
    need(len(p)==4 and p[1]in bodies and type(p[2])is int and type(p[3])is int and p[2]>=0 and p[3]>=0 and p[2]+p[3]<=len(bodies[p[1]]),'Exact reference slice')
    chunks.append(bodies[p[1]][p[2]:p[2]+p[3]])
   else:need(len(p)==2 and p[0]=='new','Known literal part');chunks.append(bytes.fromhex(p[1]))
  body=b''.join(chunks);need(sha(body)==h,'Whole new original reconstructed body');out[h]=body
 need(all(h in out for h in c['paths'].values()),'All capture paths reconstructable')
 need(len(out)==v['complete_capture_bodies']and sum(map(len,out.values()))==v['complete_capture_raw_bytes'],'Full new capture totals')
 return len(c['paths']),len(out)
def replay(spec):
 # Full original selected preparation and external39 remain independently checked.
 prep=P/'known23592692_operations21_preparation01';checker=prep/'verify_preparation21.py';raw=checker.read_bytes()
 need(sha(raw)=='2431da20fc9996e4ffe8f530a557565262f4a99325154524b595e58a82f94253','Authenticated preparer closure reader')
 n={'__file__':str(checker),'__name__':'_independent_closed_preparation'};exec(compile(raw,str(checker),'exec',dont_inherit=True,optimize=0),n);mf=n['check_manifest']('f1a3c3b228228f7c8ecfef3d597f597d5b994d1fa85fbd0a07a6ed17395a426f');old=n['replay']()
 need(old['status']=='PASS'and old['action_authority']is False,'Retained65/32/7 packet, not fresh rerun')
 for item in spec['successful_natives']:
  v=original_native(W/item['path'],item['sha256']);stdout=base64.b64decode(v['streams']['stdout']['base64'])
  if item['role']=='lifecycle':
   r=strict(stdout);need(r==strict((W/'INDEPENDENT_LIFECYCLE_RESULT03.json').read_bytes()),'Exact whole fresh lifecycle original/result equality');world(r);paths,bodies=captures(W/'INDEPENDENT_LIFECYCLE_CAPTURE03.json.gz',r);whole=r
  if item['role']=='formula_followup':
   r=strict(stdout);need(r==strict((W/'FORMULA_CENSUS_FOLLOWUP_RESULT01.json').read_bytes())and r['status']=='PASS'and r['positive_full286_shape_passed']is True and r['formula_scalar_only_changed']is True and r['numeric_and_display_values_unchanged']is True and r['negative_error']=='CENSUS20: full sheet differs from286 or exact single own literal287','Corrected genuine formula-only boundary')
  if item['role']=='parent_framework':
   r=strict(stdout);need(r['status']=='FRAMEWORK_SMOKE_PASS_NOT_SOURCE21_VERIFICATION'and r['cases']==11 and len(set(r['four_native_child_pids']))==4,'ExactParent03 framework11')
  if item['role']=='parent_prechild':
   r=strict(stdout);need(r['status']=='PARENT03_PRECHILD_GUARDS_PASS_NOT_SOURCE21_VERIFICATION'and r['controls']==9,'ExactParent03 prechild9')
  if item['role']=='intake':
   r=strict(stdout);need(r['status']=='PASS'and r['payload_entries']==599 and r['external_selected_files']==39,'Independent actual intake cold599/39')
  if item['role']=='buffer_auth':
   r=strict(stdout);need(r==strict((W/'INDEPENDENT_BUFFER_AUTH_RESULT01.json').read_bytes())and r['status']=='PASS'and len(r['controls'])==6 and all(x['selected_AST_compiles']==0 for x in r['controls']),'Six new exact buffer constructor refusals before compile')
  if item['role']=='entry_controller':
   r=strict(stdout);need(r==strict((W/'INDEPENDENT_ENTRY_CONTROLLER_RESULT02.json').read_bytes())and r['status']=='PASS'and len(r['checks'])==21,'Exact new controller original/result')
   need(len(set(r['four_actual_child_pids']))==4,'Four distinct actual controller children')
 for key,value in [('appends',2),('native_calls',['create']),('answers',[]),('action_authority',True)]:
  bad=dict(whole);bad[key]=value
  try:world(bad)
  except RuntimeError:pass
  else:raise RuntimeError('False hash-consistent world outcome accepted')
 # Raw failed attempts remain honest; no outcome projection promotes them.
 timeout=strict((W/'native_independent_lifecycle02/SUPERVISOR_TIMEOUT_ACCOUNTING.json').read_bytes())
 need(timeout['complete_actor_outcome']is False and timeout['counted_as_success']is False,'Partial timeout not promoted')
 return {'status':'PASS','preparation_entries':len(mf['entries']),'retained_preparation_external39':old['external_selected_files'],'whole03_recorded_negatives':len(whole['negative_controls']),'whole03_meaningful_negatives':len(whole['negative_controls'])-1,'corrected_formula_followup_negatives':1,'capture_paths':paths,'capture_bodies':bodies,'actual_service_effects':0,'action_authority':False,'mathematical373_freshly_rerun':False,'coverage':'Fresh actual same-process lifecycle/overlay/20; actual entry spies after component auth; actual controller4 separate inert children; independent exactParent03. Explicit provider/path/stub seams, not one production-entry/network world.'}
def main():
 a=argparse.ArgumentParser();a.add_argument('--manifest-sha256',required=True);wanted=a.parse_args().manifest_sha256
 b=(E/'MANIFEST.json').read_bytes();need(sha(b)==wanted,'Externally pinned entire own closure');mf=strict(b)
 paths={'.':E,**{str(p.relative_to(E)):p for p in E.rglob('*')}};need(set(paths)==set(mf['entries']),'Entire own sealed namespace')
 for name,p in paths.items():
  pin=mf['entries'][name]
  if name=='MANIFEST.json':need(meta(p)==pin['physical']and pin['self_reserved']is True,'Reserved self metadata')
  else:need(record(p)==pin,'Own complete metadata/body '+name)
 ex=strict((E/'EXTERNAL_INPUTS.json').read_bytes());exclude=[E,W/'completion']
 current={str(p):p for p in[W,*W.rglob('*')]if not any(p==q or q in p.parents for q in exclude)}
 need(set(current)==set(ex['own_outside_seal']),'Entire owned external namespace, completion excluded')
 for p,pin in ex['own_outside_seal'].items():need(record(Path(p))==pin,'Own exact external input '+p)
 for p,pin in ex['fixed_external'].items():need(record(Path(p))==pin,'Dated fixed external '+p)
 f=os.statvfs(W);need(sum(p.lstat().st_blocks*512 for p in[W,*W.rglob('*')])<=24*1024**2 and f.f_bavail*f.f_frsize>=120*1024**2,'Prospective final24MiB/free120MiB')
 need(mf['action_authority']is False and mf['source21_sha256']=='c64fae35c2ea0ebd7213e0791559f3cb5eba9f87a5b6fa8a0fc2038af2da9670','Own scope/no action authority')
 r=replay(strict((E/'SELECTION.json').read_bytes()));r['own_manifest_sha256']=wanted;r['own_payload_entries']=len(paths);print(json.dumps(r,sort_keys=True))
if __name__=='__main__':main()
