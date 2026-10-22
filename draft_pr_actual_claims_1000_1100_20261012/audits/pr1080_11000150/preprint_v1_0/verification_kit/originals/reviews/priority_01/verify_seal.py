#!/usr/bin/env python3
"""Read-only verification of the authored output seal and frozen source custody."""
from pathlib import Path
import hashlib
import json

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    b = Path(__file__).resolve().parent
    root = b.parents[4]
    assert (root/'AGENTS.md').is_file()
    seal = json.loads((b/'TERMINAL_SEAL.json').read_text())
    assert digest(b/'OUTPUT_PINS.json') == seal['output_pins_sha256']
    pins = json.loads((b/'OUTPUT_PINS.json').read_text())
    for r in pins['files']:
        p = b/r['path']
        assert p.stat().st_size == r['bytes']
        assert digest(p) == r['sha256']
    current = json.loads((b/'INPUT_PINS.json').read_text())
    for r in current['files']:
        p = root/r['path']
        assert p.stat().st_size == r['bytes']
        assert digest(p) == r['sha256']
    source = json.loads((b/'SOURCE_READ_SCOPE.json').read_text())
    for r in source['sources']:
        p = root/r['path']
        assert p.stat().st_size == r['bytes']
        assert digest(p) == r['sha256']
        assert digest(root/r['text_path']) == r['text_sha256']
    for r in source['renders']:
        p = root/r['path']
        assert p.stat().st_size == r['bytes']
        assert digest(p) == r['sha256']
    frozen = json.loads((b/'DERIVATION_FREEZE.json').read_text())
    for r in frozen['files']:
        assert digest(b/r['path']) == r['sha256']
    print(json.dumps({'status':'PASS','authored_outputs':len(pins['files']),
                      'current_frozen_inputs':len(current['files']),
                      'primary_full_source_pdfs':len(source['sources']),
                      'source_renders':len(source['renders']),
                      'derivation_freeze_unchanged':True},indent=2))

if __name__ == '__main__':
    main()
