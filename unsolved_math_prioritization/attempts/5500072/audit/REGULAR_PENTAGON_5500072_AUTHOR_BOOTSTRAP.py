#!/usr/bin/env python3
"""Verify the frozen packet and replay in fresh directories; accepts no network input."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def fingerprint(raw):
    return {'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()}


def verify_tree(directory, manifest):
    files = manifest['files']
    got = sorted(p.name for p in Path(directory).iterdir() if p.is_file())
    require(got == sorted(files), 'Extracted member inventory mismatch')
    for name, expected in files.items():
        require(fingerprint((Path(directory)/name).read_bytes()) == expected,
                'Extracted member mismatch: '+name)


def main():
    ap = argparse.ArgumentParser()
    home = Path(__file__).resolve().parent
    ap.add_argument('--archive', type=Path, default=home/'REGULAR_PENTAGON_5500072_AUTHOR_SAFE_FREEZE.zip')
    ap.add_argument('--manifest', type=Path, default=home/'REGULAR_PENTAGON_5500072_AUTHOR_EXTERNAL_MANIFEST.json')
    ap.add_argument('--catalog')
    ap.add_argument('--problems')
    ap.add_argument('--reports')
    ap.add_argument('--source-dir')
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text())
    require(manifest['problem_id'] == 5500072, 'Manifest identity mismatch')
    require(fingerprint(Path(__file__).read_bytes()) == manifest['bootstrap'], 'Bootstrap byte mismatch')
    require(fingerprint(args.archive.read_bytes()) == manifest['archive'], 'Archive byte mismatch')
    forwarded = []
    for key in ['catalog', 'problems', 'reports', 'source_dir']:
        val = getattr(args, key)
        if val is not None:
            forwarded += ['--'+key.replace('_','-'), str(Path(val).resolve())]
    outputs = []
    with zipfile.ZipFile(args.archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'Duplicate archive members')
        require(set(names) == set(manifest['files']), 'Archive inventory mismatch')
        require(all(Path(n).name == n and n not in ['.', '..'] for n in names), 'Unsafe archive member path')
        for name in names:
            require(fingerprint(z.read(name)) == manifest['files'][name], 'Archive member mismatch: '+name)
        for optimized in [False, True]:
            with tempfile.TemporaryDirectory(prefix='regular-pentagon-replay-') as tmp:
                z.extractall(tmp)
                verify_tree(tmp, manifest)
                command = [sys.executable] + (['-O'] if optimized else [])
                command += [str(Path(tmp)/'diagnostics.py')] + forwarded
                run = subprocess.run(command, cwd=tmp, text=True, capture_output=True)
                require(run.returncode == 0, 'Diagnostic failure: '+run.stderr)
                result = json.loads(run.stdout)
                require(result['checks_passed'] and result['status'] == 'stalled_partial', 'Replay did not report partial success')
                outputs.append(result)
                verify_tree(tmp, manifest)
    require(outputs[0] == outputs[1], 'Normal/optimized replay differs')
    print(json.dumps({'problem_id':5500072,'archive_verified':True,'normal_optimized_identical':True,
                      'isolated_replays':2,'result':outputs[0]}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
