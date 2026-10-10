#!/usr/bin/env python3
"""Fail-closed frozen-package and finite-certificate replay."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
from pathlib import Path

FILES = {'README.md','PROOF.md','APPROACHES.md','SOURCES.json','QA.md',
         'exact_geometry.py','results.json','verify.py','test_fail_closed.py'}


def check(ok, msg):
    if not ok:
        raise ValueError(msg)


def unique_object(pairs):
    d = {}
    for k,v in pairs:
        check(k not in d, 'duplicate JSON key')
        d[k] = v
    return d


def read_json(p):
    return json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def main():
    check(len(sys.argv) == 1, 'no bypass flags or external input paths accepted')
    root = Path(__file__).resolve().parent
    check(not any(p.is_symlink() for p in root.iterdir()), 'symlink in package')
    actual = {p.name for p in root.iterdir()}
    check(actual == FILES | {'MANIFEST.json'}, 'unexpected or missing package member')
    manifest = read_json(root/'MANIFEST.json')
    check(set(manifest) == {'schema','status','files'}, 'manifest schema')
    check(manifest['schema'] == 1 and type(manifest['schema']) is int, 'schema version')
    check(manifest['status'] == 'PARTIAL_UNSOLVED', 'manifest overclaim')
    check(set(manifest['files']) == FILES, 'manifest allowlist')
    verified_bytes = {}
    for name in sorted(FILES):
        p = root/name
        check(p.is_file(), 'not a regular file')
        entry = manifest['files'][name]
        check(set(entry) == {'bytes','sha256'}, 'manifest entry fields')
        b = p.read_bytes()
        check(type(entry['bytes']) is int and entry['bytes'] == len(b), 'byte mismatch: '+name)
        check(entry['sha256'] == hashlib.sha256(b).hexdigest(), 'hash mismatch: '+name)
        verified_bytes[name] = b
    # Execute the exact verified source bytes; never consult Python bytecode caches.
    geometry = {'__name__': 'verified_exact_geometry', '__file__': str(root/'exact_geometry.py')}
    exec(compile(verified_bytes['exact_geometry.py'], geometry['__file__'], 'exec'), geometry)
    expected_results = geometry['expected_results']
    actual_results = read_json(root/'results.json')
    expected = expected_results()
    canon = lambda d: json.dumps(d, sort_keys=True, separators=(',',':'), allow_nan=False)
    check(canon(actual_results) == canon(expected), 'certificate/result mismatch')
    src = read_json(root/'SOURCES.json')
    claims = {'full_resolution', 'independent_audit_claimed', 'novelty_asserted',
              'remote_mutation_performed', 'source_documents_in_package'}
    check(set(src['claims']) == claims and all(src['claims'][key] is False for key in claims),
          'source overclaim')
    check(src['problem_id'] == 30000638 and src['problem_number'] == 'OWR-1394-015', 'source target')
    check(src['record_review']['sha256'] == '7c16b99985deb840b0695c618ce1f79f12c7da37eaecaa1e33145695b89756e6', 'review identity')
    check(src['record_review']['bytes'] == 3670, 'review size')
    check(src['record_review']['report_present'] is False, 'absent report convention')
    check(src['resolution_status'] == 'No authoritative complete resolution located in the stated bounded search.', 'source status')
    print(json.dumps({'status':'PASS_PARTIAL','geometric_cases':37,'residue_cases':7,
                      'product_parameter_checks':4900,'laguerre_identity_checks':20,
                      'original_question':'UNSOLVED','proof_scope':'human-readable arguments require mathematical audit'},sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('FAIL: '+str(e), file=sys.stderr)
        sys.exit(1)
