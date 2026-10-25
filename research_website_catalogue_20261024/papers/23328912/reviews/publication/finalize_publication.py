"""Bind two root-cleared drafts; never render or mutate shared/site files."""
from pathlib import Path
import datetime, hashlib, json, re, zipfile

R = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
IDS = ('23328912', '23524971')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):
    return json.loads(path.read_text())
def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def normalized_abstract(rid, body):
    if rid == '23328912':
        body = body.replace(r'\CAT', 'CAT').replace(r'\mapsto', '→').replace('$', '').replace('~', ' ')
    else:
        body = body.replace('birth--death', 'birth–death')
    return ' '.join(body.split())

utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
shared = [R/'scripts/render_page.py', R/'verification/final-content-check.py']
shared_before = {str(x.relative_to(R)): sha(x) for x in shared}
for rid in IDS:
    p = R/'papers'/rid
    out = p/'reviews/publication'
    draft = out/'publication.draft.json'
    c = read(draft)
    clearance_path = R/f'verification/root-clearance-{rid}-20261025.json'
    clearance = read(clearance_path)
    receipt = read(p/'sources/receipt.json')
    record = read(p/'sources/record.json')
    assert clearance['record_id'] == rid and clearance['status'] == 'PASS'
    assert clearance['disposition_by'] == 'root'
    assert sha(p/'sources/receipt.json') == clearance['source_receipt_sha256'] == c['source_binding']['receipt_sha256']
    assert sha(p/'sources/record.json') == c['source_binding']['record_sha256']
    assert c['title'] == record['metadata']['title']
    assert c['version'] == record['metadata']['version'] == '1.0'
    assert c['doi'] == record['metadata']['doi']
    assert c['publication_date'] == record['metadata']['publication_date']
    assert c['source_binding']['record_created_utc'] == record['created']
    assets = {}
    for asset in receipt['files']:
        name = asset.get('name', asset.get('filename'))
        path = p/'sources'/name
        assert sha(path) == asset['sha256'] and path.stat().st_size == asset['bytes']
        assert hashlib.md5(path.read_bytes()).hexdigest() == asset['md5']
        if name.endswith('.zip'):
            with zipfile.ZipFile(path) as z:
                assert z.testzip() is None
        assets[name] = asset
    assert sha(p/'sources'/c['pdf_filename']) == clearance['pdf_sha256']
    source_path = p/c['source_binding']['source_tex_path']
    source = source_path.read_text()
    assert sha(source_path) == c['source_binding']['source_tex_sha256']
    abstract_raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', source, re.S).group(1)
    assert normalized_abstract(rid, abstract_raw) == c['abstract']
    assert (out/'abstract_original.txt').read_text().strip() == c['abstract']
    assert len(c['abstract'].split()) == {'23328912':97, '23524971':124}[rid]
    assert c['follow_up'] is None
    reviews = {}
    for family, binding in clearance['reviews'].items():
        report = R/binding['report']
        verdict = R/binding['verdict']
        assert sha(report) == binding['report_sha256']
        assert sha(verdict) == binding['verdict_sha256']
        reviews[family] = {
            'report': str(report.relative_to(p)), 'sha256': sha(report),
            'verdict_file': str(verdict.relative_to(p)), 'verdict_sha256': sha(verdict),
            'verdict': read(verdict),
            'root_disposition': 'SCOPE_COMPLETE' if family == 'scope' else 'PASS',
        }
    assert set(reviews) == {'analytic','adversarial','scope'}
    assert reviews['scope']['verdict'].get('mathematical_verdict') is None
    for flag in ('candidate_only', 'candidate_gate'):
        c.pop(flag, None)
    c['publication_date_label'] = 'Manuscript dated'
    c['edition_label'] = 'Zenodo version 1.0'
    c['citation_edition_label'] = 'Zenodo version 1.0'
    day, created_day = ('12 October 2026','13 October 2026') if rid == '23328912' else ('20 October 2026','21 October 2026')
    c['edition_note'] = (
        f'The manuscript and Zenodo publication-date metadata are dated {day}. '
        f'Zenodo records this version as created on {created_day} (UTC). '
        'The displayed date is the manuscript date, not verified public availability on that date. '
        'Neither date establishes first priority. Version 1.0 is the Zenodo version; the manuscript does not print a version number.'
    )
    c['bibtex_note'] = f'Unrefereed preprint; Zenodo version 1.0; manuscript dated {day}; Zenodo record created {created_day} UTC'
    if rid == '23328912':
        assert r'\date{October 12, 2026}' in source
        c['supplement_filename'] = None
        for asset in c['additional_assets']:
            asset['kind'] = 'zip'
        candidate = 'reviews/scope/CONTENT_CANDIDATE.md'
    else:
        assert r'\date{20 October 2026\\\small Unrefereed preprint draft}' in source
        c['supplement_filename'] = 'dfc_stability_verification.zip'
        c['supplement_label'] = 'Source and verification package (ZIP)'
        c['additional_assets'] = []
        candidate = 'reviews/scope/content.json'
    supplement_sha = assets[c['supplement_filename']]['sha256'] if c['supplement_filename'] else None
    c['source_binding'].update({
        'files': receipt['files'],
        'source_receipt_sha256': sha(p/'sources/receipt.json'),
        'supplement_sha256': supplement_sha,
        'abstract_source': str(source_path.relative_to(p)),
        'abstract_source_sha256': sha(source_path),
        'abstract_word_count': len(c['abstract'].split()),
        'abstract_normalization': 'Complete original abstract; TeX mathematical typography and whitespace normalized without dropping sentences. Apostrophe retained; birth--death normalized to birth–death in DFC.',
        'embedded_assets': [],
        'frozen_scope_content_path': candidate,
        'frozen_scope_content_sha256': sha(p/candidate),
        'publication_state': 'BINDINGS_READY_RENDERING_PENDING',
        'review_boundary': 'Exact unchanged original review verdicts are retained in promotion.json. Scope-only pending language remains frozen; the subsequent root clearance approves the exact scientific scope. These are internal AI reviews, not external human peer review or proof-assistant certification.',
    })
    c['review_metadata'] = {
        'prepared_utc': utc, 'completion_percent': 100,
        'scientific_clearance_received': True,
        'root_clearance_file': str(clearance_path.relative_to(R)),
        'root_clearance_sha256': sha(clearance_path),
        'publication_state': 'BINDINGS_READY_RENDERING_PENDING',
        'rendered': False, 'deployed': False,
        'editor_authorization': 'Parent authorized paper-specific publication and promotion bindings only; rendering, shared checker edits, deployment, browser and tracker actions remain with root.',
    }
    save(p/'publication.json', c)
    gate = {
        'record_id': rid, 'status': 'PASS', 'disposition_by': 'root', 'created_utc': utc,
        'approved_scope': clearance['approved_scope'],
        'root_clearance': clearance['authorization'],
        'root_clearance_file': str(clearance_path.relative_to(R)),
        'root_clearance_sha256': sha(clearance_path),
        'root_clearance_record': clearance,
        'pdf_sha256': clearance['pdf_sha256'], 'supplement_sha256': supplement_sha,
        'publication_sha256': sha(p/'publication.json'),
        'source_receipt_sha256': sha(p/'sources/receipt.json'), 'source_files': receipt['files'],
        'reviews': reviews, 'scope_gate_resolution': clearance['scope_gate_resolution'],
        'source_repair': False, 'human_peer_review': False, 'formal_machine_verification': False,
        'follow_up': None,
        'preparation_state': 'BINDINGS_READY_RENDERING_PENDING',
    }
    save(p/'promotion.json', gate)
    save(out/'binding-check.json', {
        'utc': utc, 'status': 'PASS_PREPARATION_BINDINGS_ONLY', 'completion_percent': 100,
        'record_id': rid, 'publication_sha256': sha(p/'publication.json'),
        'promotion_sha256': sha(p/'promotion.json'), 'original_draft_sha256': sha(draft),
        'all_public_assets_size_md5_sha256_verified': True,
        'all_public_zip_crc_verified': True,
        'complete_original_abstract_text_match': True,
        'abstract_word_count': len(c['abstract'].split()),
        'source_date_and_metadata_checked': True,
        'all_three_exact_review_objects_and_hashes_bound': True,
        'root_clearance_exact_object_and_hash_bound': True,
        'scope_original_pending_language_preserved': True,
        'source_assets_count': len(assets), 'reader_pages': 6,
        'shared_files_readonly_observed': shared_before,
        'rendered_page_content_check': 'PENDING', 'desktop_mobile_pdf_browser_qa': 'PENDING',
        'live_deployment': 'PENDING', 'spreadsheet_url': 'NOT_WRITTEN',
    })
    (out/'FINALIZATION_LOG.md').write_text(
        '# Publication binding finalization\n\n'
        f'- {utc} — 100% of the assigned paper-specific binding preparation complete. '
        'Rechecked the full original abstract, printed date, metadata date/version/creation timestamp, all public asset size/MD5/SHA-256 and ZIP CRC, source TeX, frozen scope candidate, all three report/verdict hashes, and exact root clearance. '
        'Original drafts, preflight manifests, reviews and source bytes preserved.\n'
        '- The original scope verdict remains scope-only; root’s later decision is recorded separately. '
        'No new mathematical review verdict is issued here.\n'
        '- Publication and promotion JSON are ready for root review. No rendering, site/shared checker change, Git, deployment, browser, Sheet or outreach action was taken. '
        'Live publication is not complete.\n'
    )
assert {str(x.relative_to(R)):sha(x) for x in shared} == shared_before
print(json.dumps({rid: {'publication':sha(R/'papers'/rid/'publication.json'), 'promotion':sha(R/'papers'/rid/'promotion.json')} for rid in IDS}, indent=2))
