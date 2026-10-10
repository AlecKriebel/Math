#!/usr/bin/env python3
"""Reproduce freeze, non-root read-only, optimization, and mutation checks.

Usage: python run_audit.py /path/to/frozen/public /path/to/writable/output
Outputs contain authored-program checks and hash metadata only.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint(folder):
    return {f.name: {'bytes': f.stat().st_size, 'sha256': sha(f.read_bytes())}
            for f in sorted(folder.iterdir()) if f.is_file()}


def main():
    check(len(sys.argv) == 3, 'supply frozen public and writable output directory')
    frozen, output = [Path(p).resolve() for p in sys.argv[1:]]
    check(os.getuid() == os.geteuid() == 1000, 'genuine non-root UID/EUID 1000 required')
    output.mkdir(parents=True, exist_ok=True)
    before = fingerprint(frozen)
    check(len(before) == 9 and sum(r['bytes'] for r in before.values()) == 67843,
          'frozen file count and total byte count')
    check(before['MANIFEST.sha256']['sha256'] ==
          'a8cd4866d04bba62d53083e3e3f353e90974d955f09218f59244687f6d9152e4',
          'frozen manifest identity')
    for line in (frozen/'MANIFEST.sha256').read_text().splitlines():
        digest, name = line.split('  ')
        check(before[name]['sha256'] == digest, 'candidate manifest member '+name)
    original = (frozen/'verify.py').read_text()
    independent = Path(__file__).with_name('independent_verify.py').read_text()
    check(not any(isinstance(n, ast.Assert) for body in (original, independent)
                  for n in ast.walk(ast.parse(body))), 'no optimized-away Python asserts')
    ro = output/'readonly'
    ro.mkdir()
    (ro/'candidate.py').write_text(original)
    (ro/'independent.py').write_text(independent)
    for p in ro.iterdir():
        p.chmod(0o444)
    ro.chmod(0o555)
    probe = """import json,os
result={'uid':os.getuid(),'euid':os.geteuid(),'directory_mode':oct(os.stat('.').st_mode & 0o777),'directory_writable':os.access('.',os.W_OK)}
try:
    open('must_not_be_created','x').close()
    result['creation_denied']=False
except PermissionError:
    result['creation_denied']=True
