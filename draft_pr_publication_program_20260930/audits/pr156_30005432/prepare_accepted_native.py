"""Add actual publication receipts without changing reviewed scientific bytes."""
from pathlib import Path
import datetime, hashlib, json, shutil

A = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    gate = json.loads((A / 'ROOT_PUBLICATION_GATE.json').read_text())
    pub = json.loads((A / 'ZENODO_PUBLICATION_READBACK.json').read_text())
    tracker = json.loads((A / 'TRACKER_ACCEPTANCE.json').read_text())
    require(gate['status'] == 'READY_FOR_AUTHORIZED_PUBLICATION' and gate['fresh_seal_first_review_clean'], 'Clean whole-package gate required')
    require(pub['state'] == 'published' and tracker['DOI'] == pub['doi'] and tracker['DOI_count'] == 1, 'Actual publication and exact tracker required')
    before = A / 'native_proposal_v1'
    after = A / 'integration_preparation/native_accepted'
    require(not after.exists(), 'Inspect existing preparation before replacing it')
    after.parent.mkdir(exist_ok=True)
    shutil.copytree(before, after)
    now = datetime.datetime.now(datetime.UTC).isoformat()
    readme = (after / 'README.md').read_text()
    old = 'publication_package contains the proposed research note, exact metadata and verification archive. Publication and merge receipts will be recorded separately after actual success. Whole-package adversarial review is pending in this prepared proposal. No DOI or merge is claimed here.'
    new = ('publication_package contains the published research note, exact metadata and verification archive. '
           'Two fresh complete-package reviews found no substantive defect; the final reviewer sealed an independent direct-input assessment before prior verdicts. '
           'Actual publication: ' + pub['doi_url'] + '. Tracker: ' + tracker['range'] + ', DOI occurs once. '
           'MAIN integration/merge remains pending. Publication/tracker receipts and readiness.json record actual verified state.')
    require(old in readme, 'Expected prepared README paragraph absent')
    (after / 'README.md').write_text(readme.replace(old, new))
    counterexample = (after / 'COUNTEREXAMPLE.md').read_text()
    old_status = 'Qualified research note prepared; whole-package review and publication are pending.'
    new_status = 'Qualified research note published after two fresh full-package reviews; the final direct-input assessment was sealed before prior verdicts. Publication DOI: ' + pub['doi_url'] + '. Tracker accepted; MAIN integration is pending.'
    require(old_status in counterexample, 'Expected prepared status absent')
    counterexample = counterexample.replace(old_status, new_status)
    counterexample = counterexample.replace('are the publication proposal.', 'are the published scientific package. Its proof and metadata are unchanged from the reviewed candidate.')
    (after / 'COUNTEREXAMPLE.md').write_text(counterexample)
    with (after / 'RESEARCH_LOG.md').open('a') as handle:
        handle.write('\n' + now + ' — Full-package R1 and new seal-first R2 clean; frozen PDF/support archive and exact metadata published at ' + pub['doi_url'] + '; one Google Workspace tracker row ' + tracker['range'] + ' accepted by returned values and two fresh reads. Mathematical proof unchanged, historical priority and independence unresolved. Math100%, bounded priority100%, case90%; original-head merge remains pending.\n')
    for name in ['ZENODO_PUBLICATION_READBACK.json', 'TRACKER_ACCEPTANCE.json']:
        shutil.copyfile(A / name, after / name)
    save(after / 'readiness.json', {'UTC': now, 'status': 'PUBLISHED_TRACKED_MERGE_PENDING', 'PR': 156, 'problem_id': 30005432, 'original_head': 'aec31742f3f26c5b1e533404da57539d17dc94a1', 'mathematics_cleared': True, 'bounded_priority_audit_complete': True, 'historical_novelty_or_independence_certified': False, 'whole_package_reviews': 2, 'fresh_seal_first_review_clean': True, 'published': True, 'DOI': pub['doi'], 'tracker_range': tracker['range'], 'tracker_DOI_count': 1, 'merged': False, 'case_percent': 90, 'unrefereed': True, 'extensive_AI_assistance': True})
    allowed = {'README.md', 'COUNTEREXAMPLE.md', 'RESEARCH_LOG.md'}
    original_names = {p.relative_to(before).as_posix() for p in before.rglob('*') if p.is_file()}
    actual_names = {p.relative_to(after).as_posix() for p in after.rglob('*') if p.is_file()}
    require(actual_names == original_names | {'readiness.json', 'ZENODO_PUBLICATION_READBACK.json', 'TRACKER_ACCEPTANCE.json'}, 'Native inventory changed unexpectedly')
    for name in original_names - allowed:
        require((before / name).read_bytes() == (after / name).read_bytes(), 'Reviewed scientific body changed: ' + name)
    def math_part(text):
        return text.split('## 1.', 1)[1].split('## 6.', 1)[0]
    require(math_part((before / 'COUNTEREXAMPLE.md').read_text()) == math_part(counterexample), 'Proof sections changed')
    body = (A / 'PR_BODY_PROPOSAL_V1.md').read_text()
    pending = 'Whole-package review, upload, tracker and actual merge remain pending at this prepared snapshot.'
    require(pending in body, 'Prepared PR body differs')
    body = body.replace('A concise qualified research note and reproducibility package are prepared.', 'A concise qualified research note and reproducibility package are published.')
    body = body.replace(pending, 'Two fresh full-package reviews found no substantive defect; the final reviewer sealed independent direct-input assessment before prior verdicts. Published research note and complete verification/source/priority package: [' + pub['doi'] + '](' + pub['doi_url'] + '). Exact metadata/files and one tracker row ' + tracker['range'] + ' were verified. Original-head merge remains pending.')
    (A / 'PR_BODY_ACCEPTED.md').write_text(body)
    save(after.parent / 'CURRENT_TEMPLATE.json', {'UTC': now, 'current_template': 'native_accepted', 'original_proposal': 'native_proposal_v1', 'reviewed_package': gate['package'], 'mathematical_package_and_scripts_unchanged': True, 'proof_sections_unchanged': True, 'post_review_operational_changes': sorted(allowed | {'readiness.json', 'ZENODO_PUBLICATION_READBACK.json', 'TRACKER_ACCEPTANCE.json'}), 'MAIN_integration_pending': True, 'native_files': len(actual_names)})
    print(json.dumps({'status': 'ACTUAL_PUBLISHED_TRACKED_NATIVE_TEMPLATE_PREPARED', 'native_files': len(actual_names), 'DOI': pub['doi'], 'tracker': tracker['range'], 'science_unchanged': True}))

if __name__ == '__main__':
    main()
