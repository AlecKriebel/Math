#!/usr/bin/env python3
"""Read-only full-input pins and exact-record verification; emits metadata only."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

PINS = {
    'catalog.json': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems.json': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'research_results.json': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
    'k3-author.pdf': (6578041, 'ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f'),
    'gabai-v2.pdf': (5545549, '7dc88288db810ee6b14473b677f950e9d13d7ae0b9bd2cc778e9b6b7af63805c'),
    'singh-v3.pdf': (1613895, '2818860c0fe7a237866b039759ed9ff74f135ef592f19768d17650afb6cb1eb3'),
}
PAIR = '81b4b9cb5a480c8dfbc00462cc890d43edcc424a07568d2b642c82b731a91020'
STATEMENT = '2ab0530ff6f2e7e4105b1ecf66fd99fe4a853a0c95c9cd46dcae76dd1e1d1774'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('catalog')
    parser.add_argument('problems')
    parser.add_argument('reports')
    parser.add_argument('pdf_directory')
    args = parser.parse_args()
    paths = {'catalog.json': Path(args.catalog), 'problems.json': Path(args.problems),
             'research_results.json': Path(args.reports)}
    paths.update({name: Path(args.pdf_directory) / name for name in PINS if name.endswith('.pdf')})
    data, results = {}, []
    for name, path in paths.items():
        require(path.is_file() and not path.is_symlink(), 'missing/nonregular source: ' + name)
        raw = path.read_bytes()
        actual = (len(raw), sha(raw))
        require(actual == PINS[name], 'source pin mismatch: ' + name)
        results.append({'logical_name': name, 'bytes': actual[0], 'sha256': actual[1], 'match': True})
        if name.endswith('.json'):
            data[name] = json.loads(raw)
    catalog = [row for row in data['catalog.json'] if str(row.get('id')) == '2950']
    records = [row for row in data['problems.json'] if str(row.get('id')) == '2950']
    require(len(catalog) == len(records) == 1, 'exact-ID uniqueness')
    cat, record = catalog[0], records[0]
    require(cat['rank'] == 921 and cat['problem_number'] == record['problem_number'] == 'KP-4.74', 'identity/rank')
    report = data['research_results.json'].get(record['problem_number'], {})
    pair = sha(json.dumps([record, report], sort_keys=True).encode())
    statement = sha(record['statement'].encode())
    require(pair == PAIR == cat['review_hash'], 'complete record/report pair')
    require(statement == STATEMENT == cat['statement_hash'], 'statement')
    require(report == {}, 'unexpected inherited report')
    return {'result': 'PASS', 'problem_id': 2950, 'rank': 921, 'pins': results,
            'complete_record_report_pair_sha256': pair, 'statement_sha256': statement,
            'pair_serialization': 'json.dumps([complete_problem_record, report_or_empty_object], sort_keys=True), Python defaults, UTF-8',
            'inherited_report_key_present': record['problem_number'] in data['research_results.json'],
            'inherited_report_empty': True, 'catalog_records': len(data['catalog.json']),
            'problem_records': len(data['problems.json']), 'research_result_keys': len(data['research_results.json']),
            'source_contents_emitted': False, 'mathematical_proof_check': False}

if __name__ == '__main__':
    try:
        print(json.dumps(main(), sort_keys=True))
    except Exception as error:
        print('REJECT: ' + str(error), file=sys.stderr)
        sys.exit(1)
