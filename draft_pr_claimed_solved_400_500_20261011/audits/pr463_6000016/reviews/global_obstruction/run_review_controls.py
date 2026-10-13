#!/usr/bin/env python3
"""Run authored algebra and eight intentional in-memory false-claim controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    code = Path(__file__).resolve().with_name('check_global_obstruction.py')
    cases = ('connection_sign','covariant_sign','drop_second_covariant_slot',
             'holonomy_half','geodesic_sign','pseudo_potential_cubic',
             'pretend_local_positive_descends','pretend_indefinite_is_positive')
    results = []
    valid = []
    for optimized in (False,True):
        prefix = [sys.executable]+(['-O'] if optimized else [])+[str(code)]
        good = subprocess.run(prefix,capture_output=True,check=False)
        require(good.returncode == 0,'Valid algebra rejected')
        require(good.stderr == b'','Valid algebra wrote unexpected stderr')
        parsed = json.loads(good.stdout)
        require(parsed['verdict'] == 'PASS','Valid algebra verdict mismatch')
        require(type(parsed['check_count']) is int and parsed['check_count'] == len(parsed['checks']),'Invalid count')
        require(len(set(parsed['checks'])) == len(parsed['checks']),'Duplicate check names')
        valid.append(good.stdout)
        results.append({'mode':'optimized' if optimized else 'normal','case':'valid',
                        'exit':0,'checks':parsed['check_count'],
                        'stdout_sha256':hashlib.sha256(good.stdout).hexdigest()})
        for name in cases:
            bad = subprocess.run(prefix+['--corrupt',name],capture_output=True,check=False)
            require(bad.returncode == 4,'False claim was not rejected: '+name)
            require(bad.stdout == b'','False claim emitted success data: '+name)
            require(bad.stderr.startswith(b'InvalidClaim: '),'False claim rejection type mismatch: '+name)
            results.append({'mode':'optimized' if optimized else 'normal','case':name,
                            'exit':bad.returncode,'rejected_as':'InvalidClaim',
                            'stderr_sha256':hashlib.sha256(bad.stderr).hexdigest()})
    require(valid[0] == valid[1],'Normal and optimized valid output differ')
    print(json.dumps({'verdict':'PASS','valid_runs':2,'false_claim_rejections':16,
                      'exact_checks_per_valid_run':json.loads(valid[0])['check_count'],
                      'byte_identical_valid_modes':True,
                      'source_sha256':hashlib.sha256(code.read_bytes()).hexdigest(),
                      'sympy_version':__import__('sympy').__version__,
                      'external_service_calls':0,'results':results},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
