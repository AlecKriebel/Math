#!/usr/bin/env python3
"""Pure custody and bounded search replay; no Git, network, extraction or source imports."""
from pathlib import Path
import hashlib
import json
import re
import sys
import unicodedata

A = Path(__file__).resolve().parent
P = A.parents[1]
B = P / 'redirects/median-gap-preflight-sol-20261115'
SCOPE = 'f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3'
TERMINAL = {'OWNED_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(p):
    return json.loads(Path(p).read_text())


def pin(e, base=None):
    p = Path(e['path'])
    if not p.is_absolute():
        p = base / p
    need(p.is_file() and not p.is_symlink(), 'nonregular/missing pin: ' + str(p))
    b = p.read_bytes()
    need(len(b) == e['bytes'] and hashlib.sha256(b).hexdigest() == e.get('SHA256', e.get('sha256')),
         'byte binding changed: ' + str(p))
    return b


def pins(x):
    if isinstance(x, dict):
        if all(k in x for k in ['path', 'bytes']) and ('SHA256' in x or 'sha256' in x):
            pin(x)
        else:
            for value in x.values():
                pins(value)
    elif isinstance(x, list):
        for value in x:
            pins(value)


def native(p):
    x = read(p)
    need(x.get('isError') is not True, 'connector failure')
    return json.loads(x['structuredContent']['content'])


def git_hash(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def tree_hash(entries):
    ordered = sorted(entries, key=lambda x: (x['path'] + ('/' if x['type'] == 'tree' else '')).encode())
    b = b''.join(str(int(e['mode'])).encode() + b' ' + e['path'].encode() + b'\0' + bytes.fromhex(e['sha']) for e in ordered)
    return git_hash('tree', b)


def fold(s):
    return unicodedata.normalize('NFKC', s).casefold().translate(str.maketrans('‐‑‒–—−', '------'))


def compact(s):
    return ''.join(c for c in fold(s) if c.isalnum())


def main():
    inputs = read(A / 'INPUT_MANIFEST.json')
    pins(inputs)
    prior = read(B / 'FINAL_SEAL.json')
    need(hashlib.sha256((B / 'OWNED_MANIFEST.json').read_bytes()).hexdigest() == prior['OWNED_MANIFEST_SHA256'], 'prior manifest anchor')
    for e in read(B / 'OWNED_MANIFEST.json')['files']:
        pin(e, B)
    pins(read(A / 'REUSED_EXTERNAL_BYTE_MANIFEST.json'))
    old = {e['path']: e for e in read(B / 'CURRENT_BLOB_BINDINGS.json')}
    t = native(A / 'raw/current-docs-recursive.json')
    need(t['sha'] == SCOPE and t['truncated'] is False, 'actual assigned complete docs tree')
    groups = {'': []}; hashes = {'': SCOPE}
    for e in t['tree']:
        need(e['type'] in ['tree', 'blob'], 'unexpected non-blob/tree docs entry')
        parent, _, name = e['path'].rpartition('/')
        groups.setdefault(parent, []).append({**e, 'path': name})
        if e['type'] == 'tree':
            groups.setdefault(e['path'], [])
            hashes[e['path']] = e['sha']
    need(len(groups) == 51 and all(tree_hash(v) == hashes[k] for k,v in groups.items()), 'all51 recursive tree hashes')
    for prefix in ['opening', 'closing']:
        ref = native(A / 'raw' / (prefix + '-main.json'))
        commit = native(A / 'raw' / (prefix + '-commit.json'))
        root = native(A / 'raw' / (prefix + '-root-tree.json'))
        need(ref['object']['sha'] == commit['sha'] and commit['tree']['sha'] == root['sha'], 'actual observed ref/commit/root association')
        need(root['truncated'] is False and tree_hash(root['tree']) == root['sha'], 'actual observed root hash')
        need(next(e['sha'] for e in root['tree'] if e['path'] == 'docs') == SCOPE, 'opening/closing docs scope differs')
    rows = read(A / 'CURRENT_BODY_MANIFEST.json')
    by_path = {e['path']: e for e in rows}
    leaves = [e for e in t['tree'] if e['type'] == 'blob']
    need(len(rows) == len(by_path) == len(leaves) == 254 and set(by_path) == set(old), 'complete254 current body set')
    changed = []
    for e in leaves:
        row = by_path['docs/' + e['path']]; previous = old[row['path']]
        need((row['blob'],row['mode'],row['bytes']) == (e['sha'],e['mode'],e['size']), 'current body/native leaf association')
        if row['blob'] == previous['blob']:
            need(row['SHA256'] == previous['sha256'] and row['prior_body_binding'] == previous, 'exact unchanged prior body authentication')
        else:
            changed.append(row)
    need(len(changed) == 1 and changed[0]['path'] == 'docs/papers/strict-dirichlet-gap/index.html' and
         changed[0]['blob'] == '7b7411fefe1638f4721bc2180486574497f69ab0' and changed[0]['bytes'] == 838, 'known119 sole docs delta')
    representations = read(A / 'SEARCH_REPRESENTATIONS.json')
    need(len(representations) == 260 and sum(x['kind']=='raw_UTF8' for x in representations) == 137 and
         sum(x['kind']=='decoded_HTML' for x in representations) == 47 and
         sum(x['kind']=='complete_PDF_text' for x in representations) == 76 and
         sum(x.get('pages',0) for x in representations) == 854, 'exact representation/page scope')
    need(len({x['text_file']['path'] for x in representations if x['kind']=='complete_PDF_text'}) == 73, 'unique cached PDF texts')
    q = read(A / 'QUERY_DEFINITIONS.json')['queries']
    actual_hits = []
    for r in representations:
        b = pin(r['text_file']); body = b.decode('utf8')
        need(r['blob'] == by_path[r['public_path']]['blob'], 'stale representation blob')
        if r['kind'] == 'raw_UTF8':
            need(git_hash('blob', b) == r['blob'] and hashlib.sha256(b).hexdigest() == by_path[r['public_path']]['SHA256'], 'whole UTF8 current body')
        if r['kind'] == 'complete_PDF_text':
            old_pdf = r['original_whole_PDF_extract_binding']
            need(old_pdf['pdf_blob'] == r['blob'] and old_pdf['pdf_sha256'] == by_path[r['public_path']]['SHA256'], 'inherited full PDF text association')
        folded = fold(body); title_text = compact(body)
        for query in q:
            count = len(list(re.finditer(re.escape(query['pattern']), title_text))) if query['mode']=='compact_literal' else len(list(re.finditer(query['pattern'],folded)))
            if count:
                actual_hits.append((query['record_id'],query['tier'],r['public_path'],r['kind'],count))
    search = read(A / 'SEARCH_RESULTS.json')
    stored = [(h['record_id'],h['tier'],h['representation']['public_path'],h['representation']['kind'],h['match_count']) for h in search['hits']]
    need(actual_hits == stored and len(stored) == 14, 'whole-corpus bounded search replay')
    path_search = read(A / 'PATHNAME_SEARCH_RESULTS.json')
    need(path_search['all_current_paths_searched'] == 254 and path_search['hits'] == [] and
         all(not x['matching_current_paths'] for x in path_search['distinctive_native_filename_checks']), 'pathname/filename disposition')
    for row in rows:
        for query in q:
            match = query['pattern'] in compact(row['path']) if query['mode']=='compact_literal' else re.search(query['pattern'],fold(row['path']))
            need(not match, 'missed current pathname match')
    exclusions = read(A / 'EXCLUSIONS.json')
    partition = [i for g in exclusions['groups'] for i in g['hit_rows']]
    need(sorted(partition) == list(range(14)), 'false-hit rows not completely disposed')
    targets = read(A / 'TARGET_IDENTITIES.json')['targets']
    comparison = read(A / 'NATIVE_ASSET_COMPARISONS.json')
    need(len(targets) == 3 and len(comparison) == 6, 'exact target/asset cardinality')
    for target in targets:
        rid = target['record_id']; config = json.loads(pin(target['config']))
        need(pin(target['config']) == pin(target['owned_raw_config_copy']), 'exact sealed config snapshot')
        pin(target['editorial_seal']); source = json.loads(pin(target['source_ready']))
        need((A/'target-inputs'/rid/'SOURCE_READY.json').read_bytes() == Path(target['source_ready']['path']).read_bytes(), 'whole raw source snapshot')
        seal = read(target['editorial_seal']['path'])
        expected = seal['PRIVATE_PUBLICATION_CONFIG_SHA256'] if rid=='23578599' else seal['publication_json_SHA256'] if rid=='23423736' else seal['bindings']['publication.json']['SHA256']
        need(hashlib.sha256(pin(target['config'])).hexdigest() == expected, 'proposal not bound by final editorial seal')
        for key,value in target['literal_fields'].items():
            need(key in config and type(value) is type(config[key]) and value == config[key], 'literal target field')
        need(config['canonical_url'] is None and config['AA'] is None, 'private canonical/AA snapshot')
        need(str(source['record_id']) == rid and config['doi'] == source['DOI'] and config['version'] == source['version'] and
             config['publication_date'] == source['publication_date'], 'source version/record identity')
    for item in comparison:
        asset = item['native_asset']; b = pin(asset)
        need(hashlib.md5(b).hexdigest() == asset['original_api_file_object']['checksum'].split(':')[1], 'native MD5 identity')
        actual = [r for r in rows if r['SHA256']==asset['SHA256'] and r['bytes']==asset['bytes']]
        need(actual == item['current_docs_exact_SHA256_and_size_matches'] == [], 'native full asset match disposition')
    ledger = read(A / 'REMOTE_GET_LEDGER.json')
    need(len(ledger['calls']) == 7 and ledger['mutating_calls'] == [] and all(not c['mutating'] for c in ledger['calls']), 'exact readonly transport set')
    for call in ledger['calls']:
        need(read(call['result_file']).get('isError') is not True, 'actual GET tool failure')
    verdict = read(A / 'CUSTOM_VERDICT.json')
    for item in verdict['records'].values():
        need(item['disposition']=='BOUNDED_NEGATIVE_NO_GENUINE_CORRESPONDENCE_LOCATED' and item['genuine_legacy_URL'] is None and
             item['redirect_candidate_prepared'] is False and item['redirect_authority'] is False, 'unjustified redirect/correspondence claim')
    need(verdict['follow_up'] is None and verdict['global_or_repository_history_or_unexpanded_archive_absence_claim'] is False, 'absence/follow-up scope')
    annotations = read(A/'NATIVE_PDF_ANNOTATION_IDENTITIES.json')
    need(annotations['metadata_annotation_inspection_completed'] is False and annotations['new_PDF_text_extractions'] == 0, 'actual optional reader limit')
    if (A/'OWNED_MANIFEST.json').exists():
        manifest = read(A/'OWNED_MANIFEST.json')
        expected = {e['path'] for e in manifest['files']}
        actual = {str(p) for p in A.rglob('*') if p.is_file() and p.name not in TERMINAL}
        need(actual == expected and len(expected)==len(manifest['files']), 'exact fail-closed owned membership')
        pins(manifest['files'])
    if (A/'FINAL_SEAL.json').exists():
        pins(read(A/'FINAL_SEAL.json')['bindings'])
    return {'status':'PASS_BOUNDED_CORRESPONDENCE_AND_CUSTODY','docs_tree':SCOPE,'reconstructed_docs_trees':51,
            'current_blob_paths':254,'replayed_whole_text_representations':260,'PDF_path_occurrences':76,'unique_PDF_texts':73,
            'PDF_pages_path_occurrence_total':854,'native_original_assets_compared':6,'native_exact_asset_matches':0,
            'false_hit_representation_rows_completely_disposed':14,'genuine_candidates_located':0,
            'native_annotation_reader_unavailable_limit_preserved':True,'new_PDF_extractions':0,
            'Git_network_source_execution_or_writes':False,'redirect_or_publication_authority':False}


if __name__ == '__main__':
    try:
        print(json.dumps(main(),indent=2))
    except (ValueError,KeyError,OSError,TypeError,StopIteration) as error:
        print(json.dumps({'status':'FAIL','error':str(error)}))
        sys.exit(1)
