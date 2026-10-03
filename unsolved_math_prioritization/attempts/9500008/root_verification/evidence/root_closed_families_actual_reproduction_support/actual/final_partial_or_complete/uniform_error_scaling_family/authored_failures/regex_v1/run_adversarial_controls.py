#!/usr/bin/env python3
"""Execute baseline and real mutations; preserve programs, prose and streams."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parent
source = root/'frozen_original'
records = []


def run(name, command, expected_exit):
    result = subprocess.run(command, capture_output=True)
    (root/'streams'/(name+'.stdout')).write_bytes(result.stdout)
    (root/'streams'/(name+'.stderr')).write_bytes(result.stderr)
    row = {'name': name, 'command': command, 'exit_code': result.returncode,
           'expected_exit': expected_exit, 'observed_expected': result.returncode == expected_exit,
           'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
           'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()}
    records.append(row)
    assert row['observed_expected'], row


run('new_controls_baseline', ['/usr/bin/python3', str(root/'audit_controls.py'),
    '--candidate', str(source/'PARTIAL.md'), '--out', str(root/'exact_control_results.json')], 0)
doc = (source/'PARTIAL.md').read_text()
mutations = {
    'prose_boundary_removed': ('2\\,\\omega_W(c;R_0+c)', '2\\,\\omega_W(c;R_0)'),
    'prose_rotation_sign': ('[W(a+T)-W(a+T-u)]-[W(a+u)-W(a)]', '[W(a+T)-W(a+T-u)]+[W(a+u)-W(a)]'),
    'prose_tail_nonsummable': ('Take \\(r=8\\sqrt{cm}\\)', 'Take \\(r=1\\sqrt{cm}\\)'),
    'prose_uniform_bound_weakened': ('common deterministic finite bound', 'piecewise finite bound'),
    'prose_independence_removed': ('are independent but need not be identically distributed', 'may be dependent and need not be identically distributed'),
    'prose_divergence_removed': ('sums of durations diverge in both directions', 'sums of durations may converge in both directions'),
    'prose_scaling_as_upgrade': ('\\Longrightarrow', '\\longrightarrow\\quad\\text{almost-sure Brownian scaling limit}'),
    'prose_all_origins_upgrade': ('(2)\n', '(2)\nThis bound holds uniformly over every translated observation window.\n'),
}
for name, (before, after) in mutations.items():
    assert before in doc, (name, before)
    d = root/'executed_mutations'/name
    d.mkdir(parents=True, exist_ok=True)
    mutant = d/'PARTIAL.md'
    mutant.write_text(doc.replace(before, after, 1))
    run(name, ['/usr/bin/python3', str(root/'audit_controls.py'), '--candidate', str(mutant), '--out', str(d/'receipt.json')], 1)
    records[-1]['mutation'] = {'before': before, 'after': after}
    records[-1]['mutated_prose_sha256'] = hashlib.sha256(mutant.read_bytes()).hexdigest()

programs = {
    'code_original_rotation_sign': ('verify.py', 'Y[j]+Y[j+T]-Y[j+T-u]', 'Y[j]+Y[j+T]+Y[j+T-u]'),
    'code_old_independent_tail': ('review/independent_checks.py', '(8*s.sqrt(c*m))**2', '(1*s.sqrt(c*m))**2'),
}
for name, (original, before, after) in programs.items():
    d = root/'executed_mutations'/name
    d.mkdir(parents=True, exist_ok=True)
    original_text = (source/original).read_text()
    assert before in original_text
    mutant = d/Path(original).name
    mutant.write_text(original_text.replace(before, after, 1))
    run(name, ['/usr/bin/python3', str(mutant)], 1)
    records[-1]['mutation'] = {'before': before, 'after': after}
    records[-1]['mutated_program_sha256'] = hashlib.sha256(mutant.read_bytes()).hexdigest()

out = {'utc': datetime.now(timezone.utc).isoformat(), 'records': records,
       'scope': 'Baseline succeeds; eight prose mutations and two original-program mutations fail. Mutation rejection is not a general automated proof certificate.'}
(root/'adversarial_execution_receipts.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
