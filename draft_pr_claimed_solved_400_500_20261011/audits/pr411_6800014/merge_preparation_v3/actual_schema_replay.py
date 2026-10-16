#!/usr/bin/env python3
"""Offline replay of pinned ADMIN JSON only; no network, assets or tracker reads.

Authenticated/public responses remain exact bytes. Stop deliberately before
asset download so this is metadata projection evidence, not a publication or
Sheet certificate. Mathematical payload files are never opened.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
MAPPING = ('publication_preparation/ROOT_ACTUAL_PUBLICATION_MAPPING_ACCEPTANCE.json',
           'ff8e97f7e9c4f88efcaa2fc88bfa41ddf7777e036e668da81c785a2b1c964dad')
TYPES = ('publication_preparation/ROOT_ACTUAL_PUBLICATION_RESPONSE_TYPES.json',
         'd4f56a5b66c19bf7a3190604b89f3980e5070b20e59d840141207a8b4c0cdbd8')
SNAPSHOT = ('private_sources/publication_admin_helper/ROOT_READONLY_DRAFT_NATIVE_20261013T0414/NATIVE_METADATA_ACCESS_SNAPSHOT.json',
            '0743c2bed2a7081bd4417ee5e5f594d6856bbe35eedcbcb7be70fb446d69d6ee')
PREFIX = 'private_sources/publication_admin_helper_v2/ROOT_READONLY_PUBLIC_MAPPING_20261013T0510/'


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class SchemaCheckpoint(Exception):
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--private-dir', type=Path, required=True)
    args = parser.parse_args()
    current = module(HERE / 'pr411_admin.py', 'v3_current')
    mapping = json.loads(current.read_local(args.case, *MAPPING))
    current.read_local(args.case, *TYPES)
    snapshot_raw = current.read_local(args.case, *SNAPSHOT)
    originals = {}
    for name in ('0000_intent.json', '0000_response.json', '0001_response.json', '0003_response.json',
                 '0003_native.json', '0004_response.json', '0004_native.json'):
        key = PREFIX + name
        pin = mapping['positive_private_originals'][key]
        raw = current.read_local(args.case, key, pin['sha256'])
        current.need(len(raw) == pin['bytes'], 'actual original size differs')
        originals[name] = raw
    tests = module(HERE / 'offline_tests.py', 'synthetic_tracker_not_consumed')
    w = tests.World(args.private_dir)
    parsed = {name: json.loads(raw) for name, raw in originals.items()}
    w.record_id, w.doi = mapping['id'], mapping['doi']
    w.public, w.native = parsed['0003_response.json'], parsed['0004_response.json']
    # Only asset metadata is used. No binary scientific artifact is opened.
    approved = {'assets': [{'name': item['name'], 'bytes': item['size'], 'sha256': item['sha256']}
                           for item in mapping['public_downloads']]}
    binding = w.binding
    binding['doi'] = w.doi
    def copied(name, raw):
        target = w.root / name
        target.write_bytes(raw)
        return {'path': name, 'sha256': hashlib.sha256(raw).hexdigest()}
    pub = binding['publication']
    for field, source in {'submitted_intent': '0000_intent.json', 'submitted_response': '0000_response.json',
                          'authenticated_native_response': '0001_response.json',
                          'legacy_public_response': '0003_response.json', 'legacy_public_native': '0003_native.json',
                          'public_native_response': '0004_response.json', 'public_native_native': '0004_native.json'}.items():
        pub[field] = copied('ACTUAL_' + source, originals[source])
    pub['approved_native_snapshot'] = copied('ACTUAL_APPROVED_SNAPSHOT.json', snapshot_raw)
    class OfflineActualRecords:
        def production_record(self, record_id, native=False):
            current.need(record_id == w.record_id, 'actual record identity differs')
            return w.native if native else w.public
        def production_asset(self, record_id, name, size):
            raise SchemaCheckpoint('all original metadata projection joins passed; asset byte verification not executed')
    results = []
    candidates = [('accepted_original', args.case / 'merge_preparation/pr411_admin.py',
                   '1a3963efbab49cf96ea75326cc77b9c3c7455a6c87140a382fc294e739afa131', False),
                  ('initial_v3_superseded', args.case / 'private_sources/merge_preparation_v3/initial_v3_schema_candidate/pr411_admin.py',
                   'd29a712a23d69d9b5af567e990313ed700240c595a250f8b6748ffea68bb1094', False),
                  ('initial_v3_integer_only_counterfactual', args.case / 'private_sources/merge_preparation_v3/initial_v3_schema_candidate/INTEGER_ONLY_COUNTERFACTUAL_PROBE.py',
                   '3b2b87d56441f9940e87d85f6c1f70b5a429c0981db56dba4decc94fe70c2930', False),
                  ('pre_raw_join_type_repair', args.case / 'private_sources/merge_preparation_v3/pre_raw_join_type_repair/pr411_admin.py',
                   '8072a4383aa5cca4d0c77273b4b91a33dc5bc749a027d46f1c6262b44dcd03ee', True),
                  ('current_v3', HERE / 'pr411_admin.py', hashlib.sha256((HERE / 'pr411_admin.py').read_bytes()).hexdigest(), True)]
    for tag, path, pin, expected in candidates:
        current.need(hashlib.sha256(path.read_bytes()).hexdigest() == pin, 'administration source pin differs')
        candidate = module(path, tag)
        outcome, detail = False, None
        try:
            candidate.evidence(w.root, binding, approved, OfflineActualRecords())
            raise RuntimeError('deliberate metadata-only checkpoint was not reached')
        except SchemaCheckpoint as exc:
            outcome, detail = True, str(exc)
        except candidate.Stop as exc:
            detail = str(exc)
        current.need(outcome is expected, 'unexpected actual-schema replay result: ' + tag + ': ' + str(detail))
        results.append({'candidate': tag, 'source_sha256': pin, 'metadata_projection_passed': outcome,
                        'expected_metadata_projection_passed': expected, 'detail': detail})
    output = {'result': 'PASS_OFFLINE_PINNED_ACTUAL_SCHEMA_REPLAY', 'tests': results,
              'root_mapping_sha256': MAPPING[1], 'root_type_addendum_sha256': TYPES[1],
              'approved_native_snapshot_sha256': SNAPSHOT[1], 'native_requests': 0, 'native_mutations': 0,
              'asset_byte_verification_executed': False, 'tracker_verification_executed': False,
              'scientific_files_or_blobs_opened': 0,
              'boundary': 'Exact original ADMIN JSON replay only, with deliberately unconsumed synthetic tracker fixture. Not a publication, tracker, integration, ready or merge certificate.'}
    (w.root / 'RESULT.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
