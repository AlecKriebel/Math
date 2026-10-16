#!/usr/bin/env python3
"""Replay intentional verifier failures in normal and optimized child processes.

Standard library only. Writes JSON to stdout and creates no receipt implicitly.
This is a finite fault-rejection harness, not a proof of the universal theorem.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXPECTED_SOURCE_SHA256 = 'dfa1ff339e1f3a6004563aec9c01f6f14d6bb65a94e2437f3ba3a41e5b393d85'
FAULTS = ('wrong-area','wrong-product','empty-polygon','colliding-polygon',
          'nan-coordinate','inf-coordinate','bool-coordinate','wrong-period',
          'bool-repetition','fraction-repetition','missing-count',
          'wrong-physical-area','wrong-physical-product')

def main():
    source = Path(__file__).resolve().with_name('portable_exact_verifier.py')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise RuntimeError('Pinned verifier source differs')
    attempts = []
    for optimized in (False, True):
        flags = ['-E','-S','-B','-P'] + (['-O'] if optimized else [])
        for fault in FAULTS:
            command = [sys.executable] + flags + [str(source),'--fault',fault]
            run = subprocess.run(command, capture_output=True, text=True, timeout=60)
            result = json.loads(run.stdout)
            if (run.returncode != 1 or result.get('status') != 'FAIL' or
                    result.get('runtime',{}).get('source_sha256') != digest or run.stderr):
                raise RuntimeError('Intentional fault did not reject cleanly: '+fault)
            attempts.append({'flags':flags,'arguments':['portable_exact_verifier.py','--fault',fault],
                             'expected_exit':1,'actual_exit':run.returncode,
                             'stdout':run.stdout,'stderr':run.stderr})
    print(json.dumps({'status':'PASS','meaning':'all intentional faults rejected',
                      'attempt_count':len(attempts),'modes':['normal','optimized'],
                      'verifier_source_sha256':digest,
                      'harness_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'python':sys.version,'flags':repr(sys.flags),
                      'limits':'Finite negative controls only; not human peer review or a universal proof certificate.',
                      'attempts':attempts},indent=2,sort_keys=True,allow_nan=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status':'FAIL','error_type':type(error).__name__,
                          'error':str(error)},allow_nan=False))
        raise SystemExit(1)