print(json.dumps(result,sort_keys=True))
"""
    p = subprocess.run([sys.executable, '-c', probe], cwd=ro, capture_output=True)
    check(p.returncode == 0, 'readonly probe executable')
    probe_result = json.loads(p.stdout)
    check(probe_result['uid'] == probe_result['euid'] == 1000 and
          probe_result['creation_denied'] and not probe_result['directory_writable'],
          'readonly permission denial is real')
    frozen_saved = (frozen/'verification_results.json').read_bytes()
    runs = []
    outputs = {}
    for script in ('candidate', 'independent'):
        for flags in ([], ['-O'], ['-OO']):
            run = subprocess.run([sys.executable]+flags+[script+'.py'],
                                 cwd=ro, capture_output=True)
            check(run.returncode == 0 and not run.stderr, 'clean read-only run '+script+str(flags))
            if script == 'candidate':
                check(run.stdout == frozen_saved, 'candidate output byte-exact to freeze')
            if script in outputs:
                check(run.stdout == outputs[script], 'optimization output equality '+script)
            outputs[script] = run.stdout
            runs.append({'program': script, 'flags': flags, 'exit_code': run.returncode,
                         'output_bytes': len(run.stdout), 'sha256': sha(run.stdout)})
    independent_result = json.loads(outputs['independent'])
    check(independent_result['finite_group']['orbit_sizes'] == [216, 144], 'independent exact orbits')
    (output/'independent_results.json').write_bytes(outputs['independent'])
    cases = [
        ('candidate', 'collapse_first_generator', 'A = (1, 1, 0, 1)', 'A = (1, 0, 0, 1)', 'RuntimeError'),
        ('candidate', 'remove_partial_conjugator', 'P = (0, 1, 2, 0)', 'P = (1, 0, 0, 1)', 'RuntimeError'),
        ('candidate', 'wrong_saturation_pairing', 'saturated=((-r,1),(1,0))', 'saturated=((-r,2),(2,0))', 'RuntimeError'),
        ('candidate', 'wrong_canonical_coefficient', 'ky=(2,3*r-2)', 'ky=(2,3*r-1)', 'RuntimeError'),
        ('candidate', 'wrong_signature', 'sig=-24*r', 'sig=-24*r+1', 'RuntimeError'),
        ('candidate', 'wrong_pencil_nodes', 'nodes=e+d*(3*k*k+2*k)', 'nodes=e+d*(3*k*k+3*k)', 'RuntimeError'),
        ('candidate', 'wrong_hurwitz_inverse', 'qconj(qinv(b),a)', 'qconj(b,a)', 'RuntimeError'),
        ('candidate', 'wrong_formal_canonical_vector', 'kval=[3]*(4*r-1)', 'kval=[2]*(4*r-1)', 'RuntimeError'),
        ('candidate', 'truncate_orbit_to_seed', 'return seen\n\n\ndef check_finite_example', 'return {t}\n\n\ndef check_finite_example', 'saved_output_mismatch'),
        ('independent', 'wrong_orbit_cardinality', '== [216, 144]', '== [216, 143]', 'RuntimeError'),
        ('independent', 'wrong_saturation_pairing', 'saturation = ((-r, 1), (1, 0))', 'saturation = ((-r, 2), (2, 0))', 'RuntimeError'),
        ('independent', 'wrong_pencil_nodes', 'euler+base-4+4*genus', 'euler+base-4+5*genus', 'RuntimeError'),
        ('independent', 'wrong_hurwitz_inverse', 'conjugate(inverse(y), x)', 'conjugate(y, x)', 'RuntimeError'),
        ('independent', 'wrong_canonical_coefficient', 'ky = (2, 3*r-2)', 'ky = (2, 3*r-1)', 'RuntimeError'),
        ('independent', 'collapse_partial_conjugation', 'tp = (conjugate(p, a), conjugate(p, b), inverse(b), inverse(a))', 'tp = t', 'RuntimeError'),
    ]
    mutation_results = []
    for program, name, old, new, expected in cases:
        source = original if program == 'candidate' else independent
        check(source.count(old) == 1, 'mutation has exactly one target: '+name)
        path = output/(program+'_'+name+'.py')
        path.write_text(source.replace(old, new))
        result = {'program': program, 'mutation': name, 'expected_rejection': expected, 'runs': []}
        for flags in ([], ['-O'], ['-OO']):
            run = subprocess.run([sys.executable]+flags+[str(path)], cwd=ro, capture_output=True)
            if expected == 'RuntimeError':
                check(run.returncode != 0 and b'RuntimeError:' in run.stderr,
                      'meaningful fail-closed mutation '+name+str(flags))
            else:
                check(run.returncode == 0 and run.stdout != frozen_saved,
                      'strict output comparator rejects omitted orbit closure '+str(flags))
            result['runs'].append({'flags': flags, 'exit_code': run.returncode,
                                   'stdout_sha256': sha(run.stdout),
                                   'failure': run.stderr.decode().splitlines()[-1] if run.stderr else 'strict saved-output comparison rejected changed orbit sizes'})
        mutation_results.append(result)
    check(fingerprint(frozen) == before, 'frozen candidate unchanged after every test')
    check(sorted(p.name for p in ro.iterdir()) == ['candidate.py', 'independent.py'],
          'no state created in read-only execution directory')
    record = {'status': 'passed', 'python_version': platform.python_version(),
              'frozen_files': before, 'frozen_file_count': 9, 'frozen_total_bytes': 67843,
              'freeze_unchanged': True, 'readonly_probe': probe_result,
              'readonly_runs': runs, 'mutations': mutation_results,
              'mutation_count': len(cases), 'mutation_executions': 3*len(cases),
              'independent_result': independent_result,
              'limits': ['Finite arithmetic supplements mathematical argument, not induction.',
                         'The finite example is not a quotient of actual Horikawa monodromy.',
                         'No surface diffeomorphism or canonical symplectomorphism has been computed.']}
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
