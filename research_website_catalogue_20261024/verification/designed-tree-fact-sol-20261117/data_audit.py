"""Bounded data-only audit. Reads local inputs; emits JSON; never writes or executes them."""
import hashlib
import json
import re
import stat
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = P / 'verification/designed-tree-editorial-sol-20261117'
S = P / 'papers/23527793/sources'
T = S / 'published-source/container-001/tree/congestion-fragmentation-verification'

def need(ok, label):
    if not ok:
        raise ValueError(label)

def mode(value):
    return int(value, 8) if isinstance(value, str) else value

def readj(path):
    return json.loads(path.read_text(encoding='utf-8'))

def file_record(path, name):
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode), 'not regular: ' + str(path))
    body = path.read_bytes()
    return {'path': name, 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'mode': oct(stat.S_IMODE(st.st_mode))}

def pin(path, size, digest, expected_mode=0o644):
    got = file_record(path, path.name)
    need((got['bytes'], got['SHA256'], mode(got['mode'])) == (size, digest, expected_mode), 'pin mismatch: ' + str(path))
    return got

def inventory(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'not directory: ' + str(root))
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        st = path.lstat()
        if stat.S_ISDIR(st.st_mode):
            directories.append({'path': rel, 'mode': oct(stat.S_IMODE(st.st_mode))})
        else:
            files.append(file_record(path, rel))
    return {'root': str(root), 'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)), 'files': files, 'directories': directories}

def normalized(entries):
    return sorted(({**entry, 'mode': mode(entry['mode'])} for entry in entries), key=lambda entry: entry['path'])

def authenticate(root, manifest, filekey, excluded):
    inv = inventory(root)
    need(inv['root_mode'] == oct(mode(manifest['root_mode'])), 'root mode mismatch')
    need(manifest.get('root', manifest.get('source_root')) == str(root), 'root path mismatch')
    need(set(manifest['exact_terminal_exclusions']) == set(excluded), 'terminal exclusions mismatch')
    payload = [entry for entry in inv['files'] if entry['path'] not in excluded]
    need(normalized(payload) == normalized(manifest[filekey]), 'whole payload mismatch: ' + str(root))
    need(normalized(inv['directories']) == normalized(manifest['directories']), 'directories mismatch: ' + str(root))
    need({entry['path'] for entry in inv['files']} == {entry['path'] for entry in manifest[filekey]} | set(excluded), 'whole names mismatch')
    return inv

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids = [], []
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])

def one_match(pattern, text):
    matches = re.findall(pattern, text, re.S)
    need(len(matches) == 1, 'unique expression missing: ' + pattern)
    return matches[0]

def plain(text):
    return ' '.join(unescape(re.sub('<[^>]*>', '', text)).split())

final_pin = pin(W / 'FINAL.json', 4834, '6d6e5fc828877744b4f48b1658a094a5b912b0e9d61ebe31d3353b1408a622df')
manifest_pin = pin(W / 'MANIFEST.json', 4076, 'b6ea05d5c4ddec612c16451b7f396e0af661e49fb84c7d5b7353b18741195e4d')
final, manifest = readj(W / 'FINAL.json'), readj(W / 'MANIFEST.json')
writer_inv = authenticate(W, manifest, 'payload_files', ['MANIFEST.json', 'FINAL.json'])
need((len(writer_inv['files']), len(writer_inv['directories'])) == (22, 1), 'writer extent mismatch')
need(sorted(final['extent']['all_paths']) == [entry['path'] for entry in writer_inv['files']], 'FINAL extent differs')
empty_streams = ['FINAL_CHECK.stderr.txt', 'FINAL_CHECK.stdout.txt', 'STATIC_CHECK.stderr.txt', 'STATIC_CHECK.stdout.txt']
need(all((W / name).read_bytes() == b'' for name in empty_streams), 'nonempty writer stream')
clear_path = P / 'verification/root-clearance-23527793-20261117.json'
clear_pin = pin(clear_path, 2092, '6fde779a24c6270f69429828a804784bb9f996c11683df47d7bd117ce0bb42c3')
clear = readj(clear_path)
for key in ['root_review', 'root_INITIAL', 'finite_evidence_adoption', 'native_flow_receipt']:
    entry = clear[key]
    pin(P / entry['path'], entry['bytes'], entry['SHA256'])
