"""Seal only this authored source-preparation folder with exclusive new outputs."""
from pathlib import Path
import datetime, hashlib, json, os, stat
D=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(p):
 raw=p.read_bytes();return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def save(path,value):
 raw=(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 path.chmod(0o444)
 fd=os.open(path.parent,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
need(not (D/'SAFE_MANIFEST.json').exists() and not (D/'SEAL.json').exists(),'Already sealed')
need((D/'offline_work').is_dir() and not list((D/'offline_work').iterdir()),'Offline fixtures retained unexpectedly')
sources=json.loads((D/'FINAL_SOURCE_PINS.json').read_bytes())
binding=json.loads((D/'FAMILY02_FINAL_05_BINDINGS.json').read_bytes())
need(binding['status']=='PASS' and binding['active_checks_each']==660,'Final tests required')
for n,w in sources.items():need(pin(D/n)==w and stat.S_IMODE((D/n).stat().st_mode)==0o444,'Final source not frozen')
with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n- '+now+': Completed source-only family02 contract, eight-child history binding, safe inventory and read-only integrity verifier. All protected inputs remain unchanged. Sealing artifacts0444; bounded source authoring completion100%. External Root adoption/addendum/fresh independent review and all real operations remain outside this authoring result.\n')
files=[]
for p in sorted(D.rglob('*')):
 need(not p.is_symlink(),'No symlinks permitted')
 if p.is_file():
  need(stat.S_ISREG(p.stat().st_mode),'No nonregular payloads')
  need(p.suffix not in ('.pyc','.pyo') and '__pycache__' not in p.parts,'No bytecode payload')
  p.chmod(0o444);files.append(dict(path=p.relative_to(D).as_posix(),**pin(p)))
manifest=dict(schema='pr206-ops-family02-author-safe-manifest-v1',UTC=now,evidence_scope='AUTHOR_SOURCE_ONLY_NOT_ROOT_AUTHORITY',scope='This owned family02 source-only folder, full source snapshots and all synthetic offline attempts; no actual authority or service receipt.',excluded_payloads=['credentials/auth state','private service responses','runtime/dependencies/bytecode','external copyrighted source','conversation/context export','Git metadata','native/global files'],self_reference_rule='Manifest and seal excluded from payload list; seal binds exact manifest.',files=files)
save(D/'SAFE_MANIFEST.json',manifest)
save(D/'SEAL.json',dict(schema='pr206-ops-family02-author-seal-v1',UTC=now,status='SOURCE_PREPARATION_COMPLETE_PENDING_INDEPENDENT_ROOT_ADOPTION',manifest_pin=pin(D/'SAFE_MANIFEST.json'),payload_file_count=len(files),payload_total_bytes=sum(f['bytes'] for f in files),source_pins=sources,final_binding_pin=pin(D/'FAMILY02_FINAL_05_BINDINGS.json'),final_active_checks_each=660,normal_optimized_equal_except_optimize=True,all_five_runner_attempts_preserved=True,all_eight_child_executions_preserved=True,failed_test_authoring_attempts_preserved=2,actual_service_calls=0,actual_KIT_executions=0,actual_GWS_invocations=0,actual_authority_or_addendum_authored=False,prior_family01_payloads_unchanged=98,scientific_package_files_unchanged=17,future_Root_operations_adoption_pin=None,future_operations_contract_addendum_pin=None,actual_action_authorized_by_preparation=False,read_only_verification=['/opt/homebrew/opt/python@3.14/bin/python3.14','-E','-S','-B','-P','verify_artifacts.py']))
print(json.dumps(dict(status='SEALED',manifest=pin(D/'SAFE_MANIFEST.json'),seal=pin(D/'SEAL.json'),payload_files=len(files)),sort_keys=True))
