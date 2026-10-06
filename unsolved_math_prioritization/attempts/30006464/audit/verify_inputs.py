#!/usr/bin/env python3
"""Independent full-input identity replay; never output corpus contents or paths."""
import hashlib
import json
import pathlib
import stat
import sys

EXPECTED = (
    (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566', 15458),
    (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf', 15458),
    (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b', 6701),
)

def require(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    require(len(sys.argv) == 4, 'supply the three complete corpora in catalog/problems/research-results order')
    inputs = []
    for name, (size, digest, count) in zip(sys.argv[1:], EXPECTED):
        path = pathlib.Path(name)
        require(stat.S_ISREG(path.lstat().st_mode), 'input is not a regular file')
        raw = path.read_bytes()
        require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, 'complete input identity mismatch')
        data = json.loads(raw)
        require(len(data) == count, 'record count mismatch')
        inputs.append(data)
    catalog, problems, reports = inputs
    cat = [entry for entry in catalog if str(entry['id']) == '30006464']
    prob = [entry for entry in problems if entry['id'] == 30006464]
    require(len(cat) == len(prob) == 1, 'target is not unique')
    c, p = cat[0], prob[0]
    number = p['problem_number']
    require(number == c['problem_number'] == 'OWR-14299577-017' and c['rank'] == 831, 'target mismatch')
    require(number not in reports, 'report unexpectedly present')
    statement_hash = hashlib.sha256(p['statement'].encode('utf-8')).hexdigest()
    review = json.dumps([p, reports.get(number, {})], sort_keys=True).encode('utf-8')
    review_hash = hashlib.sha256(review).hexdigest()
    require(statement_hash == c['statement_hash'] == '3fd58aab3ddd149d21db6223b60f498cdc98c006ae67bf89495dc0e180f9605e', 'statement mismatch')
    require(review_hash == c['review_hash'] == '73ff2584746c1f75184a94669e67aea3ff3000e90e8c2b54cb6bac17cb33a395' and len(review) == 4313, 'full record review mismatch')
    print(json.dumps({'status': 'pass', 'problem_id': 30006464, 'rank': 831,
                      'corpora_matched': 3, 'record_counts': [len(x) for x in inputs],
                      'review_bytes': len(review), 'review_sha256': review_hash,
                      'statement_sha256': statement_hash, 'report_present': False,
                      'missing_report_representation': {}, 'full_record_default_serialization': True}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('FAIL: ' + str(exc))
