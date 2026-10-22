"""Independent complete-data and virtual full-entry authority adversary; no real effects."""
from pathlib import Path
import copy,json,hashlib,sys,io,contextlib,os,socket,subprocess,http.client,urllib.request,ast
from unittest.mock import patch
D=Path(__file__).resolve().parent;P=D.parent/'publication_postpublish_preview_init_recovery_preparation02';OLD=D.parent/'publication_samecase_recovery_preparation01';OPS=D.parent/'publication_operations_preparation_07'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p,name=None):
 b=p.read_bytes();n={'__file__':str(p),'__name__':name or p.stem};exec(compile(b,str(p),'exec',dont_inherit=True),n);return n
def out(name,v): (D/'private'/name).write_text(json.dumps(v,ensure_ascii=True,indent=2)+'\n')
need=lambda v,m: v or (_ for _ in ()).throw(RuntimeError(m))
attempts=[]
def blocked(*a,**kw):attempts.append('BLOCKED_EXTERNAL');raise RuntimeError('Independent review blocks actual network/process/credential')
for mod,name in [(socket,'socket'),(socket,'create_connection'),(socket,'getaddrinfo'),(http.client,'HTTPConnection'),(http.client,'HTTPSConnection'),(urllib.request,'urlopen'),(subprocess,'Popen'),(os,'system'),(os,'popen')]:setattr(mod,name,blocked)
boot=load(OPS/'bootstrap.py','review_checked_core');loader,_=boot['load_verified'](OPS,'193013d467111f11726f151ddc2a4f38b0dfa5868950042d860cfdb7f4845148','22c4e8c67a657798c4ffd93c2ab4fcfd33868c716bf7c29c17607692f88b762d')
c=loader('common');c.zenodo.token_for=blocked;native=loader('native_policy');life=loader('lifecycle');original=native.validate_target;policy=load(P/'preview_policy.py');g=load(P/'postpublish_guard.py');og=load(OLD/'recovery_guard.py');entry=load(P/'POSTRECOVER.py','full_entry_no_effect')
source=json.loads((OPS/'SOURCE_MANIFEST.json').read_bytes());delta=policy['install'](native,life,(OPS/'native_policy.py').read_bytes(),source['files']['native_policy.py'])
data={k:json.loads((P/'private'/('ACTUAL_'+k+'.json')).read_bytes())for k in ['LEGACY','NATIVE','FINALIZED_FILES']};post=json.loads((P/'private/ORIGINAL_PUBLISH_RESPONSE.json').read_bytes())['response'];pkg=c.package()
def validate(x,record=23578142,published=True,legacy=None):
 return native.validate_target(x['LEGACY']if legacy is None else legacy,x['NATIVE'],x['FINALIZED_FILES'],pkg['metadata'],pkg['uploads'],record,published,{c.PDF,c.ZIP})
results=[]
def reject(label,fn):
 try:fn()
 except Exception as e:results.append({'case':label,'rejected':True,'exception':type(e).__name__,'message':str(e)});return
 raise RuntimeError('Adversarial FALSE acceptance: '+label)
before=copy.deepcopy(data);old_error=None
try:original(data['LEGACY'],data['NATIVE'],data['FINALIZED_FILES'],pkg['metadata'],pkg['uploads'],23578142,True,{c.PDF,c.ZIP})
except RuntimeError as e:old_error=str(e)
assert old_error=='Unreviewed derived-media processor/source'
a=validate(data);b=validate(data,legacy=post);assert data==before and a['files']==b['files'];results.append({'case':'genuine_three_views_and_original_POST','accepted':True,'old_rejection':old_error,'files':a['files'],'single_AST_delta':delta})
for status in ['queued','running','finished','failed']:
 x=copy.deepcopy(data);x['NATIVE']['media_files']['entries'][c.PDF+'.ptif']['processor']['status']=status
 assert original(x['LEGACY'],x['NATIVE'],x['FINALIZED_FILES'],pkg['metadata'],pkg['uploads'],23578142,True,{c.PDF,c.ZIP})==validate(x)
 results.append({'case':'old_status_'+status,'identical_result':True})
# Mutate every leaf in the exact added init-envelope independently, including type
# confusions and extra aliases. These are not derived from the preparer's fault list.
def leaves(v,path=()):
 if type(v)is dict:
  for k,x in v.items():yield from leaves(x,path+(k,))
 elif type(v)is list:
  if not v:yield path,v
  else:
   for i,x in enumerate(v):yield from leaves(x,path+(i,))
 else:yield path,v
def assign(root,path,value):
 n=root
 for k in path[:-1]:n=n[k]
 n[path[-1]]=value
media=data['NATIVE']['media_files']
for i,(path,value)in enumerate(leaves(media)):
 alternatives=[False,True,0,1,0.0,1.0,None,'',[],{}]
 if type(value)is str:alternatives+=['contrary',value+'extra']
 for j,z in enumerate(alternatives):
  if type(z)is type(value)and z==value:continue
  x=copy.deepcopy(data);assign(x['NATIVE']['media_files'],path,z);reject('media_leaf_%d_%d'%(i,j),lambda x=x:validate(x))
