#!/usr/bin/env python3
"""Verify saved review closure and exact input bindings, without network access."""
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / 'MANIFEST.json').read_text())
    files = manifest['authored_files']
    actual = sorted(str(p.relative_to(base)) for p in base.rglob('*')
                    if p.is_file() and p.name != 'MANIFEST.json'
                    and 'tmp' not in p.relative_to(base).parts
                    and '__pycache__' not in p.relative_to(base).parts)
    require(actual == sorted(x['path'] for x in files), 'Review closure mismatch')
    for entry in files:
        data = (base / entry['path']).read_bytes()
        require(len(data) == entry['bytes'], 'Review byte count mismatch')
        require(hashlib.sha256(data).hexdigest() == entry['sha256'],
                'Review hash mismatch: ' + entry['path'])
    binding = json.loads((base / 'INPUT_BINDING.json').read_text())
    for entry in binding['inputs']:
        data = (base.parent / entry['path_from_audit']).read_bytes()
        require(len(data) == entry['bytes'], 'Input byte count mismatch')
        require(hashlib.sha256(data).hexdigest() == entry['sha256'],
                'Input hash mismatch: ' + entry['path_from_audit'])
    verdict = json.loads((base / 'VERDICT.json').read_text())
    require(verdict['reviewed_head'] == binding['reviewed_head'], 'Head mismatch')
    require(verdict['result'] == 'CONDITIONAL_PASS_CREDITED_ALTERNATIVE_PROOF',
            'Unexpected priority verdict')
    require(verdict['no_math_repairs_required'] is True, 'Unexpected repair gate')
    require(not (base / 'tmp').exists(), 'Private scratch remains')
    print(json.dumps({'result': 'PASS_CLOSED_REVIEW_AND_INPUT_BINDINGS',
                      'authored_files': len(files),
                      'input_bindings': len(binding['inputs']),
                      'meaning': 'Integrity check; not a simulated literature search or proof certificate.'},
                     indent=2))


if __name__ == '__main__':
    main()
