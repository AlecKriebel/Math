"""Independent readonly custody audit; production source is read only as bytes/text."""
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat

F = Path(__file__).absolute().parent
A = F.parent
R = A.parents[2]
H = A / 'acceptance_preparation_family_v2'
PIN = '48ddcccb22eb898c42598278fa4914d84fa0da640e098973a1e70d7c60577662'
all_rows = {}
groups = {}
assertions = 0


def need(v, message):
    global assertions
    assertions += 1
    if not v:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def parse(raw):
    def pairs(items):
        obj = {}
        for k, v in items:
            need(k not in obj, 'duplicate JSON key')
            obj[k] = v
        return obj
    def finite(s):
        n = float(s)
        need(math.isfinite(n), 'nonfinite number')
        return n
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))


def safe(name):
    need(type(name) is str and name and '\\' not in name and '\x00' not in name, 'path literal')
    pp = PurePosixPath(name)
    need(pp.as_posix() == name and not pp.is_absolute() and name != '.'
         and not {'.', '..', '.git', '__pycache__'}.intersection(pp.parts), 'canonical path')
    path = R / name
    need(not path.is_symlink() and stat.S_ISREG(path.stat().st_mode), 'regular bound member')
    need(all(not p.is_symlink() for p in path.parents), 'no symlink ancestor')
    return path


def add(group, row):
    need(type(row) is dict and set(row) == {'path', 'bytes', 'sha256', 'full_mode'}, 'normalized four keys')
    need(type(row['bytes']) is int and row['bytes'] >= 0 and type(row['full_mode']) is int
         and 0 <= row['full_mode'] <= 0o7777, 'typed size and fullmode')
    need(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'SHA256')
    path = safe(row['path'])
    raw = path.read_bytes()
    need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'entire fixed body: ' + row['path'])
    need(stat.S_IMODE(path.stat().st_mode) == row['full_mode'], 'fullmode: ' + row['path'])
    if row['path'] in all_rows:
        need(equal(all_rows[row['path']], row), 'conflicting row')
    all_rows[row['path']] = row
    groups.setdefault(group, []).append(row['path'])
    return raw


def live_row(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(R).as_posix(), 'bytes': len(raw), 'sha256': sha(raw),
            'full_mode': stat.S_IMODE(path.stat().st_mode)}


def closure(base, name, pin, count, group):
    body = add(group, live_row(base / name))
    need(sha(body) == pin, 'explicit known manifest')
    m = parse(body)
    need(m['self_excluded'] == [name] and type(m['files_count']) is int
         and m['files_count'] == count and len(m['files']) == count, 'exact self-only count')
    names = set()
    for z in m['files']:
        need(type(z) is dict and set(z) == {'path', 'bytes', 'sha256'} and z['path'] not in names
             and z['path'] != name, 'exact unique closure row')
        names.add(z['path'])
        add(group, {'path': (base / z['path']).relative_to(R).as_posix(),
                    'bytes': z['bytes'], 'sha256': z['sha256'], 'full_mode': 0o444})
    need(stat.S_IMODE((base / name).stat().st_mode) == 0o444, 'literal manifest full444')
    files, dirs = set(), set()
    for path in base.rglob('*'):
        need(not path.is_symlink() and (path.is_file() or path.is_dir()), 'regular closed topology')
        (files if path.is_file() else dirs).add(path.relative_to(base).as_posix())
    expected_files = names | {name}
    expected_dirs = {p.as_posix() for n in expected_files for p in PurePosixPath(n).parents
                     if p.as_posix() != '.'}
    need(files == expected_files and dirs == expected_dirs, 'whole recursive topology')
    return m, len(dirs)


