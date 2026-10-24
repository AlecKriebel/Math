"""Run negative controls only in writable temporary copies; never alter the frozen package."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import replay

ROOT = Path(__file__).absolute().parent

def run(path, optimized=False):
    return subprocess.run([sys.executable, *(['-O'] if optimized else []), '-B', str(path/'replay.py')], capture_output=True, timeout=40)

def main():
    replay.inventory(ROOT)
    # Establish clean trusted baseline before mutation tests.
    for optimized in [False, True]:
        replay.require(run(ROOT, optimized).returncode == 0, 'baseline failed')
    results = []
    controls = ['missing_file','extra_file','symlink_manifest','fifo_manifest','directory_manifest',
                'hardlink_manifest','bool_schema','float_schema','bool_bytes','float_bytes','duplicate_key','tampered_math']
    with tempfile.TemporaryDirectory(prefix='fast_diffusion_controls_') as temp:
        base = Path(temp)
        for kind in controls:
            p = base/kind
            shutil.copytree(ROOT, p)
            for f in p.iterdir():
                f.chmod(0o644)
            p.chmod(0o755)
            mf = p/'MANIFEST.json'
            if kind == 'missing_file': (p/'README.md').unlink()
            elif kind == 'extra_file': (p/'EXTRA').write_text('x')
            elif kind == 'tampered_math': (p/'MATHEMATICAL_AUDIT.md').write_text('tampered')
            elif kind in ['symlink_manifest','fifo_manifest','directory_manifest','hardlink_manifest']:
                backup = base/(kind+'.json'); shutil.copyfile(mf, backup); mf.unlink()
                if kind == 'symlink_manifest': mf.symlink_to(backup)
                elif kind == 'fifo_manifest': os.mkfifo(mf)
                elif kind == 'directory_manifest': mf.mkdir()
                else: os.link(backup, mf)
            elif kind == 'duplicate_key': mf.write_text(mf.read_text().replace('"schema": 1', '"schema": 1, "schema": 1'))
            else:
                m = json.loads(mf.read_text())
                if kind == 'bool_schema': m['schema'] = True
                elif kind == 'float_schema': m['schema'] = 1.0
                elif kind == 'bool_bytes': m['files']['README.md']['bytes'] = True
                elif kind == 'float_bytes': m['files']['README.md']['bytes'] = float(m['files']['README.md']['bytes'])
                mf.write_text(json.dumps(m))
            for optimized in [False, True]:
                out = run(p, optimized)
                replay.require(out.returncode != 0, 'negative control accepted: '+kind)
                results.append({'control':kind, 'optimized':optimized, 'rejected':True})
        code = (ROOT/'CHECK_ADAPTIVE_IDENTITY.py').read_text()
        mutations = [
          ('missing_adaptive_factor', 'corrected = a*sigmap/sigma', 'corrected = sigmap/sigma'),
          ('wrong_remainder_scaling', '*(j-4*b*f)-R', '*(j-4*b*f)-sigma**(2*a)*R'),
          ('wrong_entropy_derivative_sign', 'sigmap-Cp)', 'sigmap+Cp)'),
          ('wrong_profile_velocity', 'trL/n-2*li', 'trL/n-3*li'),
        ]
        for name, old, new in mutations:
            replay.require(code.count(old) == 1, 'mutation anchor not unique')
            mutated = code.replace(old,new)
            f = base/(name+'.py'); f.write_text(mutated)
            for optimized in [False, True]:
                out = subprocess.run([sys.executable, *(['-O'] if optimized else []), '-B', str(f)], capture_output=True, timeout=30)
                replay.require(out.returncode != 0 and b'RuntimeError' in out.stderr, 'algebraic mutation escaped: '+name)
                results.append({'control':name, 'optimized':optimized, 'rejected':True,
                                'mutant_sha256':hashlib.sha256(mutated.encode()).hexdigest()})
    print(json.dumps({'status':'PASS', 'negative_controls':results, 'count':len(results),
                      'boundary':'No sockets or network; structural controls use temporary writable copies; algebraic controls execute mutated diagnostic directly, independently of integrity rejection.'}, indent=2))

if __name__ == '__main__': main()
