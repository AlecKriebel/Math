"""Latest dispatcher/installer regression and exact entrypoint tests, offline."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
H=Path(__file__).absolute().parent
PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
OUT=H/'final_results';OUT.mkdir()
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def run(label, source, harness, args, optimized=False):
 argv=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(harness)]+args
 r={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'argv':argv,'source':ident(source),'harness':ident(harness),'interpreter':ident(Path(PY).resolve())}
 try:
  p=subprocess.run(argv,cwd=H,capture_output=True,timeout=3)
  r.update(exit=p.returncode,timeout=False,stdout=p.stdout.decode(),stderr=p.stderr.decode())
 except subprocess.TimeoutExpired as e:r.update(exit=None,timeout=True,stdout=(e.stdout or b'').decode(),stderr=(e.stderr or b'').decode())
 (OUT/(label+'.json')).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 return r
D=H.parent/'root_lifecycle_runner_01/run_lifecycle206_v3.py'
I=H.parent/'root_program_lock_installation_01/install_program_lock206_v4.py'
scenarios=['checked_regular','checked_writable','checked_symlink','checked_directory','checked_oversize','checked_dotdot','checked_fifo','checked_fifo_swap','preflight','bind','phase_exception','phase_exception_uncaught','chained_exception_uncaught','constructor_failure','install_before_constructor','install_after_aliases','alias_read_failure','alias_restore_failure','close_failure','guard_relative','guard_outside','guard_kwargs','bad_graph','bad_dispatcher_pin','bad_backend_pin','bad_source_pin','bad_gate_pin','bad_adoption_pin']
scenarios+=['route_'+p+'_'+a for p in ('ready','merge','factual','completion') for a in ('preflight','bind','prepare','verify','accept','sync','pointer')]
records=[]
for scenario in scenarios:records.append(run('dispatcher_'+scenario,D,H/'audit_harness_final.py',[scenario]))
for scenario in ('create','reuse','bad_protocol','bad_self_pin','bad_payload','bad_mode','fifo_adoption','fifo_lock','symlink_lock','busy_lock','existing_receipt','error_uncaught','fifo_swap_before_lock_open'):
 records.append(run('installer_'+scenario,I,H/'installer_harness_final.py',[scenario]))
for label,source in (('dispatcher',D),('installer',I)):
 copy=H/('FINAL_'+source.name);copy.write_bytes(source.read_bytes());copy.chmod(0o444)
 for kind,args in [('help',['--help']),('badint',['--adoption-bytes','SYNTHETIC_PARSE_SECRET_206']),('unknown',['--SYNTHETIC_UNKNOWN_SECRET_206']),('missing',[])]:
  records.append(run(label+'_'+kind,source,copy,args))
 records.append(run(label+'_optimized',source,copy,['--help'],optimized=True))
summary={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tests':len(records),'timeouts':[r['label'] for r in records if r['timeout']],'runner':ident(Path(__file__))}
(H/'FINAL_RUN_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps(summary,sort_keys=True))
