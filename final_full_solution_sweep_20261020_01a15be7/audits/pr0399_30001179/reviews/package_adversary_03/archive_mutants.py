#!/usr/bin/env python3
"""Rehashed semantic archive mutations under inherited optimization; no providers."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
A = Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179')
R = A / 'reviews/package_adversary_03'
S = A.parents[1] / 'private/pr0399_package03'
B = S / 'extract/free-product-tensor-core-verification'
PYTHON = Path('/Users/alec/Documents/Math/.venv/bin/python3.9')


def reseal(root, relative):
    p = root / relative
    m = json.loads((root / 'FILES.json').read_text())
    entry = next(e for e in m['files'] if e['path'] == relative)
    entry.update(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    (root / 'FILES.json').write_text(json.dumps(m))


def main():
    results = []
    for mode, flags in [('normal', []), ('optimized', ['-O'])]:
        for mutant in ['nested_historical_assert', 'guarded_count_type', 'guarded_false_status']:
            with tempfile.TemporaryDirectory(dir=S, prefix='archive_mutant_') as directory:
                root = Path(directory) / 'bundle'
                shutil.copytree(B, root)
                if mutant == 'nested_historical_assert':
                    relative = 'original/check_density_chain.py'
                    p = root / relative
                    p.write_text('assert False, "reviewer03 nested assertion must execute"\n')
                    historical = root / 'original/PUBLIC_PACKET_MANIFEST.json'
                    manifest = json.loads(historical.read_text())
                    entries = manifest['files']
                    entry = entries['check_density_chain.py'] if isinstance(entries, dict) else next(
                        e for e in entries if e['path'] == 'check_density_chain.py')
                    entry.update(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                    historical.write_text(json.dumps(manifest))
                    reseal(root, relative)
                    reseal(root, 'original/PUBLIC_PACKET_MANIFEST.json')
                else:
                    relative = 'reviews/measure_ordinal/independent_controls.py'
                    output = {'status': 'PASS', 'exact_finite_checks': True} if mutant == 'guarded_count_type' else {'status': 'FAIL'}
                    (root / relative).write_text('import json\nprint(json.dumps('+repr(output)+'))\n')
                    reseal(root, relative)
                # Byte integrity must accept the updated manifest before replay fails.
                integrity = subprocess.run([str(PYTHON), *flags, '-B', str(root/'tools/integrity.py'), str(root)],
                                           capture_output=True, text=True)
                if integrity.returncode:
                    raise RuntimeError('Mutant did not reach semantic replay: '+integrity.stderr)
                env = dict(os.environ)
                env['PYTHONOPTIMIZE'] = '2'
                proc = subprocess.run([str(PYTHON), *flags, '-B', str(root/'tools/reproduce.py'), str(root)],
                                      capture_output=True, text=True, env=env)
                if proc.returncode == 0:
                    raise RuntimeError('Rehashed semantic mutant escaped: '+mutant)
                results.append({'mode': mode, 'mutant': mutant, 'rehash_integrity_accepted': True,
                                'inherited_PYTHONOPTIMIZE': '2', 'replay_rejected': True,
                                'diagnostic': proc.stderr[-1500:]})
    (R/'ARCHIVE_SEMANTIC_MUTANTS.json').write_text(json.dumps({'results': results,
        'scope': 'Six finite hostile rehashed failures. The wrapper is trusted source bound by the external frozen ZIP hash; self-manifests are not signatures.'}, indent=2)+'\n')
    print(json.dumps({'semantic_mutations_rejected': len(results)}))


if __name__ == '__main__':
    main()
