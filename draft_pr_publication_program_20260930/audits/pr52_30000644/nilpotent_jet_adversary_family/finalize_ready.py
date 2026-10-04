"""Preparer's bounded SOURCE-ready finalizer; never executes ROOT helpers."""
import datetime
import json
import os
from pathlib import Path
from closure_common import F, MF, digest, identity, inspect, read_json

assert not MF.exists() and not (F / 'INDEX.json').exists() and not (F / 'READY.json').exists()
successful = F / 'captures' / 'revised_exact_quotient_checks'
interrupted = F / 'captures' / 'initial_exact_quotient_checks'
capture = read_json(successful / 'CAPTURE.json')
result = read_json(successful / 'stdout.bin')
assert capture['exit_code'] == 0 and capture['child_pid'] == 91494
assert result['schema'] == 'pr52-independent-nilpotent-jet-checks/v2'
assert result['status'] == 'PASS' and type(result['assertions']) is int and result['assertions'] == 9612
assert type(result['case_count']) is int and result['case_count'] == len(result['cases']) == 61
assert read_json(interrupted / 'CAPTURE.json')['exit_code'] == -2
assert read_json(interrupted / 'CAPTURE.json')['child_pid'] == 83751
assert (F / 'independent_jet_checks.py').read_bytes() == (interrupted / 'source_prelaunch.py').read_bytes()
assert (F / 'independent_jet_checks_v2.py').read_bytes() == (successful / 'source_prelaunch.py').read_bytes()
verdict = read_json(F / 'verdict.json')
assert verdict['mandatory_mathematical_corrections'] == []
assert verdict['universal_proof_gap_within_literal_claim'] is None
original = F.parent / 'original_preparation_family' / 'original'
original_files = sorted(p for p in original.rglob('*') if p.is_file())
assert len(original_files) == 19
external = original_files + [
    F.parent / 'original_preparation_family' / 'primary_selected' / 'owr2007-decisive-page.png',
    F.parent / 'original_preparation_family' / 'primary_selected' / 'acta-open-problems2007-decisive-page.png',
    Path('/Users/alec/Documents/Math/AGENTS.md'),
]
assert all(not p.is_symlink() for p in F.rglob('*'))
payload = sorted(p for p in F.rglob('*') if p.is_file())
for p in payload: p.chmod(0o444)
rows = []
for p in payload:
    row = identity(p)
    row['relative_path'] = str(p.relative_to(F))
    row.pop('path')
    rows.append(row)
idx = {'schema': 'pr52-nilpotent-jet-index/v1',
       'original_head': 'd40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a',
       'payload_bindings': rows, 'fixed_external_rows': [identity(p) for p in external],
       'fixed_external_byte_binding_is_not_personal_content_read_attestation': True,
       'actual_capture_paths': [str(successful)],
       'retained_interrupted_capture_paths': [str(interrupted)],
       'directories': sorted(str(p.relative_to(F)) for p in F.rglob('*') if p.is_dir())}
(F / 'INDEX.json').write_text(json.dumps(idx, indent=2, sort_keys=True) + '\n')
(F / 'INDEX.json').chmod(0o444)
ready = {'schema': 'pr52-nilpotent-jet-ready/v1',
         'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'preparer_finalizer_pid': os.getpid(),
         'preparer_finalizer_source_sha256': digest(Path(__file__).read_bytes()),
         'finalizer_completion_and_exit_not_self_attested': True,
         'index_sha256': digest((F / 'INDEX.json').read_bytes()),
         'payload_files': len(payload), 'prepared_files_including_index_and_ready': len(payload) + 2,
         'fixed_external_rows': len(external), 'root_closure_required_after_preparer_exit': True,
         'closer_reader_executed_by_preparer': False, 'self_manifest_present_at_handoff': False,
         'root_personal_read_attestation': False, 'native_acceptance_authority': False,
         'remote_action_authority': False, 'mathematical_audit_completion_percent': 100,
         'new_discovery_credit_percent': 0}
(F / 'READY.json').write_text(json.dumps(ready, indent=2, sort_keys=True) + '\n')
(F / 'READY.json').chmod(0o444)
r = inspect(ready['index_sha256'], digest((F / 'READY.json').read_bytes()), False)
print(json.dumps({'status': 'INDEPENDENT_REVIEW_SOURCE_READY_ROOT_CLOSURE_PENDING',
                  'index_sha256': ready['index_sha256'], 'ready_sha256': digest((F / 'READY.json').read_bytes()),
                  'prepared_files': len(r['file_bindings']), 'fixed_external_rows': len(external),
                  'root_closer_or_reader_executed': False}, sort_keys=True))
