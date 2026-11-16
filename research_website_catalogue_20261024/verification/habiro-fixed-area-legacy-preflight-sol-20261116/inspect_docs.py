"""Finite offline docs identity inspection; no scientific or old-helper execution."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime, timezone
import hashlib, html, json, re, unicodedata

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/habiro-fixed-area-legacy-preflight-sol-20261116'
OLD = P / 'verification/three-research-legacy-preflight-sol-20261115/AUTHENTICATED_CORPUS_INTERFACE.json'

def digest(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'SHA256': digest(b)}
def bound(row):
    b = Path(row['path']).read_bytes()
    assert len(b) == row['bytes'] and digest(b) == row['SHA256'], row['path']
    return b
def content(name): return json.loads((O / name).read_text())['structuredContent']['content']
def git_hash(kind, b): return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def tree_hash(rows):
    rows = sorted(rows, key=lambda x: (x['path'] + ('/' if x['type'] == 'tree' else '')).encode())
    data = b''.join(x['mode'].lstrip('0').encode() + b' ' + x['path'].encode() + b'\0' + bytes.fromhex(x['sha']) for x in rows)
    return git_hash('tree', data)
def folded(s):
    s = unicodedata.normalize('NFKC', html.unescape(s)).casefold()
    return ' '.join(re.sub(r'[\W_]+', ' ', s).split())

class Visible(HTMLParser):
    def __init__(self, s):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.feed(s)
    def handle_data(self, data): self.parts.append(data)

old = json.loads(OLD.read_text())
assert digest(OLD.read_bytes()) == '4e3603f1683befb1c37a8ac5b0dc0fd37d277e618a96ba23d1fcd4cbdeb87f4f'
for row in old['reference_bindings']: bound(row)
root = json.loads(content('OPEN_ROOT_TREE.connector.json'))
assert not root['truncated'] and tree_hash(root['tree']) == root['sha']
docs = json.loads(content('OPEN_DOCS_RECURSIVE.connector.json'))
assert not docs['truncated'] and docs['sha'] == next(x['sha'] for x in root['tree'] if x['path'] == 'docs')
trees = {'': docs['sha'], **{x['path']: x['sha'] for x in docs['tree'] if x['type'] == 'tree'}}
for directory, expected in trees.items():
    direct = []
    for row in docs['tree']:
        name = row['path']; parent = name.rsplit('/', 1)[0] if '/' in name else ''
        if parent == directory: direct.append({**row, 'path': name.rsplit('/', 1)[-1]})
    assert tree_hash(direct) == expected, directory
blobs = {x['path']: x for x in docs['tree'] if x['type'] == 'blob'}
prior = {x['path'][5:]: x for x in old['whole_blob_bindings']}
assert len(blobs) == len(prior) == 254 and set(blobs) == set(prior)
changed = [n for n in blobs if blobs[n]['sha'] != prior[n]['blob']]
assert changed == ['papers/brandes-coefficient-normalization/index.html']
changed_body = content('CHANGED_COEFFICIENT_BLOB.connector.json').encode()
(O / 'CHANGED_COEFFICIENT_ARTICLE.html').write_bytes(changed_body)
body_bindings, bodies = [], {}
for name, row in blobs.items():
    if name in changed:
        b = changed_body; source = pin(O / 'CHANGED_COEFFICIENT_ARTICLE.html')
    else:
        source = prior[name]['reused_complete_body']; b = bound(source)
        assert digest(b) == prior[name]['SHA256'] and len(b) == prior[name]['bytes']
    assert len(b) == row['size'] and git_hash('blob', b) == row['sha'], name
    bodies[name] = b
    body_bindings.append({'path': 'docs/' + name, 'mode': row['mode'], 'blob': row['sha'], 'bytes': len(b), 'SHA256': digest(b), 'whole_body_reference': source, 'fresh_connector_delta': name in changed})
cached = []
for row in old['whole_text_representations']:
    b = bound(row['text_file']); cached.append((row, b))
representations = []
for name, b in bodies.items():
    if name.endswith('.html'):
        s = b.decode('utf-8'); visible = ' '.join(Visible(s).parts)
        representations.extend([('docs/' + name, blobs[name]['sha'], 'current_raw_HTML_UTF8', s), ('docs/' + name, blobs[name]['sha'], 'current_decoded_HTML', visible)])
for row, b in cached:
    name = row['public_path'][5:]
    if name.endswith('.html'): continue
    assert row['blob'] == blobs[name]['sha']
    representations.append((row['public_path'], row['blob'], row['kind'], b.decode('utf-8')))
assert len(representations) == 260
targets = json.loads((O / 'TARGET_IDENTITIES.json').read_text()); hits = []; path_hits = []; candidates = {}
for target in targets:
    terms = [(term, folded(term)) for term in target['literal_search_terms']]
    for name in blobs:
        found = [term for term, f in terms if f and f in folded(name)]
        if found: path_hits.append({'record_id': target['record_id'], 'path': 'docs/' + name, 'terms': found})
    for name, blob, kind, text in representations:
        ftext = folded(text); found = [term for term, f in terms if f and f in ftext]
        if not found: continue
        hits.append({'record_id': target['record_id'], 'path': name, 'blob': blob, 'kind': kind, 'terms': found})
        if name.endswith('.html'): candidates.setdefault(name, set()).add(target['record_id'])
candidate_rows = []
for i, (name, records) in enumerate(sorted(candidates.items()), 1):
    filename = 'HTML_HIT_' + str(i).zfill(2) + '.html'; b = bodies[name[5:]]; (O / filename).write_bytes(b)
    candidate_rows.append({'public_path': name, 'records_with_identity_term_hits': sorted(records), 'blob': blobs[name[5:]]['sha'], 'saved_whole_body': pin(O / filename), 'catalogue_requires_separate_exclusion': name in ['docs/index.html', 'docs/papers/index.html']})
receipt = {'UTC': datetime.now(timezone.utc).isoformat(), 'root_commit': '9579e21fa33c14d0b7a099c78a41a54149f3da85', 'root_tree': root['sha'], 'docs_tree': docs['sha'], 'root_tree_reconstructed': True, 'docs_tree_objects_reconstructed_including_root': len(trees), 'recursive_tree_truncated': False, 'whole_current_blobs': body_bindings, 'old_corpus_interface': pin(OLD), 'unchanged_body_reuses': 253, 'fresh_changed_bodies': 1, 'exact_changed_paths': changed, 'old_cached_representations_authenticated': len(cached), 'current_search_representations': [{'path': n, 'blob': blob, 'kind': kind, 'characters': len(text), 'UTF8_SHA256': digest(text.encode())} for n, blob, kind, text in representations], 'HTML_paths': 47, 'whole_current_text_representations': 260, 'opaque_blob_paths_not_text_searched': sorted('docs/' + n for n in blobs if not any(r[0] == 'docs/' + n for r in representations)), 'new_PDF_extractions': 0, 'scientific_native_oldhelper_or_network_execution': False}
(O / 'CORPUS_AUTHENTICATION.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
(O / 'IDENTITY_SEARCH_RESULTS.json').write_text(json.dumps({'UTC': receipt['UTC'], 'normalization': 'NFKC; HTML entity decode; casefold; punctuation-to-space; whitespace collapse. Literal query terms are frozen in TARGET_IDENTITIES.', 'path_hits': path_hits, 'whole_representation_hits': hits, 'HTML_hit_bodies_for_personal_reading': candidate_rows, 'correspondence_verdict_not_automatically_inferred': True}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'docs_tree': docs['sha'], 'tree_objects': len(trees), 'whole_bodies': len(body_bindings), 'text_representations': len(representations), 'path_hits': path_hits, 'HTML_hit_bodies': candidate_rows, 'non_HTML_hit_count': sum(not x['path'].endswith('.html') for x in hits)}, ensure_ascii=False, indent=2))
