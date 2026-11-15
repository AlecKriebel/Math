#!/usr/bin/env python3
"""Private authoring only. Writes solely inside this editorial namespace."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import html
import json
import re
import shutil

A = Path(__file__).resolve().parent
R = A.parents[1]
S = R / 'sources'
P = R.parents[1]
if (A / 'SEAL.json').exists():
    raise RuntimeError('sealed editorial packet is immutable')


def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}


def load(p):
    return json.loads(p.read_text())


def write(p, value):
    if not p.resolve().is_relative_to(A):
        raise ValueError('write outside owned editorial folder')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value)


def put(p, value):
    write(p, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


source = load(S / 'SOURCE_READY.json')
clear_path = P / 'verification/root-clearance-23333002-20261115.json'
clearance = load(clear_path)
if pin(S / 'SOURCE_READY.json')['SHA256'] != '91a2924e8c97f248e5ac8c9d5b61f6623c93df30b40d71cdbf852284bb294d1b':
    raise ValueError('source authority mismatch')
if pin(clear_path)['SHA256'] != 'dda6df711f74abcd94d77f8187dafc1140465ef33a4610b75e20a7ebc78060c3':
    raise ValueError('root authority mismatch')
if clearance['whole_literal_source_ready'] != source:
    raise ValueError('whole source object association')

draft = load(A / 'DRAFT_SECTIONS.json')
tex = (S / 'published-source/note.tex').read_text()
raw_abstract = re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}', tex).group(1)
abstract = ' '.join(raw_abstract.split())
write(A / 'abstract-source.tex', raw_abstract)
write(A / 'abstract-original.txt', abstract + '\n')
native_api = [{'role': x['role'], 'file': x, 'whole_original_object': load(Path(x['path']))}
              for x in source['whole_native_API_objects']]
record = next(x['whole_original_object'] for x in native_api if x['role'] == 'record')
aggregate = load(S / 'ALL_TRANSPORT_RECEIPTS.json')
receipts = aggregate['receipts']
if [x['HTTP_status'] for x in receipts] != [200, 301, 200, 200, 200, 200, 200]:
    raise ValueError('literal transport history mismatch')
reviews = []
for entry in clearance['independent_review_packets']:
    vpath = P / entry['verdict_path']
    verdict = load(vpath)
    if pin(vpath)['SHA256'] != entry['verdict_sha256'] or verdict != entry['whole_literal_custom_verdict']:
        raise ValueError('literal scientific verdict mismatch')
    seal = P / entry['seal']['path']
    reviews.append({'lane': entry['lane'], 'verdict_file': pin(vpath),
                    'whole_original_custom_verdict': verdict, 'seal_file': pin(seal),
                    'whole_original_review_seal': load(seal)})
if len(reviews) != 2:
    raise ValueError('actual review cardinality')

copy_map = []
copied = set()


def copy_original(p, target):
    p = p.resolve()
    if p in copied:
        return
    if not target.resolve().is_relative_to(A):
        raise ValueError('copy outside owned namespace')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, target)
    if p.read_bytes() != target.read_bytes():
        raise ValueError('copy changed bytes')
    copy_map.append({'original': pin(p), 'owned_byte_identical_copy': pin(target)})
    copied.add(p)


metadata_names = ['SOURCE_READY.json', 'SOURCE_READY_SEAL.json', 'SOURCE_READY_MANIFEST.json',
                  'SOURCE_READY_CLOSURE.json', 'ALL_TRANSPORT_RECEIPTS.json', 'ARCHIVE_CUSTODY.json',
                  'NATIVE_SCHEMA_TYPES.json', 'MANUSCRIPT_CUSTODY.json', 'QUEUE_BINDING.json',
                  'ACQUIRED_NATIVE.json', 'NATIVE_SHEET_IDENTITY_SUBRANGES.json']
for name in metadata_names:
    copy_original(S / name, A / 'inputs/source' / name)
for x in source['whole_native_API_objects']:
    p = Path(x['path'])
    copy_original(p, A / 'inputs/source' / p.relative_to(S))
transport_files = list(S.rglob('*.transport.json'))
for receipt in receipts:
    body = Path(receipt['body_path'])
    copy_original(body, A / 'inputs/source' / body.relative_to(S))
    matches = [p for p in transport_files if load(p) == receipt]
    if len(matches) != 1:
        raise ValueError('actual transport file not uniquely matched by whole object')
    copy_original(matches[0], A / 'inputs/source' / matches[0].relative_to(S))
copy_original(clear_path, A / 'inputs/root-clearance.json')
copy_original(R / 'reviews/root/ROOT_REVIEW_20261115.md', A / 'inputs/ROOT_REVIEW_20261115.md')
copy_original(R / 'reviews/root/POST_INITIAL_PRIMARY_READING_20261115.json', A / 'inputs/ROOT_PRIMARY_READING.json')
for review in reviews:
    for key in ['verdict_file', 'seal_file']:
        p = Path(review[key]['path'])
        copy_original(p, A / 'inputs/science' / review['lane'] / p.name)
for name in ['README.md', 'original_packet/README.md', 'requirements.txt']:
    copy_original(S / 'published-source' / name, A / 'inputs/authored' / name)

assets = source['all_native_assets_in_original_order']
for item in assets:
    p = Path(item['path'])
    b = p.read_bytes()
    if len(b) != item['bytes'] or hashlib.sha256(b).hexdigest() != item['SHA256']:
        raise ValueError('native asset hash/size')
    expected_md5 = item['original_api_file_object']['checksum'].split(':', 1)[1]
    if hashlib.md5(b).hexdigest() != expected_md5:
        raise ValueError('native asset MD5')
    write_path = A / 'candidate/assets' / item['original_api_file_object']['key']
    write_path.write_bytes(b)

root_review = (R / 'reviews/root/ROOT_REVIEW_20261115.md').read_text()
source_binding = {'schema': 'private-whole-source-protocol-23333002-v1',
    'source_ready_file': pin(S / 'SOURCE_READY.json'), 'whole_original_SOURCE_READY': source,
    'whole_original_native_API_objects': native_api,
    'whole_original_seven_transport_objects': receipts,
    'whole_original_transport_aggregate': aggregate,
    'whole_original_archive_custody': load(S / 'ARCHIVE_CUSTODY.json'),
    'whole_original_native_schema_types': load(S / 'NATIVE_SCHEMA_TYPES.json'),
    'whole_original_source_terminal_seal': load(S / 'SOURCE_READY_SEAL.json'),
    'native_asset_order': [x['original_api_file_object']['key'] for x in assets],
    'all85_original_regular_payloads_preserved_by_unchanged_whole_ZIP': True,
    'no_source_acquisition_or_archive_extraction_replay': True,
    'raw_original_byte_copies': copy_map}
review_metadata = {'whole_root_scientific_clearance': clearance,
    'root_scientific_clearance_file': pin(clear_path), 'whole_root_scientific_review': root_review,
    'whole_actual_original_scientific_review_records': reviews,
    'actual_scientific_review_cardinality': 2,
    'editor_role': 'Informed editorial preparation after root clearance; prior own125 source acquisition was metadata/custody only; no new blind science claim.',
    'editorial_is_new_scientific_review': False, 'new_scientific_or_native_programme_runs': [],
    'root_editorial_full_copy_adoption_received': False}
put(A / 'SOURCE_PROTOCOL_BINDINGS.json', source_binding)

pdf_name = assets[0]['original_api_file_object']['key']
zip_name = assets[1]['original_api_file_object']['key']
doi = record['doi']
date = record['metadata']['publication_date']
version = record['metadata']['version']
bib = ('@misc{kriebel2026robinsontangency,\n'
       '  author = {Kriebel, Alec},\n'
       '  title = {A Robinson counterexample to ideal-only tangency certificates},\n'
       '  year = {2026},\n  month = oct,\n  day = {12},\n'
       '  date = {2026-10-12},\n  version = {1.0},\n  publisher = {Zenodo},\n'
       f'  doi = {{{doi}}},\n  url = {{https://doi.org/{doi}}},\n'
       '  note = {Unrefereed preprint. Original version 1.0, dated 12 October 2026.}\n}\n')
write(A / 'citation.bib', bib)
write(A / 'candidate/assets/citation.bib', bib)
proposed = 'https://aleckriebel.com/research/' + draft['slug'] + '/'
pub = dict(draft)
pub.update({'abstract': abstract, 'abstract_heading': 'Original abstract', 'abstract_is_original': True,
    'author': 'Alec Kriebel', 'orcid': 'https://orcid.org/0009-0001-9320-500X',
    'publication_date': date, 'publication_date_label': '12 October 2026', 'version': version,
    'printed_version': '1.0', 'version_field_present': True, 'edition_label': 'Version 1.0',
    'citation_edition_label': 'Version 1.0', 'doi': doi,
    'edition_note': 'The manuscript prints 12 October 2026 and Version 1.0, matching the declared Zenodo edition. Record creation on 13 October is a separate metadata event.',
    'native_created': record['created'], 'native_updated': record['updated'],
    'pdf_filename': pdf_name, 'pdf_pages': 4, 'supplement_filename': zip_name,
    'supplement_label': 'Complete original source and verification archive (ZIP)', 'additional_assets': [],
    'license': 'CC BY 4.0', 'license_url': 'https://creativecommons.org/licenses/by/4.0/',
    'authored_package_license': 'CC BY 4.0', 'code_license': None,
    'authored_code_covered_by_package_CC_BY_4_0': True,
    'code_license_basis': 'The actual README explicitly grants CC BY4.0 to authored manuscript, proofs, code and audits. No distinct code-specific instrument or MIT grant is asserted.',
    'prepared_bibtex': bib, 'canonical_url': None, 'AA': None, 'native_sheet_aa_url': None,
    'proposed_canonical_url': proposed, 'follow_up': None,
    'followup_rationale': 'No source-supported follow-up meeting the required significance bar is proposed.',
    'seo': {'title': draft['title'] + ' | Alec Kriebel', 'description': draft['description'],
            'robots_private_candidate': 'noindex,nofollow'},
    'source_binding': source_binding, 'review_metadata': review_metadata})
put(A / 'publication.json', pub)

gate_names = ['rendered', 'deployed', 'rendered_public_copy_approved', 'rendered_copy_verified',
    'local_http_verified', 'live_http_verified', 'live_verified', 'browser_verified', 'native_verified',
    'native_sheet_publication_verified', 'public_page_published', 'root_editorial_clearance_received',
    'production_integration_authorized', 'publication_clearance', 'ready_to_publish', 'canonical_verified']
promotion = {'record_id': '23333002', 'sheet_row': 125,
    'status': 'PRIVATE_COMPLETE_EDITORIAL_CANDIDATE_PENDING_ROOT_FULL_COPY_ADOPTION',
    'scientific_status': clearance['status'], 'full_original_mathematical_scope_supported': True,
    'approved_scope': clearance['mathematical_scope'], 'whole_root_scientific_clearance_record': clearance,
    'whole_original_custom_scientific_verdicts': [x['whole_original_custom_verdict'] for x in reviews],
    'whole_original_scientific_review_seals': [x['whole_original_review_seal'] for x in reviews],
    'actual_scientific_review_cardinality': len(reviews), 'whole_original_source_ready': source,
    'whole_original_native_API_objects': native_api, 'whole_original_seven_transport_objects': receipts,
    'whole_original_transport_aggregate': aggregate, 'source_ready_sha256': pin(S / 'SOURCE_READY.json')['SHA256'],
    'root_clearance_file': str(clear_path), 'root_clearance_sha256': pin(clear_path)['SHA256'],
    'private_static_candidate_written': True, 'source_repair': False, 'narrowed_replacement': False,
    'human_peer_review': False, 'formal_certification': False, 'canonical_url': None, 'AA': None,
    'native_sheet_aa_url': None, 'proposed_canonical_url': proposed, 'follow_up': None,
    'publication_sha256': pin(A / 'publication.json')['SHA256'], 'all203_complete_claimed': False,
    'root_configs_outside_owned_namespace_written': False}
promotion.update({k: False for k in gate_names})
put(A / 'promotion.json', promotion)

sections = {'abstract': abstract, **{k: draft[k] for k in ['plain_language', 'result', 'why_it_works',
    'limitations', 'background', 'collaboration', 'status', 'ai_disclosure',
    'reader_intro', 'rights_notice', 'related_resources']}}
put(A / 'public-sections.json', sections)

def paras(value):
    values = value if isinstance(value, list) else [value]
    return ''.join('<p class="math">' + html.escape(v) + '</p>' for v in values)


ordered = [('What the result means', 'plain_language'), ('The full result', 'result'),
           ('Why the obstruction works', 'why_it_works'),
           ('Scope and limitations', 'limitations'), ('Background and credit', 'background'),
           ('Contribution and collaboration', 'collaboration'), ('AI and review disclosure', 'ai_disclosure')]
citation = f'Alec Kriebel. {draft["title"]}. Version {version}, 12 October 2026. Zenodo. doi:{doi}.'
reader = (paras(draft['reader_intro']) + f'<p><a href="assets/{pdf_name}">Open original PDF</a> · '
    f'<a href="assets/{pdf_name}" download>Download original PDF</a> · '
    f'<a href="assets/{zip_name}" download>Download the complete original ZIP</a> · '
    '<a href="assets/citation.bib" download>Download BibTeX</a></p>'
    f'<p><a href="https://zenodo.org/records/23333002">Zenodo record</a> · <a href="https://doi.org/{doi}">DOI</a> · '
    f'<a href="{assets[0]["original_api_file_object"]["links"]["self"]}">Original PDF on Zenodo</a> · '
    f'<a href="{assets[1]["original_api_file_object"]["links"]["self"]}">Original ZIP on Zenodo</a></p>'
    f'<iframe class="paper-pdf" src="assets/{pdf_name}#view=FitH" title="{html.escape(draft["title"])} — complete four-page PDF" width="100%" height="850" loading="lazy"></iframe>')
links = '<ul>' + ''.join('<li><a href="' + html.escape(x['url']) + '">' + html.escape(x['title']) + '</a></li>' for x in draft['related_resources']) + '</ul>'
article = '<p><a href="https://aleckriebel.com/research/">Research</a></p><article>'
article += '<h1>' + html.escape(draft['title']) + '</h1><p>Alec Kriebel · <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></p>'
article += '<p>12 October 2026 · Version 1.0 · Unrefereed preprint</p>'
article += '<section><h2>Original abstract</h2>' + paras(abstract) + '</section>'
for heading, key in ordered:
    article += '<section><h2>' + heading + '</h2>' + paras(draft[key]) + '</section>'
article += '<section><h2>Read and download</h2>' + reader + '</section><section><h2>Citation</h2>' + paras(citation) + '</section>'
article += '<section><h2>Primary background</h2>' + links + '</section><section><h2>Rights</h2>' + paras(draft['rights_notice'])
article += '<p><a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0 license</a></p></section></article>'
schema = {'@context': 'https://schema.org', '@type': 'ScholarlyArticle', 'headline': draft['title'],
    'name': draft['title'], 'description': draft['description'], 'abstract': abstract,
    'author': {'@type': 'Person', 'name': 'Alec Kriebel', 'sameAs': pub['orcid']},
    'datePublished': date, 'version': version, 'creativeWorkStatus': draft['status'],
    'identifier': {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': doi},
    'sameAs': 'https://doi.org/' + doi, 'license': pub['license_url'], 'keywords': draft['keywords'],
    'encoding': [{'@type': 'MediaObject', 'encodingFormat': 'application/pdf' if x['original_api_file_object']['key'].endswith('.pdf') else 'application/zip',
                  'contentUrl': x['original_api_file_object']['links']['self']} for x in assets]}
head = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
head += '<meta name="robots" content="noindex,nofollow"><title>' + html.escape(pub['seo']['title']) + '</title>'
metadata = {'description': draft['description'], 'author': 'Alec Kriebel', 'citation_title': draft['title'],
    'citation_author': 'Alec Kriebel', 'citation_publication_date': date.replace('-', '/'),
    'citation_version': version, 'citation_doi': doi, 'citation_pdf_url': 'assets/' + pdf_name}
head += ''.join('<meta name="' + k + '" content="' + html.escape(v) + '">' for k, v in metadata.items())
head += '<meta property="og:type" content="article"><meta property="og:title" content="' + html.escape(draft['title']) + '">'
head += '<meta property="og:description" content="' + html.escape(draft['description']) + '">'
head += '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script>'
head += '<style>body{font-family:Arial,Helvetica,sans-serif;background:#fff;color:#111;max-width:850px;margin:0 auto;padding:26px 20px;line-height:1.6}h1{font-size:2rem;line-height:1.2}h2{font-size:1.3rem;line-height:1.3;margin-top:2.1rem}p,a{overflow-wrap:anywhere}.math{white-space:pre-wrap}a{color:#24558b}li{margin:.5em 0}.paper-pdf{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;border:1px solid #ccc;box-sizing:border-box}@media(max-width:600px){body{padding:20px 15px}h1{font-size:1.65rem}}</style></head>'
write(A / 'candidate/index.html', head + '<body><main>' + article + '</main></body></html>\n')
write(A / 'ARTICLE_MAIN.html', article + '\n')
md = '# ' + draft['title'] + '\n\nAlec Kriebel · [ORCID](' + pub['orcid'] + ')\n\n12 October 2026 · Version 1.0 · Unrefereed preprint\n\n## Original abstract\n\n' + abstract + '\n'
for heading, key in ordered:
    values = draft[key] if isinstance(draft[key], list) else [draft[key]]
    md += '\n## ' + heading + '\n\n' + '\n\n'.join(values) + '\n'
md += '\n## Read and download\n\n' + draft['reader_intro'] + '\n\n'
md += f'- [Open original PDF](assets/{pdf_name})\n- <a href="assets/{pdf_name}" download>Download original PDF</a>\n'
md += f'- [Download the complete original ZIP](assets/{zip_name})\n- [Download BibTeX](assets/citation.bib)\n- [Zenodo record](https://zenodo.org/records/23333002)\n- [DOI](https://doi.org/{doi})\n\n'
md += '- [Original PDF on Zenodo](' + assets[0]['original_api_file_object']['links']['self'] + ')\n'
md += '- [Original ZIP on Zenodo](' + assets[1]['original_api_file_object']['links']['self'] + ')\n\n'
md += f'<iframe src="assets/{pdf_name}#view=FitH" title="{draft["title"]} — complete four-page PDF" width="100%" height="850" loading="lazy"></iframe>\n'
md += '\n## Citation\n\n' + citation + '\n\n## Primary background\n\n'
md += '\n'.join('- [' + x['title'] + '](' + x['url'] + ')' for x in draft['related_resources'])
md += '\n\n## Rights\n\n' + draft['rights_notice'] + '\n'
write(A / 'PUBLIC_COPY.md', md)
put(A / 'SCHEMA_ADAPTER.json', {'schema': 'private-editorial-source-adapter-23333002-v1',
    'whole_original_protocol_binding': source_binding,
    'whole_original_review_metadata': review_metadata,
    'exact_actual_interfaces': {'asset_order': 'all_native_assets_in_original_order',
       'asset_hash': 'SHA256', 'PDF': 'selected_actual_PDF', 'TeX': 'controlling_TeX.extracted_path',
       'transports': 'ALL_TRANSPORT_RECEIPTS.json.receipts; actual seven matched whole transport files',
       'all_versions': 'whole_native_API_objects role=versions_page001',
       'historical_unread_flags': 'Original SOURCE_READY booleans remain literal despite later editorial reading',
       'native_license': 'native_license_metadata_whole_field.original_value; actual README authored-code grant'},
    'private_publication_config': str(A / 'publication.json'), 'private_promotion_config': str(A / 'promotion.json'),
    'preferred_complete_presentation_source': 'candidate/index.html or ARTICLE_MAIN.html; explicit full main tree, no legacy Markdown/TeX subset assumed',
    'publication_root_configs_written': False, 'root_full_copy_and_config_adoption_required': True,
    'canonical_url': None, 'AA': None, 'publication_authority': False, 'follow_up': None})
put(A / 'RIGHTS_AND_IDENTITY.json', {'native_title': record['metadata']['title'], 'declared_date': date,
    'printed_date': '12 October 2026', 'printed_version': 'Version 1.0', 'native_version': version,
    'native_created': record['created'], 'native_updated': record['updated'],
    'actual_README_explicitly_covers_authored_code': True, 'paper_and_authored_package_license': 'CC BY 4.0',
    'distinct_code_specific_instrument': None, 'MIT_grant_asserted': False,
    'third_party_source_bodies_redistributed': False,
    'README_reproduction_requirements': 'Python3.10+ with SymPy1.14.0; wrapper may run normally or with -O but raw historical assertion-based children are run without optimization. No native program replay here.',
    'whole_README': (S / 'published-source/README.md').read_text(),
    'whole_original_packet_README': (S / 'published-source/original_packet/README.md').read_text()})
print(json.dumps({'status': 'PRIVATE_EDITORIAL_PREPARED', 'assets': len(assets), 'scientific_verdicts': len(reviews),
                  'whole_transport_objects': len(receipts), 'raw_byte_copies': len(copy_map),
                  'candidate': pin(A / 'candidate/index.html'), 'publication': pin(A / 'publication.json')}))
