"""SYNTHETIC_NON_RECEIPT. Independent final07 offline source falsification."""
import sys
sys.dont_write_bytecode=True
import ast,copy,hashlib,json,os,pathlib,stat,traceback,types
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import offline_guard
offline_guard.install()
SOURCE=ROOT/'authenticated_sources'
CASE=ROOT.parent
PINS=json.loads((ROOT/'REVIEWED_SOURCE_PINS.json').read_bytes())['sources_and_contract']
for name,w in PINS.items():
 raw=(SOURCE/name).read_bytes()
 if len(raw)!=w['bytes'] or hashlib.sha256(raw).hexdigest()!=w['sha256']:raise RuntimeError('source pin drift '+name)

def load(name):
 raw=(SOURCE/(name+'.py')).read_bytes();m=types.ModuleType(name);m.__file__=str(SOURCE/(name+'.py'));sys.modules[name]=m
 exec(compile(raw,m.__file__,'exec'),m.__dict__);return m
c=load('ops_common206');p=load('publisher206');t=load('tracker206')
KIT=pathlib.Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
if c.pin(KIT)!={'bytes':25740,'sha256':c.KIT_SHA}:raise RuntimeError('actual unchanged kit pin differs')
WORK=ROOT/('independent_work_O'+str(sys.flags.optimize));WORK.mkdir(exist_ok=False)
RESULTS=[];CURRENT=None;SYNC=[]
REAL_FSYNC=os.fsync

def tracked_fsync(fd):
 st=os.fstat(fd);SYNC.append((st.st_dev,st.st_ino,stat.S_ISDIR(st.st_mode)));return REAL_FSYNC(fd)
os.fsync=tracked_fsync

