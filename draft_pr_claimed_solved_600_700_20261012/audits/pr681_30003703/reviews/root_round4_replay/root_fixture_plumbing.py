#!/usr/bin/env python3
"""Exact root readback with fake kit/client/HTTP transports in a toy checkout."""
import builtins,copy,contextlib,hashlib,importlib._bootstrap_external,importlib.util,io,json,shutil,sys,types
from pathlib import Path
R=Path(__file__).absolute().parent;A=R.parent.parent;REPO=A.parents[2];RID=999999991
T=R/'tmp'/('root-readback-optimized'if sys.flags.optimize else'root-readback-normal')
if T.exists():shutil.rmtree(T)
T.mkdir(parents=True,exist_ok=True)
F=T/'toyrepo/program/audits/pr681_30003703';F.mkdir(parents=True,exist_ok=True)
(F/'tmp').mkdir(exist_ok=True)
P=F/'publication';P.mkdir(exist_ok=True)
for n in ['zenodo-deposit.json','satoh_filtration_counterexamples.pdf','satoh_filtration_verification.zip']:shutil.copy2(A/'publication'/n,P/n)
K=T/'toyrepo/zenodo_deposit_tool/zenodo.py';K.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(REPO/'zenodo_deposit_tool/zenodo.py',K)
root_source=(A/'root_zenodo_readback.py').read_bytes();(F/'root_zenodo_readback.py').write_bytes(root_source)
# Valid timestamp/size stale caches are deliberately harmless sentinels. The
# repaired loader must ignore them and execute the captured source instead.
cache=Path(importlib.util.cache_from_source(str(K)));cache.parent.mkdir(exist_ok=True);st=K.stat()
cache.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(compile("raise RuntimeError('STALE_KIT_SENTINEL_EXECUTED')",str(K),'exec'),int(st.st_mtime),st.st_size))
original=json.loads((A/'ZENODO_STAGED_NATIVE_READBACK.json').read_bytes());meta=json.loads((P/'zenodo-deposit.json').read_bytes())['metadata'];calls=[];phase='staged';loaded=[]
def need(c,m):
 if not c:raise ValueError(m)
def native():
 entries={n:{'size':p['bytes'],'checksum':'md5:'+p['md5']}for n,p in original['files'].items()}
 return {'id':str(RID),'is_published':phase=='published','status':'published'if phase=='published'else'draft','metadata':copy.deepcopy(original['native_metadata']),'access':copy.deepcopy(original['native_access']),'files':{'entries':entries},'pids':{'doi':{'identifier':f'10.5281/zenodo.{RID}'}}if phase=='published'else{}}
class Client:
 def __init__(self,environment,token):need(environment=='production'and token=='FAKE-NOT-REAL','selected client');self.token=token
 def get(self,rid):
  need(rid==RID,'legacy id');calls.append('MOCK_LEGACY_GET')
  return {'id':RID,'submitted':phase=='published','metadata':copy.deepcopy(original['legacy_supplied_metadata_fields']),'files':[{'filename':n,'filesize':p['bytes'],'checksum':'md5:'+p['md5']}for n,p in original['files'].items()]}
 def native_get(self,rid,draft=False):need(rid==RID and draft and phase=='staged','native draft route');calls.append('MOCK_NATIVE_DRAFT_GET');return native()
class Conn:
 def __init__(self,host,timeout):need(host=='zenodo.org','download host')
 def request(self,method,target,headers):
  need(method=='GET','read-only HTTP');self.name=next(n for n in original['files']if '/files/'+n+'/content' in target);need(str(RID)in target,'download id')
  need(headers.get('Authorization')==('Bearer FAKE-NOT-REAL'if phase=='staged'else None),'phase authorization')
  calls.append('MOCK_CONTENT_GET_'+self.name)
 def getresponse(self):return types.SimpleNamespace(status=200,read=lambda limit:(P/self.name).read_bytes())
 def close(self):pass
class PublicResponse:
 status=200
 def __enter__(self):return self
 def __exit__(self,*args):pass
 def read(self,*args):return json.dumps(native()).encode()
def opener(request,timeout):need(request.get_method()=='GET'and request.full_url==f'https://zenodo.org/api/records/{RID}','public native route');need(not request.has_header('Authorization'),'public auth leak');calls.append('MOCK_PUBLIC_NATIVE_GET');return PublicResponse()
m=types.ModuleType('exact_root_readback_transport_fixture');m.__file__=str(F/'root_zenodo_readback.py');exec(compile(root_source,m.__file__,'exec'),m.__dict__)
def captured_exec(code,ns):
 builtins.exec(code,ns);need(ns.get('USER_AGENT')=='Math-Zenodo-Deposit-Tool/1.0','captured real kit did not execute')
 loaded.append(True);ns['token_for']=lambda environment:'FAKE-NOT-REAL';ns['ZenodoClient']=Client;ns['local_state']=lambda *args:(T/'FAKE_STATE.json',{'id':RID})
m.exec=captured_exec
m.http=types.SimpleNamespace(client=types.SimpleNamespace(HTTPSConnection=Conn))
m.urllib=types.SimpleNamespace(parse=importlib.import_module('urllib.parse'),request=types.SimpleNamespace(Request=importlib.import_module('urllib.request').Request,urlopen=opener))
results=[]
for ph in ['staged','published']:
 phase=ph;argv=sys.argv;sys.argv=['root_zenodo_readback.py','--phase',ph,'--receipt',f'FAKE_{ph}.json']
 try:
  with contextlib.redirect_stdout(io.StringIO()):m.main()
 finally:sys.argv=argv
 out=json.loads((F/f'FAKE_{ph}.json').read_bytes());need(out['id']==RID and out['published']is(ph=='published')and out['only_read_requests']is True,'result identity/state')
 need(out['all_supplied_metadata_fields_verified']==11 and out['legacy_metadata_normalizations']==original['legacy_metadata_normalizations'],'metadata mapping')
 need(out['files']==original['files'],'download validation')
 results.append({'name':'exact_'+ph+'_native_metadata_and_two_file_download_readback','status':'PASS'})
 if ph=='staged':shutil.copy2(F/f'FAKE_{ph}.json',F/'ZENODO_STAGED_NATIVE_READBACK.json')
need(len(loaded)==2,'captured module load count')
print(json.dumps({'schema':'pr681-round3-root-readback-controls-v1','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','root_readback_sha256':hashlib.sha256(root_source).hexdigest(),'kit_source_sha256':hashlib.sha256(K.read_bytes()).hexdigest(),'stale_pyc_ignored':True,'controls':results,'all11_metadata_fields_exact':True,'two_downloaded_files_each_phase':True,'fake_transports':calls,'real_network_credentials_or_mutations':0,'fake_record_id':RID},indent=2,sort_keys=True))
