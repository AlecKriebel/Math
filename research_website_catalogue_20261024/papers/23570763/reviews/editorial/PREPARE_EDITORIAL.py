"""Explicit private127 editorial preparation. No work or source imports on import."""
from pathlib import Path
import argparse
import datetime
import hashlib
import html
import json
import re

HERE = Path(__file__).absolute().parent
PAPER = HERE.parent.parent
PROJECT = PAPER.parent.parent
SOURCE = PAPER / 'sources'
ROOT = PROJECT / 'verification/root-clearance-23570763-20261115.json'
ROOT_SHA = '56a6e20fcef53e11e3cd7ab2bba1ad6503d0720509983be7b60d5a19bd9dc33f'
READY_SHA = '64b0c9408ee2d24da06d20d3c9bd7653e2ed9537f571a1051d40826ee5e0ab73'
CC = 'https://creativecommons.org/licenses/by/4.0/'
MIT = 'https://opensource.org/license/mit/'


def require(ok, message):
    if not ok: raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def literal(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def binding(path):
    path = Path(path); raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'SHA256': digest(raw)}


def whole(path, role):
    row = binding(path); row['role'] = role; row['whole_literal_object'] = json.loads(Path(path).read_bytes()); return row


def original_abstract(tex):
    raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)
    text = raw
    for before, after in [(r'$p$', 'p'), (r'$n\geq2$', 'n ≥ 2'), (r'$p\nmid n-1$', 'p ∤ n − 1'), (r'$\mathbb F_p(t)$', '𝔽ₚ(t)'), ('R\\"omer', 'Römer')]:
        text = text.replace(before, after)
    return raw, ' '.join(text.split())


def esc(text):
    return html.escape(str(text), quote=True)


def paragraph(text):
    return '<p>' + esc(text) + '</p>'


def make_main(p):
    result = ['<main><article><header><h1>' + esc(p['title']) + '</h1>',
        '<p>Alec Kriebel · <a href="' + p['orcid'] + '">ORCID 0009-0001-9320-500X</a></p>',
        '<p>22 October 2026 · Version 1.0.0 · Unrefereed preprint</p>', paragraph(p['edition_note']), '</header>']
    sections = [('abstract', 'Original abstract', [p['abstract']]), ('plain-language', 'What this means', p['plain_language']),
        ('result', 'The construction and exact classification', p['result']), ('why-it-works', 'Why the pattern occurs', p['why_it_works']),
        ('limitations', 'Scope and limitations', p['limitations']), ('background', 'Context and credit', p['background']),
        ('collaboration', 'Collaboration', p['collaboration']), ('status', 'Authorship and review status', [p['status'], p['ai_disclosure']])]
    for sid, heading, paragraphs in sections:
        result += ['<section id="' + sid + '"><h2>' + heading + '</h2>'] + [paragraph(x) for x in paragraphs] + ['</section>']
    result += ['<section id="primary-background"><h2>Primary background</h2><ul>']
    result += ['<li><a href="' + esc(x['url']) + '">' + esc(x['label']) + '</a></li>' for x in p['related_resources']]
    result += ['</ul></section>', '<section id="read"><h2>Read the paper</h2>', paragraph(p['reader_intro'])]
    result += ['<p><a href="assets/' + p['pdf_filename'] + '" target="_blank" rel="noopener">Open the complete PDF</a> · <a href="assets/' + p['pdf_filename'] + '" download>Download PDF</a> · <a href="assets/' + p['supplement_filename'] + '" download>Download complete source and verification ZIP</a> · <a href="assets/citation.bib" download>Download BibTeX</a></p>']
    for a in p['source_binding']['whole_original_source_ready']['all_native_assets_in_original_order']:
        native = a['original_api_file_object']; result.append('<p><a href="' + esc(native['links']['self']) + '">Zenodo original: ' + esc(native['key']) + '</a></p>')
    result += ['<iframe class="paper-pdf" loading="lazy" src="assets/' + p['pdf_filename'] + '#view=FitH" title="' + esc(p['title']) + ' — complete four-page PDF"></iframe>', '</section>',
        '<section id="cite"><h2>Cite this paper</h2>', '<p>Alec Kriebel. ' + esc(p['title']) + '. Version 1.0.0, 22 October 2026. Zenodo. <a href="https://doi.org/' + p['doi'] + '">doi:' + p['doi'] + '</a>.</p>', '</section>',
        '<section id="rights"><h2>Rights and supporting materials</h2>', paragraph(p['rights_notice']), '<p><a href="' + CC + '">CC BY 4.0</a> · <a href="' + MIT + '">MIT License</a></p>', '</section></article></main>']
    return '\n'.join(result)


