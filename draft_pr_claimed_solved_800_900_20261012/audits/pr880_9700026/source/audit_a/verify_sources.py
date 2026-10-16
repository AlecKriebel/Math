#!/usr/bin/env python3
"""Private input replay. Prints metadata only, never copied source contents."""
import hashlib
import json
import pathlib
import sys

PINS = {
    'catalog.json': (21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
    'problems.json': (68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
    'research_results.json': (80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
    'cities-notes.pdf': (295226, '9cfbe9da2660fcea7e44d7ef013cb7a8a1604ff54a9e7734e71ef76959c38b89'),
    'cities-2012.pdf': (398185, 'eeecb371b6e6c2860c01e1b73d812468b619ddb7e3c4cd1d0e3affc056e8a077'),
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def verify(corpus, sources):
    loaded = {}
    rows = []
    for name, (size, digest) in PINS.items():
        data = ((corpus if name.endswith('.json') else sources) / name).read_bytes()
        require((len(data), sha(data)) == (size, digest), 'Input pin mismatch: ' + name)
        rows.append({'name': name, 'bytes': len(data), 'sha256': sha(data), 'match': True})
        if name.endswith('.json'):
            loaded[name] = json.loads(data)
    catalog = [r for r in loaded['catalog.json'] if str(r.get('id')) == '9700026']
    records = [r for r in loaded['problems.json'] if str(r.get('id')) == '9700026']
    require(len(catalog) == len(records) == 1, 'Exact ID is not unique')
    cat, rec = catalog[0], records[0]
    require(cat['rank'] == 934, 'Wrong catalog rank')
    require(cat['problem_number'] == rec['problem_number'] == 'AMR-096-0026', 'Wrong code')
    require(cat['title'] == rec['title'], 'Identity title mismatch')
    reports = loaded['research_results.json']
    require('AMR-096-0026' in reports, 'Missing exact-code report')
    pair = json.dumps([rec, reports.get(rec['problem_number'], {})], sort_keys=True).encode()
    require(len(pair) == 4409, 'Wrong canonical pair byte count')
    require(sha(pair) == cat['review_hash'] == '7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193', 'Review pair mismatch')
    require(sha(rec['statement'].encode()) == cat['statement_hash'] == '5544971834bd618005b3fdf611f753b4cf41bab24b857d0e96a7a067ee3f7b7e', 'Statement mismatch')
    return {'status': 'PASS', 'inputs': rows, 'exact_id_count': 1, 'catalog_rank': 934,
            'problem_id': '9700026', 'problem_number': 'AMR-096-0026',
            'canonical_pair_bytes': len(pair), 'canonical_pair_sha256': sha(pair),
            'catalog_review_hash_match': True, 'catalog_statement_hash_match': True,
            'source_interpretation': 'Human-readable mathematical audit is separate; hashes do not prove source interpretation.'}

if __name__ == '__main__':
    require(len(sys.argv) == 3, 'Usage: verify_sources.py CORPUS_DIRECTORY PDF_DIRECTORY')
    print(json.dumps(verify(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])), indent=2, sort_keys=True))
