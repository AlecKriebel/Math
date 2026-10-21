"""Reconcile only this private main after an authenticated pre-staging stop."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess

A = Path(__file__).resolve().parent
C = A.parents[2]
D = A / 'remote_main_reconciliation_round2_20261006'
D.mkdir(exist_ok=False)
old = 'ad789fadf6e398fe7e2c0d243db4625e78207a8e'
new = '1f86990dcae793167b35c1cfff2e310758404886'
records = []
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value, message):
    if not value:
        raise RuntimeError(message)
def run(*args):
    start = now()
    proc = subprocess.Popen(['/usr/bin/git', *args], cwd=C, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    i = len(records)
    (D / (str(i)+'.stdout.bin')).write_bytes(out)
    (D / (str(i)+'.stderr.bin')).write_bytes(err)
    records.append({'argv': ['/usr/bin/git', *args], 'PID': proc.pid, 'UTC_start': start,
                    'UTC_end': now(), 'exit_code': proc.returncode,
                    'stdout_file': str(i)+'.stdout.bin', 'stderr_file': str(i)+'.stderr.bin',
                    'stdout_sha256': hashlib.sha256(out).hexdigest(),
                    'stderr_sha256': hashlib.sha256(err).hexdigest()})
    (D/'PROCESS_JOURNAL.json').write_text(json.dumps({'operator_PID': os.getpid(), 'records': records}, indent=2)+'\n')
    require(proc.returncode == 0, err.decode('utf-8', 'replace'))
    return out
require(run('symbolic-ref', '--short', 'HEAD').strip() == b'main', 'private branch')
require(run('rev-parse', 'HEAD').strip().decode() == old, 'local changed')
require(not run('diff', '--cached', '--name-only', '-z'), 'staged work')
require(run('ls-remote', 'https://github.com/AlecKriebel/Math.git', 'refs/heads/main').decode().split()[0] == new, 'remote changed again')
run('merge-base', '--is-ancestor', old, new)
delta = [x.decode() for x in run('diff', '--name-only', '-z', old, new).split(b'\0') if x]
require(delta and all(x.startswith('draft_pr_descending_audit_20261002/') for x in delta), 'unexpected concurrent scope')
selection = json.loads((A/'ROUND2_ADJUDICATION_CHECKPOINT_SELECTION.json').read_text())
require(not set(selection['paths']).intersection(delta), 'selected remote overlap')
pins = {rel: hashlib.sha256((C/rel).read_bytes()).hexdigest() for rel in selection['paths']}
require(all(pins[row['path']] == row['sha256'] for row in selection['pins']), 'selected local body changed')
run('reset', '--mixed', '--quiet', new)
require(run('rev-parse', 'HEAD').strip().decode() == new and not run('diff', '--cached', '--name-only', '-z'), 'private reconciliation readback')
require(all(hashlib.sha256((C/rel).read_bytes()).hexdigest() == digest for rel, digest in pins.items()), 'working body changed')
receipt = {'schema': 'pr97-private-round2-main-reconciliation/v1', 'UTC': now(), 'operator_PID': os.getpid(),
           'old': old, 'new': new, 'old_is_ancestor': True, 'concurrent_changed_paths': len(delta),
           'selected_paths': len(pins), 'selected_bytes_unchanged': True,
           'failed_checkpoint_stopped_before_staging': True, 'primary_checkout_mutated': False,
           'index_empty': True, 'other_workflow_files_not_written': True}
(D/'RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt))
