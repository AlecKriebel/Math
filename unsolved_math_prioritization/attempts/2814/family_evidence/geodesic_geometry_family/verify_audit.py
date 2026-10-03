#!/usr/bin/env python3
"""Read-only exact closure/input/control verifier for this scientific family.

Run with python3 -B. Never executes submitted helpers or reads live Git state.
"""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parent
MANIFEST = 'ARTIFACT_MANIFEST.json'
SCHEMA = 'pr40-geodesic-authored-family/v1'
SNAPSHOT_SHA = '781f7df1f6a2e3d8e5041b555097f1765a44c1e2080c034971fd802d65e332d5'
HEAD = '163e34d566d6cbaee3a2a8fdc6394fbb9e49a539'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, 'Duplicate JSON key: '+key)
        value[key] = item
    return value


def load(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON '+value)))


def path_ok(value):
    require(type(value) is str and bool(value) and not value.startswith('/'), 'Invalid path type/absolute path')
    p = PurePosixPath(value)
    require(str(p) == value and not any(c in ('.', '..', '') for c in value.split('/')), 'Noncanonical path')
    require('\\' not in value, 'Backslash path forbidden')
    return value


def row(path, base):
    require(path.is_file() and not path.is_symlink(), 'Expected regular nonsymlink member')
    data = path.read_bytes()
    return {'path': path.relative_to(base).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def typed_rows(rows):
    require(type(rows) is list, 'Rows must be a list')
    paths = []
    for entry in rows:
        require(type(entry) is dict and set(entry) == {'path', 'bytes', 'sha256'}, 'Exact row fields required')
        paths.append(path_ok(entry['path']))
        require(type(entry['bytes']) is int and entry['bytes'] >= 0, 'Byte count must be nonnegative integer')
        digest = entry['sha256']
        require(type(digest) is str and len(digest) == 64 and all(c in '0123456789abcdef' for c in digest), 'Invalid SHA256')
    require(paths == sorted(set(paths)), 'Rows must be sorted and unique')
    return rows


def walk(base):
    files, dirs = [], []
    require(base.is_dir() and not base.is_symlink(), 'Invalid root')
    for p in sorted(base.rglob('*')):
        require(not p.is_symlink(), 'Symlink anywhere in closure: '+p.relative_to(base).as_posix())
        if p.is_dir():
            dirs.append(p.relative_to(base).as_posix())
        else:
            require(p.is_file(), 'Nonregular member')
            files.append(p)
    return files, dirs


def validate_closure(base):
    manifest = load(base / MANIFEST)
    require(manifest['schema'] == SCHEMA, 'Wrong closure schema')
    require(type(manifest['root_name']) is str and manifest['root_name'] == base.name, 'Wrong family root')
    require(manifest['self_excluded_paths'] == [MANIFEST], 'Only root manifest may self-exclude')
    require(manifest['foreign_excluded_prefixes'] == ['primary/'], 'Only exact rooted primary foreign prefix allowed')
    require(manifest['bytecode_excluded_components'] == [], 'No bytecode exclusions in exact closure')
    require(manifest['foreign_inventory_path'] == 'FOREIGN_PRIMARY_INVENTORY.json', 'Wrong foreign inventory location')
    members = typed_rows(manifest['members'])
    require(MANIFEST not in [e['path'] for e in members], 'Manifest improperly includes itself')
    files, dirs = walk(base)
    authored = [p for p in files if p.relative_to(base).as_posix() != MANIFEST and not p.relative_to(base).as_posix().startswith('primary/')]
    require(members == [row(p, base) for p in authored], 'Authored bytes/file inventory mismatch')
    expected_dirs = [s for s in dirs if s != 'primary' and not s.startswith('primary/')]
    require(manifest['directories'] == expected_dirs, 'Authored directory inventory mismatch')
    inventory = load(base / 'FOREIGN_PRIMARY_INVENTORY.json')
    require(inventory['foreign_prefix'] == 'primary/', 'Wrong foreign inventory root')
    foreign = typed_rows(inventory['members'])
    require(all(e['path'].startswith('primary/') for e in foreign), 'Foreign path escapes rooted primary')
    actual_foreign = [row(p, base) for p in files if p.relative_to(base).as_posix().startswith('primary/')]
    require(foreign == actual_foreign, 'Foreign bytes/file inventory mismatch')
    require(inventory['directories'] == [s for s in dirs if s == 'primary' or s.startswith('primary/')], 'Foreign directory inventory mismatch')
    for p in authored:
        if p.suffix == '.json':
            load(p)
    return manifest


def validate_inputs(base):
    coverage = load(base / 'SOURCE_AND_READ_COVERAGE.json')
    require(coverage['original_head'] == HEAD, 'Head binding mismatch')
    outer = base.parent
    snapshot_path = outer / 'snapshot_manifest.json'
    require(hashlib.sha256(snapshot_path.read_bytes()).hexdigest() == SNAPSHOT_SHA, 'Frozen snapshot manifest drift')
    snapshot = load(snapshot_path)
    require(snapshot['head'] == HEAD and snapshot['pr'] == 40 and snapshot['problem'] == '2814', 'Frozen source identity mismatch')
    actual = []
    source_root = outer / 'source_snapshot'
    source_files, source_dirs = walk(source_root)
    require(len(snapshot['files']) == 13 and len(snapshot['changed_paths']) == 14, 'Wrong original member/path count')
    for entry in snapshot['files']:
        path_ok(entry['path'])
        p = source_root / entry['path']
        actual_row = row(p, source_root)
        require(actual_row['bytes'] == entry['size'] and actual_row['sha256'] == entry['sha256'], 'Original source drift')
        data = p.read_bytes()
        object_header = ('blob '+str(len(data))+'\0').encode()
        require(hashlib.sha1(object_header+data).hexdigest() == entry['git_blob'], 'Declared original blob does not match bytes')
        require(entry['mode'] == '100644', 'Unexpected declared source mode')
        actual.append(actual_row)
    actual.sort(key=lambda e: e['path'])
    require(actual == coverage['original_source_members'], 'Source coverage binding drift')
    require(actual == [row(p, source_root) for p in source_files], 'Original source exact closure mismatch')
    require(source_dirs == ['review'], 'Original source directory closure mismatch')
    diff = outer / 'pr_input' / 'diff.patch'
    data = diff.read_bytes()
    require(len(data) == snapshot['diff_bytes'] and hashlib.sha256(data).hexdigest() == snapshot['diff_sha256'], 'Original retained diff drift')
    require(load(source_root / 'prior_report.json') is None, 'Literal prior no longer null')
    turns = load(source_root / 'turns.json')
    require(type(turns['substantive_attempts']) is list and turns['substantive_attempts'] == [], 'Original attempt ledger drift')
    budget = load(base / 'BUDGET_AND_DISPOSITION.json')
    for key in ['original_substantive_attempts', 'new_substantive_attempts', 'verification_attempts_added']:
        require(key in budget and type(budget[key]) is int and budget[key] == 0, 'Budget value/type mismatch')
    require(type(budget['max_substantive_attempts']) is int and budget['max_substantive_attempts'] == 5, 'Maximum budget drift')
    require(budget['full_problem_solved'] is False and budget['new_mathematical_result_claimed'] is False, 'Unqualified scientific promotion')
    require(budget['disposition'] == 'PASS_SOURCE_STATUS_WITH_EXPLICIT_PROOF_QUALIFICATIONS', 'Disposition drift')
    seal = load(base / 'SOURCE_FIRST_SEAL.json')
    proof = base / seal['proof_claim']['path']
    require(row(proof, base) == seal['proof_claim'], 'Source-first claim drift')
    require(hashlib.sha256((base / 'SOURCE_FIRST_SEAL.json').read_bytes()).hexdigest() == 'ae15b43d946519695729b07e328070077d1ac30e25c19182539d00a0285f7000', 'Source-first seal drift')
    for source in coverage['primary_sources']:
        require(source['foreign_import'] is True, 'Primary wrongly authored')
        for key in ['pdf', 'extracted_text']:
            entry = source[key]
            require(row(base / entry['path'], base) == entry, 'Primary source binding drift')
        receipt = load(base / source['acquisition_receipt'])
        require(receipt['http_status'] == 200 and receipt['extract_exit'] == 0 and 'failure' not in receipt, 'Primary acquisition not successful')
        require(receipt['sha256'] == source['pdf']['sha256'] and receipt['bytes'] == source['pdf']['bytes'], 'Primary receipt PDF drift')
        require(receipt['text_sha256'] == source['extracted_text']['sha256'] and receipt['text_bytes'] == source['extracted_text']['bytes'], 'Primary receipt text drift')
    run = subprocess.run([sys.executable, '-B', str(base / 'geometric_controls.py')], capture_output=True)
    require(run.returncode == 0, 'Own geometric controls failed')
    require(run.stdout == (base / 'receipts' / 'geometric_controls.stdout.json').read_bytes(), 'Retained own control stdout mismatch')
    require(run.stderr == (base / 'receipts' / 'geometric_controls.stderr').read_bytes(), 'Retained own control stderr mismatch')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--closure-only', action='store_true')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        validate_closure(args.root)
        if not args.closure_only:
            require(args.root.resolve() == ROOT, 'Full verification restricted to actual family')
            validate_inputs(args.root)
        print(json.dumps({'status':'PASS','scope':'Exact authored/foreign closure'+(' only' if args.closure_only else ', frozen13 source/diff bindings and exact geometric controls'),
                          'submitted_code_executed':False,'live_git_state_checked':False}, sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},sort_keys=True))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
