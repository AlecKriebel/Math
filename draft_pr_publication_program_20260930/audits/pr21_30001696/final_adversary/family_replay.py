"""Replay preserved family controls in ignored copies without modifying them."""
from pathlib import Path
import hashlib,json,shutil,subprocess
from datetime import datetime,timezone
base=Path(__file__).resolve().parent;parent=base.parent;tmp=base/'tmp/family_replay';tmp.mkdir(exist_ok=True)
rows=[]
shutil.copytree(parent/'source_snapshot',tmp/'source_snapshot',dirs_exist_ok=True)
specs=[('analytic_family','new_controls.py','new_control_results.json',['created_at_utc','runtime']),('topology_family','countermodel_controls.py','countermodel_results.json',['created_at_utc']),('primary_scope_family','scope_checks.py','scope_checks.json',['utc']),('priority_mechanism_family','priority_controls.py','CONTROL_RESULTS.json',[])]
for family,script,result,exclude in specs:
 work=tmp/family;work.mkdir(exist_ok=True);shutil.copy(parent/family/script,work/script)
 if family=='primary_scope_family':shutil.copy(parent/family/'first_pass_seal.json',work/'first_pass_seal.json')
 reused=(work/result).exists()
 if not reused:
  proc=subprocess.run(['/usr/bin/python3',str(work/script)],capture_output=True,text=True)
  assert proc.returncode==0,(family,proc.stderr)
 a=json.loads((parent/family/result).read_text());b=json.loads((work/result).read_text())
 for key in exclude:a.pop(key,None);b.pop(key,None)
 assert a==b,(family,a,b)
 rows.append({'family':family,'script':script,'script_sha256':hashlib.sha256((parent/family/script).read_bytes()).hexdigest(),'excluded_fields':exclude,'all_other_fields_equal':True,'reused_completed_ignored_receipt':reused,'assertions':b.get('assertions',b.get('total_assertions')),'status':'PASS'})
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','replays':rows,'mathematical_family_total':sum(r['assertions'] for r in rows[:3]),'scope':'Finite receipt reproduction, not proof. Analytic runtime differs legitimately (Python3.9.6 versus3.14.6); excluded runtime and timestamp only after initial complete equality check flagged runtime. No mathematical value differed.'}
(base/'FAMILY_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
