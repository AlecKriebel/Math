from pathlib import Path
import json,hashlib,subprocess,datetime
a=Path(__file__).resolve().parent
repo=a.parents[3]
p=a.parent/'publication_package_v3'
actual=a.parent.parent/'pr45_9900007/root_pr50_v3_checker_actual_capture'
ver=a.parent.parent/'pr45_9900007/root_pr50_v3_interpreter_version_actual_capture'
old=a.parent/'preprint_v1/verification_run'
record=json.loads((a/'private/extracted/VERIFICATION_RECORD.json').read_text())
newcap=json.loads((actual/'CAPTURE.json').read_text())
oldcap=json.loads((old/'CAPTURE.json').read_text())
print('new actual author capture',json.dumps(newcap,indent=2))
print('new actual prelaunch operator', (actual/'prelaunch_operator.py').read_text())
print('old actual author capture',json.dumps(oldcap,indent=2))
print('new interpreter',(ver/'stdout.bin').read_text())
assert newcap['pid']==76825 and newcap['exit_code']==0 and newcap['completed']
assert (actual/'stdout.bin').read_bytes()==(p/'expected_results.json').read_bytes()
assert (actual/'stderr.bin').read_bytes()==b''
assert record['actual_completed_run']['child_pid']==newcap['pid']
assert record['actual_completed_run']['operator_interval_utc']['started']==newcap['started_utc']
assert record['actual_completed_run']['operator_interval_utc']['finished']==newcap['finished_utc']
assert record['actual_completed_run']['interpreter']==(ver/'stdout.bin').read_text().strip()
hist=record['historical_pre_strengthening_verification']
assert hist['actual_completed_run']['child_pid']==oldcap['child_pid']==95899
assert hist['actual_completed_run']['operator_pid']==oldcap['operator_pid']==95888
assert hashlib.sha256((old/'stdout.bin').read_bytes()).hexdigest()==hist['expected_result_binding']['sha256']
assert hashlib.sha256((a.parent/'publication_package_v2/VERIFICATION_RECORD.json').read_bytes()).hexdigest()==hist['record_binding']['sha256']
assert hashlib.sha256((a.parent/'publication_package_v2/verify_even_calculus.py').read_bytes()).hexdigest()==hist['checker_binding']['sha256']
assert json.loads((old/'stdout.bin').read_text())['checks']==7106
def run(name,argv):
    b=a/'private/commands'/name;start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with b.with_suffix('.stdout').open('wb') as out,b.with_suffix('.stderr').open('wb') as err:
        child=subprocess.Popen(argv,cwd=repo,stdin=subprocess.DEVNULL,stdout=out,stderr=err);rc=child.wait()
    b.with_suffix('.json').write_text(json.dumps({'argv':argv,'pid':child.pid,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cwd':str(repo),'exit_code':rc},indent=2)+'\n');b.with_suffix('.stdin').write_bytes(b'')
    assert rc==0
    return b.with_suffix('.stdout').read_text()
branch=run('read_branch',['git','branch','--show-current']).strip()
assert branch=='main'
local=(repo/'unsolved_math_prioritization/QUEUE.md').read_text()
submitted=run('read_submitted_queue',['git','show','7260315f8b8b193020c09d4ef6df9d943a3a13ff:unsolved_math_prioritization/QUEUE.md'])
state={'branch':branch,'submitted_head':'7260315f8b8b193020c09d4ef6df9d943a3a13ff','local_rows':[line for line in local.splitlines() if '10600042' in line],'submitted_rows':[line for line in submitted.splitlines() if '10600042' in line]}
print('state',json.dumps(state,indent=2))
pins=json.loads((a/'INPUT_PINS.json').read_text())
for n in ['even_strand_markov.tex','even_strand_markov.pdf','even-strand-markov-verification-v3.zip','zenodo-deposit.json']:
    b=(p/n).read_bytes()
    assert len(b)==pins[n]['size'] and hashlib.sha256(b).hexdigest()==pins[n]['sha256']
primaries=a.parent/'current_promotion_adversary_20261004/private'
primarypins={n:hashlib.sha256((primaries/n).read_bytes()).hexdigest() for n in ['kamada.pdf','kl.pdf','gks.pdf','survey.pdf','survey_publisher_correct.pdf','nencka_scan_153.webp','nencka_scan_154.webp','nencka_scan_004.webp']}
(a/'PRIMARY_PINS.json').write_text(json.dumps(primarypins,indent=2)+'\n')
print('PASS independent provenance/state/pin audit')
