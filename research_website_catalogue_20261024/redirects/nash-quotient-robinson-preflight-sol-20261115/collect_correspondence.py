#!/usr/bin/env python3
"""Bounded cache reuse/search, no network, Git, source execution or PDF text extraction."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import html
import json
import re
import shutil
import unicodedata

A = Path(__file__).resolve().parent
P = A.parents[1]
B = P / 'redirects/median-gap-preflight-sol-20261115'
APP = P / 'redirects/strict-gap-root-application-20261115'
if (A / 'FINAL_SEAL.json').exists():
    raise RuntimeError('sealed preflight is immutable')


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_hash(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'SHA256': sha(b)}


def load(p):
    return json.loads(p.read_text())


def put(name, obj):
    path = A / name
    if not path.resolve().is_relative_to(A):
        raise ValueError('outside owned namespace')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def verified_pin(entry, base=None):
    p = Path(entry['path'])
    if not p.is_absolute():
        p = base / p
    expected = entry.get('SHA256', entry.get('sha256'))
    b = p.read_bytes()
    if len(b) != entry['bytes'] or sha(b) != expected:
        raise ValueError('prior byte binding failed: ' + str(p))
    return p


def native(p):
    x = load(p)
    if x.get('isError'):
        raise ValueError('connector failed')
    return json.loads(x['structuredContent']['content'])


def tree_hash(entries):
    rows = sorted(entries, key=lambda x: (x['path'] + ('/' if x['type'] == 'tree' else '')).encode())
    body = b''.join(str(int(e['mode'])).encode() + b' ' + e['path'].encode() + b'\0' + bytes.fromhex(e['sha']) for e in rows)
    return git_hash('tree', body)


prior_seal = load(B / 'FINAL_SEAL.json')
if sha((B / 'OWNED_MANIFEST.json').read_bytes()) != prior_seal['OWNED_MANIFEST_SHA256']:
    raise ValueError('prior manifest anchor')
prior_owned = load(B / 'OWNED_MANIFEST.json')
for e in prior_owned['files']:
    verified_pin(e, B)
prior_owned_set = {e['path'] for e in prior_owned['files']}
prior_input = load(B / 'INPUT_MANIFEST.json')
if sha((B / 'INPUT_MANIFEST.json').read_bytes()) != prior_seal['INPUT_MANIFEST_SHA256']:
    raise ValueError('prior input manifest anchor')
old = load(B / 'CURRENT_BLOB_BINDINGS.json')
old_by_path = {e['path']: e for e in old}
tree = native(A / 'raw/current-docs-recursive.json')
if tree['sha'] != 'f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3' or tree['truncated'] is not False:
    raise ValueError('assigned complete docs scope')
groups = {'': []}
expected_trees = {'': tree['sha']}
for e in tree['tree']:
    parent, _, name = e['path'].rpartition('/')
    groups.setdefault(parent, []).append({**e, 'path': name})
    if e['type'] == 'tree':
        groups.setdefault(e['path'], [])
        expected_trees[e['path']] = e['sha']
for directory, entries in groups.items():
    if tree_hash(entries) != expected_trees[directory]:
        raise ValueError('recursive native tree reconstruction failed: ' + directory)
leaves = [e for e in tree['tree'] if e['type'] == 'blob']
if len(leaves) != 254 or {'docs/' + e['path'] for e in leaves} != set(old_by_path):
    raise ValueError('unexpected docs membership; do not silently reuse a narrower corpus')
changed = [e for e in leaves if e['sha'] != old_by_path['docs/' + e['path']]['blob']]
if len(changed) != 1 or changed[0]['path'] != 'papers/strict-dirichlet-gap/index.html' or changed[0]['sha'] != '7b7411fefe1638f4721bc2180486574497f69ab0':
    raise ValueError('unexpected docs delta')
app_manifest = load(APP / 'OWNED_MANIFEST.json')
app_seal = load(APP / 'FINAL_SEAL.json')
verified_pin(app_seal['bindings']['OWNED_MANIFEST.json'])
delivery = load(APP / 'http/AFTERBUILD1/ALL_DELIVERIES.json')
index_delivery = next(x for x in delivery['records'] if x['legacy_name'] == 'index.html')
body_path = Path(index_delivery['hops'][-1]['body_path'])
body = body_path.read_bytes()
if git_hash('blob', body) != changed[0]['sha'] or sha(body) != 'dedb9326ddf053603601dc22355b00c555ed1ec05a8767b6119bcec03455965c':
    raise ValueError('exact current119 redirect body identity')
app_entry = next(e for e in app_manifest['files'] if e['path'] == str(body_path))
verified_pin(app_entry)
new_raw = A / 'cache-new' / (changed[0]['sha'] + '.raw')
new_raw.write_bytes(body)


class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden -= 1

    def handle_data(self, value):
        if self.hidden == 0:
            self.parts.append(value)


v = Visible(); v.feed(body.decode())
new_visible = A / 'cache-new' / (changed[0]['sha'] + '.visible.txt')
new_visible.write_text(' '.join(v.parts))
pdf_bindings = load(B / 'REUSED_EXTRACT_BINDINGS.json')
pdf_by_path = {x['public_path']: x for x in pdf_bindings}
representations = []
current = []
used_external = {}
for e in leaves:
    public = 'docs/' + e['path']
    prior = old_by_path[public]
    if e['mode'] != prior['mode'] or e['size'] != (len(body) if e in changed else prior['bytes']):
        raise ValueError('unexpected leaf type/size')
    item = {'path': public, 'mode': e['mode'], 'kind': e['type'], 'blob': e['sha'], 'bytes': e['size'],
            'SHA256': sha(body) if e in changed else prior['sha256'],
            'body_authentication': 'sealed_actual119_HTTP_body_copy' if e in changed else 'prior_sealed_full_body_authentication_reused_by_exact_unchanged_Git_blob_identity',
            'prior_body_binding': None if e in changed else prior}
    current.append(item)
    raw = new_raw if e in changed else B / 'corpus' / (e['sha'] + '.raw')
    if raw.exists():
        b = raw.read_bytes()
        if len(b) != item['bytes'] or sha(b) != item['SHA256'] or git_hash('blob', b) != e['sha']:
            raise ValueError('raw current body/cache mismatch')
        b.decode('utf8')
        representations.append({'public_path': public, 'blob': e['sha'], 'kind': 'raw_UTF8', 'text_file': pin(raw), 'prior_parse_reused': e not in changed})
        if e not in changed:
            used_external[str(raw)] = pin(raw)
    visible = new_visible if e in changed else B / 'corpus' / (e['sha'] + '.visible.txt')
    if visible.exists():
        if e not in changed and str(visible.relative_to(B)) not in prior_owned_set:
            raise ValueError('unbound old HTML parse')
        representations.append({'public_path': public, 'blob': e['sha'], 'kind': 'decoded_HTML', 'text_file': pin(visible), 'prior_parse_reused': e not in changed})
        if e not in changed:
            used_external[str(visible)] = pin(visible)
    if public in pdf_by_path:
        old_pdf = pdf_by_path[public]
        if old_pdf['pdf_blob'] != e['sha'] or old_pdf['pdf_sha256'] != item['SHA256']:
            raise ValueError('PDF parse association is not current exact blob')
        p = verified_pin(old_pdf)
        if not any(x['path'] == str(p) and x.get('SHA256', x.get('sha256')) == old_pdf['sha256'] for x in prior_input['files']):
            raise ValueError('old complete PDF extract not anchored in prior input manifest')
        representations.append({'public_path': public, 'blob': e['sha'], 'kind': 'complete_PDF_text',
                                'text_file': pin(p), 'pages': old_pdf['pages'], 'prior_parse_reused': True,
                                'original_whole_PDF_extract_binding': old_pdf})
        used_external[str(p)] = pin(p)
if len(representations) != 260:
    raise ValueError('representation scope differs from authenticated corpus')
put('CURRENT_BODY_MANIFEST.json', current)
put('SEARCH_REPRESENTATIONS.json', representations)
put('REUSED_EXTERNAL_BYTE_MANIFEST.json', list(used_external.values()))
put('DOCS_REUSE_PROOF.json', {'UTC': now(), 'prior_seal': pin(B / 'FINAL_SEAL.json'),
    'prior_owned_manifest': pin(B / 'OWNED_MANIFEST.json'), 'prior_input_manifest': pin(B / 'INPUT_MANIFEST.json'),
    'prior_owned_payloads_checked': len(prior_owned['files']), 'prior_tree': prior_seal['released_docs_tree'],
    'actual_current_docs_tree': tree['sha'], 'all_recursive_tree_hashes_reconstructed': len(groups),
    'current_blob_path_occurrences': len(current), 'unique_current_blob_ids': len({x['blob'] for x in current}),
    'unchanged_body_occurrences_reused': len(current) - 1,
    'changed_only_path': 'docs/' + changed[0]['path'], 'old_blob': old_by_path['docs/' + changed[0]['path']]['blob'],
    'new_blob': changed[0]['sha'], 'new_body_source': pin(body_path), 'new_body_source_application_seal': pin(APP / 'FINAL_SEAL.json'),
    'binary_body_hashes_inherited_not_fresh_binary_rehash_claim': True,
    'new_full_PDF_text_extractions': 0, 'archive_expansions_or_source_programmes': [],
    'raw_UTF8_occurrences': sum(x['kind'] == 'raw_UTF8' for x in representations),
    'decoded_HTML_occurrences': sum(x['kind'] == 'decoded_HTML' for x in representations),
    'complete_PDF_text_path_occurrences': sum(x['kind'] == 'complete_PDF_text' for x in representations),
    'unique_complete_PDF_text_files': len({x['text_file']['path'] for x in representations if x['kind'] == 'complete_PDF_text'}),
    'complete_PDF_pages_path_occurrence_total': sum(x.get('pages', 0) for x in representations),
    'new_HTML_visible_parse_only': 1, 'local_Git_or_ref_operation': False,
    'unexpanded_binary_archives_searched_by_whole_native_asset_identity_only': True})

target_specs = [('23578599', 'config/publication.json'), ('23423736', 'configs/publication.json'), ('23333002', 'publication.json')]
targets = []
for rid, rel in target_specs:
    E = P / 'papers' / rid / 'reviews/editorial'
    config = E / rel
    seal = E / 'SEAL.json'
    c = load(config); se = load(seal)
    if rid == '23578599':
        expected = se['PRIVATE_PUBLICATION_CONFIG_SHA256']
    elif rid == '23423736':
        expected = se['publication_json_SHA256']
    else:
        expected = se['bindings']['publication.json']['SHA256']
    if sha(config.read_bytes()) != expected:
        raise ValueError('config not bound by final editorial seal')
    src_path = P / 'papers' / rid / 'sources/SOURCE_READY.json'
    src = load(src_path)
    folder = A / 'target-inputs' / rid
    folder.mkdir(parents=True, exist_ok=True)
    for p, name in [(config, 'publication.json'), (seal, 'EDITORIAL_SEAL.json'), (src_path, 'SOURCE_READY.json')]:
        shutil.copyfile(p, folder / name)
    fields = ['title', 'slug', 'doi', 'publication_date', 'version', 'canonical_url', 'AA',
              'native_sheet_aa_url', 'proposed_canonical_url', 'pdf_filename', 'pdf_pages', 'supplement_filename']
    t = {'record_id': rid, 'source_ready': pin(src_path), 'editorial_seal': pin(seal), 'config': pin(config),
         'owned_raw_config_copy': pin(folder / 'publication.json'),
         'literal_fields': {k: c[k] for k in fields if k in c}, 'fields_absent': [k for k in fields if k not in c],
         'native_concept_record_original': src['native_conceptrecid_whole_field'],
         'whole_original_native_assets_in_order': src['all_native_assets_in_original_order'],
         'proposed_target_only_not_live_or_AA_authority': True}
    targets.append(t)
put('TARGET_IDENTITIES.json', {'UTC': now(), 'targets': targets,
    'informed_prior_roles': {'23578599': 'source metadata/custody acquisition',
      '23423736': 'source acquisition and completed independent analytic science',
      '23333002': 'source acquisition and completed informed editorial preparation'},
    'operational_correspondence_not_new_blind_scientific_review': True,
    'no_config_canonical_or_AA_flags_rewritten': True})
asset_comparisons = []
for t in targets:
    for asset in t['whole_original_native_assets_in_order']:
        p = Path(asset['path']); b = p.read_bytes()
        if len(b) != asset['bytes'] or sha(b) != asset['SHA256']:
            raise ValueError('frozen native asset identity')
        if hashlib.md5(b).hexdigest() != asset['original_api_file_object']['checksum'].split(':')[1]:
            raise ValueError('frozen native asset MD5')
        asset_comparisons.append({'record_id': t['record_id'], 'native_asset': asset,
            'current_docs_exact_SHA256_and_size_matches': [x for x in current if x['SHA256'] == asset['SHA256'] and x['bytes'] == asset['bytes']],
            'new_native_GET_claimed': False})
put('NATIVE_ASSET_COMPARISONS.json', asset_comparisons)

def fold(s):
    return unicodedata.normalize('NFKC', s).casefold().translate(str.maketrans('‐‑‒–—−', '------'))


def compact(s):
    return ''.join(c for c in fold(s) if c.isalnum())


patterns = {
 '23578599': [('distinctive', r'nash[- ]intersection|free[- ]chain'),
              ('broader_claim_context', r'\bnash\b|curvett|divisorial|contact loc(?:us|i)|point blow[- ]?up')],
 '23423736': [('distinctive', r'rogalski|sierra|projective[- ]line quotient|twisted homogeneous coordinate'),
              ('broader_claim_context', r'x[_ ]?3\s*-\s*x[_ ]?1|x[_ ]?4\s*-\s*x[_ ]?2|birationally commutative|graded prime ideal')],
 '23333002': [('distinctive', r'robinson|tangency|schweighofer|ideal[- ]only|gradient ideal'),
              ('broader_claim_context', r'\bschur\b|non[- ]sos|sum(?:s)? of (?:polynomial )?squares|sextic')]}
queries = []
for t in targets:
    rid = t['record_id']
    ids = [rid, str(t['native_concept_record_original']['original_value']), t['literal_fields']['doi']]
    queries.append({'record_id': rid, 'tier': 'record_DOI_concept', 'pattern': '|'.join(re.escape(s) for s in ids), 'mode': 'regex'})
    queries.append({'record_id': rid, 'tier': 'exact_title_compact', 'pattern': compact(t['literal_fields']['title']), 'mode': 'compact_literal'})
    for tier, pattern in patterns[rid]:
        queries.append({'record_id': rid, 'tier': tier, 'pattern': pattern, 'mode': 'regex'})
put('QUERY_DEFINITIONS.json', {'normalization': 'NFKC/casefold and six dash variants to ASCII; title additionally strips nonalphanumerics', 'queries': queries})
hits = []
for representation in representations:
    original = Path(representation['text_file']['path']).read_text()
    text = fold(original)
    for q in queries:
        if q['mode'] == 'compact_literal':
            matches = [m for m in re.finditer(re.escape(q['pattern']), compact(original))]
            if matches:
                hits.append({'record_id': q['record_id'], 'tier': q['tier'], 'representation': representation,
                    'match_count': len(matches), 'compact_match': True, 'original_context': original[:2400],
                    'full_text_bound_not_clipped_for_search': True})
        else:
            matches = list(re.finditer(q['pattern'], text))
            if matches:
                contexts = [{'matched_normalized': m.group(0), 'normalized_start': m.start(),
                             'normalized_context': text[max(0,m.start()-650):min(len(text),m.end()+900)]} for m in matches]
                hits.append({'record_id': q['record_id'], 'tier': q['tier'], 'representation': representation,
                             'match_count': len(matches), 'all_match_contexts': contexts,
                             'full_text_bound_not_clipped_for_search': True})
put('SEARCH_RESULTS.json', {'UTC': now(), 'representations_searched': len(representations), 'hits': hits,
                           'each_whole_representation_searched': True})
put('CORPUS_RECEIPT.json', {'UTC': now(), 'scope_docs_tree': tree['sha'], 'blobs': len(current),
    'representations': len(representations), 'raw_UTF8': sum(x['kind']=='raw_UTF8' for x in representations),
    'decoded_HTML': sum(x['kind']=='decoded_HTML' for x in representations),
    'complete_PDF_text_path_occurrences': len(pdf_bindings), 'complete_PDF_pages_path_occurrences': sum(x['pages'] for x in pdf_bindings),
    'unique_PDF_text_files': len({x['path'] for x in pdf_bindings}), 'new_PDF_text_extractions': 0,
    'archive_expansions': 0, 'source_or_prior_helpers_imported_or_executed': False,
    'search_hit_representation_counts': {rid: {tier: sum(h['record_id']==rid and h['tier']==tier for h in hits)
      for tier in ['record_DOI_concept','exact_title_compact','distinctive','broader_claim_context']} for rid, _ in target_specs}})
print(json.dumps({'status':'BOUNDED_COLLECTION_AND_SEARCH_COMPLETE', 'current_blobs': len(current),
    'current_representations':len(representations),'reconstructed_tree_hashes':len(groups),
    'target_native_exact_asset_matches':sum(len(x['current_docs_exact_SHA256_and_size_matches']) for x in asset_comparisons),
    'hit_rows':len(hits),'counts':load(A/'CORPUS_RECEIPT.json')['search_hit_representation_counts']},indent=2))
