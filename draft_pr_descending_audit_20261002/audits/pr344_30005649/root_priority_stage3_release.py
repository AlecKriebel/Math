"""One-time broader priority exposure after full independent first assessment."""
from pathlib import Path
import datetime, hashlib, json, stat
A = Path(__file__).resolve().parent
N = A / 'priority_audit'
pins = []
for name, expected in [('BASELINE_FREEZE.json', '6f8c0651093181220b6147bdc86caf818661e7bcb961be931247dfebd21cac0e'), ('FIRST_CANDIDATE_FREEZE.json', '224ee2c6f5bfb2e71c7abf308e5d97518d5eaa3f7fedf2d4c48f0916c390b1de')]:
    p = N / name
    data = p.read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected
    for item in json.loads(data)['frozen_files']:
        f = N / item['path']
        b = f.read_bytes()
        assert len(b) == item['bytes'] and hashlib.sha256(b).hexdigest() == item['sha256']
        pins.append({'path': str(f), 'bytes': len(b), 'sha256': item['sha256'], 'mode': stat.S_IMODE(f.stat().st_mode)})
    pins.append({'path': str(p), 'bytes': len(data), 'sha256': expected, 'mode': stat.S_IMODE(p.stat().st_mode)})
out = A / 'ROOT_PRIORITY_STAGE3_RELEASE.json'
assert not out.exists()
rec = {
    'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'BROADER_PRIORITY_EXPOSURE_AUTHORIZED_AFTER_COMPLETE_ROOT_FIRST_ASSESSMENT_READ',
    'verified_frozen_records': pins,
    'root_fully_read_stage2': 'All seven listed stage-2 records, including complete assessment, exposure, log, freeze, checker stdout/execution receipt, and graph encoding, displayed without truncation.',
    'scope_now_allowed': ['Entire frozen PR344 snapshot', 'Historical author review and priority material', 'Primary classification papers and their corrections and versions', 'Root and sibling mathematical assessments', 'Root primary priority findings and retrieved private primary sources', 'Read-only candidate repository and Zenodo chronology', 'Read-only relevant queue and imported records'],
    'scope_required': 'Perform full current priority audit under the frozen prospective tests. Distinguish classified module and known non-self-duality from exact qss flag plus admissible W-lift and answer to the posed question. Credit all inputs and retain every accessibility/version gap.',
    'mutation_limits': 'Own family folder only; no shared Git/index/main/queue/history writes, external-person communications, publication, or sealing. Preserve all prior frozen records; use a new stage-3 log.',
    'closure_authorized': False,
    'publication_authorized': False,
    'first_candidate_stage_percent': 100,
    'full_audit_percent': 20,
}
out.write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({'path': str(out), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'utc': rec['recorded_utc']}, indent=2))