def check(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError('ASSERTION:'+msg)
 CURRENT['checks'].append(msg)
def denied(fn,msg):
 try:fn()
 except Exception as e:
  check(True,msg);CURRENT['rejections'].append({'probe':msg,'type':type(e).__name__,'message':str(e)[:300]});return e
 raise RuntimeError('FALSE_ACCEPT:'+msg)
def write(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():path.chmod(0o600)
 path.write_bytes(obj if type(obj) is bytes else c.encoded(obj));path.chmod(0o444);return path

def synced(path):
 s=path.stat();d=path.parent.stat();return (s.st_dev,s.st_ino,False) in SYNC and (d.st_dev,d.st_ino,True) in SYNC

class Fixture:
 def __init__(self,fullmap=False):
  self.base=WORK/CURRENT['id'];self.base.mkdir();self.package=self.base/'synthetic_package';self.package.mkdir()
  packet=json.loads((CASE/'ROOT_WHOLE_PACKAGE_PACKET_01.json').read_bytes())
  # The byte payload is the already frozen public package; the enclosing authority is synthetic only.
  for name in packet['all_package_files']:write(self.package/name,(CASE/'publication_package_v1'/name).read_bytes())
  self.metadata=json.loads((self.package/'zenodo-deposit.json').read_bytes())['metadata'];self.metadata['title']='SYNTHETIC_NON_RECEIPT '+self.metadata['title']
  self.upload=copy.deepcopy(packet['upload_files']);write(self.package/'zenodo-deposit.json',{'metadata':self.metadata,'files':[{'path':n} for n in self.upload]})
  self.safe={n:c.pin(self.package/n) for n in packet['all_package_files']}
  self.other={};self.roles={}
  for role in ('mathematics','priority','portable','package','visual'):
   name='synthetic_support/'+role+'.json';q=write(self.base/name,{'SYNTHETIC_NON_RECEIPT':True,'role':role});self.other[name]=c.pin(q);self.roles[role]={'path':name,**c.pin(q)}
  for name in ('ROOT_PRIORITY_EDITORIAL_GATE_01.json','ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json'):
   q=write(self.base/name,(CASE/name).read_bytes());self.other[name]=c.pin(q)
  self.events=[]
  for i in (1,2):
   d='SYNTHETIC_NEW_WHOLE_REVIEW_'+str(i);r=write(self.base/d/'REPORT.md',b'SYNTHETIC_NON_RECEIPT independent fixture report\n')
   e={'review_number':i,'directory':d,'report_file':'REPORT.md','safe_files':{'REPORT.md':c.pin(r)},'report_pin':c.pin(r),'reviewed_package':self.package.name,'reviewed_package_seal':self.safe['PACKAGE_SEAL.json'],'verdict':'CLEANPASS','whole_package_scope':True,'open_findings':0}
   a=write(self.base/('SYNTHETIC_REVIEW_ACCEPTANCE_'+str(i)+'.json'),{'SYNTHETIC_NON_RECEIPT':True,'PR':206,'original_head':c.HEAD,'review_accepted':True,'NEW_whole_package_reviews_completed':i,'review_cycle_repairs_required_now':False,'review_event':copy.deepcopy(e)})
   self.events.append(e|{'Root_acceptance_file':a.name,'Root_acceptance_pin':c.pin(a)})
  self.gate={'SYNTHETIC_NON_RECEIPT':True,'PR':206,'problem_id':5100062,'original_head':c.HEAD,'whole_package_review_events':self.events,'package':self.package.name,'package_seal':self.safe['PACKAGE_SEAL.json'],'package_safe_files':self.safe,'metadata':self.metadata,'intended_upload_files':self.upload,'other_safe_files':self.other,'preparation_receipts':self.roles}
  for field in ('publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','bounded_priority_audit_complete','current_portable_verifier_accepted','qualified_attributed_note_editorially_cleared'):self.gate[field]=True
  self.gp=self.base/'ROOT_PUBLICATION_GATE_01.json';write(self.gp,self.gate)
  self.selected=copy.deepcopy(json.loads((CASE/'custody_checkpoint_02/custody10_03/ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())['selected_files']) if fullmap else {}
  self.ready=self.base/'SYNTHETIC_READY90';self.ready.mkdir()
  self.ac={'SYNTHETIC_NON_RECEIPT':True,'schema':'pr206-lifecycle-actual-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':206,'original_head':c.HEAD,'case_percent':90,'actual_original_PR_head':c.HEAD,'actual_original_PR_is_draft':True,'actual_original_PR_state':'open','historical_firstness_independence_established':False,'package':self.package.name,'package_seal':self.safe['PACKAGE_SEAL.json'],'checkpoint_commit':'c'*40,'main_observed':'c'*40}
  for field in ('accepted','every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','QUEUE_native_original_PR_unchanged','mathematical_clearance','source_contract_clearance','priority_clearance','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','publication_ready'):self.ac[field]=True
  self.pointer={'SYNTHETIC_NON_RECEIPT':True,'schema':'pr206-lifecycle-actual-pointer-v1','PR':206,'phase':'ready','Root_recorded_only_after_actual_full_scope_acceptance':True,'directory':self.ready.name,'checkpoint_commit':'c'*40,'main_observed':'c'*40}
  for name in c.CODES:write(self.base/c.OWN/name,(SOURCE/name).read_bytes())
  self.adopt={'SYNTHETIC_NON_RECEIPT':True,'schema':'pr206-root-publication-operations-adoption-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted_preparation_only':True,'PR':206,'original_head':c.HEAD,'sources':{c.OWN+'/'+n:c.pin(SOURCE/n) for n in c.CODES}}
  self.refresh()
 def inputs(self):
  d={'ROOT_PUBLICATION_GATE_01.json':self.gp};d.update({self.package.name+'/'+n:self.package/n for n in self.safe});d.update({n:self.base/n for n in self.other})
  for e in self.events:
   d.update({e['directory']+'/'+n:self.base/e['directory']/n for n in e['safe_files']});d[e['Root_acceptance_file']]=self.base/e['Root_acceptance_file']
  return d
 def refresh(self,gate=True,inputs=True,adopt=True):
  if gate:write(self.gp,self.gate)
  if inputs:self.selected.update({c.PREFIX+n:c.native_identity(q) for n,q in self.inputs().items()})
  md=c.digest(json.dumps(self.selected,sort_keys=True,separators=(',',':')).encode());mp=write(self.ready/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',{'selected_files':self.selected,'selected_map_sha256':md})
  self.ac.update(Root_publication_gate_pin=c.pin(self.gp),actual_current_map_file=c.pin(mp),actual_current_selected_map_sha256=md,selected_files=len(self.selected))
  ap=write(self.ready/'ACCEPTANCE.json',self.ac);self.pointer['acceptance_pin']=c.pin(ap);rp=write(self.base/'ROOT_ACTUAL_READY_CHECKPOINT.json',self.pointer)
  if adopt:
   self.adopt.update(approved_publication_gate_pin=c.pin(self.gp),approved_actual_ready_pointer_pin=c.pin(rp));self.authorize()
 def authorize(self):
  ap=write(self.base/'SYNTHETIC_OPS_ADOPTION.json',self.adopt);c.configure_authority(ap.name,c.pin(ap))
 def context(self):return c.load_context(self.base)
 def publisher(self,behavior=None,public_behavior=None):
  k=Kit(self,behavior);h=Public(self,public_behavior);return p.Publisher(self.base,KIT,k,h),k,h
 def published(self):
  pub,k,h=self.publisher();pub.invoke('stage');pub.invoke('publish',k.id);pub.invoke('inspect-doi',k.id);pub.finalize();return pub,k,h

class Kit:
 def __init__(self,f,behavior=None):self.f=f;self.behavior=behavior;self.calls=[];self.mutations=[];self.id=999999999998;self.published=False
 def run(self,argv,env):
  mode=argv[6];self.calls.append(mode)
  check(argv[:6]==[sys.executable,'-E','-S','-B','-P',str(KIT)],'actual kit argv pinned but intercepted')
  if mode in ('stage','publish'):
   m=self.f.base/'private_operations/zenodo'/(mode.upper()+'_INFLIGHT.json');check(m.exists() and synced(m),'create-only marker file and directory fsynced before '+mode);self.mutations.append(mode)
   if mode=='publish':self.published=True
  if self.behavior=='timeout' and mode=='stage':raise TimeoutError('SYNTHETIC timeout after mutation')
  j={'environment':'production','id':self.id,'state':'published' if self.published else 'ready_to_publish','title':self.f.metadata['title'],'metadata_normalizations':[],'files':[{'name':n,'size':w['bytes'],'sha256':w['sha256']} for n,w in self.f.upload.items()]}
  if self.published:j.update(record_url='https://zenodo.org/records/'+str(self.id),doi='10.5281/zenodo.'+str(self.id),doi_url='https://doi.org/10.5281/zenodo.'+str(self.id),doi_resolution={'status':'resolved','http_status':200})
  if self.behavior=='stage_published' and mode=='stage':j['state']='published'
  if self.behavior=='bad_metadata':j['metadata_normalizations']=['SYNTHETIC wrong creator']
  if self.behavior=='bad_title':j['title']+='corrupt'
  if self.behavior=='bad_file':j['files'][1]['sha256']='0'*64
  if self.behavior=='missing_file':j['files'].pop()
  if self.behavior=='extra_file':j['files'].append(j['files'][0])
  if self.behavior=='wrong_id' and mode=='inspect':j['id']+=1
  if self.behavior=='drift':write(self.f.gp,self.f.gate|{'postlaunch_drift':True})
  if self.behavior=='malformed':return types.SimpleNamespace(returncode=0,stdout='{',stderr='')
  if self.behavior=='partial':return types.SimpleNamespace(returncode=0,stdout='{}',stderr='')
  if self.behavior=='exit_error':return types.SimpleNamespace(returncode=7,stdout=json.dumps(j),stderr='SYNTHETIC error')
  return types.SimpleNamespace(returncode=0,stdout=json.dumps(j),stderr='')

class Public:
 def __init__(self,f,behavior=None):self.f=f;self.behavior=behavior;self.calls=[]
 def get(self,url,limit):
  self.calls.append(url)
  if self.behavior=='timeout':raise TimeoutError('SYNTHETIC public read timeout')
  if url.startswith('https://doi.org/'):
   target='https://zenodo.org/records/999999999998'
   if self.behavior=='wrong_doi':target='https://zenodo.org/records/999999999997'
   if self.behavior=='wrong_host':target='https://example.invalid/records/999999999998'
   return 404 if self.behavior=='resolver404' else 200,b'',target
  name=url.split('/files/')[1].split('/content')[0];raw=(self.f.package/name).read_bytes()
  if self.behavior=='hash':raw=raw[:-1]+bytes([raw[-1]^1])
  if self.behavior=='partial':raw=raw[:-1]
  return 200,raw,('http://zenodo.org/insecure' if self.behavior=='insecure' else url)

class Sheet:
 def __init__(self,f,behavior=None):
  self.f=f;self.behavior=behavior;self.calls=[];self.appends=0;self.full=0
  self.data=[list(t.HEADERS),['foreign','','','retain'],['foreign','','','retain'],[True,1,1.0,'typed'],['blank foreign','','','']];self.before=copy.deepcopy(self.data)
 def run(self,resources,params,body=None):
  self.calls.append({'resources':resources,'params':copy.deepcopy(params),'body':copy.deepcopy(body)})
  check(params['spreadsheetId']==t.SID,'exact spreadsheet id')
  if resources==['spreadsheets','get']:
   value={'spreadsheetId':t.SID,'sheets':[{'properties':{'sheetId':t.GID,'title':t.TAB,'gridProperties':{'rowCount':1000,'columnCount':4}}}]}
   if self.behavior=='wrong_gid':value['sheets'][0]['properties']['sheetId']+=1
   if self.behavior=='float_gid':value['sheets'][0]['properties']['sheetId']=float(t.GID)
   if self.behavior=='wrong_tab':value['sheets'][0]['properties']['title']='Wrong'
  elif resources[-1]=='append':
   self.appends+=1;m=self.f.base/'private_operations/tracker/APPEND_INFLIGHT.json';check(synced(m),'tracker inflight file and directory fsynced before mutation')
   check(params==dict(spreadsheetId=t.SID,range=t.FULL_RANGE,valueInputOption='RAW',insertDataOption='INSERT_ROWS',includeValuesInResponse=True) and body['majorDimension']=='ROWS' and len(body['values'])==1 and len(body['values'][0])==4,'only one four-cell RAW INSERT_ROWS append')
   if self.behavior!='lost_before':self.data.append(copy.deepcopy(body['values'][0]))
   if self.behavior in ('lost_before','lost_after'):raise TimeoutError('SYNTHETIC unknown append outcome')
   n=len(self.data);value={'spreadsheetId':t.SID,'updates':{'updatedRows':1,'updatedColumns':4,'updatedCells':4,'updatedRange':f"'Math Puzzles'!A{n}:D{n}",'updatedData':{'values':copy.deepcopy(body['values'])}}}
   if self.behavior=='range':value['updates']['updatedRange']=f"'Math Puzzles'!A{n+1}:D{n+1}"
   if self.behavior=='boolcount':value['updates']['updatedRows']=True
   if self.behavior=='floatcount':value['updates']['updatedRows']=1.0
   if self.behavior=='values':value['updates']['updatedData']['values'][0][0]='corrupt'
   if self.behavior=='partial':value={'spreadsheetId':t.SID}
   if self.behavior=='malformed':return types.SimpleNamespace(returncode=0,stdout='{',stderr='')
  else:
   if params['range']==t.FULL_RANGE:
    self.full+=1
    if self.behavior=='baseline_loss' and self.full==2:self.data.pop(1)
    if self.behavior=='shift_after_own' and self.full==3:self.data.insert(1,['concurrent foreign','','',''])
    if self.behavior=='after_loss' and self.full==3:self.data.pop(1)
    if self.behavior=='after2_loss' and self.full==4:self.data.pop(1)
    if self.behavior=='after2_doi' and self.full==4:self.data.pop()
    value={'values':copy.deepcopy(self.data)}
    if self.behavior=='after2_malformed' and self.full==4:return types.SimpleNamespace(returncode=0,stdout='{',stderr='')
    if self.behavior=='after2_timeout' and self.full==4:raise TimeoutError('SYNTHETIC second read timeout')
   else:
    n=int(params['range'].split('!A')[1].split(':D')[0]);value={'values':[copy.deepcopy(self.data[n-1])]}
    if self.behavior=='own_corrupt':value['values'][0][3]='corrupt'
  return types.SimpleNamespace(returncode=0,stdout=json.dumps(value),stderr='')

# A complete per-case exception record is preserved; a failed probe never becomes a PASS.
def case(name,fn):
 global CURRENT
 CURRENT={'id':name,'checks':[],'rejections':[],'status':'RUNNING'}
 try:fn();CURRENT['status']='PASS'
 except Exception as e:CURRENT.update(status='FAIL',error_type=type(e).__name__,error=str(e),traceback=traceback.format_exc())
 RESULTS.append(CURRENT)

case('actual_absent_authority',lambda:(setattr(c,'_authority',None),denied(lambda:p.Publisher(CASE,KIT,types.SimpleNamespace(run=lambda *_:(_ for _ in ()).throw(RuntimeError('BAD TRANSPORT')))).invoke('stage'),'actual absent adoption denies before transport')))

def baseline():
 f=Fixture(fullmap=True);ctx=f.context();check(len(f.selected)>=4416,'actual custody4416 identities retained in synthetic full ready map');pub,k,h=f.published();r=t.Tracker(f.base,Sheet(f)).run();check(r['range']=="'Math Puzzles'!A6:D6" and r['row'][1]=='','dynamic one-row range and blank B');check(r['two_fresh_full_readbacks'] and r['foreign_rows_retained'],'two fresh readbacks and retained foreign multiplicities');check(len(h.calls)==4 and k.mutations==['stage','publish'],'strict stage publish then independent public evidence');check(c.pin(f.base/'ROOT_PUBLICATION_RECEIPT.json')['bytes']>0,'synthetic final publication receipt exists only in own fixture')
case('full_context_happy_path',baseline)

GATE_TRUE=['publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','bounded_priority_audit_complete','current_portable_verifier_accepted','qualified_attributed_note_editorially_cleared']
for field in GATE_TRUE:
 def probe(field=field):
  f=Fixture();f.gate[field]=False;f.refresh();pub,k,h=f.publisher();denied(lambda:pub.invoke('stage'),'gate false '+field);check(not k.calls,'zero transport')
 case('gate_false_'+field,probe)
for field in ['theorem_novelty_cleared','historical_priority_established','actual_publication_verified','actual_tracker_row_verified','current_openness_established']:
 def probe(field=field):
  f=Fixture();f.gate[field]=True;f.refresh();pub,k,h=f.publisher();denied(lambda:pub.invoke('stage'),'unsupported true '+field);check(not k.calls,'zero transport')
 case('gate_unsupported_'+field,probe)
for variant in ('missing_adoption','missing_gate','missing_ready','source_copy_changed','package_extra','package_hash','metadata','one_event','duplicate_event','noncanonical_event','review_tamper','wrong_draft_head','not_draft','closed','missing_custody','map_missing','ready_chain_swap'):
 def probe(v=variant):
  f=Fixture()
  if v=='missing_adoption':(f.base/'SYNTHETIC_OPS_ADOPTION.json').unlink()
  elif v=='missing_gate':f.gp.unlink()
  elif v=='missing_ready':(f.base/'ROOT_ACTUAL_READY_CHECKPOINT.json').unlink()
  elif v=='source_copy_changed':write(f.base/c.OWN/'run_offline.py',b'SYNTHETIC corrupt')
  elif v=='package_extra':write(f.package/'extra.txt',b'SYNTHETIC extra')
  elif v=='package_hash':write(f.package/'focal_inverse_area_product.pdf',b'SYNTHETIC corrupt')
  elif v=='metadata':f.gate['metadata']=copy.deepcopy(f.metadata);f.gate['metadata']['creators'][0]['orcid']='wrong';f.refresh()
  elif v=='one_event':f.gate['whole_package_review_events']=f.events[:1];f.refresh()
  elif v=='duplicate_event':f.gate['whole_package_review_events']=[f.events[0],f.events[0]];f.refresh()
  elif v=='noncanonical_event':f.events[1]['review_number']=3;f.refresh()
  elif v=='review_tamper':write(f.base/f.events[0]['directory']/'REPORT.md',b'corrupt')
  elif v=='wrong_draft_head':f.ac['actual_original_PR_head']='0'*40;f.refresh()
  elif v=='not_draft':f.ac['actual_original_PR_is_draft']=False;f.refresh()
  elif v=='closed':f.ac['actual_original_PR_state']='closed';f.refresh()
  elif v=='missing_custody':f.other.pop('ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json');f.refresh()
  elif v=='map_missing':f.selected.pop(c.PREFIX+f.package.name+'/README.md');f.refresh(inputs=False)
  elif v=='ready_chain_swap':
   old=c.pin(f.base/'SYNTHETIC_OPS_ADOPTION.json');f.ac['checkpoint_commit']='e'*40;f.ac['main_observed']='e'*40;f.pointer['checkpoint_commit']='e'*40;f.pointer['main_observed']='e'*40;f.refresh(adopt=False);check(c.pin(f.base/'SYNTHETIC_OPS_ADOPTION.json')==old,'ready replacement leaves externally pinned adoption unchanged')
  pub,k,h=f.publisher();denied(lambda:pub.invoke('stage'),v+' denied');check(not k.calls,'zero transport')
 case('auth_'+variant,probe)

for behavior in ('timeout','malformed','partial','exit_error','bad_metadata','bad_title','bad_file','missing_file','extra_file','stage_published','drift'):
 def probe(b=behavior):
  f=Fixture();pub,k,h=f.publisher(b);denied(lambda:pub.invoke('stage'),'bad stage '+b);denied(lambda:pub.invoke('stage'),'no stage duplicate after '+b);check(k.mutations==['stage'],'one mutation despite uncertain/bad response');check((pub.directory/'STAGE_INFLIGHT.json').exists(),'durable inflight retained')
 case('publisher_'+behavior,probe)

def uncertain_recovery():
 f=Fixture();pub,k,h=f.publisher('timeout');denied(lambda:pub.invoke('stage'),'unknown stage');k.behavior=None;pub.invoke('inspect',k.id);pub.invoke('publish',k.id);pub.invoke('inspect-doi',k.id);pub.finalize();check(k.mutations==['stage','publish'],'unknown stage recovered by read-only inspect without duplicate');denied(lambda:pub.invoke('publish',k.id),'existing final blocks publish');check(k.mutations==['stage','publish'],'no final replay')
case('publisher_readonly_unknown_recovery',uncertain_recovery)

for behavior in ('hash','partial','insecure','wrong_doi','wrong_host','resolver404','timeout'):
 def probe(b=behavior):
  f=Fixture();pub,k,h=f.publisher(public_behavior=b);pub.invoke('stage');pub.invoke('publish',k.id);denied(pub.finalize,'finalize requires inspect-doi before public evidence');check(not h.calls,'no public reads before fresh inspect-doi');pub.invoke('inspect-doi',k.id);denied(pub.finalize,'public evidence '+b+' rejected');check(not (f.base/'ROOT_PUBLICATION_RECEIPT.json').exists(),'no accepted public receipt')
 case('public_'+behavior,probe)

for behavior in ('wrong_gid','float_gid','wrong_tab','baseline_loss','range','boolcount','floatcount','values','partial','malformed','own_corrupt','after_loss','after2_loss','after2_doi','after2_malformed','after2_timeout','shift_after_own'):
 def probe(b=behavior):
  f=Fixture();f.published();s=Sheet(f,b);tr=t.Tracker(f.base,s);denied(tr.run,'tracker '+b+' denied');check(not (f.base/'ROOT_TRACKER_RECEIPT.json').exists(),'no tracker acceptance');n=s.appends;denied(lambda:tr.run(True),'failed/corrupt '+b+' does not blindly accept') if b in ('after_loss','after2_loss','after2_doi','shift_after_own') else None;check(s.appends==n,'read-only recovery never appends')
 case('tracker_'+behavior,probe)
for col in range(4):
 def probe(col=col):
  f=Fixture();f.published();s=Sheet(f);s.data.append(['','','','']);s.data[-1][col]='prefix DOI10.5281/zenodo.999999999998 suffix';denied(lambda:t.Tracker(f.base,s).run(),'duplicate DOI in cell '+str(col));check(s.appends==0,'existing DOI zero append')
 case('tracker_doi_column_'+str(col),probe)
for lost in ('lost_before','lost_after'):
 def probe(b=lost):
  f=Fixture();f.published();s=Sheet(f,b);tr=t.Tracker(f.base,s);denied(tr.run,'unknown append '+b);old=c.pin(tr.directory/'APPEND_INFLIGHT.json')
  if b=='lost_after':r=tr.run(True);check(r['recovered_unknown_outcome'],'unknown successful append accepted by read-only evidence')
  else:denied(lambda:tr.run(True),'unknown absent append requires external reconciliation')
  check(s.appends==1 and c.pin(tr.directory/'APPEND_INFLIGHT.json')==old,'exactly one append and marker unchanged')
 case('tracker_'+lost,probe)

for label,mut in [('missingvalues',{}),('overwide',{'values':[[1,2,3,4,5]]}),('nested',{'values':[[{}]]}),('nan',{'values':[[float('nan')]]}),('malformedvalues',{'values':None})]:
 def probe(label=label,mut=mut):
  if label=='missingvalues':check(t.rows(mut)==[],'missing values is empty and caller must reject missing header')
  else:denied(lambda:t.rows(mut),'malformed rows '+label)
 case('rows_'+label,probe)

def durability():
 f=Fixture();q=f.base/'exclusive.json';c.durable_json(q,{'SYNTHETIC_NON_RECEIPT':True});old=c.pin(q);denied(lambda:c.durable_json(q,{'bad':True}),'create-only durable output');check(c.pin(q)==old,'existing durable bytes preserved');pub,k,h=f.publisher();real=p.os.fsync
 def broken(fd):raise OSError('SYNTHETIC fsync failure')
 p.os.fsync=broken
 try:denied(lambda:pub.invoke('stage'),'fsync failure before transport')
 finally:p.os.fsync=real
 check(not k.calls,'zero mutation on fsync failure')
case('durability_create_only_fsync',durability)

def pin_buffer():
 raw=b'{"synthetic":true}\n'
 class Once:
  def __init__(self):self.reads=0
  def read_bytes(self):self.reads+=1;return raw if self.reads==1 else b'{}'
 o=Once();check(c.read_pinned(o,{'bytes':len(raw),'sha256':c.digest(raw)})=={'synthetic':True} and o.reads==1,'same authenticated JSON buffer read exactly once')
case('pinned_parse_single_buffer',pin_buffer)

def runtime_static():
 for name,w in PINS.items():
  check(c.pin(SOURCE/name)=={'bytes':w['bytes'],'sha256':w['sha256']},'reviewed source/contract bytes unchanged '+name)
  if name.endswith('.py'):check(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((SOURCE/name).read_bytes()))),'no optimized-away assertion '+name)
 check(c.pin(KIT)=={'bytes':25740,'sha256':c.KIT_SHA},'actual repository kit unchanged after fake tests')
 check(not offline_guard.BLOCKED_EVENTS,'no attempted prohibited network/process/write')
case('runtime_source_binding',runtime_static)
result={'schema':'pr206-independent-adversary-synthetic-tests-v1','SYNTHETIC_NON_RECEIPT':True,'offline_only':True,'optimization_flag':sys.flags.optimize,'status':'PASS' if all(x['status']=='PASS' for x in RESULTS) else 'FAIL','case_count':len(RESULTS),'check_count':sum(len(x['checks']) for x in RESULTS),'cases':RESULTS,'reviewed_pins':PINS,'runtime':{'executable':sys.executable,'version':sys.version,'flags':repr(sys.flags)},'blocked_prohibited_events':offline_guard.BLOCKED_EVENTS,'limits':'Source falsification only. No live gate, ready90, source adoption, service receipt, operational clearance or mathematical claim.'}
output=ROOT/('INDEPENDENT_RESULT_O'+str(sys.flags.optimize)+'.json')
with output.open('xb') as f:f.write(json.dumps(result,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
print(json.dumps({'status':result['status'],'case_count':result['case_count'],'check_count':result['check_count'],'optimization_flag':sys.flags.optimize,'result_sha256':c.pin(output)['sha256'],'failed_cases':[x['id'] for x in RESULTS if x['status']!='PASS']},sort_keys=True))
raise SystemExit(0 if result['status']=='PASS' else 1)
