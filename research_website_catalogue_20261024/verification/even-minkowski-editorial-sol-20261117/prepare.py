"""Own data-only editorial preparation; never executes/imports source programs."""
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
OWN = P / 'verification/even-minkowski-editorial-sol-20261117'
S = P / 'papers/23203081/sources'
T = S / 'archives/02-source-and-verification.zip.extracted'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
SLUG = 'even-minkowski-uniqueness'

def need(ok, label):
    if not ok:
        raise ValueError(label)

def readj(path):
    return json.loads(path.read_bytes().decode('utf-8'))

def rec(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Not regular: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'MD5': hashlib.md5(body).hexdigest(), 'mode': oct(stat.S_IMODE(info.st_mode))}

def pin(path, size, digest):
    value = rec(path)
    need(value['bytes'] == size and value['SHA256'] == digest and value['mode'] == '0o644', 'Input pin differs: ' + str(path))
    return value

def inv(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Not directory')
    files, dirs = {}, {}
    for path in sorted(root.rglob('*'), key=lambda item: item.relative_to(root).as_posix()):
        name = path.relative_to(root).as_posix()
        if stat.S_ISDIR(path.lstat().st_mode):
            dirs[name] = {'mode': oct(stat.S_IMODE(path.lstat().st_mode)), 'empty': not any(path.iterdir())}
        else:
            files[name] = rec(path)
    return {'root': str(root), 'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)), 'root_empty': not any(root.iterdir()), 'files': files, 'directories': dirs}

def guards():
    pins = {'clearance': pin(P / 'verification/root-clearance-23203081-20261117.json', 1977, '008042d4a6d50c8bd0bfdc979db9afeff5c808091aaa2c8be5b4ec25c9dd6ada'),
        'root_review': pin(P / 'papers/23203081/reviews/root-continuation-20261117/ROOT_REVIEW.md', 16412, '527f2415f022d84d4344175c3abaedb8057c8006b4f6a184830bdd2eebfce848'),
        'source_final': pin(S / 'SOURCE_FINAL.json', 1259, 'b5b65ecc9a2cc31bfec3a7e97236b92d8dfebe4a7c5c7ace1f875586dfab9de2'),
        'source_manifest': pin(S / 'SOURCE_MANIFEST.json', 17636, '8c5a0654a6439a632f286e60dcaec2897edba6d9f6e40eff796962da3da6b8a3'),
        'shared_CSS': pin(W / 'research/research.css', 1170, 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a')}
    clear = readj(P / 'verification/root-clearance-23203081-20261117.json')
    need(clear['verdict'] == 'PASS' and clear['unresolved_central_written_gap'] is None and clear['follow_up'] is None and clear['publication_authority'] is False, 'Clearance differs')
    snapshot, manifest = inv(S), readj(S / 'SOURCE_MANIFEST.json')
    need(set(manifest['excluded_control_files']) == {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}, 'Source exclusions differ')
    entries = manifest['entries']
    need(len({item['path'] for item in entries}) == len(entries), 'Duplicate source entry')
    expected_files = {item['path']: {'bytes': item['bytes'], 'SHA256': item['sha256'], 'MD5': item['md5'], 'mode': item['mode_octal']} for item in entries if item['kind'] == 'file'}
    expected_dirs = {item['path']: {'mode': item['mode_octal'], 'empty': item['empty']} for item in entries if item['kind'] == 'directory'}
    need({key: value for key, value in snapshot['files'].items() if key not in manifest['excluded_control_files']} == expected_files, 'Source files differ')
    need(snapshot['directories'] == {key: value for key, value in expected_dirs.items() if key != '.'} and {'mode': snapshot['root_mode'], 'empty': snapshot['root_empty']} == expected_dirs['.'], 'Source directory topology differs')
    need((len(snapshot['files']), len(snapshot['directories'])) == (51, 12), 'Source extent differs')
    need(not (W / 'research' / SLUG).exists(), 'Proposed slug collides')
    return {'pins': pins, 'source': snapshot, 'proposed_slug_absent': True}

def put(name, body):
    need(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe owned path')
    path = OWN / name
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
native = readj(S / 'native-metadata/record-api.json')
meta = native['metadata']
need(native['id'] == 23203081 and native['status'] == 'published' and 'version' not in meta, 'Native identity/version differs')
need(meta['publication_date'] == '2026-10-06' and meta['creators'][0]['orcid'] == '0009-0001-9320-500X', 'Native date/ORCID differs')
need(b'Version v1</span>' in (S / 'native-metadata/record-page.html').read_bytes(), 'Separate host edition absent')
tex = (T / 'main.tex').read_bytes().decode('utf-8')
need(len(tex.splitlines()) == 183, 'Controlling TeX extent differs')
abstract = only(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex)
render = {'$n\\ge2$': 'n ≥ 2', '$0\\le p<1$': '0 ≤ p < 1', '$S^{n-1}$': 'Sⁿ⁻¹', '$h^{1-p}\\det(\\nabla^2h+hI)=f$': 'h¹⁻ᵖ det(∇²h+hI)=f', '$0<p<1$': '0 < p < 1', '$L_p$': 'Lₚ', '$p=0$': 'p=0'}
for original, rendered in render.items():
    abstract = abstract.replace(original, rendered)
abstract = ' '.join(abstract.replace('--', '–').split())
need('$' not in abstract and '\\' not in abstract, 'Unexpected abstract TeX')
put('ABSTRACT.txt', (abstract + '\n').encode())
need([item['key'] for item in native['files']] == ['paper.pdf', 'source-and-verification.zip', 'README.md'], 'Native asset order differs')
assets = []
formats = {'paper.pdf': 'application/pdf', 'source-and-verification.zip': 'application/zip', 'README.md': 'text/markdown'}
for item in native['files']:
    source = S / 'zenodo-files' / item['key']
    value = rec(source)
    need(value['bytes'] == item['size'] and 'md5:' + value['MD5'] == item['checksum'], 'Native asset identity differs')
    target = OWN / 'assets' / item['key']
    target.parent.mkdir(exist_ok=True)
    shutil.copy2(source, target)
    need(rec(target) == value, 'Copied original differs')
    assets.append({'name': item['key'], 'local_path': 'assets/' + item['key'], **value, 'native_checksum': item['checksum'], 'format': formats[item['key']], 'native_url': item['links']['self']})
title = meta['title']
seo = 'Even Minkowski uniqueness and logarithmic Brunn–Minkowski | Alec Kriebel'
description = 'Two distinct uniqueness consequences: smooth positive even data for 0≤p<1, and arbitrary origin-symmetric bodies with equal unnormalized Lp measures for 0<p<1.'
model = {'schema': 'private-editorial-page-model-v1', 'record_id': '23203081', 'sheet_row': 189, 'title': title, 'seo_title': seo, 'meta_description': description,
    'author': {'name': 'Alec Kriebel', 'ORCID': 'https://orcid.org/0009-0001-9320-500X'}, 'doi': native['doi'], 'doi_url': native['doi_url'], 'zenodo_record': native['links']['self_html'],
    'native_version': None, 'native_API_version_field_absent': True, 'native_HTML_display_version': 'v1', 'host_edition_qualification': 'Zenodo display edition only; not an author-supplied API version', 'printed_version': None, 'printed_date': 'October 6, 2026', 'publication_date': meta['publication_date'], 'record_created': native['created'], 'record_updated': native['updated'], 'status': 'Unrefereed, AI-assisted preprint',
    'abstract': abstract, 'abstract_source': 'Complete native183-line main.tex abstract; declared math/TeX dash rendering and whitespace normalization only', 'abstract_math_rendering': render, 'native_Description_source': 'papers/23203081/sources/native-metadata/record-api.json metadata.description; not substituted for manuscript abstract',
    'canonical_url': None, 'base_url': None, 'production_url': None, 'actual_publication_date': None, 'AA': None, 'publication_authority': False, 'robots': 'noindex, nofollow',
    'deployment_proposal': {'slug': SLUG, 'path': '/research/' + SLUG + '/', 'proposed_canonical_url': 'https://aleckriebel.com/research/' + SLUG + '/', 'current_public_page_created': False, 'passive_slug_collision_check_absent': True, 'future_payloads': ['index.html', 'citation.bib'] + [item['local_path'] for item in assets], 'shared_stylesheet': '/research/research.css', 'requires_separate_root_adoption_staging_publication_and_live_verification': True},
    'native_asset_order': assets, 'pdf_pages': 5, 'citation_bib': 'citation.bib', 'rights': {'owned_contribution': 'CC BY 4.0', 'third_party': 'Cited third-party works retain their own rights', 'source_rights_statement': 'Native publication README and archive README; no invented code-license split'},
    'scientific_scope': {'dimension': 'Ambient n>=2; spherical tangent dimension n-1',
        'smooth_claim': 'Every real0<=p<1 and every f in C∞(S^(n-1)) strictlypositive/even has exactly one positiveeven smooth support h satisfying h^(1-p)detQ(h)=f,Q=∇²h+hI>0',
        'general_body_claim': 'ONLY0<p<1: arbitrary full-dimensional origin-symmetric convex K,L, equal UNNORMALIZED S_K,p=S_L,p implies K=L; no smoothness required',
        'normalization': 'dS_K,p=h_K^(1-p)dS_K; unnormalized round dω; no volume-one or division by volume/total mass; dilation c^(n-p), evenness fixes center; atp0 nV=integral f',
        'positive_p_route': 'Nonsmooth Wulff variation/log-Minkowski; Jensen strictness only S_K-a.e.; ordinary first Minkowski equality upgrades to homothety; symmetry kills translation and equal measure fixes volumes/scale',
        'endpoint_route': 'w=log(h1/h0),q_t=h0exp(tw); local Q>0 by openness on compact sphere only near0; minimizer/volume argument then same PDE for small t>=0; right derivative identity -tr((Q^-1A)^2)-(n+1)w²+2hQ^-1(∇w,∇w)=0; both extrema imply w=0',
        'existence_regularity': 'BBCY symmetry-preserving existence with{±I}; origin interior/positive support; BBC global boundary/support-chart bridge; CW higher regularity; n2 direct ODE',
        'singular_p0_boundary': 'Equal-volume coordinate boxes B(1,...,1),B(s,s^-1,1,...),s>0,s!=1 have identical atomic S0 with each atom V/2; excluded from smooth strictlypositive density class',
        'limits': 'No degenerate/non-even/arbitrary nonadmissible functions; no arbitrary-measure p0 extension, volume-one normalization, new inequality/transfer/firstness/formal/human-review certificate'},
    'attribution': ['OpenAI logarithmic Brunn–Minkowski exactpin adc7f1241b42e322a6451854ab7e4b4c146bf78a', 'Böröczky–Lutwak–Yang–Zhang classical transfers', 'He–Liu v1 Theorem4/Section3 endpoint mechanism', 'Bianchi–Böröczky–Colesanti–Yang symmetry existence', 'Bianchi–Böröczky–Colesanti global regularity', 'Chou–Wang higher regularity', 'Stancu2018 earlier announcement credited in native manuscript'],
    'verification_wording': 'Finite exact-arithmetic checks support identities/boundaries, not universal proofs; no reproduced kernel/axiom/Comparator/follow-on formalization claim',
    'AI_disclosure': 'Extensive research/drafting/verification; unrefereed; automated reviews not conventional human peer review', 'collaboration': 'Passive substantive variation/endpoint/existence-regularity verification, exposition or journal-version work; authorship based on actual contributions',
    'scientific_clearance': {'inherited': True, 'new_scientific_review': False, 'path': 'verification/root-clearance-23203081-20261117.json'}, 'follow_up': None, 'rendered_or_live_certificate': False}
putj('page-model.json', model)
schema = {'@context': 'https://schema.org', '@type': 'ScholarlyArticle', 'name': title, 'headline': title, 'description': description, 'abstract': abstract,
    'author': {'@type': 'Person', 'name': 'Alec Kriebel', 'identifier': model['author']['ORCID']}, 'datePublished': meta['publication_date'], 'dateCreated': native['created'], 'dateModified': native['updated'], 'creativeWorkStatus': model['status'], 'inLanguage': 'en', 'isAccessibleForFree': True, 'identifier': {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': native['doi']}, 'sameAs': native['doi_url'], 'license': 'https://creativecommons.org/licenses/by/4.0/', 'keywords': meta['keywords'],
    'encoding': [{'@type': 'MediaObject', 'name': item['name'], 'contentUrl': item['local_path'], 'encodingFormat': item['format'], 'contentSize': str(item['bytes']) + ' bytes', 'sameAs': item['native_url']} for item in assets]}
head = '<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>' + html.escape(seo) + '</title>\n'
metas = [('description', description), ('author', 'Alec Kriebel'), ('robots', model['robots']), ('googlebot', model['robots']), ('citation_title', title), ('citation_author', 'Kriebel, Alec'), ('citation_author_orcid', '0009-0001-9320-500X'), ('citation_publication_date', '2026/10/06'), ('citation_date', '2026/10/06'), ('citation_doi', native['doi']), ('citation_pdf_url', 'assets/paper.pdf'), ('citation_language', 'en'), ('DC.title', title), ('DC.creator', 'Alec Kriebel'), ('DC.date', meta['publication_date']), ('DC.description', abstract), ('DC.identifier', 'doi:' + native['doi']), ('DC.type', 'Text'), ('DC.language', 'en'), ('DC.rights', 'Owned contribution CC BY 4.0; cited third-party rights retained'), ('twitter:card', 'summary'), ('twitter:title', title), ('twitter:description', description)]
head += ''.join('<meta name="' + name + '" content="' + html.escape(value, quote=True) + '">\n' for name, value in metas)
head += ''.join('<meta property="' + name + '" content="' + html.escape(value, quote=True) + '">\n' for name, value in [('og:type', 'article'), ('og:title', title), ('og:description', description), ('og:site_name', 'Alec Kriebel'), ('article:published_time', meta['publication_date']), ('article:modified_time', native['updated'])])
head += '<link rel="stylesheet" href="/research/research.css">\n<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>\n</head>\n'
put('head.html', head.encode())
main = (OWN / 'main.html').read_bytes().decode('utf-8')
article = '<!doctype html>\n<html lang="en">\n' + head + '<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="https://aleckriebel.com/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="https://aleckriebel.com/">Home</a> · <a href="https://aleckriebel.com/research/">Research</a></nav></header>\n' + main + '<footer><p><a href="https://aleckriebel.com/research/">Research index</a> · <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></p></footer>\n</body>\n</html>\n'
put('article.html', article.encode())
need(only(r'(<head>.*?</head>\n)', article) == head and only(r'(<main id="main">.*?</main>\n)', article) == main, 'Whole assembly differs')
need(html.unescape(only(r'<p id="abstract-text">(.*?)</p>', main)) == abstract == schema['abstract'] == model['abstract'], 'Complete original abstract differs')
tags = Tags(article)
need(len(tags.ids) == len(set(tags.ids)), 'Duplicate identifier')
actual_metas = {attrs.get('name', attrs.get('property')): attrs.get('content') for tag, attrs in tags.tags if tag == 'meta'}
need(actual_metas['DC.description'] == abstract and actual_metas['robots'] == actual_metas['googlebot'] == 'noindex, nofollow', 'Abstract/private head differs')
need('version' not in schema and 'citation_version' not in actual_metas and 'version =' not in (OWN / 'citation.bib').read_text(), 'Author API version invented')
need(all(model[key] is None for key in ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up']) and model['publication_authority'] is False, 'Private actual gate differs')
need(not any(tag == 'link' and attrs.get('rel') == 'canonical' for tag, attrs in tags.tags) and 'url' not in schema and 'mainEntityOfPage' not in schema, 'Actual canonical present')
need([item['contentUrl'] for item in schema['encoding']] == ['assets/paper.pdf', 'assets/source-and-verification.zip', 'assets/README.md'], 'Native3 encodings differ')
need(re.findall(r'<a href="(assets/[^\"]+)" download>', only(r'<ol id="native-assets">(.*?)</ol>', main)) == [item['local_path'] for item in assets], 'Visible native order differs')
need(any(tag == 'iframe' and attrs.get('src') == 'assets/paper.pdf#view=FitH' for tag, attrs in tags.tags), 'Local PDF iframe differs')
need(any(tag == 'a' and attrs.get('href') == 'assets/paper.pdf' and 'download' not in attrs for tag, attrs in tags.tags), 'PDF direct open missing')
need(any(tag == 'a' and attrs.get('href') == 'assets/paper.pdf' and 'download' in attrs for tag, attrs in tags.tags), 'PDF download missing')
need('MIT' not in main + head and 'Apache' not in main + head and 'CC BY 4.0' in main, 'Invented license split')
for tag, attrs in tags.tags:
    for key in ['href', 'src']:
        if key not in attrs:
            continue
        url = urlsplit(attrs[key])
        if url.scheme or url.netloc:
            continue
        if url.path.startswith('/'):
            need(url.path == '/research/research.css' and (W / url.path.lstrip('/')).is_file(), 'Unexpected root path')
        elif url.path:
            path = OWN / unquote(url.path)
            need(path.resolve().is_relative_to(OWN.resolve()) and path.is_file(), 'Local path missing/escaping')
        elif url.fragment:
            need(url.fragment in tags.ids, 'Local fragment missing')
    for ident in attrs.get('aria-labelledby', '').split():
        need(ident in tags.ids, 'Label id missing')
bib = (OWN / 'citation.bib').read_bytes().decode('utf-8')
need(all(value in bib for value in [title, native['doi'], 'date = {2026-10-06}', 'Kriebel, Alec', 'Zenodo displays edition v1']) and '1.0.0' not in article + bib, 'Citation identity/host edition differs')
after = guards()
need(before == after, 'Source/root/CSS/slug guard drift')
putj('SOURCE_GUARDS_AFTER.json', after)
putj('STATIC_CHECK.json', {'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_PRIVATE_DATA_ONLY_ASSEMBLY_AND_STATIC_CHECKS', 'whole_head_MAIN_exact': True, 'full_abstract_visible_DC_schema_model_exact': True, 'native51files12dirs_rootpins_unchanged': True, 'PDF_ZIP_README_names_bytes_MD5_SHA256_modes_and3encodings_exact': True, 'API_version_absent_host_v1_qualified_no_invented_author_version': True, 'owned_CCBY4_thirdparty_rights_no_invented_license_split': True, 'private_noindex_null_actual_canonical_publication_AA_followup': True, 'local_links_ids_Bib_shared_CSS_checked': True, 'scientific_clearance_inherited': True, 'native_scientific_execution_import_AST_compiler_or_test': False, 'new_formal_human_priority_certificate': False, 'current_render_or_live_certificate': False})
