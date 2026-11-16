#!/usr/bin/env python3
"""One read-only full-body search of exactly 47 authenticated current docs HTMLs."""
import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/odd-areas-boolean-city-stage-audit-sol-20261116'
C = P / 'verification/supercritical-nonuniqueness-legacy-preflight-sol-20261116/SEARCH.stdout.json'

def raw(p):
    assert p.is_file() and not p.is_symlink(), str(p)
    return p.read_bytes()

def obj(p):
    return json.loads(raw(p))

def receipt(name):
    r = obj(O / name)
    assert r.get('isError') is False
    return json.loads(r['structuredContent']['content'])

def git_hash(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()

ref = receipt('LEGACY160_OPEN_REF.connector.json')
commit = receipt('LEGACY160_OPEN_COMMIT.connector.json')
root = receipt('LEGACY160_OPEN_ROOT.connector.json')
docs = receipt('LEGACY160_DOCS_TREE.connector.json')
assert ref['object']['sha'] == commit['sha'] == '31a55d31327752e58cae11a3511bb9334ce1e879'
assert commit['tree']['sha'] == root['sha'] == '1ad3042232146ff96dee611b5fb6f347f15e4ae3'
assert root['truncated'] is False and docs['truncated'] is False
assert next(x for x in root['tree'] if x['path'] == 'docs')['sha'] == docs['sha'] == 'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'
entries = docs['tree']
assert len(entries) == 304 and len({x['path'] for x in entries}) == 304

def tree_hash(prefix):
    children = [x for x in entries if str(PurePosixPath(x['path']).parent) == (prefix or '.')]
    children.sort(key=lambda x: (PurePosixPath(x['path']).name + ('/' if x['type'] == 'tree' else '')).encode())
    b = b''
    for x in children:
        assert x['type'] in {'tree', 'blob'}
        if x['type'] == 'tree':
            assert tree_hash(x['path']) == x['sha']
        mode = x['mode'].lstrip('0') or '0'
        b += mode.encode() + b' ' + PurePosixPath(x['path']).name.encode() + b'\0' + bytes.fromhex(x['sha'])
    return git_hash('tree', b)

assert tree_hash('') == docs['sha']
current = {'docs/' + x['path']: x for x in entries if x['type'] == 'blob' and x['path'].lower().endswith('.html')}
assert len(current) == 47
cached = obj(C)
assert cached['docs_tree'] == docs['sha']
rows = cached['rows']
assert len(rows) == 47 and {x['path'] for x in rows} == set(current)
native = obj(P / 'papers/23393139/sources/record.response.body')
assert native['id'] == 23393139 and native['metadata']['doi'] == '10.5281/zenodo.23393139'
adoption_path = P / 'verification/root-editorial-23393139-20261116.json'
adoption_bytes = raw(adoption_path)
assert len(adoption_bytes) == 4316 and hashlib.sha256(adoption_bytes).hexdigest() == 'fe3e276bb17fb83ef3279e13a4125ed2235b60692ceedfd4f83d83cc9eabbf73'
adoption = json.loads(adoption_bytes)
approved = raw(P / adoption['MAIN']['path'])
assert len(approved) == adoption['MAIN']['bytes']
assert hashlib.sha256(approved).hexdigest() == adoption['MAIN']['SHA256']
terms = [
    ('complete native title', re.escape(native['metadata']['title'])),
    ('native or concept record', r'2339313[89]'),
    ('native or concept DOI', r'10\.5281/zenodo\.2339313[89]'),
    ('fixed city', r'fixed[\s_-]*cit(?:y|ies)'),
    ('city growth', r'cit(?:y|ies)[\s_-]+growth'),
    ('city ODE or native source alias', r'city[\s_-]*(?:ode|persistence)'),
    ('Aldous', r'\bAldous\b'),
    ('literal conjecture 32', r'conjecture\s*32(?:\s*\(?a\)?)?'),
    ('actual PR source 880', r'(?:/pull/880\b|\bPR[\s_-]*880\b)'),
    ('source catalogue alias', r'9700026'),
    ('distinctive upper bound', r'2047\s*/\s*2048'),
    ('original source claim alias', r'persistence\s+refutes\s+the\s+literal\s+city'),
]
result = []
for row in rows:
    e = current[row['path']]
    assert e['sha'] == row['Git_blob'] and e['size'] == row['bytes']
    br = row['body_reference']
    if 'container' in br:
        assert br['container'] == 'structuredContent.content UTF-8'
        b = obj(Path(br['path']))['structuredContent']['content'].encode()
    else:
        b = raw(Path(br['path']))
    assert len(b) == row['bytes'] and git_hash('blob', b) == row['Git_blob']
    assert hashlib.sha256(b).hexdigest() == row['SHA256']
    literal = b.decode('utf-8')
    plain = ' '.join(html.unescape(re.sub(r'<[^>]*>', ' ', literal)).split())
    hits = []
    for label, expression in terms:
        match = re.search(expression, literal, re.I) or re.search(expression, plain, re.I)
        if match:
            hits.append(label)
    result.append({'path': row['path'], 'Git_blob': row['Git_blob'], 'bytes': len(b), 'SHA256': row['SHA256'], 'body_reference': br, 'matched_terms': hits})
print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'scope': 'exact 47 current docs HTML whole bodies; no history/assets/PDF/ZIP scan', 'main': commit['sha'], 'root_tree': root['sha'], 'docs_tree': docs['sha'], 'metadata_entries': len(entries), 'tree_objects_authenticated': 1 + sum(x['type'] == 'tree' for x in entries), 'whole_HTML_buffers_authenticated_and_searched': 47, 'HTML_body_fetches': 0, 'reused_exact_current_blobs': 47, 'native_title': native['metadata']['title'], 'native_related_identifiers': native['metadata'].get('related_identifiers'), 'proposed_private_slug': adoption['proposed_slug'], 'approved_MAIN_ids': re.findall(r'\bid="([^"]+)"', approved.decode()), 'query_expressions': terms, 'rows': result, 'matching_paths': [x['path'] for x in result if x['matched_terms']], 'global_or_history_absence_claim': False, 'redirect_or_publication_authority': False}, indent=2))
