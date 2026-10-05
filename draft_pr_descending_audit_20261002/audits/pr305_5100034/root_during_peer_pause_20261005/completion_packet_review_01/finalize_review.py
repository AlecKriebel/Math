"""Final local freeze descriptor, not a self-issued native completion receipt."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
O = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
inputs = json.loads((O / 'INPUT_INVENTORY.json').read_bytes())['files']
for e in inputs:
    p = Path(e['path'])
    assert p.is_file() and not p.is_symlink()
    b = p.read_bytes()
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
    assert stat.S_IMODE(p.stat().st_mode) == e['mode']
native = json.loads((O / 'native_run_001/execution.json').read_bytes())
assert native['actual_PID'] == 76310 and native['exit_code'] == 0
for k in ['stdout', 'stderr']:
    b = (O / 'native_run_001' / (k + '.bin')).read_bytes()
    assert len(b) == native[k + '_bytes'] and sha(b) == native[k + '_sha256']
for e in native['programs']:
    p = Path(e['path']);b = p.read_bytes()
    assert len(b) == e['bytes'] and sha(b) == e['sha256'] and stat.S_IMODE(p.stat().st_mode) == e['mode']
verdictp = O / 'VERDICT.json'
verdict = json.loads(verdictp.read_bytes())
assert verdict['required_findings_count'] == 0 and verdict['literal_targets'] == 88
verdict['final_output_inventory_pending'] = False
verdict['final_output_inventory'] = 'OUTPUT_INVENTORY.json'
verdict['recorded_input_and_native_launch_modes_are_historical_before_review_freeze'] = True
verdict['output_bodies_frozen_after_report_verdict'] = True
verdictp.write_text(json.dumps(verdict, indent=2) + '\n')
payloads = []
for p in sorted(O.rglob('*')):
    assert not p.is_symlink()
    if p.is_file():
        p.chmod(0o444)
        b = p.read_bytes()
        payloads.append(dict(path=str(p.relative_to(O)), bytes=len(b), sha256=sha(b), mode=stat.S_IMODE(p.stat().st_mode)))
inventory = dict(UTC=datetime.now(timezone.utc).isoformat(), status='CLOSED_PASS_EXACT_PR305_COMPLETION_PACKET',
    exact_plan_sha256=verdict['exact_packet_plan']['sha256'], literal_targets=88, mandatory_findings=0,
    optional_findings=2, files=payloads, payload_files=len(payloads), payload_body_bytes=sum(x['bytes'] for x in payloads),
    excludes_only_self='OUTPUT_INVENTORY.json', current_file_modes='0444', current_directory_modes='0555',
    historical_input_and_native_launch_modes_preserved=True,
    known_local_input_CRITERIA_only_mode_changed_by_review_freeze=True,
    all_external_inputs_reauthenticated_at_final_close=True,
    no_production_operation_or_candidate_global_write=True,
    closure_descriptor_is_not_a_native_process_completion_receipt=True,
    reviewer_writes_stopped_after_this_inventory_and_mode_freeze=True)
p = O / 'OUTPUT_INVENTORY.json'
p.write_text(json.dumps(inventory, indent=2) + '\n');p.chmod(0o444)
for p in sorted((x for x in O.rglob('*') if x.is_dir()), key=lambda x: len(x.parts), reverse=True):
    p.chmod(0o555)
O.chmod(0o555)
summary = {}
for name in ['REPORT.md', 'VERDICT.json', 'CRITERIA.json', 'INPUT_INVENTORY.json', 'OUTPUT_INVENTORY.json']:
    p = O / name;b = p.read_bytes()
    summary[name] = dict(bytes=len(b), sha256=sha(b), mode=oct(stat.S_IMODE(p.stat().st_mode)))
print(json.dumps(dict(status=inventory['status'], payload_files=inventory['payload_files'], pins=summary), indent=2))
