#!/usr/bin/env python3
"""External pinned audit gate. Execute with Python -I -S -B."""
import hashlib
import json
import pathlib
import subprocess
import sys
PIN = '0dfc23c434add4b5d8d23a61712cfd646dfd85afc8439a7f59ad1242f39cf53a'
EXPECTED = set(['ACCEPTANCE.json', 'ACCEPTANCE.md', 'AUTHOR_REPLAY_OPTIMIZED_RESULTS.json', 'AUTHOR_REPLAY_RESULTS.json', 'CORPUS_REPLAY_OPTIMIZED_RESULTS.json', 'CORPUS_REPLAY_RESULTS.json', 'CORPUS_VERIFICATION.json', 'INDEPENDENT_DIAGNOSTICS.json', 'INDEPENDENT_DIAGNOSTICS_OPTIMIZED.json', 'MATHEMATICAL_AUDIT.md', 'PATCH_METADATA.json', 'README.md', 'SOURCE_VERIFICATION.json', 'independent_math.py', 'replay_author.py', 'verify_audit.py', 'verify_corpus.py', 'MANIFEST.json'])
def need(ok, message):
    if not ok:
        raise ValueError(message)
def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out
def main():
    need(sys.flags.isolated == 1 and sys.flags.no_site == 1, 'run with -I -S')
    need(len(sys.argv) == 2, 'one audit directory required')
    root = pathlib.Path(sys.argv[1]).absolute()
    need(root.is_dir() and not any(p.is_symlink() for p in (root, *root.parents)), 'invalid root')
    entries = list(root.iterdir())
    need({p.name for p in entries} == EXPECTED, 'closed inventory mismatch')
    need(all(p.is_file() and not p.is_symlink() for p in entries), 'nonregular member')
    raw = (root / 'MANIFEST.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'manifest pin mismatch')
    manifest = json.loads(raw, object_pairs_hook=unique)
    need(set(manifest) == {'schema', 'files'} and manifest['schema'] == 1, 'manifest shape')
    need(set(manifest['files']) == EXPECTED - {'MANIFEST.json'}, 'manifest inventory')
    for name, record in manifest['files'].items():
        need(set(record) == {'bytes', 'sha256'} and type(record['bytes']) is int, 'metadata shape')
        raw = (root / name).read_bytes()
        need(len(raw) == record['bytes'] and hashlib.sha256(raw).hexdigest() == record['sha256'], 'member pin mismatch')
    flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
    child = subprocess.run([sys.executable, *flags, str(root / 'verify_audit.py')], capture_output=True, text=True, timeout=30)
    need(child.returncode == 0 and not child.stderr, 'audit checker failed')
    print(child.stdout, end='')
if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print('REJECT: ' + str(exc), file=sys.stderr)
        sys.exit(2)
