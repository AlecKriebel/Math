from pathlib import Path
import subprocess,json,datetime
d=Path("/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015")/'initial_review_20261016/root_reproduction_14_native_repair02/publication/native_repair_02'
with (d/'ROOT_R03.stdout').open('xb') as out,(d/'ROOT_R03.stderr').open('xb') as err:r=subprocess.run(["/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",'-B',str(d/'R03_final_retry.py')],stdout=out,stderr=err)
print('ACTUAL_ROOT_R03_CHILD_EXIT',r.returncode,flush=True)
(d/'ROOT_R03_EXIT.json').write_text(json.dumps(dict(actual_child_exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))+'\n')
assert r.returncode==0
rows=json.loads((d/'R03_final_retry/JOINT_COMPACT_RESULTS.json').read_bytes());old=json.loads((d/'JOINT_COMPACT_RESULTS.json').read_bytes())
assert len(rows)==1 and len(old)==36 and all(x['PASS'] for x in rows+old)
(d/'ROOT_REPLAY_RECEIPT.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),M03_actual36_complete_controls_PASS=True,M03_wrapper_exit_unavailable_recorded=True,M03_child_stderr_bytes=0,R03_separate_one_group_PASS=True,R03_actual_child_exit=0,R03_actual_stderr_bytes=(d/'ROOT_R03.stderr').stat().st_size,actual_completed_controls_total=37,no_single_successful37_wrapper_claim=True,providers_only_controlled=True,no_release_authority=True,case_completion_percent=65),indent=2)+'\n')
print('ROOT_ALL37_RECORDED_PASS',flush=True)
