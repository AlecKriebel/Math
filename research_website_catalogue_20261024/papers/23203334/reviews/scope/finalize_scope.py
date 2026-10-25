from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for ident in ['23203334', '22013710']:
    p = B/ident/'reviews/scope'
    content = json.loads((p/'content.json').read_text())
    integrity = json.loads((p/'source_integrity.json').read_text())
    assert integrity['passed'] and integrity['all_public_record_assets_present']
    assert content['follow_up'] is None
    assert content['source_binding']['zenodo_version'] is None
    assert (p/'REVIEW.md').is_file()
    now = datetime.now(timezone.utc).isoformat()
    exposed = ident == '23203334'
    sha = hashlib.sha256((p/'content.json').read_bytes()).hexdigest()
    verdict = dict(
        record_id=ident,
        role='publication_scope_and_primary_literature_review_with_archived_support_exposure' if exposed else 'independent_publication_scope_and_primary_literature_review',
        timestamp_utc=now, completion_percent=100,
        scope_verdict='no_publication_scope_defect_identified',
        publication_disposition='candidate_content_only_pending_separate_mathematical_gates',
        mathematical_gate=False, novelty_certified=False, independent_human_peer_review=False,
        full_published_paper_read=True, published_paper_pages=integrity['main_pdf_pages'],
        published_supplement_pdfs=[], all_published_assets_acquired=True, source_integrity_pass=True,
        strict_archived_opinion_independence=not exposed,
        archived_review_opinion_exposure=exposed,
        archived_or_sibling_review_verdicts_used=False,
        current_sibling_mathematical_findings_consulted=False,
        independence_note=(
            'The full mathematically relevant published occupation supplement included historical independent audit assessments. These were read before the 60% scope checkpoint and promptly disclosed to root. Strict exclusion of archived opinions therefore cannot be claimed. They were not used as validation. No current sibling mathematical findings were consulted; source coordination concerned only raw primary paths, acquisition and intended source scope.'
            if exposed else
            'Own scope conclusion was recorded at 60% before sibling mathematical opinions. No dedicated archived audit or adjudication verdict consulted. Manuscript-authored historical and AI assertions were encountered but not adopted as validation. Later GHR coordination shared raw source paths and author-preprint edition status only.'
        ),
        content_sha256=sha, source_binding=content['source_binding'],
        follow_up=None, followup_rationale=content['followup_rationale'], defects=[],
        key_boundaries=content['limitations'],
        primary_source_review_limitations=(
            ['The pinned 49-page upstream PDF was acquired and hash-matched; its introduction, theorem and proof strategy were read, but this scope reviewer does not claim a full independent reading of all upstream analytical sections.', 'Glassey–Schaeffer 1988 and Glassey 1996 bodies were not acquired; exact historical hypothesis comparisons are not independently certified.', 'Internal finite certificates do not certify the analytical theorem.']
            if exposed else
            ['GHR was read in the 31-page author-preprint edition, not final IMRN typesetting.', 'Original Wenzl and Turaev source bodies were not acquired directly.', 'Historical release chronology and private discovery priority were not independently adjudicated.', 'Verification source was read, but no execution of mathematical checkers is claimed by this scope reviewer.']
        )
    )
    (p/'verdict.json').write_text(json.dumps(verdict, indent=2, ensure_ascii=False)+'\n')
    with (p/'RESEARCH_LOG.md').open('a') as f:
        f.write(f'\n## {now} — 100%\n\nFull scope report, candidate content and verdict finalized. All published assets and internal manifests pass integrity checks. No substantive scope defect identified; mathematical gates remain separate. Content SHA-256: {sha}. Follow-up remains null. '+('Historical occupation-audit opinion exposure is explicitly disclosed; this is not a strictly independent mathematical gate.' if exposed else 'No dedicated archived or sibling mathematical opinions used.')+' No external or website/spreadsheet/Git/Zenodo mutations.\n')
    print(ident, sha)
