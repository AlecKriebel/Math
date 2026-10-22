"""Verify exact complete inputs, emitting metadata only. This does not prove mathematics."""
import argparse
import hashlib
import json
from pathlib import Path

PINS = {
    'catalog': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'reports': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
    'k3': (6578041, 'ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f'),
    'fkr': (616146, 'c47e99511d18c560a5ac48f1eb531be2368769b65414978ab87690f4817d4c8f'),
    'bfs': (865101, '6de14d4cc1ab4a503ddaf5db46b896a180b535dd3fbadc724543b4a0da90a13c'),
    'long_reid': (97204, 'bdb24740cb5a358ec3f2f6385e0e92efebeb5c38ed8b24d9ac7de163466d1465'),
    'hatcher': (384715, 'f3781c43b4ed981f98fab36761d5eefe92bb53cc1a7100a0146954f9af5a029b'),
}
PAIR_SHA = 'fc3af508fdb48578890fc4e5a8c01e7f8123397993e517706059a038141e46ae'
STATEMENT_SHA = 'b679b03a935318ed98193d750b04f84361b4cd27b9425a3a533e5cad80ff793f'

def require(condition, label):
    if not condition:
        raise ValueError(label)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def check_pin(label, data):
    size, sha = PINS[label]
    require(len(data) == size and digest(data) == sha, 'source pin mismatch: ' + label)
    return {'source_label': label, 'bytes': size, 'sha256': sha, 'matches_expected': True}

def verify(paths):
    require(set(paths) == set(PINS), 'all eight input paths are required')
    raw = {}
    checks = []
    for label in PINS:
        data = Path(paths[label]).read_bytes()
        checks.append(check_pin(label, data))
        if label in ('catalog', 'problems', 'reports'):
            raw[label] = json.loads(data)
    catalog = [x for x in raw['catalog'] if str(x.get('id')) == '2875']
    records = [x for x in raw['problems'] if str(x.get('id')) == '2875']
    require(len(catalog) == len(records) == 1, 'exact ID multiplicity')
    cat, record = catalog[0], records[0]
    require(cat['rank'] == 916 and cat['problem_number'] == record['problem_number'] == 'KP-3.77', 'identity mismatch')
    report = raw['reports'].get(record['problem_number'], {})
    pair = json.dumps([record, report], sort_keys=True).encode('utf-8')
    require(digest(pair) == PAIR_SHA and len(pair) == 5695, 'complete pair mismatch')
    require(digest(record['statement'].encode('utf-8')) == STATEMENT_SHA, 'statement mismatch')
    require(cat['statement_hash'] == STATEMENT_SHA and cat['review_hash'] == PAIR_SHA, 'catalog hash mismatch')
    require(report == {}, 'associated report is not empty')
    return {
        'status': 'PASS', 'problem_id': 2875, 'problem_number': 'KP-3.77', 'rank': 916,
        'full_corpus_count': 3, 'pdf_count': 5, 'source_checks': checks,
        'complete_pair_bytes': len(pair), 'complete_pair_sha256': PAIR_SHA,
        'statement_sha256': STATEMENT_SHA, 'exact_record_count': 1, 'associated_report_empty': True,
        'pair_serialization': 'json.dumps([complete record, reports.get(problem_number, {})], sort_keys=True), default separators and ensure_ascii',
        'scope': 'Complete-byte integrity and exact-ID extraction only. No corpus content is emitted. No mathematical proof is certified.'
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for label in PINS:
        parser.add_argument('--' + label.replace('_', '-'), required=True)
    args = parser.parse_args()
    print(json.dumps(verify(vars(args)), indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
