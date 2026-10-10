#!/usr/bin/env python3
"""Source-free integrity and replay checks, not a proof checker or source audit."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def manifest_check(base, name):
    entries = json.loads((base / name).read_text())['files']
    paths = set()
    for entry in entries:
        rel = Path(entry['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe manifest path')
        require(rel.as_posix() not in paths, 'Duplicate manifest path')
        paths.add(rel.as_posix())
        data = (base / rel).read_bytes()
        require(len(data) == entry['bytes'], 'Byte count: ' + str(rel))
        require(sha(data) == entry['sha256'], 'SHA-256: ' + str(rel))
    return paths

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--numerical', action='store_true',
                        help='Rerun the complete uncertified search in a temporary directory')
    args = parser.parse_args()
    paths = manifest_check(ROOT, 'MANIFEST.json')
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    require(actual == paths | {'MANIFEST.json'}, 'Packet allowlist mismatch')
    manifest_check(ROOT / 'author', 'MANIFEST.json')
    manifest_check(ROOT / 'review', 'MANIFEST.json')
    archive = ROOT / 'AUTHOR_30005600.zip'
    require(archive.stat().st_size == 25093, 'Archive size')
    require(sha(archive.read_bytes()) ==
            '891e8c125dbb0310074a63f83d4071712cc50bab1584c6153ae829a5d5ed7782', 'Archive pin')
    require(sha((ROOT / 'author/PROOF.md').read_bytes()) ==
            'c8bebb5be39bab1bbc1f2d28bbe99d021eeaf478499c3f385b1b689d3916c44b', 'Proof pin')
    require(sha((ROOT / 'review/AUDIT.md').read_bytes()) ==
            '76e8414f0f0b75a5623befc01ceae7bb37283520f94e108c6affd3cc7e5ffa33', 'Audit pin')
    require(sha((ROOT / 'review/SCOPE_CORRECTIONS.patch').read_bytes()) ==
            '5e1af7fa8603e35e840661152c154b606d1e1189bea64ac939c947e261a7a99e', 'Patch pin')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        expected = sorted('author/' + p.name for p in (ROOT / 'author').iterdir() if p.is_file())
        require(len(names) == len(set(names)) and sorted(names) == expected, 'Archive member list')
        for name in names:
            require(z.read(name) == (ROOT / name).read_bytes(), 'Archive member: ' + name)
    require(shutil.which('patch') is not None, 'Standard patch command is required')
    with tempfile.TemporaryDirectory(prefix='torus-30005600-') as folder:
        temp = Path(folder)
        (temp / 'author').mkdir()
        for name in ['PROOF.md', 'RESEARCH_LOG.md']:
            shutil.copyfile(ROOT / 'author' / name, temp / 'author' / name)
        p = subprocess.run(['patch', '--batch', '--forward', '--fuzz=0', '-p1',
                            '-i', str(ROOT / 'review/SCOPE_CORRECTIONS.patch')],
                           cwd=temp, capture_output=True, check=True)
        require(b'offset' not in p.stdout.lower() and b'fuzz' not in p.stdout.lower(),
                'Patch required offset or fuzz')
        for name in ['PROOF.md', 'RESEARCH_LOG.md']:
            require((temp / 'author' / name).read_bytes() ==
                    (ROOT / 'review/reading_copy' / name).read_bytes(), 'Corrected copy: ' + name)
        expected = (ROOT / 'author/EXACT_CHECKS.json').read_bytes()
        for options in [[], ['-O']]:
            p = subprocess.run([sys.executable, *options, str(ROOT / 'author/check_exact.py')],
                               cwd=temp, capture_output=True, check=True)
            require(p.stdout == expected, 'Exact replay mismatch: ' + repr(options))
        for name in ['EXACT_REPLAY.json', 'EXACT_OPTIMIZED_REPLAY.json']:
            require((ROOT / 'review' / name).read_bytes() == expected, 'Frozen exact receipt: ' + name)
        numerical = (ROOT / 'author/SEARCH_RESULTS.json').read_bytes()
        require((ROOT / 'review/replay/SEARCH_RESULTS.json').read_bytes() == numerical,
                'Frozen auditor numerical receipt')
        numerical_status = 'not_rerun; frozen auditor replay is byte-identical'
        if args.numerical:
            script = temp / 'search_conformal.py'
            shutil.copyfile(ROOT / 'author/search_conformal.py', script)
            env = dict(os.environ)
            for key in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                        'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS']:
                env[key] = '1'
            p = subprocess.run([sys.executable, str(script)], cwd=temp, env=env,
                               capture_output=True, check=True)
            result = (temp / 'SEARCH_RESULTS.json').read_bytes()
            require(result == numerical,
                    'Numerical replay mismatch; observed SHA-256 ' + sha(result))
            numerical_status = 'rerun_pass_byte_identical; floating point remains uncertified'
    print(json.dumps({
        'status': 'PASS',
        'manifest_archive_and_patch': 'PASS',
        'normal_and_optimized_exact_replays': 'PASS_byte_identical',
        'numerical_replay': numerical_status,
        'scope': 'integrity and finite computational controls only; no analytic proof verification',
        'excluded_checks': ['source-file retrieval and inspection', 'absent corpus content hashes',
                            'worldwide open status', 'novelty', 'rigorous spectral lower bounds'],
    }, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
