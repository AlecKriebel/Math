#!/usr/bin/env python3
"""Offline, read-only next-fixed-three corpus identity scan; no other programs.

Uses pinned complete old corpus bytes/text by reference, never old conclusions
or helper execution. No network/Git/PDF extraction, writes, or science verdict.
"""
from pathlib import Path, PurePosixPath
from collections import Counter
import hashlib
import json
import stat
import sys
import unicodedata

A = Path(__file__).resolve().parent


def need(c, s):
    if not c:
        raise ValueError(s)


def whole(p):
    p = Path(p)
    need(p.is_absolute() and '..' not in p.parts, 'absolute safe reference')
    need(all(not q.is_symlink() for q in (p,) + tuple(p.parents)), 'no symlink reference')
    need(stat.S_ISREG(p.stat().st_mode), 'regular whole reference')
    return p.read_bytes()


def load(p):
    return json.loads(whole(p))


def check(r):
    b = whole(r['path'])
    need(len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r.get('SHA256', r.get('sha256')), 'whole pinned reference: ' + r['path'])
    return b


def obj(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def tree(entries):
    names = [e['path'] for e in entries]
    need(len(names) == len(set(names)), 'unique direct tree names')
    body = b''
    for e in sorted(entries, key=lambda e: (e['path'] + ('/' if e['type'] == 'tree' else '')).encode()):
        need('/' not in e['path'] and e['path'] not in ('', '.', '..'), 'safe direct tree name')
        need(e['type'] in ('tree', 'blob'), 'ordinary tree/blob')
        body += e['mode'].lstrip('0').encode() + b' ' + e['path'].encode() + b'\0' + bytes.fromhex(e['sha'])
    return obj('tree', body)


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s).casefold() if c.isalnum())


def actual(name):
    o = load(A / name)
    need(o['actual_tool'] == 'mcp__codex_apps__github_fetch' and o['whole_returned_wrapper']['isError'] is False, 'actual GitHub read wrapper')
    return json.loads(o['whole_returned_wrapper']['structuredContent']['content'])


