#!/usr/bin/env python3
"""Check package integrity, the axiom-gap witness, and optional external bytes."""
import argparse
import hashlib
import json
import pathlib
import runpy
import sys

MEMBERS = {'README.md', 'AUDIT_REPORT.md', 'SCOPE_CORRECTION.md', 'AUDIT_CERTIFICATE.json',
           'SOURCES.json', 'WITNESS.json', 'WITNESS_RESULT.json', 'TEST_RESULTS.json',
           'PACKAGE_TEST_RESULTS.json', 'witness_check.py', 'test_witness.py',
           'verify_audit.py', 'test_integrity.py', 'MANIFEST.json'}
PINS = {'AUDIT_REPORT.md': '57f5a5896fb12275a7360880b5ac58fe8c9a510bd57e9f78174ce4a544125911', 'SCOPE_CORRECTION.md': 'f0eeb8d06a27c296583e140e560807f8bfe38784f7fd110f68937f1e9cee2ff6', 'AUDIT_CERTIFICATE.json': 'c15a0f1dceec27724e4a91b0a1d542caeac8e2653defcb6996fd66649dfa82bc', 'SOURCES.json': '542d5e212d219358cd197420a1584fbb3f9c042a44ef1a62b9789217743a51d1', 'WITNESS.json': '585bddbe34e2a349b131c9a5384970504d585702ed21671cc58cffbb32b360d6', 'witness_check.py': '7131fbc7c4e24726879070f322c07e2572e4bc14fc49dc7ddcd79f3e09069226'}
PDFS = {
    'owr': (731001, '3fcc907de0d7003b3d2cdfe3e7151e18309e926a4b6471e818e70f1ab085af35'),
    'hp': (1872177, '8266d3ae09b37aad8b077eb50154521bd957faf06c30e5ba661d2150eb3b74d7'),
    'gp': (87494, 'b91a17b8e5bd41e555a38563953768b35352a89be6c998452ac73b225be920b9'),
    'interval': (122401, '471fc06b3935b8646feb7a3728cade5ac7fc66c029307adf21c8d1bdf4773407'),
}
AUTHOR = (9569, '6f8aa56d3832584a9f687165f57316a04e488d51753f6e844b25e84fd571f89c')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'Duplicate JSON key: ' + key)
        out[key] = value
    return out


def read_json(path):
    def reject(value):
        raise ValueError('Nonfinite constant: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify(root, sources_dir=None, author_zip=None):
    require(root.is_dir() and not root.is_symlink(), 'Invalid package root')
    members = list(root.iterdir())
    require({p.name for p in members} == MEMBERS, 'Unexpected or missing member')
    require(all(p.is_file() and not p.is_symlink() for p in members), 'Nonregular member')
    manifest = read_json(root / 'MANIFEST.json')
    require(type(manifest) is dict and set(manifest) == {'schema', 'files'}, 'Invalid manifest')
    require(type(manifest['schema']) is int and manifest['schema'] == 1, 'Invalid schema')
    files = manifest['files']
    require(type(files) is dict and set(files) == MEMBERS - {'MANIFEST.json'}, 'Manifest member mismatch')
    for name, record in files.items():
        require(type(record) is dict and set(record) == {'bytes', 'sha256'}, 'Invalid record')
        size, sha = identity(root / name)
        require(type(record['bytes']) is int and record['bytes'] == size, 'Byte mismatch: ' + name)
        require(record['sha256'] == sha, 'Hash mismatch: ' + name)
    for name, sha in PINS.items():
        require(identity(root / name)[1] == sha, 'Frozen audit content mismatch: ' + name)
    cert = read_json(root / 'AUDIT_CERTIFICATE.json')
    require(cert['problem_id'] == 30001054 and cert['audit_gate'] == 'NEEDS_SCOPE_CORRECTION', 'Wrong gate')
    require(cert['literal_four_axiom_disposition'] == 'FALSE_BY_FINITE_WITNESS', 'Wrong literal scope')
    require(cert['intended_switch_once_fibration_disposition'] == 'SOLVED_IN_LITERATURE_AFFIRMATIVE', 'Wrong credited scope')
    require(cert['novelty_claimed'] is False and cert['independent_full_representation_proof_claimed'] is False,
            'Unsupported proof or novelty claim')
    api = runpy.run_path(str(root / 'witness_check.py'), run_name='audit_witness_import')
    result = api['verify_witness'](root / 'WITNESS.json')
    require(result == read_json(root / 'WITNESS_RESULT.json'), 'Witness result mismatch')
    sources = read_json(root / 'SOURCES.json')['sources']
    require(len(sources) == 4 and {s['id'] for s in sources} == set(PDFS), 'Wrong sources')
    for source in sources:
        require((source['bytes'], source['sha256']) == PDFS[source['id']], 'Wrong source identity')
    checked = []
    if sources_dir is not None:
        for key, expected in PDFS.items():
            path = sources_dir / (key + '.pdf')
            require(path.is_file() and identity(path) == expected, 'External PDF mismatch: ' + key)
            checked.append(key)
    if author_zip is not None:
        require(author_zip.is_file() and identity(author_zip) == AUTHOR, 'Historical author ZIP mismatch')
    return {'result': 'PASS_AUDIT_INTEGRITY_AND_WITNESS', 'audit_gate': cert['audit_gate'],
            'fresh_external_pdfs_byte_verified': checked,
            'historical_author_zip_byte_verified_this_run': author_zip is not None,
            'imported_representation_theorem_proved_by_code': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent)
    parser.add_argument('--sources-dir', type=pathlib.Path)
    parser.add_argument('--author-zip', type=pathlib.Path)
    args = parser.parse_args()
    try:
        result = verify(args.root, args.sources_dir, args.author_zip)
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
