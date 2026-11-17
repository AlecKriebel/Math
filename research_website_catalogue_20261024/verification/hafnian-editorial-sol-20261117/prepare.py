"""Own data-only article assembly and static checks; never executes source code."""
import hashlib
import html
import json
import os
import re
import shutil
import stat
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/hafnian-editorial-sol-20261117'
S = P / 'papers/23205294/sources'
T = S / 'published-source/container-001/tree'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
SLUG = 'nonnegative-rational-hafnians'

def need(ok, label):
    if not ok:
        raise ValueError(label)

def readj(path):
    return json.loads(path.read_bytes().decode('utf-8'))

def rec(path):
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode), 'Not a regular file: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'mode': oct(stat.S_IMODE(st.st_mode))}

def pin(path, size, digest):
    got = rec(path)
    need(got == {'bytes': size, 'SHA256': digest, 'mode': '0o644'}, 'Pin differs: ' + str(path))
    return got

def inv(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Not directory')
    files, dirs = {}, {}
    for path in sorted(root.rglob('*'), key=lambda item: item.relative_to(root).as_posix()):
        name = path.relative_to(root).as_posix()
        if stat.S_ISDIR(path.lstat().st_mode):
            dirs[name] = oct(stat.S_IMODE(path.lstat().st_mode))
        else:
            files[name] = rec(path)
    return {'root': str(root), 'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)), 'files': files, 'directories': dirs}

def guards():
    pins = {
        'clearance': pin(P / 'verification/root-clearance-23205294-20261117.json', 2183, '9926f66d5651c887b60e20ee689567459a21edc15f76b0b4ec390c69a624dbf7'),
        'root_review': pin(P / 'papers/23205294/reviews/root/ROOT_REVIEW.md', 13467, 'd41464f5a849fc70c5b21d52249c9924e06e091ef7339a1825736c7224f15114'),
        'source_final': pin(S / 'SOURCE_FINAL.json', 827, '09da60cf7a73285d2eccac7186d563f8f1e898c5bcc0390761a8a416989064d7'),
        'source_manifest': pin(S / 'SOURCE_MANIFEST.json', 11912, '340a82f34c9cb70a48e60c9bb7db4e1f8a0980e5ca037771c3fe7dc16c6677e7'),
        'shared_CSS': pin(W / 'research/research.css', 1170, 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a')}
    clearance = readj(P / 'verification/root-clearance-23205294-20261117.json')
    need(clearance['status'] == 'PASS_FULL_ORIGINAL_PRIVATE_EDITORIAL_PREPARATION_ALLOWED' and clearance['follow_up'] is None, 'Clearance scope differs')
    snapshot, manifest = inv(S), readj(S / 'SOURCE_MANIFEST.json')
    need(snapshot['root_mode'] == oct(manifest['root_mode']) == '0o755', 'Source root mode differs')
    need(set(manifest['exact_terminal_exclusions']) == {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}, 'Source exclusions differ')
    expected = {entry['path']: {'bytes': entry['bytes'], 'SHA256': entry['SHA256'], 'mode': oct(entry['mode'])} for entry in manifest['files']}
    need(len(expected) == len(manifest['files']), 'Duplicate source entry')
    need({key: value for key, value in snapshot['files'].items() if key not in manifest['exact_terminal_exclusions']} == expected, 'Source payload differs')
    need(snapshot['directories'] == {entry['path']: oct(entry['mode']) for entry in manifest['directories']}, 'Source directory boundary differs')
    need((len(snapshot['files']), len(snapshot['directories'])) == (56, 10), 'Source extent differs')
    need(not (W / 'research' / SLUG).exists(), 'Proposed slug collides')
    return {'pins': pins, 'source': snapshot, 'proposed_slug_absent': True}

def put(name, body):
    path = OWN / name
    need(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe output')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(body)
    os.chmod(path, 0o644)

def putj(name, value):
    put(name, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())

class Tags(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids = [], []
        self.feed(raw)
        self.close()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])

def only(pattern, raw):
    found = re.findall(pattern, raw, re.S)
    need(len(found) == 1, 'Expected unique expression')
    return found[0]

before = guards()
putj('SOURCE_GUARDS_BEFORE.json', before)
native = readj(S / 'record.response.body')
meta = native['metadata']
api = readj(S / 'files-23205294.response.body')
need(native['id'] == 23205294 and native['status'] == 'published', 'Native record differs')
need(meta['version'] == '1.0.0' and meta['publication_date'] == '2026-10-06' and meta['creators'][0]['orcid'] == '0009-0001-9320-500X', 'Native identity differs')
tex = (T / 'main.tex').read_bytes().decode('utf-8')
need(len(tex.splitlines()) == 165, 'Controlling manuscript extent differs')
abstract = only(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex)
abstract = abstract.replace('$W$', 'W').replace('$(W,1,0,0)$', '(W,1,0,0)').replace('$4\\bits(W)-2$', '4 bits(W)−2')
need('$' not in abstract and '\\' not in abstract, 'Unexpected abstract TeX')
abstract = ' '.join(abstract.split())
put('ABSTRACT.txt', (abstract + '\n').encode())
need([entry['key'] for entry in native['files']] == [entry['key'] for entry in api['entries']] == ['source-and-verification.zip', 'README.md', 'paper.pdf'], 'Native asset order differs')
assets = []
for item, api_item in zip(native['files'], api['entries']):
    source = S / 'assets' / item['key']
    body = source.read_bytes()
    need(len(body) == item['size'] == api_item['size'] and 'md5:' + hashlib.md5(body).hexdigest() == item['checksum'] == api_item['checksum'], 'Native asset differs')
    target = OWN / 'assets' / item['key']
    target.parent.mkdir(exist_ok=True)
    shutil.copy2(source, target)
    need(target.read_bytes() == body and rec(target) == rec(source), 'Copied asset differs')
    assets.append({'name': item['key'], 'local_path': 'assets/' + item['key'], **rec(source), 'native_checksum': item['checksum'], 'format': api_item['mimetype'], 'native_url': item['links']['self']})
title = meta['title']
seo = 'Nonnegative rational hafnians and perfect matchings | Alec Kriebel'
description = 'An attributed exact reduction of binary rational hafnians to unweighted perfect matchings, with polynomial bit bounds and quantitative approximate sampling.'
proposal = 'https://aleckriebel.com/research/' + SLUG + '/'
model = {
    'schema': 'private-editorial-page-model-v1', 'record_id': '23205294', 'sheet_row': 186, 'title': title, 'seo_title': seo, 'meta_description': description,
    'author': {'name': 'Alec Kriebel', 'ORCID': 'https://orcid.org/0009-0001-9320-500X'}, 'doi': native['doi'], 'doi_url': native['doi_url'], 'zenodo_record': native['links']['self_html'],
    'native_version': meta['version'], 'printed_version': None, 'printed_date': 'October 6, 2026', 'publication_date': meta['publication_date'], 'record_created': native['created'], 'record_updated': native['updated'],
    'status': 'Unrefereed, AI-assisted preprint', 'abstract': abstract, 'abstract_source': 'Complete native 165-line main.tex abstract; only whitespace and declared W/signature/4 bits(W)−2 TeX-to-Unicode rendering',
    'native_Description_source': 'papers/23205294/sources/record.response.body metadata.description; preserved native object, not substituted for manuscript abstract',
    'canonical_url': None, 'base_url': None, 'production_url': None, 'actual_publication_date': None, 'AA': None, 'publication_authority': False, 'robots': 'noindex, nofollow',
    'deployment_proposal': {'slug': SLUG, 'path': '/research/' + SLUG + '/', 'proposed_canonical_url': proposal, 'current_public_page_created': False, 'passive_slug_collision_check_absent': True, 'future_payloads': ['index.html', 'citation.bib'] + [item['local_path'] for item in assets], 'shared_stylesheet': '/research/research.css', 'requires_separate_root_adoption_staging_publication_and_live_verification': True},
    'native_asset_order': assets, 'pdf_pages': 6, 'citation_bib': 'citation.bib',
    'rights': {'native_metadata_license': 'cc-by-4.0', 'newly_authored_prose_proofs_explanatory_documents_and_data': 'CC BY 4.0', 'newly_authored_Python': 'MIT', 'actual_archive_statements': ['LICENSES.md', 'LICENSE_CODE.txt'], 'third_party': 'Cited works retain their authorship and rights'},
    'scientific_scope': {'input': 'Explicit symmetric 2m-by-2m matrix, nonnegative binary rational off-diagonal entries; ignore diagonal/delete zero edges; input length includes rational parameter encodings',
        'signature': '(#PM(H_W),#PM(H_W-{u,v}),#PM(H_W-u),#PM(H_W-v))=(W,1,0,0); ell=bits(W), 4ell-2 vertices, 4ell-4 internal, at most6ell-5 edges',
        'exact_reduction': 'D=product positive-entry denominators; W_e=p_e(D/q_e); #PM(H)=D^m haf(A); each M has D^m product A_e lifts',
        'bit_bounds': 'O(L²) vertices and edges; O(L² log(L+2)) explicit graph encoding; scale D^m has O(mL+1) bits; polynomial-bit construction',
        'approximation': 'Using pinned OpenAI Theorem1.1 and Edmonds, relative epsilon/failure delta for rational0<epsilon,delta<1; every-execution time polynomial in full input,epsilon^-1,log(delta^-1); zero iff hafnian zero on every tape; positive input failed-zero replacement before scaling',
        'sampling': 'Expanded N=2s>=2,C=s²,alpha=eta/(4s),gamma=eta/(4C),b=ceil(log2(4C/eta)); <=C counter calls,<=C+1 feasibility/witness calls,<=sb additional categorical fair bits; counter randomness additional',
        'sampling_bounds': 'Counting budget C T(Bprime,4s/eta,log(4C/eta)) plus polynomial witness/arithmetic; TV<=s alpha/(1-alpha)+C gamma+C 2^-b<=5eta/6<eta unconditionally; weighted law product A_e/haf(A); output always feasible',
        'boundary': 'Empty hafnian1/empty matching; exact infeasibility; disconnected support, weights<1, large denominators, arbitrarily small positive values; no density/connectivity/positive-weight lower bound',
        'limits': 'No signed/complex/unrestricted GBS, exact or pointwise-relative sampler, polynomial-in-log(eta^-1), practical upstream FPRAS implementation/benchmark, new weight-removal or complexity classification, formal verification or independent415-module audit'},
    'attribution': ['McQuillan2013 Section7.2 Lemmas25–27 binary rational equivalence', 'Dell–Husfeldt–Wahlen2010/expanded2014 binary gadgets', 'Jerrum–Valiant–Vazirani1986 classical count-to-sample', 'Edmonds1965 feasibility/witnesses', 'OpenAI Theorem1.1 exact commit adc7f1241b42e322a6451854ab7e4b4c146bf78a'],
    'framing': 'Attributed consequence/exposition/implementation; inherited approximation breakthrough, logarithmic weight removal and count-to-sample machinery; no first-publication claim',
    'AI_disclosure': 'Extensive research/drafting/implementation/automated adversarial verification; unrefereed; automated reviews are not conventional human peer review',
    'collaboration': 'Passive invitation for substantive verification, exposition/implementation improvements or journal-version development; authorship based on actual contributions',
    'scientific_clearance': {'inherited': True, 'new_scientific_review': False, 'path': 'verification/root-clearance-23205294-20261117.json'}, 'follow_up': None, 'rendered_or_live_certificate': False}
putj('page-model.json', model)
scholarly = {'@context': 'https://schema.org', '@type': 'ScholarlyArticle', 'name': title, 'headline': title, 'description': description, 'abstract': abstract,
    'author': {'@type': 'Person', 'name': 'Alec Kriebel', 'identifier': model['author']['ORCID']}, 'datePublished': meta['publication_date'], 'dateCreated': native['created'], 'dateModified': native['updated'],
    'version': meta['version'], 'creativeWorkStatus': model['status'], 'inLanguage': 'en', 'isAccessibleForFree': True, 'identifier': {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': native['doi']}, 'sameAs': native['doi_url'], 'license': 'https://creativecommons.org/licenses/by/4.0/', 'keywords': meta['keywords'],
    'encoding': [{'@type': 'MediaObject', 'name': item['name'], 'contentUrl': item['local_path'], 'encodingFormat': item['format'], 'contentSize': str(item['bytes']) + ' bytes', 'sameAs': item['native_url']} for item in assets]}
head = '<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>' + html.escape(seo) + '</title>\n'
metas = [('description', description), ('author', 'Alec Kriebel'), ('robots', model['robots']), ('googlebot', model['robots']), ('citation_title', title), ('citation_author', 'Kriebel, Alec'), ('citation_author_orcid', '0009-0001-9320-500X'), ('citation_publication_date', '2026/10/06'), ('citation_date', '2026/10/06'), ('citation_version', meta['version']), ('citation_doi', native['doi']), ('citation_pdf_url', 'assets/paper.pdf'), ('citation_language', 'en'), ('DC.title', title), ('DC.creator', 'Alec Kriebel'), ('DC.date', meta['publication_date']), ('DC.description', abstract), ('DC.identifier', 'doi:' + native['doi']), ('DC.type', 'Text'), ('DC.language', 'en'), ('DC.rights', 'Newly authored prose/data CC BY 4.0; Python code MIT; third-party rights retained'), ('twitter:card', 'summary'), ('twitter:title', title), ('twitter:description', description)]
head += ''.join('<meta name="' + name + '" content="' + html.escape(value, quote=True) + '">\n' for name, value in metas)
head += ''.join('<meta property="' + name + '" content="' + html.escape(value, quote=True) + '">\n' for name, value in [('og:type', 'article'), ('og:title', title), ('og:description', description), ('og:site_name', 'Alec Kriebel'), ('article:published_time', meta['publication_date']), ('article:modified_time', native['updated'])])
head += '<link rel="stylesheet" href="/research/research.css">\n<script type="application/ld+json">' + json.dumps(scholarly, ensure_ascii=False) + '</script>\n</head>\n'
put('head.html', head.encode())
main = (OWN / 'main.html').read_bytes().decode('utf-8')
article = '<!doctype html>\n<html lang="en">\n' + head + '<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="https://aleckriebel.com/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="https://aleckriebel.com/">Home</a> · <a href="https://aleckriebel.com/research/">Research</a></nav></header>\n' + main + '<footer><p><a href="https://aleckriebel.com/research/">Research index</a> · <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></p></footer>\n</body>\n</html>\n'
put('article.html', article.encode())
need(only(r'(<head>.*?</head>\n)', article) == head and only(r'(<main id="main">.*?</main>\n)', article) == main, 'Whole assembly differs')
visible = only(r'<p id="abstract-text">(.*?)</p>', main)
need(html.unescape(visible) == abstract == scholarly['abstract'] == model['abstract'], 'Complete abstract differs')
tags = Tags(article)
need(len(tags.ids) == len(set(tags.ids)), 'Duplicate id')
actual_metas = {attrs.get('name', attrs.get('property')): attrs.get('content') for tag, attrs in tags.tags if tag == 'meta'}
need(actual_metas['DC.description'] == abstract and actual_metas['robots'] == actual_metas['googlebot'] == 'noindex, nofollow', 'Abstract/private metadata differs')
need(all(model[key] is None for key in ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up']) and model['publication_authority'] is False, 'Private actual gate differs')
need(not any(tag == 'link' and attrs.get('rel') == 'canonical' for tag, attrs in tags.tags) and 'url' not in scholarly and 'mainEntityOfPage' not in scholarly, 'Actual page canonical present')
need([item['contentUrl'] for item in scholarly['encoding']] == ['assets/source-and-verification.zip', 'assets/README.md', 'assets/paper.pdf'], 'Three native encodings differ')
need(re.findall(r'<a href="(assets/[^\"]+)" download>', only(r'<ol id="native-assets">(.*?)</ol>', main)) == [item['local_path'] for item in assets], 'Visible native order differs')
need(any(tag == 'iframe' and attrs.get('src') == 'assets/paper.pdf#view=FitH' for tag, attrs in tags.tags), 'Local iframe differs')
need(any(tag == 'a' and attrs.get('href') == 'assets/paper.pdf' and 'download' not in attrs for tag, attrs in tags.tags), 'Direct PDF open missing')
need(any(tag == 'a' and attrs.get('href') == 'assets/paper.pdf' and 'download' in attrs for tag, attrs in tags.tags), 'Direct PDF download missing')
for tag, attrs in tags.tags:
    for key in ['href', 'src']:
        if key not in attrs:
            continue
        target = urlsplit(attrs[key])
        if target.scheme or target.netloc:
            continue
        if target.path:
            if target.path.startswith('/'):
                need(target.path == '/research/research.css' and (W / target.path.lstrip('/')).is_file(), 'Unexpected site-root target')
            else:
                path = OWN / unquote(target.path)
                need(path.resolve().is_relative_to(OWN.resolve()) and path.is_file(), 'Missing/escaping local target')
        elif target.fragment:
            need(target.fragment in tags.ids, 'Missing local fragment')
    for ident in attrs.get('aria-labelledby', '').split():
        need(ident in tags.ids, 'Missing label id')
bib = (OWN / 'citation.bib').read_bytes().decode('utf-8')
need(all(value in bib for value in [title, native['doi'], 'date = {2026-10-06}', 'version = {1.0.0}', 'Kriebel, Alec', 'Unrefereed']), 'Bib identity differs')
after = guards()
need(after == before, 'Source/clearance/style/slug guards changed')
putj('SOURCE_GUARDS_AFTER.json', after)
putj('STATIC_CHECK.json', {'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_PRIVATE_DATA_ONLY_ASSEMBLY_AND_STATIC_CHECKS', 'complete_abstract_visible_DC_schema_model_equal': True, 'whole_head_MAIN_assembly_exact': True, 'source56files10dirs_and_root_pins_unchanged': True, 'all3_native_ZIP_README_PDF_names_bytes_MD5_SHA256_modes_and_encodings_exact': True, 'identity_date_version_ORCID_rights_private_gates_and_paths_checked': True, 'shared_white_Arial_stylesheet_exact': True, 'slug_passively_absent': True, 'scientific_clearance_inherited': True, 'new_scientific_or_archived_helper_execution': False, 'rendered_or_live_certificate': False, 'follow_up': None})
