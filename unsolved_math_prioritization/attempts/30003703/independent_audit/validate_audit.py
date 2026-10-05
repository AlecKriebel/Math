#!/usr/bin/env python3
"""Read-only, offline replay of independent audit and exact release binding."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--release', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here/'AUDIT_MANIFEST.json').read_text())
    expected = {item['path'] for item in manifest['files']} | {'AUDIT_MANIFEST.json'}
    assert {p.name for p in here.iterdir()} == expected, 'Unexpected or missing audit item'
    for item in manifest['files']:
        raw = (here/item['path']).read_bytes()
        assert len(raw) == item['bytes'], item['path']
        assert hashlib.sha256(raw).hexdigest() == item['sha256'], item['path']
    from independent_controls import run, EXPECTED_MANIFEST
    assert manifest['subject_release_manifest_sha256'] == EXPECTED_MANIFEST
    binding = json.loads((here/'BINDING.json').read_text())
    assert binding['release_manifest']['sha256'] == EXPECTED_MANIFEST
    actual_release_items = {p.name for p in args.release.iterdir()}
    release_manifest = json.loads((args.release/'MANIFEST.json').read_text())
    expected_release_items = {x['path'] for x in release_manifest['files']} | {'MANIFEST.json'}
    assert actual_release_items == expected_release_items, 'Unexpected or missing release item'
    current = run(args.release)
    assert current == json.loads((here/'independent_results.json').read_text())
    negative = json.loads((here/'NEGATIVE_CONTROLS.json').read_text())
    assert negative['controls'] == current['negative_controls']
    assert len(negative['controls']) == negative['count'] == 12
    print(json.dumps({'result':'PASS','audit_files':len(manifest['files']),
                      'negative_controls':12,'release_files':current['binding']['files_verified'],
                      'verdict':binding['verdict'],'release_unchanged':True},sort_keys=True))


if __name__ == '__main__':
    main()
