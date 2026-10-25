"""One explicit old67 checker dispatch and 67 actual paired renderer runs."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,sys,time
O=Path(__file__).resolve().parent
frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text());ids=frozen['old_configured_record_ids_in_order']
if len(ids)!=67 or len(set(ids))!=67:raise RuntimeError('unexpected frozen old set')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def binding(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
sentinel=O/'LEGACY_SUITE_ONCE.json'
if sentinel.exists():raise RuntimeError('old67 campaign already dispatched; do not repeat')
tested={n:binding(O/n) for n in ['odd_ear_blocking_source.py','oeb_body_contract.py','render_page.proposed.py','final-content-check.proposed.py','final-content-check.stage.py','memory_render_pair.py','legacy_once.py']}
sentinel.write_text(json.dumps({'utc':now(),'old_record_ids_in_order':ids,'checker_dispatches_authorized':1,'paired_records':67,'complete_renderer_executions_expected':134,'tested_programs':tested},indent=2)+'\n')
out=O/'legacy67';out.mkdir()
cmd=[sys.executable,'-B',str(O/'execute.py'),str(O/'stage_reader.py'),str(O/'final-content-check.stage.py')]+ids+['--site',str(O/'public'),'--output-dir',str(out),'--output-stem','actual-old67']
started=now();t=time.monotonic();r=subprocess.run(cmd,capture_output=True,timeout=240)
(out/'stdout').write_bytes(r.stdout);(out/'stderr').write_bytes(r.stderr)
qa=json.loads((out/'actual-old67.json').read_text()) if (out/'actual-old67.json').exists() else None
good=r.returncode==0 and not r.stderr and qa and qa['status']=='PASS' and list(qa['papers'])==ids and all(all(p['checks'].values()) for p in qa['papers'].values())
receipt={'started_utc':started,'finished_utc':now(),'command':cmd,'exit_code':r.returncode,'stderr_bytes':len(r.stderr),'elapsed_seconds':time.monotonic()-t,'actual_status':None if qa is None else qa['status'],'actual_record_count':0 if qa is None else len(qa['papers']),'actual_checks':0 if qa is None else sum(len(p['checks']) for p in qa['papers'].values()),'verified':bool(good)}
(out/'execution.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
if not good:sys.exit(1)
root=O/'memory-equivalence';root.mkdir()
def run(rid):
 cmd=[sys.executable,'-B',str(O/'execute.py'),str(O/'memory_render_pair.py'),rid]
 started=now();t=time.monotonic();r=subprocess.run(cmd,capture_output=True,timeout=120)
 (root/(rid+'.stdout')).write_bytes(r.stdout);(root/(rid+'.stderr')).write_bytes(r.stderr)
 result=json.loads(r.stdout) if r.returncode==0 else None
 good=r.returncode==0 and not r.stderr and result and result['current_and_proposed_actual_output_bytes_equal'] and result['original_reads_equal'] and result['renderer_receipts_equal']
 row={'record_id':rid,'started_utc':started,'finished_utc':now(),'command':cmd,'exit_code':r.returncode,'stderr_bytes':len(r.stderr),'elapsed_seconds':time.monotonic()-t,'verified':bool(good)}
 (root/(rid+'.execution.json')).write_text(json.dumps(row,indent=2)+'\n');return row,result
results=[];inputs={}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for row,result in pool.map(run,ids):
  results.append(row)
  if result:
   for path,b in result['original_read_bindings'].items():
    if path in inputs and inputs[path]!=b:raise RuntimeError('mutable original read during campaign:'+path)
    inputs[path]=b
  if len(results)%10==0:print(json.dumps({'paired_records_complete':len(results),'verified':sum(x['verified'] for x in results)}),flush=True)
summary={'utc':now(),'status':'PASS' if all(x['verified'] for x in results) else 'FAIL','paired_records':len(results),'complete_renderer_executions':2*len(results),'comparison':'actual complete output dictionaries compared by byte equality before emitting hash metadata','filesystem_output_writes':0,'results':results}
(root/'ACTUAL_INPUT_BINDINGS.json').write_text(json.dumps({'utc':now(),'bindings':inputs},indent=2)+'\n')
(root/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='results'}),flush=True)
sys.exit(0 if summary['status']=='PASS' else 1)
