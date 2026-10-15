"""Append unchanged final review and advance administrative acceptance only."""
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUB = HERE / 'publication'
EVIDENCE = PUB / 'evidence'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def main():
    if (HERE / 'FINAL_SEAL.json').exists():
        raise RuntimeError('Final seal exists; do not rewrite a frozen package')
    review = HERE / 'reviews/package_02'
    verdict = json.loads((review / 'VERDICT.json').read_text())
    if verdict['status'] != 'CLEAN' or verdict['actionable_issue_count'] != 0:
        raise RuntimeError('Fresh whole-package review has not passed cleanly')
    archive = PUB / 'rational_mixed_integer_bipartite_covers_source_verification_v1.zip'
    if digest(archive) != verdict['candidate_archive_sha256']:
        raise RuntimeError('Candidate archive differs from reviewed bytes')
    payload = [PUB / name for name in ('research_note.tex', 'research_note.pdf',
               'metadata.json', 'run_checks.py')]
    payload += sorted((PUB / 'checks').rglob('*'))
    frozen = {p.relative_to(PUB).as_posix(): digest(p) for p in payload if p.is_file()}
    copied = []
    for source in sorted(review.rglob('*')):
        if not source.is_file():
            continue
        relative = source.relative_to(review)
        if 'raw' in relative.parts or '__pycache__' in relative.parts:
            continue
        if source.suffix in {'.png', '.pdf', '.zip', '.pyc'}:
            continue
        target = EVIDENCE / 'package_review_02' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        copied.append({'path': target.relative_to(PUB).as_posix(),
                       'bytes': target.stat().st_size, 'sha256': digest(target)})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(EVIDENCE / 'PACKAGE_REVIEW_02_COPY.json', {
        'utc': now, 'all_copied_bytes_unchanged': True,
        'excluded': 'raw third-party bodies, own PDF renders, caches and duplicate input archives',
        'historical_manifests_describe_original_review_inputs': True, 'files': copied})
    state = json.loads((EVIDENCE / 'CURRENT_REVIEW_STATE.json').read_text())
    state['fresh_package_reviews'].append({'round': 2, 'status': 'CLEAN',
        'actionable_issue_count': 0, 'both_prior_repairs_verified': True,
        'input_archive_sha256': verdict['candidate_archive_sha256']})
    state.update({'preprint_ready_for_immutable_publication': True,
        'all_actionable_issues_resolved': True, 'published': False,
        'next_gate': 'owner final integrity, production publication and tracker',
        'pending_issues': []})
    save(EVIDENCE / 'CURRENT_REVIEW_STATE.json', state)
    save(EVIDENCE / 'FINAL_ACCEPTANCE.json', {
        'utc': now, 'pr': 1025, 'audited_head': verdict['audited_head'],
        'mathematics': 'root deductions and two distinct independent families passed',
        'priority': 'bounded primary-body audit; classical lineage credited globally',
        'new_whole_package_reviews': 2, 'final_review_status': 'CLEAN',
        'all_actionable_issues_resolved': True, 'preprint_ready': True,
        'scope': 'complete rational binary-input optimization and exact strong separation/membership theorem for arbitrary free-sign mixed-integer bipartite covers; Conjecture 2 unaddressed',
        'AI_used_extensively': True, 'unrefereed': True, 'human_peer_review': False,
        'worldwide_priority_certified': False,
        'finite_checks_are_universal_or_complexity_proof': False,
        'reviewed_mathematical_payload_unchanged': frozen})
    readme = PUB / 'README.md'
    text = readme.read_text()
    old = ('whole-package reviewer found two P3 presentation/boundary repairs; both have\n'
           'been applied, and a NEW second review remains required. This draft is not\n'
           'approved for submission or immutable publication. The polynomial LP, submodular')
    new = ('whole-package review 1 found two P3 presentation/boundary repairs; both were\n'
           'applied. A NEW independent review 2 verified both repairs and the entire\n'
           'package, finding zero actionable issues. The preprint is ready for immutable\n'
           'publication; [final acceptance](evidence/FINAL_ACCEPTANCE.json) and\n'
           '[current review state](evidence/CURRENT_REVIEW_STATE.json) record the gate.\n'
           'The polynomial LP, submodular')
    if text.count(old) != 1:
        raise RuntimeError('README acceptance text anchor differs')
    readme.write_text(text.replace(old, new))
    supplement = PUB / 'SUPPLEMENT.md'
    text = supplement.read_text()
    old = ('preserved. A NEW second review remains required. This draft is not yet approved for\n'
           'immutable publication. Extensive AI use, unrefereed status and all scope/credit')
    new = ('preserved. A NEW independent second review verified the fixes and the complete\n'
           'package, with zero actionable issues. [Final acceptance](evidence/FINAL_ACCEPTANCE.json)\n'
           'and [review state](evidence/CURRENT_REVIEW_STATE.json) now record readiness\n'
           'for immutable publication. Extensive AI use, unrefereed status and all scope/credit')
    if text.count(old) != 1:
        raise RuntimeError('Supplement acceptance text anchor differs')
    supplement.write_text(text.replace(old, new))
    index = EVIDENCE / 'INDEX.md'
    text = index.read_text()
    old = ('A NEW second whole-package review remains pending. This draft is not yet\n'
           'approved for immutable publication.')
    new = ('[NEW second whole-package review](package_review_02/REVIEW.md),\n'
           '[clean verdict](package_review_02/VERDICT.json) and\n'
           '[unchanged copy pins](PACKAGE_REVIEW_02_COPY.json) independently verify\n'
           'both repairs and the full candidate. Zero actionable issues remain.\n'
           '[Final acceptance](FINAL_ACCEPTANCE.json) advances the current gate.\n'
           'The last reviewed mathematical source, PDF, checker and metadata bytes\n'
           'are unchanged; only unchanged review evidence and administrative\n'
           'acceptance/navigation records were added after that review. Historical\n'
           'input manifests refer to their original stages.')
    if text.count(old) != 1:
        raise RuntimeError('Evidence index acceptance text anchor differs')
    index.write_text(text.replace(old, new))
    if any(digest(PUB / name) != value for name, value in frozen.items()):
        raise RuntimeError('Mathematical payload changed after final review')
    save(HERE / 'FINAL_SEAL.json', {'utc': now, 'mathematical_payload': frozen,
        'immutable_ready': True, 'new_whole_package_reviews': 2,
        'no_actionable_concerns': True, 'appended_final_review_files': len(copied)})
    print(json.dumps({'final_acceptance': True, 'unchanged_review_files': len(copied),
                      'mathematical_payload_unchanged': True}))


if __name__ == '__main__':
    main()
