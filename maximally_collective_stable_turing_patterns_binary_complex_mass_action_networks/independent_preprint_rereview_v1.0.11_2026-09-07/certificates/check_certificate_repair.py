#!/usr/bin/env python3
"""Independent bounded data mutation campaign for the v1.0.11 repair."""
from pathlib import Path
from copy import deepcopy
import datetime
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source_snapshot'
SCRATCH = HERE / 'scratch'
SCRATCH.mkdir(exist_ok=True)
sys.path.insert(0, str(SOURCE / 'independent_verifier'))

def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

mode = load('current_mode', 'independent_verifier/frontier_verify_mode_certificates.py')
exposition = load('current_exposition', 'independent_verifier/frontier_verify_exposition_identities.py')
generator = load('current_generator', 'computation/generate_tables.py')
baseline = json.loads((SOURCE / 'independent_verifier/pareto_all_m_certificate.json').read_text())
records = []
baseline_tables = {}

def outcome(function):
    try:
        value = function()
        return {'status': 'ACCEPTED'}, value
    except (AssertionError, ValueError, TypeError, KeyError) as error:
        return {'status': 'REJECTED', 'type': type(error).__name__, 'reason': str(error)}, None

for section_name, parameter, alternate in [('homogeneous', 'U', 'A'), ('spatial', 'A', 'U')]:
    required = f'coefficient_in_{parameter}_ascending'
    alternate_key = f'coefficient_in_{alternate}_ascending'
    for mutation in ['baseline', 'dual_conflict', 'dual_identical', 'only_wrong_field',
                     'missing_required', 'wrong_coefficient', 'reversed_coefficients',
                     'descriptive_metadata', 'variable_swap', 'wrong_bound', 'wrong_parameter']:
        if section_name == 'spatial' and mutation == 'wrong_parameter':
            continue  # Spatial section has no declared coefficient_parameter field.
        payload = deepcopy(baseline)
        section = payload['modulus'][section_name]
        row = next((r for r in section['terms'] if r['powers'] == [6, 1, 0]), section['terms'][0])
        if mutation == 'dual_conflict': row[alternate_key] = ['1']
        elif mutation == 'dual_identical': row[alternate_key] = row[required][:]
        elif mutation == 'only_wrong_field': row[alternate_key] = row.pop(required)
        elif mutation == 'missing_required': del row[required]
        elif mutation == 'wrong_coefficient': row[required][0] = '2'
        elif mutation == 'reversed_coefficients':
            row = next(r for r in section['terms'] if len(r[required]) > 1 and r[required] != list(reversed(r[required])))
            row[required].reverse()
        elif mutation == 'descriptive_metadata': row['review_note'] = 'Unconsumed descriptive metadata.'
        elif mutation == 'variable_swap': section['variables'][0], section['variables'][1] = section['variables'][1], section['variables'][0]
        elif mutation == 'wrong_bound': section['B'] = '7'
        elif mutation == 'wrong_parameter': section['coefficient_parameter'] = 'A'
        candidate = SCRATCH / f'{section_name}_{mutation}.json'
        candidate.write_text(json.dumps(payload, indent=2) + '\n')
        expected_variables = ('x', 'z') if section_name == 'homogeneous' else ('x', 'z', 's')
        record = {'section': section_name, 'mutation': mutation}
        record['mode_reader'], _ = outcome(lambda: mode.verify(candidate))
        record['exposition_reader'], _ = outcome(lambda: exposition.verify_modulus_source_polynomials(pareto_certificate=candidate))
        record['generator'], table = outcome(lambda: generator.cert_table('probe', section['variables'], section['terms'], section['term_count'], expected_variables, parameter))
        if mutation == 'baseline':
            baseline_tables[section_name] = table
        elif mutation == 'descriptive_metadata':
            assert table == baseline_tables[section_name]
            record['generated_table_unchanged'] = True
        if mutation in ['baseline', 'descriptive_metadata']:
            assert all(record[k]['status'] == 'ACCEPTED' for k in ['mode_reader', 'exposition_reader', 'generator']), record
        elif mutation in ['dual_conflict', 'dual_identical', 'only_wrong_field', 'missing_required', 'variable_swap']:
            assert all(record[k]['status'] == 'REJECTED' for k in ['mode_reader', 'exposition_reader', 'generator']), record
        elif mutation in ['wrong_coefficient', 'reversed_coefficients']:
            assert all(record[k]['status'] == 'REJECTED' for k in ['mode_reader', 'exposition_reader']), record
        else:
            assert record['mode_reader']['status'] == 'REJECTED', record
        records.append(record)

