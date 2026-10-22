"""Verify a publication against a separately trusted manifest hash.
Usage: python -I -S [-O] verify_publication.py EXPECTED_MANIFEST_SHA256
Trusted interpreter, standard library, operating system and bootstrap required.
"""
import hashlib
import json
import pathlib
import stat
import subprocess
import sys
import tempfile

def need(ok, label):
    if not ok:
        raise RuntimeError('publication validation failed: ' + label)

need(sys.flags.isolated == 1 and sys.flags.no_site == 1, 'invoke_with_I_S')
need(len(sys.argv) == 2 and len(sys.argv[1]) == 64, 'external_manifest_pin_required')
root = pathlib.Path(__file__).resolve().parent
manifest_path = root / 'PUBLICATION_MANIFEST.json'
need(not manifest_path.is_symlink(), 'manifest_type')
mb = manifest_path.read_bytes()
need(hashlib.sha256(mb).hexdigest() == sys.argv[1], 'manifest_sha256')
manifest = json.loads(mb)
expected = {r['path']: r for r in manifest['files']}
need(len(expected) == len(manifest['files']) and 'verify_publication.py' in expected, 'manifest_inventory')
actual = set()
for p in root.rglob('*'):
    need(not p.is_symlink(), 'symlink')
    if p.is_dir():
        continue
    need(stat.S_ISREG(p.stat().st_mode), 'file_type')
    actual.add(p.relative_to(root).as_posix())
need(actual == set(expected) | {'PUBLICATION_MANIFEST.json'}, 'exact_file_inventory')
snapshot = {}
for n, r in expected.items():
    p = pathlib.PurePosixPath(n)
    need(not p.is_absolute() and '..' not in p.parts and '\\' not in n, 'member_path')
    b = (root / n).read_bytes()
    need(len(b) == r['bytes'], 'file_bytes:' + n)
    need(hashlib.sha256(b).hexdigest() == r['sha256'], 'file_sha256:' + n)
    snapshot[n] = b
# No payload code runs until the complete inventory and all bytes pass.
with tempfile.TemporaryDirectory(prefix='graph-nls-publication-') as td:
    work = pathlib.Path(td)
    for n, b in snapshot.items():
        p = work / n
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
    checks = []
    for stem in ('CORRECTED', 'INDEPENDENT_AUDIT'):
        for optimized in (False, True):
            name = 'GRAPH_NLS_30003521_' + stem + '_BOOTSTRAP.py'
            proc = subprocess.run([sys.executable, '-I', '-S', '-B'] + (['-O'] if optimized else []) + [str(work / 'releases' / name)], cwd=work, env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C.UTF-8'}, capture_output=True, text=True, timeout=180)
            need(proc.returncode == 0, 'bootstrap_execution:' + stem)
            result = json.loads(proc.stdout)
            need(result['integrity_before_payload_execution'] is True, 'integrity_result')
            if stem == 'CORRECTED':
                need(result['fail_closed_with_optimization'] is True and result['checker']['passed'] is True and result['checker']['count'] == 11 and all(v is True for v in result['checker']['checks'].values()), 'finite_checker_result')
            else:
                need(result['all_expected_control_results'] is True and result['control_count'] == 46 and result['original_optimization_failure_confirmed'] is True and result['corrected_release_accepted'] is True, 'audit_result')
            checks.append({'target': stem, 'optimized': optimized, 'passed': True})
print(json.dumps({'passed': True, 'manifest_sha256': sys.argv[1], 'verified_files': len(snapshot), 'integrity_before_payload_execution': True, 'replays': checks, 'scope': 'Finite integrity verification only; no PDE or full approximation theorem verified.'}, indent=2, sort_keys=True))