need(clear['status'] == 'PASS_FULL_ORIGINAL_PRIVATE_EDITORIAL_PREPARATION_ALLOWED' and clear['follow_up'] is None, 'clearance scope mismatch')
source_final_pin = pin(S / 'SOURCE_FINAL.json', 828, 'cc7d41efdfdb532269c7579192ff839893c1a6f5a719bcc6b2eb24673102486a')
source_manifest_pin = pin(S / 'SOURCE_MANIFEST.json', 44620, '5a28bd01fb98dd9d08f746fc4bef54bb19744a1c190db03c0ffb795630ee6d84')
source_final, source_manifest = readj(S / 'SOURCE_FINAL.json'), readj(S / 'SOURCE_MANIFEST.json')
source_inv = authenticate(S, source_manifest, 'files', ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'])
need((len(source_inv['files']), len(source_inv['directories'])) == (162, 23), 'source extent mismatch')
need(source_final['manifest']['SHA256'] == source_manifest_pin['SHA256'], 'source seal disagreement')
guards = readj(W / 'SOURCE_GUARDS.json')
need(normalized(source_inv['files']) == normalized(guards['files']), 'writer source guard files mismatch')
need(normalized(source_inv['directories']) == normalized(guards['directories']), 'writer source guard directories mismatch')
record, files_api = readj(S / 'record.response.body'), readj(S / 'files-23527793.response.body')
model = readj(W / 'page-model.json')
need(record['id'] == 23527793 and record['status'] == 'published', 'native record mismatch')
need([entry['key'] for entry in record['files']] == [entry['key'] for entry in files_api['entries']] == ['congestion-fragmentation-verification.zip', 'congestion-fragmentation.pdf'], 'native order mismatch')
need([entry['name'] for entry in model['native_asset_order']] == [entry['key'] for entry in record['files']], 'model order mismatch')
for native, api, asset in zip(record['files'], files_api['entries'], model['native_asset_order']):
    rel = 'assets/' + native['key']
    body = (S / rel).read_bytes()
    need(body == (W / rel).read_bytes(), 'native copy differs')
    need(native['size'] == api['size'] == asset['bytes'] == len(body), 'asset size differs')
    need(native['checksum'] == api['checksum'] == asset['native_checksum'] == 'md5:' + hashlib.md5(body).hexdigest(), 'asset MD5 differs')
    need(asset['SHA256'] == hashlib.sha256(body).hexdigest() and asset['local_path'] == rel, 'asset model differs')
    need(asset['native_url'] == native['links']['self'] == api['links']['content'], 'asset native URL differs')
article = (W / 'article.html').read_bytes().decode('utf-8')
head, main = (W / 'head.html').read_bytes().decode('utf-8'), (W / 'public-main.html').read_bytes().decode('utf-8')
need(one_match(r'(<head>.*?</head>\n)', article) == head, 'whole head differs')
need(one_match(r'(<main id="main">.*?</main>\n)', article) == main, 'whole MAIN differs')
tags = Tags(article)
need(len(tags.ids) == len(set(tags.ids)), 'duplicate HTML IDs')
metas = {attrs.get('name', attrs.get('property')): attrs.get('content') for tag, attrs in tags.tags if tag == 'meta'}
schema = json.loads(one_match(r'<script type="application/ld\+json">(.*?)</script>', article))
tex = (T / 'paper/main.tex').read_text(encoding='utf-8')
abstract = one_match(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex)
abstract = abstract.replace(r'\(k^2\)', 'k²').replace(r'\(16\sqrt{\log k/k}\)', '16√(log k/k)')
need('\\' not in abstract, 'unexpected TeX remains in abstract')
abstract = ' '.join(abstract.split())
need(abstract == model['abstract'] == schema['abstract'] == metas['DC.description'] == plain(one_match(r'<p id="abstract-text">(.*?)</p>', main)), 'full abstract differs')
need(model['title'] == record['metadata']['title'] == schema['name'] == metas['citation_title'], 'title differs')
need(model['doi'] == record['doi'] == schema['identifier']['value'] == metas['citation_doi'], 'DOI differs')
need(model['publication_date'] == record['metadata']['publication_date'] == schema['datePublished'] == '2026-10-21', 'date differs')
need(metas['citation_date'] == metas['citation_publication_date'] == '2026/10/21', 'citation date differs')
need(model['native_version'] == model['printed_version'] == record['metadata']['version'] == schema['version'] == metas['citation_version'] == '1.0', 'version differs')
need(model['author']['ORCID'] == schema['author']['identifier'] == 'https://orcid.org/' + record['metadata']['creators'][0]['orcid'] == 'https://orcid.org/' + metas['citation_author_orcid'], 'ORCID differs')
need(r'\date{21 October 2026\quad (version 1.0; unrefereed preprint)}' in tex, 'printed date/version differs')
need(plain((T / 'LICENSE.txt').read_text()) == model['rights']['actual_LICENSE_txt'], 'actual rights text differs')
need(record['metadata']['license']['id'] == model['rights']['native_metadata_license'] == 'cc-by-4.0', 'license differs')
need(schema['license'] == 'https://creativecommons.org/licenses/by/4.0/' and model['rights']['MIT_split_inferred'] is False, 'rights scope differs')
for obj in [model, final]:
    need(all(key in obj and obj[key] is None for key in ['actual_publication_date', 'canonical_url', 'base_url', 'production_url', 'AA', 'follow_up']), 'private null gate differs')
    need(obj['publication_authority'] is False, 'publication authority present')
need(metas['robots'] == metas['googlebot'] == model['robots'] == 'noindex, nofollow', 'robots differs')
need(not any(tag == 'link' and 'canonical' in attrs.get('rel', '').split() for tag, attrs in tags.tags), 'actual canonical present')
need('url' not in schema and 'mainEntityOfPage' not in schema, 'actual schema page URL present')
need(model['scientific_clearance']['inherited'] is True and model['scientific_clearance']['new_independent_scientific_review'] is False, 'review scope differs')
asset_list = one_match(r'<ol id="native-assets">(.*?)</ol>', main)
need(re.findall(r'<a href="(assets/[^\"]+)" download>', asset_list) == [asset['local_path'] for asset in model['native_asset_order']], 'visible asset order differs')
pdf = 'assets/congestion-fragmentation.pdf'
need(metas['citation_pdf_url'] == pdf, 'citation PDF path differs')
iframes = [attrs for tag, attrs in tags.tags if tag == 'iframe']
need(len(iframes) == 1 and iframes[0]['src'] == pdf + '#view=FitH' and bool(iframes[0].get('title')), 'iframe path/title differs')
anchors = [attrs for tag, attrs in tags.tags if tag == 'a']
need(any(attrs.get('href') == pdf and 'download' not in attrs for attrs in anchors), 'direct PDF open missing')
need(any(attrs.get('href') == pdf and 'download' in attrs for attrs in anchors), 'PDF download missing')
for tag, attrs in tags.tags:
    for key in ['href', 'src']:
        if key not in attrs:
            continue
        target = urlsplit(attrs[key])
        if target.scheme or target.netloc:
            continue
        if target.path:
            path = W / unquote(target.path)
            need(path.resolve().is_relative_to(W.resolve()) and path.is_file(), 'local path missing/escaping')
        elif target.fragment:
            need(target.fragment in tags.ids, 'fragment ID missing')
    for ident in attrs.get('aria-labelledby', '').split():
        need(ident in tags.ids, 'label ID missing')
bib = (W / 'citation.bib').read_text(encoding='utf-8')
need(all(text in bib for text in [model['title'], 'Kriebel, Alec', model['doi'], 'date = {2026-10-21}', 'version = {1.0}', 'CC BY 4.0', 'Unrefereed preprint']), 'Bib identity differs')
print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_DATA_ONLY_CUSTODY_AND_COPY_CONSISTENCY', 'scientific_clearance_inherited': True, 'new_scientific_verdict': False, 'render_or_live_certification': False, 'source_program_execution': False, 'writes_performed': [], 'pins': {'writer_final': final_pin, 'writer_manifest': manifest_pin, 'root_clearance': clear_pin, 'source_final': source_final_pin, 'source_manifest': source_manifest_pin}, 'writer_inventory': writer_inv, 'source_inventory': source_inv, 'full_abstract_equal': True, 'native_asset_order_and_bytes_MD5_exact': True, 'whole_head_MAIN_equal': True, 'private_null_noindex_gates_exact': True, 'local_PDF_paths_and_ids_exact': True, 'follow_up': None}, indent=2) + '\n', end='')
