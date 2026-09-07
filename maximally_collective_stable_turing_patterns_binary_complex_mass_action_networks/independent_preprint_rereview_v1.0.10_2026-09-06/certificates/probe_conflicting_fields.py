#!/usr/bin/env python3
"""Probe a data-only disagreement between the exact reader and TeX producer."""
from pathlib import Path
import datetime
import importlib.util
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source_snapshot'
sys.path.insert(0, str(SOURCE / 'independent_verifier'))
SCRATCH = HERE / 'scratch' / 'conflicting_fields'
SCRATCH.mkdir(parents=True, exist_ok=True)

def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

mode = load('probe_mode', 'independent_verifier/frontier_verify_mode_certificates.py')
exposition = load('probe_exposition', 'independent_verifier/frontier_verify_exposition_identities.py')
generator = load('probe_generator', 'computation/generate_tables.py')
unit = json.loads((SOURCE / 'independent_verifier/improved_modulus_certificate.json').read_text())
payload = json.loads((SOURCE / 'independent_verifier/pareto_all_m_certificate.json').read_text())
rows = payload['modulus']['spatial']['terms']
index = next(i for i, row in enumerate(rows) if len(row['coefficient_in_A_ascending']) == 1)
row = rows[index]
original = json.loads(json.dumps(row))
row['coefficient_in_U_ascending'] = ['1']
mutant = HERE / 'conflicting_coefficient_fields.json'
mutant.write_text(json.dumps(payload, indent=2) + '\n')

results = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'source_commit': '953c836a12b9d9d474521feb4a96e218c1155203',
           'mutation': {'section': 'modulus.spatial', 'index': index, 'before': original, 'after': row}}
for label, function in [('direct_mode_reader', lambda: mode.verify(mutant)),
                        ('source_polynomial_reader', lambda: exposition.verify_modulus_source_polynomials(pareto_certificate=mutant))]:
    try:
        function()
        results[label] = 'ACCEPTED'
    except BaseException as exc:
        results[label] = {'rejected': type(exc).__name__, 'message': str(exc)}

parts = [
    generator.cert_table('35-term homogeneous certificate', unit['homogeneous']['variables'], unit['homogeneous']['terms'], unit['homogeneous']['term_count'], ('x', 'z')),
    generator.cert_table('77-term improved-profile spatial certificate', unit['improved_mode']['variables'], unit['improved_mode']['terms'], unit['improved_mode']['term_count'], ('x', 'z', 's')),
    generator.cert_table(r'22-term equilibrium-scaled homogeneous certificate ($U=A-1/4$)', payload['modulus']['homogeneous']['variables'], payload['modulus']['homogeneous']['terms'], payload['modulus']['homogeneous']['term_count'], ('x', 'z'), True),
    generator.cert_table('84-term equilibrium-scaled spatial certificate', payload['modulus']['spatial']['variables'], rows, payload['modulus']['spatial']['term_count'], ('x', 'z', 's'), True),
]
generated = '\n\n'.join(parts) + '\n'
(HERE / 'conflicting_coefficient_fields_table.tex').write_text(generated)
original_table = (SOURCE / 'data/certificate_tables.tex').read_text()
before_lines = original_table.splitlines()
after_lines = generated.splitlines()
results['table_differences'] = [{'line': i+1, 'before': b, 'after': a} for i, (b,a) in enumerate(zip(before_lines, after_lines)) if b != a]
old_table_check = subprocess.run([
    sys.executable, str(SOURCE / 'computation/generate_tables.py'),
    '--pareto-certificate', str(mutant), '--check-certificate-table',
    str(SOURCE / 'data/certificate_tables.tex'),
], capture_output=True, text=True)
assert old_table_check.returncode != 0
assert 'STALE_GENERATED_MODULUS_TABLE' in old_table_check.stdout + old_table_check.stderr
results['unchanged_table_containment'] = {'returncode': old_table_check.returncode, 'result': 'STALE_GENERATED_MODULUS_TABLE'}

tree = SCRATCH / 'project'
if tree.exists():
    shutil.rmtree(tree)
tree.mkdir()
for directory in ['independent_verifier', 'computation', 'data', 'manuscript', 'external_audit', 'literature', 'proof_audit']:
    # External audit only needs its two source exports for the source audit.
    if directory == 'external_audit':
        (tree / directory).mkdir()
        for file in ['theorem_summary.tex', 'proof_skeleton.tex']:
            shutil.copy2(SOURCE / directory / file, tree / directory / file)
    else:
        shutil.copytree(SOURCE / directory, tree / directory)
for file in ['CITATION.cff']:
    shutil.copy2(SOURCE / file, tree / file)
shutil.copy2(mutant, tree / 'independent_verifier/pareto_all_m_certificate.json')
(tree / 'data/certificate_tables.tex').write_text(generated)

for label, relative in [('full_symbolic_suite', 'independent_verifier/verify_symbolic_certificates.py'),
                        ('manuscript_source_audit', 'computation/audit_manuscript.py')]:
    completed = subprocess.run([sys.executable, str(tree / relative)], cwd=tree, capture_output=True, text=True)
    (HERE / f'{label}_conflicting_fields.log').write_text(completed.stdout + completed.stderr)
    results[label] = {'returncode': completed.returncode, 'last_stdout': completed.stdout.splitlines()[-4:]}
    (HERE / 'CONFLICTING_FIELDS_RESULT.json').write_text(json.dumps(results, indent=2) + '\n')

print(json.dumps(results, indent=2))
