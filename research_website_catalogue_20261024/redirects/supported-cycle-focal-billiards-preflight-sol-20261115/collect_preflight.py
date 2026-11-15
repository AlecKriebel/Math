"""Own one-time offline byte authentication/search; writes only this new namespace."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import unicodedata

A = Path(__file__).resolve().parent
P = A.parents[1]
B = P / 'redirects/five-centers-mixed-face-preflight-sol-20261115'
DOCS = 'f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3'
external = {}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def bind(path):
    require(not path.is_symlink() and path.is_file(), 'regular external input')
    raw = path.read_bytes()
    item = {'path': str(path), 'bytes': len(raw), 'SHA256': sha(raw)}
    external[str(path)] = item
    return item


def check(item):
    path = Path(item['path'])
    pin = bind(path)
    require(pin['bytes'] == item['bytes'] and pin['SHA256'] == item.get('SHA256', item.get('sha256')), 'input pin ' + str(path))
    return path.read_bytes()


def put(name, value):
    path = A / name
    require(path.parent == A, 'own root output only')
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def native(role):
    packet = load(A / 'raw' / (role + '.json'))
    require(packet['role'] == role and packet['result']['isError'] is False, 'actual native request')
    return json.loads(packet['result']['structuredContent']['content'])


def git(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def tree_hash(entries):
    entries = sorted(entries, key=lambda x: (x['path'] + ('/' if x['type'] == 'tree' else '')).encode())
    raw = b''.join(str(int(x['mode'])).encode() + b' ' + x['path'].encode() + b'\0' + bytes.fromhex(x['sha']) for x in entries)
    return git('tree', raw)


def fold(text):
    return unicodedata.normalize('NFKC', text).casefold().translate(str.maketrans('‐‑‒–—−', '------'))


def compact(text):
    return ''.join(c for c in fold(text) if c.isalnum())


def main():
    require(not (A / 'FINAL_SEAL.json').exists(), 'final is immutable')
    freeze = load(A / 'SCOPE_FREEZE.json')
    require(freeze['native_target_identity_and_queries_frozen_before_search'] is True, 'presearch freeze')
    seal = load(B / 'FINAL_SEAL.json')
    require(sha((B / 'FINAL_SEAL.json').read_bytes()) == freeze['prior_completed_packet']['SHA256'], 'prior seal pin')
    check(seal['bindings']['OWNED_MANIFEST.json'])
    prior = load(B / 'OWNED_MANIFEST.json')
    for item in prior['files']:
        check(item)
    prior_names = sorted(Path(x['path']).relative_to(B).as_posix() for x in prior['files'])
    expected_prior = sorted(prior_names + ['OWNED_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'])
    require(sorted(x.relative_to(B).as_posix() for x in B.rglob('*') if x.is_file()) == expected_prior, 'prior closed file namespace')
    require(not any(x.is_symlink() for x in B.rglob('*')), 'prior symlinks')
    for name in ['FINAL_SEAL.json', 'FINAL_CLOSURE.json', 'OWNED_MANIFEST.json', 'CURRENT_BLOB_BINDINGS.json', 'SEARCH_REPRESENTATIONS.json', 'INPUT_MANIFEST.json', 'CORPUS_RECEIPT.json', 'REMOTE_BOUNDARY.json', 'REPORT.md']:
        bind(B / name)

    opening, commit, root, recursive = [native(x) for x in ['opening-main', 'opening-commit', 'opening-root', 'docs-recursive']]
    require(opening['object']['sha'] == commit['sha'] and commit['tree']['sha'] == root['sha'], 'opening ref chain')
    require(root['truncated'] is False, 'complete root')
    docs = [x for x in root['tree'] if x['path'] == 'docs']
    require(len(docs) == 1 and docs[0]['type'] == 'tree' and docs[0]['sha'] == DOCS, 'current docs tree changed')
    require(recursive['sha'] == DOCS and recursive['truncated'] is False, 'complete recursive tree')
    groups, hashes = {'': []}, {'': DOCS}
    for item in recursive['tree']:
        parent, _, basename = item['path'].rpartition('/')
        groups.setdefault(parent, []).append({**item, 'path': basename})
        if item['type'] == 'tree':
            groups.setdefault(item['path'], [])
            hashes[item['path']] = item['sha']
    for path, items in groups.items():
        require(tree_hash(items) == hashes[path], 'native tree reconstruction ' + path)
    leaves = [x for x in recursive['tree'] if x['type'] == 'blob']
    current = load(B / 'CURRENT_BLOB_BINDINGS.json')
    by_path = {x['path']: x for x in current}
    require(len(leaves) == 254 and set(by_path) == {'docs/' + x['path'] for x in leaves}, 'complete blob membership')
    bodies = []
    for leaf in leaves:
        old = by_path['docs/' + leaf['path']]
        raw = check(old['reused_complete_body'])
        require((old['blob'], old['mode'], old['bytes']) == (leaf['sha'], leaf['mode'], leaf['size']), 'leaf identity')
        require(sha(raw) == old['SHA256'] and git('blob', raw) == leaf['sha'], 'complete native blob bytes')
        bodies.append(old)
    put('CURRENT_BLOB_BINDINGS.json', bodies)

    representations = load(B / 'SEARCH_REPRESENTATIONS.json')
    require(len(representations) == 260, 'complete representation interface')
    for rep in representations:
        raw = check(rep['text_file'])
        require(rep['blob'] == by_path[rep['public_path']]['blob'], 'representation association')
        if rep['kind'] == 'raw_UTF8':
            require(git('blob', raw) == rep['blob'], 'raw UTF8 identity')
        if rep['kind'] == 'complete_PDF_text':
            item = rep['original_whole_PDF_extract_binding']
            require(item['pdf_blob'] == rep['blob'] and item['pdf_sha256'] == by_path[rep['public_path']]['SHA256'], 'whole PDF text binding')
    put('SEARCH_REPRESENTATIONS.json', representations)
    targets = load(A / 'TARGET_IDENTITIES.json')
    asset_matches = []
    for target in targets:
        require(target['native_version_whole_field'] == {'present': True, 'original_value': '1.0.0'}, 'native version distinction')
        check(target['SOURCE_READY_pin'])
        check(target['native_record_pin'])
        check(target['source_seal_pin'])
        for asset in target['whole_original_native_assets_in_original_order']:
            raw = check(asset)
            require(hashlib.md5(raw).hexdigest() == asset['original_api_file_object']['checksum'].split(':')[1], 'native MD5')
            asset_matches.append({'record_id': target['record_id'], 'whole_original_asset': asset,
                                  'whole_current_docs_byte_matches': [x for x in bodies if (x['bytes'], x['SHA256']) == (asset['bytes'], asset['SHA256'])]})
    put('NATIVE_ASSET_COMPARISONS.json', asset_matches)

    query_definition = load(A / 'QUERY_DEFINITIONS.json')
    queries = query_definition['queries']
    hits, path_hits, compact_hits = [], [], []
    for rep in representations:
        raw = check(rep['text_file'])
        text = raw.decode('utf8')
        normalized, packed = fold(text), compact(text)
        for query in queries:
            hay = packed if query['mode'] == 'compact_literal' else normalized
            pattern = re.escape(query['pattern']) if query['mode'] == 'compact_literal' else query['pattern']
            matches = list(re.finditer(pattern, hay))
            if matches:
                hits.append({'record_id': query['record_id'], 'tier': query['tier'], 'representation': rep,
                             'match_count': len(matches), 'all_matches': [{'normalized_start': m.start(), 'matched': m.group(), 'context': hay[max(0, m.start()-600):m.end()+900]} for m in matches]})
        for rid, signatures in query_definition['second_mechanism_compact_aliases'].items():
            for signature in signatures:
                if compact(signature) in packed:
                    compact_hits.append({'record_id': rid, 'signature': signature, 'representation': rep})
    for item in bodies:
        for query in queries:
            hay = compact(item['path']) if query['mode'] == 'compact_literal' else fold(item['path'])
            pattern = re.escape(query['pattern']) if query['mode'] == 'compact_literal' else query['pattern']
            matches = list(re.finditer(pattern, hay))
            if matches:
                path_hits.append({'record_id': query['record_id'], 'tier': query['tier'], 'public_path': item['path'], 'matches': [m.group() for m in matches]})
    put('SEARCH_RESULTS.json', {'UTC': now(), 'representations_searched': 260, 'all_complete_representations_searched': True, 'hits': hits})
    put('PATHNAME_SEARCH_RESULTS.json', {'paths_searched': 254, 'hits': path_hits})
    put('PUNCTUATION_INSENSITIVE_SEARCH.json', {'whole_representations': 260, 'mechanism': 'whole text NFKC/casefold with every nonalphanumeric removed; second mechanism, not another reviewer', 'hits': compact_hits})
    put('REUSE_AUTHENTICATION.json', {'UTC': now(), 'prior_packet_seal': bind(B / 'FINAL_SEAL.json'), 'prior_payload_count': len(prior['files']), 'prior_exact_file_names': expected_prior, 'prior_exact_directories': sorted(x.relative_to(B).as_posix() for x in B.rglob('*') if x.is_dir()), 'prior_packet_root': str(B), 'all_current_whole_bytes_and_Git_blobs_reread': True, 'prior_helpers_imported_or_executed': False})
    put('INPUT_MANIFEST.json', {'UTC': now(), 'files': list(external.values()), 'whole_external_data_not_reserialized_in_place': True})
    put('CORPUS_RECEIPT.json', {'UTC': now(), 'docs_tree_kind': 'docs subtree, not commit', 'docs_tree': DOCS, 'opening_main': opening['object']['sha'], 'opening_root': root['sha'], 'recursive_entries': len(recursive['tree']), 'native_tree_objects_reconstructed': len(groups), 'blob_paths': len(leaves), 'unique_blobs': len({x['blob'] for x in bodies}), 'whole_body_bytes_path_occurrences': sum(x['bytes'] for x in bodies), 'complete_text_representations': len(representations), 'representation_kinds': {kind: sum(x['kind'] == kind for x in representations) for kind in ['raw_UTF8', 'decoded_HTML', 'complete_PDF_text']}, 'PDF_text_path_occurrences_not_new_semantic_reading': sum(x['kind'] == 'complete_PDF_text' for x in representations), 'inherited_PDF_page_occurrences_not_new_semantic_reading': sum(x.get('pages', 0) for x in representations), 'opaque_binary_paths_not_unpacked_or_pixel_searched': sorted(set(by_path) - {x['public_path'] for x in representations}), 'new_PDF_extractions_or_renders': 0, 'scientific_programs_executed': 0})
    print(json.dumps({'status': 'AUTHENTICATED_BOUNDED_SEARCH_COMPLETE', 'hit_rows': len(hits), 'pathname_hits': len(path_hits), 'compact_hits': len(compact_hits), 'hits': [{'record': x['record_id'], 'tier': x['tier'], 'path': x['representation']['public_path'], 'kind': x['representation']['kind'], 'matches': x['match_count']} for x in hits]}, indent=2))


if __name__ == '__main__':
    main()
