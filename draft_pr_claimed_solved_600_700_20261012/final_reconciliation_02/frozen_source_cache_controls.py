#!/usr/bin/env python3
"""Offline stale-pyc controls. All probes/poison caches are harmless local fixtures.

A normal SourceFileLoader.get_code accepts each poisoned cache, proving its
matching timestamp/size header is effective, but the returned code is NEVER
executed. The frozen launcher must execute captured fresh sources instead.
"""
from pathlib import Path
import ast,contextlib,hashlib,importlib.machinery,importlib.util,io,json,marshal,os,struct,sys,tempfile,types
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
MARKER='HARMLESS_STALE_PYC_SENTINEL_MUST_NEVER_EXECUTE'
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
 launcher_path=OUT/'run_frozen_sources.py';launcher_bytes=launcher_path.read_bytes()
 namespace={'__name__':'captured_launcher_for_offline_controls','__file__':str(launcher_path)}
 exec(compile(launcher_bytes,str(launcher_path),'exec',dont_inherit=True),namespace)
 namespace['disable_transports']()
 root=Path(tempfile.mkdtemp(prefix='frozen_source_controls_',dir=OUT/'tmp'))
 (OUT/'tmp'/'LAST_SOURCE_CACHE_CONTROL_FIXTURE.txt').write_text(str(root)+'\n')
 source_pins={p.name:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(OUT.glob('*.py'))}
 controls=[]
 def check(name,ok,detail=None):
  if not ok:raise RuntimeError('Frozen source control failed: '+name)
  item={'control':name,'pass':True}
  if detail is not None:item['detail']=detail
  controls.append(item)
 def source(text):return (text+'\n').ljust(240).encode()
 dependencies={
 'metadata_rules.py':source("ORIGIN='CAPTURED_FROZEN_SOURCE'"),
 'scope_sheet_evidence.py':source("ORIGIN='CAPTURED_FROZEN_SOURCE'"),
 'expected_state.py':source("import metadata_rules,scope_sheet_evidence\nif metadata_rules.ORIGIN!='CAPTURED_FROZEN_SOURCE' or scope_sheet_evidence.ORIGIN!='CAPTURED_FROZEN_SOURCE':raise RuntimeError('WRONG_DEPENDENCY')\nORIGIN='CAPTURED_FROZEN_SOURCE'")}
 probe=b"import json,metadata_rules,scope_sheet_evidence,expected_state\nfor name in ('metadata_rules','scope_sheet_evidence','expected_state'):\n module=globals()[name]\n if module.ORIGIN!='CAPTURED_FROZEN_SOURCE' or hasattr(module,'__STALE_PYC_SENTINEL__'):raise RuntimeError('STALE_MODULE_EXECUTED')\n if module.__frozen_source_sha256__!=__frozen_sources__[name+'.py']:raise RuntimeError('MODULE_SOURCE_PIN_MISMATCH')\nif __frozen_source_sha256__!=__frozen_sources__['preparation_controls.py']:raise RuntimeError('ENTRY_SOURCE_PIN_MISMATCH')\nprint(json.dumps({'status':'PASS','captured_dependencies':3,'captured_entry':True,'stale_sentinel_executed':False},sort_keys=True))\n"
 def fixture(name,poison=True):
  path=root/name;path.mkdir()
  sources={**dependencies,'preparation_controls.py':probe,'run_frozen_sources.py':launcher_bytes}
  for filename,data in sources.items():
   target=path/filename;target.write_bytes(data);os.utime(target,(1700000000,1700000000))
  pins={filename:{'bytes':len(data),'sha256':sha(data)} for filename,data in sources.items()}
  freeze=json.dumps({'files':pins,'scope':'SYNTHETIC_OFFLINE_STALE_CACHE_FIXTURE'},sort_keys=True).encode()
  (path/'PREPARATION_FREEZE.json').write_bytes(freeze)
  if poison:
   for filename in (*dependencies,'preparation_controls.py'):
    source_path=path/filename;st=source_path.stat()
    code=compile("raise RuntimeError("+repr(MARKER+':'+filename)+")\n",str(source_path),'exec',dont_inherit=True,optimize=0)
    pyc=importlib.util.MAGIC_NUMBER+struct.pack('<III',0,int(st.st_mtime)&0xffffffff,st.st_size&0xffffffff)+marshal.dumps(code)
    for optimization in ('','1'):
     cached=Path(importlib.util.cache_from_source(str(source_path),optimization=optimization));cached.parent.mkdir(exist_ok=True);cached.write_bytes(pyc)
     raw=cached.read_bytes();flags,mtime,size=struct.unpack('<III',raw[4:16])
     check('Cache_header:'+name+':'+filename+':'+(optimization or 'normal'),raw[:4]==importlib.util.MAGIC_NUMBER and flags==0 and mtime==int(st.st_mtime)&0xffffffff and size==st.st_size,{'timestamp_matches':True,'size_matches':True})
    returned=importlib.machinery.SourceFileLoader(filename[:-3],str(source_path)).get_code(filename[:-3])
    check('Ordinary_loader_accepts_but_does_not_execute_cache:'+name+':'+filename,any(isinstance(c,str) and MARKER in c for c in returned.co_consts))
  return path,sha(freeze)
 def launch(path,pin,**options):
  capture=io.StringIO()
  with contextlib.redirect_stdout(capture):result=namespace['run'](path,pin,'preparation_controls.py',(),offline=True,**options)
  return result,json.loads(capture.getvalue())
 path,pin=fixture('stale_pyc')
 result,report=launch(path,pin)
 check('Frozen_launcher_ignores_valid_stale_dependency_and_entry_pyc',result==0 and report['status']=='PASS' and report['stale_sentinel_executed'] is False and report['captured_dependencies']==3 and report['captured_entry'] is True)
 previous={name:sys.modules.get(name) for name in namespace['DEPENDENCIES']}
 poisons={name:types.ModuleType(name) for name in namespace['DEPENDENCIES']}
 try:
  for name,module in poisons.items():module.ORIGIN='STALE_SYS_MODULE';module.__STALE_PYC_SENTINEL__=MARKER;sys.modules[name]=module
  result,report=launch(path,pin)
  check('Frozen_launcher_replaces_existing_local_sys_modules',result==0 and report['stale_sentinel_executed'] is False)
  check('Frozen_launcher_restores_prior_module_registry_after_execution',all(sys.modules.get(name) is module for name,module in poisons.items()))
 finally:
  for name,old in previous.items():
   if old is None:sys.modules.pop(name,None)
   else:sys.modules[name]=old
 def refused(label,path,pin,expected,entry='preparation_controls.py',args=()):
  try:namespace['run'](path,pin,entry,args,offline=True)
  except namespace['FrozenSourceError'] as exc:check(label,expected in str(exc))
  else:check(label,False)
 refused('Wrong_external_freeze_pin_rejected_before_execution',path,'0'*64,'external SHA-256 pin')
 tampered,tampered_pin=fixture('changed_source',False);changed=source("raise RuntimeError('TAMPERED_SOURCE_MUST_NOT_EXECUTE')")
 (tampered/'metadata_rules.py').write_bytes(changed);os.utime(tampered/'metadata_rules.py',(1700000000,1700000000))
 check('Tampered_source_keeps_timestamp_and_size',len(changed)==len(dependencies['metadata_rules.py']) and int((tampered/'metadata_rules.py').stat().st_mtime)==1700000000)
 refused('Changed_source_hash_rejected_despite_matching_timestamp_size',tampered,tampered_pin,'Frozen source bytes differ: metadata_rules.py')
 extra,extra_pin=fixture('extra_source',False);(extra/'unmanifested_local_module.py').write_text("raise RuntimeError('UNMANIFESTED_MUST_NOT_EXECUTE')\n")
 refused('Unmanifested_root_Python_source_rejected',extra,extra_pin,'source inventory differs')
 linked,linked_pin=fixture('symlink_source',False);(linked/'real_metadata_rules.txt').write_bytes(dependencies['metadata_rules.py']);(linked/'metadata_rules.py').unlink();(linked/'metadata_rules.py').symlink_to(linked/'real_metadata_rules.txt')
 refused('Symlinked_source_rejected_even_when_bytes_match',linked,linked_pin,'regular file: metadata_rules.py')
 refused('Offline_collection_refused_before_dispatch',path,pin,'Offline preparation cannot dispatch collection',entry='collect_readbacks.py',args=('--collect',))
 import socket,subprocess
 try:socket.socket()
 except namespace['OfflineTransportError']:check('Socket_creation_denied_before_network_dispatch',True)
 else:check('Socket_creation_denied_before_network_dispatch',False)
 try:subprocess.run([sys.executable,'-c','raise SystemExit(0)'])
 except namespace['OfflineTransportError']:check('Child_process_denied_before_launch',True)
 else:check('Child_process_denied_before_launch',False)
 check('All_actual_preparation_source_files_remain_unchanged',all((OUT/name).stat().st_size==pin['bytes'] and sha((OUT/name).read_bytes())==pin['sha256'] for name,pin in source_pins.items()))
 print(json.dumps({'status':'PASS','scope':'Purely offline source-only execution controls; synthetic harmless stale caches only','controls':len(controls),'matching_timestamp_size_caches_per_module':2,'cached_dependency_modules':3,'cached_entry_scripts':1,'ordinary_loader_cache_acceptance_proved_without_execution':True,'stale_sentinel_executions':0,'external_requests_made':0,'child_processes_launched':0,'transport_audit_guard_enabled':True,'source_pins':source_pins,'results':controls},indent=2,sort_keys=True))
if __name__=='__main__':main()