for path in [(),('entries',),('entries',c.PDF+'.ptif'),('entries',c.PDF+'.ptif','processor'),('entries',c.PDF+'.ptif','access'),('entries',c.PDF+'.ptif','links')]:
 x=copy.deepcopy(data);v=x['NATIVE']['media_files']
 for k in path:v=v[k]
 v['unknown_alias']=False;reject('media_extra_'+repr(path),lambda x=x:validate(x))
for record in [True,23578141,23578143,'23578142',23578142.0,None]:reject('record_'+repr(record),lambda record=record:validate(data,record))
for published in [False,1,'true',None]:reject('published_'+repr(published),lambda published=published:validate(data,published=published))
for root,path,z in [('NATIVE',('metadata','title'),'wrong'),('NATIVE',('parent','access','owned_by','user'),'999'),('NATIVE',('pids','doi','identifier'),'10.5281/zenodo.999'),('NATIVE',('files','entries',c.PDF,'size'),81252),('NATIVE',('files','entries',c.ZIP,'checksum'),'md5:'+'0'*32),('LEGACY',('title',),'wrong'),('FINALIZED_FILES',('entries',0,'size'),0)]:
 x=copy.deepcopy(data);assign(x[root],path,z);reject('scientific_or_identity_'+str(path),lambda x=x:validate(x))
# Exact deployed entry authority path, with only three READ buffers virtualized.
# No new authority or PASS review is written to the actual filesystem.
contract=g['contract'](P,'b788049646d45487d4883c8bb7f7418c9170ef4ae8bba8a5095e2e8913de9984',og)
assert not contract['new'].exists()
review={'schema':'pr1208-postpublish-preview-init-review-v2','pr':1208,'record':23578142,'source_sha256':contract['source_sha'],'status':'PASS','fresh_independent_review':True,'unresolved_findings':[]}
virtual_receipt=D/'private/VIRTUAL_REVIEW_RECEIPT_ONLY';virtual_manifest=D/'private/VIRTUAL_REVIEW_MANIFEST_ONLY';rb=c.canonical(review);mb=b'INERT_REVIEW_MANIFEST_VIRTUAL_ONLY'
auth={**g['expected_authority'](contract),'schema':'pr1208-postpublish-preview-init-recovery-v2','template_only':False,'root_complete_sources_and_fresh_review_read':True,'ready_for_execution':True,'unresolved_findings':[],'packet_manifest_sha256':pin((P/'RECOVERY_MANIFEST.json').read_bytes())['sha256'],'fresh_independent_review':{'receipt_path':virtual_receipt.relative_to(c.REPO).as_posix(),'receipt_pin':pin(rb),'manifest_path':virtual_manifest.relative_to(c.REPO).as_posix(),'manifest_pin':pin(mb)}}
actual_read=Path.read_bytes;full_entry=[]
def invoke(a,receipt=rb,manifest=mb,action='reconcile'):
 raw=c.canonical(a);buffers={contract['new']:raw,virtual_receipt:receipt,virtual_manifest:manifest};stream=io.StringIO()
 def read(path):return buffers[path]if path in buffers else actual_read(path)
 with patch.object(Path,'read_bytes',read),contextlib.redirect_stdout(stream):
  result=entry['main']([action,'--source-sha256',contract['source_sha'],'--authorization-sha256',pin(raw)['sha256']])
 return stream.getvalue()
s=invoke(auth);status=json.loads(s);assert status=={'status':'AUTHORITY_VALIDATED_NO_ACTION','service_calls':0,'CASE_changed':False,'action':'reconcile'};full_entry.append({'case':'actual_full_entry_with_virtual_authority_and_default_repo_review_paths','result':status,'no_actual_authority_file':True})
for k,z in [('record',True),('concept',23578142),('allowed_actions',['reconcile','publish']),('case_path','/otherCASE'),('ready_for_execution',False),('root_complete_sources_and_fresh_review_read',False),('original_publish_response',{'bytes':0,'sha256':'0'*64}),('packet_manifest_sha256','0'*64),('extra',False)]:
 x=copy.deepcopy(auth);x[k]=z;reject('full_entry_authority_'+k,lambda x=x:invoke(x))
reject('full_entry_actual_receipt_pin_corrupted',lambda:invoke(auth,receipt=rb+b' '))
reject('full_entry_actual_manifest_pin_corrupted',lambda:invoke(auth,manifest=mb+b' '))
for path in ['../escape','/absolute','a//b','a/./b','a/../b','a\\b','a:b']:
 x=copy.deepcopy(auth);x['fresh_independent_review']['receipt_path']=path;reject('full_entry_safe_review_path_'+repr(path),lambda x=x:invoke(x))
assert not contract['new'].exists()and not virtual_receipt.exists()and not virtual_manifest.exists()and not attempts
out('INDEPENDENT_DATA_AND_FULL_ENTRY_AUTHORITY.json',{'status':'PASS','cases':results,'case_count':len(results),'full_entry':full_entry,'source_manifest':contract['source_sha'],'actual_production_authority_files_created':0,'actual_external_attempts':attempts,'readiness':False})
print('INDEPENDENT_DATA_AND_FULL_ENTRY_PASS',len(results))
