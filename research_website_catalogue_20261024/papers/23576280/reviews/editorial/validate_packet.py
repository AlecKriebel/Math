"""Read-only static checks for the private 23576280 editorial packet.

Prints JSON to stdout. Does not render, fetch, execute source support, or write.
"""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, re, stat, zipfile, zlib
from pypdf import PdfReader

E = Path(__file__).resolve().parent
B = E.parents[1]
P = B.parents[1]
S = B / 'sources'
checks = []

def load(path):
    return json.loads(Path(path).read_text())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check(name, condition, detail=None):
    checks.append({'check': name, 'passed': bool(condition), 'detail': detail})

def bindings(rows, root=None):
    failures = []
    for row in rows:
        path = Path(row['path'])
        if not path.is_absolute():
            path = root / path
        if not path.is_file() or path.stat().st_size != row['bytes'] or sha(path) != row['sha256']:
            failures.append(str(path))
    return failures

pub, pro = load(B/'publication.json'), load(B/'promotion.json')
sb = pub['source_binding']
ready, meta, raw = [load(S/n) for n in ('SOURCE_READY.json', 'normalized-metadata.json', 'record.raw.json')]
transport, intake = [load(S/n) for n in ('api-and-file-receipts.json', 'api-intake-initial-receipts.json')]
baseline = load(E/'ORIGINAL_BINDINGS_BEFORE.json')
check('all_frozen_baseline_files_unchanged', not bindings(baseline['files']), baseline['file_count'])
check('baseline_count_and_unique_paths', len(baseline['files']) == baseline['file_count'] == len({r['path'] for r in baseline['files']}) == 2122)
check('ready_and_final_source_manifests_unchanged', all(not bindings(load(S/n)['files'], S) for n in ('SOURCE_READY_MANIFEST.json','SOURCE_MANIFEST.json')))
check('original_source_package_count', len([p for p in S.rglob('*') if p.is_file()]) == 26)
check('whole_native_source_receipts', sb['source_receipt_original'] == ready == pro['source_receipt_original'])
check('whole_native_metadata', sb['metadata_original'] == meta)
check('whole_native_assets_and_API_file_objects', ready['all_assets'] == meta['all_assets'] == sb['all_assets'] == pro['all_assets'] and raw['files'] == sb['published_file_objects'] == pro['published_file_objects'] == [a['original_api_file_object'] for a in ready['all_assets']])
check('exact_distinct_transport_lists', sb['transport_receipt_original'] == transport == pro['transport_receipt_original'] and sb['initial_intake_receipt_original'] == intake == pro['initial_intake_receipt_original'] and len(transport) == 4 and len(intake) == 1)
check('genuine_transport_keys_retained', all(set(r) == {'requested_url','started_utc','completed_utc','status','final_url','headers','path','bytes','sha256'} and r['status'] == 200 and isinstance(r['headers'],dict) for r in transport + intake))
check('no_source_aliases', not any((S/n).exists() for n in ('receipt.json','record.json','api-receipts.json')))
assets = ready['all_assets']
check('ZIP_then_PDF_asset_order', [a['original_api_file_object']['key'] for a in assets] == [pub['supplement_filename'],pub['pdf_filename']])
for a in assets:
    path, api = Path(a['path']), a['original_api_file_object']
    check('asset_' + api['key'], path.stat().st_size == a['bytes'] == api['size'] and sha(path) == a['sha256'] and hashlib.md5(path.read_bytes()).hexdigest() == a['md5'] == api['checksum'].removeprefix('md5:'))
for key in ('metadata','raw_record','source_receipt','recursive_archive_inventory','transport_receipt','initial_intake_receipt','source_tex','prepared_bibtex'):
    check('config_binding_' + key, sha(B/sb[key+'_path']) == sb[key+'_sha256'])
