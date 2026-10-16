"""Record one-time candidate exposure after root's complete baseline read."""
from pathlib import Path
import datetime, hashlib, json, stat

A = Path(__file__).resolve().parent
N = A / 'priority_audit'
freeze = json.loads((N / 'BASELINE_FREEZE.json').read_text())
expected = {x['path']: x for x in freeze['frozen_files']}
expected['BASELINE_FREEZE.json'] = {'sha256': '6f8c0651093181220b6147bdc86caf818661e7bcb961be931247dfebd21cac0e'}
pins = []
for name, item in expected.items():
    p = N / name
    data = p.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    assert sha == item['sha256']
    if 'bytes' in item:
        assert len(data) == item['bytes']
    pins.append({'path': str(p), 'sha256': sha, 'bytes': len(data), 'mode': stat.S_IMODE(p.stat().st_mode)})
sources = json.loads((N / 'SOURCE_PINS.json').read_text())
for item in sources['local_primary_sources']:
    data = Path(item['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == item['sha256'] and len(data) == item['bytes']
out = A / 'ROOT_PRIORITY_CANDIDATE_RELEASE.json'
assert not out.exists()
rec = {
    'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'FIRST_CANDIDATE_EXPOSURE_AUTHORIZED_AFTER_FULL_ROOT_BASELINE_READ',
    'root_fully_read_files': pins,
    'root_full_read_note': 'First combined tool output was truncated; SOURCE_ONLY_BASELINE.md was reread alone in full. Other five records were displayed completely. Nine local primary source pins independently checked.',
    'candidate_files_allowed': [str(A / 'snapshot/problems/30005649_qss_self_duality' / f) for f in ['SOURCE_GATE.md', 'README.md', 'TURN_1.md', 'turn1/check_module.py']],
    'stage_next': 'Freeze independent first-candidate priority assessment before historic author review, root assessment, sibling mathematics, or root priority findings. Send paths and hashes and wait for explicit further exposure release.',
    'previous_failed_attempt': 'Inline recording attempt failed with SyntaxError before execution or any file write; genuine tool output retained in conversation. This is the corrected standalone program.',
    'no_novelty_or_priority_verdict': True,
    'source_stage_percent': 100,
    'full_audit_percent': 10,
}
out.write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({'path': str(out), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'utc': rec['recorded_utc']}, indent=2))
