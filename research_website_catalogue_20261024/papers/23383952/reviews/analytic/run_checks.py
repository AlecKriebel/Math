"""Run only one inspected pure arithmetic source and this own exact checker."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
O=Path(__file__).resolve().parent;B=O.parents[1]
source=B/'sources/published-source/trace_audit_01/check_trace_bounds.py';own=O/'analytic_checks.py'
rows=[]
for name,script in [('deposited-arithmetic',source),('independent-arithmetic',own)]:
 for mode in ['normal','optimized']:
  cmd=[sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(script)];started=datetime.datetime.now(datetime.timezone.utc).isoformat()
  r=subprocess.run(cmd,cwd=O,capture_output=True,timeout=30)
  stem=O/(name+'-'+mode);stem.with_suffix('.stdout').write_bytes(r.stdout);stem.with_suffix('.stderr').write_bytes(r.stderr)
  result=json.loads(r.stdout) if r.returncode==0 else None
  good=r.returncode==0 and not r.stderr and result and (result.get('accepted') is True if name=='deposited-arithmetic' else result.get('status')=='PASS')
  row={'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'script_bytes':script.stat().st_size,'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'exit_code':r.returncode,'stderr_bytes':len(r.stderr),'verified':bool(good)}
  stem.with_suffix('.execution.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
  if not good:raise RuntimeError('exact arithmetic failure:'+name+':'+mode)
(O/'CHECKS_SUMMARY.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_runs':4,'source_program_scope':'Only fully read pure stdlib Fraction arithmetic program; no source builder/finalizer/verifier','independent_program_is_not_source_import':'Own different pi identity/root algorithm/Taylor degrees','runs':rows},indent=2)+'\n')
print(json.dumps({'status':'PASS','actual_runs':4}))
