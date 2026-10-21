"""Offline-only PR204 guards and uncertain-outcome recovery with fake transports."""
import sys
sys.dont_write_bytecode=True
import argparse,copy,contextlib,json,os,pathlib,shutil,stat,subprocess,tempfile,urllib.request
from types import SimpleNamespace
import operations_common as c
import publish_exact as p
import update_tracker as t

HERE=pathlib.Path(__file__).resolve().parent
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

KIT=p.locate_kit(HERE.parent)
check(c.pin(KIT)['sha256']==c.KIT_SHA,'read-only original KIT SHA pinned; never launched')
WORK=HERE/'offline_work'
WORK.mkdir(exist_ok=True)

class Fixture:
 def __init__(self,root):
  self.base=root/'pr204_5100012';self.base.mkdir()
  self.package=self.base/'publication_package_v7';self.package.mkdir()
  self.metadata=dict(title='Centered original-side pedal-area product: an attributed verification note',creators=[dict(name='Kriebel, Alec',orcid='0009-0001-9320-500X')],description='Offline fixture only.')
  for name in sorted(c.UPLOADS):write(self.package/name,('offline fixture '+name+'\n').encode())
  write(self.package/'zenodo-deposit.json',dict(metadata=self.metadata,files=[dict(path=x) for x in sorted(c.UPLOADS)]))
  write(self.package/'PACKAGE_SEAL.json',dict(offline=True))
  safe={x.name:c.pin(x) for x in self.package.iterdir()}
  self.events=[]
  for i in (1,2):
   rd=self.base/('fresh_review_'+str(i));write(rd/'REPORT.md',b'OFFLINE CLEANPASS fixture\n')
   ap=write(self.base/('ROOT_REVIEW_ACCEPTANCE_'+str(i)+'.json'),dict(offline=True,review=i))
   self.events.append(dict(review_number=i,directory=rd.name,report_file='REPORT.md',safe_files={'REPORT.md':c.pin(rd/'REPORT.md')},Root_acceptance_file=ap.name,Root_acceptance_pin=c.pin(ap),reviewed_package=self.package.name,reviewed_package_seal=safe['PACKAGE_SEAL.json'],verdict='CLEANPASS'))
  self.gate=dict(PR=204,problem_id=5100012,publication_ready_gate_accepted=True,whole_package_review_loop_complete=True,historical_priority_established=False,whole_package_review_events=self.events,package=self.package.name,package_seal=safe['PACKAGE_SEAL.json'],package_safe_files=safe,metadata=self.metadata,intended_upload_files={n:safe[n] for n in sorted(c.UPLOADS)})
  self.gp=self.base/'ROOT_PUBLICATION_GATE_01.json';write(self.gp,self.gate)
  self.checkpoint=self.base/'publication_checkpoint_01/ready90_99';self.checkpoint.mkdir(parents=True)
  selected={c.PREFIX+'ROOT_PUBLICATION_GATE_01.json':c.native_identity(self.gp)}
  selected.update({c.PREFIX+self.package.name+'/'+n:c.native_identity(self.package/n) for n in safe})
  self.selected=selected
  self.acceptance=dict(PR=204,accepted=True,case_percent=90,checkpoint_commit='c'*40,main_observed='m'*40,selected_files=len(selected),historical_firstness_independence_established=False)
  for field in ['every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','QUEUE_native_original_PR_unchanged','mathematical_clearance','source_contract_clearance','priority_clearance','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','publication_ready']:self.acceptance[field]=True
  self.pointer=dict(PR=204,phase='ready',directory=self.checkpoint.relative_to(self.base).as_posix(),checkpoint_commit='c'*40,main_observed='m'*40,Root_recorded_only_after_actual_full_scope_acceptance=True)
  self.rebind_map()
 def rebind_map(self):
  sha=c.digest(json.dumps(self.selected,sort_keys=True,separators=(',',':')).encode())
  mp=write(self.checkpoint/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',dict(selected_files=self.selected,selected_map_sha256=sha))
  self.acceptance.update(selected_files=len(self.selected),actual_current_map_file=c.pin(mp),actual_current_selected_map_sha256=sha)
  self.write_acceptance()
 def write_acceptance(self):
  ap=write(self.checkpoint/'ACCEPTANCE.json',self.acceptance);self.pointer['acceptance_pin']=c.pin(ap)
  write(self.base/'ROOT_ACTUAL_READY_CHECKPOINT.json',self.pointer)
 def change_gate(self,field,value):
  self.gate[field]=value;write(self.gp,self.gate)
 def context(self):return c.load_context(self.base)

@contextlib.contextmanager
def fixture():
 with tempfile.TemporaryDirectory(prefix='offline_',dir=WORK) as root:yield Fixture(pathlib.Path(root))

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
  return 200,raw,url

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
  self.before=copy.deepcopy(self.data)
 def run(self,resources,params,body=None):
  self.calls.append((resources,copy.deepcopy(params),copy.deepcopy(body)))
  check(params['spreadsheetId']==t.SID,'exact tracker spreadsheet')
  if resources==['spreadsheets','get']:
   value=dict(spreadsheetId=t.SID,sheets=[dict(properties=dict(sheetId=0 if self.behavior=='wrong_gid' else t.GID,title=t.TAB,gridProperties=dict(rowCount=100,columnCount=4)))])
  elif resources[-1]=='append':
   self.appends+=1
   marker=self.f.base/'private_operations/tracker/APPEND_INFLIGHT.json'
   check(marker.exists() and marker_synced(marker),'append durable exclusive file and directory before fake request')
   check(params.get('valueInputOption')=='RAW' and params.get('insertDataOption')=='INSERT_ROWS' and body.get('majorDimension')=='ROWS' and len(body['values'])==1 and len(body['values'][0])==4,'single RAW INSERT_ROWS request')
   if self.behavior!='lost_before':self.data.append(copy.deepcopy(body['values'][0]))
   if self.behavior=='drop_foreign':self.data.pop(1)
   if self.behavior in ('lost_before','lost_after'):raise OSError('fake uncertain append')
   n=len(self.data);value=dict(updates=dict(updatedRows=True if self.behavior=='boolean_count' else 1,updatedColumns=4,updatedCells=4,updatedRange="'Math Puzzles'!A"+str(n)+':D'+str(n)))
  else:
   if params['range']==t.FULL_RANGE:
    self.full_reads+=1
    if self.behavior=='between_reads' and self.full_reads==2:self.data.pop(1)
    value=dict(values=copy.deepcopy(self.data))
   else:
    n=int(params['range'].split('!A',1)[1].split(':D',1)[0]);value=dict(values=[copy.deepcopy(self.data[n-1])])
  return SimpleNamespace(returncode=0,stdout=json.dumps(value),stderr='')

def verified_publication(f):
 pub,k,h=published(f);pub.finalize();return pub,k,h

def run():
 # Every below fixture exists only inside the owned temporary work directory.
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
  event=f.events[0];target=f.base/event['directory']/event['report_file'];target.unlink();target.symlink_to(f.package/'centered_pedal_dn.pdf')
  pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'symlinked review input rejected')
  check(not k.calls,'symlinked review no child transport')
 mutations=[
 ('wrong gate PR',lambda f:f.change_gate('PR',203)),
 ('only one review',lambda f:f.change_gate('whole_package_review_events',f.events[:1])),
 ('historical priority false required',lambda f:f.change_gate('historical_priority_established',True)),
 ('last verdict nonclean',lambda f:f.events[-1].update(verdict='ISSUES')),
 ('fresh report absent',lambda f:f.events[-1]['safe_files'].clear()),
 ('wrong ready PR',lambda f:f.pointer.update(PR=203)),
 ('foreign scope unaccepted',lambda f:f.acceptance.update(full_foreign_tree_scope_preserved=False)),
 ('not actual ready90',lambda f:f.acceptance.update(case_percent=80)),
 ('gate missing from selected map',lambda f:f.selected.pop(c.PREFIX+'ROOT_PUBLICATION_GATE_01.json')),
 ('package missing from selected map',lambda f:f.selected.pop(c.PREFIX+f.package.name+'/centered_pedal_dn.pdf')),
 ]
 for name,mut in mutations:
  with fixture() as f:
   mut(f)
   # Save mutated fixture data without forging any real project gate.
   write(f.gp,f.gate);f.rebind_map()
   pub,k,h=publisher(f)
   fails(lambda:pub.invoke('stage'),name+' rejected before transport')
   check(not k.calls,name+' makes zero child calls')
 for missing in ('ROOT_PUBLICATION_GATE_01.json','ROOT_ACTUAL_READY_CHECKPOINT.json'):
  with fixture() as f:
   (f.base/missing).unlink();pub,k,h=publisher(f)
   fails(lambda:pub.invoke('stage'),'missing '+missing+' fails closed');check(not k.calls,'missing local gate/ready zero child')
 with fixture() as f:
  write(f.package/'centered_pedal_dn.pdf',b'changed')
  pub,k,h=publisher(f);fails(lambda:pub.invoke('stage'),'changed package fails before child');check(not k.calls,'changed package zero child')
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
 for bad in ('download','doi'):
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
  check(all(x in r['row'][3] for x in ('23085904','23400541','October1','neither firstness','Extensive AI','least N','PR204')),'truthful attributed tracker notes')
  fails(lambda:t.Tracker(f.base,sheet).run(),'verified tracker never appends again');check(sheet.appends==1,'one successful append total')
 for bad in ('wrong_gid','between_reads'):
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
 check(not REAL_CALLS,'no real process or network transports launched')
 check(not list(WORK.iterdir()),'all disposable fixture directories removed')
 return dict(status='PASS',offline_only=True,optimization_flag=sys.flags.optimize,active_checks=len(CHECKS),checks=CHECKS,real_process_or_network_calls=len(REAL_CALLS),all_fake_fixture_directories_removed=True,limits='Offline guarded helper preparation only; no mathematical, publication, credential, remote API, or real tracker clearance.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args()
 result=run();c.durable_json(a.output,result)
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
