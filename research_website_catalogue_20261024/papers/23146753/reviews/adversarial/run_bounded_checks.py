"""Run already-inspected diagnostics and source replay, bounded as process groups."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, signal, subprocess, sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / 'sources' / 'published-source'
stamp = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
jobs = [
    ('independent', [sys.executable, str(HERE / 'independent_controls.py'), str(HERE / 'CONTROL_RESULTS.json')], HERE),
    ('assertion_guard', [sys.executable, '-O', str(HERE / 'independent_controls.py'), str(HERE / 'SHOULD_NOT_EXIST.json')], HERE),
    ('published_replay', [sys.executable, str(SOURCE / 'REPRODUCE.py'), '--out-dir', str(HERE / 'cache' / 'source-replay')], HERE),
]
receipts = []
for label, command, cwd in jobs:
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    started = stamp()
    proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = proc.communicate(timeout=55)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate()
        raise RuntimeError(f'{label} exceeded bounded timeout')
    (HERE / (label + '.stdout.txt')).write_bytes(stdout)
    (HERE / (label + '.stderr.txt')).write_bytes(stderr)
    good = (proc.returncode != 0 and not (HERE / 'SHOULD_NOT_EXIST.json').exists()
            if label == 'assertion_guard' else proc.returncode == 0 and not stderr)
    receipt = dict(label=label, command=command, cwd=str(cwd), started_utc=started,
                   ended_utc=stamp(), exit_code=proc.returncode, expected_outcome_observed=good,
                   stdout_sha256=hashlib.sha256(stdout).hexdigest(), stderr_sha256=hashlib.sha256(stderr).hexdigest(),
                   timeout_seconds=55, process_group_cleanup='SIGKILL whole group on timeout',
                   programs_read_before_execution=True)
    receipts.append(receipt)
    if not good:
        raise RuntimeError(receipt)
(HERE / 'EXECUTION_LEDGER.json').write_text(json.dumps(dict(jobs=receipts,
    original_sources_modified=False, external_network_used_by_programs=False,
    original_source_programs_executed=['REPRODUCE.py', 'verify_boundary.py', 'verify_priority_examples.py'],
    finite_computations_do_not_prove_universal_theorem=True), indent=2) + '\n')
print(json.dumps(receipts, indent=2))
