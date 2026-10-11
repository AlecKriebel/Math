"""Close the adjacent source-only folder; never import/run/compile the builder."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import stat

P = Path(__file__).resolve().parent
A = P.parent
def H(raw):
    return hashlib.sha256(raw).hexdigest()
def J(path):
    return json.loads(path.read_bytes())
def row(path):
    assert path.is_file() and not path.is_symlink() and all(not p.is_symlink() for p in path.parents)
    raw = path.read_bytes()
    assert len(raw) < 100 * 1024 * 1024
    return dict(path=path.relative_to(P).as_posix(), bytes=len(raw), sha256=H(raw))
assert not (P / 'PREPARATION_MANIFEST.json').exists()
assert not (P / 'SOURCE_STATUS.json').exists()
assert not (A / 'reviewed_candidate').exists()
repair = J(P / 'REPAIR_INPUT_PINS.json')
for info in repair['prior_closed_evidence']:
    root = A / info['directory']
    manifest = root / info['manifest']['path']
    assert H(manifest.read_bytes()) == info['manifest']['sha256']
    value = J(manifest)
    files, directories = set(), set()
    for path in root.rglob('*'):
        assert not path.is_symlink()
        if path.is_file():
            files.add(path.relative_to(root).as_posix())
        else:
            assert path.is_dir()
            directories.add(path.relative_to(root).as_posix())
    assert files == {item['path'] for item in value['files']} | {manifest.name}
    assert directories == set(info['directories'])
    for item in value['files']:
        path = root / item['path']
        raw = path.read_bytes()
        assert len(raw) == item['bytes'] and H(raw) == item['sha256']
        if 'permission_mode' in item:
            assert oct(stat.S_IMODE(path.stat().st_mode)) == item['permission_mode']
for name in ['INPUT_PINS.json', 'SOURCE_PRECISION_QUALIFICATIONS.md', 'CURRENT_OVERVIEW.md',
             'DRAFT_ROOT_READ_LEDGER.json', 'DRAFT_ROOT_SCIENCE_CARD.json', 'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
    assert (P / name).read_bytes() == (A / 'current_preparation_family' / name).read_bytes()
assert row(P / 'prepare_current_packet.py') == repair['new_builder']
assert row(P / 'SOURCE_REPAIR_DELTA.patch') == repair['delta']
for name, pid in [('AUTHORING_ACTUAL_CAPTURE', 22454), ('PERMISSION_ACTUAL_CAPTURE', 22572)]:
    capture = J(P / name / 'CAPTURE.json')
    assert capture['actual_execution'] is True and capture['completed'] is True
    assert capture['pid'] == pid and capture['exit_code'] == 0 and capture['builder_imported_executed_compiled'] is False
    for channel in ['stdout', 'stderr']:
        raw = (P / name / capture[channel]['path']).read_bytes()
        assert len(raw) == capture[channel]['bytes'] and H(raw) == capture[channel]['sha256']
controls = J(P / 'PERMISSION_CONTROL_RESULTS.json')
assert controls['wrong_mode_cases_rejected'] == 3 and controls['ordinary_0444_accepted'] is True
for case in controls['cases']:
    path = P / case['path']
    assert oct(stat.S_IMODE(path.stat().st_mode)) == case['observed_full_permission']
now = dt.datetime.now(dt.timezone.utc).isoformat()
status = dict(schema='PR42_ADJACENT_V2_CLOSED_SOURCE_ONLY_STATUS_v1', utc=now,
              static_whole_source_contract_draft_read_completed=True,
              builder=row(P / 'prepare_current_packet.py'), prior_closures_unchanged=True,
              full_permission_guard_repaired=True, own_actual_finite_wrong_modes_rejected=3,
              own_actual_ordinary_0444_accepted=True, builder_imported_executed_compiled=False,
              candidate_created=False, ROOT_reading_or_approval_attested_by_preparer=False,
              new_different_source_adversary='PENDING', NEW_whole_current_gate='PENDING',
              future_whole_current_verdict=None, current_model=None, current_reasoning_effort=None,
              current_deadline_utc=None, full_problem_solved=False, novelty_claimed=False,
              original_substantive_attempts=2, turn_limit=5, new_substantive_attempts=0, audit_turns=0,
              source_preparation_completion_percent=100, publication_workflow_percent=65,
              full_problem_discovery_percent=0, native_canonical_git_index_remote_writes=False,
              external_human_contact=False)
(P / 'SOURCE_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
(P / 'SOURCE_PREPARATION_RESEARCH_LOG.md').write_text(
    '# Adjacent v2 source-preparation research log\n\n'
    '2026-10-02T23:24:21.020270+00:00 — genuine authoring PID22454, exit0. Exact original21+self and source-adversary193+self/four intentional emptydirs checked unchanged. Full permission guards and all six source anchors revised; exact delta/source/predecessor refs retained. Source preparation70%; publication workflow65%; full discovery0%. Original2/5,new0/audit0.\n\n'
    '2026-10-02T23:24:28.103915+00:00 — own permission predicates PID22572, exit0. Actual04444/02444/01444 rejected;0444 accepted. Four probe files and complete source/capture retained. No builder/helper import/compile/execute. Source preparation85%; publication workflow65%; full discovery0%.\n\n'
    + now + ' — whole source/contracts/drafts statically read and exact adjacent closure verified. Source preparation100%; publication workflow65%; full discovery0%. Original qualification/science/eight flags/four ROOT schemas and dated native13 unchanged. NEW different source adversary, ROOT genuine fresh13/prerequisites, future freeze and NEW whole-current review PENDING. Full EP-653 UNSOLVED. No fabricated future PASS or runtime. Tool-only failed guessed read/truncated display disclosed.\n')
files, directories = [], set()
for path in sorted(P.rglob('*')):
    assert not path.is_symlink()
    if path.is_file():
        files.append(row(path))
    else:
        assert path.is_dir()
        directories.add(path.relative_to(P).as_posix())
assert directories == {parent.as_posix() for item in files for parent in Path(item['path']).parents if parent.as_posix() != '.'}
manifest = dict(schema='PR42_ADJACENT_V2_SOURCE_ONLY_PREPARATION_MANIFEST_v1',
                status='CLOSED_SOURCE_ONLY_CURRENT_PREPARATION', utc=now,
                self_excluded=['PREPARATION_MANIFEST.json'], files_count=len(files), files=files,
                builder_imported_executed_compiled=False, future_current_freeze_or_whole_PASS_claimed=False,
                prior_preparation_manifest_sha256='af4f28f77df2b7541b099a47fb89a5a454dda5a64272be6e9b70254d17b5c5fa',
                prior_source_adversary_manifest_sha256='6c1d15b46aeba383cb8fea883755efa27bbe9f6b9e8d46f6243d783f3997c518',
                original_substantive_attempts=2, new_substantive_attempts=0, audit_turns=0)
(P / 'PREPARATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
for item in files:
    assert row(P / item['path']) == item
assert {path.relative_to(P).as_posix() for path in P.rglob('*') if path.is_file()} == {item['path'] for item in files} | {'PREPARATION_MANIFEST.json'}
print(json.dumps(dict(status=manifest['status'], source_sha256=status['builder']['sha256'],
                     manifest_sha256=H((P / 'PREPARATION_MANIFEST.json').read_bytes()),
                     qualification_sha256=repair['qualification_sha256'], files=len(files),
                     candidate_created=False, builder_imported_executed_compiled=False), indent=2))
