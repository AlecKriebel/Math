from pathlib import Path
import shutil
import subprocess
import json
import hashlib
import datetime

A = Path(__file__).resolve().parent
R = A.parent
PRIVATE = A / 'private_runs'
P = PRIVATE / 'portable_candidate'
shutil.copytree(R / 'snapshot', P, dirs_exist_ok=True)
target = P / 'problems' / '30002762_conjugation_norms'
outputs = []
for name, script in [('author_full_replay', 'REPLAY_ALL.py'),
                     ('old_review_exact_replay', 'review/independent_check.py'),
                     ('publication_wrapper', 'verify_publication.py')]:
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run = subprocess.run(['python3', str(target / script)], cwd=target,
                         capture_output=True, text=True)
    (PRIVATE / f'{name}.stdout').write_text(run.stdout)
    (PRIVATE / f'{name}.stderr').write_text(run.stderr)
    outputs.append({'name': name, 'command': ['python3', str(target / script)],
                    'started_utc': start,
                    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'exit_code': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr,
                    'stdout_sha256': hashlib.sha256(run.stdout.encode()).hexdigest(),
                    'stderr_sha256': hashlib.sha256(run.stderr.encode()).hexdigest(),
                    'head': '9946a67cf8a1f7e3130d2a12de902db05875283a'})
    print(name, run.returncode, run.stdout, run.stderr, flush=True)
    if run.returncode:
        break
(A / 'PORTABLE_REPLAY_FULL_RESULTS.json').write_text(json.dumps(outputs, indent=2) + '\n')
if any(x['exit_code'] for x in outputs):
    raise SystemExit(1)
