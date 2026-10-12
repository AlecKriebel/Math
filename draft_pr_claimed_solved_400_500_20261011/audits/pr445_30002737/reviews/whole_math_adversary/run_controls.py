#!/usr/bin/env python3
"""Preserve raw optimized and mutation controls; write only in this folder."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1]/'source_snapshot/unsolved_math_prioritization/attempts/30002737'
RECORDS = HERE/'records'
FIXTURES = HERE/'private/fixtures'
RECORDS.mkdir(exist_ok=True)
FIXTURES.mkdir(parents=True, exist_ok=True)


def require(condition, text):
    if not condition:
        raise ValueError(text)


def execute(name, code, optimized=False):
    command = [sys.executable] + (['-O'] if optimized else []) + [str(code)]
    run = subprocess.run(command, capture_output=True, text=True)
    record = {'case': name, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'command': command, 'returncode': run.returncode,
              'stdout': run.stdout, 'stderr': run.stderr,
              'executed_bytes': len(code.read_bytes()),
              'executed_sha256': hashlib.sha256(code.read_bytes()).hexdigest()}
    (RECORDS/(name+'.json')).write_text(json.dumps(record, indent=2)+'\n')
    return record


baseline = execute('fresh_controls_optimized', HERE/'controls.py', True)
require(baseline['returncode'] == 0, 'own optimized baseline failed')
(HERE/'CONTROL_RESULTS_OPTIMIZED.json').write_text(baseline['stdout'])
normal = json.loads((HERE/'CONTROL_RESULTS.json').read_text())
optimized = json.loads(baseline['stdout'])
require({k:v for k,v in normal.items() if k != 'optimized'} ==
        {k:v for k,v in optimized.items() if k != 'optimized'}, 'own execution mode mismatch')

original = SOURCE/'author/checks/verify_counterexample.py'
original_bytes = original.read_bytes()
text = original_bytes.decode()
cases = [('original_baseline', text, False, True),
         ('original_baseline_optimized', text, True, True),
         ('original_bad_marker_normal', text.replace('E = (F(1, 10), F(1, 10))', 'E = (F(1, 6), F(0))'), False, False),
         ('original_bad_marker_optimized', text.replace('E = (F(1, 10), F(1, 10))', 'E = (F(1, 6), F(0))'), True, True),
         ('original_bad_pair_normal', text.replace('if slot < 2:', 'if slot < 3:'), False, False),
         ('original_bad_pair_optimized', text.replace('if slot < 2:', 'if slot < 3:'), True, True),
         ('original_bad_flow_normal', text.replace('target = max(F(0), 1-abs(t))', 'target = F(1)'), False, False),
         ('original_bad_flow_optimized', text.replace('target = max(F(0), 1-abs(t))', 'target = F(1)'), True, True)]
results = []
for name, contents, optimized_mode, expected_success in cases:
    copy_dir = FIXTURES/name
    copy_dir.mkdir(exist_ok=True)
    copy = copy_dir/'verify_counterexample.py'
    copy.write_text(contents)
    record = execute(name, copy, optimized_mode)
    require((record['returncode'] == 0) == expected_success, 'unexpected mutation outcome: '+name)
    results.append({'case': name, 'returncode': record['returncode'],
                    'bad_input_false_success': name.startswith('original_bad') and record['returncode'] == 0})

# A materially wrong marker must be rejected by our explicit checks in both modes.
own_text = (HERE/'controls.py').read_text()
replacement = own_text.replace('(F(1, 10), F(1, 10))', '(F(1, 6), F(0))')
require(replacement != own_text, 'mutation did not change own source')
for mode in [False, True]:
    name = 'fresh_bad_marker_' + ('optimized' if mode else 'normal')
    copy = FIXTURES/(name+'.py')
    copy.write_text(replacement)
    record = execute(name, copy, mode)
    require(record['returncode'] != 0 and 'marker collision' in record['stderr'], 'explicit guard did not reject own bad marker')
    results.append({'case': name, 'returncode': record['returncode'], 'wrong_input_rejected': True})
require(original.read_bytes() == original_bytes, 'original source changed')
summary = {'pr': 445, 'problem_id': '30002737', 'reviewer': '/root/pr445_whole_math_adversary',
           'original_head': '3242c84e06db7e99012c7fe581adde5c3f89fc89',
           'original_check_source_unchanged': True, 'original_source_sha256': hashlib.sha256(original_bytes).hexdigest(),
           'essential_assert_issue_reproduced': True, 'own_explicit_guards_survive_optimized_python': True,
           'cases': results, 'raw_records': [str(p.relative_to(HERE)) for p in sorted(RECORDS.glob('*.json'))]}
(HERE/'CONTROL_RUN_SUMMARY.json').write_text(json.dumps(summary, indent=2)+'\n')
print(json.dumps(summary, indent=2))
