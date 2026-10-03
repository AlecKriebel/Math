"""Root genuine unchanged original-file replays in new private copies."""
import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr42_2233';S=A/'source_snapshot_v2';O=A/'root_original_actual_reproduction_v2'
def H(b):return hashlib.sha256(b).hexdigest()
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def row(p):
    b=p.read_bytes();return dict(path=p.relative_to(O).as_posix(),bytes=len(b),sha256=H(b))
def J(p):return json.loads(p.read_bytes())
assert sys.flags.optimize==0 and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
O.mkdir(exist_ok=False);(O/'prelaunch_operator.py').write_bytes(Path(__file__).read_bytes())
snapshot=J(A/'snapshot_manifest_v2.json')
for z in snapshot['files']:
    b=(S/z['path']).read_bytes();assert len(b)==z.get('size',z.get('bytes')) and H(b)==z['sha256']
assert (S/'check_spectra.py').read_bytes()==(S/'review/submitted_check_spectra.py').read_bytes()
old=(S/'review/PARTIAL.md').read_bytes();current=(S/'PARTIAL.md').read_bytes()
assert H(old)=='b51799d262ea7f633771128422708232c0522e7fddbaa5062a955911ed2e79f5'
assert H(current)=='0b116a4593d84d7e9d02f635a080eb0e2242aaba66acfc8efeae74462ad89898'
saved=J(S/'check_results.json');assert saved==J(S/'review/submitted_results.json')
runs=[]
def run(label,source,proof,resultname):
    work=O/label;work.mkdir();(work/source.name).write_bytes(source.read_bytes());(work/'PARTIAL.md').write_bytes(proof)
    cap=work/'actual_capture';cap.mkdir();(cap/'PRELAUNCH_SOURCE.py').write_bytes(source.read_bytes())
    argv=['/usr/bin/python3','-B',str(work/source.name)];start=stamp()
    with (cap/'stdout.bin').open('wb') as stdout,(cap/'stderr.bin').open('wb') as stderr:
        p=subprocess.Popen(argv,cwd=work,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr);pid=p.pid;code=p.wait(timeout=180)
    receipt=dict(argv=argv,cwd=str(work),actual_execution=True,completed=True,pid=pid,started_utc=start,finished_utc=stamp(),exit_code=code,stdin_supplied=False,source=row(cap/'PRELAUNCH_SOURCE.py'),stdout=row(cap/'stdout.bin'),stderr=row(cap/'stderr.bin'),optimizer_parent=0,PYTHONOPTIMIZE=os.environ.get('PYTHONOPTIMIZE'),output_file=row(work/resultname) if (work/resultname).exists() else None)
    (cap/'CAPTURE.json').write_text(json.dumps(receipt,indent=2)+'\n');runs.append(receipt)
    (O/'ACTUAL_RUNS.json').write_text(json.dumps(runs,indent=2)+'\n')
    assert code==0 and not (cap/'stderr.bin').read_bytes()
    assert (cap/'PRELAUNCH_SOURCE.py').read_bytes()==source.read_bytes()==(work/source.name).read_bytes()
    return J(work/resultname),(work/resultname).read_bytes()
fresh,freshb=run('current_author_private',S/'check_spectra.py',current,'check_results.json')
expected=dict(saved);expected['partial_sha256']=H(current)
assert fresh==expected and fresh['assertions']==18306 and fresh['all_passed'] is True
historical,historicalb=run('reviewed_author_private',S/'review/submitted_check_spectra.py',old,'check_results.json')
assert historical==saved and historicalb==(S/'check_results.json').read_bytes()
ind,indb=run('original_independent_private',S/'review/independent_checks.py',old,'independent_results.json')
savedind=J(S/'review/independent_results.json')
assert ind==savedind and indb==(S/'review/independent_results.json').read_bytes()
assert ind['passed']==len(ind['checks'])==1263 and ind['failed']==0 and all(type(v) is str and v=='PASS' for v in ind['checks'].values())
# Whole raw/SQLite importer comparison, independent of candidate source claims.
cache=R/'unsolved_math_prioritization/cache';rawb=(cache/'problems.json').read_bytes();priorb=(cache/'research_results.json').read_bytes();raw=json.loads(rawb);priors=json.loads(priorb)
byid={str(v['id']):v for v in raw};codes=collections.Counter(v['problem_number'] for v in raw)
assert len(raw)==len(byid)==15458 and len(priors)==6701
conn=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True);conn.execute('PRAGMA query_only=ON');assert conn.execute('PRAGMA query_only').fetchone()==(1,)
sql=conn.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall();assert len(sql)==15458
for key,payload,report in sql:
    expected=dict(byid[key]);code=expected['problem_number']
    if codes[code]>1 and code in priors:expected['_ambiguous_report']=True
    ep={} if expected.get('_ambiguous_report') else priors.get(code,{})
    assert json.loads(payload)==expected and json.loads(report)==ep,key
conn.close()
assert 'EP-653' not in priors and byid['2233']==J(S/'source_record.json')==J(A/'pinned_problem.json')
ledgerb=(S/'turns.jsonl').read_bytes();ledger=[json.loads(line) for line in ledgerb.splitlines()];assert len(ledger)==2
result=dict(status='PASS_ROOT_GENUINE_ORIGINAL_REPRODUCTION',utc=stamp(),actual_outer_runs=runs,entire_current_author_result=fresh,entire_reviewed_author_result=historical,entire_original_independent_result=ind,author_assertions=18306,independent_assertions=1263,all_original17_full_bytes_verified=True,current_author_saved_difference_only=dict(field='partial_sha256',reviewed=H(old),final=H(current)),reviewed_author_and_independent_saved_files_byte_exact=True,whole_raw_bytes=len(rawb)+len(priorb),whole_SQL_rows=15458,original_prior_raw_key_present=False,prior_SQL_empty_object_is_fallback=True,whole_original_ledger=ledger,original_ledger_sha256=H(ledgerb),original_substantive_attempts=2,new_substantive_attempts=0,audit_turns=0,full_problem_solved=False,finite_checks_are_not_asymptotic_proof=True,own_prior_inspector_failure=dict(actual_pid=88582,exit_code=1,source="reproduce_original_checks.py",failure="Own guessed submitted receipt filename did not exist; actual original name is review/submitted_results.json. No scientific helper ran; failed output folder and full capture/source retained."),current_model=None,current_reasoning_effort=None,current_deadline_utc=None)
(O/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
members=[row(p) for p in sorted(O.rglob('*')) if p.is_file()]
(O/'MANIFEST.json').write_text(json.dumps(dict(schema='pr42-root-original-actual-reproduction/v1',files_count=len(members),files=members,self_excluded=['MANIFEST.json']),indent=2)+'\n')
print(json.dumps(dict(status=result['status'],actual_pids=[v['pid'] for v in runs],author_assertions=18306,independent_assertions=1263,original17_verified=True,SQL_rows=15458,manifest_sha256=H((O/'MANIFEST.json').read_bytes()))))
