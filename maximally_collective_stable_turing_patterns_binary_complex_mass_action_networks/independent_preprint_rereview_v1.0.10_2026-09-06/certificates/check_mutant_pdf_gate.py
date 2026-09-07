#!/usr/bin/env python3
"""Build the one-coefficient scratch supplement and exercise the full PDF gate."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source_snapshot'
TREE = HERE / 'scratch/conflicting_fields/project'
environment = os.environ.copy()
environment.update({
    'PATH': '/private/tmp/exact-diffusion-tinytex.oRiOLW/TinyTeX/bin/universal-darwin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin',
    'PYTHONPATH': '/Users/alec/Documents/Math/maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_preprint_rereview_v1.0.9_2026-09-06/software/scratch/pypdf',
    'SOURCE_DATE_EPOCH': '1787443200', 'FORCE_SOURCE_DATE': '1', 'TZ': 'UTC',
    'LC_ALL': 'C', 'PYTHONOPTIMIZE': '0', 'PYTHONHASHSEED': '0', 'MPLBACKEND': 'Agg',
    'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
})
shutil.copytree(SOURCE / 'figures', TREE / 'figures', dirs_exist_ok=True)
for name in ['theorem_summary.pdf', 'proof_skeleton.pdf']:
    shutil.copy2(SOURCE / 'external_audit' / name, TREE / 'external_audit' / name)
results = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'source_commit': '953c836a12b9d9d474521feb4a96e218c1155203',
           'scope': 'One changed data coefficient and rebuilt scratch supplement; all other PDFs copied unchanged from source snapshot.',
           'steps': []}
steps = [
    ('supplement_latex_pass_1', ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'supplement.tex'], TREE / 'manuscript'),
    ('supplement_latex_pass_2', ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'supplement.tex'], TREE / 'manuscript'),
    ('supplement_latex_pass_3', ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'supplement.tex'], TREE / 'manuscript'),
    ('full_pdf_audit', ['/usr/local/bin/python', str(TREE / 'computation/audit_pdfs.py'), '--profile', 'full', '--output-dir', str(HERE / 'scratch/mutant_pdf_preflight')], TREE),
]
for label, command, directory in steps:
    proc = subprocess.run(command, cwd=directory, env=environment, capture_output=True, text=True)
    (HERE / f'{label}_conflicting_fields.log').write_text(proc.stdout + proc.stderr)
    summary = [line for line in proc.stdout.splitlines() if 'PASS' in line or line.startswith('Output written') or line.startswith('Transcript written')]
    results['steps'].append({'name': label, 'returncode': proc.returncode, 'last_stdout': summary[-4:]})
    (HERE / 'MUTANT_PDF_GATE_RESULT.json').write_text(json.dumps(results, indent=2) + '\n')
    if proc.returncode:
        break
if results['steps'][-1]['name'] == 'full_pdf_audit' and results['steps'][-1]['returncode'] == 0:
    evidence = HERE / 'scratch/mutant_pdf_preflight/manuscript_supplement_pdf.txt'
    shutil.copy2(evidence, HERE / 'mutant_supplement_pdf_evidence.txt')
    paths = ['independent_verifier/pareto_all_m_certificate.json', 'data/certificate_tables.tex', 'manuscript/supplement.pdf']
    manifest = (SOURCE / 'release/sha256_manifest.txt').read_text().splitlines()
    records = []
    for relative in paths:
        digest = next(line.split()[0] for line in manifest if line.endswith('  ' + relative) or line.endswith('  ./' + relative))
        original = hashlib.sha256((SOURCE / relative).read_bytes()).hexdigest()
        mutated = hashlib.sha256((TREE / relative).read_bytes()).hexdigest()
        assert digest == original and digest != mutated
        records.append({'file': relative, 'published_manifest_sha256': digest, 'source_sha256': original,
                        'mutant_sha256': mutated, 'published_hash_rejects_mutant': True})
    log = (TREE / 'manuscript/supplement.log').read_text()
    results['final_tex_warning_matches'] = re.findall(r'^.*(?:LaTeX Warning|Package .*Warning|Overfull|Underfull|undefined references).*$', log, re.M)
    assert not results['final_tex_warning_matches']
    certificate_result = json.loads((HERE / 'CONFLICTING_FIELDS_RESULT.json').read_text())
    certificate_result['displayed_minus_actual_polynomial'] = '16019*x**6*z/24300'
    certificate_result['positive_point'] = {'x': 1, 'z': 1, 's': 1, 'A': 4, 'difference': '16019/24300'}
    certificate_result['published_hash_containment'] = records
    (HERE / 'CONFLICTING_FIELDS_RESULT.json').write_text(json.dumps(certificate_result, indent=2) + '\n')
    (HERE / 'MUTANT_PDF_GATE_RESULT.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
