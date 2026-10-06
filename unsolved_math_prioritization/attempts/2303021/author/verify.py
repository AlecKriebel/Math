#!/usr/bin/env python3
"""Static inventory/claim checks. This is not a theorem prover."""
import hashlib
import json
import pathlib
import sys


def fail(message):
    raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def require(condition, message):
    if not condition:
        fail(message)


def verify(root):
    require(root.is_dir() and not root.is_symlink(), 'invalid root')
    expected_names = {'APPROACHES.md', 'CLAIMS.json', 'MANIFEST.json',
                      'README.md', 'RESULT.md', 'SOURCES.json', 'verify.py'}
    entries = list(root.iterdir())
    require({p.name for p in entries} == expected_names, 'inventory mismatch')
    for path in entries:
        require(path.is_file() and not path.is_symlink(), 'nonregular entry')
    manifest = read_json(root / 'MANIFEST.json')
    require(set(manifest) == {'schema', 'files'}, 'manifest keys')
    require(manifest['schema'] == 1, 'manifest schema')
    require(set(manifest['files']) == expected_names - {'MANIFEST.json'}, 'manifest inventory')
    for name, record in manifest['files'].items():
        require(set(record) == {'bytes', 'sha256'}, 'file metadata keys')
        data = (root / name).read_bytes()
        require(type(record['bytes']) is int and len(data) == record['bytes'], 'byte count: ' + name)
        require(hashlib.sha256(data).hexdigest() == record['sha256'], 'hash mismatch: ' + name)
    claims = read_json(root / 'CLAIMS.json')
    require(claims['problem_id'] == 2303021 and claims['rank'] == 853, 'target binding')
    require(claims['status'] == 'already_solved', 'status binding')
    require(claims['authored_effort'] == '1/5', 'effort binding')
    for field in ['new_solution', 'gaier_dependency_reproved', 'frw_pdf_bytes_retrieved',
                  'frw_page_images_inspected', 'mathematical_formal_verification', 'publication_performed']:
        require(claims[field] is False, 'scope inflation: ' + field)
    require(claims['published_theorem_is_external_input'] is True, 'external theorem input')
    require(claims['scope']['observation_point_outside_set'] is True, 'origin qualification')
    require(claims['scope']['boundary_contact_counts'] is True, 'boundary convention')
    require(claims['scope']['equality_classification_claimed'] is False, 'equality scope')
    require(claims['theorem']['doi'] == '10.1090/S0002-9947-1985-0768733-1', 'theorem binding')
    require(claims['theorem']['bound'] == 'omega >= asin(d/2)/pi', 'formula binding')
    require(claims['independent_audit'] == 'pending', 'historical audit status')
    source = read_json(root / 'SOURCES.json')
    require(source['redistributed_source_contents'] is False, 'source-content boundary')
    require(len(source['sources']) == 4, 'source record count')
    return {'inventory_files': len(entries), 'status': claims['status'],
            'authored_effort': claims['authored_effort'], 'formal_proof': False,
            'result': 'PASS: static inventory and declared scope'}


if __name__ == '__main__':
    require(len(sys.argv) == 1, 'no extra arguments accepted')
    print(json.dumps(verify(pathlib.Path(__file__).resolve().parent), sort_keys=True))
