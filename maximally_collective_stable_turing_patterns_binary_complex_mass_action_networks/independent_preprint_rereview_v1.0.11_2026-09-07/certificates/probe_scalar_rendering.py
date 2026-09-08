#!/usr/bin/env python3
"""Bounded scalar coercion/rendering probe; no published inputs are edited."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source_snapshot'
TREE = HERE / 'scratch/scalar_project'
TREE.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(SOURCE / 'independent_verifier'))

def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

unit = load('scalar_unit', 'independent_verifier/verify_mode_isolation.py')
duplicate = load('scalar_duplicate', 'independent_verifier/dd_verify_mode_isolation.py')
exposition = load('scalar_exposition', 'independent_verifier/frontier_verify_exposition_identities.py')
generator = load('scalar_generator', 'computation/generate_tables.py')
results = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'commit': '137ffa9f1a340f621651395ad0236cf1bdadb51c',
           'scope': 'Scalar type/spelling outside the shipped canonical rational-string forms; C1 mixed-field repair remains closed.',
           'source_audit_scope': 'Includes release/ and submission/ conditional source checks. No full release refresh was run on the mutant.',
           'direct_cases': [], 'steps': []}
for label, value in [('boolean_true', True), ('scientific_string', '1e0')]:
    payload = json.loads((SOURCE / 'independent_verifier/improved_modulus_certificate.json').read_text())
    payload['homogeneous']['terms'][0]['coefficient'] = value
    candidate = HERE / f'{label}_certificate.json'
    candidate.write_text(json.dumps(payload, indent=2) + '\n')
    record = {'case': label, 'powers': [10, 0], 'before': '1', 'after': value, 'reader_value': '1'}
    for reader, function in [('unit_reader', lambda: unit.verify_certificate(candidate)),
                             ('duplicate_reader', lambda: duplicate.verify_certificate(candidate)),
                             ('exposition_reader', lambda: exposition.verify_modulus_source_polynomials(unit_certificate=candidate))]:
        function()
        record[reader] = 'ACCEPTED'
    section = payload['homogeneous']
    table = generator.cert_table('probe', section['variables'], section['terms'], section['term_count'], ('x', 'z'))
    record['generated_row'] = next(line for line in table.splitlines() if line.startswith('10 & 0 &'))
    results['direct_cases'].append(record)

for directory in ['independent_verifier', 'computation', 'data', 'manuscript', 'literature', 'proof_audit', 'figures', 'release', 'submission']:
    shutil.copytree(SOURCE / directory, TREE / directory, dirs_exist_ok=True)
(TREE / 'external_audit').mkdir(exist_ok=True)
for name in ['theorem_summary.tex', 'proof_skeleton.tex', 'theorem_summary.pdf', 'proof_skeleton.pdf']:
    shutil.copy2(SOURCE / 'external_audit' / name, TREE / 'external_audit' / name)
shutil.copy2(SOURCE / 'CITATION.cff', TREE / 'CITATION.cff')
shutil.copy2(HERE / 'boolean_true_certificate.json', TREE / 'independent_verifier/improved_modulus_certificate.json')
freshness = subprocess.run([
    sys.executable, str(TREE / 'computation/generate_tables.py'),
    '--check-certificate-table', str(SOURCE / 'data/certificate_tables.tex'),
], capture_output=True, text=True)
assert freshness.returncode != 0 and 'STALE_GENERATED_MODULUS_TABLE' in freshness.stderr
results['unchanged_table_freshness'] = {'returncode': freshness.returncode, 'diagnostic': 'STALE_GENERATED_MODULUS_TABLE'}

environment = os.environ.copy()
environment.update({
    'PATH': '/private/tmp/exact-diffusion-tinytex.oRiOLW/TinyTeX/bin/universal-darwin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
    'PYTHONPATH': '/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_preprint_rereview_v1.0.9_2026-09-06/software/scratch/pypdf',
    'SOURCE_DATE_EPOCH': '1787443200', 'FORCE_SOURCE_DATE': '1', 'TZ': 'UTC',
    'LC_ALL': 'C', 'PYTHONOPTIMIZE': '0', 'PYTHONHASHSEED': '0', 'MPLBACKEND': 'Agg',
    'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
})
steps = [
    ('regenerate_tables', [sys.executable, str(TREE / 'computation/generate_tables.py')], TREE),
    ('full_symbolic_suite', [sys.executable, str(TREE / 'independent_verifier/verify_symbolic_certificates.py')], TREE),
    ('source_audit', [sys.executable, str(TREE / 'computation/audit_manuscript.py')], TREE),
    ('latex_pass_1', ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'supplement.tex'], TREE / 'manuscript'),
    ('latex_pass_2', ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'supplement.tex'], TREE / 'manuscript'),
    ('latex_pass_3', ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'supplement.tex'], TREE / 'manuscript'),
    ('full_pdf_audit', ['/usr/local/bin/python', str(TREE / 'computation/audit_pdfs.py'), '--profile', 'full', '--output-dir', str(HERE / 'scratch/scalar_pdf_preflight')], TREE),
]
for label, command, directory in steps:
    proc = subprocess.run(command, cwd=directory, env=environment, capture_output=True, text=True)
    (HERE / f'scalar_{label}.log').write_text(proc.stdout + proc.stderr)
    summary = [line for line in proc.stdout.splitlines() if 'PASS' in line or line.startswith('Output written') or line.startswith('TABLES_GENERATED')]
    results['steps'].append({'name': label, 'returncode': proc.returncode, 'summary': summary})
    (HERE / 'SCALAR_RENDERING_RESULTS.json').write_text(json.dumps(results, indent=2) + '\n')
    if proc.returncode:
        break

original = (SOURCE / 'data/certificate_tables.tex').read_text().splitlines()
mutated = (TREE / 'data/certificate_tables.tex').read_text().splitlines()
results['table_differences'] = [{'line': i+1, 'before': a, 'after': b} for i, (a,b) in enumerate(zip(original,mutated)) if a != b]
manifest = (SOURCE / 'release/sha256_manifest.txt').read_text().splitlines()
results['published_hash_containment'] = []
for relative in ['independent_verifier/improved_modulus_certificate.json', 'data/certificate_tables.tex', 'manuscript/supplement.pdf']:
    recorded = next(line.split()[0] for line in manifest if line.endswith('  ' + relative) or line.endswith('  ./' + relative))
    shipped = hashlib.sha256((SOURCE / relative).read_bytes()).hexdigest()
    changed = hashlib.sha256((TREE / relative).read_bytes()).hexdigest()
    assert recorded == shipped and recorded != changed
    results['published_hash_containment'].append({'path': relative, 'published': recorded, 'mutated': changed, 'detects_mutation': True})
log = (TREE / 'manuscript/supplement.log').read_text()
results['final_selected_tex_warnings'] = re.findall(r'^.*(?:LaTeX Warning|Package .*Warning|Overfull|Underfull|undefined references).*$', log, re.M)
evidence = HERE / 'scratch/scalar_pdf_preflight/manuscript_supplement_pdf.txt'
if evidence.exists():
    shutil.copy2(evidence, HERE / 'scalar_mutant_pdf_evidence.txt')
(HERE / 'SCALAR_RENDERING_RESULTS.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
