"""Pure offline custody/search closure: stdlib reads only, no target imports or writes."""
from pathlib import Path
import hashlib
import json
import re
import sys
import unicodedata

A = Path(__file__).resolve().parent
TERMINALS = ['FINAL_CLOSURE.json', 'FINAL_SEAL.json', 'OWNED_MANIFEST.json']
DOCS = 'f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3'
checks = 0


def need(ok, message):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError(message)


def read(path):
    need(path.is_file() and not path.is_symlink(), 'regular input ' + str(path))
    return path.read_bytes()


def load(path):
    return json.loads(read(path))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check(item, path=None):
    path = Path(item['path']) if path is None else path
    raw = read(path)
    need(len(raw) == item['bytes'] and sha(raw) == item.get('SHA256', item.get('sha256')), 'byte pin ' + str(path))
    return raw


def namespace(root):
    files, dirs = [], []
    for path in root.rglob('*'):
        need(not path.is_symlink(), 'namespace symlink')
        relative = path.relative_to(root).as_posix()
        if path.is_dir():
            dirs.append(relative)
        else:
            need(path.is_file(), 'namespace nonregular')
            files.append(relative)
    return sorted(files), sorted(dirs)


def native(role):
    packet = load(A / 'raw' / (role + '.json'))
    need(packet['role'] == role and packet['result']['isError'] is False, 'native result role')
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
    need(sys.argv[1:] in ([], ['--preseal']), 'only preseal or default')
    preseal = sys.argv[1:] == ['--preseal']
    manifest = load(A / 'OWNED_MANIFEST.json')
    need(manifest['owner_namespace'] == str(A), 'owner root')
    need(manifest['exact_root_relative_terminal_exclusions'] == TERMINALS, 'exact root terminal exclusions')
    files, dirs = namespace(A)
    payloads = [x for x in files if x not in TERMINALS]
    need(payloads == sorted(x['path'] for x in manifest['files']), 'closed owned files')
    need(dirs == manifest['directories'], 'closed owned directories')
    for item in manifest['files']:
        relative = Path(item['path'])
        need(not relative.is_absolute() and '..' not in relative.parts, 'safe relative payload')
        check(item, A / relative)
    for item in load(A / 'INPUT_MANIFEST.json')['files']:
        check(item)
    freeze = load(A / 'SCOPE_FREEZE.json')
    need(freeze['docs_subtree_SHA'] == DOCS and freeze['native_target_identity_and_queries_frozen_before_search'] is True, 'frozen boundary')
    reuse = load(A / 'REUSE_AUTHENTICATION.json')
    prior_root = Path(reuse['prior_packet_root'])
    old_files, old_dirs = namespace(prior_root)
    need(old_files == reuse['prior_exact_file_names'], 'closed prior files')
    need(old_dirs == reuse['prior_exact_directories'], 'closed prior directories')
    check(reuse['prior_packet_seal'])

    for prefix in ['opening', 'closing']:
        ref, commit, root = [native(prefix + '-' + suffix) for suffix in ['main', 'commit', 'root']]
        need(ref['ref'] == 'refs/heads/main' and ref['object']['type'] == 'commit', 'actual main ref')
        need(ref['object']['sha'] == commit['sha'] and commit['tree']['sha'] == root['sha'], 'actual commit/root chain')
        need(root['truncated'] is False, 'complete native root')
        docs = [x for x in root['tree'] if x['path'] == 'docs']
        need(len(docs) == 1 and docs[0]['type'] == 'tree' and docs[0]['sha'] == DOCS, 'same exact docs subtree')
        need(tree_hash(root['tree']) == root['sha'], 'whole native root tree hash')
    recursive = native('docs-recursive')
    need(recursive['sha'] == DOCS and recursive['truncated'] is False and len(recursive['tree']) == 304, 'complete docs recursive response')
    groups, hashes = {'': []}, {'': DOCS}
    for entry in recursive['tree']:
        parent, _, basename = entry['path'].rpartition('/')
        groups.setdefault(parent, []).append({**entry, 'path': basename})
        if entry['type'] == 'tree':
            groups.setdefault(entry['path'], [])
            hashes[entry['path']] = entry['sha']
    need(len(groups) == 51, 'all docs tree objects')
    for path, entries in groups.items():
        need(tree_hash(entries) == hashes[path], 'native tree hash ' + path)
    current = load(A / 'CURRENT_BLOB_BINDINGS.json')
    by_path = {x['path']: x for x in current}
    leaves = [x for x in recursive['tree'] if x['type'] == 'blob']
    need(len(current) == len(leaves) == 254 and set(by_path) == {'docs/' + x['path'] for x in leaves}, 'all 254 blob paths')
    for entry in leaves:
        item = by_path['docs/' + entry['path']]
        raw = check(item['reused_complete_body'])
        need((item['blob'], item['mode'], item['bytes']) == (entry['sha'], entry['mode'], entry['size']), 'whole blob association')
        need(sha(raw) == item['SHA256'] and git('blob', raw) == entry['sha'], 'whole native blob bytes')
    need(len({x['blob'] for x in current}) == 247 and sum(x['bytes'] for x in current) == 40684709, 'whole corpus counts')

    targets = load(A / 'TARGET_IDENTITIES.json')
    need([x['record_id'] for x in targets] == ['23578142', '23306203'], 'exact two records')
    need([x['sheet_row'] for x in targets] == [126, 129], 'exact rows')
    for target in targets:
        rid = target['record_id']
        source = json.loads(check(target['SOURCE_READY_pin']))
        record = json.loads(check(target['native_record_pin']))
        need(target['title'] == source['title'] == record['metadata']['title'], 'native title')
        need(target['DOI'] == source['DOI'] == record['metadata']['doi'], 'native DOI')
        need(target['whole_native_metadata'] == record['metadata'], 'whole native metadata retained')
        need(target['native_version_whole_field'] == source['native_version_whole_field'] == {'present': True, 'original_value': '1.0.0'}, 'native version')
        need(target['whole_original_native_assets_in_original_order'] == source['all_native_assets_in_original_order'], 'whole original asset order/objects')
        for asset in target['whole_original_native_assets_in_original_order']:
            raw = check(asset)
            need(hashlib.md5(raw).hexdigest() == asset['original_api_file_object']['checksum'].split(':')[1], 'native checksum')
            need(not any((x['bytes'], x['SHA256']) == (asset['bytes'], asset['SHA256']) for x in current), 'native whole asset comparison')

    representations = load(A / 'SEARCH_REPRESENTATIONS.json')
    need(len(representations) == 260, 'all 260 complete representations')
    kinds = {kind: sum(x['kind'] == kind for x in representations) for kind in ['raw_UTF8', 'decoded_HTML', 'complete_PDF_text']}
    need(kinds == {'raw_UTF8': 137, 'decoded_HTML': 47, 'complete_PDF_text': 76}, 'representation kinds')
    need(sum(x.get('pages', 0) for x in representations) == 854, 'inherited page occurrences not semantic read count')
    definition = load(A / 'QUERY_DEFINITIONS.json')
    queries = definition['queries']
    hits, compact_hits = [], []
    for rep in representations:
        raw = check(rep['text_file'])
        need(rep['blob'] == by_path[rep['public_path']]['blob'], 'representation current association')
        if rep['kind'] == 'raw_UTF8':
            need(git('blob', raw) == rep['blob'], 'raw representation Git hash')
        if rep['kind'] == 'complete_PDF_text':
            z = rep['original_whole_PDF_extract_binding']
            need(z['pdf_blob'] == rep['blob'] and z['pdf_sha256'] == by_path[rep['public_path']]['SHA256'], 'complete PDF/text binding')
        normalized, packed = fold(raw.decode('utf8')), compact(raw.decode('utf8'))
        for query in queries:
            hay = packed if query['mode'] == 'compact_literal' else normalized
            pattern = re.escape(query['pattern']) if query['mode'] == 'compact_literal' else query['pattern']
            if re.search(pattern, hay):
                hits.append((query['record_id'], query['tier'], rep['public_path']))
        for rid, signatures in definition['second_mechanism_compact_aliases'].items():
            for signature in signatures:
                if compact(signature) in packed:
                    compact_hits.append((rid, signature, rep['public_path']))
    need(hits == [] and load(A / 'SEARCH_RESULTS.json')['hits'] == [], 'whole exact/alias/control search replay')
    saved = load(A / 'PUNCTUATION_INSENSITIVE_SEARCH.json')['hits']
    need(compact_hits == [(x['record_id'], x['signature'], x['representation']['public_path']) for x in saved], 'whole compact search replay')
    need(compact_hits == [('23306203', 'k114', 'docs/papers/k3p-theta-trinet-collision/technical-summary.pdf')], 'exact one false compact candidate')
    for entry in current:
        for query in queries:
            hay = compact(entry['path']) if query['mode'] == 'compact_literal' else fold(entry['path'])
            pattern = re.escape(query['pattern']) if query['mode'] == 'compact_literal' else query['pattern']
            need(re.search(pattern, hay) is None, 'whole pathname search')
    need(load(A / 'PATHNAME_SEARCH_RESULTS.json')['hits'] == [], 'saved pathname result')
    exclusions = load(A / 'EXCLUSIONS.json')
    need(len(exclusions['items']) == 1 and exclusions['items'][0]['genuine_corresponding_target_article'] is False, 'concrete false candidate exclusion')
    strict = by_path['docs/papers/strict-dirichlet-gap/index.html']
    need(strict['bytes'] == 838 and strict['SHA256'] == 'dedb9326ddf053603601dc22355b00c555ed1ec05a8767b6119bcec03455965c', 'preserved unrelated redirect')
    verdict = load(A / 'VERDICT.json')
    need(verdict['redirects_prepared'] == [] and verdict['redirects_written'] == [], 'no redirect preparation')
    need(verdict['global_absence_claim'] is False and verdict['redirect_or_publication_authority'] is False, 'bounded authority')
    need(verdict['genuine_corresponding_articles_located'] == 0, 'bounded correspondence result')
    if not preseal:
        need(all((A / name).is_file() for name in TERMINALS), 'existing exact terminals')
        seal = load(A / 'FINAL_SEAL.json')
        for item in seal['bindings'].values():
            check(item)
        need(seal['immutable_after_final'] is True, 'immutable final')
    print(json.dumps({'status': 'PASS_PURE_READ_ONLY_CORRESPONDENCE_CLOSURE', 'mode': 'preseal' if preseal else 'final', 'checks': checks, 'owned_payloads': len(payloads), 'owned_directories': len(dirs), 'current_whole_blob_paths': 254, 'complete_text_representations': 260, 'compact_false_candidates': 1, 'genuine_corresponding_articles': 0, 'network_requests': 0, 'writes': 0, 'subprocesses': 0, 'project_imports': 0, 'scientific_programmes_executed': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