def main():
    need(not sys.argv[1:], 'read-only default only')
    check({'path': str(A / 'INITIAL_SEAL.json'), 'bytes': 404,
           'SHA256': 'bba8b25c7bfa5a62860c0f30c4ef35ec6b5f2b0d7189d308b3a2b49f70886901'})
    seal = load(A / 'INITIAL_SEAL.json')
    initial = json.loads(check(seal['initial']))
    targets = initial['targets']
    need([(t['record_id'], t['sheet_row']) for t in targets] == [('23331331', 133), ('23203732', 137), ('23204591', 138)], 'exact next fixed targets')
    for t in targets:
        source, editorial = json.loads(check(t['source_ready'])), json.loads(check(t['root_editorial_adoption']))
        need(str(source['record_id']) == t['record_id'] and source['sheet_row'] == t['sheet_row'], 'native target identity')
        need(all(source[k] == v for k, v in t['identity'].items()), 'whole selected source identity/date/version')
        need(editorial['status'] == t['root_editorial_status'] and editorial['proposed_slug'] == t['root_proposed_slug'], 'current root editorial identity')
    branch, root = actual('open-branch.connector.json'), actual('open-root.connector.json')
    commit = branch['commit']['sha']
    need(branch['name'] == 'main' and commit == initial['root_supplied_remote_main_before_observation'], 'actual main opening identity')
    need(root['sha'] == branch['commit']['commit']['tree']['sha'] and root['truncated'] is False and tree(root['tree']) == root['sha'], 'whole current root tree')
    docs = [e for e in root['tree'] if e['path'] == 'docs']
    need(len(docs) == 1 and docs[0]['type'] == 'tree' and docs[0]['sha'] == initial['previous_docs_subtree_reference_only'], 'actual current docs subtree')
    c = json.loads(check(initial['old_authenticated_corpus_reference']))
    need(c['current_docs_subtree'] == c['docs_tree_reconstructed'] == docs[0]['sha'], 'same exact corpus, no conclusion adopted')
    refs = {Path(r['path']).name: r for r in c['reference_bindings']}
    need(len(refs) == len(c['reference_bindings']) == 5, 'finite unique corpus metadata references')
    for r in refs.values():
        check(r)
    blobs, reps = c['whole_blob_bindings'], c['whole_text_representations']
    need(blobs == json.loads(check(refs['CURRENT_BLOB_BINDINGS.json'])) and reps == json.loads(check(refs['SEARCH_REPRESENTATIONS.json'])), 'whole original body/text interface')
    w = json.loads(check(refs['docs-recursive.json']))
    recursive = json.loads(w['result']['structuredContent']['content'])
    need(recursive['sha'] == docs[0]['sha'] and recursive['truncated'] is False, 'complete immutable recursive docs tree')
    children = {}
    for e in recursive['tree']:
        p = PurePosixPath(e['path'])
        need(not p.is_absolute() and '..' not in p.parts, 'safe recursive path')
        parent = '' if str(p.parent) == '.' else str(p.parent)
        children.setdefault(parent, []).append({**e, 'path': p.name})
    for e in recursive['tree']:
        if e['type'] == 'tree':
            need(tree(children[e['path']]) == e['sha'], 'exact recursive child object')
    need(tree(children['']) == docs[0]['sha'], 'exact docs root object')
    bypath = {r['path']: r for r in blobs}
    native = [e for e in recursive['tree'] if e['type'] == 'blob']
    need(len(blobs) == len(bypath) == len(native) == 254 and len(reps) == 260, 'exact bounded corpus extent')
    need(set(bypath) == {'docs/' + e['path'] for e in native}, 'whole exact path coverage')
    for e in native:
        r = bypath['docs/' + e['path']]
        b = check(r['reused_complete_body'])
        need(obj('blob', b) == r['blob'] == e['sha'] and len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['SHA256'] and r['mode'] == e['mode'], 'whole blob/mode/size/SHA identity')
    hits, paths = [], []
    for r in reps:
        b = check(r['text_file'])
        text = b.decode('utf-8')
        need(r['public_path'] in bypath and r['blob'] == bypath[r['public_path']]['blob'], 'text-to-current-blob interface')
        if r['kind'] == 'raw_UTF8':
            need(obj('blob', b) == r['blob'], 'entire original UTF8')
        if r['kind'] == 'complete_PDF_text':
            ex = r['original_whole_PDF_extract_binding']
            need(ex['pdf_blob'] == r['blob'] and ex['pdf_sha256'] == bypath[r['public_path']]['SHA256'] and check(ex) == b, 'complete historical PDF-text provenance')
        compact = norm(text)
        for t in targets:
            exact = [s for s in t['exact_queries'] if s.casefold() in text.casefold()]
            aliases = [s for s in t['normalized_aliases'] if norm(s) in compact]
            if exact or aliases:
                hits.append({'record_id': t['record_id'], 'public_path': r['public_path'], 'blob': r['blob'], 'kind': r['kind'], 'exact_hits': exact, 'normalized_alias_hits': aliases, 'complete_text_binding': r['text_file']})
    for p in sorted(bypath):
        for t in targets:
            matched = [s for s in t['exact_queries'] + t['normalized_aliases'] if norm(s) in norm(p)]
            if matched:
                paths.append({'record_id': t['record_id'], 'public_path': p, 'matched': matched})
    html = {p for p in bypath if p.casefold().endswith(('.html', '.htm'))}
    need(len(html) == 47 and all(sorted(r['kind'] for r in reps if r['public_path'] == p) == ['decoded_HTML', 'raw_UTF8'] for p in html), 'complete47HTML raw/decoded coverage')
    if (A / 'FINAL_SEAL.json').exists():
        final = load(A / 'FINAL_SEAL.json')
        manifest = json.loads(check(final['manifest']))
        need(not any(p.is_dir() or p.is_symlink() for p in A.iterdir()), 'flat ordinary final extent')
        need(sorted(p.name for p in A.iterdir()) == sorted([r['path'] for r in manifest['files']] + ['MANIFEST.json', 'FINAL_SEAL.json']), 'strict finite final files')
        for r in manifest['files']:
            need('/' not in r['path'] and r['path'] not in ('.', '..'), 'flat exact manifest payload')
            check({**r, 'path': str(A / r['path'])})
    result = {'status': 'BOUNDED_IDENTITY_SCAN_COMPLETE', 'opening_commit': commit, 'root_tree': root['sha'], 'docs_subtree': docs[0]['sha'],
              'root_entries': len(root['tree']), 'docs_tree_objects_including_root': 1 + sum(e['type'] == 'tree' for e in recursive['tree']),
              'whole_blob_paths': len(blobs), 'complete_text_representations': len(reps), 'representation_kinds': dict(Counter(r['kind'] for r in reps)),
              'unique_paths_with_text': len({r['public_path'] for r in reps}), 'opaque_paths_without_text': len(set(bypath) - {r['public_path'] for r in reps}),
              'HTML_paths_with_complete_raw_and_decoded_text': len(html), 'text_hits': hits, 'pathname_hits': paths,
              'new_network_Git_or_PDF_extraction': False, 'writes': 0, 'no_scientific_verdict': True}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