def make_page(p, main, build_date):
    url = p['proposed_canonical_url']
    article = {'@type': 'ScholarlyArticle', '@id': url + '#article', 'headline': p['title'], 'name': p['title'], 'description': p['description'], 'abstract': p['abstract'],
        'author': {'@type': 'Person', 'name': p['author'], 'sameAs': p['orcid']}, 'datePublished': p['publication_date'], 'version': p['version'], 'creativeWorkStatus': 'Unrefereed preprint',
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': p['doi']}, 'sameAs': 'https://doi.org/' + p['doi'], 'license': CC, 'keywords': p['keywords'],
        'encoding': [{'@type': 'MediaObject', 'encodingFormat': 'application/zip' if i == 0 else 'application/pdf', 'contentUrl': a['original_api_file_object']['links']['self'],
                     'license': [CC, MIT] if i == 0 else CC} for i, a in enumerate(p['source_binding']['whole_original_source_ready']['all_native_assets_in_original_order'])]}
    graph = {'@context': 'https://schema.org', '@graph': [{'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'dateModified': build_date, 'mainEntity': {'@id': url + '#article'}}, article]}
    head = ['<!doctype html>', '<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">', '<title>' + esc(p['seo']['title']) + '</title>']
    for key, value in [('robots', 'noindex,nofollow'), ('description', p['description']), ('author', p['author']), ('citation_title', p['title']), ('citation_author', p['author']),
        ('citation_author_orcid', p['orcid']), ('citation_publication_date', '2026/10/22'), ('citation_version', '1.0.0'), ('citation_doi', p['doi']), ('citation_pdf_url', 'assets/' + p['pdf_filename']), ('twitter:card', 'summary')]:
        head.append('<meta name="' + key + '" content="' + esc(value) + '">')
    head.append('<link rel="canonical" href="' + url + '">')
    for key, value in [('og:type', 'article'), ('og:title', p['title']), ('og:description', p['description']), ('og:url', url)]:head.append('<meta property="' + key + '" content="' + esc(value) + '">')
    head += ['<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False).replace('</', '<\\/') + '</script>',
        '<style>body{font-family:Arial,Helvetica,sans-serif;color:#111;background:#fff;max-width:850px;margin:0 auto;padding:26px 20px;line-height:1.6}h1{line-height:1.2;font-size:2rem}h2{line-height:1.3;margin-top:2.1rem;font-size:1.3rem}p,a{overflow-wrap:anywhere}a{color:#24558b}.paper-pdf{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;border:1px solid #ccc;box-sizing:border-box}li{margin:.5em 0}@media(max-width:600px){body{padding:20px 15px}h1{font-size:1.65rem}}</style></head><body>', main, '</body></html>']
    return '\n'.join(head) + '\n'


def prepare(build_date):
    require(datetime.date.fromisoformat(build_date).isoformat() == build_date, 'explicit ISO date')
    require(not (HERE / 'SEAL.json').exists() and not (HERE / 'config').exists() and not (HERE / 'candidate').exists(), 'new private editorial outputs only; no overwrite/replay of a prepared packet')
    require(digest(ROOT.read_bytes()) == ROOT_SHA, 'exact root clearance authority')
    authority = json.loads(ROOT.read_bytes()); ready = json.loads((SOURCE / 'SOURCE_READY.json').read_bytes())
    require(digest((SOURCE / 'SOURCE_READY.json').read_bytes()) == READY_SHA, 'exact immutable source READY')
    require(literal(authority['whole_original_SOURCE_READY']) == literal(ready), 'whole original READY including historical unread/null fields')
    draft = json.loads((HERE / 'DRAFT_SECTIONS.json').read_text()); tex_path = Path(ready['controlling_TeX']['extracted_path']); abstract_raw, abstract = original_abstract(tex_path.read_text())
    require(draft['abstract'] == abstract, 'complete original abstract, exact words and declared math rendering')
    require(not (PAPER / 'publication.json').exists() and not (PAPER / 'promotion.json').exists(), 'nested configs only; no paper-level overwrite')
    verdicts = [whole(PAPER / 'reviews/scope/VERDICT.json', 'scope'), whole(PAPER / 'reviews/adversarial/VERDICT.json', 'adversarial')]
    require(literal(verdicts[0]['whole_literal_object']) == literal(authority['whole_independent_scope_VERDICT']), 'whole original scope verdict')
    require(literal(verdicts[1]['whole_literal_object']) == literal(authority['whole_independent_adversarial_VERDICT']), 'whole original adversarial verdict')
    transports = json.loads((SOURCE / 'ALL_TRANSPORT_RECEIPTS.json').read_bytes())
    require(type(transports) is list and [x['HTTP_status'] for x in transports] == [200,301,200,200,200,200,200], 'actual heterogeneous aggregate is seven-item list')
    protocol = {'schema': 'editorial127-whole-native-source-protocol-v1', 'original_source_ready': whole(SOURCE / 'SOURCE_READY.json', 'source READY'),
        'source_terminal_objects': [whole(SOURCE / x, x) for x in ['SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json','SOURCE_READY_CLOSURE.json']],
        'native_API_objects': [whole(x['path'], x['role']) for x in ready['whole_native_API_objects']],
        'transport_aggregate': whole(SOURCE / 'ALL_TRANSPORT_RECEIPTS.json', 'original seven-item transport list'),
        'transport_objects': [whole(SOURCE / (Path(x['body_path']).name + '.transport.json'), 'native dispatch ' + str(i)) for i,x in enumerate(transports)],
        'native_schema_types': whole(SOURCE / 'NATIVE_SCHEMA_TYPES.json', 'native heterogeneous types'), 'archive_custody': whole(SOURCE / 'ARCHIVE_CUSTODY.json', 'all18 regular occurrences'),
        'whole_original_two_science_verdicts': verdicts, 'scientific_review_seals': [whole(PAPER / 'reviews' / x / 'SEAL.json', x + ' final seal') for x in ['scope','adversarial']],
        'historical_flags_unchanged': True, 'literal_native_order': [x['original_api_file_object']['key'] for x in ready['all_native_assets_in_original_order']], 'native_source_objects_not_normalized': True}
    bib = '@misc{kriebel2026periodiclefschetz,\n  author = {Kriebel, Alec},\n  title = {' + draft['title'] + '},\n  year = {2026},\n  month = oct,\n  day = {22},\n  version = {1.0.0},\n  publisher = {Zenodo},\n  doi = {10.5281/zenodo.23570763},\n  url = {https://doi.org/10.5281/zenodo.23570763},\n  note = {Unrefereed preprint. Original version 1.0.0, dated 22 October 2026.}\n}\n'
    pub = dict(draft); pub.update({'abstract_heading': 'Original abstract', 'abstract_is_original': True, 'followup_rationale': 'No sufficiently justified high-bar follow-up proposed; no current worldwide-open-status inference.',
        'publication_date': '2026-10-22', 'version': '1.0.0', 'version_field_present': True, 'printed_version': '1.0.0', 'doi': '10.5281/zenodo.23570763', 'author': 'Alec Kriebel', 'orcid': 'https://orcid.org/0009-0001-9320-500X',
        'pdf_filename': 'periodic-lefschetz.pdf', 'pdf_pages': 4, 'supplement_filename': 'periodic-lefschetz-source-and-verification.zip', 'supplement_label': 'Complete original source and verification ZIP', 'additional_assets': [],
        'license': 'CC BY 4.0', 'license_url': CC, 'code_license': 'MIT', 'code_license_url': MIT, 'code_license_basis': 'Actual separate LICENSE-CODE-MIT.txt and README; prose/source text governed by LICENSE-PROSE-CC-BY-4.0.txt.',
        'publication_date_label': 'Original publication date', 'edition_label': 'Version 1.0.0', 'edition_note': 'Original printed and Zenodo edition: version 1.0.0, dated 22 October 2026. Native record creation is separately recorded in the metadata.',
        'native_record_created': ready['created'], 'native_record_updated': ready['updated'], 'canonical_url': None, 'AA': None, 'native_sheet_aa_url': None,
        'proposed_canonical_url': 'https://aleckriebel.com/research/' + draft['slug'] + '/', 'seo': {'title': draft['title'] + ' | Alec Kriebel', 'description': draft['description'], 'robots_private_candidate': 'noindex,nofollow'}, 'prepared_bibtex': bib,
        'source_binding': {'source_ready_path': str(SOURCE / 'SOURCE_READY.json'), 'source_ready_sha256': READY_SHA, 'whole_original_source_ready': ready,
            'source_protocol_binding_path': str(HERE / 'SOURCE_PROTOCOL_BINDINGS.json'), 'whole_original_native_API_objects': protocol['native_API_objects'],
            'whole_original_seven_transport_objects': protocol['transport_objects'], 'whole_original_transport_aggregate': protocol['transport_aggregate'],
            'whole_original_archive_custody': protocol['archive_custody'], 'whole_original_native_schema_types': protocol['native_schema_types'],
            'whole_original_source_terminal_objects': protocol['source_terminal_objects'], 'historical_unread_flags_and_nulls_preserved_literally': True,
            'all18_original_ZIP_payloads_unchanged': True, 'native_asset_order': protocol['literal_native_order']},
        'review_metadata': {'root_scientific_authority_file': str(ROOT), 'root_scientific_authority_sha256': ROOT_SHA, 'whole_root_scientific_clearance_record': authority,
            'whole_original_two_scientific_custom_verdicts': verdicts, 'whole_original_scientific_review_seals': protocol['scientific_review_seals'], 'actual_scientific_review_cardinality': 2,
            'editorial_role': 'Informed editorial preparation after root adoption; prior127 source-only acquisition role disclosed, no127 independent scientific-review claim.', 'root_full_copy_and_config_adoption_pending': True}})
    promotion = {'record_id': '23570763', 'sheet_row': 127, 'status': 'Private editorial candidate — full-copy/config root adoption pending', 'scientific_status': authority['disposition'], 'created_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'full_original_scope_supported': True, 'root_clearance_file': str(ROOT), 'root_clearance_sha256': ROOT_SHA, 'whole_root_scientific_clearance_record': authority,
        'whole_original_two_scientific_custom_verdicts': verdicts, 'whole_original_source_ready': ready, 'whole_original_native_API_objects': protocol['native_API_objects'],
        'whole_original_seven_transport_objects': protocol['transport_objects'], 'whole_original_transport_aggregate': protocol['transport_aggregate'], 'actual_scientific_review_cardinality': 2,
        'source_repair': False, 'narrowed_replacement': False, 'follow_up': None, 'human_peer_review': False, 'formal_certification': False, 'private_static_candidate_written': True,
        'rendered': False, 'deployed': False, 'rendered_public_copy_approved': False, 'rendered_copy_verified': False, 'local_http_verified': False, 'live_http_verified': False, 'live_verified': False,
        'browser_verified': False, 'native_verified': False, 'native_sheet_publication_verified': False, 'public_page_published': False, 'root_editorial_clearance_received': False,
        'production_integration_authorized': False, 'publication_clearance': False, 'ready_to_publish': False, 'canonical_verified': False, 'canonical_url': None, 'AA': None, 'native_sheet_aa_url': None,
        'proposed_canonical_url': pub['proposed_canonical_url'], 'historical_source_and_review_flags_not_normalized': True}
    # Only explicit owned destinations are written; all originals are read-only.
    def write(name, obj):
        out = HERE / name; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    write('SOURCE_PROTOCOL_BINDINGS.json', protocol); pub['source_binding']['source_protocol_binding_sha256'] = digest((HERE / 'SOURCE_PROTOCOL_BINDINGS.json').read_bytes())
    write('config/publication.json', pub); promotion['publication_sha256'] = digest((HERE / 'config/publication.json').read_bytes()); write('config/promotion.json', promotion)
    main = make_main(pub); (HERE / 'PUBLIC_MAIN.html').write_text(main + '\n'); (HERE / 'abstract-source.tex').write_text(abstract_raw); (HERE / 'citation.bib').write_text(bib)
    out = HERE / 'candidate'; (out / 'assets').mkdir(parents=True, exist_ok=True); (out / 'index.html').write_text(make_page(pub, main, build_date))
    for a in ready['all_native_assets_in_original_order']:
        raw = Path(a['path']).read_bytes(); require(len(raw) == a['bytes'] and digest(raw) == a['SHA256'], 'unchanged native asset')
        require(hashlib.md5(raw).hexdigest() == a['original_api_file_object']['checksum'].removeprefix('md5:'), 'actual native MD5')
        (out / 'assets' / a['original_api_file_object']['key']).write_bytes(raw)
    (out / 'assets/citation.bib').write_text(bib)
    copy = ['# ' + pub['title'], '\nAlec Kriebel · ORCID ' + pub['orcid'], '\n22 October 2026 · Version 1.0.0 · Unrefereed preprint']
    for title,key in [('Original abstract','abstract'),('What this means','plain_language'),('The construction and exact classification','result'),('Why the pattern occurs','why_it_works'),('Scope and limitations','limitations'),('Context and credit','background'),('Collaboration','collaboration'),('Authorship and review status','status')]:
        vals = pub[key] if isinstance(pub[key],list) else [pub[key]];copy += ['\n## ' + title] + ['\n' + x for x in vals]
        if key == 'status': copy.append('\n' + pub['ai_disclosure'])
    copy += ['\n## Primary background'] + ['\n- [' + x['label'] + '](' + x['url'] + ')' for x in pub['related_resources']]
    copy += ['\n## Read the paper', '\n' + pub['reader_intro'], '\n- Local unchanged PDF: assets/' + pub['pdf_filename'], '\n- Complete original ZIP: assets/' + pub['supplement_filename'], '\n- Citation: assets/citation.bib', '\n- Zenodo DOI: https://doi.org/' + pub['doi'], '\n## Rights', '\n' + pub['rights_notice']]
    (HERE / 'PUBLIC_COPY.md').write_text('\n'.join(copy) + '\n')
    write('SCHEMA_ADAPTER.json', {'schema': 'private-editorial-config-placement-and-native-adapter127-v1', 'publication_path': str(HERE / 'config/publication.json'), 'promotion_path': str(HERE / 'config/promotion.json'),
        'paper_level_configs_absent_and_not_created': True, 'whole_original_source_binding': pub['source_binding'], 'whole_original_review_metadata': pub['review_metadata'],
        'literal_aggregate_type': 'list', 'native_asset_order': protocol['literal_native_order'], 'source_production_or_science_mutations': False,
        'printed_identity_separate_from_historical_source_unread_nulls': {'date': '2026-10-22', 'version': '1.0.0'}, 'source_native_order_nulls_types_headers_and_seals_preserved': True})
    return {'status': 'PRIVATE_EDITORIAL_CANDIDATE_ONLY', 'owned_root': str(HERE), 'PDF_pages': 4, 'complete_ZIP_payloads': 18, 'source_or_production_changes': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--write-private-candidate', action='store_true', required=True); ap.add_argument('--build-date', required=True)
    args = ap.parse_args(); print(json.dumps(prepare(args.build_date), indent=2))


if __name__ == '__main__':
    main()
