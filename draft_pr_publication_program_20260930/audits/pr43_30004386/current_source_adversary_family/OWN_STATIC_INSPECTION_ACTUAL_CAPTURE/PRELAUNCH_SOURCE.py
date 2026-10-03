#!/usr/bin/env python3
"""Independent whole-byte static inspector. No candidate import/compile/execution.

Writes only this adversary's dedicated family. Inputs are read as bytes or strict
JSON; candidate Python text is never parsed as executable code. Two actual Git
children query branch/HEAD only, with their full truthful streams retained here.
"""
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess

F = Path(__file__).absolute().parent
A = F.parent
R = A.parents[2]
P = A / 'current_preparation_family'
inputs = {}
trees = []
checks = []


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def require(ok, label):
    if not ok:
        raise ValueError(label)
    checks.append(label)


def strict(raw):
    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def bad(value):
        raise ValueError('nonfinite JSON constant ' + value)
    def floating(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError('nonfinite JSON float')
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad, parse_float=floating)


def canonical(name):
    p = PurePosixPath(name)
    require(type(name) is str and name and '\\' not in name and not p.is_absolute()
            and p.as_posix() == name and not {'.', '..', '.git', '__pycache__'}.intersection(p.parts),
            'canonical path: ' + name)
    return name


def read(path, role):
    require(not path.is_symlink() and all(not p.is_symlink() for p in path.parents),
            'nonsymlink input: ' + str(path))
    mode = path.stat().st_mode
    require(stat.S_ISREG(mode), 'regular input: ' + str(path))
    raw = path.read_bytes()
    name = path.relative_to(R).as_posix()
    item = dict(path=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                full_stat_S_IMODE=format(stat.S_IMODE(mode), '05o'), roles=[role])
    if name in inputs:
        previous = inputs[name]
        require(all(previous[key] == item[key] for key in ['path', 'bytes', 'sha256', 'full_stat_S_IMODE']),
                'repeat input exact: ' + name)
        item['roles'] = sorted(set(previous['roles'] + item['roles']))
    inputs[name] = item
    if path.suffix == '.json':
        strict(raw)
    elif path.suffix == '.jsonl':
        for line in raw.splitlines():
            require(bool(line.strip()), 'nonblank JSONL line: ' + name)
            strict(line)
    return raw


def bind(root, item, role):
    require(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'}
            and type(item['bytes']) is int and item['bytes'] >= 0,
            'typed pin row: ' + str(item.get('path')))
    raw = read(root / canonical(item['path']), role)
    require(len(raw) == item['bytes'] and hashlib.sha256(raw).hexdigest() == item['sha256'],
            'whole-byte pin: ' + item['path'])
    return raw


def tree(root, expected):
    require(root.is_dir() and not root.is_symlink(), 'regular tree root: ' + str(root))
    files, directories = [], []
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(), 'tree nonsymlink: ' + str(p))
        mode = p.stat().st_mode
        entry = dict(path=p.relative_to(root).as_posix(), full_stat_S_IMODE=format(stat.S_IMODE(mode), '05o'))
        if stat.S_ISREG(mode):
            files.append(entry)
        else:
            require(stat.S_ISDIR(mode), 'tree regular directory: ' + str(p))
            directories.append(entry)
    require({x['path'] for x in files} == set(expected), 'exact files: ' + str(root))
    wanted = {p.as_posix() for name in expected for p in PurePosixPath(name).parents if p.as_posix() != '.'}
    require({x['path'] for x in directories} == wanted, 'exact directories: ' + str(root))
    trees.append(dict(root=root.relative_to(R).as_posix(), root_full_stat_S_IMODE=format(stat.S_IMODE(root.stat().st_mode), '05o'),
                      files=files, directories=directories))


