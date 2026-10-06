#!/usr/bin/env python3
"""Read full authorized local corpus inputs; print only verification metadata.
Usage: verify_corpus.py CATALOG_JSON PROBLEMS_JSON RESEARCH_RESULTS_JSON
"""
import hashlib
import json
import pathlib
import sys

PINS = [
    ('catalog.json', 21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566', 15458),
    ('problems.json', 68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf', 15458),
    ('research_results.json', 80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b', 6701),
]
STATEMENT = '9d374f446c3cae8d7ea16cec4b49b5633fb0fed6db6361cab1f71f92bc054048'
REVIEW = 'ec496d5459f876cb044108dbd678ddf6e34cd1498bd2b9230519bb4b90f21a65'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def main():
    need(sys.flags.isolated and sys.flags.no_site, 'run with -I -S')
    need(len(sys.argv) == 4, 'three input files required')
    objects, records = [], []
    for argument, (name, size, sha, count) in zip(sys.argv[1:], PINS):
        p = pathlib.Path(argument)
        need(p.is_file() and not p.is_symlink(), 'nonregular input')
        raw = p.read_bytes()
        need(len(raw) == size and digest(raw) == sha, 'complete corpus pin mismatch')
        obj = json.loads(raw, object_pairs_hook=unique)
        need(len(obj) == count, 'record count')
        records.append({'name': name, 'bytes': len(raw), 'sha256': digest(raw), 'records': len(obj)})
        objects.append(obj)
    catalog, problems, reports = objects
    cc = [x for x in catalog if str(x.get('id')) == '2303021']
    pp = [x for x in problems if str(x.get('id')) == '2303021']
    need(len(cc) == len(pp) == 1, 'unique target')
    c, p = cc[0], pp[0]
    need(c['rank'] == 853 and p['problem_number'] == c['problem_number'] == 'AMR-022-3021', 'target identity')
    statement = digest(p['statement'].encode())
    review = digest(json.dumps([p, reports.get(p['problem_number'], {})], sort_keys=True).encode())
    need(statement == STATEMENT == c['statement_hash'], 'statement binding')
    need(review == REVIEW == c['review_hash'], 'complete pair default-JSON binding')
    print(json.dumps({'problem_id': 2303021, 'rank': 853, 'result': 'PASS', 'corpora': records,
        'statement_sha256': statement, 'review_sha256': review,
        'serialization': 'json.dumps([complete_problem,reports.get(problem_number,{})],sort_keys=True).encode()',
        'contents_disclosed': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
