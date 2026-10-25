from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile

B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for id in ('23410944', '23422055'):
    p = B/id
    s = p/'sources'
    q = p/'reviews/scope'
    c = json.loads((q/'content.json').read_text())
    integrity = json.loads((q/'source_integrity.json').read_text())
    assert integrity['passed']
    assert c['follow_up'] is None and c['additional_assets'] == []
    assert c['publication_date'] == c['source_binding']['publication_date']
    assert c['version'] == c['source_binding']['zenodo_version'] == '1.0'
    assert c['pdf_filename'] in {f['name'] for f in c['source_binding']['files']}
    assert c['supplement_filename'] in {f['name'] for f in c['source_binding']['files']}
    assert c['source_binding']['reviewed_documents'][0]['pages'] == integrity['main_pdf_pages']
    z = zipfile.ZipFile(s/c['supplement_filename'])
    manifest = json.loads(z.read(integrity['top_level_manifest']))['files']
    if isinstance(manifest, dict):
        manifest = [dict(path=k, **v) for k,v in manifest.items()]
    count = 0
    for f in manifest:
        local = s/'published-source'/f['path']
        assert local.is_file(), local
        assert hashlib.sha256(local.read_bytes()).hexdigest() == f['sha256'], local
        count += 1
    integrity['extracted_manifest_files_verified'] = count
    integrity['extracted_file_check_boundary'] = 'All manifest-bound extraction bytes checked; no review content interpreted.'
    (q/'source_integrity.json').write_text(json.dumps(integrity,indent=2)+'\n')
    v = dict(record_id=id, role='independent_publication_scope_and_primary_literature_review',
             timestamp_utc=datetime.now(timezone.utc).isoformat(), completion_percent=100,
             scope_verdict='no_publication_scope_defect_identified',
             publication_disposition='candidate_content_only_pending_separate_mathematical_gates',
             mathematical_gate=False, novelty_certified=False, independent_human_peer_review=False,
             full_published_paper_read=True, published_paper_pages=integrity['main_pdf_pages'],
             published_supplement_pdfs=[], all_published_assets_acquired=True, source_integrity_pass=True,
             archived_or_sibling_review_verdicts_used=False,
             independence_note='Own scope conclusion recorded at the 60% checkpoint. No dedicated archived or sibling mathematical review opinions consulted. Historical author status and AI-review assertions in the published paper and original authored proof were encountered but not adopted as validation. ZIP/manifest hash checks do not interpret archived verdicts.',
             content_sha256=hashlib.sha256((q/'content.json').read_bytes()).hexdigest(),
             source_binding=c['source_binding'], follow_up=None, followup_rationale=c['followup_rationale'],
             defects=[], key_boundaries=c['limitations'])
    (q/'verdict.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
    with (q/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n## '+datetime.now(timezone.utc).isoformat()+' — 100%\n\nIndependent scope report, primary-source receipts, source integrity and source-bound candidate content finalized. All public source hashes and every extracted manifest file match. Original abstract visually checked. No publication-scope defect identified; independent mathematical gates remain separate. No source modifications, repairs, website, spreadsheet, Git, Zenodo or outreach actions. Content SHA-256: '+v['content_sha256']+'.\n')
    print(id, v['content_sha256'], 'extracted files', count)
