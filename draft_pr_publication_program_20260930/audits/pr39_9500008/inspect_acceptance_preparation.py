#!/usr/bin/env python3
"""Root's independent byte/type/closure inspection; never import proposed helpers."""
import ast
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath

R = Path('/Users/alec/Documents/Math')
A = R / 'draft_pr_publication_program_20260930/audits/pr39_9500008'
P = A / 'acceptance_preparation_family'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def unique(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, ('duplicate key', key)
        out[key] = value
    return out

def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def pin(path):
    raw = path.read_bytes()
    return dict(path=path.relative_to(R).as_posix(), bytes=len(raw), sha256=sha(raw))

def normalize(value):
    if isinstance(value, dict):
        value = [dict(path=k, **v) for k, v in value.items()]
    out = []
    for row in value:
        row = dict(row)
        row['bytes'] = row.get('bytes', row.get('size'))
        assert type(row['bytes']) is int
        name = PurePosixPath(row['path'])
        assert not name.is_absolute() and '..' not in name.parts and str(name) == row['path']
        out.append(row)
    assert len({x['path'] for x in out}) == len(out)
    return out

checked, parsed, negative = {}, {}, {}
exceptions = parse((P / 'INPUT_BINDINGS.json').read_bytes())['qualified_JSON_negative_inputs']
exception_by_path = {x['path']: x for x in exceptions}

def check(base, row):
    path = base / row['path']
    assert path.is_file() and not path.is_symlink()
    for parent in path.parents:
        if parent == base:
            break
        assert not parent.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], path
    name = path.relative_to(R).as_posix()
    checked[name] = pin(path)
    if path.suffix in {'.json', '.jsonl'}:
        if name in exception_by_path:
            ex = exception_by_path[name]
            assert len(raw) == ex['bytes'] and sha(raw) == ex['sha256']
            try:
                parse(raw)
            except (json.JSONDecodeError, AssertionError, ValueError) as error:
                assert str(error) == ex['parse_failure'] or ex['parse_failure'] == 'duplicate key status' and str(error) == "('duplicate key', 'status')"
                negative[name] = str(error)
            else:
                raise AssertionError('Negative parsed: ' + name)
        elif path.suffix == '.json':
            parsed[name] = parse(raw)
        else:
            assert not raw or raw.endswith(b'\n')
            parsed[name] = [parse(line) for line in raw.splitlines()]

def closure(base, members, self_name, private=(), empty=()):
    expected = {x['path'] for x in members} | {self_name}
    actual, dirs = set(), set()
    for path in base.rglob('*'):
        assert not path.is_symlink() and (path.is_file() or path.is_dir()), path
        name = path.relative_to(base).as_posix()
        if name.split('/')[0] in private:
            continue
        (dirs if path.is_dir() else actual).add(name)
    assert actual == expected, (base, sorted(actual ^ expected))
    expected_dirs = {str(p) for n in expected for p in PurePosixPath(n).parents if str(p) != '.'} | set(empty)
    assert dirs == expected_dirs, (base, sorted(dirs ^ expected_dirs))
    for name in empty:
        assert not any((base / name).iterdir())
    for row in members:
        check(base, row)
    checked[(base / self_name).relative_to(R).as_posix()] = pin(base / self_name)
    parsed[(base / self_name).relative_to(R).as_posix()] = parse((base / self_name).read_bytes())

manifest = parse((P / 'PREPARATION_MANIFEST.json').read_bytes())
assert sha((P / 'PREPARATION_MANIFEST.json').read_bytes()) == 'f66df61cb4b57ae63cc007fed3c4dabf9e67e027f1d428d4e0ffbc75a6332fca'
closure(P, normalize(manifest['files']), 'PREPARATION_MANIFEST.json')
inputs = parse((P / 'INPUT_BINDINGS.json').read_bytes())
for family in inputs['closures']:
    m = family['manifest']
    check(R, m)
    path = R / m['path']
    obj = parse(path.read_bytes())
    members = normalize(obj[family['member_field']])
    assert len(members) == family['authored_count']
    closure(path.parent, members + family['qualified_extra_members'], path.name, family['excluded_root_private_trees'], family['qualified_empty_directories'])
for row in inputs['pins'].values():
    check(R, row)
deps = parse((A / 'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json').read_bytes())
assert len(deps['files']) == 2797
for row in normalize(deps['files']):
    check(A, row)
for item in inputs['outer_typed_captures']:
    path = R / item['capture']['path']
    cap = parse(path.read_bytes())
    assert cap['actual_execution'] is True and cap['completed'] is True and cap['pid'] == item['expected_pid'] and cap['exit_code'] == item['expected_exit_code']
    closure(path.parent, item['files'], path.name) if path.name not in {x['path'] for x in item['files']} else closure(path.parent, [x for x in item['files'] if x['path'] != path.name], path.name)
source_bindings = parse((P / 'SOURCE_BINDINGS.json').read_bytes())
patch = ''
for row in source_bindings['complete_sources']:
    check(R, row['new'])
    check(R, row['sealed_predecessor'])
    old_path, new_path = R / row['sealed_predecessor']['path'], R / row['new']['path']
    new = new_path.read_text()
    ast.parse(new)
    assert len(new.splitlines()) == row['new_lines']
    patch += ''.join(difflib.unified_diff(old_path.read_text().splitlines(keepends=True), new.splitlines(keepends=True), fromfile=row['sealed_predecessor']['path'], tofile=row['new']['path']))
assert patch.encode() == (P / 'ADAPTATION.patch').read_bytes()
plan = parse((P / 'DRAFT_FINAL_PLAN.json').read_bytes())
assert [plan[k] for k in ('root_full_current_read_completed', 'root_full_whole_scope_read_completed', 'independent_whole_current_pass')] == [False, False, False]
assert plan['preparation_manifest_sha256'] is None
assert plan['scientific_scope'] == parse((P / 'SCIENTIFIC_SCOPE.json').read_bytes())
assert len(plan['immutable_evidence_references']) == 33
for row in plan['immutable_evidence_references']:
    check(R, row)
result = dict(utc=dt.datetime.now(dt.timezone.utc).isoformat(), status='PASS', pr=39,
    preparation_manifest=pin(P / 'PREPARATION_MANIFEST.json'), exact_closures=len(inputs['closures']),
    unique_checked_members=len(checked), unique_checked_bytes=sum(x['bytes'] for x in checked.values()),
    complete_typed_JSON_or_JSONL_members=len(parsed), exact_negative_inputs=negative,
    preparation_authored_members=15, dependencies=2797, complete_patch_reconstructed_byte_exact=True,
    root_complete_five_sources_contract_checklist_scientific_scope_full_draft_bindings_read=True,
    proposed_helpers_imported_or_executed=False, source_only=True, new_substantive_attempts=0, audit_turns=0,
    scope='Administrative source review only. Earlier genuine root math/current/whole reading remains separately bound. Fresh actual reconciliation and remote/native acceptance still pending.')
destination = A / 'ROOT_ACCEPTANCE_PREPARATION_INSPECTION.json'
with destination.open('x') as stream:
    json.dump(result, stream, indent=2, sort_keys=True)
    stream.write('\n')
print(json.dumps(dict(status='PASS', unique_members=len(checked), bytes=result['unique_checked_bytes'], negative_inputs=len(negative), inspection=pin(destination))))
