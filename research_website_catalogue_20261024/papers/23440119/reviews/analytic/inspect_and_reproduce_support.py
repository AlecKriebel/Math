"""Read original support, check manifest, and execute byte-identical local copies.

Deposited programs were fully read before this wrapper was written. They import
only standard-library arithmetic/metadata and emit stdout; no network/file-write
operations occur in them. Raw inputs and output remain in ignored quarantine.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / 'sources' / 'support'
QUARANTINE = HERE / 'quarantine'
QUARANTINE.mkdir(exist_ok=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024 * 1024, 16 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))


manifest = json.loads((SOURCE / 'SOURCE_MANIFEST.json').read_bytes())
inventory = {}
for path in sorted(SOURCE.rglob('*')):
    if path.is_file():
        rel = path.relative_to(SOURCE).as_posix()
        data = path.read_bytes()
        inventory[rel] = {'bytes': len(data), 'sha256': sha(data)}
        if rel != 'SOURCE_MANIFEST.json':
            assert inventory[rel] == manifest[rel], (rel, inventory[rel], manifest[rel])
assert set(inventory) == set(manifest) | {'SOURCE_MANIFEST.json'}

# Parse every deposited JSON document fully. Keep a compact schema/summary plus
# exact hash; repetitive test labels are checked against fresh execution below.
json_summaries = {}
for rel in inventory:
    if rel.endswith('.json'):
        value = json.loads((SOURCE / rel).read_bytes())
        json_summaries[rel] = {'type': type(value).__name__,
                               'keys': sorted(value) if isinstance(value, dict) else None,
                               'entries': len(value)}

scripts = ['check_geometry.py', 'curvature_reproduction.py']
for name in scripts:
    data = (SOURCE / 'verification' / name).read_bytes()
    (QUARANTINE / name).write_bytes(data)
    assert sha((QUARANTINE / name).read_bytes()) == sha(data)

commands = [
    ('geometry_normal', ['-I', '-B', 'check_geometry.py']),
    ('geometry_optimized', ['-I', '-B', '-O', 'check_geometry.py']),
    ('curvature_normal', ['-I', '-B', 'curvature_reproduction.py']),
    ('curvature_optimized_rejection', ['-I', '-B', '-O', 'curvature_reproduction.py']),
]
results = {}
env = {'PATH': '/usr/bin:/bin', 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONNOUSERSITE': '1'}
for label, args in commands:
    before = {p.name: sha(p.read_bytes()) for p in QUARANTINE.glob('*.py')}
    done = subprocess.run([sys.executable, *args], cwd=QUARANTINE, env=env,
                          capture_output=True, timeout=45, preexec_fn=limits)
    after = {p.name: sha(p.read_bytes()) for p in QUARANTINE.glob('*.py')}
    assert before == after
    (QUARANTINE / (label+'.stdout')).write_bytes(done.stdout)
    (QUARANTINE / (label+'.stderr')).write_bytes(done.stderr)
    result = {'args': args, 'returncode': done.returncode,
              'stdout_bytes': len(done.stdout), 'stderr_bytes': len(done.stderr),
              'stdout_sha256': sha(done.stdout), 'stderr_sha256': sha(done.stderr),
              'input_sha256_before_after': before}
    if label == 'curvature_optimized_rejection':
        assert done.returncode != 0 and not done.stdout
        assert b'requires enabled assertions' in done.stderr
        result['expected_startup_rejection'] = True
    else:
        assert done.returncode == 0 and not done.stderr
        result['parsed_stdout'] = json.loads(done.stdout)
    results[label] = result

expected = json.loads((SOURCE / 'verification' / 'expected_results.json').read_bytes())
print(json.dumps({'expected_results_keys': sorted(expected),
                  'normal_geometry_keys': sorted(results['geometry_normal']['parsed_stdout'])}, indent=2))

# Strip only machine/runtime fields identified by the deposit README.
def stable(obj):
    return {k:v for k,v in obj.items() if k not in
            {'checked_at_utc','python_version','optimization_mode','python'}}

g = stable(results['geometry_normal']['parsed_stdout'])
go = stable(results['geometry_optimized']['parsed_stdout'])
c = stable(results['curvature_normal']['parsed_stdout'])
assert g == go
assert g['checks_passed'] == 791 and g['negative_controls_rejected'] == 8
assert c['rational_grid_cases'] == 45
assert c['independent_bivariate_logarithm_series_contractions'] == 315

if set(expected) == {'geometry', 'curvature', 'geometry_optimized', 'curvature_optimized'}:
    assert stable(expected['geometry']) == g
    assert stable(expected['curvature']) == c
    assert expected['geometry_optimized'] == 'same checks PASS'
    assert expected['curvature_optimized'] == 'rejected at startup'
else:
    # Preserve the exact unknown schema for a review, rather than pretending a
    # comparison succeeded. The observed schema is interpreted in the next step.
    raise RuntimeError(('unrecognized expected-results schema', sorted(expected)))

report = {'utc': datetime.now(timezone.utc).isoformat(),
          'support_file_count': len(inventory), 'manifest_all_match': True,
          'originals_read_only': True,
          'execution_location': str(QUARANTINE),
          'network_or_external_writes_in_deposited_programs': False,
          'scripts_reviewed_before_execution': True,
          'all_expected_results_match': True,
          'inventory': inventory, 'json_summaries': json_summaries, 'runs': results}
(HERE/'support-reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'support_file_count': len(inventory), 'manifest_all_match': True,
                  'all_expected_results_match': True,
                  'geometry_checks': 791, 'adverse_controls': 8,
                  'curvature_grid':45, 'series_contractions':315,
                  'optimized_rejected':True}, indent=2))
