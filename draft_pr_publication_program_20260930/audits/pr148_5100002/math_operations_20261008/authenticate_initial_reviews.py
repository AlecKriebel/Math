#!/usr/bin/env python3
"""ROOT readback of exact archived inputs and completed independent audit evidence."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
from fractions import Fraction
import json, os, stat

A=Path(__file__).resolve().parent.parent
def require(condition, message):
    if not condition: raise RuntimeError(message)
def pin(path):
    require(path.is_file() and not path.is_symlink(), 'not regular: '+str(path))
    b=path.read_bytes()
    return {'path':str(path.relative_to(A)), 'bytes':len(b),
            'mode':stat.S_IMODE(path.stat().st_mode), 'sha256':sha256(b).hexdigest()}
def checked(path, expected, size=None):
    p=pin(path)
    require(p['sha256']==expected and (size is None or p['bytes']==size), 'pin mismatch: '+str(path))
    return p
def read(path): return json.loads(path.read_bytes())

manifest=A/'ORIGINAL_SUBMITTED_ATTEMPT_MANIFEST.json'
checked(manifest,'efd273eb031989bddae0ae89cad8d2e92cc6f531d2076d20d09155a8b508cb02',5703)
m=read(manifest); originals=[]
require(m['original_head']=='538fd2584f7dc7375e4eaa91d73daddde3d073cd','head mismatch')
require(len(m['original_files'])==20 and m['literal_original_status']=='claimed_solved','source scope')
for r in m['original_files']:
    p=checked(A/'original_submitted_attempt'/r['path'],r['sha256'],r['bytes'])
    require(p['mode']==r['mode'],'original mode mismatch'); originals.append(p)
require({str(p.relative_to(A/'original_submitted_attempt')) for p in (A/'original_submitted_attempt').rglob('*') if p.is_file()}=={r['path'] for r in m['original_files']},'archive extras')
turns=read(A/'original_submitted_attempt/turns.json')
code=A/'verification_code_adversary_20261008'
inventory=read(code/'AUDIT_ARTIFACT_INVENTORY.json')
checked(code/'AUDIT_REPORT.md','3d18e643ca1802527abe79da535e53f62f3543847d5a95f0ebc450d2fc046162')
auditpins=[checked(code/r['path'],r['sha256'],r['bytes']) for r in inventory]
runs=[]
for d in sorted((code/'raw_runs').iterdir()):
    require(d.is_dir() and not d.is_symlink(),'raw run directory')
    r=read(d/'process_receipt.json')
    require(r['label']==d.name and r['wait_completed_and_reaped'] is True and r['group_absent_after_wait'] is True and r['termination_reason'] is None,'unclosed audit child')
    require(type(r['pid']) is int and r['pid']>0 and r['pgid']==r['pid'],'invalid child identity')
    for kind in ['stdout','stderr']:
        checked(d/(kind+'.txt'),r['raw_'+kind+'_sha256'],r['raw_'+kind+'_bytes'])
    require(r['raw_stdout_bytes']+r['raw_stderr_bytes']<=r['raw_output_cap_bytes'],'output cap')
    require(r.get('exit_expectation_met',True) is True,'unexpected audit exit')
    runs.append({'label':r['label'],'pid':r['pid'],'returncode':r['returncode'], 'receipt':pin(d/'process_receipt.json')})
require(len(runs)==62,'wrong audit child count')
g=A/'geometry_falsification_20261008'
gm=read(g/'ARTIFACT_MANIFEST.json')
gpins=[checked(g/r['name'],r['sha256'],r['bytes']) for r in gm['artifacts']]
gr=read(g/'independent_geometry_results.json')
require(gr['PH']['k108']=='11664/3125' and gr['PV']['k108']=='3645/1024' and gr['exact_k108_difference']=='553311/3200000','geometric arithmetic')
require(Fraction(gr['PH']['k108'])-Fraction(gr['PV']['k108'])==Fraction(gr['exact_k108_difference']),'difference')
an=A/'analytic_family_adversary_20261008'
apins=[pin(an/f) for f in ['ANALYTIC_AUDIT.md','check_analytic_family.py','exact_check_output.json','RESEARCH_LOG.md']]
record={'schema':'pr148-root-initial-review-readback/v1',
        'utc':datetime.now(timezone.utc).isoformat(),'actual_ROOT_PID':os.getpid(),
        'status':'ACCEPTED_INPUTS_AND_INITIAL_REVIEW_EVIDENCE_ONLY',
        'original_head':m['original_head'],'original_effort':'1/5',
        'original_author_approach_ledger_present':True,'original_author_approach_ledger_path':'turns.json',
        'actual_timestamped_author_chat_turn_ledger_present':False,
        'original_native_transition_ledger_present':False,'new_central_proof_search_turns':0,
        'original20':originals,'code_audit_artifacts':auditpins,'closed_code_audit_children':runs,
        'geometry_review_artifacts':gpins,'analytic_review_artifacts':apins,
        'code_repair_integration_pending':True,'mathematical_acceptance':None,
        'priority_acceptance':None,'publication_acceptance':None,'native_acceptance':None}
out=A/'ROOT_INITIAL_REVIEW_READBACK_20261008.json'
require(not out.exists(),'receipt already exists')
out.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':record['status'],'original_files':len(originals),'closed_audit_children':len(runs),'receipt':pin(out)}))
