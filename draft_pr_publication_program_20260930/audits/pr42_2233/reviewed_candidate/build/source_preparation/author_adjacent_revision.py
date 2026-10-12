"""Authoring-only PR42 adjacent mode-guard repair; never loads/runs/compiles builder."""
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import stat

P = Path(__file__).resolve().parent
A = P.parent
OLD = A / 'current_preparation_family'
ADV = A / 'current_source_adversary_family'
def H(raw):
    return hashlib.sha256(raw).hexdigest()
def J(path):
    return json.loads(path.read_bytes())
def row(path, anchor=A):
    assert path.is_file() and not path.is_symlink() and all(not p.is_symlink() for p in path.parents)
    raw = path.read_bytes()
    return dict(path=path.relative_to(anchor).as_posix(), bytes=len(raw), sha256=H(raw))
def tree(root):
    files, directories = set(), set()
    for path in root.rglob('*'):
        assert not path.is_symlink()
        if path.is_file():
            files.add(path.relative_to(root).as_posix())
        else:
            assert path.is_dir()
            directories.add(path.relative_to(root).as_posix())
    return files, directories
def write(name, body):
    path = P / name
    assert not path.exists()
    path.write_bytes(body)
def JSON(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()

old_manifest = J(OLD / 'PREPARATION_MANIFEST.json')
adv_manifest = J(ADV / 'OWN_CLOSED_MANIFEST.json')
assert H((OLD / 'PREPARATION_MANIFEST.json').read_bytes()) == 'af4f28f77df2b7541b099a47fb89a5a454dda5a64272be6e9b70254d17b5c5fa'
assert H((ADV / 'OWN_CLOSED_MANIFEST.json').read_bytes()) == '6c1d15b46aeba383cb8fea883755efa27bbe9f6b9e8d46f6243d783f3997c518'
assert old_manifest['files_count'] == 21 and adv_manifest['files_count'] == 193
for root, manifest, self_name in [(OLD, old_manifest, 'PREPARATION_MANIFEST.json'), (ADV, adv_manifest, 'OWN_CLOSED_MANIFEST.json')]:
    files, directories = tree(root)
    assert files == {item['path'] for item in manifest['files']} | {self_name}
    if root == ADV:
        assert directories == set(manifest['directories'])
        assert len(manifest['explicitly_retained_own_empty_finite_control_directories']) == 4
    else:
        assert directories == {parent.as_posix() for name in files for parent in Path(name).parents if parent.as_posix() != '.'}
    for item in manifest['files']:
        actual = row(root / item['path'], root)
        assert actual == {key:item[key] for key in ['path', 'bytes', 'sha256']}
        if root == ADV:
            assert oct(stat.S_IMODE((root / item['path']).stat().st_mode)) == item['permission_mode']

old_raw = (OLD / 'prepare_current_packet.py').read_bytes()
assert H(old_raw) == '66a5bc427e90032f6f86bd1007479fadf154282e3f41dfb047a9dd44551c8730'
old_source = old_raw.decode()
assert old_source.count("current_preparation_family") == 6
new_source = old_source.replace('current_preparation_family', 'current_preparation_family_v2')
assert new_source.count('import sys\n') == 1
new_source = new_source.replace('import sys\n', 'import stat\nimport sys\n')
assert new_source.count('path.stat().st_mode & 0o777 == 0o444') == 1
assert new_source.count("(stage / 'MANIFEST.json').stat().st_mode & 0o777 == 0o444") == 1
new_source = new_source.replace('path.stat().st_mode & 0o777 == 0o444', 'stat.S_IMODE(path.stat().st_mode) == 0o444')
new_source = new_source.replace("(stage / 'MANIFEST.json').stat().st_mode & 0o777 == 0o444", "stat.S_IMODE((stage / 'MANIFEST.json').stat().st_mode) == 0o444")
anchor = "    require(git('branch', '--show-current').strip() == b'main', 'Stay on main')\n"
assert new_source.count(anchor) == 1
binding = '''    repair = load(bind('current_preparation_family_v2/REPAIR_INPUT_PINS.json', 'adjacent_permission_guard_repair_contract'))
    # Bind the unchanged original source audit and full adversarial closure.
    # These already-retained sources/captures stay in their closed audit folders;
    # no large forensic logs are copied again into the current candidate.
    for info in repair['prior_closed_evidence']:
        prefix = relative(info['directory'])
        self_name = relative(info['manifest']['path'])
        raw = checked(dict(info['manifest'], path=prefix + '/' + self_name), 'unchanged_prior_source_or_adversary_manifest')
        manifest = load(raw)
        normalized = [{key: item[key] for key in ['path', 'bytes', 'sha256']} for item in manifest['files']]
        expected_files = rows(normalized) | {self_name}
        require(manifest['files_count'] == info['files_count'] and type(manifest['files_count']) is int and manifest['self_excluded'] == [self_name], 'Exact prior closed manifest shape required')
        actual_files, actual_directories = set(), set()
        for path in (audit / prefix).rglob('*'):
            require(not path.is_symlink(), 'Prior closure symlink rejected')
            name = relative(path.relative_to(audit / prefix).as_posix())
            if path.is_file():
                actual_files.add(name)
            else:
                require(path.is_dir(), 'Prior closure special member rejected')
                actual_directories.add(name)
        require(actual_files == expected_files and actual_directories == set(info['directories']), 'Prior closure extra/missing file/directory rejected')
        if 'directories' in manifest:
            require(equal(manifest['directories'], info['directories']) and equal(manifest['explicitly_retained_own_empty_finite_control_directories'], info['intentional_empty_directories']), 'Exact prior intentional directories changed')
        for item in manifest['files']:
            checked(dict({key: item[key] for key in ['path', 'bytes', 'sha256']}, path=prefix + '/' + item['path']), 'unchanged_prior_source_or_adversary_member')
            if 'permission_mode' in item:
                require(oct(stat.S_IMODE((audit / prefix / item['path']).stat().st_mode)) == item['permission_mode'], 'Original adversary control permission changed')
'''
new_source = new_source.replace(anchor, binding + anchor)
write('prepare_current_packet.py', new_source.encode())
write('SOURCE_REPAIR_DELTA.patch', ''.join(difflib.unified_diff(old_source.splitlines(keepends=True), new_source.splitlines(keepends=True), fromfile='current_preparation_family/prepare_current_packet.py', tofile='current_preparation_family_v2/prepare_current_packet.py')).encode())
copy_exact = ['INPUT_PINS.json', 'SOURCE_PRECISION_QUALIFICATIONS.md', 'CURRENT_OVERVIEW.md',
              'DRAFT_ROOT_READ_LEDGER.json', 'DRAFT_ROOT_SCIENCE_CARD.json', 'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']
for name in copy_exact:
    write(name, (OLD / name).read_bytes())
assert H((P / 'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()) == '3529898445960cde70381bf99ea8287ec88a1003d8ca1cb4c3e0d088abdee570'
for name in ['EXECUTION_CONTRACT.md', 'ROOT_READ_EXPECTATIONS.md']:
    body = (OLD / name).read_text().replace('current_preparation_family', 'current_preparation_family_v2')
    body += ('\nAdjacent v2 source-only revision: the full `stat.S_IMODE` permission check\n'
             'rejects set-user-ID/set-group-ID/sticky modes on every staged file and\n'
             'its manifest. Original preparation21+self and source-adversary193+self\n'
             'and its four intentional empty controls remain untouched and individually\n'
             'hash-bound at their exact audit locations. No large prior forensic logs\n'
             'are recopied. All scientific qualifications, eight flags, four external\n'
             'ROOT prerequisite schemas, budget/null fields and NEW whole-current\n'
             'gate remain unchanged. A NEW different source adversary must review\n'
             'this exact revision before ROOT execution.\n')
    write(name, body.encode())
prior = []
for root, manifest, self_name in [(OLD, old_manifest, 'PREPARATION_MANIFEST.json'), (ADV, adv_manifest, 'OWN_CLOSED_MANIFEST.json')]:
    _, directories = tree(root)
    prior.append(dict(directory=root.name, manifest=row(root / self_name, root), files_count=manifest['files_count'],
                      directories=sorted(directories), intentional_empty_directories=manifest.get('explicitly_retained_own_empty_finite_control_directories', [])))
repair = dict(schema='PR42_ADJACENT_PERMISSION_REPAIR_PINS_v1', utc=dt.datetime.now(dt.timezone.utc).isoformat(),
              prior_closed_evidence=prior, original_builder=row(OLD / 'prepare_current_packet.py'),
              adversary_report=row(ADV / 'SOURCE_AUDIT_REPORT.md'), adversary_verdict=row(ADV / 'FAMILY_VERDICT.json'),
              new_builder=row(P / 'prepare_current_packet.py', P), delta=row(P / 'SOURCE_REPAIR_DELTA.patch', P),
              qualification_sha256=H((P / 'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()),
              original_science_and_ROOT_schemas_unchanged=True, future_current_freeze_or_whole_PASS_claimed=False,
              original_substantive_attempts=2, new_substantive_attempts=0, audit_turns=0,
              current_model=None, current_reasoning_effort=None, current_deadline_utc=None,
              native13_remain_dated_observations=True)
write('REPAIR_INPUT_PINS.json', JSON(repair))
print(json.dumps(dict(status='ADJACENT_SOURCE_ONLY_PERMISSION_REPAIR_AUTHORED',
                     old_source_unchanged=H((OLD / 'prepare_current_packet.py').read_bytes()) == repair['original_builder']['sha256'],
                     prior_files=[info['files_count'] for info in prior], prior_adversary_empty_directories=4,
                     new_builder_sha256=repair['new_builder']['sha256'], builder_imported_executed_compiled=False), indent=2))
