"""Offline-only PR206 guards and uncertain-outcome recovery with fake transports."""
import sys
sys.dont_write_bytecode=True
import argparse,copy,contextlib,json,os,pathlib,shutil,stat,subprocess,tempfile,urllib.request
from types import SimpleNamespace,ModuleType
HERE=pathlib.Path(__file__).resolve().parent
def load_owned(alias,name):
 raw=(HERE/name).read_bytes();module=ModuleType(alias);module.__file__=str(HERE/name)
 sys.modules[alias]=module;exec(compile(raw,str(HERE/name),'exec'),module.__dict__);return module
c=load_owned('ops_common206','ops_common206.py')
p=load_owned('publisher206','publisher206.py')
t=load_owned('tracker206','tracker206.py')
CHECKS=[]
REAL_CALLS=[]
SYNC=[]
REAL_FSYNC=os.fsync
def tracked_fsync(fd):
 st=os.fstat(fd);SYNC.append((st.st_dev,st.st_ino,stat.S_ISDIR(st.st_mode)));return REAL_FSYNC(fd)
os.fsync=tracked_fsync
def forbidden(*args,**kwargs):
 REAL_CALLS.append('forbidden actual process/network call')
 raise RuntimeError('Offline suite forbids all real subprocess and HTTP transport')
subprocess.run=forbidden
urllib.request.urlopen=forbidden
def offline_audit(event,args):
 if event.startswith(('socket.','subprocess.')) or event in ('os.system','os.fork'):
  forbidden()
sys.addaudithook(offline_audit)
def check(ok,name):
 if not ok:raise RuntimeError('FAILED: '+name)
 CHECKS.append(name)
def fails(fn,name):
 try:fn()
 except (RuntimeError,KeyError,FileNotFoundError,TypeError,ValueError):CHECKS.append(name);return
 raise RuntimeError('Expected explicit rejection: '+name)
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():path.chmod(0o600)
 raw=value if isinstance(value,bytes) else c.encoded(value)
 path.write_bytes(raw);path.chmod(0o444)
 return path
def marker_synced(path):
 st=path.stat();parent=path.parent.stat()
 return (st.st_dev,st.st_ino,False) in SYNC and (parent.st_dev,parent.st_ino,True) in SYNC

# Test-only substitution of exact mandatory fact pins: no actual Root receipt is
# copied into this synthetic authority tree. Live common constants stay unchanged.
SYNTHETIC_FACTS={name:c.encoded(dict(synthetic_fixture_only=True,role=role)) for name,role in [('ROOT_PRIORITY_EDITORIAL_GATE_01.json','priority'),('ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json','custody')]}
c.PRIORITY_PIN=dict(bytes=len(SYNTHETIC_FACTS['ROOT_PRIORITY_EDITORIAL_GATE_01.json']),sha256=c.digest(SYNTHETIC_FACTS['ROOT_PRIORITY_EDITORIAL_GATE_01.json']))
c.CUSTODY_PIN=dict(bytes=len(SYNTHETIC_FACTS['ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json']),sha256=c.digest(SYNTHETIC_FACTS['ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json']))
KIT=p.locate_kit(HERE.parent)
check(c.pin(KIT)['sha256']==c.KIT_SHA,'read-only original KIT SHA pinned; never launched')
WORK=HERE/'offline_work'
WORK.mkdir(exist_ok=True)