pdf = S / pub['pdf_filename']
check('complete_selected_reader', len(PdfReader(pdf).pages) == pub['pdf_pages'] == ready['PDF_pages'] == 6 and sha(pdf) == pro['pdf_sha256'] == sb['pdf_sha256'])
inventory = load(S/'archive-members.json')
archive_ok, details = True, []
with zipfile.ZipFile(S/pub['supplement_filename']) as z:
    infos = z.infolist()
    check('archive_all_CRCs', z.testzip() is None)
    check('complete_archive_member_counts', len(infos) == len(inventory['files']) == inventory['safe_all_depth_members'] == 12 and inventory['expanded_bytes'] == 184923 and not inventory['nested_archives'])
    table = {r['member']: r for r in inventory['files']}
    for info in infos:
        parts = PurePosixPath(info.filename)
        safe = not parts.is_absolute() and '..' not in parts.parts and '\\' not in info.filename and not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG)
        data = z.read(info)
        r = table[info.filename]
        good = safe and not r['archive_chain'] and len(data) == r['bytes'] == info.file_size and hashlib.sha256(data).hexdigest() == r['sha256'] and zlib.crc32(data) == info.CRC and f'{info.CRC:08x}' == r['CRC32'] and data == (S/r['path']).read_bytes()
        archive_ok &= good
        details.append({'member': info.filename, 'safe_CRC_hash_extracted_bytes_equal': good})
    check('embedded_PDF_exactly_one_identical_reader', [i.filename for i in infos if i.filename.lower().endswith('.pdf')] == ['paper.pdf'] and z.read('paper.pdf') == pdf.read_bytes())
check('all_original_archive_bodies_authenticated_without_reextracting', archive_ok, details)
check('complete_original_ZIP_binding', sha(S/pub['supplement_filename']) == pro['supplement_sha256'] == sb['supplement_sha256'])
tex = (B/sb['source_tex_path']).read_text()
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)
normalized = abstract.replace(r'Seb\H{o}', 'Sebő').replace('Benchetrit--','Benchetrit–').replace(r'\(','').replace(r'\)','').replace(r'\beta','β').replace(r'\ge','≥')
normalized = ' '.join(normalized.split())
check('full_original_abstract_exact_source_and_only_declared_typography_normalization', (E/'ORIGINAL_ABSTRACT.tex').read_text() == abstract == sb['abstract_tex'] and pub['abstract'] == normalized and pub['abstract_is_original'] is True and pub['abstract_heading'] == 'Original abstract')
check('full_actual_reader_text_retained', all(page.extract_text().strip() in (E/'ACTUAL_MANUSCRIPT_READ.txt').read_text() for page in PdfReader(pdf).pages))
check('exact_version_date_DOI_author', pub['version'] == sb['version'] == ready['version'] == meta['version'] == pro['version'] == '1.0.0' and pub['publication_date'] == ready['publication_date'] == '2026-10-22' and pub['doi'] == raw['doi'] == '10.5281/zenodo.23576280' and pub['author'] == 'Alec Kriebel' and pub['orcid'] == 'https://orcid.org/0009-0001-9320-500X')
check('prepared_BibTeX_exact', pub['prepared_bibtex'] == (E/'CITATION.bib').read_text() and all(x in pub['prepared_bibtex'] for x in ('version = {1.0.0}', 'date = {2026-10-22}', 'doi = {10.5281/zenodo.23576280}', 'author = {Kriebel, Alec}', '0009-0001-9320-500X')))
clearance_path = P/pro['root_clearance_file']
authority = load(clearance_path)
check('separate_existing_root_scientific_authority', sha(clearance_path) == pro['root_clearance_sha256'] == pub['review_metadata']['root_clearance_sha256'] == '1135fe54724927c75d2e03e4fa15b61fc294bd90611c3a92f273c4e18a1a6e7e' and authority == pro['root_clearance_record'] and pro['status'] == authority['status'] == 'PASS' and pro['disposition_by'] == authority['disposition_by'] == 'root')
for lane, entry in pro['reviews'].items():
    check('whole_original_' + lane + '_verdict_and_root_entry', entry['verdict'] == load(B/entry['verdict_file']) and sha(B/entry['verdict_file']) == entry['verdict_sha256'] and sha(B/entry['report']) == entry['report_sha256'] and entry['root_authority_entry'] == authority['reviews'][lane])
