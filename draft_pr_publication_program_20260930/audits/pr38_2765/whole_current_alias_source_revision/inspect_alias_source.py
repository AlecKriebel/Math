"""Independent read-only inspection; never imports or executes the alias builder."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import ast
import hashlib
import json

OWN = Path(__file__).resolve().parent
AUDIT = OWN.parents[1]
PREP = AUDIT / 'acceptance_preparation_family/alias_source_revision'
V1 = AUDIT / 'reviewed_candidate'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            assert key not in out, ('duplicate JSON key', key)
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=unique)


def exact(root, rows, self_name):
    expected, dirs = {}, set()
    assert root.is_dir() and not root.is_symlink()
    assert all(not p.is_symlink() for p in root.parents)
    for row in rows:
        assert set(row) == {'path', 'bytes', 'sha256'}
        name = row['path']
        path = PurePosixPath(name)
        assert name and path.as_posix() == name and not path.is_absolute()
        assert '..' not in path.parts and '\\' not in name
        assert name not in expected and name != self_name
        assert type(row['bytes']) is int and row['bytes'] >= 0
        expected[name] = row
        dirs.update(p.as_posix() for p in path.parents if p.as_posix() != '.')
    files, actual_dirs = set(), set()
    for path in root.rglob('*'):
        assert not path.is_symlink() and (path.is_file() or path.is_dir())
        (files if path.is_file() else actual_dirs).add(path.relative_to(root).as_posix())
    assert files == set(expected) | {self_name}
    assert actual_dirs == dirs
    payload = {}
    for name, row in expected.items():
        raw = (root / name).read_bytes()
        assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], name
        payload[name] = raw
    return payload


prep_raw = (PREP / 'ALIAS_PREPARATION_MANIFEST.json').read_bytes()
assert sha(prep_raw) == '0ed8ecfad28606427b8fd3312da3d1b86d17f7b46e1802f831c962c9b0da0e8a'
prep = parse(prep_raw)
assert prep['self_excluded'] == ['ALIAS_PREPARATION_MANIFEST.json']
assert prep['files_count'] == len(prep['files']) == 8
inputs = exact(PREP, prep['files'], 'ALIAS_PREPARATION_MANIFEST.json')
source = inputs['restore_review_alias.py']
assert sha(source) == 'c30a30983e3d26f36b2ca055177a0445b26870deb0085082eb6d7f44db554210'
ast.parse(source)
assert len(source.splitlines()) == 131

v1_raw = (V1 / 'MANIFEST.json').read_bytes()
assert sha(v1_raw) == '054b156eb6d44903eadeffeda2012a23c68db530b514294830cc0f45c7b93912'
v1 = parse(v1_raw)
assert v1['self_excluded'] == ['MANIFEST.json']
assert v1['files_count'] == len(v1['files']) == 1499
old = exact(V1, v1['files'], 'MANIFEST.json')
assert 'review/REVIEW.md' not in old
assert b'see review/REVIEW.md.' in old['RESULTS.md']
alias = old['original_archive/review/REVIEW.md']
assert len(alias) == 13796 and sha(alias) == '8f02671b88b1cdf6e887d087780d3b191672db35e67a8320be3601cbe3834896'
receipt = parse(inputs['EXPECTED_V2_ALIAS_RECEIPT.json'])
assert receipt['actual_execution_attested'] is False
assert receipt['builder_sha256'] == sha(source)
assert receipt['source_v1_manifest_sha256'] == sha(v1_raw)
assert receipt['metadata_append_sha256'] == sha(inputs['ARCHIVAL_NOTICE_APPEND.txt'])
expected_raw = inputs['EXPECTED_V2_MANIFEST.json']
assert sha(expected_raw) == 'b48e3e17b884056143a7132fd519872ac5223a0ef15fa4bb3d5738e3f58bb52c'
expected = parse(expected_raw)
assert expected['self_excluded'] == ['MANIFEST.json']
assert expected['files_count'] == len(expected['files']) == 1502
new = dict(old)
for name in ['README.md', 'CURRENT_CONTEXT.md']:
    new[name] = old[name] + inputs['ARCHIVAL_NOTICE_APPEND.txt']
new['review/REVIEW.md'] = alias
new['V1_MANIFEST.json'] = v1_raw
new['V2_ALIAS_RECEIPT.json'] = inputs['EXPECTED_V2_ALIAS_RECEIPT.json']
rows = [{'path': n, 'bytes': len(raw), 'sha256': sha(raw)} for n, raw in sorted(new.items())]
assert rows == expected['files']
changed = sorted(n for n in old if old[n] != new[n])
added = sorted(set(new) - set(old))
assert changed == ['CURRENT_CONTEXT.md', 'README.md']
assert added == ['V1_MANIFEST.json', 'V2_ALIAS_RECEIPT.json', 'review/REVIEW.md']
assert sum(old[n] == new[n] for n in old) == 1497
assert sha(new['CURRENT_PROOF_DEPENDENCIES.json']) == '1b9d41f102cf3345777f4b77c5c5ffbf2db1084d82b6ce8b4a7fb8b5b4af2e79'
result = {
    'utc': datetime.now(timezone.utc).isoformat(),
    'verdict': 'PASS_SOURCE_ONLY_EXACT_ALIAS_REVISION',
    'builder_imported': False, 'builder_executed': False,
    'candidate_or_shared_writes': False,
    'preparation_members_verified': 8,
    'preparation_manifest_sha256': sha(prep_raw),
    'builder_sha256': sha(source), 'builder_lines_read': 131,
    'v1_members_read_and_hashed': 1499,
    'v1_manifest_sha256': sha(v1_raw),
    'prospective_v2_members': 1502,
    'prospective_v2_manifest_sha256': sha(expected_raw),
    'prospective_existing_changes': changed,
    'prospective_additions': added,
    'original_members_byte_unchanged': 1497,
    'actual_v2_review_pending': True,
    'new_substantive_attempts': 0, 'audit_turns': 0,
}
(OWN / 'SOURCE_ONLY_INSPECTION.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
