"""Own data-only editorial assembly; no source execution/import/AST/compiler/test."""
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
OWN = P / 'verification/complex-retract-editorial-sol-20261117'
S = P / 'papers/23203270/sources'
T = S / 'archives/01-source-and-verification.zip.extracted'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
SLUG = 'complex-polynomial-retract-five-variables'

def need(ok, label):
    if not ok:
        raise ValueError(label)

def readj(path):
    return json.loads(path.read_bytes().decode('utf-8'))

def rec(path):
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode), 'Not regular: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'MD5': hashlib.md5(body).hexdigest(), 'mode': oct(stat.S_IMODE(st.st_mode))}

def pin(path, size, digest):
    value = rec(path)
    need(value['bytes'] == size and value['SHA256'] == digest and value['mode'] == '0o644', 'Pin differs: ' + str(path))
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
    pins = {'clearance': pin(P / 'verification/root-clearance-23203270-20261117.json', 2486, '7b7096d4fcdf0260f849140e95a97c26e5a1fac8e999bd4d86bbe0b505a93774'),
        'root_review': pin(P / 'papers/23203270/reviews/root-continuation-20261117/ROOT_REVIEW.md', 13285, '3a8c154c15491194fc85df87faabe47a4ed65e2d644f4c02b6cf27749a093300'),
        'source_final': pin(S / 'SOURCE_FINAL.json', 1259, '2fec24204f44586d98bd88fbe26a1519e7b55b4abe221275475b1cbf2a7bc62e'),
        'source_manifest': pin(S / 'SOURCE_MANIFEST.json', 33336, '4d41d1b02c1f436a7a0fd8f6249515aa69eced4658527a1c56f3fec20c86a704'),
        'shared_CSS': pin(W / 'research/research.css', 1170, 'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a')}
    need(readj(P / 'verification/root-clearance-23203270-20261117.json')['status'] == 'PASS_FULL_ORIGINAL_PRIVATE_EDITORIAL_PREPARATION_ALLOWED', 'Clearance differs')
    snapshot, manifest = inv(S), readj(S / 'SOURCE_MANIFEST.json')
    need(set(manifest['excluded_control_files']) == {'SOURCE_FINAL.json', 'SOURCE_MANIFEST.json'}, 'Source exclusions differ')
    entries = manifest['entries']
    need(len({item['path'] for item in entries}) == len(entries), 'Duplicate source entry')
    expected_files = {item['path']: {'bytes': item['bytes'], 'SHA256': item['sha256'], 'MD5': item['md5'], 'mode': item['mode_octal']} for item in entries if item['kind'] == 'file'}
    expected_dirs = {item['path']: {'mode': item['mode_octal'], 'empty': item['empty']} for item in entries if item['kind'] == 'directory'}
    need({key: value for key, value in snapshot['files'].items() if key not in manifest['excluded_control_files']} == expected_files, 'Source file namespace differs')
    need(snapshot['directories'] == {key: value for key, value in expected_dirs.items() if key != '.'}, 'Source directory namespace differs')
    need({'mode': snapshot['root_mode'], 'empty': snapshot['root_empty']} == expected_dirs['.'], 'Source root differs')
    need((len(snapshot['files']), len(snapshot['directories'])) == (97, 12), 'Source extent differs')
    need(not (W / 'research' / SLUG).exists(), 'Proposed slug collides')
    return {'pins': pins, 'source': snapshot, 'proposed_slug_absent': True}

