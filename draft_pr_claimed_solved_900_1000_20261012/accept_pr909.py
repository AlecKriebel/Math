"""Record acceptance only after authenticating the exact two clean reviews."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

P = Path(__file__).resolve().parent
ROOT = P.parent
A = P / 'audits/pr909_30001345'
HEAD = 'd186dea31791cd3e8acf6829e0b65d01849623b8'
FREEZE = 'c58e74cd19d42ac1b867dc9add2f6c3ab9075248dcac0e19432f851ccba7509f'
PACKAGE = '0189e0ecd7bb39a1ed3899ee785cfc9f48bae7fdf386cd3002fd0a4849b70313'
BODY = 'ec4a9e42a7fa23d23024f918d7ff54f0f7e829971c567f89f9963ba243a8a43d'
PINS = {1: '38787f000151676ef3f1691d314317abf3e15dd699bc03e3845a49b86ecad0eb',
        2: '9190526562c8637f10a0477f3bc21031b1f79fe9c92540507491659f1efad403'}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    require(path.is_file() and not path.is_symlink(), 'Nonregular artifact: ' + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def run(args, binary=False):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True,
                          text=not binary).stdout


def main():
    now = datetime.now(timezone.utc).isoformat()
    pub = A / 'publication'
    require(not (A / 'ACCEPTANCE.json').exists(), 'Acceptance already exists; inspect instead')
    require(digest(pub / 'PREPUBLICATION_FREEZE.json') == FREEZE, 'Wrong frozen candidate')
    freeze = load(pub / 'PREPUBLICATION_FREEZE.json')
    require(freeze['revision_candidate'] == 1 and freeze['original_pr_head'] == HEAD
            and freeze['package_manifest_sha256'] == PACKAGE
            and len(freeze['files']) == 14, 'Wrong release scope')
    for name, record in freeze['files'].items():
        path = pub / name
        require(digest(path) == record['sha256'] and path.stat().st_size == record['bytes'],
                'Frozen artifact drift: ' + name)
    with zipfile.ZipFile(pub / 'rough-m-arrangements-source-verification-v1.0.zip') as archive:
        require(len(archive.infolist()) == 106 and
                hashlib.sha256(archive.read('PACKAGE_MANIFEST.json')).hexdigest() == PACKAGE,
                'Wrong archive inventory or manifest')
    results = {}
    counts = {}
    for number, pin in PINS.items():
        folder = A / 'reviews' / ('full_package_0' + str(number))
        require(digest(folder / 'MANIFEST.json') == pin, 'Unexpected review seal')
        manifest = load(folder / 'MANIFEST.json')
        records = manifest['files']
        require(set(manifest['explicit_public_allowlist']) - {'MANIFEST.json'} == set(records),
                'Review public allowlist inconsistent')
        for name, record in records.items():
            path = folder / name
            require(digest(path) == record['sha256'] and path.stat().st_size == record['bytes'],
                    'Sealed review drift: ' + str(path))
        counts[number] = len(records)
        result = results[number] = load(folder / 'RESULT.json')
        require(result['required_issues'] == [] and result['optional_issues'] == []
                and result['mathematical_remaining_gap_for_stated_theorem'] is None
                and result['priority_and_scope']['classical_corollary_framing_accurate'] is True,
                'Whole-package review not clean for the precise framing')
        require(result['candidate']['freeze_sha256'] == FREEZE
                and result['candidate']['original_head'] == HEAD
                and result['candidate']['package_manifest_sha256'] == PACKAGE,
                'Review cleared different candidate')
    require(counts == {1: 17, 2: 21}, 'Unexpected sealed review sizes')
    require(results[1]['validation']['review_reproducer_fresh_full_pipeline_replay'].startswith('PASS:')
            and results[2]['validation']['reproducer_fresh_full_pipeline_replay'].startswith('PASS:')
            and results[2]['clean_for_preprint_under_attributed_framing'] is True,
            'Full reviewer replay or final cleanliness absent')
    second = A / 'reviews/full_package_02'
    start = load(second / 'AUTHENTICATION_START.json')
    end = load(second / 'AUTHENTICATION_END.json')
    require(datetime.fromisoformat(start['utc']) >
            datetime.fromisoformat(results[1]['completed_utc']), 'Reviews not sequential')
    require(start['freeze_sha256'] == FREEZE and start['all_candidate_matches'] is True
            and start['all_original_git_matches'] is True
            and start['archive_regular_members_including_manifest'] == 106
            and start['archive_payloads_excluding_manifest'] == 105
            and end['freeze_sha256'] == FREEZE and end['all_match'] is True
            and len(end['candidate14_match']) == 14 and all(end['candidate14_match'].values())
            and len(end['original28_match_Git_and_disk']) == 28
            and all(end['original28_match_Git_and_disk'].values())
            and end['final_after_reproducer_reauthentication_passed'] is True,
            'Review endpoint authentication failed')
    helpers = load(second / 'HELPER_REVIEW.json')['future_helpers']
    require(len(helpers) == 5, 'Wrong future-helper review scope')
    for name, record in helpers.items():
        require(digest(P / name) == record['sha256'] and
                (P / name).stat().st_size == record['bytes'], 'Reviewed helper drift: ' + name)
    disposition = load(A / 'PUBLICATION_DISPOSITION.json')
    require(disposition['decision'] ==
            'EVALUATE_AND_IF_ALL_FINAL_GATES_PASS_ACCEPT_EXPLICITLY_ATTRIBUTED_CLASSICAL_COROLLARY'
            and disposition['silence_treated_as_approval'] is False
            and disposition['novel_current_open_problem_resolution_claim_licensed'] is False,
            'Disposition changed or unsupported claim licensed')
    scope = load(A / 'PREMERGE_QUEUE_SCOPE_CHECK.json')
    require(scope['original_head'] == HEAD and scope['non_target_queue_bytes_identical'] is True,
            'Original PR changes unrelated queue bytes')
    snapshot = load(A / 'ORIGINAL_SNAPSHOT.json')
    require(snapshot['head'] == HEAD and len(snapshot['files']) == 28, 'Wrong original snapshot')
    for name, pin in snapshot['files'].items():
        require(digest(A / 'original' / name) == pin and
                hashlib.sha256(run(['git', 'show', HEAD + ':' + name], binary=True)).hexdigest() == pin,
                'Original disk/Git packet drift: ' + name)
    pr = json.loads(run(['gh', 'pr', 'view', '909', '--repo', 'AlecKriebel/Math',
                         '--json', 'number,state,isDraft,headRefOid,headRefName,baseRefName,url,title,body']))
    require(pr['state'] == 'OPEN' and pr['isDraft'] is True and
            pr['headRefOid'] == HEAD and pr['baseRefName'] == 'main', 'Live eligibility changed')
    require(hashlib.sha256(pr['body'].encode()).hexdigest() == BODY and
            pr['title'] == '30001345: attributed multibranch rough-M counterexample; claimed_solved',
            'Reviewed live title/body drift')
    queue = run(['git', 'show', HEAD + ':unsolved_math_prioritization/QUEUE.md'])
    rows = [row for row in queue.splitlines() if '| 30001345 /' in row]
    require(len(rows) == 1 and rows[0].split('|')[8].strip() == 'claimed_solved'
            and rows[0].split('|')[9].strip() == '1 verified/5', 'Exact status or recovery label changed')
    parent = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
    run(['git', 'fetch', '--no-write-fetch-head', 'origin', parent])
    source = load(A / 'TARGET_IDENTITY_PREFLIGHT.json')
    catalog = json.loads(run(['git', 'show', parent + ':unsolved_math_prioritization/catalog.json']))
    target = next(t for t in catalog if str(t['id']) == '30001345')
    require(target.get('present') is True and target.get('holds') == [] and
            target['statement_hash'] == source['statement_hash'] and
            target['review_hash'] == source['review_hash'], 'Current source identity/holds changed')
    root_check = {'utc': now, 'review': 2, 'new_clean_context': True,
                  'sequential_after_clean_review01': True, 'manifest_sha256': PINS[2],
                  'public_files_authenticated': 21, 'root_read_full_audit_and_final_result': True,
                  'required_issues': [], 'optional_issues': [], 'candidate_freeze_sha256': FREEZE,
                  'all_14_frozen_and_28_actual_Git_originals_unchanged': True,
                  'all_five_reviewed_future_helpers_unchanged': True,
                  'both_review_reproducer_full_pipeline_passed': True,
                  'attributed_classical_corollary_only': True}
    save(A / 'WHOLE_PACKAGE_REVIEW02_ROOT_CHECK.json', root_check)
    accepted = {'utc': now, 'accepted': True, 'original_pr_head': HEAD,
                'live_gate_status': 'claimed_solved',
                'original_attempt_turns': '1 verified/5; earlier-attempt count unavailable',
                'original_total_attempt_count_known': False, 'verified_candidate_approaches': 1,
                'native_turns_used_to_record': None, 'new_author_proof_search_turns_added': 0,
                'candidate_revision': 1, 'freeze_sha256': FREEZE,
                'package_manifest_sha256': PACKAGE, 'files': freeze['files'],
                'exact_claim': results[2]['strongest_verified_theorem'],
                'proof_gap': None,
                'source_scope': 'Negative answer to unrestricted multibranch summed reading of '
                                'OWR2009 question with following fixed-ball setup; not later '
                                'unibranched parametric Conjecture3.8 or a marked-section assertion.',
                'priority': 'Explicit classical corollary: arrangement, deformation method and '
                            'ordinary-point formula attributed to prior literature. No new construction, '
                            'method, firstness, continued openness or author unstated intent claimed. '
                            'Earlier literal same rough-M theorem not established; history gap disclosed.',
                'disposition_basis': 'Already-authorized reasonable repair, as root explicitly stated; '
                                     'unanswered optional preference is not approval.',
                'silence_treated_as_approval': False,
                'full_package_reviews': [
                    {'round': n, 'clean_context': True, 'manifest_sha256': PINS[n],
                     'required_repairs': [], 'optional_improvements': [],
                     'clean_for_publication_under_attributed_framing': True,
                     'freeze_sha256': FREEZE} for n in (1, 2)],
                'AI_assisted': True, 'unrefereed': True,
                'independent_human_peer_review': False, 'formal_machine_proof_certification': False,
                'merge_and_publication_authorized_by_user': True}
    save(A / 'ACCEPTANCE.json', accepted)
    (A / 'ACCEPTANCE.md').write_text(
        'Accept the exact scoped counterexample as an explicitly attributed classical corollary. '
        'Both sequential new whole-package reviews report no required or optional issue; all frozen '
        'release files, 28 actual original Git blobs, source identity, live description and exact '
        'claimed_solved gate remain unchanged. The negative answer concerns the unrestricted '
        'multibranch summed rough-M reading with the fixed-ball setup, not the later unibranched '
        'parametric conjecture. Prior arrangement, deformation method and invariant formula are '
        'credited. No new method, firstness or continued openness is claimed. Publish candidate1 '
        'with its reviewed metadata and AI/unrefereed disclosures. Preserve 1 verified/5 and '
        'unknown earlier attempt history; do not certify one total historical attempt. This '
        'reasonable-repair disposition follows existing authorization; silence on an optional '
        'preference question is not treated as approval. Historical pending records remain '
        'accurate for their timestamps and are superseded administratively by this acceptance.\n')
    save(A / 'FINAL_ACCEPTANCE_GATE.json', {
        'utc': now, 'pr': {k: v for k, v in pr.items() if k != 'body'},
        'corrected_body_sha256': BODY, 'remote_main': parent,
        'source_identity_unchanged': True, 'review_manifests': PINS,
        'original_files_unchanged': 28, 'freeze_sha256': FREEZE,
        'exact_queue_status': 'claimed_solved', 'non_target_original_queue_bytes_unchanged': True})
    state = load(P / 'CURRENT_STATE.json')
    state.update(utc=now, phase='PR909_accepted_merge_and_publish_next',
                 active_pr_completion_estimate_percent=96,
                 shard_completion_estimate_percent=(4 + .96) / 12 * 100,
                 publication_disposition='Accepted precisely scoped attributed classical corollary; no firstness/current-openness claim')
    save(P / 'CURRENT_STATE.json', state)
    for log in [A / 'RESEARCH_LOG.md', P / 'RESEARCH_LOG.md']:
        with log.open('a') as out:
            out.write('\n' + now + ' — PR909 accepted (96% workflow; shard41.333%): '
                      'two sequential new clean whole-package reviews authenticated (17/21 public files); '
                      'no required/optional issue. All14 frozen files/original28 Git bytes/current '
                      'source identity/holds/live body/exact claimed_solved1 verified/5 unchanged. '
                      'Accept attributed classical corollary only, preserve unknown earlier total; '
                      'merge and exact-reviewed-metadata publication next. No silence-as-approval.\n')
    print(json.dumps({'accepted': True, 'freeze_sha256': FREEZE,
                      'review_files_authenticated': counts, 'live_status': 'claimed_solved'}, indent=2))


if __name__ == '__main__':
    main()
