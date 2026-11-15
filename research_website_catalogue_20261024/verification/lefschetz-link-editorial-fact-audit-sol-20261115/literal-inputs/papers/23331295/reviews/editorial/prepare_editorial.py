"""New private editorial authoring only. No source programmes or external writes."""
from pathlib import Path
import hashlib
import html
import json


def need(value, message):
    if not value: raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()
def esc(value): return html.escape(str(value), quote=True)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def render(pub):
    schema = {'@context': 'https://schema.org', '@type': 'ScholarlyArticle', 'headline': pub['title'], 'name': pub['title'],
        'description': pub['description'], 'abstract': pub['abstract'],
        'author': {'@type': 'Person', 'name': pub['author'], 'sameAs': pub['orcid']},
        'datePublished': pub['publication_date'], 'version': pub['version'],
        'creativeWorkStatus': 'Unrefereed preprint', 'identifier': {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': pub['doi']},
        'sameAs': 'https://doi.org/' + pub['doi'], 'license': pub['license_url'], 'keywords': pub['keywords'],
        'encoding': [{'@type': 'MediaObject', 'encodingFormat': a['whole_original_native_files_entry']['mimetype'],
            'contentUrl': a['original_api_file_object']['links']['self']} for a in pub['source_binding']['native_assets_in_original_order']]}
    css = 'body{font-family:Arial,Helvetica,sans-serif;color:#111;background:#fff;max-width:900px;margin:0 auto;padding:26px 20px;line-height:1.6}h1{line-height:1.2;font-size:2rem}h2{line-height:1.3;margin-top:2rem;font-size:1.3rem}p,a{overflow-wrap:anywhere}a{color:#24558b}.paper-pdf{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;border:1px solid #ccc;box-sizing:border-box}li{margin:.5em 0}@media(max-width:600px){body{padding:20px 15px}h1{font-size:1.6rem}}'
    head = '<!DOCTYPE html>\n<html lang="en">\n<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>' + esc(pub['seo']['title']) + '</title>'
    for key, value in [('description', pub['description']), ('citation_title', pub['title']), ('citation_author', pub['author']),
        ('citation_author_orcid', pub['orcid']), ('citation_publication_date', pub['publication_date'].replace('-', '/')),
        ('citation_version', pub['version']), ('citation_doi', pub['doi']), ('citation_pdf_url', 'assets/' + pub['pdf_filename'])]:
        head += '<meta name="' + key + '" content="' + esc(value) + '">'
    head += '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('</', '<\/') + '</script><style>' + css + '</style></head>\n'
    main = '<main><article><header><h1>' + esc(pub['title']) + '</h1><p>Alec Kriebel · <a href="' + esc(pub['orcid']) + '">ORCID 0009-0001-9320-500X</a></p><p>12 October 2026 · Zenodo version 1.0 · Unrefereed preprint</p><p>' + esc(pub['edition_note']) + '</p></header>'
    def section(identifier, title, paragraphs):
        return '<section id="' + identifier + '"><h2>' + title + '</h2>' + ''.join('<p>' + esc(p) + '</p>' for p in paragraphs) + '</section>'
    main += section('abstract', 'Original abstract', [pub['abstract']])
    for key, title in [('plain_language', 'What the result means'), ('result', 'The full result'), ('why_it_works', 'Why the obstruction works'), ('limitations', 'Scope and limitations'), ('background', 'Background and credit')]:
        main += section(key.replace('_', '-'), title, pub[key])
    main += section('collaboration', 'Contribution and collaboration', [pub['collaboration']])
    main += section('status', 'AI and review disclosure', [pub['ai_disclosure']])
    links = '<p><a href="assets/nullstellensatz.pdf" target="_blank" rel="noopener">Open original PDF</a> · <a href="assets/nullstellensatz.pdf" download>Download PDF</a> · <a href="assets/citation.bib" download>BibTeX</a> · <a href="https://doi.org/' + pub['doi'] + '">Zenodo record and DOI</a></p>'
    native = '<ul>' + ''.join('<li><a href="assets/' + esc(a['original_api_file_object']['key']) + '" download>' + esc(label) + '</a> · <a href="' + esc(a['original_api_file_object']['links']['self']) + '">Original Zenodo file</a></li>' for a, label in zip(pub['source_binding']['native_assets_in_original_order'], ['Original standalone TeX source', 'Complete original proof and verification ZIP', 'Complete original four-page PDF'])) + '</ul>'
    frame = '<iframe class="paper-pdf" loading="lazy" src="assets/nullstellensatz.pdf#view=FitH" title="' + esc(pub['title']) + ' — complete four-page PDF"></iframe>'
    main += '<section id="read"><h2>Read and download</h2><p>' + esc(pub['reader_intro']) + '</p>' + links + native + frame + '</section>'
    main += section('cite', 'Citation', [pub['citation_text']])
    main += '<section id="primary-background"><h2>Primary background</h2><ul>' + ''.join('<li><a href="' + esc(r['url']) + '">' + esc(r['title']) + '</a></li>' for r in pub['related_resources']) + '</ul></section>'
    main += '<section id="rights"><h2>Rights</h2><p>' + esc(pub['rights_notice']) + '</p><p><a href="' + esc(pub['license_url']) + '">Creative Commons Attribution 4.0 International</a></p></section>'
    main += '</article></main>'
    return head + '<body>\n' + main + '\n</body>\n</html>\n', main


def main():
    root = Path(__file__).resolve().parent
    need(root.name == 'editorial' and root.parent.parent.name == '23331295', 'owned editorial root only')
    draft = json.loads((root / 'DRAFT_SECTIONS.json').read_bytes()); protocol = json.loads((root / 'SOURCE_PROTOCOL_BINDINGS.json').read_bytes())
    ready = protocol['whole_original_SOURCE_READY']['whole_literal_object']; authority = protocol['whole_root_scientific_authority']['whole_literal_object']
    need(ready['record_id'] == 23331295 and ready['version'] == '1.0' and authority['printed_version'] is None, 'actual native/printed version distinction')
    need([a['original_api_file_object']['key'] for a in ready['all_native_assets_in_original_order']] == ['nullstellensatz.tex', 'verification-package.zip', 'nullstellensatz.pdf'], 'native TeX ZIP PDF order')
    pub = dict(draft)
    pub.update({'schema': 'private-editorial-23331295-v1', 'author': 'Alec Kriebel', 'orcid': 'https://orcid.org/0009-0001-9320-500X',
        'abstract': protocol['actual_source_manuscript_and_companion_read']['entire_original_abstract_rendered_plain'], 'abstract_heading': 'Original abstract', 'abstract_is_original': True,
        'publication_date': '2026-10-12', 'publication_date_label': '12 October 2026', 'version': '1.0', 'version_field_present': True,
        'printed_date': '12 October 2026', 'printed_version': None, 'printed_version_field_present': False,
        'native_record_created': ready['created'], 'native_record_updated': ready['updated'], 'created_updated_not_substituted_for_publication_date': True,
        'edition_label': 'Zenodo version 1.0', 'edition_note': 'The manuscript is dated 12 October 2026 and prints no version number; 1.0 is the Zenodo version.',
        'doi': ready['DOI'], 'pdf_filename': 'nullstellensatz.pdf', 'pdf_pages': 4, 'supplement_filename': 'verification-package.zip',
        'supplement_label': 'Complete original proof and verification ZIP', 'additional_assets': [{'filename': 'nullstellensatz.tex', 'label': 'Original standalone TeX source', 'mimetype': 'application/x-tex', 'native_ordinal_zero_based': 0}],
        'license': 'CC BY 4.0', 'license_url': 'https://creativecommons.org/licenses/by/4.0/', 'authored_package_license': 'CC BY 4.0', 'code_license': None,
        'code_license_basis': 'Actual README grants broad CC BY4.0 to the authored package including code; no separate code-specific instrument or MIT default.',
        'status': 'Unrefereed preprint', 'follow_up': None, 'followup_rationale': 'No source-supported followup meeting the programme significance bar is proposed.',
        'canonical_url': None, 'AA': None, 'native_sheet_aa_url': None, 'proposed_canonical_url': 'https://aleckriebel.com/research/' + draft['slug'] + '/',
        'keywords': ['finite-type link invariants', 'Vassiliev invariants', 'actual-link zero sets', 'radical ideals', 'twist-restriction polynomial', 'Bar-Natan Problem 2.27', 'whole-algebra character']})
    pub['seo'] = {'title': pub['title'] + ' | Alec Kriebel', 'description': pub['description'], 'robots_private_candidate': 'noindex,nofollow'}
    pub['citation_text'] = 'Alec Kriebel. ' + pub['title'] + '. Zenodo version 1.0, 12 October 2026. doi:' + pub['doi'] + '.'
    pub['prepared_bibtex'] = '@misc{kriebel2026actuallinknullstellensatz,\n  author = {Kriebel, Alec},\n  title = {' + pub['title'] + '},\n  year = {2026},\n  month = oct,\n  day = {12},\n  version = {1.0},\n  publisher = {Zenodo},\n  doi = {' + pub['doi'] + '},\n  url = {https://doi.org/' + pub['doi'] + '},\n  note = {Unrefereed preprint. Zenodo version 1.0; manuscript dated 12 October 2026 without a printed version number.}\n}\n'
    sb = {'source_ready_path': protocol['whole_original_SOURCE_READY']['path'], 'source_ready_SHA256': protocol['whole_original_SOURCE_READY']['SHA256'],
        'whole_original_source_ready': ready, 'whole_original_native_API_objects': protocol['whole_original_native_API_objects'],
        'whole_original_eight_ordered_transport_objects': protocol['whole_original_eight_ordered_transport_objects'],
        'whole_original_native_schema_types': protocol['whole_original_NATIVE_SCHEMA_TYPES'], 'whole_original_archive_custody': protocol['whole_original_ARCHIVE_CUSTODY'],
        'whole_original_queue_binding': protocol['whole_original_QUEUE_BINDING'], 'whole_original_native_sheet_identity_subset': protocol['whole_original_native_sheet_identity_subset'],
        'native_assets_in_original_order': ready['all_native_assets_in_original_order'], 'standalone_control_TeX_byte_identical': True,
        'embedded_PDFs': ready['embedded_PDFs'], 'source_protocol_binding_path': str(root / 'SOURCE_PROTOCOL_BINDINGS.json'),
        'source_protocol_binding_SHA256': sha((root / 'SOURCE_PROTOCOL_BINDINGS.json').read_bytes()), 'historical_unread_null_flags_not_normalized': True}
    pub['source_binding'] = sb
    pub['review_metadata'] = {'root_scientific_authority': protocol['whole_root_scientific_authority'],
        'whole_original_two_scientific_custom_verdicts': protocol['whole_original_two_scientific_custom_verdicts'],
        'new_root_primary_access_update_separate_from_immutable_peer_limits': protocol['new_root_Stoimenow_finding_separate_from_immutable_peer_limits'],
        'editorial_role': 'Informed editorial preparation after root full science; not a fresh independent science review.', 'root_full_copy_config_adoption_pending': True}
    promotion = {'record_id': '23331295', 'sheet_row': 128, 'status': 'PRIVATE_FULL_ORIGINAL_PRINCIPAL_IDEAL_EDITORIAL_PENDING_ROOT_COPY_ADOPTION',
        'scientific_status_literal_from_root': authority['root_scientific_disposition'], 'whole_root_scientific_authority': protocol['whole_root_scientific_authority'],
        'whole_original_two_scientific_custom_verdicts': protocol['whole_original_two_scientific_custom_verdicts'], 'whole_source_binding': sb,
        'new_root_primary_access_update_separate_from_immutable_peer_limits': protocol['new_root_Stoimenow_finding_separate_from_immutable_peer_limits'],
        'source_repair': False, 'narrowed_replacement': False, 'follow_up': None, 'human_peer_review': False, 'formal_certification': False,
        'private_static_candidate_written': True, 'root_full_editorial_adoption_pending': True, 'rendered_public_copy_approved': False,
        'production_integration_authorized': False, 'ready_to_publish': False, 'installed': False, 'deployed': False, 'live_verified': False,
        'local_http_verified': False, 'browser_verified': False, 'native_verified': False, 'native_sheet_publication_verified': False,
        'canonical_verified': False, 'public_page_published': False, 'canonical_url': None, 'AA': None, 'native_sheet_aa_url': None,
        'proposed_canonical_url': pub['proposed_canonical_url'], 'all203_complete_claimed': False}
    candidate = root / 'candidate'; assets = candidate / 'assets'; assets.mkdir(parents=True, exist_ok=True)
    for a in ready['all_native_assets_in_original_order']:
        raw = Path(a['path']).read_bytes(); need(len(raw) == a['bytes'] and sha(raw) == a['SHA256'], 'complete original asset binding')
        (assets / a['original_api_file_object']['key']).write_bytes(raw)
    (root / 'citation.bib').write_text(pub['prepared_bibtex']); (assets / 'citation.bib').write_text(pub['prepared_bibtex'])
    page, body = render(pub); (candidate / 'index.html').write_text(page); (root / 'PUBLIC_MAIN.html').write_text(body + '\n')
    write_json(root / 'publication.json', pub); write_json(root / 'promotion.json', promotion)
    public = '# ' + pub['title'] + '\n\nAlec Kriebel · [ORCID](' + pub['orcid'] + ')\n\n12 October 2026 · Zenodo version 1.0 · Unrefereed preprint\n\n' + pub['edition_note'] + '\n\n## Original abstract\n\n' + pub['abstract'] + '\n'
    for key, title in [('plain_language', 'What the result means'), ('result', 'The full result'), ('why_it_works', 'Why the obstruction works'), ('limitations', 'Scope and limitations'), ('background', 'Background and credit')]:
        public += '\n## ' + title + '\n\n' + '\n\n'.join(pub[key]) + '\n'
    for title, value in [('Contribution and collaboration', pub['collaboration']), ('AI and review disclosure', pub['ai_disclosure']), ('Read and download', pub['reader_intro'])]: public += '\n## ' + title + '\n\n' + value + '\n'
    public += '\n[Open original PDF](assets/nullstellensatz.pdf) · <a href="assets/nullstellensatz.pdf" download>Download PDF</a> · [BibTeX](assets/citation.bib) · [Zenodo and DOI](https://doi.org/' + pub['doi'] + ')\n\n'
    for a, label in zip(ready['all_native_assets_in_original_order'], ['Original standalone TeX', 'Complete original proof and verification ZIP', 'Complete original four-page PDF']): public += '- [' + label + '](assets/' + a['original_api_file_object']['key'] + ')\n'
    public += '\n<iframe src="assets/nullstellensatz.pdf#view=FitH" title="Complete four-page PDF" width="100%" height="850" loading="lazy"></iframe>\n\n## Citation\n\n' + pub['citation_text'] + '\n\n## Primary background\n\n'
    for r in pub['related_resources']: public += '- [' + r['title'] + '](' + r['url'] + ')\n'
    public += '\n## Rights\n\n' + pub['rights_notice'] + '\n\n[Creative Commons Attribution 4.0 International](' + pub['license_url'] + ')\n'; (root / 'PUBLIC_COPY.md').write_text(public)
    write_json(root / 'public-sections.json', {k: pub[k] for k in ['abstract', 'plain_language', 'result', 'why_it_works', 'limitations', 'background', 'collaboration', 'ai_disclosure', 'reader_intro', 'rights_notice']})
    print(json.dumps({'literal_custom_status': 'PRIVATE_EDITORIAL_ARTIFACTS_PREPARED_ONLY', 'owned_root': str(root), 'native_assets_copied': 3,
        'native_order': ['TeX', 'ZIP', 'PDF'], 'source_programmes_run': False, 'production_or_paper_level_configs_modified': False}, indent=2))


if __name__ == '__main__':
    main()
