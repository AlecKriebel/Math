#!/usr/bin/env python3
"""Verify the exact safe packet against a separately pinned manifest hash."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest-sha256', required=True)
    args = p.parse_args()
    require(re.fullmatch('[0-9a-f]{64}', args.manifest_sha256) is not None, 'invalid external manifest hash')
    root = pathlib.Path(__file__).resolve().parent
    manifest_path = root / 'MANIFEST.json'
    require(not manifest_path.is_symlink(), 'manifest symlink forbidden')
    raw = manifest_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == args.manifest_sha256, 'external manifest pin mismatch')
    manifest = json.loads(raw)
    require(set(manifest) == {'schema','problem_id','files'}, 'manifest schema keys')
    require(manifest['schema'] == 'safe-author-packet-v1' and manifest['problem_id'] == 2811, 'manifest identity')
    files = manifest['files']
    require(isinstance(files, list) and len(files) > 0, 'manifest list required')
    names = []
    for rec in files:
        require(isinstance(rec, dict) and set(rec) == {'path','bytes','sha256'}, 'manifest entry schema')
        name = rec['path']
        require(isinstance(name,str) and re.fullmatch('[A-Za-z0-9_.-]+',name) is not None
                and name not in {'.','..','MANIFEST.json'}, 'unsafe or reserved payload path')
        require(isinstance(rec['bytes'],int) and not isinstance(rec['bytes'],bool) and rec['bytes'] >= 0, 'invalid size')
        require(isinstance(rec['sha256'],str) and re.fullmatch('[0-9a-f]{64}',rec['sha256']) is not None, 'invalid payload hash')
        names.append(name)
    require(len(names) == len(set(names)), 'duplicate payload path')
    actual = list(root.iterdir())
    require(all(x.is_file() and not x.is_symlink() for x in actual), 'non-file or symlink payload forbidden')
    require({x.name for x in actual} == set(names) | {'MANIFEST.json'}, 'unexpected or missing payload')
    for rec in files:
        b = (root / rec['path']).read_bytes()
        require(len(b) == rec['bytes'], 'payload size mismatch: '+rec['path'])
        require(hashlib.sha256(b).hexdigest() == rec['sha256'], 'payload hash mismatch: '+rec['path'])
    result = subprocess.run([sys.executable, '-B', str(root/'check_math.py')], check=False, capture_output=True)
    require(result.returncode == 0 and not result.stderr, 'math replay failed')
    require(result.stdout == (root/'CHECK_RESULTS.json').read_bytes(), 'math replay receipt mismatch')
    optimized = subprocess.run([sys.executable, '-B', '-O', str(root/'check_math.py')], check=False, capture_output=True)
    require(optimized.returncode == 0 and not optimized.stderr and optimized.stdout == result.stdout, 'optimized replay mismatch')
    print(json.dumps({'status':'PASS_PINNED_PACKET_AND_REPLAY','problem_id':2811,
                      'payload_files':len(files),'internal_manifest_sha256':args.manifest_sha256,
                      'normal_and_optimized_math_replays_identical':True},sort_keys=True,indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('REJECT: '+str(e), file=sys.stderr)
        sys.exit(1)