def put(name, body):
    need(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe owned path')
    target = OWN / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as handle:
        handle.write(body)
    os.chmod(target, 0o644)

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
need(native['id'] == 23203270 and native['status'] == 'published', 'Native record differs')
need('version' not in meta and meta['publication_date'] == '2026-10-06' and meta['creators'][0]['orcid'] == '0009-0001-9320-500X', 'Native identity/version differs')
need(b'Version v1</span>' in (S / 'native-metadata/record-page.html').read_bytes(), 'Separate host edition label absent')
tex = (T / 'main.tex').read_bytes().decode('utf-8')
need(len(tex.splitlines()) == 362, 'Controlling TeX extent differs')
abstract = ' '.join(only(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex).split())
need('\\' not in abstract and '$' not in abstract, 'Unexpected abstract TeX')
put('ABSTRACT.txt', (abstract + '\n').encode())
need([item['key'] for item in native['files']] == ['source-and-verification.zip', 'paper.pdf'], 'Native asset order differs')
assets = []
for item in native['files']:
    source = S / 'zenodo-files' / item['key']
    value = rec(source)
    need(value['bytes'] == item['size'] and 'md5:' + value['MD5'] == item['checksum'], 'Native asset identity differs')
    target = OWN / 'assets' / item['key']
    target.parent.mkdir(exist_ok=True)
    shutil.copy2(source, target)
    need(rec(target) == value, 'Copied native asset differs')
    assets.append({'name': item['key'], 'local_path': 'assets/' + item['key'], **value, 'native_checksum': item['checksum'], 'format': 'application/zip' if item['key'].endswith('.zip') else 'application/pdf', 'native_url': item['links']['self']})
title = meta['title']
seo = 'A complex polynomial retract in five variables | Alec Kriebel'
description = 'An explicit polynomial idempotent on complex affine five-space with a smooth fourfold image whose coordinate algebra is not a polynomial ring.'
model = {'schema': 'private-editorial-page-model-v1', 'record_id': '23203270', 'sheet_row': 188, 'title': title, 'seo_title': seo, 'meta_description': description,
    'author': {'name': 'Alec Kriebel', 'ORCID': 'https://orcid.org/0009-0001-9320-500X'}, 'doi': native['doi'], 'doi_url': native['doi_url'], 'zenodo_record': native['links']['self_html'],
    'native_version': None, 'native_API_version_field_absent': True, 'native_HTML_display_version': 'v1', 'host_edition_qualification': 'Zenodo display edition only; not an author-supplied API version', 'printed_version': None, 'printed_date': 'October 6, 2026', 'publication_date': meta['publication_date'], 'record_created': native['created'], 'record_updated': native['updated'], 'status': 'Unrefereed, AI-assisted preprint',
    'abstract': abstract, 'abstract_source': 'Complete native 362-line main.tex abstract; whitespace normalized only', 'native_Description_source': 'papers/23203270/sources/native-metadata/record-api.json metadata.description; not substituted for manuscript abstract',
    'canonical_url': None, 'base_url': None, 'production_url': None, 'actual_publication_date': None, 'AA': None, 'publication_authority': False, 'robots': 'noindex, nofollow',
    'deployment_proposal': {'slug': SLUG, 'path': '/research/' + SLUG + '/', 'proposed_canonical_url': 'https://aleckriebel.com/research/' + SLUG + '/', 'current_public_page_created': False, 'passive_slug_collision_check_absent': True, 'future_payloads': ['index.html', 'citation.bib'] + [item['local_path'] for item in assets], 'shared_stylesheet': '/research/research.css', 'requires_separate_root_adoption_staging_publication_and_live_verification': True},
    'native_asset_order': assets, 'pdf_pages': 6, 'citation_bib': 'citation.bib',
    'rights': {'original_note_and_original_verification_package': 'CC BY 4.0', 'bundled_OpenAI_Lean_and_adapted_configuration_audit_harness': 'Apache License 2.0 explicit exception', 'archive_statements': ['LICENSES.md', 'THIRD_PARTY_NOTICES.md'], 'third_party': 'Cited publications retain their own rights'},
    'scientific_scope': {'field': 'Full complex field; unital complex-algebra maps', 'algebra': 'P=C[p,s,u,F,J],x=s²+u³+p²F,H=x²F-(1+2sx)J-p²J²-pu,A=P/(H)',
        'result': 'A smooth integral complex algebra/transcendence degree4; explicit i:A->B=C[p,s,u,m,e],r:B->A,ri=id; i(A) not polynomial',
        'scheme_image': 'pi=Spec(i):A5->Spec(A),sigma=Spec(r) closed embedding,pi sigma=id;rho=sigma pi idempotent; scheme image sigma(Spec A), coordinate B/ker(r)=A',
        'factored_map': 'Manuscript Sections2–3 copied with explicit M-dependence f_M,j_M,C_M,Q_1,M; helper Q(L) written as2x0F²-2sFJ-J² after inverse coordinate substitution; each helper recomputes s,u factors',
        'global': 'All5 components polynomial, no coordinate denominators; p=0 formula W=-e-u kappa m,rho=(0,s,u,m+3u²W,-u kappa(m+3u²W)); kappa is bracket polynomial even at m=0',
        'limits': 'No linear/orthogonal/nearest-point/distance property, real-form or positive-characteristic theorem, ambient4 resolution, independent cancellation breakthrough, firstness or formal verification'},
    'attribution': ['OpenAI exact pinned cancellation theorem/example/stabilization/nonpolynomiality, adc7f1241b42e322a6451854ab7e4b4c146bf78a', 'Nagamine arXiv1811.04153v2 Proposition1.4 classical cylinder-to-retract mechanism', 'Costa1977 retract question'],
    'verification_wording': 'Written identities and split-map proof; archive contains symbolic scripts/regression examples; no fresh symbolic PASS or new55module scan or formal build asserted',
    'AI_disclosure': 'Extensive research/drafting/symbolic verification/adversarial audits; unrefereed; automated reviews not conventional human peer review', 'collaboration': 'Passive substantive polynomial/scheme verification, exposition improvements or journal-version development; authorship based on actual contributions', 'scientific_clearance': {'inherited': True, 'new_scientific_review': False, 'path': 'verification/root-clearance-23203270-20261117.json'}, 'follow_up': None, 'rendered_or_live_certificate': False}
putj('page-model.json', model)
scholarly = {'@context': 'https://schema.org', '@type': 'ScholarlyArticle', 'name': title, 'headline': title, 'description': description, 'abstract': abstract,
    'author': {'@type': 'Person', 'name': 'Alec Kriebel', 'identifier': model['author']['ORCID']}, 'datePublished': meta['publication_date'], 'dateCreated': native['created'], 'dateModified': native['updated'], 'creativeWorkStatus': model['status'], 'inLanguage': 'en', 'isAccessibleForFree': True, 'identifier': {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': native['doi']}, 'sameAs': native['doi_url'], 'license': 'https://creativecommons.org/licenses/by/4.0/', 'keywords': meta['keywords'],
    'encoding': [{'@type': 'MediaObject', 'name': item['name'], 'contentUrl': item['local_path'], 'encodingFormat': item['format'], 'contentSize': str(item['bytes']) + ' bytes', 'sameAs': item['native_url']} for item in assets]}
head = '<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>' + html.escape(seo) + '</title>\n'
metas = [('description', description), ('author', 'Alec Kriebel'), ('robots', model['robots']), ('googlebot', model['robots']), ('citation_title', title), ('citation_author', 'Kriebel, Alec'), ('citation_author_orcid', '0009-0001-9320-500X'), ('citation_publication_date', '2026/10/06'), ('citation_date', '2026/10/06'), ('citation_doi', native['doi']), ('citation_pdf_url', 'assets/paper.pdf'), ('citation_language', 'en'), ('DC.title', title), ('DC.creator', 'Alec Kriebel'), ('DC.date', meta['publication_date']), ('DC.description', abstract), ('DC.identifier', 'doi:' + native['doi']), ('DC.type', 'Text'), ('DC.language', 'en'), ('DC.rights', 'Original note/verification CC BY 4.0; bundled OpenAI Lean/adapted configuration/harness Apache 2.0; third-party rights retained'), ('twitter:card', 'summary'), ('twitter:title', title), ('twitter:description', description)]
head += ''.join('<meta name="' + name + '" content="' + html.escape(value, quote=True) + '">\n' for name, value in metas)
head += ''.join('<meta property="' + name + '" content="' + html.escape(value, quote=True) + '">\n' for name, value in [('og:type', 'article'), ('og:title', title), ('og:description', description), ('og:site_name', 'Alec Kriebel'), ('article:published_time', meta['publication_date']), ('article:modified_time', native['updated'])])
head += '<link rel="stylesheet" href="/research/research.css">\n<script type="application/ld+json">' + json.dumps(scholarly, ensure_ascii=False) + '</script>\n</head>\n'
put('head.html', head.encode())
main = (OWN / 'main.html').read_bytes().decode('utf-8')
article = '<!doctype html>\n<html lang="en">\n' + head + '<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="https://aleckriebel.com/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="https://aleckriebel.com/">Home</a> · <a href="https://aleckriebel.com/research/">Research</a></nav></header>\n' + main + '<footer><p><a href="https://aleckriebel.com/research/">Research index</a> · <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></p></footer>\n</body>\n</html>\n'
put('article.html', article.encode())
need(only(r'(<head>.*?</head>\n)', article) == head and only(r'(<main id="main">.*?</main>\n)', article) == main, 'Whole assembly differs')
need(html.unescape(only(r'<p id="abstract-text">(.*?)</p>', main)) == abstract == model['abstract'] == scholarly['abstract'], 'Full original abstract differs')
tags = Tags(article)
need(len(tags.ids) == len(set(tags.ids)), 'Duplicate identifier')
actual_metas = {attrs.get('name', attrs.get('property')): attrs.get('content') for tag, attrs in tags.tags if tag == 'meta'}
need('citation_version' not in actual_metas and 'version' not in scholarly and 'version =' not in (OWN / 'citation.bib').read_text(), 'Author version invented')
need(actual_metas['DC.description'] == abstract and actual_metas['robots'] == actual_metas['googlebot'] == 'noindex, nofollow', 'Abstract/private head differs')
need(all(model[key] is None for key in ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up']) and not model['publication_authority'], 'Private gate differs')
need(not any(tag == 'link' and attrs.get('rel') == 'canonical' for tag, attrs in tags.tags) and 'url' not in scholarly and 'mainEntityOfPage' not in scholarly, 'Actual page canonical present')
need([item['contentUrl'] for item in scholarly['encoding']] == ['assets/source-and-verification.zip', 'assets/paper.pdf'], 'Native2 encodings differ')
need(re.findall(r'<a href="(assets/[^\"]+)" download>', only(r'<ol id="native-assets">(.*?)</ol>', main)) == [item['local_path'] for item in assets], 'Visible native order differs')
need(any(tag == 'iframe' and attrs.get('src') == 'assets/paper.pdf#view=FitH' for tag, attrs in tags.tags), 'Local iframe differs')
need(any(tag == 'a' and attrs.get('href') == 'assets/paper.pdf' and 'download' not in attrs for tag, attrs in tags.tags), 'PDF direct open missing')
need(any(tag == 'a' and attrs.get('href') == 'assets/paper.pdf' and 'download' in attrs for tag, attrs in tags.tags), 'PDF download missing')
need('Apache' in main and 'MIT' not in main + head, 'Actual license exception lost')
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
            need(path.resolve().is_relative_to(OWN.resolve()) and path.is_file(), 'Local link missing/escaping')
        elif url.fragment:
            need(url.fragment in tags.ids, 'Local fragment missing')
    for ident in attrs.get('aria-labelledby', '').split():
        need(ident in tags.ids, 'Label target missing')
bib = (OWN / 'citation.bib').read_bytes().decode('utf-8')
need(all(value in bib for value in [title, native['doi'], 'date = {2026-10-06}', 'Kriebel, Alec', 'Zenodo displays edition v1']) and '1.0.0' not in article + bib, 'Citation identity/edition differs')
after = guards()
need(before == after, 'Source/root/style/slug guard drift')
putj('SOURCE_GUARDS_AFTER.json', after)
putj('STATIC_CHECK.json', {'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_PRIVATE_DATA_ONLY_ASSEMBLY_AND_STATIC_CHECKS', 'whole_head_MAIN_exact': True, 'full_abstract_visible_DC_schema_model_exact': True, 'native97files12dirs_rootpins_unchanged': True, 'ZIP_then_PDF_names_bytes_MD5_SHA256_modes_and2encodings_exact': True, 'API_version_absent_host_HTML_v1_separately_preserved_no_invented_author_version': True, 'CCBY4_original_verification_Apache2_bundled_exception_no_MIT': True, 'private_noindex_null_actual_canonical_publication_AA_followup': True, 'local_links_ids_Bib_and_shared_CSS_checked': True, 'scientific_clearance_inherited': True, 'source_execution_import_AST_compiler_or_test': False, 'new_formal_or_symbolic_PASS_claim': False, 'current_render_or_live_certificate': False})
