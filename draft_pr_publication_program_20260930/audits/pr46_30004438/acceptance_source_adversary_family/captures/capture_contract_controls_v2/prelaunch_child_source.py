#!/usr/bin/env python3
"""Independently inspect historical captures and mutate private schema objects."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import os
import copy
import sys

assert __debug__ and sys.flags.optimize == 0
F = Path(__file__).resolve().parent
A = F.parent
P = A / 'acceptance_preparation_family'
R = A.parents[2]
checks = 0
read_rows = []


def require(value, label):
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)


def parse(raw):
    def pairs(items):
        o = {}
        for k, v in items:
            if k in o:
                raise ValueError('duplicate')
            o[k] = v
        return o
    def constant(v):
        raise ValueError('constant')
    def number(v):
        x = float(v)
        if not math.isfinite(x):
            raise ValueError('number')
        return x
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=number)


def read(path):
    require(not path.is_symlink() and path.is_file(), 'regular capture body')
    raw = path.read_bytes()
    read_rows.append({'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'full_mode': path.stat().st_mode & 0o7777})
    return raw


def utc(s):
    require(type(s) is str and s == s.strip(), 'literal clock')
    d = datetime.fromisoformat(s[:-1] + '+00:00' if s.endswith('Z') else s)
    require(d.tzinfo is not None and d.utcoffset().total_seconds() == 0, 'aware UTC')
    return d


def stream(folder, ref):
    require(type(ref) is dict and set(ref) == {'path', 'bytes', 'sha256'}, 'exact stream ref')
    require(ref['path'] in {'stdout.bin', 'stderr.bin'} and type(ref['bytes']) is int, 'typed literal stream')
    raw = read(folder / ref['path'])
    require(len(raw) == ref['bytes'] and hashlib.sha256(raw).hexdigest() == ref['sha256'], 'complete stream hash')
    return raw


source_rows = []
for path in sorted(P.rglob('CAPTURE.json')):
    folder = path.parent
    cap = parse(read(path))
    require(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid'] > 0,
            'genuine completed actual capture fields')
    require(type(cap['operator_pid']) is int and cap['operator_pid'] > 0 and type(cap['exit_code']) is int, 'typed actual capture PIDs/exit')
    start, finish = utc(cap['started_utc']), utc(cap['finished_utc'])
    require(start <= finish <= datetime.now(timezone.utc), 'genuine capture order')
    stdout = stream(folder, cap['stdout']); stderr = stream(folder, cap['stderr'])
    pre = parse(read(folder / 'PRELAUNCH.json'))
    source = read(folder / 'PRELAUNCH_SOURCE.py')
    if 'schema' in cap:
        require(cap['schema'] == 'pr46-source-operation-actual-capture/v1', 'recognized source-operation schema')
        require(cap['prelaunch'] == pre, 'complete embedded genuine prelaunch')
        require(utc(pre['created_utc']) <= start and pre['operator_pid'] == cap['operator_pid'], 'prelaunch precedes child')
        require(hashlib.sha256(source).hexdigest() == pre['source_sha256'], 'historical literal child source')
        operator = read(folder / 'PRELAUNCH_OPERATOR.py')
        require(hashlib.sha256(operator).hexdigest() == pre['operator_sha256'], 'historical literal operator source')
        require(cap['operator_unchanged'] is True and cap['source_unchanged'] is True, 'source unchanged during historical execution')
        require(cap['status'] == ('PASS' if cap['exit_code'] == 0 else 'FAIL'), 'failed source run is not PASS')
        family = 'source-operation'
    else:
        require(pre['argv'] == cap['argv'] and pre['cwd'] == cap['cwd'], 'complete historical Git prelaunch')
        require(hashlib.sha256(source).hexdigest() == cap['source_sha256'], 'literal historical Git operator source')
        require(cap['source_unchanged'] is True and cap['exit_code'] == 0 and cap['stdin_supplied'] is False, 'actual readonly Git disposition')
        family = 'schema-absent-historical-readonly-Git'
    source_rows.append({'path': str(path.relative_to(P)), 'capture_family': family, 'pid': cap['pid'],
                        'exit_code': cap['exit_code'], 'complete_sources_prelaunch_streams_checked': True})
require(len(source_rows) == 19 and sum(x['capture_family'] == 'source-operation' for x in source_rows) == 10,
        'all19 source preparation actual captures, ten operations andnine literal schema-absent Git')

external = []
for name, pid in [('root_pr46_acceptance_source_closure_actual_capture', 41857),
                  ('root_pr46_acceptance_source_closed_readback_actual_capture', 47451)]:
    folder = R / 'draft_pr_publication_program_20260930/audits/pr45_9900007' / name
    cap = parse(read(folder / 'CAPTURE.json'))
    require(cap['pid'] == pid and type(cap['pid']) is int and cap['actual_execution'] is True
            and cap['completed'] is True and cap['exit_code'] == 0, 'genuine external ROOT source closure/readback')
    start, finish = utc(cap['started_utc']), utc(cap['finished_utc'])
    require(start <= finish <= datetime.now(timezone.utc), 'ROOT closure chronology')
    stream(folder, cap['stdout']); stream(folder, cap['stderr'])
    # These are literal four-member ROOT captures: no standalone PRELAUNCH.json
    # is present. Preserve that historical absence without inventing a file.
    require(cap['schema'] == 'root-explicit-command-capture/v1', 'known four-member ROOT operator capture, not future sealer schema')
    operator = read(folder / 'prelaunch_operator.py')
    require(hashlib.sha256(operator).hexdigest() == cap['operator_sha256'] and cap['operator_unchanged'] is True, 'exact actual ROOT operator source')
    require({p.name for p in folder.iterdir()} == {'CAPTURE.json', 'stdout.bin', 'stderr.bin', 'prelaunch_operator.py'}, 'literal four-member ROOT capture topology')
    external.append({'path': str(folder / 'CAPTURE.json'), 'pid': cap['pid'], 'exit_code': cap['exit_code'],
                     'actual_full_split_streams_read': True})

contract = parse(read(P / 'ROOT_POST_CONTRACT.json'))
keyset = set(contract['required_ROOT_complete_keyset'])
require(len(keyset) == 21, '21 exact prospective ROOT keys')
template = {k: None for k in keyset}
template.update(contract['required_completed_values'])
template['schema'] = contract['required_ROOT_schema']
template['all_six_real_phase_captures'] = [{'path': 'private_fixture/' + str(i), 'bytes': 0,
    'sha256': hashlib.sha256(b'').hexdigest()} for i in range(6)]
template['entire_post'] = copy.deepcopy(contract['required_entire_post_values'])
def structural_fixture_valid(z):
    return (set(z) == keyset and type(z['completed_primary_prs']) is int and z['completed_primary_prs'] == 36
            and type(z['new_substantive_attempts']) is int and z['new_substantive_attempts'] == 0
            and type(z['all_six_real_phase_captures']) is list and len(z['all_six_real_phase_captures']) == 6)
require(structural_fixture_valid(template), 'positive private structural fixture passes before mutation')
rejections = []
for name, transform in [('drop_entire_post', lambda z: z.pop('entire_post')),
                        ('extra_fake_approval', lambda z: z.update(future_acceptance_approved=True)),
                        ('abbreviate_capture_list', lambda z: z.update(all_six_real_phase_captures=[])),
                        ('bool_primary_count', lambda z: z.update(completed_primary_prs=True)),
                        ('wrong_discovery_credit', lambda z: z.update(new_substantive_attempts=1)),
                        ('omit_response', lambda z: z.pop('original_source_verification_responses'))]:
    z = copy.deepcopy(template); transform(z)
    require(not structural_fixture_valid(z), 'positive-fixture prospective structural mutant rejected ' + name)
    rejections.append(name)

result = {'schema': 'pr46-source-adversary-capture-contract-controls/v1', 'status': 'PASS_PRIVATE_CAPTURE_AND_CONTRACT_CHECKS',
          'actual_pid': os.getpid(), 'finished_utc': datetime.now(timezone.utc).isoformat(), 'assertions': checks,
          'source_preparation_captures': source_rows, 'ROOT_source_closure_and_readback': external,
          'full_read_bindings': read_rows, 'contract_private_mutants_rejected': rejections,
          'contract_mutant_scope': 'Positive private structural fixture only; no real prospective ROOT completion or full contract execution is claimed.',
          'historical_schema_absence_is_not_null': True, 'production_imported_compiled_executed': False,
          'future_ROOT_post_completed': False, 'future_acceptance_approved': False}
(F / 'CAPTURE_CONTRACT_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'actual_pid': os.getpid(), 'assertions': checks,
                   'source_capture_count': len(source_rows), 'external_ROOT_capture_count': len(external)}, indent=2))