check('publication_hash_matches_promotion', pro['publication_sha256'] == sha(B/'publication.json'))
gates = ('rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received')
check('all_later_gates_false', all(obj[k] is False for obj in (pro,pub['review_metadata']) for k in gates) and pub['review_metadata']['rendered'] is False and pub['review_metadata']['deployed'] is False)
check('followup_canonical_AA_null', all(obj[k] is None for obj in (pub,pro) for k in ('follow_up','canonical_url','AA')) and pro['native_sheet_aa_url'] is None and pub['review_metadata']['native_sheet_aa_url'] is None)
copies = load(E/'ORIGINAL_OBJECT_COPIES.json')['copies']
check('eleven_whole_verbatim_original_copies', len(copies) == 11 and all(Path(r['original']['path']).read_bytes() == Path(r['verbatim_private_copy']['path']).read_bytes() and r['original']['sha256'] == r['verbatim_private_copy']['sha256'] for r in copies))
copy, sections, prose = (E/'PUBLIC_COPY.md').read_text(), load(E/'public-sections.json'), load(E/'public-prose.json')
check('whole_public_config_prose_matches_private_draft', all(prose[k] == pub[k] for k in prose) and all(x in copy for k in ('plain_language','result','why_it_works','limitations') for x in pub[k]) and all(pub[k] in copy for k in ('abstract','status','ai_disclosure','edition_note','reader_intro','collaboration')) and all(x['title'] in copy and x['url'] in copy and x['note'] in copy for x in pub['background']))
check('section_arrays_preserve_all_paragraphs', all(sections[k] == pub[k] for k in ('plain_language','result','why_it_works','limitations','background')) and sections['abstract'] == [pub['abstract']] and sections['status'] == [pub['status'],pub['ai_disclosure'],pub['edition_note']] and sections['collaboration'] == [pub['collaboration']] and sections['follow_up'] is None)
check('later_Ferudun_positive_link_and_limits', any(x['url'] == 'https://doi.org/10.5281/zenodo.23592264' and 'Alper Ferudun' in x['title'] and '3-SAT' in x['note'] and '23 October' in x['note'] and '22 October' in x['note'] and 'does not certify' in x['note'] for x in pub['background']))
check('public_no_private_hash_or_review_narrative', not re.search(r'\b[0-9a-f]{64}\b',copy) and not any(x in copy for x in ('SOURCE_READY','root-clearance','root review','PASS','2,122','2122','08:44','EARLY_SEAL')))
check('no_public_followup', '## Follow' not in copy and pub['follow_up'] is None)
check('one_full_reader_complete_ZIP_and_four_future_files_only', pub['additional_assets'] == [] and load(E/'METADATA_READER_SUPPORT_REQUIREMENTS.json')['future_article_files'] == ['index.html',pub['pdf_filename'],pub['supplement_filename'],'citation.bib'] and sb['public_page_reader_pdf_count'] == sb['total_distinct_reader_pdf_count'] == 1 and sb['archive_embedded_pdf_count'] == 1)
check('no_rendered_article_or_source_alias_created', not list(E.rglob('*.html')) and not (B/'index.html').exists() and not any((S/n).exists() for n in ('receipt.json','record.json')))
check('consumer_specification_explicitly_pending', 'does not install a source helper' in (E/'SCHEMA_ADAPTER.md').read_text() and 'require separately authorized work' in (E/'SCHEMA_ADAPTER.md').read_text())
result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'record_id':23576280, 'kind':'PRIVATE_EDITORIAL_STATIC_VALIDATION_ONLY', 'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL', 'checks_count':len(checks), 'checks':checks, 'no_render_HTTP_UI_Git_source_execution_or_writes_by_this_validator':True, 'publication_authority':False}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result['status'] == 'PASS' else 1)
