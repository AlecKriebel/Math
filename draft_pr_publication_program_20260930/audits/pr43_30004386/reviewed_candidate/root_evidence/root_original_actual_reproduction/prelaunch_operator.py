"""ROOT unchanged helpers in private copies; full original/raw/SQL comparisons."""
import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr43_30004386';S=A/'source_snapshot';O=A/'root_original_actual_reproduction'
def H(b):return hashlib.sha256(b).hexdigest()
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def J(p):return json.loads(p.read_bytes())
def row(p):
    b=p.read_bytes();return dict(path=p.relative_to(O).as_posix(),bytes=len(b),sha256=H(b))
assert sys.flags.optimize==0 and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
O.mkdir(exist_ok=False);(O/'prelaunch_operator.py').write_bytes(Path(__file__).read_bytes())
snapshot=J(A/'snapshot_manifest.json');assert len(snapshot['files'])==16
for z in snapshot['files']:
    b=(S/z['path']).read_bytes();assert len(b)==z['size'] and H(b)==z['sha256']
assert (S/'check_normalization.py').read_bytes()==(S/'review/author_replay/check_normalization.py').read_bytes()
saved=J(S/'check_results.json');assert (S/'check_results.json').read_bytes()==(S/'review/author_replay/check_results.json').read_bytes()
argv=['git','show','2bdeb95df6b1f4c2289455b176f8d8617a36bb92:unsolved_math_prioritization/attempts/30004386/SOURCE_STATUS.md']
start=stamp();p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);old,err=p.communicate()
(O/'historical_source_status.md').write_bytes(old);(O/'historical_source_git.stderr').write_bytes(err)
gitcap=dict(argv=argv,cwd=str(R),pid=p.pid,actual_execution=True,completed=True,exit_code=p.returncode,started_utc=start,finished_utc=stamp(),stdin_supplied=False,stdout=row(O/'historical_source_status.md'),stderr=row(O/'historical_source_git.stderr'))
(O/'HISTORICAL_SOURCE_GIT_CAPTURE.json').write_text(json.dumps(gitcap,indent=2)+'\n');assert p.returncode==0 and not err
current=(S/'SOURCE_STATUS.md').read_bytes()
assert H(old)==saved['source_status_sha256']=='98918841ab30dd1e41d51dbc7ec8515a66f1f1c82f01ff08ccc5462b758a2727'
assert H(current)=='90402aea80b79b7713d740863b6058b43c64050c3499701b2bf8490c90b210e3'
before=b'Separate adversarial review of this identification is pending.';after=b'Separate adversarial AI review of this identification passed; see [the report](review/REVIEW.md).'
assert old.count(before)==1 and old.replace(before,after,1)==current
runs=[]
def run(label,source,science,stdout_is_result=False):
    work=O/label;work.mkdir();(work/source.name).write_bytes(source.read_bytes())
    if science is not None:(work/'SOURCE_STATUS.md').write_bytes(science)
    cap=work/'actual_capture';cap.mkdir();(cap/'PRELAUNCH_SOURCE.py').write_bytes(source.read_bytes())
    argv=['/usr/bin/python3','-B',str(work/source.name)];started=stamp()
    with (cap/'stdout.bin').open('xb') as out,(cap/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(argv,cwd=work,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
        try:code=child.wait(timeout=180)
        except BaseException:child.kill();child.wait();raise
    output=cap/'stdout.bin' if stdout_is_result else work/'check_results.json'
    rec=dict(argv=argv,cwd=str(work),actual_execution=True,completed=True,pid=child.pid,started_utc=started,finished_utc=stamp(),exit_code=code,stdin_supplied=False,source=row(cap/'PRELAUNCH_SOURCE.py'),stdout=row(cap/'stdout.bin'),stderr=row(cap/'stderr.bin'),output_file=row(output) if output.exists() else None,output_is_helper_stdout=stdout_is_result,optimizer_parent=0,PYTHONOPTIMIZE=os.environ.get('PYTHONOPTIMIZE'))
    (cap/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n');runs.append(rec);(O/'ACTUAL_RUNS.json').write_text(json.dumps(runs,indent=2)+'\n')
    assert code==0 and not (cap/'stderr.bin').read_bytes() and source.read_bytes()==(work/source.name).read_bytes()==(cap/'PRELAUNCH_SOURCE.py').read_bytes()
    result=J(output);assert result==J(cap/'stdout.bin')
    return result,output.read_bytes()
fresh,freshb=run('current_author_private',S/'check_normalization.py',current)
assert fresh==dict(saved,source_status_sha256=H(current)) and fresh['assertions']==527 and fresh['all_passed'] is True
historical,historicalb=run('historical_author_private',S/'review/author_replay/check_normalization.py',old)
assert historical==saved and historicalb==(S/'check_results.json').read_bytes()
ind,indb=run('original_independent_private',S/'review/independent_checks.py',None,True)
assert ind==J(S/'review/independent_results.json') and indb==(S/'review/independent_results.json').read_bytes()
assert type(ind['assertions']) is int and ind['assertions']==sum(ind['checks'].values())==664 and ind['status']=='PASS'
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
conn.close();code='OWR-17469-011';assert byid['30004386']==J(S/'source_record.json')
raw_present=code in priors;prior=priors.get(code,{})
(A/'pinned_problem.json').write_bytes((S/'source_record.json').read_bytes());(A/'pinned_prior_report.json').write_text(json.dumps(prior,indent=2)+'\n')
ledger=(S/'turns.jsonl').read_bytes();assert ledger==b''
result=dict(status='PASS_ROOT_GENUINE_ORIGINAL_REPRODUCTION',utc=stamp(),all_original16_full_bytes_verified=True,actual_outer_runs=runs,entire_current_author_result=fresh,entire_historical_author_result=historical,entire_original_independent_result=ind,author_assertions=527,independent_assertions=664,historical_author_and_independent_saved_files_byte_exact=True,current_author_only_saved_difference=dict(field='source_status_sha256',old=H(old),current=H(current)),historical_source_entire_difference='Exactly one review-status sentence; actual original Git source retained.',historical_source_actual_capture=gitcap,whole_raw_bytes=len(rawb)+len(priorb),whole_SQL_rows=len(sql),prior_raw_key_present=raw_present,entire_prior_report=prior,prior_SQL_empty_object_is_fallback=not raw_present,source_prior_null_retrieval_certified=raw_present and prior is None,whole_original_ledger=[],original_ledger_sha256=H(ledger),original_substantive_attempts=0,new_substantive_attempts=0,audit_turns=0,finite_checks_are_not_LDP_proof=True,current_model=None,current_reasoning_effort=None,current_deadline_utc=None,current_mathematical_and_whole_review='PENDING')
(O/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
members=[row(p) for p in sorted(O.rglob('*')) if p.is_file()]
(O/'MANIFEST.json').write_text(json.dumps(dict(schema='pr43-root-original-actual-reproduction/v1',files_count=len(members),files=members,self_excluded=['MANIFEST.json']),indent=2)+'\n')
print(json.dumps(dict(status=result['status'],actual_pids=[x['pid'] for x in runs],author_assertions=527,independent_assertions=664,prior_raw_key_present=raw_present,SQL_rows=len(sql),manifest_sha256=H((O/'MANIFEST.json').read_bytes()))))
