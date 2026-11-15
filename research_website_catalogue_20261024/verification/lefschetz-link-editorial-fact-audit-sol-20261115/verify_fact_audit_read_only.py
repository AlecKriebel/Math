"""Own pure offline editorial custody checker. No project imports, writes or science."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import zipfile
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
CAT = ROOT.parent.parent
IDS = ('23570763', '23331295')
PINS = {
    '23570763': ('f9a6c973d657449db4087605189e0ac4a655a246fbf012b9c05a7dc60566187e',
                 '56a6e20fcef53e11e3cd7ab2bba1ad6503d0720509983be7b60d5a19bd9dc33f'),
    '23331295': ('307ac0b4005de084926d2a99ecd309854e544957f03a5c7620d999475c218d4d',
                 'a4dbd16bc3bd3bb81b674183f3c75f87d1234b5a0facb89320bb8f08a3b5ed25'),
}
checks = 0
wrappers = 0

def need(ok, what):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError(what)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def J(path):
    return json.loads(Path(path).read_text())

def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b

def point(obj, ptr):
    if not ptr:
        return obj
    for key in ptr.lstrip('/').split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    return obj

def namespace(root):
    need(root.is_dir() and not root.is_symlink() and root.resolve() == root,
         'namespace root must be a real directory without symlink ancestors: ' + str(root))
    files, dirs = [], []
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'symlink in namespace: ' + str(p))
        if p.is_file():
            files.append(p.relative_to(root).as_posix())
        elif p.is_dir():
            dirs.append(p.relative_to(root).as_posix())
        else:
            raise RuntimeError('nonregular namespace entry: ' + str(p))
    return sorted(files), sorted(dirs)

def guard_pin(p, n, h):
    body = p.read_bytes()
    need(len(body) == n, 'byte length: ' + str(p))
    need(sha(body) == h, 'hash: ' + str(p))
    return body

def embedded(obj, editorial):
    global wrappers
    if isinstance(obj, dict):
        if 'path' in obj and isinstance(obj['path'], str) and obj['path'].startswith('/'):
            if 'whole_literal_object' in obj or 'whole_literal_text' in obj or 'whole_actual_text' in obj:
                path = Path(obj['path'])
                body = guard_pin(path, obj['bytes'], obj['SHA256'])
                for key in ('whole_literal_object', 'whole_literal_text', 'whole_actual_text'):
                    if key in obj:
                        val = J(path) if key == 'whole_literal_object' else body.decode()
                        need(same(obj[key], val), 'whole literal mismatch: ' + str(path))
                        wrappers += 1
                if 'raw_blob' in obj:
                    need((editorial / obj['raw_blob']).read_bytes() == body, 'raw blob mismatch')
        for value in obj.values():
            embedded(value, editorial)
    elif isinstance(obj, list):
        for value in obj:
            embedded(value, editorial)

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.meta = {}
        self.ld = []
        self.in_ld = False
        self.abstract = False
        self.abstract_text = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.tags.append((tag, d))
        if tag == 'meta' and 'name' in d:
            self.meta[d['name']] = d.get('content')
        if tag == 'script' and d.get('type') == 'application/ld+json':
            self.in_ld = True
        if tag == 'section' and d.get('id') == 'abstract':
            self.abstract = True
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_ld = False
        if tag == 'section':
            self.abstract = False
    def handle_data(self, data):
        if self.in_ld:
            self.ld.append(data)
        if self.abstract:
            self.abstract_text.append(data)

def main():
    manifest = J(ROOT / 'INPUT_MANIFEST.json')
    for row in manifest['files']:
        p = Path(row['path'])
        need(not p.is_symlink(), 'input symlink')
        body = guard_pin(p, row['bytes'], row['SHA256'])
        need((ROOT / row['copy']).read_bytes() == body, 'literal input copy mismatch')
    ns_counts = []
    for row in manifest['strict_namespaces']:
        fs, ds = namespace(Path(row['root']))
        need(fs == sorted(row['exact_relative_file_names']), 'strict file namespace changed')
        need(ds == row['exact_relative_directory_names'], 'strict directory namespace changed')
        ns_counts.append(len(fs))
    comp = J(ROOT / 'WHOLE_TYPED_COMPARISONS.json')['comparisons']
    for row in comp:
        a = point(J(row['input_path']), row['JSON_pointer'])
        b = point(J(row['reference_path']), row['reference_JSON_pointer'])
        need(same(a, b), 'typed/key/list/null/history comparison mismatch')
    payload_counts, original_assets = [], 0
    for ident in IDS:
        paper = CAT / 'papers' / ident
        e, s = paper / 'reviews/editorial', paper / 'sources'
        need(sha((e / 'SEAL.json').read_bytes()) == PINS[ident][0], 'editorial seal pin')
        a_path = CAT / 'verification' / ('root-clearance-' + ident + '-20261115.json')
        need(sha(a_path.read_bytes()) == PINS[ident][1], 'root authority pin')
        seal, m = J(e / 'SEAL.json'), J(e / 'MANIFEST.json')
        need(sha((e / 'MANIFEST.json').read_bytes()) == seal['MANIFEST_SHA256'], 'owner manifest seal')
        for row in m['files']:
            guard_pin(e / row['path'], row['bytes'], row['SHA256'])
        exact_terminals = {'MANIFEST.json', 'SEAL.json'}
        if ident == '23331295':
            exact_terminals |= {'CLOSURE_NORMAL.stderr', 'CLOSURE_NORMAL.stdout.json',
                                'CLOSURE_OPTIMIZED.stderr', 'CLOSURE_OPTIMIZED.stdout.json',
                                'CLOSURE_RECEIPT.json'}
            for row in seal['terminal_payload_receipts']:
                guard_pin(e / row['path'], row['bytes'], row['SHA256'])
        fs, _ = namespace(e)
        need(set(fs) == {r['path'] for r in m['files']} | exact_terminals,
             'sealed owner namespace; only exact root-relative terminal names excepted')
        pub_path = e / ('config/publication.json' if ident == '23570763' else 'publication.json')
        pro_path = e / ('config/promotion.json' if ident == '23570763' else 'promotion.json')
        pub, pro, ready, native = J(pub_path), J(pro_path), J(s / 'SOURCE_READY.json'), J(s / 'record.response.body')
        for p in (pub_path, pro_path, e / 'SCHEMA_ADAPTER.json', e / 'SOURCE_PROTOCOL_BINDINGS.json', e / 'RIGHTS_AND_IDENTITY.json'):
            embedded(J(p), e)
        for key in ('canonical_url', 'AA', 'native_sheet_aa_url', 'follow_up'):
            need(pub[key] is None and pro[key] is None, 'unassigned publication/AA/followup')
        for key in ('ready_to_publish', 'deployed', 'live_verified', 'browser_verified', 'native_verified',
                    'native_sheet_publication_verified', 'canonical_verified', 'public_page_published', 'production_integration_authorized'):
            need(pro[key] is False, 'future publication gate incorrectly positive')
        for key, nk in (('title', 'title'), ('doi', 'doi'), ('version', 'version'), ('publication_date', 'publication_date')):
            need(same(pub[key], native['metadata'][nk]), 'native metadata identity')
        need(pub['orcid'].endswith(native['metadata']['creators'][0]['orcid']), 'ORCID identity')
        need(not (paper / 'publication.json').exists() and not (paper / 'promotion.json').exists(), 'paper configs created')
        need((s / 'record.response.body').read_bytes() == (s / 'latest.response.body.redirect-01').read_bytes(), 'whole latest record bytes')
        versions = J(s / 'versions-page001.response.body')
        need(len(versions['hits']['hits']) == 1, 'exact single enumerated version')
        hit = versions['hits']['hits'][0]
        expect = dict(native)
        expect['swh'] = None
        need(same(hit, expect), 'versions full native object and swh distinction')
        need(versions['hits']['total'] == 1 and 'next' not in versions['links'], 'exhaustive version enumeration')
        files = J(s / 'files.response.body')
        need(files['order'] == [] and files['default_preview'] is None, 'native files null/empty states')
        expected_assets = 2 if ident == '23570763' else 3
        need(len(ready['all_native_assets_in_original_order']) == len(files['entries']) == len(native['files']) == expected_assets,
             'complete equal-length native asset lists')
        for asset, entry, api in zip(ready['all_native_assets_in_original_order'], files['entries'], native['files']):
            need(same(asset['original_api_file_object'], api), 'native original API asset object')
            need(same(asset['whole_original_native_files_entry'], entry), 'native whole files entry')
            src = Path(asset['path']).read_bytes()
            need((e / 'candidate/assets' / api['key']).read_bytes() == src, 'unchanged whole native candidate asset')
            need(hashlib.md5(src).hexdigest() == api['checksum'].split(':')[1], 'native MD5')
            original_assets += 1
            if api['key'].endswith('.zip'):
                with zipfile.ZipFile(Path(asset['path'])) as z:
                    infos = [i for i in z.infolist() if not i.is_dir()]
                    need(len(infos) == (18 if ident == '23570763' else 15), 'whole ZIP regular payload count')
                    for i in infos:
                        need(not PurePosixPath(i.filename).is_absolute() and '..' not in PurePosixPath(i.filename).parts, 'archive member path safety')
                        root = s / ('published-source/asset-001' if ident == '23570763' else 'published-source/asset-002')
                        need(z.read(i) == (root / i.filename).read_bytes(), 'whole ZIP payload bytes/CRC')
                    pdfs = [i for i in infos if i.filename.endswith('.pdf')]
                    need(len(pdfs) == (1 if ident == '23570763' else 0), 'embedded PDF presence')
                    if pdfs:
                        need(z.read(pdfs[0]) == Path(ready['selected_actual_PDF']['path']).read_bytes(), 'embedded PDF whole identity')
                    payload_counts.append(len(infos))
        tex = Path(ready['controlling_TeX']['extracted_path']).read_text()
        raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)
        need(raw == (e / 'abstract-source.tex').read_text(), 'whole actual TeX abstract block')
        abstract = raw
        if ident == '23570763':
            for before, after in [('$p$', 'p'), ('$n\\geq2$', 'n ≥ 2'), ('$p\\nmid n-1$', 'p ∤ n − 1'),
                                  ('$\\mathbb F_p(t)$', '𝔽ₚ(t)'), ('R\\"omer', 'Römer')]:
                abstract = abstract.replace(before, after)
        else:
            abstract = abstract.replace('\\(', '').replace('\\)', '').replace('~', ' ')
        abstract = ' '.join(abstract.split())
        need(abstract == pub['abstract'], 'complete abstract faithful transcription')
        need(pub['prepared_bibtex'] == (e / 'citation.bib').read_text(), 'whole configured BibTeX')
        need((e / 'citation.bib').read_bytes() == (e / 'candidate/assets/citation.bib').read_bytes(), 'candidate BibTeX identity')
        page = Page()
        html = (e / 'candidate/index.html').read_text()
        main_tree = re.search(r'(<main>.*?</main>)', html, re.S).group(1)
        need(main_tree == (e / 'PUBLIC_MAIN.html').read_text().strip(), 'entire sealed HTML main tree')
        page.feed(html)
        need(page.meta['robots'] == 'noindex,nofollow', 'private robots state')
        for mk, pk in (('citation_title', 'title'), ('citation_doi', 'doi'), ('citation_version', 'version'), ('citation_author', 'author')):
            need(page.meta[mk] == pub[pk], 'citation metadata fidelity')
        need(' '.join(page.abstract_text).split('Original abstract', 1)[-1].strip() == abstract, 'full visible HTML abstract')
        ld = json.loads(''.join(page.ld))
        article = next(q for q in ld['@graph'] if q['@type'] == 'ScholarlyArticle') if '@graph' in ld else ld
        need(article['abstract'] == abstract and article['datePublished'] == pub['publication_date'], 'whole scholarly abstract/date')
        need([q['contentUrl'] for q in article['encoding']] == [a['links']['self'] for a in native['files']], 'native encoding asset order')
        frames = [d for t, d in page.tags if t == 'iframe']
        need(len(frames) == 1 and frames[0]['src'].split('#')[0] == 'assets/' + pub['pdf_filename'], 'unchanged complete reader target')
        for tag, attrs in page.tags:
            link = attrs.get('href', '')
            if link.startswith('assets/'):
                need((e / 'candidate' / link).is_file(), 'candidate local linked asset')
        if ident == '23331295':
            need(pub['printed_version'] is None and pub['printed_version_field_present'] is False, 'printed version truly absent')
            need(pub['code_license'] is None, 'no invented separate code license')
            need(Path(ready['controlling_TeX']['extracted_path']).read_bytes() == (s / 'assets/nullstellensatz.tex').read_bytes(), 'native standalone TeX/control equality')
            root_auth = J(a_path)
            q = root_auth['additional_Stoimenow_root_vs_peer_qualification']
            update = pro['new_root_primary_access_update_separate_from_immutable_peer_limits']
            need(same(update['whole_original_root_qualification'], q), 'whole original new root2010 qualification')
            need(update['fresh_remote_GET_claimed'] is False and update['editorial_new_full_or_critical_primary_body_read_claimed'] is False,
                 'no invented editorial2010 reading or remote acquisition')
            guard_pin(Path(q['path']), 618917, '86b9466b99f2cf67656b49311e67b97267c807d6c0f99d746a874c74379ca508')
            need(q['root_actual_physical_pages_read'] == [1, 2, 7, 8, 10, 11] and q['root_reference63_entry_read'] is True,
                 'exact newly authenticated selected root2010 reading')
            need(q['whole46page_new_root_read_claimed'] is False, 'no new whole2010 reading certificate')
        else:
            need(pub['code_license'] == 'MIT', 'actual separate MIT instrument retained')
    own_closed = False
    if (ROOT / 'OWNED_MANIFEST.json').exists():
        own = J(ROOT / 'OWNED_MANIFEST.json')
        for row in own['files']:
            guard_pin(ROOT / row['path'], row['bytes'], row['SHA256'])
        files, _ = namespace(ROOT)
        need(set(files) == {r['path'] for r in own['files']} | {'OWNED_MANIFEST.json', 'SEAL.json'}, 'own exact sealed namespace')
        seal = J(ROOT / 'SEAL.json')
        need(sha((ROOT / 'OWNED_MANIFEST.json').read_bytes()) == seal['OWNED_MANIFEST_SHA256'], 'own final seal')
        own_closed = True
    print(json.dumps({'status': 'PASS_INFORMED_EDITORIAL_FACT_CUSTODY_ONLY', 'checks': checks,
                      'protected_original_files': len(manifest['files']), 'strict_namespace_file_counts': ns_counts,
                      'whole_recorded_typed_comparisons': len(comp), 'whole_embedded_wrapper_comparisons': wrappers,
                      'original_candidate_assets': original_assets, 'ZIP_regular_payloads': payload_counts,
                      'scientific_programs_executed': [], 'network': False, 'writes': False,
                      'browser_or_live_claim': False, 'own_final_seal_checked': own_closed}, indent=2))

if __name__ == '__main__':
    main()
