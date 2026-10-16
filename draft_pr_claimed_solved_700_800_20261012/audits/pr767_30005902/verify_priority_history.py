"""Read-only portable custody and arithmetic replay; independent of mtimes.

Use python3 -B or PYTHONDONTWRITEBYTECODE=1. Original sealed packets remain
unchanged. Filesystem creation timestamps are not mathematical evidence.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    receipts = []
    for family, pin in [
        ('priority_audit', '23c40037c5ac92211c5f86103decce7b4050115f53eaf9b2ecc136ec4ee3b067'),
        ('priority_adversary01', '3fe15309cc91a67545093089763b500bee6dd555690e305683f15b833cc33a91'),
    ]:
        directory = root / family
        raw = (directory / 'MANIFEST.json').read_bytes()
        need(sha(raw) == pin, 'Pinned manifest changed: ' + family)
        manifest = json.loads(raw)['files']
        expected = manifest if isinstance(manifest, dict) else {
            row['path']: {key: row[key] for key in ('bytes', 'sha256')} for row in manifest}
        need(len(expected) == len(manifest), 'Duplicate manifest entry')
        actual = {}
        for parent, directories, files in os.walk(directory, followlinks=False):
            need(bool(directories or files), 'Empty authored directory')
            for name in directories + files:
                path = Path(parent) / name
                mode = path.lstat().st_mode
                need(stat.S_ISDIR(mode) or stat.S_ISREG(mode), 'Symlink or special node')
            for name in files:
                path = Path(parent) / name
                relative = path.relative_to(directory).as_posix()
                if relative == 'MANIFEST.json':
                    continue
                data = path.read_bytes()
                actual[relative] = {'bytes': len(data), 'sha256': sha(data)}
        need(actual == expected, 'Exact recursive custody mismatch: ' + family)
        receipts.append({'family': family, 'manifest_sha256': pin, 'authored_files': len(actual),
                         'authored_bytes': sum(row['bytes'] for row in actual.values())})
    results = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for script, expected_file in [
        ('verify_implications.py', 'implication_results.json'),
        ('adversary/check_heisenberg.py', 'adversary/CHECK_RESULTS.json'),
    ]:
        directory = root / 'priority_audit'
        expected = (directory / expected_file).read_bytes()
        for optimized in (False, True):
            args = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(directory / script)]
            result = subprocess.run(args, capture_output=True, env=env)
            need(result.returncode == 0, result.stderr.decode())
            need(result.stdout == expected, 'Arithmetic replay differs: ' + script)
            results.append({'script': script, 'optimized': optimized, 'stdout_sha256': sha(expected)})
    print(json.dumps({'result': 'PASS', 'scope': 'Portable byte custody and supplemental exact arithmetic; no timestamp, network, Git, or adjacent private-input requirement',
                      'packets': receipts, 'replays': results}, sort_keys=True))


if __name__ == '__main__':
    main()
