"""Independent actual v2 inspection. No candidate builder/program is imported or run."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast
import hashlib
import json

OWN = Path(__file__).resolve().parent
AUDIT = OWN.parent
V1 = AUDIT / 'reviewed_candidate'
V2 = AUDIT / 'reviewed_candidate_v2'
PREP = AUDIT / 'acceptance_preparation_family/alias_source_revision'
SOURCE_REVIEW = AUDIT / 'whole_current_alias_source_revision'
V1_REVIEW = AUDIT / 'whole_current_source_first_family'
CAP = AUDIT / 'root_v2_alias_actual_capture'
READS = []


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, role):
    assert path.is_file() and not path.is_symlink(), str(path)
    assert all(not p.is_symlink() for p in path.parents), str(path)
    raw = path.read_bytes()
    READS.append({'path': str(path.relative_to(AUDIT)), 'bytes': len(raw),
                  'sha256': sha(raw), 'role': role})
    return raw


def parse(raw):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            assert key not in out, ('duplicate JSON key', key)
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=unique)


def safe(name):
    p = PurePosixPath(name)
    return bool(name) and p.as_posix() == name and not p.is_absolute() and '..' not in p.parts and '\\' not in name


def exact(root, rows, self_name, role):
    expected, dirs = {}, set()
    assert root.is_dir() and not root.is_symlink()
    assert all(not p.is_symlink() for p in root.parents)
    for row in rows:
        assert set(row) == {'path', 'bytes', 'sha256'}
        name = row['path']
        assert safe(name) and name not in expected and name != self_name
        assert type(row['bytes']) is int and row['bytes'] >= 0
        expected[name] = row
        dirs.update(p.as_posix() for p in PurePosixPath(name).parents if p.as_posix() != '.')
    files, actual_dirs = set(), set()
    for path in root.rglob('*'):
        assert not path.is_symlink() and (path.is_file() or path.is_dir()), str(path)
        (files if path.is_file() else actual_dirs).add(path.relative_to(root).as_posix())
    assert files == set(expected) | {self_name}, ('file closure', str(root))
    assert actual_dirs == dirs, ('directory closure', str(root))
    payload = {}
    for name, row in expected.items():
        raw = read(root / name, role)
        assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], name
        payload[name] = raw
    return payload


v1raw = read(V1 / 'MANIFEST.json', 'frozen_v1_self')
v2raw = read(V2 / 'MANIFEST.json', 'actual_v2_self')
assert sha(v1raw) == '054b156eb6d44903eadeffeda2012a23c68db530b514294830cc0f45c7b93912'
assert sha(v2raw) == 'b48e3e17b884056143a7132fd519872ac5223a0ef15fa4bb3d5738e3f58bb52c'
v1, v2 = parse(v1raw), parse(v2raw)
assert v1['self_excluded'] == v2['self_excluded'] == ['MANIFEST.json']
assert v1['files_count'] == len(v1['files']) == 1499
assert v2['files_count'] == len(v2['files']) == 1502
old = exact(V1, v1['files'], 'MANIFEST.json', 'frozen_v1_member')
new = exact(V2, v2['files'], 'MANIFEST.json', 'actual_v2_member')
expected_manifest = read(PREP / 'EXPECTED_V2_MANIFEST.json', 'source_only_expected_manifest')
assert v2raw == expected_manifest
notice = read(PREP / 'ARCHIVAL_NOTICE_APPEND.txt', 'pinned_archival_notice')
changed = sorted(n for n in old if old[n] != new[n])
added = sorted(set(new) - set(old))
assert changed == ['CURRENT_CONTEXT.md', 'README.md']
assert added == ['V1_MANIFEST.json', 'V2_ALIAS_RECEIPT.json', 'review/REVIEW.md']
assert not (set(old) - set(new))
for name in changed:
    assert new[name] == old[name] + notice
assert sum(new[n] == old[n] for n in old) == 1497
assert new['V1_MANIFEST.json'] == v1raw
assert new['V2_ALIAS_RECEIPT.json'] == read(PREP / 'EXPECTED_V2_ALIAS_RECEIPT.json', 'pinned_derivation_receipt')
assert new['review/REVIEW.md'] == old['original_archive/review/REVIEW.md']
assert new['RESULTS.md'] == old['RESULTS.md'] and b'see review/REVIEW.md.' in new['RESULTS.md']
assert 'review/REVIEW.md' not in old
assert parse(new['V2_ALIAS_RECEIPT.json'])['actual_execution_attested'] is False

dependency_raw = new['CURRENT_PROOF_DEPENDENCIES.json']
assert dependency_raw == old['CURRENT_PROOF_DEPENDENCIES.json']
assert sha(dependency_raw) == '1b9d41f102cf3345777f4b77c5c5ffbf2db1084d82b6ce8b4a7fb8b5b4af2e79'
dependencies = parse(dependency_raw)
assert dependencies['dependency_anchor_repository_relative'] == 'draft_pr_publication_program_20260930/audits/pr38_2765'
dep_rows = dependencies['files']
assert len(dep_rows) == len({r['path'] for r in dep_rows}) == 1472
dep_payload = {}
for row in dep_rows:
    name = row['path']
    assert safe(name) and not name.startswith(('tmp/', 'ignoredtmp/'))
    assert Path(name).suffix not in ['.pdf', '.sqlite']
    raw = read(AUDIT / name, 'actual_unchanged_dependency')
    assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], name
    dep_payload[name] = raw

support = AUDIT / 'root_closed_families_actual_reproduction_support'
support_raw = read(support / 'ROOT_SUPPORT_MANIFEST.json', 'retained_support_self')
assert sha(support_raw) == dependencies['retention_manifest']['sha256']
support_manifest = parse(support_raw)
support_rows = support_manifest['files']
assert len(support_rows) == 1269
support_payload = exact(support, support_rows, 'ROOT_SUPPORT_MANIFEST.json', 'retained_support_member')

prior = parse(read(V1_REVIEW / 'WHOLE_CURRENT_COVERAGE.json', 'independent_prior_control_qualification'))
bad = {r['path']: r for r in prior['exact_malformed_negative_inputs'] if r['root'] == 'candidate'}
assert len(bad) == 12
baseline = read(AUDIT / 'current_measure_family/bonahon_access_followup.json', 'original_negative_control_baseline')
qualified = []
json_counts, jsonl_counts, ast_counts = {}, {}, {}
for label, payload in [('actual_v2', dict(new, **{'MANIFEST.json': v2raw})),
                       ('retained_support', dict(support_payload, **{'ROOT_SUPPORT_MANIFEST.json': support_raw})),
                       ('dependencies', dep_payload)]:
    valid, exceptions, lines, asts = 0, set(), 0, 0
    for name, raw in payload.items():
        if name.endswith('.json'):
            try:
                parse(raw)
                valid += 1
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                relative = name
                if label == 'dependencies':
                    prefix = 'root_closed_families_actual_reproduction_support/'
                    assert name.startswith(prefix)
                    relative = name[len(prefix):]
                pin = bad.get(relative)
                assert pin is not None and len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], name
                if relative.endswith('bonahon_access_followup.json'):
                    assert raw == bytes([baseline[0] ^ 1]) + baseline[1:]
                    provenance = 'one-byte XOR of complete pinned original current_measure baseline'
                else:
                    assert raw == b'Actual nested same-basename extra-file control.\n'
                    provenance = 'exact literal deliberate nested-manifest control input'
                exceptions.add(relative)
                qualified.append({'root': label, 'path': name, 'bytes': len(raw),
                                  'sha256': sha(raw), 'parse_error': str(exc), 'provenance': provenance})
        elif name.endswith('.jsonl'):
            for line in raw.splitlines():
                if line.strip():
                    parse(line)
                    lines += 1
        elif name.endswith('.py'):
            ast.parse(raw)
            asts += 1
    assert exceptions == set(bad), label
    json_counts[label], jsonl_counts[label], ast_counts[label] = valid, lines, asts
assert json_counts['actual_v2'] == 456 and json_counts['dependencies'] == 436

capture_raw = read(CAP / 'CAPTURE.json', 'root_actual_capture')
capture = parse(capture_raw)
captured_source = read(CAP / 'prelaunch_source.py', 'complete_root_prelaunch_source')
builder = read(PREP / 'restore_review_alias.py', 'reviewed_alias_source')
assert captured_source == builder and sha(builder) == capture['source_sha256'] == 'c30a30983e3d26f36b2ca055177a0445b26870deb0085082eb6d7f44db554210'
assert len(builder.splitlines()) == 131
assert capture['argv'] == ['/usr/bin/python3', '-B', str(PREP / 'restore_review_alias.py'), '--execute', '--preparation-manifest-sha256', '0ed8ecfad28606427b8fd3312da3d1b86d17f7b46e1802f831c962c9b0da0e8a']
assert capture['cwd'] == str(AUDIT)
assert capture['actual_execution'] is True and capture['completed'] is True
assert capture['exit_code'] == 0 and capture['status'] == 'PASS' and capture['pid'] == 40932
assert datetime.fromisoformat(capture['finished_utc']) > datetime.fromisoformat(capture['started_utc'])
streams = {}
for name in ['stdout', 'stderr']:
    row = capture[name]
    assert row['path'] == name + '.bin'
    raw = read(CAP / row['path'], 'complete_root_actual_' + name)
    assert len(raw) == row['size'] and sha(raw) == row['sha256']
    streams[name] = raw
assert len(streams['stdout']) == 588 and streams['stderr'] == b''
emitted = parse(streams['stdout'])
assert emitted == {'status': 'ACTUAL_ADMINISTRATIVE_V2_ALIAS_BUILD_COMPLETE', 'candidate': str(V2), 'files_count': 1502, 'manifest_bytes': len(v2raw), 'manifest_sha256': sha(v2raw), 'v1_manifest_sha256_unchanged': sha(v1raw), 'alias_sha256': sha(new['review/REVIEW.md']), 'actual_capture_by_root_required': True, 'new_substantive_attempts': 0, 'audit_turns': 0}

# The relocated source-only scope is preserved and the old v1 scope is restored.
source_review_raw = read(SOURCE_REVIEW / 'FAMILY_MANIFEST.json', 'closed_source_only_followup_manifest')
assert sha(source_review_raw) == '3ef1b8341556d005097c9982edeaa532aa673dfd006d2b9feef1ef949d971c5d'
source_review_manifest = parse(source_review_raw)
exact(SOURCE_REVIEW, source_review_manifest['files'], 'FAMILY_MANIFEST.json', 'closed_source_only_followup_member')
v1_review_raw = read(V1_REVIEW / 'FAMILY_MANIFEST.json', 'closed_original_independent_v1_manifest')
assert sha(v1_review_raw) == '9f581a31a7514ff6c1ebe30301c4efbb30adaf67a1cf4b8c85d926130a769e10'
v1_review = parse(v1_review_raw)
actual_firstparty = {p.relative_to(V1_REVIEW).as_posix() for p in V1_REVIEW.rglob('*')
                     if p.is_file() and not p.relative_to(V1_REVIEW).as_posix().startswith('primary_text/')}
assert actual_firstparty == {r['path'] for r in v1_review['files']} | {'FAMILY_MANIFEST.json'}
assert len(v1_review['files']) == 12
for row in v1_review['files']:
    raw = read(V1_REVIEW / row['path'], 'preserved_original_independent_v1_member')
    assert len(raw) == row['bytes'] and sha(raw) == row['sha256']

receipt = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'verdict': 'VALID_UNSOLVED_PARTIAL_NO_REMAINING_MANDATORY_CORRECTIONS',
    'actual_v2_manifest_sha256': sha(v2raw), 'actual_v2_members_plus_self': [1502, 1],
    'frozen_v1_manifest_sha256': sha(v1raw), 'frozen_v1_members_plus_self': [1499, 1],
    'changed_existing_members': changed, 'added_members': added,
    'other_original_member_bytes_unchanged': 1497,
    'dependency_manifest_sha256': sha(dependency_raw), 'dependencies_checked': 1472,
    'retained_support_members_plus_self': [1269, 1],
    'every_complete_JSON_parsed_except_exact_control_inputs': json_counts,
    'exact_malformed_control_qualifications': qualified,
    'complete_JSONL_records_parsed': jsonl_counts, 'Python_ASTs_parsed_no_imports': ast_counts,
    'root_actual_capture_sha256': sha(capture_raw), 'root_actual_capture': capture,
    'root_stdout_whole_JSON_checked': emitted,
    'all_complete_byte_reads': READS,
    'candidate_builder_or_science_imported_or_executed_by_reviewer': False,
    'candidate_shared_native_git_remote_writes_by_reviewer': False,
    'scientific_verdict_qualification': 'The four scoped propositions retain the prior independent report with explicitly imported standard continuity/uniformization inputs. Arbitrary closed self-intersecting references remain unresolved. These finite administrative checks supply no new general mathematical proof.',
    'root_new_final_gate_pending': True,
    'original_substantive_attempts': 2, 'new_substantive_attempts': 0, 'audit_turns': 0,
}
(OWN / 'ACTUAL_V2_INSPECTION.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k not in ['all_complete_byte_reads', 'exact_malformed_control_qualifications']}, indent=2))