def capture4(folder, pid, argv):
    need({p.name for p in folder.iterdir()} == {'CAPTURE.json', 'prelaunch_operator.py',
                                              'stdout.bin', 'stderr.bin'}, 'actual CAP4 topology')
    for path in folder.iterdir():
        add('actual_ROOT_V2_closure_and_readback', live_row(path))
    c = parse((folder / 'CAPTURE.json').read_bytes())
    required = {'schema': 'root-explicit-command-capture/v1', 'argv': argv, 'cwd': str(R),
                'actual_execution': True, 'pid': pid, 'exit_code': 0, 'completed': True,
                'stdin_supplied': False, 'operator_unchanged': True, 'expected_exit_code': 0,
                'status': 'PASS',
                'operator_sha256': 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'}
    for key, value in required.items():
        need(key in c and equal(c[key], value), 'typed entire actual capture ' + key)
    need(sha((folder / 'prelaunch_operator.py').read_bytes()) == c['operator_sha256'], 'full operator source')
    start, finish = [dt.datetime.fromisoformat(c[k]) for k in ['started_utc', 'finished_utc']]
    need(start.tzinfo is not None and finish.tzinfo is not None
         and start.utcoffset() == finish.utcoffset() == dt.timedelta(0)
         and start <= finish <= dt.datetime.now(dt.timezone.utc), 'actual UTC')
    for channel in ['stdout', 'stderr']:
        z = c[channel]
        raw = (folder / (channel + '.bin')).read_bytes()
        need(set(z) == {'path', 'bytes', 'sha256'} and z['path'] == channel + '.bin'
             and type(z['bytes']) is int and len(raw) == z['bytes'] and sha(raw) == z['sha256'], 'full stream')
    need((folder / 'stderr.bin').read_bytes() == b'', 'entire actual stderr')
    out = parse((folder / 'stdout.bin').read_bytes())
    need(out['manifest_sha256'] == PIN and out['production_imported_compiled_executed'] is False
         and out['future_acceptance_approved'] is False, 'actual closure is only source closure')
    return {'capture': live_row(folder / 'CAPTURE.json'), 'complete_capture': c,
            'complete_members': [live_row(p) for p in sorted(folder.iterdir())]}


def main():
    m, dirs = closure(H, 'PREPARATION_MANIFEST.json', PIN, 70, 'closed_preparation_V2')
    need(set(m) == {'schema', 'status', 'utc', 'self_excluded', 'files_count', 'files', 'source_only',
                    'proposed_helpers_imported_compiled_executed', 'future_acceptance_or_ROOT_approval_claimed'}, 'exact V2 closure schema')
    need(m['schema'] == 'pr48-acceptance-source-closure/v2' and m['status'] == 'CLOSED_SOURCE_ONLY'
         and m['source_only'] is True and m['proposed_helpers_imported_compiled_executed'] is False
         and m['future_acceptance_or_ROOT_approval_claimed'] is False and dirs == 3, 'V2 source only')
    inputs = parse((H / 'INPUT_BINDINGS.json').read_bytes())
    need(inputs['actual_predecessor_PR47_completed'] is False and inputs['previous_mirror'] is None
         and inputs['previous_post'] is None and inputs['previous_root_post'] is None
         and inputs['previous_post_contract'] is None and inputs['future_native13_and_main_required'] is True,
         'never promote source ancestry to actual predecessor')
    need(len(inputs['external_input_rows']) == 3912 and len({z['path'] for z in inputs['external_input_rows']}) == 3912,
         '3912 fixed external rows, dated native4 excluded')
    native4 = {'draft_pr_publication_program_20260930/inventory.json', 'unsolved_math_prioritization/QUEUE.md',
               'unsolved_math_prioritization/state.json', 'unsolved_math_prioritization/history.jsonl'}
    need(not native4.intersection({z['path'] for z in inputs['external_input_rows']}), 'historical native4 not pinned live')
    for group, values in [('fixed3912_external', inputs['external_input_rows']), ('fixed_source_pins', list(inputs['pins'].values())),
                          ('dated_predecessor_SOURCE_only', list(inputs['source_pattern_dated_references'].values())
                           + [inputs['known_predecessor_source_contract'], inputs['known_predecessor_source_manifest']])]:
        for z in values:
            add(group, z)
    history = parse((H / 'SUPERSEDED_SOURCE_BINDINGS.json').read_bytes())
    need(history['status'] == 'SUPERSEDED_V1_NEEDS_M1_REPAIR_NOT_PROMOTED'
         and history['previous_PASS_transferred'] is False, 'honest closed adverse history')
    for key, count in [('superseded_source', 121), ('closed_adverse', 45)]:
        section = history[key]
        add(key, section['manifest'])
        base = (R / section['manifest']['path']).parent
        prior, unused = closure(base, Path(section['manifest']['path']).name,
                                section['manifest']['sha256'], count, key)
        need(equal(prior, section['entire_manifest']), 'whole historical manifest')
        for z in section['individual_closed_members']:
            add(key, z)
    for key in ['report', 'verdict']:
        add('closed_adverse_report_and_verdict', history[key])
    need(equal(parse((R / history['verdict']['path']).read_bytes()), history['entire_adverse_verdict'])
         and history['entire_adverse_verdict']['verdict'] == 'NEEDS_SOURCE_CORRECTION_SCOPED', 'complete M1 verdict')
    for row in history['actual_source_and_adverse_closure_readback_captures']:
        body = add('historical_actual_captures', row['capture'])
        need(equal(parse(body), row['complete_capture']), 'complete retained actual capture')
        for z in row['complete_members']:
            add('historical_actual_captures', z)
    capture_parent = R / 'draft_pr_publication_program_20260930/audits/pr45_9900007'
    rootcaps = [capture4(capture_parent / 'root_pr48_source_v2_closure_actual_capture', 45165,
                         ['/usr/bin/python3', '-B', str(H / 'close_source.py'), '--expected-report-sha256',
                          'db1895a028e08003d6e4796dee7f0a5087e1f665ebb3147ccd8a25c1c18c459a']),
                capture4(capture_parent / 'root_pr48_source_v2_closed_readback_actual_capture', 45457,
                         ['/usr/bin/python3', '-B', str(H / 'verify_closed_source.py'), '--expected-manifest-sha256', PIN])]
    need(dt.datetime.fromisoformat(rootcaps[0]['complete_capture']['finished_utc'])
         <= dt.datetime.fromisoformat(rootcaps[1]['complete_capture']['started_utc']), 'actual separate readback after closure')
    changes = parse((H / 'CHANGE_MAP.json').read_bytes())
    for z in changes['helper_bodies']:
        old = (A / 'acceptance_preparation_family' / z['name']).read_bytes()
        new = (H / z['name']).read_bytes()
        need(sha(old) == z['old_sha256'] and sha(new) == z['new_sha256']
             and (old == new) == z['unchanged'], 'literal old/new entire helper ' + z['name'])
    for z in changes['metadata_copies_unchanged']:
        need((A / 'acceptance_preparation_family' / z['name']).read_bytes() == (H / z['name']).read_bytes()
             and sha((H / z['name']).read_bytes()) == z['sha256'], 'unchanged source metadata ' + z['name'])
    science = parse((H / 'SCIENTIFIC_SCOPE.json').read_bytes())
    for key, value in {'full_problem_solved': False, 'full_problem_solved_by_project': False,
                       'novelty_claimed': False, 'priority_claimed': False, 'original_substantive_attempts': 2,
                       'new_substantive_attempts': 0, 'audit_turns': 0, 'paper_or_new_doi_or_tracker': False,
                       'related_alias_native_entry_added': False, 'related_alias_QUEUE_row_absent_preserved': True,
                       'duplicate_shared_budget': True}.items():
        need(key in science and equal(science[key], value), 'fixed science disposition ' + key)
    current = A / 'reviewed_candidate'
    current_m = parse((current / 'MANIFEST.json').read_bytes())
    need(sha((current / 'MANIFEST.json').read_bytes()) == '3f8d6b38fcd0268df5a32fc006c5a759b2dd61f225f2fa2fa959861a9bcb115f'
         and len(current_m['files']) == 1946, 'known current1946 closure')
    current_names = {(current / z['path']).relative_to(R).as_posix() for z in current_m['files']}
    need(current_names <= set(all_rows), 'every1946 current body individually covered')
    need(sha((current / 'CURRENT_DEPENDENCIES.json').read_bytes()) == '8e39fb3c8f6f2142737143caaacd256c68110e8938f815541020a0cf2055736a'
         and len(parse((current / 'CURRENT_DEPENDENCIES.json').read_bytes())['files']) == 1798, 'known1798 dependencies')
    whole = A / 'current_whole_adversary_family'
    whole_m, whole_dirs = closure(whole, 'MANIFEST.json', inputs['closed_whole_manifest']['sha256'],
                                  162, 'closed_WHOLE_first_party162')
    need(whole_dirs == 38, 'whole38 exact directories')
    need(len(whole_m['files']) == 162 and equal(whole_m, parse((H / 'EXPECTED_WHOLE_MANIFEST.json').read_bytes())), 'entire162 WHOLE')
    whole_names = {(whole / z['path']).relative_to(R).as_posix() for z in whole_m['files']}
    need(whole_names <= set(all_rows), 'every162 WHOLE body individually covered')
    root = parse((A / 'ROOT_WHOLE_CURRENT_REVIEW.json').read_bytes())
    need(equal(root, parse((H / 'EXPECTED_ROOT_WHOLE_REVIEW.json').read_bytes()))
         and root['future_execution_approved'] is False and root['future_acceptance_approved'] is False,
         'whole historical ROOT science read is not acceptance approval')
    rows = sorted(all_rows.values(), key=lambda z: z['path'])
    normalized = {'schema': 'pr48-v2-fresh-source-adversary-fixed-inputs/v1',
                  'unique_count': len(rows), 'rows': rows,
                  'groups': {k: sorted(set(v)) for k, v in sorted(groups.items())},
                  'dated_native4_pinned_live': False,
                  'actual_PR47_post_certified': False, 'future_acceptance_approved': False}
    with (F / 'INPUT_BINDINGS.json').open('x') as stream:
        json.dump(normalized, stream, sort_keys=True, indent=2)
        stream.write('\n')
    result = {'schema': 'pr48-v2-fresh-source-adversary-custody-result/v1', 'status': 'PASS_FIXED_CUSTODY_SOURCE_ONLY',
              'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid': os.getpid(),
              'assertions': assertions, 'preparation_manifest_sha256': PIN,
              'preparation_payload_files': 70, 'preparation_directories': dirs,
              'normalized_unique_fixed_inputs': len(rows),
              'complete_actual_ROOT_V2_closing_and_readback_captures': rootcaps,
              'full_current1946_body_coverage': True, 'full_WHOLE162_body_coverage': True,
              'fixed3912_external_inputs_checked': True, 'historical_native4_are_not_live_authority': True,
              'production_imported_compiled_executed': False, 'actual_PR47_post_certified': False,
              'future_acceptance_approved': False, 'ROOT_approval_authored': False}
    with (F / 'CUSTODY_RESULT.json').open('x') as stream:
        json.dump(result, stream, sort_keys=True, indent=2)
        stream.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'complete_actual_ROOT_V2_closing_and_readback_captures'}, sort_keys=True))


if __name__ == '__main__':
    main()
