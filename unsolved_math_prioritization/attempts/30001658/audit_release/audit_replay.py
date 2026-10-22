#!/usr/bin/env python3
"""Replay pinned author and independent checks without altering source files."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SOURCE_PIN = '68a1fa6b5900a7cc03cd2d991e1a135afb2366a169b680ad5ac9db335203ed68'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def snapshot(root):
    paths = sorted(root.iterdir())
    require(all(p.is_file() and not p.is_symlink() for p in paths), 'Nonregular source entry')
    return [{'path':p.name,'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in paths]

def run(path, optimized=False, args=()):
    command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(path)] + list(args)
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source-dir', type=Path)
    args = ap.parse_args()
    own = Path(__file__).resolve().parent
    source = args.source_dir.resolve() if args.source_dir else own.parent/'release'
    binding = json.loads((own/'INPUT_BINDING.json').read_bytes())
    initial = snapshot(source)
    require(initial == binding['files'], 'Source binding differs')
    require(len(initial) == 9 and sum(e['bytes'] for e in initial) == 41351, 'Source inventory')
    require(sha((source/'MANIFEST.json').read_bytes()) == SOURCE_PIN == binding['source_manifest_sha256'],
            'Source manifest pin')
    results = {}
    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        author = run(source/'verify_packet.py', optimized, ['--expected-manifest-sha256', SOURCE_PIN])
        require(author.returncode == 0 and not author.stderr, 'Author replay failed: '+mode)
        parsed = json.loads(author.stdout)
        require(parsed['mathematical_checks'] == 704115 and parsed['integrity_negative_controls'] == 8
                and parsed['mathematical_negative_controls'] == 6, 'Author result counts')
        independent = run(own/'independent_checks.py', optimized)
        require(independent.returncode == 0 and not independent.stderr, 'Independent replay failed: '+mode)
        require(independent.stdout == (own/'INDEPENDENT_RESULTS.json').read_bytes(), 'Independent frozen output changed')
        independent_parsed = json.loads(independent.stdout)
        require(independent_parsed['total_checks'] == 1282085, 'Independent result counts')
        # Actual filesystem contaminants, not only in-memory manifest mutations.
        filesystem = {}
        for kind in ('empty_directory', 'extra_symlink', 'replacement_symlink'):
            with tempfile.TemporaryDirectory(prefix='boolean-audit-') as td:
                copy = Path(td)/'release'
                shutil.copytree(source, copy)
                if kind == 'empty_directory':
                    (copy/'empty').mkdir()
                elif kind == 'extra_symlink':
                    (copy/'extra_link').symlink_to('PROOF.md')
                else:
                    (copy/'PROOF.md').unlink()
                    (copy/'PROOF.md').symlink_to(source/'PROOF.md')
                rejected = run(copy/'verify_packet.py', optimized, ['--expected-manifest-sha256', SOURCE_PIN])
                require(rejected.returncode != 0, 'Contaminated filesystem accepted: '+kind)
                require(b'Directories and symlinks are forbidden' in rejected.stderr,
                        'Unexpected failure instead of filesystem rejection: '+kind)
                filesystem[kind] = 'rejected_by_strict_filesystem_guard'
        results[mode] = {'author':parsed,
                         'author_stdout_sha256':sha(author.stdout),
                         'independent_total_checks':independent_parsed['total_checks'],
                         'independent_stdout_sha256':sha(independent.stdout),
                         'independent_mathematical_negative_controls':len(independent_parsed['mathematical_negative_controls']),
                         'filesystem_negative_controls':filesystem}
    require(snapshot(source) == initial, 'Original source packet changed during audit')
    print(json.dumps({'status':'PASS_PINNED_REPLAY_AND_FILESYSTEM_CONTROLS',
                      'source_manifest_sha256':SOURCE_PIN,
                      'source_files':9,'source_bytes':41351,
                      'source_unchanged':True,'modes':results},sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
