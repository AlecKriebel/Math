#!/usr/bin/env python3
"""Exercise changed readers and inventory the current distributed copies."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import sys
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source_snapshot'
sys.path.insert(0, str(SOURCE / 'independent_verifier'))
SCRATCH = HERE / 'scratch' / 'variables'
SCRATCH.mkdir(parents=True, exist_ok=True)

def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

unit_reader = load('variable_unit', 'independent_verifier/verify_mode_isolation.py')
duplicate_reader = load('variable_duplicate', 'independent_verifier/dd_verify_mode_isolation.py')
scaled_reader = load('variable_scaled', 'independent_verifier/frontier_verify_mode_certificates.py')
exposition = load('variable_exposition', 'independent_verifier/frontier_verify_exposition_identities.py')
generator = load('variable_generator', 'computation/generate_tables.py')
results = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'source_commit': '953c836a12b9d9d474521feb4a96e218c1155203',
           'negative_controls': []}

for filename, section_path, expected in [
    ('improved_modulus_certificate.json', ['homogeneous'], ['x', 'z']),
    ('improved_modulus_certificate.json', ['improved_mode'], ['x', 'z', 's']),
    ('pareto_all_m_certificate.json', ['modulus', 'homogeneous'], ['x', 'z']),
    ('pareto_all_m_certificate.json', ['modulus', 'spatial'], ['x', 'z', 's']),
]:
    payload = json.loads((SOURCE / 'independent_verifier' / filename).read_text())
    section = payload
    for name in section_path:
        section = section[name]
    section['variables'][0], section['variables'][1] = section['variables'][1], section['variables'][0]
    candidate = SCRATCH / (filename + '_'.join(section_path))
    candidate.write_text(json.dumps(payload))
    scaled = filename.startswith('pareto')
    functions = [('generator', lambda: generator.cert_table('probe', section['variables'], section['terms'], section['term_count'], expected, scaled))]
    if scaled:
        functions += [('scaled_reader', lambda: scaled_reader.verify(candidate)),
                      ('exposition_reader', lambda: exposition.verify_modulus_source_polynomials(pareto_certificate=candidate))]
    else:
        functions += [('unit_reader', lambda: unit_reader.verify_certificate(candidate)),
                      ('duplicate_reader', lambda: duplicate_reader.verify_certificate(candidate)),
                      ('exposition_reader', lambda: exposition.verify_modulus_source_polynomials(unit_certificate=candidate))]
    for label, function in functions:
        try:
            function()
        except (AssertionError, ValueError):
            status = 'REJECTED'
        else:
            status = 'ACCEPTED'
        results['negative_controls'].append({'section': '.'.join(section_path), 'file': filename, 'reader': label, 'result': status})
        assert status == 'REJECTED', results['negative_controls'][-1]

names = ['verify_mode_isolation.py', 'dd_verify_mode_isolation.py',
         'frontier_verify_mode_certificates.py', 'frontier_verify_exposition_identities.py',
         'generate_tables.py']
canonical = {name: (SOURCE / ('computation' if name == 'generate_tables.py' else 'independent_verifier') / name).read_bytes() for name in names}
copies = []
for directory in ['independent_verifier', 'computation', 'external_audit/minimal_verifier',
                  'external_audit/packets/reaction_network/minimal_verifier',
                  'external_audit/packets/pde/minimal_verifier',
                  'external_audit/packets/symbolic/minimal_verifier', 'public/repository']:
    for path in (SOURCE / directory).rglob('*.py'):
        if path.name not in canonical:
            continue
        contents = path.read_bytes()
        assert contents == canonical[path.name], str(path)
        copies.append({'path': str(path.relative_to(SOURCE)), 'sha256': hashlib.sha256(contents).hexdigest(), 'matches_canonical': True})

zip_copies = []
for line in (SOURCE / 'release/bundle_sha256.txt').read_text().splitlines():
    _digest, relative = line.split(maxsplit=1)
    with zipfile.ZipFile(SOURCE / relative) as archive:
        for path in archive.namelist():
            name = Path(path).name
            if name not in canonical:
                continue
            contents = archive.read(path)
            assert contents == canonical[name], (relative, path)
            zip_copies.append({'archive': relative, 'path': path, 'sha256': hashlib.sha256(contents).hexdigest(), 'matches_canonical': True})
results['current_unpacked_copies'] = copies
results['current_zip_copies'] = zip_copies
results['counts'] = {'negative_controls_rejected': len(results['negative_controls']), 'current_unpacked_copies': len(copies), 'current_zip_copies': len(zip_copies)}
results['historical_exclusion'] = 'Named full_referee_validation_packet_v1.0.7 and prior referee snapshots are historical; absent from seven current bundle manifest and nine current release assets.'
(HERE / 'ORDERED_VARIABLE_RESULTS.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results['counts'], indent=2))
