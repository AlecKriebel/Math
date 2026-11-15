"""Explicit one-shot authoring of this new private packet; never scientific execution."""
import hashlib
import html
import json
from pathlib import Path

E = Path(__file__).resolve().parent
S = E.parents[1] / 'sources'


def read(name):
    return json.loads((E / 'inputs' / name).read_bytes())


def write(name, obj):
    (E / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def bound(name):
    p = E / 'inputs' / name
    b = p.read_bytes()
    return {'copy': 'inputs/' + name, 'bytes': len(b),
            'SHA256': hashlib.sha256(b).hexdigest(), 'whole_literal_object': json.loads(b)}


def para(text):
    return '<p>' + html.escape(text) + '</p>'


if __name__ != '__main__':
    raise SystemExit('Authoring is an explicit terminal operation, not an import interface.')

if (E / 'publication.json').exists() or (E / 'SEAL.json').exists():
    raise SystemExit('Refusing to replace any authored or sealed packet.')

ready = read('SOURCE_READY.json')
authority = read('ROOT_CLEARANCE.json')
original_verdicts = [bound('scope-VERDICT.json'), bound('adversarial-VERDICT.json')]
native = [bound(x) for x in ['record.response.body', 'latest.response.body.redirect-01',
                            'versions-page001.response.body', 'files.response.body']]
protocol = {
    'source_ready': bound('SOURCE_READY.json'),
    'whole_native_API_objects': native,
    'whole_ordered_transport_receipts': bound('ALL_TRANSPORT_RECEIPTS.json'),
    'whole_native_schema_types': bound('NATIVE_SCHEMA_TYPES.json'),
    'whole_archive_custody': bound('ARCHIVE_CUSTODY.json'),
    'whole_original_queue_binding': bound('QUEUE_BINDING.json'),
    'whole_original_native_identity_subset': bound('NATIVE_IDENTITY_MATCH.json'),
    'whole_original_scientific_custom_verdicts': original_verdicts,
    'whole_root_scientific_authority': bound('ROOT_CLEARANCE.json'),
    'source_manifest': bound('SOURCE_READY_MANIFEST.json'),
    'source_seal': bound('SOURCE_READY_SEAL.json'),
    'native_asset_order': [x['original_api_file_object']['key'] for x in ready['all_native_assets_in_original_order']],
    'whole_objects_types_keys_list_header_order_absent_null_and_history_preserved': True,
    'historical_reading_flags_unchanged': True,
    'new_native_or_scientific_execution': False
}
write('SOURCE_PROTOCOL_BINDINGS.json', protocol)

abstract = ('We specify six algebraic boundary points, an incoming center, and at least five distinct outgoing centers for a cube move of 16-realizations. Existence follows from strict rational sign bounds for two continuous one-variable residuals. The boundary parameters are uniquely defined real roots of monotone polynomials. This contradicts the at-most-three expectation for construction curves sharing a focus in Remark 4.8 of Melotti–Ramassamy–Thévenin, in the realization setting allowing crossings. The fixed boundary is crossed, so the example concerns no proper embedding. Neither the exact number of centers for this boundary nor a universal maximum is determined.')
sections = {
    'title': ready['title'],
    'description': 'One fixed algebraic crossed boundary admits an incoming exponent-16 realization and at least five distinct outgoing centers, exceeding the stated maximum-three expectation.',
    'plain_language': [
        'A local cube move replaces one central point by another while keeping six boundary points fixed. The quadrilateral rule equates the sums of opposite side lengths raised to a chosen power.',
        'At power 16, this note gives one fixed algebraic boundary with an incoming center and at least five outgoing choices. The same boundary works for all of them; its segments cross, so this is a realization allowing crossings.'
    ],
    'result': [
        'Six fixed distinct algebraic points A₁,…,A₆, with both alternating triples noncollinear, admit an incoming center Z and at least five distinct outgoing centers X at α = 16. Every selected center differs from every boundary point.',
        'A quadrilateral PQRS is an α-quad when |P−Q|^α + |R−S|^α = |P−S|^α + |Q−R|^α. The three incoming ordered faces are A₁A₂A₃Z, A₃A₄A₅Z and A₅A₆A₁Z; the three outgoing ordered faces are A₂A₃A₄X, A₄A₅A₆X and A₆A₁A₂X. All six identities hold for the same boundary.',
        'The outgoing centers are at least five intersections of two distinct smooth construction curves sharing the focus A₂. This exceeds the at-most-three expectation for α > 1 in Melotti–Ramassamy–Thévenin, Remark 4.8, p. 811, and the maximum-three conjecture in the crossing-permitted workshop setting, p. 1785. The cited existence theorem is a separate statement.'
    ],
    'why_it_works': [
        'Set A = (0,0), B = (2073/10000,0), C = (4719/10000,64/10000) and λ = 27/1250. The outgoing equations are |X−B|¹⁶ − |X−A|¹⁶ = λ and |X−C|¹⁶ − |X−A|¹⁶ = 1.',
        'With s = |X−A|¹⁶, nonnegative real eighth roots give the three squared distances. An invertible linear system recovers X; one continuous residual G(s) then characterizes the original equations in both directions, retaining all real-branch constraints.',
        'Strict rational signs at 9/10000, 11/10000, 13/10000, 1/2, 1 and 10¹⁶ alternate. The intermediate value theorem supplies a zero in each of five disjoint finite intervals. Different s give different centers; uniqueness within an interval is unnecessary. A concavity estimate controls the remote endpoint without subtracting nearly equal large radicals.',
        'Three uniquely defined real roots of monotone rational polynomials fix the other boundary vertices. Their exact edge-power identities telescope. For this same fixed boundary, a second continuous residual has opposite strict endpoint signs and produces an actual incoming center. The written algebra verifies every incoming and outgoing ordered face, including the dependent third incoming identity.',
        'Exact rational enclosures separate the selected centers from boundary vertices and every line through a boundary pair. A strict orientation pattern proves an interior crossing of [A₁,A₂] and [A₃,A₄].',
        'Each common-focus curve is individually smooth because its powered-distance difference has a nonzero gradient. The boundary point A₃ lies on one curve and has a strictly positive residual for the other, proving that the two curves are distinct sets. This individual regularity does not assert joint transversality of their intersections.',
        'The original standard-library verifier and rational certificate accompany the proof. Its default command recomputes and compares the complete certificate without writing; integer and Fraction arithmetic decide the signs. The existence argument uses the written distance equivalence, monotone boundary definitions, strict signs and exact face identities.'
    ],
    'limitations': [
        'The fixed boundary crosses. It cannot yield a proper embedding for any choice of central point, and the construction concerns the realization and immersion conventions that permit crossings.',
        'At least five is a lower bound. The exact total for this boundary and a universal maximum are undetermined here. No result for α < 1, root uniqueness within the brackets or joint intersection transversality is asserted.',
        'The note does not establish historical firstness, independence from unknown work or the present worldwide status of stronger questions.'
    ],
    'background': [
        'Melotti–Ramassamy–Thévenin define the α-quad and cube-move realization setting, including crossed faces. Their Remark 4.8 states the common-focus intersection-count expectation addressed by this construction. The Oberwolfach contribution states the corresponding maximum-three conjecture for crossing-permitted α-immersions.',
        'Weighted-distance and pure-power families predate this note. Ash–Bolker study costs φ(|x−P|)+w(P), including a fourth-power example. Their separate oscillatory cost t+k sin(t) is a different example and does not itself settle this pure-power shared-focus count.',
        'Bourne–Peletier–Roper define p-power costs |x−xᵢ|^p−wᵢ in the author manuscript, Definition 4.12; Bourne–Roper also discuss this established family. At p = 16 with weights (0,λ,1), equality of the three costs is exactly the displayed outgoing system. The contribution here is the explicit fixed-boundary count construction, with its incoming witness and face identities.'
    ],
    'collaboration': 'Independent verification, a substantive primary-source comparison or work toward a journal submission would be welcome. Collaboration and authorship would reflect actual contributions.',
    'ai_disclosure': 'AI systems were used extensively in proof exploration, drafting, code generation and adversarial mathematical checks. This is an unrefereed preprint and has not received conventional human peer review. No formal proof-assistant certification is claimed.',
    'reader_intro': 'Read the complete unchanged six-page paper below, open or download the original PDF, or download the complete original verification ZIP. The original standalone TeX is also available separately. The ZIP includes the authored proof and exact verification materials.',
    'rights_notice': 'The note and its original supporting artifacts, including the authored code, are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Cited third-party publications retain their own rights; their full texts are not included.',
    'related_resources': [
        {'label': 'Melotti–Ramassamy–Thévenin: Cube moves for s-embeddings and α-realizations', 'url': 'https://doi.org/10.4171/AIHPD/163', 'context': 'Published 2023 article; Definitions 2.1, 2.4–2.5 and 2.7, Remark 2.8, and Remark 4.8, p. 811.'},
        {'label': 'Melotti: Cube flips in s-embeddings and α-immersions', 'url': 'https://doi.org/10.4171/OWR/2020/35', 'context': 'Oberwolfach Report 35/2020, pp. 1783–1785; maximum-three conjecture on p. 1785.'},
        {'label': 'Ash–Bolker: Generalized Dirichlet tessellations', 'url': 'https://doi.org/10.1007/BF00164401', 'context': '1986 published weighted-distance family, including pure fourth-power and separate oscillatory examples.'},
        {'label': 'Bourne–Peletier–Roper: Hexagonal patterns in a simplified model for block copolymers', 'url': 'https://doi.org/10.1137/130922732', 'context': '2014 publication; author manuscript v2, Definition 4.12, p. 16, gives the p-power family.', 'author_manuscript': 'https://arxiv.org/abs/1305.6540v2'},
        {'label': 'Bourne–Roper: Centroidal power diagrams, Lloyd’s algorithm and applications to optimal location problems', 'url': 'https://doi.org/10.1137/141000993', 'context': '2015 publication; author manuscript v1, Section 1.7, pp. 12–13, describes p-power cells.', 'author_manuscript': 'https://arxiv.org/abs/1409.2786v1'}
    ]
}
write('public-sections.json', sections)
bib = '''@misc{kriebel2026fivecenters,
  author = {Kriebel, Alec},
  title = {Five outgoing centers in a 16-realization cube move},
  year = {2026},
  month = oct,
  day = {15},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23392409},
  url = {https://doi.org/10.5281/zenodo.23392409},
  note = {Unrefereed research note. Manuscript dated 15 October 2026.}
}
'''
(E / 'citation.bib').write_text(bib)
source_binding = {'source_ready_path': str(S / 'SOURCE_READY.json'),
                  'source_ready_SHA256': protocol['source_ready']['SHA256'],
                  'whole_original_source_ready': ready,
                  'whole_original_native_API_objects': native,
                  'whole_original_ordered_transport_receipts': protocol['whole_ordered_transport_receipts'],
                  'native_assets_in_original_order': ready['all_native_assets_in_original_order'],
                  'protocol_path': 'SOURCE_PROTOCOL_BINDINGS.json',
                  'original_objects_historical_flags_preserved': True}
review = {'root_authority': bound('ROOT_CLEARANCE.json'),
          'whole_original_custom_verdicts': original_verdicts,
          'root_primary_reading_scope': authority['root_primary_reading_scope'],
          'role': 'Informed editorial proposal, not a new scientific review.',
          'root_full_copy_config_adoption_pending': True}
publication = dict(sections)
publication.update({
    'schema': 'private-editorial-23392409-v1', 'slug': 'five-outgoing-centers-alpha16',
    'author': 'Alec Kriebel', 'orcid': 'https://orcid.org/0009-0001-9320-500X',
    'abstract': abstract, 'abstract_heading': 'Original abstract', 'abstract_is_original': True,
    'publication_date': '2026-10-15', 'publication_date_label': '15 October 2026',
    'version_field_present': False, 'version': None,
    'printed_version_field_present': False, 'printed_version': None,
    'printed_date': '15 October 2026', 'native_record_created': ready['created'],
    'native_record_updated': ready['updated'],
    'edition_label': 'Zenodo research note dated 15 October 2026',
    'edition_note': 'Neither the native Zenodo metadata nor the manuscript specifies a version number.',
    'doi': ready['DOI'], 'pdf_filename': 'five_centers.pdf', 'pdf_pages': 6,
    'supplement_filename': 'verification-package.zip',
    'supplement_label': 'Complete original verification ZIP',
    'additional_assets': [{'filename': 'five_centers.tex', 'label': 'Original standalone TeX source'}],
    'license': 'CC BY 4.0', 'license_url': 'https://creativecommons.org/licenses/by/4.0/',
    'authored_package_license': 'CC BY 4.0', 'code_license': None,
    'code_license_basis': 'Broad original CC BY4.0 grant includes authored support code; no separate code-specific instrument.',
    'status': 'Unrefereed preprint', 'follow_up': None,
    'canonical_url': None, 'AA': None, 'native_sheet_aa_url': None,
    'proposed_canonical_url': None,
    'keywords': ['α-realizations', 'cube moves', 'common-focus curves', 'weighted-distance bisectors', 'p-power diagrams', 'exact rational interval arithmetic'],
    'seo': {'title': ready['title'] + ' — Alec Kriebel', 'description': sections['description'], 'robots_private_candidate': 'noindex,nofollow,noarchive'},
    'citation_text': 'Alec Kriebel. Five outgoing centers in a 16-realization cube move. Zenodo, 15 October 2026. doi:10.5281/zenodo.23392409.',
    'prepared_bibtex': bib, 'source_binding': source_binding, 'review_metadata': review
})
write('publication.json', publication)
promotion = {
    'record_id': '23392409', 'sheet_row': 130,
    'status': 'PRIVATE_FULL_ORIGINAL_ALPHA16_EDITORIAL_PENDING_ROOT_COPY_ADOPTION',
    'scientific_status_literal_from_root': authority['literal_root_scientific_disposition'],
    'whole_root_scientific_authority': bound('ROOT_CLEARANCE.json'),
    'whole_original_two_scientific_custom_verdicts': original_verdicts,
    'whole_source_binding': source_binding,
    'source_repair': False, 'narrowed_replacement': False, 'follow_up': None,
    'human_peer_review': False, 'formal_certification': False,
    'private_static_candidate_written': True, 'root_full_editorial_adoption_pending': True,
    'rendered_public_copy_approved': False, 'production_integration_authorized': False,
    'ready_to_publish': False, 'installed': False, 'deployed': False,
    'live_verified': False, 'local_http_verified': False, 'browser_verified': False,
    'native_verified': False, 'native_sheet_publication_verified': False,
    'canonical_verified': False, 'public_page_published': False,
    'canonical_url': None, 'AA': None, 'native_sheet_aa_url': None,
    'all203_complete_claimed': False
}
write('promotion.json', promotion)
main = '<main><article>\n<h1>' + html.escape(sections['title']) + '</h1>\n'
main += para('Alec Kriebel · 15 October 2026 · Unrefereed research note')
main += '<p><a href="https://orcid.org/0009-0001-9320-500X">ORCID</a> · <a href="https://doi.org/10.5281/zenodo.23392409">DOI and Zenodo record</a></p>'
main += '<h2>Original abstract</h2>' + para(abstract)
for key, label in [('plain_language', 'Overview'), ('result', 'Result'), ('why_it_works', 'Why it works'), ('limitations', 'Scope'), ('background', 'Background and earlier work')]:
    main += '<h2>' + label + '</h2>' + ''.join(para(x) for x in sections[key])
main += '<h2>Paper and source files</h2>' + para(sections['reader_intro'])
main += '<p><a href="five_centers.pdf">Open PDF</a> · <a href="five_centers.pdf" download>Download PDF</a> · <a href="five_centers.tex" download>TeX source</a> · <a href="verification-package.zip" download>Complete original ZIP</a> · <a href="citation.bib" download>BibTeX</a></p>'
main += '<object data="five_centers.pdf" type="application/pdf" width="100%" height="900" aria-label="Complete six-page paper"><p><a href="five_centers.pdf">Read the complete paper</a></p></object>'
for key, label in [('collaboration', 'Collaboration'), ('ai_disclosure', 'AI assistance and review status'), ('rights_notice', 'License')]:
    main += '<h2>' + label + '</h2>' + para(sections[key])
main += '<p><a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></p><h2>Related literature</h2><ul>'
for ref in sections['related_resources']:
    main += '<li><a href="' + html.escape(ref['url']) + '">' + html.escape(ref['label']) + '</a>. ' + html.escape(ref['context'])
    if 'author_manuscript' in ref:
        main += ' <a href="' + html.escape(ref['author_manuscript']) + '">Author manuscript</a>.'
    main += '</li>'
main += '</ul><h2>Citation</h2>' + para(publication['citation_text']) + '</article></main>\n'
(E / 'PUBLIC_MAIN.html').write_text(main)
scholarly = {'@context': 'https://schema.org', '@type': 'ScholarlyArticle',
             'name': sections['title'], 'headline': sections['title'], 'description': sections['description'],
             'abstract': abstract, 'author': {'@type': 'Person', 'name': 'Alec Kriebel', 'identifier': publication['orcid']},
             'datePublished': '2026-10-15', 'identifier': ready['DOI'],
             'url': 'https://doi.org/' + ready['DOI'], 'creativeWorkStatus': 'Unrefereed preprint',
             'license': publication['license_url'], 'inLanguage': 'en',
             'encoding': {'@type': 'MediaObject', 'encodingFormat': 'application/pdf',
                          'contentUrl': 'https://zenodo.org/records/23392409/files/five_centers.pdf'}}
write('SCHOLARLY_METADATA.json', scholarly)
head = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
head += '<title>' + html.escape(publication['seo']['title']) + '</title><meta name="robots" content="noindex,nofollow,noarchive">'
head += '<meta name="description" content="' + html.escape(sections['description'], quote=True) + '">'
for name, value in [('citation_title', sections['title']), ('citation_author', 'Alec Kriebel'), ('citation_publication_date', '2026/10/15'), ('citation_doi', ready['DOI']), ('citation_pdf_url', 'https://zenodo.org/records/23392409/files/five_centers.pdf')]:
    head += '<meta name="' + name + '" content="' + html.escape(value, quote=True) + '">'
head += '<script type="application/ld+json">' + json.dumps(scholarly, ensure_ascii=False).replace('<', '\\u003c') + '</script>'
head += '<style>body{font-family:Arial,Helvetica,sans-serif;color:#111;background:#fff;max-width:1050px;margin:2rem auto;padding:0 1.25rem;line-height:1.6}h1{line-height:1.2}h2{margin-top:2rem}a{color:#0645ad}object{border:1px solid #ddd}</style></head><body>'
C = E / 'candidate'
C.mkdir()
(C / 'index.html').write_text(head + main + '</body></html>\n')
for asset in ready['all_native_assets_in_original_order']:
    (C / asset['original_api_file_object']['key']).write_bytes(Path(asset['path']).read_bytes())
(C / 'citation.bib').write_bytes((E / 'citation.bib').read_bytes())
md = '# ' + sections['title'] + '\n\nAlec Kriebel · 15 October 2026 · Unrefereed research note\n\n## Original abstract\n\n' + abstract + '\n'
for key in ['plain_language', 'result', 'why_it_works', 'limitations', 'background']:
    md += '\n## ' + key.replace('_', ' ').capitalize() + '\n\n' + '\n\n'.join(sections[key]) + '\n'
for key in ['reader_intro', 'collaboration', 'ai_disclosure', 'rights_notice']:
    md += '\n' + sections[key] + '\n'
md += '\n' + publication['citation_text'] + '\n'
(E / 'PUBLIC_COPY.md').write_text(md)
print(json.dumps({'private_candidate_written': True, 'native_assets_in_original_order': protocol['native_asset_order'], 'canonical_url': None, 'AA': None, 'publication_authority': False}))
