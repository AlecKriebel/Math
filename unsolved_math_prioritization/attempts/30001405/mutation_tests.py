#!/usr/bin/env python3
"""Adversarial byte/inventory/pin controls, including optimized execution."""
import argparse, hashlib, importlib.util, json, shutil, sys, tempfile
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--expected-manifest', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('definable_validator', root / 'verify_publication.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
manifest = validator.validate(root, args.expected_manifest)
tests = []
with tempfile.TemporaryDirectory(prefix='definable-quotient-mutations-') as temp:
    r = Path(temp) / 'packet'
    shutil.copytree(root, r)
    def reject(label, pin=None):
        try:
            validator.validate(r, args.expected_manifest if pin is None else pin)
        except (RuntimeError, OSError, ValueError, KeyError, TypeError):
            tests.append(label)
        else:
            raise RuntimeError('Mutation accepted: ' + label)
    reject('wrong external pin', '0' * 64)
    for name in sorted(manifest['files']):
        p = r / name
        original = p.read_bytes()
        p.write_bytes(original + b'\nALTERED\n')
        reject('altered: ' + name)
        p.write_bytes(original)
        p.unlink()
        reject('missing: ' + name)
        p.write_bytes(original)
    p = r / 'PUBLIC_MANIFEST.json'
    original_manifest = p.read_bytes()
    p.write_bytes(original_manifest + b'\n')
    reject('altered public manifest')
    p.unlink()
    reject('missing public manifest')
    p.symlink_to(root / 'PUBLIC_MANIFEST.json')
    reject('symlinked public manifest')
    p.unlink()
    p.write_bytes(original_manifest)
    extra = r / 'injected.txt'
    extra.write_text('unlisted content')
    reject('unlisted file')
    extra.unlink()
    extra.mkdir()
    reject('unlisted empty directory')
    extra.rmdir()
    extra.symlink_to(r / 'author/PROOF.md')
    reject('unlisted symlink')
    extra.unlink()
    p = r / 'author/PROOF.md'
    original = p.read_bytes()
    p.unlink()
    p.symlink_to(root / 'author/PROOF.md')
    reject('symlinked listed file')
    p.unlink()
    p.write_bytes(original)
    # Even a rehashed public manifest cannot replace the accepted author pin.
    altered = original + b'\nALTERED PROOF\n'
    p.write_bytes(altered)
    changed = json.loads(original_manifest)
    changed['files']['author/PROOF.md'] = {'bytes': len(altered), 'sha256': hashlib.sha256(altered).hexdigest()}
    raw = (json.dumps(changed, indent=2) + '\n').encode()
    (r / 'PUBLIC_MANIFEST.json').write_bytes(raw)
    reject('rehashed manifest cannot change accepted proof', hashlib.sha256(raw).hexdigest())
    p.write_bytes(original)
    (r / 'PUBLIC_MANIFEST.json').write_bytes(original_manifest)
    validator.validate(r, args.expected_manifest)
validator.validate(root, args.expected_manifest)
print(json.dumps({'status': 'PASS', 'rejected_mutations': len(tests), 'optimized': bool(sys.flags.optimize), 'tests': tests}, indent=2, sort_keys=True))