# The real no-check regeneration command must stop before changing its outputs.
regeneration = []
for section_name in ['homogeneous', 'spatial']:
    root = SCRATCH / f'regeneration_{section_name}'
    for directory in ['computation', 'data', 'figures', 'independent_verifier']:
        (root / directory).mkdir(parents=True, exist_ok=True)
    for relative in ['computation/generate_tables.py', 'data/current_profile_exact.json',
                     'independent_verifier/improved_modulus_certificate.json',
                     'data/contrast_table.tex', 'data/certificate_tables.tex', 'figures/contrast_table.csv']:
        shutil.copy2(SOURCE / relative, root / relative)
    shutil.copy2(SCRATCH / f'{section_name}_dual_conflict.json', root / 'independent_verifier/pareto_all_m_certificate.json')
    artifacts = ['data/contrast_table.tex', 'data/certificate_tables.tex', 'figures/contrast_table.csv']
    before = {name: (root / name).read_bytes() for name in artifacts}
    run = subprocess.run([sys.executable, str(root / 'computation/generate_tables.py')], capture_output=True, text=True)
    assert run.returncode != 0 and 'conflicting recognized' in run.stderr
    assert all((root / name).read_bytes() == value for name, value in before.items())
    regeneration.append({'section': section_name, 'returncode': run.returncode, 'diagnostic': run.stderr.splitlines()[-1], 'all_three_outputs_unchanged': True})

names = ['verify_mode_isolation.py', 'dd_verify_mode_isolation.py',
         'frontier_verify_mode_certificates.py', 'frontier_verify_exposition_identities.py', 'generate_tables.py']
canonical = {name: (SOURCE / ('computation' if name == 'generate_tables.py' else 'independent_verifier') / name).read_bytes() for name in names}
copies = []
for directory in ['independent_verifier', 'computation', 'external_audit/minimal_verifier',
                  'external_audit/packets/reaction_network/minimal_verifier',
                  'external_audit/packets/pde/minimal_verifier',
                  'external_audit/packets/symbolic/minimal_verifier', 'public/repository']:
    for file in (SOURCE / directory).rglob('*.py'):
        if file.name in canonical:
            assert file.read_bytes() == canonical[file.name], str(file)
            copies.append(str(file.relative_to(SOURCE)))
zip_copies = []
for line in (SOURCE / 'release/BUNDLE_SHA256.txt').read_text().splitlines():
    _digest, relative = line.split(maxsplit=1)
    with zipfile.ZipFile(SOURCE / relative) as archive:
        for name in archive.namelist():
            basename = Path(name).name
            if basename in canonical:
                assert archive.read(name) == canonical[basename], (relative, name)
                zip_copies.append({'archive': relative, 'member': name})

result = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'commit': '137ffa9f1a340f621651395ad0236cf1bdadb51c',
          'status': 'PASS', 'mutations': records, 'real_regeneration_controls': regeneration,
          'identical_current_unpacked_implementations': copies,
          'identical_current_zip_implementations': zip_copies,
          'counts': {'mutation_cases': len(records), 'reader_generator_calls': len(records)*3,
                     'real_regeneration_rejections': len(regeneration), 'unpacked_copies': len(copies), 'zip_copies': len(zip_copies)}}
(HERE / 'REPAIR_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result['counts'], indent=2))
