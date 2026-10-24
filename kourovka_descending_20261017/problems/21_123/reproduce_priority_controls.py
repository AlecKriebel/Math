#!/usr/bin/env python3
"""Root reproduces prior-proof diagnostic checks without rewriting frozen artifacts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys,tempfile,time
BASE=Path(__file__).resolve().parent
CHECKS=[('priority/verify_sources.py','priority/source_check.json'),('priority_crosscheck/check_literal_diagnostics.py','priority_crosscheck/literal_diagnostic_results.json'),('priority_crosscheck/fraga_proof_scope/check_operator_words.py','priority_crosscheck/fraga_proof_scope/CHECK_RESULTS.json')]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    receipt=json.loads((BASE/'priority_crosscheck/RECEIPT.json').read_text());verified=[]
    for field in ['current_inputs','outputs']:
        for x in receipt[field]:
            assert digest(BASE/x['path'])==x['sha256'],x['path'];verified.append(x['path'])
    tests=[]
    for script,out in CHECKS:
        original=json.loads((BASE/out).read_text())
        with tempfile.TemporaryDirectory(prefix='kourovka123_priority_') as td:
            target=Path(td)/'21_123';shutil.copytree(BASE,target,ignore=shutil.ignore_patterns('__pycache__','.venv','tmp'))
            start=time.monotonic();r=subprocess.run([sys.executable,str(target/script)],capture_output=True,text=True,timeout=120)
            assert r.returncode==0,(script,r.stderr)
            fresh=json.loads((target/out).read_text())
            no_time=lambda x:{k:v for k,v in x.items() if k!='utc'}
            assert no_time(original)==no_time(fresh),script
            tests.append({'checker':script,'sha256':digest(BASE/script),'exit_code':r.returncode,'seconds':round(time.monotonic()-start,4),'non_timestamp_fields_match':True,'stdout':r.stdout})
    for field in ['current_inputs','outputs']:
        for x in receipt[field]:assert digest(BASE/x['path'])==x['sha256']
    result={'utc':datetime.now(timezone.utc).isoformat(),'prior_work_doi':'10.20944/preprints202608.2109.v1','scope':'Current-byte custody and reproduction of bounded prior-proof controls, alongside separately documented unbounded human-readable proof challenge. No original result or human peer review certification.','reviewed_hashes_verified':len(verified),'checks':tests,'all_passed':True,'original_outputs_preserved':True,'source_recheck_delta':'ROOT_SOURCE_RECHECK.json'}
    (BASE/'ROOT_AUDIT_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','hashes':len(verified),'checks':len(tests)}))
if __name__=='__main__':main()