def write(name, obj):
    with (F / name).open('x') as handle:
        json.dump(obj, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')


require(F.name == 'current_source_adversary_family' and R == Path('/Users/alec/Documents/Math'), 'own exact anchor')
require(not (A / 'reviewed_candidate').exists() and not (A / 'reviewed_candidate').is_symlink(), 'candidate absent before own inspection')
prepraw = read(P / 'PREPARATION_MANIFEST.json', 'attributed closed preparation self-manifest')
require(hashlib.sha256(prepraw).hexdigest() == 'bbf269401514530da541500ee2f43e03cfd4514fab65c2a34193283e11b6fcc7', 'requested preparation seal')
prep = strict(prepraw)
require(prep['files_count'] == 38 and type(prep['files_count']) is int and prep['self_excluded'] == ['PREPARATION_MANIFEST.json'], 'exact38own+self')
for row in prep['files']:
    bind(P, row, 'attributed preparation own source/document/control/capture')
tree(P, [row['path'] for row in prep['files']] + ['PREPARATION_MANIFEST.json'])
pins = strict(read(P / 'INPUT_PINS.json', 'operative fixed-input contract'))
snapshot = strict(bind(A, pins['snapshot_manifest'], 'attributed original16 snapshot manifest'))
for row in snapshot['files']:
    raw = bind(A / 'source_snapshot', dict(path=row['path'], bytes=row['size'], sha256=row['sha256']), 'attributed immutable original scientific/source/result')
    require(stat.S_IMODE((A / 'source_snapshot' / row['path']).stat().st_mode) == 0o444, 'original full0444: ' + row['path'])
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(blob == row['git_blob'] and row['mode'] == '100644', 'original Git blob and declared mode: ' + row['path'])
tree(A / 'source_snapshot', [row['path'] for row in snapshot['files']])
diff = read(A / 'original_diff.patch', 'attributed complete original17 diff')
require(len(diff) == snapshot['diff_bytes'] == 54344 and hashlib.sha256(diff).hexdigest() == snapshot['diff_sha256']
        and len(diff.splitlines()) == 957 and diff.count(b'diff --git ') == 17, 'whole957line17path diff pin')
for info in pins['retained_closures']:
    root = A / canonical(info['directory'])
    for row in info['files']:
        bind(root, row, 'attributed ROOT retained source/result/capture')
    tree(root, [row['path'] for row in info['files']])
for row in pins['auxiliary']:
    bind(A, row, 'attributed ROOT auxiliary source/record')
for row in pins['root_foreign_members']:
    bind(A / 'foreign_primary', row, 'foreign primary or derivative; hash-bound only; not copied')
tree(A / 'foreign_primary', [row['path'] for row in pins['root_foreign_members']])
for name, info in pins['families'].items():
    root = A / canonical(name)
    manifest = strict(bind(root, info['manifest'], 'attributed independent family closure control'))
    for row in info['copied_members']:
        bind(root, row, 'attributed independent family first-party audit artifact; no novelty')
    for row in info['foreign_members']:
        bind(root, row, 'foreign primary or derivative; hash-bound only; not copied')
    names = [row['path'] for row in info['copied_members'] + info['foreign_members']] + [info['manifest']['path']]
    require(len(names) == len(set(names)), 'disjoint unique family membership: ' + name)
    tree(root, names)
    if name == 'compactness_source_family':
        require(len(info['copied_members']) == 18 and len(info['foreign_members']) == 8
                and manifest['first_party_files'] == info['copied_members']
                and [{k: row[k] for k in ['path', 'bytes', 'sha256']} for row in manifest['foreign_individually_excluded']] == info['foreign_members'], 'compactness exact18own8foreign')
    else:
        require(name == 'probability_source_family' and len(info['copied_members']) == 43 and len(info['foreign_members']) == 23,
                'probability exact43own23foreign')
        for category, listed in [('first_party_audit_artifact', info['copied_members']), ('foreign_primary_or_access_evidence', info['foreign_members'])]:
            require([{k: row[k] for k in ['path', 'bytes', 'sha256']} for row in manifest['files'] if row['classification'] == category] == listed,
                    'probability exact category: ' + category)
inspection = strict(read(A / 'ROOT_CLOSED_EVIDENCE_INSPECTION.json', 'attributed ROOT complete inspection'))
for key, root, self_name in [('closed_reproduction', 'root_original_actual_reproduction', 'MANIFEST.json'),
                              ('compactness_family', 'compactness_source_family', 'OWNERSHIP_MANIFEST.json'),
                              ('probability_family', 'probability_source_family', 'SELF_MANIFEST.json')]:
    require(inspection[key]['complete_manifest'] == strict(read(A / root / self_name, 'attributed actual closure control')),
            'handoff complete manifest matches actual: ' + key)
require(inspection['entire_reproduction_result'] == strict(read(A / 'root_original_actual_reproduction/RESULT.json', 'attributed genuine reproduction result'))
        and inspection['entire_actual_runs'] == strict(read(A / 'root_original_actual_reproduction/ACTUAL_RUNS.json', 'attributed actual run index')), 'handoff full result/run equality')
builder = read(P / 'prepare_current_packet.py', 'operative source-only builder')
operator = read(P / 'capture_root_builder_operation.py', 'operative source-only future ROOT operator')
require(hashlib.sha256(builder).hexdigest() == 'c31aaf8f54baa209ac37418643d6bb68f96fa80fa3af59130928f1c39a110e4b' and len(builder) == 45253, 'operative exact builder')
require(hashlib.sha256(operator).hexdigest() == 'c18b511b44e46c2bd42aaadd84ccead787296e99560a16843b7063817caf0626', 'operative exact operator')
line = b"        'audit_relative_inner_attempt': attempt.relative_to(audit).as_posix(),\n"
require(builder.count(line) == 1 and builder.replace(line, b'', 1) == read(P / 'builder_before_final_tool_edit_RECONSTRUCTED_AFTER.py', 'explicit after-edit reconstructed source'), 'builder exact reconstructed inverse; no historical capture claim')
new = b"        for key, path, prior in [('builder_unchanged_after_child', builder, source),\n                                 ('operator_unchanged_after_child', script, operator)]:\n            try:\n                record[key] = regular(path) == prior\n            except BaseException:\n                record[key] = False\n                record[key + '_read_failure'] = traceback.format_exc()\n"
old = b"        record['builder_unchanged_after_child'] = regular(builder) == source\n        record['operator_unchanged_after_child'] = regular(script) == operator\n"
require(operator.count(new) == 1 and operator.replace(new, old, 1) == read(P / 'operator_before_final_tool_edit_RECONSTRUCTED_AFTER.py', 'explicit after-edit reconstructed source'), 'operator exact reconstructed inverse; no historical capture claim')
native = strict(read(P / 'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json', 'false pending fresh13 draft'))['required_paths']
native_rows = []
started_native = now()
for name in native:
    read(R / canonical(name), 'dated native observation only; no ROOT approval')
    native_rows.append(inputs[name])
ended_native = now()
commands = []
(F / 'readonly_git').mkdir(exist_ok=False)
for option in [('branch', '--show-current'), ('rev-parse', 'HEAD')]:
    rec = dict(argv=['git', *option], cwd=str(R), started_utc=now(), stdin_supplied=False, actual_execution=False, completed=False)
    index = len(commands)
    with (F / 'readonly_git' / (str(index) + '.stdout.bin')).open('xb') as out, (F / 'readonly_git' / (str(index) + '.stderr.bin')).open('xb') as err:
        child = subprocess.Popen(rec['argv'], cwd=R, stdin=subprocess.DEVNULL, stdout=out, stderr=err, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
        rec.update(actual_execution=True, pid=child.pid)
        rec['exit_code'] = child.wait(timeout=60)
        rec['completed'] = True
    rec['finished_utc'] = now()
    for channel in ['stdout', 'stderr']:
        raw = (F / 'readonly_git' / (str(index) + '.' + channel + '.bin')).read_bytes()
        rec[channel] = dict(path='readonly_git/' + str(index) + '.' + channel + '.bin', bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    commands.append(rec)
    write('GIT_COMMANDS_' + str(index) + '.json', rec)
    require(rec['exit_code'] == 0 and not (F / rec['stderr']['path']).read_bytes(), 'actual readonly Git succeeded: ' + str(option))
branch = (F / commands[0]['stdout']['path']).read_bytes().decode().strip()
head = (F / commands[1]['stdout']['path']).read_bytes().decode().strip()
require(branch == 'main', 'actual main-only')
require(not (A / 'reviewed_candidate').exists() and not (A / 'reviewed_candidate').is_symlink(), 'candidate remains absent')
write('STATIC_INPUT_MANIFEST.json', dict(schema='PR43_INDEPENDENT_CURRENT_SOURCE_STATIC_INPUTS_v1', utc=now(),
      static_input_files=sorted(inputs.values(), key=lambda row: row['path']), exact_closed_trees=trees,
      native13_observation=dict(started_utc=started_native, finished_utc=ended_native, files=native_rows,
                                current_branch=branch, current_head=head, approved_by_root=False),
      own_writes_excluded_from_inputs=True, candidate_source_import_compile_execution=False,
      foreign_full_bodies_copied=False, classification='These input bytes belong to their attributed authors; none is claimed as own authored science.'))
summary = dict(schema='PR43_INDEPENDENT_CURRENT_SOURCE_STATIC_RESULT_v1', utc=now(), actual_pid=os.getpid(),
      status='COMPLETE_STATIC_INSPECTION_NO_CANDIDATE_EXECUTION', input_files=len(inputs), exact_closed_trees=len(trees),
      predicate_checks=len(checks), every_check_passed=True, checks=checks,
      actual_readonly_git_commands=commands, observed_branch=branch, observed_head=head,
      builder_imported_compiled_executed=False, future_ROOT_operator_executed=False, mathematical_helpers_executed=False,
      candidate_created=False, ROOT_approval_attested=False, future_freeze_certified=False, whole_current_verdict=None)
write('STATIC_INSPECTION_RESULT.json', summary)
print(json.dumps({key: value for key, value in summary.items() if key not in ['checks', 'actual_readonly_git_commands']}, indent=2))
