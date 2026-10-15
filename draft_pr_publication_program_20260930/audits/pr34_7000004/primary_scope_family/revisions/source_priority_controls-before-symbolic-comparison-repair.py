#!/usr/bin/env python3
"""Reproduce actual PR code, bind raw source, and test priority equivalence controls.

The universal certificate is PRIOR_EQUIVALENCE_CERTIFICATE.md. These controls
supplement it and expose false promotion by the original local-only scripts.
Run with /usr/bin/python3 (SymPy1.14.0) from any directory.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import unicodedata

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SNAP = HERE.parent / 'source_snapshot'
checks = {}
mutants = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(name, value):
    if not bool(value):
        raise AssertionError(name)
    checks[name] = 'PASS'


def rejected(name, func):
    try:
        func()
    except (AssertionError, ValueError, KeyError):
        mutants[name] = 'REJECTED'
    else:
        raise AssertionError('accepted mutant: ' + name)


def load(path):
    return json.loads(path.read_text())


def norm(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', text)).strip()


manifest = load(ROOT / 'unsolved_math_prioritization/manifest.json')
cache = ROOT / 'unsolved_math_prioritization/cache'
for name, spec in manifest['files'].items():
    data = (cache / name).read_bytes()
    check('raw_' + name + '_bytes', len(data) == spec['bytes'])
    check('raw_' + name + '_sha', sha(data) == spec['sha256'])

problems = load(cache / 'problems.json')
reports = load(cache / 'research_results.json')
selected = [p for p in problems if p.get('id') == 7000004]
check('unique_numeric_id', len(selected) == 1)
problem = selected[0]
code = problem['problem_number']
check('unique_code_for_report_join', sum(p.get('problem_number') == code for p in problems) == 1)
report = reports[code]
source = load(SNAP / 'source_record.json')
old_report = load(SNAP / 'prior_report.json')
readiness = load(SNAP / 'readiness.json')


def validate_identity(p, r, source_record, prior_report, evidence):
    assert p['id'] == 7000004 and p['problem_number'] == 'AMR-069-0004'
    assert p == source_record
    assert r == prior_report
    assert evidence['review_hash'] == sha(json.dumps([p, r], sort_keys=True).encode())
    assert evidence['statement_hash'] == sha(p['statement'].encode())


validate_identity(problem, report, source, old_report, readiness)
check('full_raw_source_and_separate_prior_report_equal', True)
db = sqlite3.connect('file:' + str((cache / 'catalog.sqlite').resolve()) + '?mode=ro', uri=True)
check('sqlite_exact_record_count', db.execute('SELECT count(*) FROM records').fetchone()[0] == manifest['records'])
check('sqlite_revision', db.execute('SELECT revision FROM metadata').fetchone()[0] == manifest['revision'])
row = db.execute('SELECT payload,report FROM records WHERE key=?', ('7000004',)).fetchone()
db.close()
check('sqlite_full_payload_and_report_equal_raw', json.loads(row[0]) == problem and json.loads(row[1]) == report)

for name, field, replacement in [('numeric_id', 'id', 7000005), ('reused_code', 'problem_number', 'AMR-069-0005'), ('changed_literal', 'statement', 'Assume a regular binormal.')]:
    altered = copy.deepcopy(problem)
    altered[field] = replacement
    rejected(name, lambda altered=altered: validate_identity(altered, report, source, old_report, readiness))
bad_report = copy.deepcopy(report)
bad_report['result'] = 'A full global linking theorem was already proved.'
rejected('wrong_report', lambda: validate_identity(problem, bad_report, source, old_report, readiness))
bad_readiness = copy.deepcopy(readiness)
bad_readiness['review_hash'] = '0' * 64
rejected('stale_review_hash', lambda: validate_identity(problem, report, source, old_report, bad_readiness))

input_manifest = load(HERE.parent / 'snapshot_manifest.json')
head = input_manifest['head']
base = input_manifest['base']
changed = subprocess.check_output(['git', 'diff', '--name-only', base, head], cwd=ROOT, text=True).splitlines()
check('actual_git_changed_paths_equal_manifest', changed == input_manifest['changed_paths'])
check('actual_git_merge_base_equal_declared_base', subprocess.check_output(['git', 'merge-base', base, head], cwd=ROOT, text=True).strip() == base)
file_bindings = []
for spec in input_manifest['files']:
    data = (SNAP / spec['path']).read_bytes()
    git_data = subprocess.check_output(['git', 'show', head + ':unsolved_math_prioritization/attempts/7000004/' + spec['path']], cwd=ROOT)
    check('original_binding_' + spec['path'], len(data) == spec['size'] and sha(data) == spec['sha256'] and data == git_data)
    file_bindings.append({'path': spec['path'], 'bytes': len(data), 'sha256': sha(data)})

header = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']


def parse_queue(q):
    lines = q.splitlines()
    h = next(line for line in lines if line.startswith('| Rank |'))
    assert [v.strip() for v in h.split('|')[1:-1]] == header
    rows = [line for line in lines if line.startswith('|') and len(line.split('|')) == 14 and line.split('|')[2].strip().split(' / ')[0] == '7000004']
    assert len(rows) == 1
    values = [v.strip() for v in rows[0].split('|')[1:-1]]
    out = dict(zip(header, values))
    assert out['Chat'] == '' and out['DOI'] == ''
    assert out['Status'] in ['queued', 'unsolved', 'already_solved']
    assert re.fullmatch(r'[0-5]/5', out['Turns'])
    return out


base_q = subprocess.check_output(['git', 'show', base + ':unsolved_math_prioritization/QUEUE.md'], cwd=ROOT, text=True)
head_q = subprocess.check_output(['git', 'show', head + ':unsolved_math_prioritization/QUEUE.md'], cwd=ROOT, text=True)
base_fields = parse_queue(base_q)
head_fields = parse_queue(head_q)
check('actual_pr_queue_named_fields', base_fields['Status'] == 'queued' and base_fields['Turns'] == '0/5' and head_fields['Status'] == 'unsolved' and head_fields['Turns'] == '1/5' and 'signed-crossing' in head_fields['Findings'])
check('all_other_queue_lines_preserved', [v for v in base_q.splitlines() if not re.match(r'\| \d+ \| 7000004 /', v)] == [v for v in head_q.splitlines() if not re.match(r'\| \d+ \| 7000004 /', v)])
current_q = (ROOT / 'unsolved_math_prioritization/QUEUE.md').read_text()
live_fields = parse_queue(current_q)
check('live_main_target_not_yet_accepted', live_fields['Status'] == 'queued' and live_fields['Turns'] == '0/5' and live_fields['Findings'] == '')
rejected('legacy_eight_column_header', lambda: parse_queue(head_q.replace('| Chat | Findings | DOI |', '| Findings | DOI |')))
selected_line = next(v for v in head_q.splitlines() if re.match(r'\| \d+ \| 7000004 /', v))
parts = selected_line.split('|')
parts[10], parts[11] = parts[11], parts[10]
bad_q = head_q.replace(selected_line, '|'.join(parts))
rejected('findings_moved_to_chat', lambda: parse_queue(bad_q))
rejected('duplicate_queue_target', lambda: parse_queue(head_q + selected_line + '\n'))

exact_duplicate_ids = [p['id'] for p in problems if norm(p.get('statement', '')) == norm(problem['statement'])]
check('full_statement_exact_duplicate_scan', exact_duplicate_ids == [7000004])
related = load(ROOT / 'unsolved_math_prioritization/review_v2/related_target_groups.json')
check('no_related_group_contains_target', all('7000004' not in g.get('ids', []) for g in related['groups']))
binormal_records = [{'id': p['id'], 'code': p.get('problem_number'), 'statement': p.get('statement')} for p in problems if 'binormal' in p.get('statement', '').lower()]

replays = []
for label, script_rel, result_rel in [('author', 'verify.py', 'verification.json'), ('old_submitted', 'review/submitted_verify.py', 'review/submitted_results.json'), ('old_independent', 'review/independent_checks.py', 'review/independent_results.json')]:
    dest = HERE / 'tmp/replays' / label
    dest.mkdir(parents=True, exist_ok=True)
    copied_script = dest / Path(script_rel).name
    shutil.copyfile(SNAP / script_rel, copied_script)
    run = subprocess.run([sys.executable, str(copied_script)], cwd=dest, capture_output=True)
    (dest / 'stdout.json').write_bytes(run.stdout)
    (dest / 'stderr.txt').write_bytes(run.stderr)
    actual_result = dest / ('submitted_verify.json' if label == 'unused' else {'author': 'verification.json', 'old_submitted': 'verification.json', 'old_independent': 'independent_results.json'}[label])
    check('actual_replay_' + label, run.returncode == 0 and actual_result.read_bytes() == (SNAP / result_rel).read_bytes())
    replays.append({'label': label, 'returncode': run.returncode, 'script_sha256': sha(copied_script.read_bytes()), 'stdout_sha256': sha(run.stdout), 'result_sha256': sha(actual_result.read_bytes())})

# Execute the actual local author program unchanged beside false global prose.
# This exposes a coverage hole rather than inventing a toy old validator.
prose_control = HERE / 'tmp/replays/false_global_prose'
prose_control.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SNAP / 'verify.py', prose_control / 'verify.py')
(prose_control / 'OBSTRUCTION.md').write_text('Every continuous injective unit binormal has nonzero linking. A global theorem is certified.\n')
false_run = subprocess.run([sys.executable, str(prose_control / 'verify.py')], cwd=prose_control, capture_output=True)
check('actual_old_program_accepts_false_global_prose', false_run.returncode == 0 and (prose_control / 'verification.json').read_bytes() == (SNAP / 'verification.json').read_bytes())

t = s.symbols('t', real=True)
x, y, a = s.symbols('x y a', real=True)
g = s.Matrix([s.cos(t), s.sin(t), s.cos(2*t)])
b = s.Matrix([-4*s.cos(t)**3, 4*s.sin(t)**3, 1])
cross = g.diff(t).cross(g.diff(t, 2))
check('prior_curve_exact_cross_product', all(s.trigsimp(cross[i] - b[i]) == 0 for i in range(3)))
check('prior_curve_graph_identity', s.trigsimp(s.cos(t)**4 - s.sin(t)**4 - s.cos(2*t)) == 0)
check('prior_binormal_orthogonal_first_second', s.trigsimp(b.dot(g.diff(t))) == 0 and s.trigsimp(b.dot(g.diff(t, 2))) == 0)
check('prior_cross_vertical_component_nonzero', cross[2] == 1)
normal = s.Matrix([-4*x**3, 4*y**3, 1])
gx = s.Matrix([1, 0, 4*x**3])
gy = s.Matrix([0, 1, -4*y**3])
check('prior_surface_exact_graph_normal', gx.cross(gy) == normal)
check('prior_normalization_positive_squared_norm', s.expand(normal.dot(normal)) == 1 + 16*x**6 + 16*y**6)
check('prior_asymptotic_II_numerator', s.trigsimp(12*s.cos(t)**2 * s.sin(t)**2 - 12*s.sin(t)**2 * s.cos(t)**2) == 0)
check('prior_surface_Hessian_determinant', s.det(s.hessian(x**4-y**4, (x, y))) == -144*x**2*y**2)
height = a + x**4 - (x-4*a*x**3)**4 + (y+4*a*y**3)**4 - y**4
q = s.Matrix([x-4*a*x**3, y+4*a*y**3, x**4-y**4+a])
check('exact_prior_pushoff_graph_height', s.expand(q[2]-q[0]**4+q[1]**4-height) == 0)
u, v = s.symbols('u v', real=True)
check('injective_cubic_exact_factorization', s.expand((u-v)*(u*u+u*v+v*v) - (u**3-v**3)) == 0)
check('injective_cubic_positive_factor', s.expand((u-v)**2+3*(u+v)**2-4*(u*u+u*v+v*v)) == 0)
check('binormal_four_cardinal_critical_points', all(b.diff(t).subs(t, v) == s.zeros(3, 1) for v in [0, s.pi/2, s.pi, 3*s.pi/2]))
check('binormal_not_regular', b.diff(t).subs(t, 0) == s.zeros(3, 1))
for denominator in [2, 3, 5, 11]:
    epsilon = s.Rational(1, 4*denominator)
    for k in range(-denominator, denominator+1):
        xv = s.Rational(k, denominator)
        yv = s.Rational(denominator-abs(k), denominator)
        check(f'height_exact_rational_{denominator}_{k}', height.subs({x:xv, y:yv, a:epsilon}) > 0)
bad_b = s.Matrix([-4*s.cos(t)**3, 4*s.sin(t)**3, 0])
rejected('wrong_binormal_vertical_coordinate', lambda: check('must_not_survive_wrong_binormal', all(s.trigsimp(cross[i]-bad_b[i]) == 0 for i in range(3))))
rejected('incorrect_positive_curvature_to_regular_B_inference', lambda: check('must_not_survive_regular_B_assertion', b.diff(t).subs(t, 0) != s.zeros(3, 1)))

out = {'passed': len(checks), 'rejected_mutants': len(mutants), 'checks': checks, 'mutants': mutants, 'sympy_version': s.__version__, 'source_identity': {'revision': manifest['revision'], 'id': problem['id'], 'code': code, 'review_hash': readiness['review_hash'], 'statement_hash': readiness['statement_hash'], 'exact_duplicate_ids': exact_duplicate_ids}, 'binormal_records': binormal_records, 'original_bindings': file_bindings, 'actual_replays': replays, 'actual_head_queue_named_fields': head_fields, 'live_main_queue_named_fields': live_fields, 'scope': 'Full universal consequence proved in certificate; controls are supplemental and original code remains local-only.'}
(HERE / 'source_priority_controls_results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False)+'\n')
print(json.dumps({'passed': len(checks), 'rejected_mutants': len(mutants), 'scope': out['scope']}, indent=2))
