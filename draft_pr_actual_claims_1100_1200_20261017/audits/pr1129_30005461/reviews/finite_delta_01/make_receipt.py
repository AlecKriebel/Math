#!/usr/bin/env python3
"""Re-run ordinary/optimized checks and fingerprint this authored audit only."""
from pathlib import Path
import datetime
import hashlib
import json
import platform
import subprocess
import sys

root=Path(__file__).resolve().parent

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def run(command,destination):
    result=subprocess.run(command,cwd=root,capture_output=True,check=False)
    (root/destination).write_bytes(result.stdout)
    if result.returncode:
        raise RuntimeError('Checker failed: '+str(command)+'; '+result.stderr.decode(errors='replace'))
    return {'command':command,'exit_code':result.returncode,'output':destination,
            'bytes':len(result.stdout),'sha256':hashlib.sha256(result.stdout).hexdigest()}

normal=run([sys.executable,'checker.py'],'RESULTS.normal.json')
optimized=run([sys.executable,'-O','checker.py'],'RESULTS.optimized.json')
if (root/normal['output']).read_bytes()!=(root/optimized['output']).read_bytes():
    raise RuntimeError('Normal and optimized mathematical outputs differ')
result=json.loads((root/normal['output']).read_text())
if result['verdict']!='PASS':raise RuntimeError('Checker result is not PASS')
public={}
for path in sorted(root.rglob('*')):
    relative=path.relative_to(root)
    if not path.is_file() or relative==Path('RECEIPT.json'):continue
    if relative.parts[0]=='tmp' or relative.parts[:2]==('sources','private'):continue
    if '__pycache__' in relative.parts:raise RuntimeError('Unexpected public Python cache')
    public[str(relative)]={'bytes':path.stat().st_size,'sha256':digest(path)}
receipt={'format':'independent-finite-delta-audit-receipt-v1',
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'audit_verdict':'PASS for assigned algebra/threshold/optional-delta interfaces',
    'publication_or_external_contact_actions':'none',
    'frozen_head_supplied_by_parent':'26fed29c1130e539ba018a37200f133870f0e036',
    'runtime':{'python':sys.version,'platform':platform.platform()},
    'runs':[normal,optimized],'normal_optimized_outputs_identical':True,
    'finite_check_count':result['total_checks'],'negative_control_count':result['negative_control_count'],
    'input_pins':result['evidence']['input_pins'],
    'source_versions':json.loads((root/'sources/FETCH_RECEIPTS.json').read_text()),
    'source_inspection_boundary_file':'sources/SOURCES.md',
    'public_authored_files_excluding_this_receipt':public,
    'exclusion_rule':'RECEIPT.json itself, ignored sources/private/**, ignored tmp/** only; no third-party source body is public',
    'claim_boundary':'Finite tests falsify transcription/interface errors; universal proofs are REPORT.md. Principal geometric theorem applicability and section lifting are separate audit-family dependencies. Optional real delta uses v1 Definition 6.3 only; prior-result bridge imports stated v1 Theorem 6.4 explicitly.'}
(root/'RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'verdict':receipt['audit_verdict'],'checks':result['total_checks'],
    'controls':result['negative_control_count'],'public_files':len(public),
    'report_sha256':digest(root/'REPORT.md'),'receipt_sha256':digest(root/'RECEIPT.json')},sort_keys=True))
