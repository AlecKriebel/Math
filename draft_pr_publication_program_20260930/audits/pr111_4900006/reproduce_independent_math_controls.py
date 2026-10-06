"""Reproduce exact family controls in root-owned directories, preserving agents."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

ROOT = Path(__file__).resolve().parent
env = {'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC',
       '__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
families = [
    ('flow','global_flow_attractor_adversary_20261006','verify_independently.py'),
    ('dimension','lyapunov_dimension_adversary_20261006','independent_checks.py'),
    ('scope','primary_source_scope_adversary_20261006','independent_scope_checks.py'),
]
records = []
for label, folder, name in families:
    source = ROOT / folder / name
    data = source.read_bytes()
    dest = ROOT / ('root_math_reproduction_20261006_' + label)
    dest.mkdir(exist_ok=False)
    replay = dest / name
    replay.write_bytes(data)
    if label == 'scope':
        (dest / 'private_primary_sources').symlink_to(ROOT / folder / 'private_primary_sources', target_is_directory=True)
    argv = [sys.executable, '-E','-S','-B','-P',str(replay)]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=45)
    (dest / 'stdout.txt').write_bytes(run.stdout)
    (dest / 'stderr.txt').write_bytes(run.stderr)
    if run.returncode != 0:
        raise RuntimeError(label+' replay failed: '+run.stderr.decode(errors='replace'))
    result = json.loads(run.stdout)
    if label == 'flow':
        (dest / 'EXACT_CONTROLS_NORMAL.json').write_bytes(run.stdout)
    receipt = {
        'family':label, 'started_at_utc':start,
        'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'original_program':str(source.relative_to(ROOT)),
        'program_bytes':len(data), 'program_sha256':hashlib.sha256(data).hexdigest(),
        'copied_program_byte_identical':replay.read_bytes()==data,
        'offered_source_unchanged':source.read_bytes()==data,
        'argv':argv, 'returncode':run.returncode,
        'stderr_bytes':len(run.stderr),'stdout_sha256':hashlib.sha256(run.stdout).hexdigest(),
        'actual_control_PID':result.get('actual_PID',result.get('actual_pid')),
        'checks':result.get('checks',result.get('check_count')),
        'all_checks_passed':result.get('all_checks_passed',result.get('all_pass',result.get('passed'))),
    }
    if not all(receipt[k] for k in ['copied_program_byte_identical','offered_source_unchanged','all_checks_passed']):
        raise RuntimeError('Root replay authentication failed')
    (dest / 'ROOT_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    records.append(receipt)
out = {'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'actual_root_PID':os.getpid(),'families':records,
       'original_candidate_or_agent_output_mutations':0,
       'new_central_proof_search_turns':0,
       'priority_cleared':False,'scope':'Reproduction of completed candidate verification; analytic arguments independently read by root.'}
(ROOT / 'ROOT_INDEPENDENT_CONTROLS_REPRODUCTION_20261006.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
