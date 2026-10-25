"""Exactly eighteen fresh single-target calls; no broad suites or rendering."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, signal, subprocess

O = Path(__file__).resolve().parent
def need(ok, message):
    if not ok:
        raise RuntimeError(message)
need(not (O/'RESULTS.json').exists(), 'preserve completed recheck')
for mode in ('normal','optimized'):
    (O/'qa'/mode).mkdir(parents=True, exist_ok=True)
(O/'read-observations').mkdir(exist_ok=True)
started = datetime.now(timezone.utc).isoformat()
rows = []
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
for mode in ('normal','optimized'):
    for rid in ('23333353','23416806','23441617'):
        for case in ('pristine','h1_valid_but_wrong_href','Research_valid_but_wrong_href'):
            command = [sys.executable,'-B'] + (['-O'] if mode == 'optimized' else []) + [str(O/'probe_one.py'),rid,case,mode]
            begin = datetime.now(timezone.utc).isoformat()
            child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     env=environment, start_new_session=True)
            timeout = False
            try:
                stdout, stderr = child.communicate(timeout=60)
            except subprocess.TimeoutExpired:
                timeout = True
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    stdout, stderr = child.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    stdout, stderr = child.communicate()
            stem = f'{rid}-{case}-{mode}'
            (O/(stem+'.stdout')).write_bytes(stdout)
            (O/(stem+'.stderr')).write_bytes(stderr)
            receipt = O/'qa'/mode/(rid+'-'+case+'.json')
            row = {'record_id':rid,'case':case,'mode':mode,'started_utc':begin,
                   'completed_utc':datetime.now(timezone.utc).isoformat(),'command':command,
                   'exit_code':child.returncode,'timeout':timeout,'timeout_seconds':60,
                   'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_bytes':len(stderr),
                   'receipt':str(receipt.relative_to(O)) if receipt.exists() else None}
            need(not timeout, 'target timeout; actual output preserved: '+stem)
            need(receipt.is_file(), 'no actual checker receipt: '+stem+' '+stderr.decode()[-1000:])
            qa = json.loads(receipt.read_text())
            need(set(qa['papers']) == {rid}, 'not exactly one requested target: '+stem)
            checks = qa['papers'][rid]['checks']
            guard = None if case == 'pristine' else ('exact_h1_selflink_destination' if case == 'h1_valid_but_wrong_href' else 'exact_main_Research_destination')
            good = (child.returncode == 0 and qa['status'] == 'PASS' and not qa['issues'] and all(checks.values())) if guard is None else (child.returncode == 1 and qa['status'] == 'ISSUES_FOUND' and qa['issues'] == [rid+': '+guard] and checks[guard] is False and all(v for k,v in checks.items() if k != guard))
            row.update({'expected_guard':guard,'status':qa['status'],'checks':len(checks),
                        'passed':sum(checks.values()),'issues':qa['issues'],'expected_outcome':good,
                        'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest()})
            rows.append(row)
            (O/'PROGRESS.json').write_text(json.dumps({'started_utc':started,'completed_runs':len(rows),'rows':rows},indent=2)+'\n')
            print(json.dumps({k:row[k] for k in ('record_id','case','mode','exit_code','checks','passed','issues','expected_outcome')}), flush=True)
            need(good, 'unexpected checker outcome; actual evidence preserved: '+stem)
            need(not stderr, 'unexpected stderr retained: '+stem)
result = {'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),
          'status':'PASS_BOUNDED_INDEPENDENT_RECHECK','actual_checker_executions':len(rows),
          'pristine_acceptances':sum(r['case']=='pristine' for r in rows),
          'distinct_retained_fault_samples':6,'actual_isolated_fault_rejections':sum(r['case']!='pristine' for r in rows),
          'normal_and_optimized_agree':True,'old64_suite_replayed':False,'renderer_executed':False,
          'schema_campaign_replayed':False,'rows':rows}
need(len(rows)==18, 'wrong bounded execution count')
(O/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'rows'}))
