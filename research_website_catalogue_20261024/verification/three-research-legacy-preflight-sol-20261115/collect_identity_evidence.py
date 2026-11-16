#!/usr/bin/env python3
"""Explicit bounded local identity scan; inert default; no science/network/Git.

Reuses exact authenticated old complete bytes/text by reference. Writes only
new metadata/search evidence here, never the original corpus or old packet.
"""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import re
import sys
import unicodedata

A = Path(__file__).resolve().parent
P = A.parents[1]
R = P / 'redirects/five-centers-mixed-face-preflight-sol-20261115'
DOCS = 'f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3'


def need(c, why):
    if not c:
        raise ValueError(why)


def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}


def check(r):
    p = Path(r['path'])
    b = p.read_bytes()
    need(len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r.get('SHA256', r.get('sha256')), 'whole reference pin: ' + str(p))
    return b


def load(p):
    return json.loads(p.read_text())


def save(n, o):
    p = A / n
    need(not p.exists(), 'never overwrite evidence: ' + n)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + '\n')


def obj_sha(kind, body):
    return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()


def tree_sha(entries):
    raw = b''
    for e in sorted(entries, key=lambda x: (x['path'] + ('/' if x['type'] == 'tree' else '')).encode()):
        raw += e['mode'].lstrip('0').encode() + b' ' + e['path'].encode() + b'\0' + bytes.fromhex(e['sha'])
    return obj_sha('tree', raw)


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s).casefold() if c.isalnum())


def main():
    if sys.argv[1:] != ['--collect']:
        print('Inert default; explicit --collect required.')
        return
    refs = ['CURRENT_BLOB_BINDINGS.json', 'SEARCH_REPRESENTATIONS.json', 'raw/docs-recursive.json', 'FINAL_SEAL.json', 'OWNED_MANIFEST.json']
    bindings = [pin(R / n) for n in refs]
    prior_seal = load(R / 'FINAL_SEAL.json')
    for b in prior_seal['bindings'].values():
        check(b)
    prior_manifest = load(R / 'OWNED_MANIFEST.json')
    for row in prior_manifest['files']:
        r = dict(row)
        if not Path(r['path']).is_absolute():
            r['path'] = str(R / r['path'])
        check(r)
    old_wrapper = load(R / 'raw/docs-recursive.json')
    recursive = json.loads(old_wrapper['result']['structuredContent']['content'])
    need(recursive['sha'] == DOCS and recursive['truncated'] is False, 'complete exact old docs tree')
    children = {}
    for e in recursive['tree']:
        path = PurePosixPath(e['path'])
        parent = '' if str(path.parent) == '.' else str(path.parent)
        children.setdefault(parent, []).append({**e, 'path': path.name})
    reconstructed = []
    for e in recursive['tree']:
        if e['type'] == 'tree':
            h = tree_sha(children[e['path']])
            need(h == e['sha'], 'exact subtree: ' + e['path'])
            reconstructed.append({'path': e['path'], 'SHA1': h})
    need(tree_sha(children['']) == DOCS, 'exact reconstructed docs subtree')
    fresh_root = json.loads(load(A / 'raw/open-root.connector.json')['whole_returned_wrapper']['structuredContent']['content'])
    need(fresh_root['truncated'] is False and tree_sha(fresh_root['tree']) == fresh_root['sha'], 'fresh root tree full object')
    entry = [e for e in fresh_root['tree'] if e['path'] == 'docs']
    need(len(entry) == 1 and entry[0]['sha'] == DOCS, 'actual current docs identity')
    blobs = load(R / 'CURRENT_BLOB_BINDINGS.json')
    bypath = {r['path']: r for r in blobs}
    native_blobs = [e for e in recursive['tree'] if e['type'] == 'blob']
    need(len(blobs) == len(native_blobs) == 254, '254 exact blob paths')
    for e in native_blobs:
        row = bypath['docs/' + e['path']]
        body = check(row['reused_complete_body'])
        need(row['blob'] == e['sha'] == obj_sha('blob', body), 'whole Git blob identity')
        need(row['mode'] == e['mode'] and row['bytes'] == len(body) and row['SHA256'] == hashlib.sha256(body).hexdigest(), 'whole blob mode/size/hash')
    reps = load(R / 'SEARCH_REPRESENTATIONS.json')
    need(len(reps) == 260, '260 exact representations')
    targets = load(A / 'TARGET_IDENTITIES.json')
    aliases = {'23418581': ['miyachi', 'simple young', 'nonprojective injective', 'simple young nonprojective injectives'],
               '23202966': ['relation liveness', 'binary consequences', 'binary relation liveness'],
               '23205305': ['rational point undecidability', 'smooth projective', 'rational numbers']}
    queries = []
    for t in targets:
        rid = t['record_id']
        queries.append({'record_id': rid, 'exact': [rid, t['DOI']], 'compact': [t['title'], t['slug_proposal']] + aliases[rid]})
    hits = []
    for rep in reps:
        body = check(rep['text_file'])
        text = body.decode('utf-8')
        need(rep['public_path'] in bypath and rep['blob'] == bypath[rep['public_path']]['blob'], 'text/current blob interface')
        if rep['kind'] == 'raw_UTF8':
            need(obj_sha('blob', body) == rep['blob'], 'whole original UTF8 blob')
        if rep['kind'] == 'complete_PDF_text':
            original = rep['original_whole_PDF_extract_binding']
            need(original['pdf_blob'] == rep['blob'] and original['pdf_sha256'] == bypath[rep['public_path']]['SHA256'], 'whole cached PDF extraction bound to original')
        n = norm(text)
        for q in queries:
            matched = [s for s in q['exact'] if s.casefold() in text.casefold()]
            compact = [s for s in q['compact'] if norm(s) in n]
            if matched or compact:
                hits.append({'record_id': q['record_id'], 'public_path': rep['public_path'], 'kind': rep['kind'],
                             'blob': rep['blob'], 'text_binding': rep['text_file'], 'exact_hits': matched, 'compact_hits': compact,
                             'entire_representation_scanned': True})
    path_hits = []
    for row in blobs:
        n = norm(row['path'])
        for q in queries:
            terms = q['exact'] + q['compact']
            matched = [s for s in terms if norm(s) in n]
            if matched:
                path_hits.append({'record_id': q['record_id'], 'path': row['path'], 'matched': matched, 'blob': row['blob']})
    save('AUTHENTICATED_CORPUS_INTERFACE.json', {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'reference_bindings': bindings, 'whole_blob_bindings': blobs, 'whole_text_representations': reps,
         'current_docs_subtree': DOCS, 'root_tree': fresh_root['sha'], 'recursive_tree_objects_reconstructed': reconstructed,
         'docs_tree_reconstructed': DOCS, 'all254whole_bodies_freshly_locally_hashed': True,
         'corpus_network_GETs': 0, 'new_PDF_text_extractions': 0, 'whole_corpus_copied': False,
         'old_programmes_imported_or_executed': False})
    save('QUERY_DEFINITIONS.json', queries)
    save('SEARCH_RESULTS.json', hits)
    save('PATHNAME_SEARCH_RESULTS.json', path_hits)
    print(json.dumps({'status': 'COMPLETE', 'paths': len(blobs), 'representations': len(reps),
                      'hit_representations': len(hits), 'candidate_public_paths': sorted(set(h['public_path'] for h in hits)),
                      'path_hits': path_hits}, ensure_ascii=False))


if __name__ == '__main__':
    main()
