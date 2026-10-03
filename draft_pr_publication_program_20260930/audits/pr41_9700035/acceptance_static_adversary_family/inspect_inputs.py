#!/usr/bin/env python3
"""Independent byte/schema/topology inspection; never loads reviewed Python code."""
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat

OWN = Path(__file__).resolve().parent
A = OWN.parent
R = A.parents[2]
P = A / 'acceptance_preparation_family'
C = A / 'reviewed_candidate'
EXPECTED = '6e8d07a73f68177ae3b7f446a1416ae39eabd560352fd7685464bcb129d0bcdc'
READ = {}
NODES = []
FOREIGN = {}


def demand(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(rr):
        obj = {}
        for key, value in rr:
            demand(key not in obj, 'duplicate JSON key')
            obj[key] = value
        return obj
    def floating(value):
        x = float(value)
        demand(math.isfinite(x), 'nonfinite decoded number')
        return x
    return json.loads(raw, object_pairs_hook=pairs, parse_float=floating,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def safe(name):
    demand(type(name) is str and name and '\\' not in name and '\0' not in name,
           'bad relative name')
    p = PurePosixPath(name)
    demand(not p.is_absolute() and p.as_posix() == name and
           not {'.', '..', '.git', '__pycache__'}.intersection(p.parts), 'unsafe name')


def walk(obj, filename, pointer=''):
    kind = type(obj).__name__
    row = {'file': filename, 'pointer': pointer, 'type': kind}
    if type(obj) is dict:
        row['complete_keys'] = list(obj)
    elif type(obj) is list:
        row['length'] = len(obj)
    elif type(obj) is str:
        # Avoid duplicating archival/source bodies. Full bytes were read and bound.
        row['utf8_bytes'] = len(obj.encode())
        row['value_sha256'] = sha(obj.encode())
    else:
        row['value'] = obj
    NODES.append(row)
    if type(obj) is dict:
        for key, value in obj.items():
            walk(value, filename, pointer + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif type(obj) is list:
        for i, value in enumerate(obj):
            walk(value, filename, pointer + '/' + str(i))


def read(path, foreign=False):
    path = Path(path)
    demand(path.is_file() and not path.is_symlink() and
           all(not q.is_symlink() for q in path.parents), 'unsafe bound file')
    demand(stat.S_ISREG(path.stat().st_mode), 'nonregular file')
    raw = path.read_bytes()
    name = path.relative_to(R).as_posix()
    if name not in READ:
        READ[name] = {'path': name, 'bytes': len(raw), 'sha256': sha(raw),
                      'worktree_mode': path.stat().st_mode & 0o7777}
        if foreign:
            FOREIGN[name] = READ[name]
        elif path.suffix == '.json':
            walk(parse(raw), name)
        elif path.suffix == '.jsonl':
            demand(not raw or raw.endswith(b'\n'), 'incomplete JSONL')
            for i, line in enumerate(raw.splitlines()):
                walk(parse(line), name, '/line/' + str(i))
    return raw


def verify_rows(base, rr, foreign=False):
    demand(type(rr) is list and len({z['path'] for z in rr}) == len(rr), 'duplicate rows')
    for z in rr:
        safe(z['path'])
        n = z['bytes'] if 'bytes' in z else z['size']
        demand(type(n) is int and n >= 0, 'untyped size')
        raw = read(base / z['path'], foreign)
        demand(len(raw) == n and sha(raw) == z['sha256'], 'full row differs: ' + z['path'])


def exact(base, names, mode=None):
    files, directories = set(), set()
    demand(base.is_dir() and not base.is_symlink(), 'unsafe base')
    for q in base.rglob('*'):
        name = q.relative_to(base).as_posix()
        safe(name)
        demand(not q.is_symlink(), 'symlink closure')
        if q.is_dir():
            directories.add(name)
        else:
            demand(q.is_file() and stat.S_ISREG(q.stat().st_mode), 'special closure')
            files.add(name)
            if mode is not None:
                demand(q.stat().st_mode & 0o7777 == mode, 'exact permission differs')
    expected_dirs = {q.as_posix() for n in names for q in PurePosixPath(n).parents
                     if q.as_posix() != '.'}
    demand(files == names and directories == expected_dirs, 'recursive membership differs')
    return {'files': sorted(files), 'directories': sorted(directories)}


def put(name, obj):
    path = OWN / name
    with path.open('x') as out:
        json.dump(obj, out, ensure_ascii=False, indent=2)
        out.write('\n')


def main():
    beginning = read(P / 'PREPARATION_MANIFEST.json')
    demand(sha(beginning) == EXPECTED, 'closed source pin differs')
    preparation = parse(beginning)
    demand(preparation['self_excluded'] == ['PREPARATION_MANIFEST.json'] and
           type(preparation['files_count']) is int and preparation['files_count'] == 35 and
           len(preparation['files']) == 35, 'exact35+self preparation')
    verify_rows(P, preparation['files'])
    topology = {'acceptance_preparation': exact(P, {z['path'] for z in preparation['files']} |
                                               {'PREPARATION_MANIFEST.json'}, 0o444)}
    inputs = parse(read(P / 'INPUT_BINDINGS.json'))
    for row in inputs['pins'].values():
        verify_rows(R, [row])
    for closure in inputs['closures']:
        base = A / closure['directory']
        raw = read(base / closure['manifest_name'])
        demand(sha(raw) == closure['manifest_sha256'], 'input manifest differs')
        verify_rows(base, closure['members'])
        verify_rows(base, closure['foreign_members'], foreign=True)
        topology[closure['directory']] = exact(base,
            {z['path'] for z in closure['members'] + closure['foreign_members']} |
            {closure['manifest_name']})
    current = parse(read(C / 'MANIFEST.json'))
    demand(sha((C / 'MANIFEST.json').read_bytes()) ==
           '3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa' and
           len(current['files']) == 547, 'frozen current changed')
    verify_rows(C, current['files'])
    topology['reviewed_candidate'] = exact(C, {z['path'] for z in current['files']} |
                                           {'MANIFEST.json'}, 0o444)
    deps = parse(read(C / 'CURRENT_PROOF_DEPENDENCIES.json'))
    demand(len(deps['files']) == 469 and sha((C / 'CURRENT_PROOF_DEPENDENCIES.json').read_bytes()) ==
           'ade2f6fe9890f1038810158a284f4a8924e34d6d2f95b3a07654d78fa6501ff6', 'deps changed')
    verify_rows(A, deps['files'])
    whole_row = inputs['whole_observed_only']
    verify_rows(R, [whole_row])
    W = (R / whole_row['path']).parent
    whole = parse(read(W / 'FIRST_PARTY_MANIFEST.json'))
    demand(len(whole['files']) == 143 and len(whole['foreign_files']) == 17, 'whole143+17')
    verify_rows(W, whole['files'])
    verify_rows(W, whole['foreign_files'], foreign=True)
    topology['whole_current_source_first_family'] = exact(W,
        {z['path'] for z in whole['files'] + whole['foreign_files']} |
        {'FIRST_PARTY_MANIFEST.json'}, 0o444)
    verify_rows(R, [inputs['root_whole_observed']])
    root = parse(read(R / inputs['root_whole_observed']['path']))
    demand(root['whole_independent_verdict'] == parse(read(W / 'RESULT.json')), 'root whole mismatch')
    snap = parse(read(A / 'snapshot_manifest.json'))
    demand(len(snap['files']) == 16 and len(snap['changed_paths']) == 17, 'original16/17')
    verify_rows(A / 'source_snapshot', snap['files'])
    topology['source_snapshot'] = exact(A / 'source_snapshot', {z['path'] for z in snap['files']})
    raw_diff = read(A / 'pr_input/diff.patch')
    demand(len(raw_diff) == 201709 and len([x for x in raw_diff.splitlines()
            if x.startswith(b'diff --git ')]) == 17, 'complete original diff')
    demand(read(P / 'PREPARATION_MANIFEST.json') == beginning, 'preparation changed during audit')
    verify_rows(P, preparation['files'])
    exact(P, {z['path'] for z in preparation['files']} | {'PREPARATION_MANIFEST.json'}, 0o444)
    put('READ_LEDGER.json', {'files': sorted(READ.values(), key=lambda z: z['path']),
                            'unique_full_files': len(READ),
                            'full_bytes': sum(z['bytes'] for z in READ.values())})
    put('INPUT_TOPOLOGY.json', topology)
    put('FOREIGN_DEPENDENCIES.json', {'individual_files': sorted(FOREIGN.values(), key=lambda z: z['path']),
                                    'foreign_bodies_copied': False,
                                    'authorship_asserted': False,
                                    'prefix_exclusions': []})
    with (OWN / 'COMPLETE_TYPED_NODES.jsonl').open('x') as out:
        for row in NODES:
            out.write(json.dumps(row, ensure_ascii=False) + '\n')
    status = {'status': 'PASS_INDEPENDENT_STATIC_INPUT_BINDING_INSPECTION',
              'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid': os.getpid(),
              'preparation_manifest_sha256': EXPECTED, 'preparation_members': 35,
              'current_members': 547, 'dependency_members': 469,
              'whole_authored_members': 143, 'whole_foreign_members': 17,
              'unique_full_files': len(READ), 'full_bytes': sum(z['bytes'] for z in READ.values()),
              'typed_nodes': len(NODES), 'foreign_individual_dependencies': len(FOREIGN),
              'proposed_helpers_imported_compiled_or_executed': False,
              'scientific_reexecution_claimed': False, 'future_runtime_gates_certified': False,
              'writes_outside_own_family': False, 'original_substantive_attempts': 2,
              'new_substantive_attempts': 0, 'audit_turns': 0}
    put('INPUT_INSPECTION_RESULT.json', status)
    print(json.dumps(status, indent=2))


if __name__ == '__main__':
    main()
