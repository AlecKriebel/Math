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
contract=g['contract'](P,'b788049646d45487d4883c8bb7f7418c9170ef4ae8bba8a5095e2e8913de9984',og)
assert not contract['new'].exists()
review={'schema':'pr1208-postpublish-preview-init-review-v2','pr':1208,'record':23578142,'source_sha256':contract['source_sha'],'status':'PASS','fresh_independent_review':True,'unresolved_findings':[]}
virtual_receipt=D/'private/VIRTUAL_REVIEW_RECEIPT_ONLY';virtual_manifest=D/'private/VIRTUAL_REVIEW_MANIFEST_ONLY';rb=c.canonical(review);mb=b'INERT_REVIEW_MANIFEST_VIRTUAL_ONLY'
auth={**g['expected_authority'](contract),'schema':'pr1208-postpublish-preview-init-recovery-v2','template_only':False,'root_complete_sources_and_fresh_review_read':True,'ready_for_execution':True,'unresolved_findings':[],'packet_manifest_sha256':pin((P/'RECOVERY_MANIFEST.json').read_bytes())['sha256'],'fresh_independent_review':{'receipt_path':virtual_receipt.relative_to(c.REPO).as_posix(),'receipt_pin':pin(rb),'manifest_path':virtual_manifest.relative_to(c.REPO).as_posix(),'manifest_pin':pin(mb)}}
import builtins
actual_read=Path.read_bytes
checks=[]
def run_actual_entry(action):
 raw=c.canonical(auth);buffers={contract['new']:raw,virtual_receipt:rb,virtual_manifest:mb};dispatched=[]
 def read(path):return buffers[path]if path in buffers else actual_read(path)
 def intercept(code,space,locals_=None):
  if locals_ is None:builtins.exec(code,space)
  else:builtins.exec(code,space,locals_)
  if space.get('__name__')=='checked_original_bootstrap07':
   original_load_verified=space['load_verified']
   def hooked_load_verified(*args,**kwargs):
    checked_load,context=original_load_verified(*args,**kwargs)
    def checked_hook(name):
     m=checked_load(name)
     if name=='runner':
      def terminal_dispatch(argv):
       expected=[action,'--expected-pr-head','1769b8385857d2b6bfae8f8a2b9f85552d543adc','--adoption',str(contract['old']['old']),'--adoption-sha256',contract['bindings']['original_authority_sha256']]
       assert argv==expected,(argv,expected)
       assert [v.__name__ for v in m.RealProvider.__mro__][:3]==['PostPublishedProvider','RecoveryProvider','RealProvider']
       lm=checked_load('lifecycle');nm=checked_load('native_policy')
       assert m.Engine.__name__=='PostPublishedEngine'and m.Engine.__mro__[1]is lm.Engine
       assert m.Engine.__init__.__code__.co_filename==str(P/'postpublish_adapter.py')
       assert nm.validate_target is lm.validate_target and '_postpublish02_exact_init'in nm.validate_target.__globals__
       verified=nm.validate_target(post,data['NATIVE'],data['FINALIZED_FILES'],pkg['metadata'],pkg['uploads'],23578142,True,{c.PDF,c.ZIP})
       assert verified['record']==23578142 and verified['concept']==23578141 and sum(v['size']for v in verified['files'].values())==225207
       dispatched.append({'argv':argv,'provider_MRO':[v.__name__ for v in m.RealProvider.__mro__],'engine_MRO':[v.__name__ for v in m.Engine.__mro__],'actual_compiled_validator_callsite_shared':True,'actual_complete_originalPOST_policy_validated':True})
       return {'inert_terminal_dispatch':True,'action':action,'service_calls':0}
      m.main=terminal_dispatch
     return m
    return checked_hook,context
   space['load_verified']=hooked_load_verified
 entry['exec']=intercept
 with patch.object(Path,'read_bytes',read):
  result=entry['main']([action,'--source-sha256',contract['source_sha'],'--authorization-sha256',pin(raw)['sha256'],'--execute-one'])
 assert result=={'inert_terminal_dispatch':True,'action':action,'service_calls':0}and len(dispatched)==1
 return {'action':action,'result':result,'observed_actual_dispatch':dispatched[0]}
for action in ['reconcile','verify-public','ledger']:checks.append(run_actual_entry(action))
assert not contract['new'].exists()and not virtual_receipt.exists()and not virtual_manifest.exists()and not attempts
out('INDEPENDENT_ACTUAL_ENTRY_COMPOSITION.json',{'status':'PASS_INERT_DISPATCH_ONLY','source_sha256':contract['source_sha'],'cases':checks,'actual_entry_source_and_local_compiled_functions_unchanged':True,'test_seam':'Only virtual reads for three absent authority/review buffers and a terminal runner.main stub installed in the fresh checked loader. No provider instantiated or journal/service action. Separately tested physical actual providers/Journal/phase guards remain simulation-only.','passing_authority_files_created':0,'actual_external_attempts':attempts,'readiness':False})
print('ACTUAL_ENTRY_COMPOSITION_PASS',len(checks))
