#!/usr/bin/env python3
"""Check that altered, missing, injected and symlinked artifacts fail closed."""
import argparse, hashlib, importlib.util, json, shutil, sys, tempfile
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('release_validator', root / 'verify_publication.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    manifest = module.validate(root, args.expected_manifest)
    tests = []
    with tempfile.TemporaryDirectory(prefix='robinson-mutations-') as td:
        r = Path(td) / 'packet'
        shutil.copytree(root, r)
        def reject(label):
            try:
                module.validate(r, args.expected_manifest)
            except (RuntimeError, FileNotFoundError, ValueError, KeyError, TypeError):
                tests.append(label)
            else:
                raise RuntimeError('Mutation accepted: ' + label)
        for name in sorted(manifest['files']):
            f = r / name
            original = f.read_bytes()
            f.write_bytes(original + b'\nMUTATION\n')
            reject('changed: ' + name)
            f.write_bytes(original)
            f.unlink()
            reject('missing: ' + name)
            f.write_bytes(original)
        f = r / 'PUBLIC_MANIFEST.json'
        original = f.read_bytes()
        f.write_bytes(original + b'\n')
        reject('manifest anchor changed')
        f.write_bytes(original)
        extra = r / 'injected.txt'
        extra.write_text('unlisted content')
        reject('unlisted file')
        extra.unlink()
        extra.symlink_to(r / 'author/PROOF.md')
        reject('symlink')
        extra.unlink()
        module.validate(r, args.expected_manifest)
    module.validate(root, args.expected_manifest)
    print(json.dumps({'verdict': 'PASS', 'rejected_mutations': len(tests), 'controls': tests}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
