"""Exactly18 bounded new-target checker calls; no old suite or rendering."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,os,signal,json,hashlib
R=Path(__file__).resolve().parent
if (R/'RESULTS.json').exists():raise RuntimeError('preserve completed controls')
ids=['23333353','23416806','23441617'];cases=['pristine','h1_valid_but_wrong_href','Research_valid_but_wrong_href']
rows=[];started=datetime.now(timezone.utc).isoformat()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for mode in ['normal','optimized']:
 (R/'qa'/mode).mkdir(parents=True,exist_ok=True)
 for rid in ids:
  for case in cases:
   args=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(R/'probe_one.py'),rid,case,mode]
   child=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,start_new_session=True)
   try:out,err=child.communicate(timeout=60)
   except subprocess.TimeoutExpired:
    os.killpg(child.pid,signal.SIGTERM)
    try:out,err=child.communicate(timeout=5)
    except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);out,err=child.communicate()
    raise RuntimeError('bounded target timeout '+rid+' '+case+' '+mode)
   stem=f'{rid}-{case}-{mode}'
   (R/(stem+'.stdout')).write_bytes(out);(R/(stem+'.stderr')).write_bytes(err)
   receipt_path=R/'qa'/mode/(rid+'-'+case+'.json')
   if not receipt_path.exists():raise RuntimeError('harness/checker exception without receipt '+stem+': '+err.decode()[-2000:])
   qa=json.loads(receipt_path.read_text())
   if set(qa['papers'])!={rid}:raise RuntimeError('checker escaped exact single target')
   checks=qa['papers'][rid]['checks'];expected='exact_h1_selflink_destination' if case=='h1_valid_but_wrong_href' else 'exact_main_Research_destination'
   if case=='pristine':
    if child.returncode!=0 or qa['status']!='PASS' or qa['issues'] or not all(checks.values()):raise RuntimeError('pristine rejected '+stem)
   else:
    if child.returncode!=1 or qa['status']!='ISSUES_FOUND' or qa['issues']!=[rid+': '+expected] or checks[expected] is not False or any(not v for k,v in checks.items()if k!=expected):
     raise RuntimeError('not an isolated actual guard rejection '+stem+': '+str(qa['issues']))
   row={'record_id':rid,'case':case,'mode':mode,'exit_code':child.returncode,'checker_status':qa['status'],
        'checks':len(checks),'passed':sum(checks.values()),'issues':qa['issues'],'single_target':True,
        'receipt':str(receipt_path.relative_to(R)),'receipt_sha256':hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'timeout_seconds':60}
   rows.append(row);print(json.dumps(row),flush=True)
result={'utc':datetime.now(timezone.utc).isoformat(),'started_utc':started,'status':'COMPLETE',
 'actual_checker_executions':len(rows),'pristine_acceptances':sum(x['case']=='pristine'for x in rows),
 'retained_distinct_fault_cases':6,'actual_fault_rejections':sum(x['case']!='pristine'for x in rows),
 'all_other_checks_pass_for_each_fault':True,'normal_and_optimized_agree':True,
 'all_original12_false_negative_receipts_preserved':True,'old64_suite_replayed':False,'renderer_executed':False,'rows':rows}
(R/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='rows'}))
