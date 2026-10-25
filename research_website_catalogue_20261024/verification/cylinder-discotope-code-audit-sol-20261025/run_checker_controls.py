"""Bounded independent controls; neither old suite nor renderer is dispatched."""
from pathlib import Path
import datetime,hashlib,json,os,signal,subprocess
A=Path(__file__).resolve().parent
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
cases=[(rid,case) for rid in ['23387774','23074543'] for case in ['pristine','omit_status_paragraph','wrong_visible_date','wrong_visible_edition','wrong_visible_citation_edition','omit_proof_paragraph','wrong_iframe','wrong_original_download','wrong_schema_license','wrong_orcid','altered_reader_bytes']]
out=[]
for rid,case in cases:
    proc=subprocess.Popen([PY,'-B',str(A/'fault_checker.py'),rid,case],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
    try:stdout,stderr=proc.communicate(timeout=25)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGTERM);stdout,stderr=proc.communicate(timeout=5);raise RuntimeError('bounded_checker_timeout')
    report=A/('checker-'+rid+'-'+case+'.json')
    result=json.loads(report.read_text()) if report.is_file() else None
    out.append({'record_id':rid,'case':case,'exit':proc.returncode,'stderr':stderr,'report':str(report) if result else None,'status':result.get('status') if result else None,'issues':result.get('issues') if result else None,'reported_check_count':sum(len(x['checks']) for x in result['papers'].values()) if result else None,'stdout_SHA256':hashlib.sha256(stdout.encode()).hexdigest(),'dispatched_old_legacy_suite':False})
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controls':out,'private_stage_mutations':False,'source_mutations':False,'fixture_tree_copies':0,'old_suite_dispatches':0,'renderer_dispatches':0}
(A/'CHECKER_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
