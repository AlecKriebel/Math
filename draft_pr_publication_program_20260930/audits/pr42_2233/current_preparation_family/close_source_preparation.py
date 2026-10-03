"""Authoring-only exact closure; never imports/executes/compiles proposed builder."""
import datetime as dt
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
A = P.parent
def H(raw):
    return hashlib.sha256(raw).hexdigest()
def row(path):
    assert path.is_file() and not path.is_symlink() and all(not p.is_symlink() for p in path.parents)
    raw = path.read_bytes()
    return dict(path=path.relative_to(P).as_posix(), bytes=len(raw), sha256=H(raw))
assert not (P / 'PREPARATION_MANIFEST.json').exists()
assert not (P / 'SOURCE_STATUS.json').exists()
assert not (P / 'SOURCE_PREPARATION_RESEARCH_LOG.md').exists()
assert not (A / 'reviewed_candidate').exists()
now = dt.datetime.now(dt.timezone.utc).isoformat()
source = row(P / 'prepare_current_packet.py')
pins = json.loads((P / 'INPUT_PINS.json').read_bytes())
capture = json.loads((P / 'AUTHORING_ACTUAL_CAPTURE/CAPTURE.json').read_bytes())
assert capture['actual_execution'] is True and capture['completed'] is True and capture['pid'] == 98633 and capture['exit_code'] == 0
assert capture['candidate_builder_imported_executed_compiled'] is False
status = dict(schema='PR42_CLOSED_SOURCE_ONLY_PREPARATION_STATUS_v1', utc=now,
              source_preparer_complete_builder_and_contract_read=True,
              static_review_completed=True, builder=source,
              builder_imported_executed_compiled=False, candidate_created=False,
              ROOT_reading_or_approval_attested_by_preparer=False,
              future_whole_current_verdict=None, current_model=None,
              current_reasoning_effort=None, current_deadline_utc=None,
              original_substantive_attempts=2, new_substantive_attempts=0, audit_turns=0,
              source_preparation_completion_percent=100, current_publication_workflow_percent=65,
              full_problem_discovery_percent=0, native_canonical_git_index_remote_writes=False,
              external_human_contact=False, input_pins_sha256=H((P / 'INPUT_PINS.json').read_bytes()))
(P / 'SOURCE_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
log = ('# Source-preparation research log\n\n'
       + '2026-10-02T22:52:35.681914+00:00 — genuine authoring-only input inspection PID98633, exit0. Original17 verified; retained ROOT104 files pinned; literal54 copied +26 individually foreign/derivative, exact41 copied +5 foreign, plus each self manifest. SOURCE_AUDIT absent raw key/SQL fallback precision correction established. Source preparation70%; publication workflow60%; full discovery0%. Original2/5,new0/audit0. No candidate/helper execution.\n\n'
       + now + ' — complete proposed source and contracts statically reviewed; strict typed true-flag comparison and complete failed-attempt tree retention added. Source preparation100%; publication workflow65%; full discovery0%. Four external genuine ROOT reading/fresh13 prerequisites remain required; NEW whole-current gate PENDING. No future freeze/PASS/runtime or ROOT fullread attestation manufactured. Current target UNSOLVED. All authoring source and actual capture retained; tool-only size failure separately disclosed.\n')
(P / 'SOURCE_PREPARATION_RESEARCH_LOG.md').write_text(log)
files, directories = [], set()
for path in sorted(P.rglob('*')):
    assert not path.is_symlink()
    if path.is_file():
        files.append(row(path))
    else:
        assert path.is_dir()
        directories.add(path.relative_to(P).as_posix())
expected_dirs = {parent.as_posix() for item in files for parent in Path(item['path']).parents if parent.as_posix() != '.'}
assert directories == expected_dirs
manifest = dict(schema='PR42_SOURCE_ONLY_PREPARATION_MANIFEST_v1', status='CLOSED_SOURCE_ONLY_CURRENT_PREPARATION',
                utc=now, self_excluded=['PREPARATION_MANIFEST.json'], files_count=len(files), files=files,
                builder_imported_executed_compiled=False, future_current_freeze_or_whole_PASS_claimed=False,
                original_substantive_attempts=2, new_substantive_attempts=0, audit_turns=0)
(P / 'PREPARATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
assert {p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()} == {item['path'] for item in files} | {'PREPARATION_MANIFEST.json'}
for item in files:
    assert row(P / item['path']) == item
print(json.dumps(dict(status=manifest['status'], source_sha256=source['sha256'],
                     manifest_sha256=H((P / 'PREPARATION_MANIFEST.json').read_bytes()),
                     qualification_sha256=pins['qualification_sha256'], files=len(files),
                     candidate_created=False, builder_imported_executed_compiled=False), indent=2))
