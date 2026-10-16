#!/usr/bin/env python3
"""Read-only strict inventory, hash, replay and negative-control verifier."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess
import sys

PAYLOAD = {'SECOND_REVIEW.md', 'README.md', 'INPUTS.json', 'RESULTS.json',
           'four_region_certificate.py', 'verify_review.py'}


def require(condition, description):
    if not condition:
        raise ValueError(description)


def verify(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'Root must be a nonsymlink directory')
    entries = list(root.iterdir())
    require({p.name for p in entries} == PAYLOAD | {'MANIFEST.json'}, 'Strict inventory mismatch')
    for p in entries:
        require(stat.S_ISREG(p.lstat().st_mode), 'Nonregular entry: ' + p.name)
    manifest = json.loads((root/'MANIFEST.json').read_text())
    require(set(manifest) == {'schema', 'problem_id', 'files'}, 'Manifest keys')
    require(manifest['schema'] == 'weighted-yamabe-second-review-v1', 'Manifest schema')
    require(manifest['problem_id'] == 30001168, 'Manifest problem')
    records = manifest['files']
    require(isinstance(records, list) and len(records) == len(PAYLOAD), 'Manifest length')
    require({r['path'] for r in records} == PAYLOAD, 'Manifest inventory')
    for r in records:
        require(set(r) == {'path', 'bytes', 'sha256'}, 'Manifest record keys')
        data = (root/r['path']).read_bytes()
        require(len(data) == r['bytes'], 'Byte mismatch: ' + r['path'])
        require(hashlib.sha256(data).hexdigest() == r['sha256'], 'Hash mismatch: ' + r['path'])
    base = [sys.executable, '-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    script = root/'four_region_certificate.py'
    result = subprocess.run(base+[str(script)], capture_output=True, text=True, cwd=root.parent, timeout=60)
    require(result.returncode == 0 and not result.stderr, 'Arithmetic replay failed')
    require(result.stdout == (root/'RESULTS.json').read_text(), 'Exact replay mismatch')
    for argument, error in [("limit=Q(16,25)", 'round bound failed'), ('length=100', 'cylinder separation')]:
        code = "import runpy; from fractions import Fraction as Q; d=runpy.run_path(" + repr(str(script)) + "); d['calculate'](" + argument + ")"
        failed = subprocess.run(base+['-c',code], capture_output=True, text=True, cwd=root.parent, timeout=60)
        require(failed.returncode != 0 and error in failed.stderr, 'Mathematical negative control did not fail correctly')
    return {'verified': True, 'problem_id': 30001168, 'optimized': bool(sys.flags.optimize),
            'payload_files': len(PAYLOAD), 'analytic_time_regions': 4,
            'mathematical_negative_controls_rejected': 2,
            'manifest_sha256': hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    require(len(sys.argv) == 1, 'No command-line arguments supported')
    print(json.dumps(verify(Path(__file__).absolute().parent), indent=2, sort_keys=True))
