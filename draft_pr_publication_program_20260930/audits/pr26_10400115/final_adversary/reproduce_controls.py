#!/usr/bin/env python3
"""Isolated unchanged copies only; current replay is not past-run attestation."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json, shutil, subprocess, sys
OWN=Path(__file__).resolve().parent
BASE=OWN.parent
RUN=OWN/'tmp/replay'
if RUN.exists():raise SystemExit('Preserve existing run; choose a new version.')
RUN.mkdir()
results=[]
for script,receipt in [('verify.py','verification.json'),('review/independent_checks.py','review/independent_results.json')]:
    p=RUN/'original'/script;p.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(BASE/'source_snapshot'/script,p)
    done=subprocess.run(['/usr/bin/python3',str(p)],cwd=p.parent,capture_output=True,text=True)
    produced=(RUN/'original'/receipt).read_bytes()
    old=(BASE/'source_snapshot'/receipt).read_bytes()
    assert done.returncode==0 and old==produced,(script,done.stderr)
    results.append({'script':script,'runtime':'/usr/bin/python3','exit':done.returncode,'receipt_byte_equal':True,'script_sha256':sha256(p.read_bytes()).hexdigest(),'receipt_sha256':sha256(produced).hexdigest(),'receipt':json.loads(produced)})
for family,script,receipt,runtime in [('specialization_family','independent_controls.py','INDEPENDENT_CONTROLS.json',sys.executable),('modular_family','modular_controls.py','modular_results.json',sys.executable),('primary_scope_family','independent_source_scope_controls.py','independent_source_scope_results.json','/usr/bin/python3')]:
    root=RUN/family;root.mkdir()
    shutil.copy2(BASE/family/script,root/script)
    if family=='primary_scope_family':
        shutil.copytree(BASE/family/'primary_sources',root/'primary_sources')
        shutil.copytree(BASE/'source_snapshot',RUN/'source_snapshot')
    done=subprocess.run([runtime,str(root/script)],cwd=root,capture_output=True,text=True)
    assert done.returncode==0,(family,done.stderr)
    fresh=json.loads((root/receipt).read_text());old=json.loads((BASE/family/receipt).read_text())
    exclude={'executed_utc','python','started_utc','finished_utc','python_version','utc','sympy_version'}
    clean=lambda x:{k:v for k,v in x.items() if k not in exclude}
    assert clean(fresh)==clean(old),(family,clean(fresh),clean(old))
    results.append({'family':family,'script':script,'runtime':runtime,'exit':done.returncode,'script_byte_equal':(root/script).read_bytes()==(BASE/family/script).read_bytes(),'mathematical_receipt_equal':True,'excluded_environment_fields':sorted(exclude&set(fresh)),'assertions':fresh['assertions'],'receipt_sha256':sha256((root/receipt).read_bytes()).hexdigest(),'recorded_receipt_sha256':sha256((BASE/family/receipt).read_bytes()).hexdigest(),'fresh_receipt':fresh})
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','results':results,'scope':'Only ignored isolated copies executed. Historical adjacent receipts and source scripts remain unchanged; clocks/interpreter fields excluded only for family comparisons. No universal proof follows from finite checks.'}
(OWN/'REPRODUCTION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','original_byte_exact_receipts':2,'family_assertions':[x.get('assertions') for x in results[2:]]}))
