#!/usr/bin/env python3
"""Independent read-only data inspection; never imports any reviewed program.

Only this source's standard-library implementation runs. Inputs are read as
bytes, strict JSON or Python AST, never as executable Python. No Git or SQL
query, subprocess, network operation, or output mutation is performed here.
The launching wrapper retains this source and both complete output streams.
"""
import ast
import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath

ROOT = Path('/Users/alec/Documents/Math')
AUDIT = ROOT / 'draft_pr_publication_program_20260930/audits/pr40_2814'
PREP = AUDIT / 'acceptance_preparation_family'
PREP_SHA = 'a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b'
json_reads = {}
byte_reads = {}


def demand(condition, explanation):
    if not condition:
        raise AssertionError(explanation)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    path = Path(path)
    demand(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), 'Not regular: ' + str(path))
    raw = path.read_bytes()
    byte_reads[path.relative_to(ROOT).as_posix()] = {'bytes': len(raw), 'sha256': sha(raw)}
    return raw


def strict(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            demand(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def finite(token):
        raise ValueError('Nonfinite JSON: ' + token)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=finite)


def types(value):
    if type(value) is dict:
        return {key: types(item) for key, item in value.items()}
    if type(value) is list:
        return [types(item) for item in value]
    return type(value).__name__


def load(path):
    raw = read(path)
    value = strict(raw)
    json_reads[Path(path).relative_to(ROOT).as_posix()] = {
        'whole_value_type': type(value).__name__,
        'whole_recursive_typed_structure_sha256': sha(json.dumps(types(value), sort_keys=True).encode()),
    }
    return value


def rel(name):
    demand(type(name) is str and bool(name) and '\\' not in name and '\0' not in name, 'Invalid relative path')
    p = PurePosixPath(name)
    demand(not p.is_absolute() and '..' not in p.parts and p.as_posix() == name and name != '.', 'Noncanonical path')
    return name


def members(rows):
    demand(type(rows) is list, 'Manifest rows must be list')
    names = set()
    for row in rows:
        demand(type(row) is dict, 'Manifest row must be object')
        name = rel(row['path'])
        demand(name not in names, 'Duplicate member')
        names.add(name)
        size = row.get('bytes', row.get('size'))
        demand(type(size) is int and size >= 0, 'Typed nonnegative size')
        digest = row['sha256']
        demand(type(digest) is str and len(digest) == 64 and all(c in '0123456789abcdef' for c in digest), 'Digest')
    return names


def bind(base, rows):
    members(rows)
    for row in rows:
        path = base / row['path']
        raw = read(path)
        demand(len(raw) == row.get('bytes', row.get('size')) and sha(raw) == row['sha256'], 'Bound bytes differ: ' + str(path))
        if path.suffix == '.json':
            load(path)
        elif path.suffix == '.jsonl':
            for line in raw.splitlines():
                strict(line)


def topology(base, names, excluded=()):
    """Exclude only declared top-level trees; exact root self is in names."""
    actual_files, actual_dirs = set(), set()
    for walkroot, dirs, files in os.walk(base, followlinks=False):
        here = Path(walkroot)
        if here == base:
            dirs[:] = [n for n in dirs if n not in excluded]
        for name in dirs + files:
            p = here / name
            mode = p.lstat().st_mode
            demand(not stat.S_ISLNK(mode), 'Symlink rejected')
            n = p.relative_to(base).as_posix()
            if stat.S_ISDIR(mode):
                actual_dirs.add(n)
            else:
                demand(stat.S_ISREG(mode), 'Special file rejected')
                actual_files.add(n)
    expected_dirs = {p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    demand(actual_files == set(names), 'Exact recursive file set: ' + str(base))
    demand(actual_dirs == expected_dirs, 'Exact recursive directory set: ' + str(base))
    return {'files': len(actual_files), 'directories': len(actual_dirs), 'excluded_root_directories': list(excluded)}


def typed_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(typed_equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def main():
    prep = load(PREP / 'PREPARATION_MANIFEST.json')
    demand(sha(read(PREP / 'PREPARATION_MANIFEST.json')) == PREP_SHA, 'Pinned source preparation')
    demand(prep['status'] == 'CLOSED_SOURCE_ONLY' and prep['files_count'] == 12, 'Source-only closure')
    bind(PREP, prep['files'])
    closures = [{'root': PREP.relative_to(ROOT).as_posix(), **topology(PREP, members(prep['files']) | {'PREPARATION_MANIFEST.json'})}]
    source_rows = []
    for row in prep['files']:
        if row['path'].endswith('.py'):
            raw = read(PREP / row['path'])
            tree = ast.parse(raw.decode(), filename=row['path'])
            source_rows.append({**row, 'lines': len(raw.splitlines()), 'AST_parsed_without_import_compile_or_execution': True,
                                'functions': [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]})
    demand(len(source_rows) == 5 and sum(r['lines'] for r in source_rows) == 632, 'All five whole sources')
    inputs = load(PREP / 'INPUT_BINDINGS.json')
    demand(len(inputs['pins']) == 10, 'Ten whole pinned inputs')
    bind(ROOT, list(inputs['pins'].values()))
    actual_counts = []
    for c in inputs['closures']:
        base = ROOT / c['root']
        if c['manifest'] is not None:
            bind(ROOT, [c['manifest']])
            obj = load(ROOT / c['manifest']['path'])
            rows = obj[c['member_field']]
            demand(len(rows) == c['authored_count_excluding_self'], 'Pinned family size')
            self_name = Path(c['manifest']['path']).name
        else:
            rows, self_name = c['files'], None
            actual_counts.append(len(rows))
        bind(base, rows)
        names = members(rows) | ({self_name} if self_name else set())
        closures.append({'root': c['root'], **topology(base, names, c['excluded_root_directories'])})
    demand(actual_counts == [4, 6, 36], 'All four freeze plus42 original/family retained members')
    original_foreign = load(AUDIT / 'current_preparation_family/INPUT_PINS.json')['foreign_inventory']
    demand(set(original_foreign) == {'primary_scope_family/foreign_cache', 'geodesic_geometry_family/primary'}, 'Exact original foreign roots')
    foreign_count = 0
    for n, v in original_foreign.items():
        bind(AUDIT / n, v['members'])
        topology(AUDIT / n, members(v['members']))
        foreign_count += len(v['members'])
    whole = AUDIT / 'whole_current_source_first_family'
    foreign_rows = load(whole / 'FOREIGN_PRIMARY_INVENTORY.json')['exact_recursive_inventory']
    demand(len(foreign_rows) == 21 and all(PurePosixPath(z['path']).parts[0] == 'ROOTforeign_primary' for z in foreign_rows), 'Exact21 separately qualified foreign')
    bind(whole, foreign_rows)
    whole_manifest = load(whole / 'FIRST_PARTY_MANIFEST.json')
    topology(whole, members(whole_manifest['files']) | members(foreign_rows) | {'FIRST_PARTY_MANIFEST.json'})
    current = AUDIT / 'reviewed_candidate'
    cm = load(current / 'MANIFEST.json')
    demand(cm['files_count'] == 239 and len(cm['files']) == 239, 'Current239')
    bind(current, cm['files'])
    current_topology = topology(current, members(cm['files']) | {'MANIFEST.json'})
    demand(all((current / n).stat().st_mode & 0o777 == 0o444 for n in members(cm['files']) | {'MANIFEST.json'}), 'Current240 readonly')
    current_json = sum(Path(z['path']).suffix == '.json' for z in cm['files'])
    demand(current_json == 109, '109 member JSON plus self110')
    deps = load(current / 'CURRENT_PROOF_DEPENDENCIES.json')
    demand(len(deps['files']) == 216 and deps['dependency_anchor_repository_relative'] == AUDIT.relative_to(ROOT).as_posix(), 'All216 exact dependency anchor')
    bind(AUDIT, deps['files'])
    snap = load(AUDIT / 'snapshot_manifest.json')
    demand(len(snap['files']) == 13 and len(snap['changed_paths']) == 14, 'Original13/diff14 retained source identities')
    bind(AUDIT / 'source_snapshot', snap['files'])
    original_sha = {}
    for row in snap['files']:
        n = row['path']
        frozen = read(AUDIT / 'source_snapshot' / n)
        demand(frozen == read(current / n) == read(current / 'original_archive' / n), 'Whole root/archive/original exact')
        original_sha[n] = sha(frozen)
    ledger = load(current / 'turns.json')
    demand(type(ledger['id']) is int and ledger['id'] == 2814 and type(ledger['count']) is int and ledger['count'] == 0 and ledger['substantive_attempts'] == [], 'Typed zero original ledger')
    demand(load(current / 'prior_report.json') is None, 'Literal null primary prior')
    duplicate = load(current / 'duplicate_prior_report.json')
    demand(type(duplicate) is dict and bool(duplicate), 'Complete duplicate prior preserved')
    draft = load(PREP / 'DRAFT_FINAL_PLAN.json')
    scope = load(PREP / 'SCIENTIFIC_SCOPE.json')
    demand(typed_equal(draft['scientific_scope'], scope), 'Full bad scope propagation begins in draft')
    demand(all(draft[k] is False for k in ['root_full_current_read_completed', 'root_full_whole_read_completed', 'independent_whole_current_pass', 'science_reexecution_of_current', 'historical_PASS_transferred', 'full_problem_solved', 'novelty_claimed', 'paper_or_new_doi_or_tracker']), 'No fabricated actual/final gate')
    demand(draft['preparation_manifest_sha256'] is None, 'Draft preparation pin pending')
    demand(all(draft[k] is None for k in ['current_model', 'current_reasoning_effort', 'current_deadline_utc']), 'Runtime nulls')
    for name in ['acceptance.json', 'status.json', 'attempt.json', 'current_readiness.json']:
        obj = load(current / name)
        demand(obj['new_whole_current_gate'] == 'PENDING' and obj['status'] == 'UNSOLVED' and obj['source_hold'] is True, 'Frozen current pending source hold')
        demand(obj['current_model'] is None and obj['current_reasoning_effort'] is None and obj['current_deadline_utc'] is None, 'Current runtime nulls')
    mirror = ROOT / 'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py'
    mirror_raw = read(mirror)
    demand(sha(mirror_raw) == 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f', 'Complete native driver pin')
    ast.parse(mirror_raw.decode(), filename=mirror.name)
    result = {
        'schema': 'pr40-independent-acceptance-static-input-inspection/v1',
        'status': 'PASS_INPUT_IDENTITY_AND_TYPED_TOPOLOGY_ONLY',
        'scientific_acceptance_status': 'REVISION_REQUIRED_SEPARATE_SCOPE_FINDING',
        'proposed_or_old_verifier_imports_or_executions': False,
        'Git_SQL_native_shared_remote_writes_or_queries': False,
        'all_five_whole_proposed_sources': source_rows,
        'source_lines': 632,
        'closures': closures,
        'current_topology': current_topology,
        'current_member_JSON_count': current_json,
        'current_JSON_count_including_exact_root_manifest': current_json + 1,
        'dependencies': 216,
        'actual_original_and_family_capture_members': 42,
        'actual_current_freeze_capture_members': 4,
        'original_foreign_bytes_rehashed_not_new_proof_reading': foreign_count,
        'whole_separately_qualified_foreign_members': 21,
        'original_root_archive_source_complete_sha256': original_sha,
        'strict_JSON_whole_recursive_typed_structures': json_reads,
        'every_complete_file_read': byte_reads,
        'current_239_and_old_sources_unchanged': True,
        'original_substantive_attempts': 0, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
        'future_actual_prior39_native_and_remote_status_not_invented': True,
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
