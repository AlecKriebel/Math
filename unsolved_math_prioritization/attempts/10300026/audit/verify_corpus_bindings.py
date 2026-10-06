"""Bind the complete supplied corpus inputs; emit only permitted verification metadata."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use -I -S -B')
import hashlib
import json
from pathlib import Path

EXPECTED = [
    ('complete_catalog', 21735099, '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566', 15458),
    ('complete_problems', 68931837, '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf', 15458),
    ('complete_research_reports', 80334822, '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b', 6701),
]
if len(sys.argv) != 4:
    raise SystemExit('usage: verify_corpus_bindings.py catalog.json problems.json research_results.json')
loaded, inputs = [], []
for name, (label, size, digest, count) in zip(sys.argv[1:], EXPECTED):
    blob = Path(name).read_bytes()
    actual = hashlib.sha256(blob).hexdigest()
    if len(blob) != size or actual != digest:
        raise SystemExit('REJECT: complete corpus identity')
    obj = json.loads(blob)
    if len(obj) != count:
        raise SystemExit('REJECT: complete corpus count')
    loaded.append(obj)
    inputs.append({'label': label, 'bytes': len(blob), 'sha256': actual, 'records': len(obj), 'match': True})
catalog, problems, reports = loaded
cc = [p for p in catalog if str(p.get('id')) == '10300026']
pp = [p for p in problems if p.get('id') == 10300026]
if len(cc) != 1 or len(pp) != 1:
    raise SystemExit('REJECT: record uniqueness')
c, p = cc[0], pp[0]
if c['rank'] != 844 or c['problem_number'] != p['problem_number'] or p['problem_number'] != 'AMR-102-0026':
    raise SystemExit('REJECT: target identity')
statement = hashlib.sha256(p['statement'].encode()).hexdigest()
review = hashlib.sha256(json.dumps([p, reports.get(p['problem_number'], {})], sort_keys=True).encode()).hexdigest()
if statement != c['statement_hash'] or statement != 'df1623ec850b43d288ee3b733ef4c0108852280687e2cd09c89c79a18659b6df':
    raise SystemExit('REJECT: statement binding')
if review != c['review_hash'] or review != 'd539a48fb43e8d346651b0e11607b0e6315c856cdaec3d0d156d348c4d77aca2':
    raise SystemExit('REJECT: complete review binding')
print(json.dumps({'problem_id': 10300026, 'problem_number': p['problem_number'], 'catalog_rank': 844, 'corpora': inputs, 'statement_sha256': statement, 'review_sha256': review, 'statement_match': True, 'review_match': True, 'complete_problem_keys': len(p), 'complete_research_report_keys': len(reports[p['problem_number']]), 'serialization': 'json.dumps([complete_problem, reports.get(problem_number, {})], sort_keys=True).encode() with default separators and ensure_ascii', 'raw_corpus_content_included': False}, indent=2, sort_keys=True))
