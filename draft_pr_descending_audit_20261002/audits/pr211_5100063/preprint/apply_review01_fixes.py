"""Apply documentary findings only after root reads the sealed first full review.

No archived original, mathematical section, provider or native ref is changed.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

BASE=Path(__file__).resolve().parent
D=BASE.parent/'initial_review_20261015'; U=BASE/'pr_update/5100063'
REVIEW=D/'whole_manuscript_adversary_01'

def write_json(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def math_sections(text):return text.split('## 1.',1)[1].split('## 8.',1)[0]

def main():
    acceptance=json.loads((D/'ROOT_REVIEW01_ACCEPTANCE.json').read_text())
    assert acceptance['root_full_report_and_controls_read'] and acceptance['mathematical_blockers']==[]
    assert acceptance['report_sha256']==sha(REVIEW/'REPORT.md')
    assert not (BASE/'REVIEW01_RESOLUTION.json').exists(),'Already applied; reconcile before another mutation'
    before={p.relative_to(U).as_posix():sha(p) for p in (U/'history/original_submission_20261015').rglob('*') if p.is_file()}
    oldproof=(U/'PROOF.md').read_text(); oldmath=math_sections(oldproof)
    proof=oldproof.replace('Mathematical/source audit accepted; qualified preprint package in preparation.',
        'Mathematical/source audit accepted. Current manuscript-review and publication status: PUBLICATION_STATUS.md.')
    proof=proof.replace('Fresh whole-manuscript/package reviews remain required before publication.',
        'The whole-manuscript/package reviews and release receipts are recorded separately in PUBLICATION_STATUS.md and the case audit.')
    proof=proof.replace('The full self-contained research note supersedes stale historical pending-review text; originals remain immutable.',
        'The full self-contained research note and current disposition supersede historical pending-review text; originals remain immutable.')
    assert math_sections(proof)==oldmath
    (U/'PROOF.md').write_text(proof)
    original=json.loads((U/'history/original_submission_20261015/source_record.json').read_text())
    source=dict(record_role='Current qualified assessment of the pinned source assertion; this is not a writeback to the upstream read-only dataset',
        id=5100063,problem_number='AMR-050-0063',title=original['title'],statement=original['statement'],
        statement_role='Original source assertion retained; exact proved domain is specified in current_assessment',
        status='claimed_solved',proposed_by=original['proposed_by'],proposed_year=2020,
        proposed_year_basis='Earliest literal printing verified here: arXiv2004.12497v10,25October2020,Table9,k808,a; renamed v11 k904,a on29October2020. No earliest-discovery-day claim.',
        historical_import=dict(path='history/original_submission_20261015/source_record.json',
            sha256=sha(U/'history/original_submission_20261015/source_record.json'),
            dataset_revision='37e53eabe540fb458758e198be61634bd02ee008',
            warning='Original2021 year,OPEN-TRIAGE/open labels,4-5/2020 dating and worldwide-open summary are historical imported fields, superseded by this qualified assessment.'),
        current_assessment=dict(mathematics='PASS for original-focus unit inversion of outer tangent vertices, signed straight-edge areas, strict nondegenerate confocal elliptical caustics, all odd least periods/coprime stars/N3 and fixed repeated traversals',
            priority='No exact earlier general proof verified in audited primary corpus; historical novelty undetermined; no first-proof or present-worldwide-open claim',
            completed_author_turns='1/5',current_release_status='PUBLICATION_STATUS.md',
            source_and_access_limits='SOURCES.md and supporting priority ledgers; no all-literature coverage certification',
            AI_use='Extensive; unrefereed, no independent human peer review or proof-assistant formalization'))
    write_json(U/'source_record.json',source)
    (U/'WIP.md').write_text('''# Historical working-log pointer

The original unreviewed working log is preserved verbatim at
`history/original_submission_20261015/WIP.md`. Its active-author, pending-checker,
unreviewed and75% labels describe that earlier checkpoint; they are not current.

The mathematics/source assessment is now PASS for the exact domain in PROOF.md,
including all odd primitive stars/N3 and repetition scaling. Author turn1/5.
Historical novelty remains undetermined; no first-proof/current-world-open claim.
PUBLICATION_STATUS.md and the case audit hold current manuscript-review and
release receipts. Extensive AI use; unrefereed, no independent human peer review.
''')
    m=json.loads((U/'metadata.json').read_text())
    for key in ['remote_wip_head','remote_wip_branch']:
        if key in m:m['historical_'+key]=m.pop(key)
    m.update(record_role='Dated prepublication presentation snapshot; later administrative release receipts supersede its stage fields',
        status='mathematics_source_accepted_qualified_proof',reviewed_input_head='9d7b623203b525386da3d9d91548c79e7445a11c',
        current_release_status='PUBLICATION_STATUS.md',completed_author_turns=1)
    write_json(U/'metadata.json',m)
    p=U/'prior_imported_report.json'
    write_json(p,dict(record_role='Historical imported triage report pointer; not current acceptance or priority evidence',
        original_path='history/original_submission_20261015/prior_imported_report.json',
        original_sha256=sha(U/'history/original_submission_20261015/prior_imported_report.json'),
        current_assessment='source_record.json and PUBLICATION_STATUS.md'))
    s=json.loads((U/'source_manifest.json').read_text());s.update(record_role='Pinned primary-source identities and historical read-only dataset revision, not a live triage-status record',
        source_version_history=dict(v10='25October2020,Table9,k808,a',v11='29October2020,Table10,k904,a'),
        source_title_note='arXiv record: Eighty New Invariants of N-Periodics in the Elliptic Billiard; pinned PDF displayed heading: Eighty New Invariants in the Elliptic Billiard')
    write_json(U/'source_manifest.json',s)
    (U/'independent_review/README_CURRENT_SCOPE.md').write_text('''# Historical independent review scope

The five original files in this directory are retained verbatim from the19-file
submission. They bind the original proof, also preserved under
`../history/original_submission_20261015/`, rather than amended current headers.
The portable harness replays that original input in isolated folders. Current
whole-manuscript review and publication receipts are recorded in
`../PUBLICATION_STATUS.md` and the case audit. Do not read an old PASS or pending
phrase here as a statement about a later packet version.
''')
    with (U/'SOURCES.md').open('a') as f:f.write('\n\nThe current source_record.json is a qualified assessment wrapper. Its exact historical upstream record, including erroneous2021/source-status triage, is preserved in history/original_submission_20261015/. The full arXiv-record title includes OfN-Periodics; the pinned PDF heading is shorter. Both refer to the same pinnedv11.\n')
    for p in [U/'README.md',BASE/'README.md']:
        text=p.read_text()
        if p.parent==U:
            text=text.replace('Mathematics/source audit accepted; qualified preprint preparation is underway and awaits sequential new whole-package reviews.',
                'Mathematics/source audit accepted; current manuscript-review/release outcomes are recorded separately in PUBLICATION_STATUS.md and the case audit.')
            text+='\nCurrent source_record.json, WIP.md and prior_imported_report.json explicitly distinguish the current qualified assessment from historical imports. Historical branch identifiers in metadata.json are labeled historical; the full original records remain byte exact in the archive.\n'
        else:
            text=text.replace('The manuscript and package await the required sequential fresh whole-package adversarial reviews before any deposit, DOI, tracker row or merge. Preparation is not publication clearance.',
                'This is a dated prepublication source/verification snapshot. The required version-bound whole-package reviews and final administrative release receipts are maintained alongside this case in the repository audit and PR#211. Historical preparation receipts are provenance, rather than live release status. Preparation alone is not publication clearance. The native release adds actual DOI/tracker/review receipts without changing the deposited proof or control bytes.')
        p.write_text(text)
    tex=BASE/'manuscript.tex';text=tex.read_text();old='\\emph{Eighty new invariants in the elliptic billiard}'
    assert text.count(old)==1
    tex.write_text(text.replace(old,'\\emph{Eighty new invariants of N-periodics in the elliptic billiard}'))
    assert before=={p.relative_to(U).as_posix():sha(p) for p in (U/'history/original_submission_20261015').rglob('*') if p.is_file()}
    result=dict(utc=datetime.now(timezone.utc).isoformat(),review_report_sha256=acceptance['report_sha256'],
        mathematical_sections_1_to_7_unchanged=True,mathematical_sections_sha256=hashlib.sha256(oldmath.encode()).hexdigest(),
        archived19_files_unchanged=True,fixes=['Explicit current source-record wrapper/date2020/qualified scope and status','Historical WIP and imported-report pointers','Historical branch identifiers labeled historical','Independent legacy-review binding note','Current versus dated preparation/release status reconciled','Full arXiv-record title in bibliography, same pinned source'],
        remaining_steps=['Recompile/export/render and actually inspect all PDF pages','Reseal current manifests and deterministic ZIP','Fresh sequential whole-package adversary02'],
        upload_cleared=False)
    write_json(BASE/'REVIEW01_RESOLUTION.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