class Fixture:
 def __init__(self,root,metadata_file='zenodo-deposit.json',upload_stem='synthetic-focal-inversion',metadata_description=None):
  self.names={upload_stem+'.pdf',upload_stem+'.tex'}|{'synthetic-attributed-evidence.zip'}
  self.base=root/'pr206_5100062';self.base.mkdir()
  self.package=self.base/'publication_package_v7';self.package.mkdir()
  self.metadata=dict(title='SYNTHETIC PR206 focal inverse area verification note',creators=[dict(name='Kriebel, Alec',orcid='0009-0001-9320-500X')],description=metadata_description if metadata_description is not None else 'SYNTHETIC OFFLINE FIXTURE ONLY. Alper Ferudun DOI10.5281/zenodo.23096994 exact theorem credit.')
  for name in sorted(self.names):write(self.package/name,('offline fixture '+name+'\n').encode())
  write(self.package/metadata_file,dict(metadata=self.metadata,files=[dict(path=x) for x in sorted(self.names)]))
  write(self.package/'PACKAGE_SEAL.json',dict(synthetic_fixture_only=True))
  safe={x.name:c.pin(x) for x in self.package.iterdir()}
  self.other={}
  self.preparation={}
  for role in ('mathematics','priority','portable','package','visual'):
   rel='synthetic_inputs/'+role+'.json';q=write(self.base/rel,dict(synthetic_fixture_only=True,role=role))
   self.other[rel]=c.pin(q);self.preparation[role]=dict(path=rel,**c.pin(q))
  for rel in ('ROOT_PRIORITY_EDITORIAL_GATE_01.json','ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json'):
   q=write(self.base/rel,SYNTHETIC_FACTS[rel]);self.other[rel]=c.pin(q)
  self.events=[]
  for i in (1,2):
   rd=self.base/('fresh_review_'+str(i));write(rd/'REPORT.md',b'SYNTHETIC OFFLINE CLEANPASS fixture\n')
   event=dict(review_number=i,directory=rd.name,report_file='REPORT.md',safe_files={'REPORT.md':c.pin(rd/'REPORT.md')},report_pin=c.pin(rd/'REPORT.md'),reviewed_package=self.package.name,reviewed_package_seal=safe['PACKAGE_SEAL.json'],verdict='CLEANPASS',whole_package_scope=True,open_findings=0)
   ap=write(self.base/('ROOT_REVIEW_ACCEPTANCE_'+str(i)+'.json'),dict(synthetic_fixture_only=True,PR=c.PR,original_head=c.HEAD,review_accepted=True,NEW_whole_package_reviews_completed=i,review_cycle_repairs_required_now=False,review_event=copy.deepcopy(event)))
   self.events.append(event|dict(Root_acceptance_file=ap.name,Root_acceptance_pin=c.pin(ap)))
  self.gate=dict(metadata_file=metadata_file,PR=c.PR,problem_id=c.PROBLEM,original_head=c.HEAD,publication_ready_gate_accepted=True,whole_package_review_loop_complete=True,mathematical_clearance=True,source_contract_clearance=True,bounded_priority_audit_complete=True,current_portable_verifier_accepted=True,qualified_attributed_note_editorially_cleared=True,historical_priority_established=False,whole_package_review_events=self.events,package=self.package.name,package_seal=safe['PACKAGE_SEAL.json'],package_safe_files=safe,metadata=self.metadata,intended_upload_files={n:safe[n] for n in sorted(self.names)},other_safe_files=self.other,preparation_receipts=self.preparation)
  self.gp=self.base/'ROOT_PUBLICATION_GATE_01.json';write(self.gp,self.gate)
  self.checkpoint=self.base/'publication_lifecycle_preparation_02/ready90_99';self.checkpoint.mkdir(parents=True)
  inputs={'ROOT_PUBLICATION_GATE_01.json':self.gp}
  inputs.update({self.package.name+'/'+n:self.package/n for n in safe})
  inputs.update({rel:self.base/rel for rel in self.other})
  for event in self.events:
   inputs.update({event['directory']+'/'+rel:self.base/event['directory']/rel for rel in event['safe_files']})
   inputs[event['Root_acceptance_file']]=self.base/event['Root_acceptance_file']
  self.selected={c.PREFIX+rel:c.native_identity(path) for rel,path in inputs.items()}
  self.views={c.PREFIX+'CURRENT_CASE_STATUS.json',c.PREFIX+'RESEARCH_LOG.md'}|{'draft_pr_publication_program_20260930/'+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
  for rel in self.views:
   raw=('SYNTHETIC HISTORICAL POSTIMAGE '+rel).encode()
   self.selected[rel]=dict(bytes=len(raw),sha256=c.digest(raw),git_blob=c.hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
  self.facts=dict(Root_publication_gate_pin=c.pin(self.gp),package=self.package.name,package_seal=self.gate['package_seal'],case_percent=90,publication_ready=True,NEW_whole_package_reviews_completed=2,whole_package_review_loop_complete=True,mathematical_clearance=True,source_contract_clearance=True,priority_clearance=True,bounded_priority_audit_complete=True,qualified_attributed_note_editorially_cleared=True,priority_clearance_scope='qualified_attributed_note_only',priority_novelty_clearance=False,historical_firstness_independence_established=False,actual_publication_verified=False,actual_tracker_row_verified=False,actual_original_PR_merged=False,completed=False,fully_completed_count=48,published_count=32,last_completed_PR=205,next_numeric_intake_cursor=206,advance_to_next_PR_authorized_now=False,goal_complete=False,DOI=None,record_id=None,tracker_range=None,actual_factual_accepted=False,actual_merge_accepted=False)
  self.acceptance=dict(schema='pr206-lifecycle-actual-acceptance-v1',evidence_scope='ACTUAL_ROOT_RECEIPT',UTC=c.utc(),phase='ready',actual_original_PR_head=c.HEAD,actual_original_PR_is_draft=True,actual_original_PR_state='open',PR=c.PR,original_head=c.HEAD,accepted=True,case_percent=90,checkpoint_commit='c'*40,main_observed='d'*40,parents=['b'*40],sole_parent='b'*40,actual_tree='e'*40,selected_files=len(self.selected),facts=self.facts)
  for field in ('every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','original_native_custody_retained'):self.acceptance[field]=True
  for field in ('Root_publication_gate_pin','package','package_seal','publication_ready','NEW_whole_package_reviews_completed','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','priority_clearance','priority_novelty_clearance','historical_firstness_independence_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged','completed','fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor','advance_to_next_PR_authorized_now','goal_complete'):self.acceptance[field]=self.facts[field]
  self.pointer=dict(schema='pr206-lifecycle-actual-pointer-v1',PR=c.PR,phase='ready',directory=self.checkpoint.relative_to(self.base).as_posix(),checkpoint_commit='c'*40,main_observed='d'*40,Root_recorded_only_after_actual_full_scope_acceptance=True)
  self.rebind_map()
  self.adoption_path=self.base/'SYNTHETIC_ROOT_OPS_ADOPTION.json'
  self.adoption=dict(synthetic_fixture_only=True,schema='pr206-root-publication-operations-adoption-v1',evidence_scope='ACTUAL_ROOT_RECEIPT',accepted_preparation_only=True,PR=c.PR,original_head=c.HEAD,sources={},approved_publication_gate_pin=c.pin(self.gp),approved_actual_ready_pointer_pin=c.pin(self.base/'ROOT_ACTUAL_READY_CHECKPOINT.json'),approved_actual_ready_verification_pin=c.pin(self.base/'ROOT_ACTUAL_READY_VERIFICATION_01.json'),dispatcher_pin=dict(bytes=123,sha256='f'*64))
  for name in c.CODES:
   q=write(self.base/c.OWN/name,(HERE/name).read_bytes());self.adoption['sources'][c.OWN+'/'+name]=c.pin(q)
  self.write_adoption()
 def write_adoption(self):
  addendum=dict(synthetic_fixture_only=True,schema='pr206-root-postready-operations-contract-addendum-v1',evidence_scope='ACTUAL_ROOT_RECEIPT',PR=c.PR,accepted=True,original_head=c.HEAD,publication_gate_pin=self.adoption['approved_publication_gate_pin'],actual_ready_pointer_pin=self.adoption['approved_actual_ready_pointer_pin'],actual_ready_verification_pin=self.adoption.get('approved_actual_ready_verification_pin'),source_family=c.OWN,sources=copy.deepcopy(self.adoption['sources']),dispatcher_pin=self.adoption.get('dispatcher_pin'),scientific_package_metadata_uploads_unchanged=True,prior_native_selected_original07_files_preserved=True,operations_sources_approved_after_original_ready_checkpoint=True,executed_current_sources_claimed_present_in_original_ready_map=False,not_a_new_scientific_or_priority_clearance=True,no_advance_or_completion_granted=True)
  self.addendum_path=self.base/'ROOT_PUBLICATION_OPERATIONS_CONTRACT_ADDENDUM_01.json';write(self.addendum_path,addendum)
  self.adoption['approved_operations_contract_addendum_pin']=c.pin(self.addendum_path)
  write(self.adoption_path,self.adoption);c.configure_authority(self.adoption_path.name,c.pin(self.adoption_path))
 def reapprove_gate(self):
  self.adoption['approved_publication_gate_pin']=c.pin(self.gp);self.write_adoption()
  self.acceptance['Root_publication_gate_pin']=c.pin(self.gp);self.facts['Root_publication_gate_pin']=c.pin(self.gp)
 def rebind_map(self,reapprove=True):
  sha=c.digest(json.dumps(self.selected,sort_keys=True,separators=(',',':')).encode())
  mp=write(self.checkpoint/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',dict(selected_files=self.selected,selected_map_sha256=sha))
  self.acceptance.update(selected_files=len(self.selected),selected_map_sha256=sha,actual_current_map_file=c.pin(mp),actual_current_selected_map_sha256=sha)
  self.write_acceptance(reapprove=reapprove)
 def write_acceptance(self,reapprove=True):
  ap=write(self.checkpoint/'ACCEPTANCE.json',self.acceptance);self.pointer['acceptance_pin']=c.pin(ap)
  write(self.base/'ROOT_ACTUAL_READY_CHECKPOINT.json',self.pointer)
  self.verification=dict(synthetic_fixture_only=True,schema='pr206-root-actual-ready-verification-v1',evidence_scope='ACTUAL_ROOT_RECEIPT',PR=c.PR,accepted=True,actual_ready90_fully_accepted_synced_and_pointer_verified=True,checkpoint_commit=self.acceptance['checkpoint_commit'],actual_main_observed=self.acceptance['main_observed'],selected_files=self.acceptance['selected_files'],actual_selected_map_sha256=self.acceptance['actual_current_selected_map_sha256'],actual_acceptance_pin=c.pin(ap),actual_ready_pointer_pin=c.pin(self.base/'ROOT_ACTUAL_READY_CHECKPOINT.json'),actual_selected_map_file_pin=self.acceptance['actual_current_map_file'],actual_publication_gate_pin=c.pin(self.gp),ready_candidate_changed_path_count=3,ready_candidate_changed_paths_exclude_QUEUE_and_all_native_attempts=True,original_native_custody_retained=True,actual_original_PR_head=self.acceptance['actual_original_PR_head'],actual_original_PR_is_draft=self.acceptance['actual_original_PR_is_draft'],actual_original_PR_state=self.acceptance['actual_original_PR_state'],actual_original_PR_merged=False,actual_publication=False,actual_tracker=False,advance=False,completed_count=48,published_count=32,cursor=206,case_completion_estimate_percent=90,every_selected_identity_checked_at_actual_observed_MAIN=True,all_overlay_body_identities_verified=True,full_foreign_tree_scope_preserved=True,all_five_local_readonly_native_postimages=[dict(path=rel,identity=copy.deepcopy(self.selected.get(rel)),mode='0o444',regular=True) for rel in sorted(self.views)],all_three_actual_steps_and_six_alias_cleanups_verified=True)
  write(self.base/'ROOT_ACTUAL_READY_VERIFICATION_01.json',self.verification)
  if hasattr(self,'adoption') and reapprove:
   self.adoption['approved_actual_ready_pointer_pin']=c.pin(self.base/'ROOT_ACTUAL_READY_CHECKPOINT.json');self.adoption['approved_actual_ready_verification_pin']=c.pin(self.base/'ROOT_ACTUAL_READY_VERIFICATION_01.json');self.write_adoption()
 def change_gate(self,field,value):
  self.gate[field]=value;write(self.gp,self.gate)
 def context(self):return c.load_context(self.base)

@contextlib.contextmanager
def fixture(**kwargs):
 with tempfile.TemporaryDirectory(prefix='offline_',dir=WORK) as root:yield Fixture(pathlib.Path(root),**kwargs)

class FakeKit:
 def __init__(self,f,behavior=None):
  self.f=f;self.behavior=behavior;self.calls=[];self.stage_count=0;self.publish_count=0;self.published=False;self.id=999999999999;self.inspect_failures=0
 def value(self):
  j=dict(environment='production',id=self.id,state='published' if self.published else 'ready_to_publish',title=self.f.metadata['title'],metadata_normalizations=[],files=[dict(name=n,size=v['bytes'],sha256=v['sha256']) for n,v in self.f.gate['intended_upload_files'].items()])
  if self.published:j.update(record_url='https://zenodo.org/records/'+str(self.id),doi='10.5281/zenodo.'+str(self.id),doi_url='https://doi.org/10.5281/zenodo.'+str(self.id),doi_resolution=dict(status='resolved',http_status=200))
  return j
 def run(self,argv,env):
  self.calls.append(list(argv));mode=argv[6]
  check(argv[1:5]==['-E','-S','-B','-P'] and env.get('PYTHONDONTWRITEBYTECODE')=='1','fake KIT command bytecode disabled '+mode)
  if mode in ('stage','publish'):
   marker=self.f.base/'private_operations/zenodo'/(mode.upper()+'_INFLIGHT.json')
   check(marker.exists() and marker_synced(marker),'durable exclusive file and directory before fake '+mode)
  if mode=='stage':
   self.stage_count+=1
   if self.behavior=='stage_lost':raise OSError('fake response lost after stage')
  elif mode=='publish':
   self.publish_count+=1;self.published=True
   check(argv[-2:]==['--confirm-id',str(self.id)],'publish confirms exact known ID')
   if self.behavior=='publish_lost':raise OSError('fake response lost after publish')
  elif mode=='inspect' and self.behavior=='inspect_lost' and not self.inspect_failures:
   self.inspect_failures+=1;raise OSError('fake read response lost')
  j=self.value()
  if self.behavior=='bad_metadata':j['metadata_normalizations']=['fake discrepancy']
  if self.behavior=='wrong_id' and mode=='inspect':j['id']+=1
  return SimpleNamespace(returncode=0,stdout=json.dumps(j),stderr='')

class FakePublic:
 def __init__(self,f,bad=None):self.f=f;self.bad=bad;self.calls=[]
 def get(self,url,limit):
  self.calls.append(url)
  if url.startswith('https://doi.org/'):
   return (404 if self.bad=='doi' else 200),b'','https://zenodo.org/records/999999999999'
  name=url.split('/files/',1)[1].split('/content',1)[0]
  raw=(self.f.package/name).read_bytes()
  if self.bad=='download':raw+=b'corrupt'
  return 200,raw,('http://zenodo.org/insecure' if self.bad=='insecure_download' else url)

def publisher(f,behavior=None,bad=None):
 k=FakeKit(f,behavior);h=FakePublic(f,bad);return p.Publisher(f.base,KIT,k,h),k,h
def published(f,behavior=None,bad=None):
 pub,k,h=publisher(f,behavior,bad)
 pub.invoke('stage')
 if behavior=='publish_lost':fails(lambda:pub.invoke('publish',k.id),'unknown publish is preserved')
 else:pub.invoke('publish',k.id)
 pub.invoke('inspect-doi',k.id)
 return pub,k,h

class FakeSheet:
 def __init__(self,f,behavior=None):
  self.f=f;self.behavior=behavior;self.calls=[];self.appends=0;self.full_reads=0
  self.data=[list(t.HEADERS),['foreign','','same','x'],['foreign','','same','x'],[True,1,'typed','retained']]
  if behavior=='preexisting_doi':self.data.append(['foreign note','','','DOI10.5281/zenodo.999999999999 already present'])
  self.before=copy.deepcopy(self.data)
 def run(self,resources,params,body=None):
  self.calls.append((resources,copy.deepcopy(params),copy.deepcopy(body)))
  check(params['spreadsheetId']==t.SID,'exact tracker spreadsheet')
  if resources==['spreadsheets','get']:
   value=dict(spreadsheetId=t.SID,sheets=[dict(properties=dict(sheetId=0 if self.behavior=='wrong_gid' else float(t.GID) if self.behavior=='float_gid' else t.GID,title=t.TAB,gridProperties=dict(rowCount=100,columnCount=4)))])
  elif resources[-1]=='append':
   self.appends+=1
   marker=self.f.base/'private_operations/tracker/APPEND_INFLIGHT.json'
   check(marker.exists() and marker_synced(marker),'append durable exclusive file and directory before fake request')
   check(params.get('valueInputOption')=='RAW' and params.get('insertDataOption')=='INSERT_ROWS' and body.get('majorDimension')=='ROWS' and len(body['values'])==1 and len(body['values'][0])==4,'single RAW INSERT_ROWS request')
   if self.behavior!='lost_before':self.data.append(copy.deepcopy(body['values'][0]))
   if self.behavior=='drop_foreign':self.data.pop(1)
   if self.behavior in ('lost_before','lost_after'):raise OSError('fake uncertain append')
   n=len(self.data)
   returned=copy.deepcopy(body['values'])
   if self.behavior=='bad_values':returned[0][0]='wrong response value'
   if self.behavior=='bad_range':n-=1
   value=dict(spreadsheetId=t.SID,updates=dict(updatedData=dict(values=returned),updatedRows=True if self.behavior=='boolean_count' else 1,updatedColumns=4,updatedCells=4,updatedRange="'Math Puzzles'!A"+str(n)+':D'+str(n)))
  else:
   if params['range']==t.FULL_RANGE:
    self.full_reads+=1
    if self.behavior=='between_reads' and self.full_reads==2:self.data.pop(1)
    if self.behavior=='shift_after_own_readback' and self.full_reads==3:self.data.insert(1,['new concurrent foreign','','','retained'])
    if self.behavior=='second_readback_foreign_loss' and self.full_reads==4:self.data.pop(1)
    if self.behavior=='second_readback_doi_loss' and self.full_reads==4:self.data.pop()
    value=dict(values=copy.deepcopy(self.data))
   else:
    n=int(params['range'].split('!A',1)[1].split(':D',1)[0]);value=dict(values=[copy.deepcopy(self.data[n-1])])
  return SimpleNamespace(returncode=0,stdout=json.dumps(value),stderr='')

def verified_publication(f):
 pub,k,h=published(f);pub.finalize();return pub,k,h

def run():
 # Every below fixture exists only inside the owned temporary work directory.
 # Synthetic source-adoption pins authorize no actual project operation.
 for name,mut in [
  ('missing explicit source adoption',lambda f:setattr(c,'_authority',None)),
  ('missing adoption file',lambda f:f.adoption_path.unlink()),
  ('adoption wrong HEAD',lambda f:(f.adoption.update(original_head='0'*40),f.write_adoption())),
  ('adoption lacks exact source set',lambda f:(f.adoption['sources'].pop(c.OWN+'/run_offline.py'),f.write_adoption())),
  ('changed adopted source copy',lambda f:write(f.base/c.OWN/'publisher206.py',b'changed source')),
  ('stale approved gate',lambda f:write(f.gp,f.gate|{'fixture_changed':True})),
 ]:
  with fixture() as f:
   mut(f);pub,k,h=publisher(f)
   fails(lambda:pub.invoke('stage'),name+' refused')
   check(not k.calls,name+' zero transports')
 with fixture() as f:
  escape=f.base/'synthetic_escape';escape.mkdir();(f.base/'private_operations').symlink_to(escape,target_is_directory=True)
  pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'symlinked private ancestor refused')
  check(not k.calls and not list(escape.iterdir()),'symlink private ancestor zero transports/output')
 with fixture() as f:
  pub,k,h=published(f);private=f.base/'private_operations';escape=f.base/'synthetic_private_saved'
  private.rename(escape);private.symlink_to(escape,target_is_directory=True)
  fails(pub.finalize,'finalize-only private symlink ancestor rejected')
  check(not h.calls and not (f.base/'ROOT_PUBLICATION_RECEIPT.json').exists(),'finalize symlink rejected before public HTTP/receipt')
 with fixture(metadata_file='synthetic-deposit-manifest.json') as f:
  pub,k,h=published(f);r=pub.finalize()
  check(r['context']['manifest_pin']==c.pin(f.package/'synthetic-deposit-manifest.json') and 'synthetic-attributed-evidence.zip' in r['verified_public_download_names'],'dynamic exact manifest and ZIP basename supported')
 with fixture() as f:
  for event in f.events:
   (f.base/event['directory']/event['report_file']).chmod(0o644)
   (f.base/event['Root_acceptance_file']).chmod(0o644)
  pub,k,h=publisher(f);pub.invoke('stage')
  check(k.stage_count==1,'exact Root-accepted review bytes permit original 0644 permissions')
 for changed in ('report','Root_acceptance'):
  with fixture() as f:
   event=f.events[0]
   target=f.base/event['directory']/event['report_file'] if changed=='report' else f.base/event['Root_acceptance_file']
   target.chmod(0o644);target.write_bytes(b'changed review input')
   pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'0644 '+changed+' tamper rejected')
   check(not k.calls,'changed '+changed+' input no child transport')
 with fixture() as f:
  event=f.events[0];target=f.base/event['directory']/event['report_file'];target.unlink();target.symlink_to(f.package/'synthetic-focal-inversion.pdf')
  pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'symlinked review input rejected')
  check(not k.calls,'symlinked review no child transport')
 mutations=[
 ('wrong gate HEAD',lambda f:f.change_gate('original_head','f'*40)),
 ('unsupported theorem novelty',lambda f:f.change_gate('theorem_novelty_cleared',True)),
 ('missing portable acceptance',lambda f:f.change_gate('current_portable_verifier_accepted',False)),
 ('missing editorial acceptance',lambda f:f.change_gate('qualified_attributed_note_editorially_cleared',False)),
 ('wrong actual original draft HEAD',lambda f:f.acceptance.update(actual_original_PR_head='0'*40)),
 ('original PR is no longer draft',lambda f:f.acceptance.update(actual_original_PR_is_draft=False)),
 ('original PR is no longer open',lambda f:f.acceptance.update(actual_original_PR_state='closed')),
 ('author-only readiness is insufficient',lambda f:f.acceptance.update(evidence_scope='LOCAL_AUTHOR_PREPARATION')),
 ('missing mathematical clearance',lambda f:f.change_gate('mathematical_clearance',False)),
 ('legacy whole scope alias alone',lambda f:(f.events[-1].pop('whole_package_scope'),f.events[-1].update(whole_scope=True))),
 ('preparation role wrong pin',lambda f:f.gate['preparation_receipts']['priority'].update(sha256='0'*64)),
 ('manifest metadata mismatch',lambda f:f.gate['metadata'].update(title='Different title')),
 ('wrong gate PR',lambda f:f.change_gate('PR',203)),
 ('only one review',lambda f:f.change_gate('whole_package_review_events',f.events[:1])),
 ('historical priority false required',lambda f:f.change_gate('historical_priority_established',True)),
 ('last verdict nonclean',lambda f:f.events[-1].update(verdict='ISSUES')),
 ('fresh report absent',lambda f:f.events[-1]['safe_files'].clear()),
 ('wrong ready HEAD',lambda f:f.acceptance.update(original_head='0'*40)),
 ('ready package drift',lambda f:f.acceptance.update(package='publication_package_stale')),
 ('pointer MAIN drift',lambda f:f.pointer.update(main_observed='e'*40)),
 ('historical firstness falsely accepted',lambda f:f.acceptance.update(historical_firstness_independence_established=True)),
 ('supporting input missing from selected map',lambda f:f.selected.pop(c.PREFIX+'synthetic_inputs/priority.json')),
 ('review missing from selected map',lambda f:f.selected.pop(c.PREFIX+f.events[0]['directory']+'/REPORT.md')),
 ('wrong ready PR',lambda f:f.pointer.update(PR=203)),
 ('foreign scope unaccepted',lambda f:f.acceptance.update(full_foreign_tree_scope_preserved=False)),
 ('not actual ready90',lambda f:f.acceptance.update(case_percent=80)),
 ('gate missing from selected map',lambda f:f.selected.pop(c.PREFIX+'ROOT_PUBLICATION_GATE_01.json')),
 ('package missing from selected map',lambda f:f.selected.pop(c.PREFIX+f.package.name+'/synthetic-focal-inversion.pdf')),
 ]
 for name,mut in mutations:
  with fixture() as f:
   mut(f)
   # Save mutated fixture data without forging any real project gate.
   write(f.gp,f.gate);f.reapprove_gate();f.rebind_map()
   pub,k,h=publisher(f)
   fails(lambda:pub.invoke('stage'),name+' rejected before transport')
   check(not k.calls,name+' makes zero child calls')
 for missing in ('ROOT_PUBLICATION_GATE_01.json','ROOT_ACTUAL_READY_CHECKPOINT.json'):
  with fixture() as f:
   (f.base/missing).unlink();pub,k,h=publisher(f)
   fails(lambda:pub.invoke('stage'),'missing '+missing+' fails closed');check(not k.calls,'missing local gate/ready zero child')
 with fixture() as f:
  write(f.package/'synthetic-focal-inversion.pdf',b'changed')
  pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'changed package fails before child');check(not k.calls,'changed package zero child')
 with fixture() as f:
  write(f.package/'unreviewed-extra.txt',b'extra')
  pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'extra package file refused');check(not k.calls,'extra file zero transports')
 with fixture() as f:
  event=f.events[0];ap=f.base/event['Root_acceptance_file'];a=c.read(ap);a['review_accepted']=False
  write(ap,a);event['Root_acceptance_pin']=c.pin(ap);write(f.gp,f.gate);f.reapprove_gate();f.rebind_map()
  pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'pinned unaccepted Root review body refused');check(not k.calls,'unaccepted Root review zero transports')
 with fixture() as f:
  fakekit=write(f.base/'fake_kit.py',b'never execute')
  k=FakeKit(f);pub=p.Publisher(f.base,fakekit,k,FakePublic(f))
  fails(lambda:pub.invoke('stage'),'changed KIT SHA rejects');check(not k.calls,'changed KIT zero child')
 with fixture() as f:
  pub,k,h=published(f);r=pub.finalize()
  check(r['package']=='publication_package_v7' and len(h.calls)==4 and r['actual_publication_verified'],'dynamic package finalizes only three downloads plus actual DOI')
  fails(lambda:pub.invoke('publish',k.id),'publication repeat prohibited')
  check(k.stage_count==k.publish_count==1,'each fake mutation exactly once')
 with fixture() as f:
  pub,k,h=publisher(f,'stage_lost')
  fails(lambda:pub.invoke('stage'),'unknown stage recorded')
  fails(lambda:pub.invoke('stage'),'unknown stage automatic retry prohibited')
  pub.invoke('inspect',k.id);pub.invoke('publish',k.id);pub.invoke('inspect-doi',k.id);pub.finalize()
  check(k.stage_count==k.publish_count==1,'unknown stage resolved by known-ID read-only inspect')
 with fixture() as f:
  pub,k,h=published(f,'publish_lost')
  fails(lambda:pub.invoke('publish',k.id),'unknown publish automatic retry prohibited')
  pub.finalize();check(k.publish_count==1,'unknown publish read-only recovery never repeats')
 with fixture() as f:
  pub,k,h=publisher(f,'inspect_lost');pub.invoke('stage')
  fails(lambda:pub.invoke('inspect',k.id),'failed read-only inspection captured')
  pub.invoke('inspect',k.id)
  check((pub.directory/'inspect_0001.raw.json').exists() and (pub.directory/'inspect_0002.json').exists(),'failed inspection consumes receipt index and later recovery succeeds')
 with fixture() as f:
  pub,k,h=publisher(f,'bad_metadata')
  fails(lambda:pub.invoke('stage'),'metadata normalization rejected')
  check((pub.directory/'STAGE_INFLIGHT.json').exists(),'metadata failure retains stage intent')
 with fixture() as f:
  pub,k,h=publisher(f);pub.invoke('stage')
  fails(lambda:pub.invoke('publish',k.id+1),'wrong explicit known ID rejected')
  check(k.publish_count==0,'wrong publish confirmation no mutation')
  k.behavior='wrong_id';fails(lambda:pub.invoke('inspect',k.id),'different inspected ID rejected')
 for bad in ('download','doi','insecure_download'):
  with fixture() as f:
   pub,k,h=published(f,bad=bad);fails(pub.finalize,'public '+bad+' corruption rejects finalization')
   check(not (f.base/'ROOT_PUBLICATION_RECEIPT.json').exists(),'no public receipt after '+bad+' failure')
 with fixture() as f:
  sheet=FakeSheet(f);fails(lambda:t.Tracker(f.base,sheet).run(),'tracker requires actual verified publication')
  check(not sheet.calls,'unpublished tracker zero sheet calls')
 with fixture() as f:
  verified_publication(f);sheet=FakeSheet(f);r=t.Tracker(f.base,sheet).run()
  check(sheet.appends==1 and r['row'][1]=='' and r['foreign_rows_retained'],'single append blank B and foreign multiplicities retained')
  check(t.retained(t.rows(dict(values=sheet.before)),t.rows(dict(values=sheet.data))),'all original foreign row multiplicities survive')
  check(all(x in r['row'][3] for x in ('Ferudun','10.5281/zenodo.23096994','No theorem/formula/method novelty','Extensive AI','odd primitive','PR206')),'truthful attributed tracker notes')
  fails(lambda:t.Tracker(f.base,sheet).run(),'verified tracker never appends again');check(sheet.appends==1,'one successful append total')
 for field in ('context','public_downloads'):
  with fixture() as f:
   verified_publication(f);rp=f.base/'ROOT_PUBLICATION_RECEIPT.json';r=c.read(rp)
   if field=='context':r[field]['checkpoint_commit']='e'*40
   else:r[field][0]['sha256']='0'*64
   write(rp,r);sheet=FakeSheet(f)
   fails(lambda:t.Tracker(f.base,sheet).run(),'changed public receipt '+field+' rejected')
   check(not sheet.calls,'public receipt '+field+' rejection before tracker transport')
 for bad in ('wrong_gid','float_gid','between_reads','preexisting_doi'):
  with fixture() as f:
   verified_publication(f);sheet=FakeSheet(f,bad)
   fails(lambda:t.Tracker(f.base,sheet).run(),bad+' fails before append')
   check(sheet.appends==0,bad+' zero append')
 with fixture() as f:
  verified_publication(f);sheet=FakeSheet(f,'lost_after');tr=t.Tracker(f.base,sheet)
  fails(tr.run,'lost append response preserves uncertainty')
  marker=tr.directory/'APPEND_INFLIGHT.json';mp=c.pin(marker);baseline=tr.directory/c.read(marker)['original_preappend_baseline']['file'];bp=c.pin(baseline)
  r=tr.run(True)
  check(r['recovered_unknown_outcome'] and sheet.appends==1,'unknown successful append recovery is read-only')
  check(c.pin(marker)==mp and c.pin(baseline)==bp,'original inflight and full baseline pins unchanged')
 with fixture() as f:
  verified_publication(f);sheet=FakeSheet(f,'lost_before');tr=t.Tracker(f.base,sheet)
  fails(tr.run,'unknown unsuccessful append recorded');fails(lambda:tr.run(True),'missing own row recovery fails closed')
  check(sheet.appends==1,'unknown unsuccessful append never retried')
 with fixture() as f:
  verified_publication(f);sheet=FakeSheet(f,'drop_foreign');tr=t.Tracker(f.base,sheet)
  fails(tr.run,'loss of one duplicate foreign row rejected')
  fails(lambda:tr.run(True),'original baseline defeats later foreign-loss recovery')
  check(sheet.appends==1,'foreign-loss failure does not append again')
 with fixture() as f:
  verified_publication(f);sheet=FakeSheet(f,'lost_after');tr=t.Tracker(f.base,sheet)
  fails(tr.run,'tamper scenario original uncertain append')
  marker=c.read(tr.directory/'APPEND_INFLIGHT.json');baseline=tr.directory/marker['original_preappend_baseline']['file'];baseline.write_bytes(b'tamper')
  before=len(sheet.calls);fails(lambda:tr.run(True),'changed original baseline rejected')
  check(len(sheet.calls)==before,'tampered baseline rejection before sheet reads')
 with fixture() as f:
  verified_publication(f);sheet=FakeSheet(f,'boolean_count');tr=t.Tracker(f.base,sheet)
  fails(tr.run,'boolean append count rejected despite integer equality')
  check(sheet.appends==1 and (tr.directory/'APPEND_INFLIGHT.json').exists(),'bad append counts preserve intent without retry')
 fails(lambda:t.rows(dict(values=[[1,2,3,4,5]])),'overwide foreign row never truncated')
 fails(lambda:t.rows(dict(values=[[dict(x=1)]])),'nested foreign cell rejected')
 fails(lambda:t.rows(dict(values=[[float('nan')]])),'nonfinite foreign cell rejected')
 check(t.counted([(True,'','','')])!=t.counted([(1,'','','')]),'Counter distinguishes bool and numeric foreign rows')
 check(not t.retained([('x','','',''),('x','','','')],[('x','','','')]),'Counter preserves duplicate foreign row multiplicity')
 with fixture(upload_stem='new-final-versioned-manuscript') as f:
  pub,k,h=published(f);r=pub.finalize()
  check(set(r['verified_public_download_names'])==f.names,'final manuscript basenames derive only from exact gate')
 with fixture(metadata_description='SYNTHETIC missing mandatory overlap credit') as f:
  pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'missing Ferudun exact-overlap metadata credit rejected')
  check(not k.calls,'missing overlap credit zero transport')
 for field in ('ROOT_PRIORITY_EDITORIAL_GATE_01.json','ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json'):
  with fixture() as f:
   f.gate['other_safe_files'].pop(field);write(f.gp,f.gate);f.reapprove_gate();f.rebind_map()
   pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'missing accepted original fact '+field)
   check(not k.calls,'missing accepted original fact zero transport '+field)
 for bad in ('bad_range','bad_values','second_readback_foreign_loss','second_readback_doi_loss'):
  with fixture() as f:
   verified_publication(f);sheet=FakeSheet(f,bad);tr=t.Tracker(f.base,sheet)
   fails(tr.run,bad+' rejects tracker receipt')
   check(sheet.appends==1 and not (f.base/'ROOT_TRACKER_RECEIPT.json').exists(),bad+' retains unique inflight without acceptance')
   if bad in ('bad_range','bad_values'):
    recovered=tr.run(True);check(recovered['recovered_unknown_outcome'],bad+' resolves only by fresh read-only recovery')
   else:fails(lambda:tr.run(True),bad+' unknown outcome cannot be accepted')
   check(sheet.appends==1,bad+' one append total')
 for value in (1,'truthy',float('nan'),float('inf')):
  fails(lambda value=value:c.require(value,'invalid predicate'),'nonboolean success guard rejected '+type(value).__name__)
 with fixture() as f:
  pub,k,h=publisher(f);state=f.base/'SYNTHETIC_PREEXISTING_KIT_STATE.json';write(state,dict(synthetic_fixture_only=True))
  pub.kit_state_path=lambda context,kit:state
  fails(lambda:pub.invoke('stage'),'prior kit state evidence blocks a new stage')
  check(not k.calls,'prior kit state zero transports')
 with fixture() as f:
  pub,k,h=publisher(f);pub.invoke('stage');k.published=True;pub.invoke('inspect',k.id)
  fails(lambda:pub.invoke('publish',k.id),'known published inspection blocks publish invocation')
  check(k.publish_count==0,'known published no new publish call')
 with fixture() as f:
  verified_publication(f);sheet=FakeSheet(f)
  fails(lambda:t.Tracker(f.base,sheet).run(1),'nonboolean recovery selector rejected before reads')
  check(not sheet.calls,'invalid recovery selector zero transport')
  target=f.base/'must_not_be_created.json'
  fails(lambda:c.durable_json(target,{},readonly='false'),'nonboolean durable readonly selector rejected')
  check(not target.exists(),'invalid readonly selector creates no file')
 findings=[]
 with fixture() as f:
  verified_publication(f);sheet=FakeSheet(f,'shift_after_own_readback');tr=t.Tracker(f.base,sheet)
  try:r=tr.run()
  except (RuntimeError,TypeError):check(True,'Root final-row-shift probe rejected before receipt')
  else:
   actual=t.hits(t.rows(dict(values=sheet.data)),r['doi'])[0]
   actual_range="'Math Puzzles'!A"+str(actual)+':D'+str(actual)
   if r['range']!=actual_range:
    findings.append('stale final tracker range '+r['range']+' vs '+actual_range)
    c.durable_json(HERE/('RACE_FALSE_ACCEPT_'+str(sys.flags.optimize)+'.json'),dict(synthetic_fixture_only=True,offline_only=True,recorded_range=r['range'],actual_range=actual_range,fake_receipt=r))
 with fixture() as f:
  original=c.pin(f.adoption_path);old_pointer=c.pin(f.base/'ROOT_ACTUAL_READY_CHECKPOINT.json')
  f.acceptance['checkpoint_commit']='e'*40;f.acceptance['main_observed']='e'*40
  f.pointer['checkpoint_commit']='e'*40;f.pointer['main_observed']='e'*40
  f.write_acceptance(reapprove=False)
  check(c.pin(f.adoption_path)==original,'Root replacement probe leaves original adoption unchanged')
  try:replacement=f.context()
  except (RuntimeError,TypeError):check(True,'Root unchanged-adoption ready-chain replacement rejected')
  else:
   findings.append('self-consistent replacement ready chain accepted under unchanged adoption')
   c.durable_json(HERE/('READY_CHAIN_FALSE_ACCEPT_'+str(sys.flags.optimize)+'.json'),dict(synthetic_fixture_only=True,offline_only=True,unchanged_adoption_pin=original,original_ready_pointer_pin=old_pointer,replaced_ready_pointer_pin=c.pin(f.base/'ROOT_ACTUAL_READY_CHECKPOINT.json'),accepted_checkpoint_commit=replacement['checkpoint_commit']))
 with fixture() as f:
  old=c.pin(f.adoption_path);f.selected.pop(next(iter(f.selected)));f.rebind_map(reapprove=False)
  check(c.pin(f.adoption_path)==old,'Root truncated map probe keeps adoption fixed')
  fails(f.context,'truncated self-consistent map chain rejected under fixed adoption')
 check(not findings,'Root requested false-accept probes: '+str(findings))
 with fixture() as f:
  path=write(f.base/'pinned_decode.json',dict(synthetic=True,expected=1));wanted=c.pin(path)
  write(path,dict(synthetic=True,unexpected=2));decoded=[];original_loads=c.json.loads
  def counted_loads(*args,**kwargs):decoded.append(True);return original_loads(*args,**kwargs)
  c.json.loads=counted_loads
  try:fails(lambda:c.read_pinned(path,wanted),'pinned JSON changed bytes reject before parsing')
  finally:c.json.loads=original_loads
  check(not decoded,'pin failure never interprets unverified JSON')
  valid=c.encoded(dict(expected=True))
  class Once:
   def __init__(self):self.calls=0
   def read_bytes(self):self.calls+=1;return valid if self.calls==1 else b'wrong replacement'
  once=Once();got=c.read_pinned(once,dict(bytes=len(valid),sha256=c.digest(valid)))
  check(got==dict(expected=True) and once.calls==1,'pinned JSON parses exactly the one authenticated buffer')
 check(not REAL_CALLS,'no real process or network transports launched')
 check(not list(WORK.iterdir()),'all disposable fixture directories removed')
 return dict(status='PASS',offline_only=True,optimization_flag=sys.flags.optimize,active_checks=len(CHECKS),checks=CHECKS,real_process_or_network_calls=len(REAL_CALLS),all_fake_fixture_directories_removed=True,limits='Offline guarded helper preparation only; no mathematical, publication, credential, remote API, or real tracker clearance.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args()
 result=run();c.durable_json(a.output,result)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
