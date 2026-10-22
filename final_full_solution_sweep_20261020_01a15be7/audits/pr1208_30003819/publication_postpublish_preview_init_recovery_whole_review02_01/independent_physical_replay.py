"""Finite blocked-transport controls. Real core parser/RealProvider/physical Journal.
No production authority file is made; simulation-only authority is explicit.
"""
from pathlib import Path
import argparse,copy,hashlib,json,os,subprocess,sys,types
D=Path(__file__).resolve().parent;P=D.parent/'publication_postpublish_preview_init_recovery_preparation02';OLD=P.parent/'publication_samecase_recovery_preparation01';OPS=P.parent/'publication_operations_preparation_07'
def need(v,m):
 if not v:raise RuntimeError(m)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 p.chmod(0o600)
def module(path):
 ns={'__name__':path.stem,'__file__':str(path)};exec(compile(path.read_bytes(),str(path),'exec',dont_inherit=True),ns);return ns
# Reference harness is immutable and uses only blocked transports at import.
H=module(OLD/'focused_controls.py');c=H['c'];pr=H['pr'];life=H['life'];runner=H['runner'];models=H['models'];fixture=H['fixture'];G=module(P/'postpublish_guard.py');A=module(P/'postpublish_adapter.py');POL=module(P/'preview_policy.py');native=H['load']('native_policy')
original_validator=native.validate_target;source=json.loads((OPS/'SOURCE_MANIFEST.json').read_text());delta=POL['install'](native,life,(OPS/'native_policy.py').read_bytes(),source['files']['native_policy.py'])
D={k:json.loads((P/'private'/('ACTUAL_'+k+'.json')).read_text()) for k in ['LEGACY','NATIVE','FINALIZED_FILES']};POST=json.loads((P/'private/ORIGINAL_PUBLISH_RESPONSE.json').read_text());pkg=c.package()
def validate(d,legacy=None,record=23578142):return native.validate_target(legacy or d['LEGACY'],d['NATIVE'],d['FINALIZED_FILES'],pkg['metadata'],pkg['uploads'],record,True,{c.PDF,c.ZIP})
# Independent bounded custody wrapper; actor/module buffers remain unchanged.
import io,tarfile,shutil,math
CAP=6*1024*1024
def allocated():return sum(p.stat().st_blocks*512 for p in D.rglob('*')if p.is_file())
RESOURCE={'peak_allocated_bytes':allocated(),'minimum_free_bytes':shutil.disk_usage(D).free,'cap_bytes':CAP}
def resources(extra=0):
 used=allocated();free=shutil.disk_usage(D).free;RESOURCE['peak_allocated_bytes']=max(RESOURCE['peak_allocated_bytes'],used);RESOURCE['minimum_free_bytes']=min(RESOURCE['minimum_free_bytes'],free)
 need(used+extra<=CAP and free>=150*1024*1024+extra,'INDEPENDENT_RESOURCE_HOLD_NOT_ACTOR_RESULT')
