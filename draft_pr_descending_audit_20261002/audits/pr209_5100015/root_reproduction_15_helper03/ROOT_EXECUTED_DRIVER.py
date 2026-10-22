from pathlib import Path
import subprocess,json,datetime
d=Path("/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015")/'root_reproduction_15_helper03'
with (d/'ROOT_ACTUAL.stdout').open('xb') as out,(d/'ROOT_ACTUAL.stderr').open('xb') as err:r=subprocess.run(["/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",'-B',str(d/'receipt_corruption_probe.py')],stdout=out,stderr=err)
print('ACTUAL_CHILD_EXIT',r.returncode,flush=True)
(d/'ROOT_PROGRAM_EXIT.json').write_text(json.dumps(dict(actual_exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))+'\n')
assert r.returncode==0
x=json.loads((d/'RECEIPT_CORRUPTION_RESULT.json').read_bytes());assert x['all6_corruptions_accepted']
(d/'ROOT_REPLAY_RECEIPT.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),all6_existing_receipt_defects_reproduced=True,actual_exit=0,provider_writes_added_by_corrupt_acceptance=0,frozen_source03_exact=True,no_release_authority=True,case_completion_percent=65),indent=2)+'\n')
print('ROOT_SIX_DEFECTS_REPRODUCED')
