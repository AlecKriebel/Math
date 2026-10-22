from pathlib import Path
import subprocess,sys,json,datetime,hashlib
R=Path(__file__).resolve().parent
runs=[]
for flags in [[],['-O'],['-OO']]:
 records={}
 for script,receipt in [('offline_guards.py','OFFLINE_GUARD_RECEIPT.json'),('offline_services.py','OFFLINE_SERVICE_RECEIPT.json'),('independent_checks.py','INDEPENDENT_CHECK_RECEIPT.json')]:
  p=subprocess.run([sys.executable,'-B',*flags,str(R/script)],capture_output=True,text=True)
  if p.returncode:raise RuntimeError(p.stderr)
  records[script]=json.loads((R/receipt).read_text())
 runs.append({'flags':flags,'records':records})
(R/'OFFLINE_MODES_RECEIPT.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'reviewer_programs':{n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['offline_guards.py','offline_services.py','independent_checks.py']}},indent=2)+'\n')
print(json.dumps({'runs':len(runs),'service_cases':len(runs[0]['records']['offline_services.py']['results']),'all_service_cases_passed':all(x['records']['offline_services.py']['all_passed'] for x in runs),'guard_expected_findings_per_mode':[[x['case'] for x in r['records']['offline_guards.py']['results'] if x['unexpected']] for r in runs]}))