# Preflight both actual physical capture files, without changing their contents.
base_factory=H['A']['provider_class']
def bounded_factory(core,capture):
 Base=base_factory(core,capture)
 class Bounded(Base):
  def capture(self,label,raw):
   import gzip
   compressed=gzip.compress(raw,mtime=0)
   resources(((len(compressed)+4095)//4096+1)*4096)
   return super().capture(label,raw)
 return Bounded
H['A']['provider_class']=bounded_factory
def packed_archive(root,out,name):
 entries=H['snapshot'](root)['entries'];data=io.BytesIO()
 with tarfile.open(fileobj=data,mode='w:xz',format=tarfile.PAX_FORMAT)as t:
  for e in entries:
   p=root if e['path']=='.'else root/e['path'];m=t.gettarinfo(str(p),arcname=e['path']);m.pax_headers['custody_mtime_ns']=str(e['mtime_ns'])
   if p.is_file():
    with p.open('rb')as f:t.addfile(m,f)
   else:t.addfile(m)
 body=data.getvalue()
 with tarfile.open(fileobj=io.BytesIO(body),mode='r:xz')as t:
  assert [m.name for m in t.getmembers()]==[e['path']for e in entries]
  for m,e in zip(t.getmembers(),entries):
   assert m.mode==e['mode']and int(m.pax_headers['custody_mtime_ns'])==e['mtime_ns']
   if e['kind']=='file':assert pin(t.extractfile(m).read())=={k:e[k]for k in ['bytes','sha256']}
 store=out/'WORLD_CUSTODY.store';offset=store.stat().st_size if store.exists()else 0
 resources(((len(body)+4095)//4096+1)*4096)
 with store.open('ab'if store.exists()else'xb')as f:f.write(body);f.flush();os.fsync(f.fileno())
 with store.open('rb')as f:f.seek(offset);assert f.read(len(body))==body
 # Full physical namespace and metadata are stored with every compressed world.
 inv=json.dumps({'case':name,'offset':offset,'compressed_bytes':len(body),'compressed_sha256':pin(body)['sha256'],'entries':entries,'full_member_readback_before_own_only_retirement':True,'inode_resumability_not_claimed':True},sort_keys=True,separators=(',',':')).encode()
 import lzma
 packed=lzma.compress(inv);p=out/(name+'.custody.json.xz');resources(((len(packed)+4095)//4096)*4096);p.write_bytes(packed)
 shutil.rmtree(root);resources()
H['archive_case']=packed_archive
def main():
 pa=argparse.ArgumentParser();pa.add_argument('--output',type=Path,required=True);pa.add_argument('--only',nargs='*');args=pa.parse_args();out=args.output.absolute();need(D/'private' in out.parents and not out.exists(),'New private output only');out.mkdir(mode=0o700);pure=[];worlds=[]
 def reject(label,fn):
  try:fn()
  except Exception as e:pure.append({'case':label,'expected_HOLD':True,'error_class':type(e).__name__,'error':str(e)});return
  raise RuntimeError('False control ACCEPTED: '+label)
 reject('frozen07_actual_full_envelope_init_HOLD',lambda:original_validator(D['LEGACY'],D['NATIVE'],D['FINALIZED_FILES'],pkg['metadata'],pkg['uploads'],23578142,True,{c.PDF,c.ZIP}))
 pristine=copy.deepcopy(D);valid=validate(D);postvalid=validate(D,POST['response']);need(D==pristine and postvalid['files']==valid['files'],'Raw views modified or original POST differs');pure.append({'case':'actual_complete_native_legacy_finalized_and_original_POST','PASS':True,'raw_unchanged':True,'record':valid['record'],'concept':valid['concept'],'files':2,'AST_delta':delta})
 for status in ['queued','running','finished','failed']:
  d=copy.deepcopy(D);d['NATIVE']['media_files']['entries'][c.PDF+'.ptif']['processor']['status']=status
  old=original_validator(d['LEGACY'],d['NATIVE'],d['FINALIZED_FILES'],pkg['metadata'],pkg['uploads'],23578142,True,{c.PDF,c.ZIP});new=validate(d);need(old==new,'Existing accepted status behavior changed');pure.append({'case':'old_status_'+status,'PASS_same_result':True})
 faults={
 'unknown_status':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif']['processor'].update(status='waiting'),
 'wrong_source':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif']['processor'].update(source_file_id='00000000-0000-0000-0000-000000000001'),
 'wrong_preview_UUID':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif'].update(id='00000000-0000-0000-0000-000000000001'),
 'wrong_PDF_UUID':lambda d:d['NATIVE']['files']['entries'][c.PDF].update(id='00000000-0000-0000-0000-000000000001'),
 'preview_nonzero':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif'].update(size=1),
 'preview_bool_zero':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif'].update(size=False),
 'preview_visible':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif']['access'].update(hidden=False),
 'preview_extra_processor':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif']['processor'].update(extra=False),
 'preview_wrong_content_link':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif']['links'].update(content='https://zenodo.org/api/records/999/files/'+c.PDF+'.ptif/content'),
 'preview_metadata_changed':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif'].update(metadata={}),
 'preview_count_bool':lambda d:d['NATIVE']['media_files'].update(count=True),
 'preview_enabled_false':lambda d:d['NATIVE']['media_files'].update(enabled=False),
 'preview_processor_type':lambda d:d['NATIVE']['media_files']['entries'][c.PDF+'.ptif']['processor'].update(type='other'),
 'native_owner':lambda d:d['NATIVE']['parent']['access']['owned_by'].update(user='999'),
 'native_DOI':lambda d:d['NATIVE']['pids']['doi'].update(identifier='10.5281/zenodo.999'),
 'native_self':lambda d:d['NATIVE']['links'].update(self='https://zenodo.org/api/records/999'),
 'legacy_title':lambda d:d['LEGACY'].update(title='contrary'),
 'legacy_file_key':lambda d:d['LEGACY']['files'][0].update(key='contrary.zip'),
 'scientific_size':lambda d:d['NATIVE']['files']['entries'][c.PDF].update(size=81252),
 'finalized_UUID':lambda d:d['FINALIZED_FILES']['entries'][0].update(file_id='00000000-0000-0000-0000-000000000001')}
 for label,fault in faults.items():
  d=copy.deepcopy(D);fault(d);reject(label,lambda d=d:validate(d))
 reject('record_bool',lambda:validate(D,record=True));reject('direct_init_wrong_record',lambda:need(POL['accept_exact_init'](23578143,True,c.PDF+'.ptif',POL['EXPECTED_MEDIA']['entries'][c.PDF+'.ptif'],POL['EXPECTED_MEDIA'],valid['files']),'Wrong record held'))
 # Exact new authority validator: virtual bytes only, never a passing file.
 from unittest.mock import patch
 ownsha=pin((P/'SOURCE_MANIFEST.json').read_bytes())['sha256'];og=H['G'];contract=G['contract'](P,ownsha,og);expected=G['expected_authority'](contract);review={'schema':'pr1208-postpublish-preview-init-review-v2','pr':1208,'record':23578142,'source_sha256':ownsha,'status':'PASS','fresh_independent_review':True,'unresolved_findings':[]};rb=c.canonical(review);mb=b'VIRTUAL_REVIEW_MANIFEST_NO_FILE';packet=b'VIRTUAL_FINAL_PACKET_NO_FILE';authority={**expected,'schema':'pr1208-postpublish-preview-init-recovery-v2','template_only':False,'root_complete_sources_and_fresh_review_read':True,'ready_for_execution':True,'unresolved_findings':[],'packet_manifest_sha256':pin(packet)['sha256'],'fresh_independent_review':{'receipt_path':'virtual/receipt','receipt_pin':pin(rb),'manifest_path':'virtual/manifest','manifest_pin':pin(mb)}}
 original_read=Path.read_bytes
 def virtual_read(path):return packet if path==P/'RECOVERY_MANIFEST.json' else original_read(path)
 def checkauth(a,action='reconcile',receipt=review):
  raw=c.canonical(a)
  with patch.object(Path,'read_bytes',virtual_read):return G['verify_authorization'](contract,pin(raw)['sha256'],action,lambda:None,lambda:raw,lambda name,p: c.canonical(receipt) if name=='virtual/receipt' else mb)
 need(checkauth(authority)['record']==23578142,'Virtual positive authority');pure.append({'case':'actual_authority_validator_virtual_positive','PASS':True,'passing_authority_file_created':False})
 for key,value in [('record',True),('concept',999),('case_path','/alternateCASE'),('allowed_actions',['publish']),('original_publish_response',{'bytes':0,'sha256':'0'*64}),('ready_for_execution',False),('template_only',True),('postpublish02_source_sha256','0'*64),('extra',False),('recovery01_authority_sha256','0'*64)]:
  a=copy.deepcopy(authority);a[key]=value;reject('authority_'+key,lambda a=a:checkauth(a))
 reject('authority_forbidden_publish',lambda:checkauth(authority,'publish'));reject('fresh_review_HOLD',lambda:checkauth(authority,receipt={**review,'status':'HOLD'}))
 save(out/'DATA_AUTHORITY_RESULTS.json',{'status':'PASS','cases':pure,'count':len(pure),'real_authority_files_created':0,'actual_data_raw_views':3,'actual_original_POST':True})
 # Derived public fixture uses the already observed public schema; never claims an
 # actual GET of this new record. Actual postpublish DATA are the three views above.
 w0=models.World(fixture);w0.native.allocated=True;w0.native.published=True;w0.native.present={u['name']:u for u in pkg['uploads']};public=w0.native.public()
 def replace(v):
  if type(v) is str:return v.replace('777','23578142').replace('778','23578141')
  if type(v) is int:return 23578142 if v==777 else 23578141 if v==778 else v
  if type(v) is list:return [replace(x) for x in v]
  if type(v) is dict:return {k:replace(x) for k,x in v.items()}
  return v
 public=replace(public);public['id']=23578142;public['conceptrecid']='23578141';public['conceptdoi']='10.5281/zenodo.23578141';public['recid']='23578142';public['owners']=[{'id':'1789874'}];public['title']=pkg['metadata']['title'];public['links']=copy.deepcopy(D['NATIVE']['links'])
 for f in public['files']:f['id']=valid['files'][f['key']]['file_id']
 # All mutation interfaces absent from the transport except exact atomic appendCells.
 BaseTransport=H['Transport'];Response=H['Response']
 class Transport(BaseTransport):
  def run(self,argv,input=None,**kwargs):
   if argv[0]=='gh':need('--method' not in argv and argv[4]!='graphql','No Git effect may reach transport')
   if argv[0]=='gws' and argv[3]=='batchUpdate':
    self.append_attempts+=1
    if self.world_name=='late_concurrent_append':self.w.snapshot['values'].append(['CONCURRENT','', 'https://doi.org/10.1000/unrelated','retain']);self.w.snapshot['formula'].append(['CONCURRENT','', 'https://doi.org/10.1000/unrelated','retain'])
   result=super().run(argv,input=input,**kwargs)
   if argv[0]=='gws' and argv[3]=='batchUpdate' and self.world_name=='lost_append_response':raise OSError('INERT lost transport response after known append')
   return result
  def urlopen(self,request,timeout=None):
   url=request.full_url if hasattr(request,'full_url') else request
   if url.startswith('https://zenodo.org/api/records?') or url=='https://zenodo.org/api/records':
    u=H['urllib'].parse.urlsplit(url);q=H['urllib'].parse.parse_qs(u.query);page=int(q['page'][0]);return Response(c.canonical({'hits':{'total':1,'hits':[copy.deepcopy(public)] if page==1 else []}}),200,url)
   if url=='https://zenodo.org/api/records/23578142':
    value=copy.deepcopy(public)
    if self.world_name=='bad_public_title':value['title']='contrary'
    return Response(c.canonical(value),200,url)
   if url=='https://doi.org/10.5281/zenodo.23578142':return Response(b'',200,'https://zenodo.org/records/'+('999' if self.world_name=='bad_DOI_destination' else '23578142'))
   for u in pkg['uploads']:
    if url=='https://zenodo.org/records/23578142/files/'+u['name']+'?download=1':return Response(b'bad' if self.world_name=='bad_payload' else u['path'].read_bytes(),200,url)
   raise RuntimeError('Unmodeled public transport blocked')
  def connection(self,host,timeout=None):
   need(host=='zenodo.org','Only modeled official host');transport=self
   class Conn:
    def __init__(self):self.headers={}
    def request(self,method,path,headers=None):self.method=method;self.path=path
    def putrequest(self,method,path):self.method=method;self.path=path
    def putheader(self,k,v):self.headers[k]=v
    def endheaders(self):pass
    def close(self):pass
    def getresponse(self):
     transport.calls.append({'kind':'HTTP','method':self.method,'path':self.path});need(self.method=='GET','Publication effects blocked')
     if self.path.startswith('/api/deposit/depositions?'):
      page=int(H['urllib'].parse.parse_qs(H['urllib'].parse.urlsplit(self.path).query)['page'][0]);value=transport.w.owned_page(page)
     elif self.path=='/api/deposit/depositions/23578142':value=copy.deepcopy(D['LEGACY'])
     elif self.path=='/api/records/23578142':
      value=copy.deepcopy(D['NATIVE'])
      if transport.world_name=='wrong_preview_after_fsync' and transport.fault_active:value['media_files']['entries'][c.PDF+'.ptif']['id']='00000000-0000-0000-0000-000000000001'
     elif self.path=='/api/records/23578142/files':value=copy.deepcopy(D['FINALIZED_FILES'])
     else:raise RuntimeError('Unmodeled GET blocked')
     return Response(c.canonical(value),200,'https://zenodo.org'+self.path)
   return Conn()
 for name in ['positive_cold_reconcile_public_first_append','lost_append_response','late_concurrent_append','bad_public_title','bad_DOI_destination','bad_payload','wrong_preview_after_fsync','late_authority_revocation','original_POST_mutation']:
  if args.only and name not in args.only:continue
  root=out/name;root.mkdir(mode=0o700);repo=root/'repo';repo.mkdir();sd=repo/'.zenodo-state';sd.mkdir(mode=0o700);(sd/Path(fixture['context_state_path']).name).write_text(fixture['context_state'])
  w=models.World(fixture);w.accounts={k:v for k,v in w.accounts.items() if k in {23224103,23430530}};w.snapshot['values']=w.snapshot['values'][:56];w.snapshot['formula']=w.snapshot['formula'][:56]
  for action in ['integrate','describe','ready','merge']:runner.Engine=life.Engine;runner.main([action,'--expected-pr-head',w.git.head],provider=w,test_adoption=w.adoption,test_journal=w.j)
  git_before=copy.deepcopy(w.git.writes);w.accounts[23578142]=copy.deepcopy(D['LEGACY']);w.adoption['allowed_actions']=A['ALLOWED'];w.adoption['target_id']=None
  statepath=c.zenodo.state_path(c.MANIFEST.resolve(),'production');actualstate={'manifest':str(c.MANIFEST.resolve()),'environment':'production','id':23578142};(sd/statepath.name).write_bytes(c.canonical(actualstate)+b'\n');(sd/statepath.name).chmod(0o600)
  case=root/'SAME_CASE';header={'simulation_only':True,'case':str(case),'production_authority':False};j=c.Journal(case,header);reads=case/'reads';reads.mkdir(mode=0o700)
  for k,v in w.j.events.items():j.write(k,v)
  j.write('TARGET_BOUND',{'id':23578142});j.write('PUBLISH_PHASE_INTENT',{'operation':'PUBLISH','action':'publish','request':{'id':23578142}});j.write('ZENODO_PUBLISH_INTENT',{'operation':'ZENODO_PUBLISH','action':'publish','request':{'id':23578142}});j.write('ZENODO_PUBLISH_RESPONSE',POST)
  original={k:j.expected[k] for k in ['PUBLISH_PHASE_INTENT','ZENODO_PUBLISH_INTENT','ZENODO_PUBLISH_RESPONSE']};prefix=H['snapshot'](case);binding={key:pin(original[source]) for key,source in [('original_publish_response','ZENODO_PUBLISH_RESPONSE'),('original_publish_intent','ZENODO_PUBLISH_INTENT'),('original_publish_phase_intent','PUBLISH_PHASE_INTENT')]};binding['additive_authorization']={'simulation_only':True,'source_sha256':ownsha}
  transport=Transport(w);transport.world_name=name;transport.append_attempts=0;transport.fault_active=False;transport.install(repo);Provider=A['provider_class'](H['A']['provider_class'](pr,reads));Provider.simulated=True;revoked=[]
  def checker(e):
   need(not revoked,'Simulated additional authority revoked after fsynced ledger intent');H['G']['prefix_check'](prefix,case);e.p.verify_captures()
  Engine=A['engine_class'](life,checker,binding);runner.Engine=Engine
  class J(c.Journal):
   def write(self,key,value):
    super().write(key,value)
    if key=='LEDGER_ROW_INTENT':
     if name=='wrong_preview_after_fsync':transport.fault_active=True
     if name=='late_authority_revocation':revoked.append(True)
  if name=='original_POST_mutation':
   q=case/'ZENODO_PUBLISH_RESPONSE.json';q.write_bytes(q.read_bytes()+b' ')
  answers=[];errors=[]
  def call(action):
   # Parse the actual restricted new CLI action set before the actual core parser.
   E=module(P/'POSTRECOVER.py');args=E['parser']().parse_args([action,'--source-sha256',ownsha]);need(args.action==action,'New parser differs');return runner.main([args.action,'--expected-pr-head',w.git.head],provider=Provider(),test_adoption=w.adoption,test_journal=J(case,header))
  try:
   if name=='positive_cold_reconcile_public_first_append':
    for action in ['ledger']:answers.append(call(action))
    need(transport.append_attempts==1 and w.row_writes==1,'Positive one append');reopened=c.Journal(case,header);need(reopened.exists('PUBLISH_VERIFIED') and reopened.exists('PUBLIC_VERIFIED') and reopened.exists('LEDGER_VERIFIED'),'Positive certificates absent')
    try:call('ledger');raise RuntimeError('Repeat ledger allowed')
    except RuntimeError as error:errors.append(str(error))
   else:
    try:answers.append(call('ledger'));raise RuntimeError('Negative action unexpectedly certified')
    except Exception as error:errors.append(str(error))
    if name in {'late_concurrent_append','lost_append_response'}:
     need(w.row_writes==1 and transport.append_attempts==1,'Known append not retained');answers.append(call('reconcile'));need(transport.append_attempts==1,'Cold reconcile repeated append')
     try:call('ledger');raise RuntimeError('Repeat append allowed')
     except RuntimeError as error:errors.append(str(error))
    else:need(w.row_writes==0 and transport.append_attempts==0,'False boundary reached append')
   need(w.git.writes==git_before and not w.native.calls and all(e.get('method','GET')=='GET' for e in transport.calls if e['kind']=='HTTP'),'Publication/Git effects reached transport')
   if name!='original_POST_mutation':
    reopened=c.Journal(case,header);need(all(reopened.expected[k]==v for k,v in original.items()),'Original publish evidence changed');need(not reopened.exists('LEDGER_VERIFIED') or name=='positive_cold_reconcile_public_first_append','False ledger certificate')
   result={'case':name,'answers':answers,'expected_errors':errors,'append_attempts':transport.append_attempts,'atomic_appends':w.row_writes,'publication_POSTs':0,'Git_effects_during_recovery':0,'actual_parser_real_provider_physical_fsynced_Journal':True,'simulation_authority_only':True,'capture_pairs':H['A']['capture_namespace'](reads,c.strict_json)[0],'source_sha256':ownsha,'readiness':False};save(root/'RESULT.json',result);worlds.append(result)
  except Exception as error:save(root/'FAILURE.json',{'error':str(error),'status':'DEV_FAILURE_NOT_PASS'});raise
  finally:H['archive_case'](root,out,name);runner.Engine=life.Engine
 save(out/'INDEPENDENT_RESOURCE.json',RESOURCE);save(out/'RESULT.json',{'status':'PASS','data_authority_cases':len(pure),'worlds':worlds,'world_count':len(worlds),'actual_network_process_credential_attempts':H['attempted'],'real_service_effects':0,'production_CASE_writes':0,'readiness':False});need(not H['attempted'],'Unmodeled external call');print(json.dumps({'status':'PASS','data_authority_cases':len(pure),'worlds':len(worlds),'readiness':False}))
if __name__=='__main__':main()
