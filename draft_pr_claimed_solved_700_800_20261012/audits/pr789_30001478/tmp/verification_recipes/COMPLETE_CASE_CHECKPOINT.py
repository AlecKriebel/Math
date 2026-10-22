from pathlib import Path
import contextlib, datetime, hashlib, io, json, sys

R = Path('/Users/alec/Documents/Math')
D = R / 'draft_pr_claimed_solved_700_800_20261012'
T = D / 'audits/pr789_30001478/tmp'
M = T / 'root-receipts'
sys.path.insert(0, str(D))
from graphql_scoped_commit import Remote, head_oid, commit_updates

assert not (M / 'COMPLETE_CHECKPOINT_RECEIPT.json').exists(), 'Reconcile existing completion; never duplicate'
graw = (T / 'FINAL_READINESS.json').read_bytes()
g = json.loads(graw)
freeze = json.loads((M / 'NATIVE_GATE_FREEZE.json').read_text())
assert hashlib.sha256(graw).hexdigest() == freeze['readiness_sha256']
native = json.loads((M / 'NATIVE_ACCEPTANCE_RECEIPT.json').read_text())
validation = json.loads((M / 'ROOT_NATIVE_VALIDATION.json').read_text())
assert native['result'] == validation['result'] == 'PASS'
assert native['commit'] == validation['native_commit']
assert native['doi'] == '10.5281/zenodo.23423736'
assert g['PR_completion_estimate_percent'] == 98 and g['merge_done']
assert g['actual_whole_preprint_rounds'] == 4
assert g['source_manifest_sha256'] == 'b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa'
pdf = T / 'preprint/output/pdf/paper.pdf'
pdfraw = pdf.read_bytes()
assert len(pdfraw) == 60079 and hashlib.sha256(pdfraw).hexdigest() == 'c91648374d0467758de9773c95ef37b32c275993a20d2e0d9067c20702f18994'
delivery = D / 'final_delivery/pr789-paper.pdf'
assert not delivery.exists() or delivery.read_bytes() == pdfraw
delivery.write_bytes(pdfraw)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
delivery_receipt = {
    'utc': now, 'result': 'PASS', 'pr': 789, 'doi': native['doi'],
    'path': delivery.relative_to(R).as_posix(), 'bytes': len(pdfraw),
    'sha256': hashlib.sha256(pdfraw).hexdigest(),
    'native_acceptance_commit': native['commit'],
    'same_bound_published_PDF': True, 'new_publication_or_review': False,
}
(M / 'FINAL_PDF_DELIVERY.json').write_text(json.dumps(delivery_receipt, indent=2) + '\n')
case = {
    'completed_utc': now, 'pr': 789, 'problem': '30001478',
    'result': 'accepted_complete_two_literal_assertions_negative_resolution_unrefereed_preprint_published',
    'accepted_scope': g['accepted_scope'], 'priority_summary': g['priority_summary'],
    'doi': native['doi'], 'record_url': g['publication_record_url'],
    'original_scientific_head': g['original_scientific_head'],
    'approved_administrative_head': g['reviewed_head'],
    'merge_commit': g['merge_commit'], 'native_acceptance_commit': native['commit'],
    'tracker_range': g['tracker_range'], 'original_files_preserved': 58,
    'closed_source_files': 151, 'source_hashes_preserved': True,
    'original_explicit_budget': '1/5', 'new_substantive_proof_turns': 0,
    'whole_preprint_review_rounds': 4, 'freshly_initialized_whole_reviewers': 4,
    'final_round_actionable_issues': 0,
    'review_versions_and_both_publication_snapshots_preserved': True,
    'independent_administrative_scope_review_additional_only': True,
    'same_reviewed_six_published': True, 'Zenodo_uploaded_files': 2,
    'single_known_Zenodo_record': 23423736,
    'unpublished_old_support_ZIP_replaced_once_before_publication': True,
    'new_duplicate_deposit_or_republication': False,
    'all_supplied_canonical_metadata_exact': True, 'metadata_normalizations': [],
    'public_two_payload_sha256_and_sizes_verified': True, 'DOI_HTTP_status': 200,
    'administrative_integration_full_scope_verified': True,
    'actual_full_merge_tree_verified_by_root_and_independent_reviewer': True,
    'native_changes_only_own7paths': True, 'unrelated_native_bytes_and_history_preserved': True,
    'historical_first_priority_certified': False, 'novelty_certified': False,
    'current_worldwide_open_status_certified': False,
    'Nevins_Sierra_Campbell_and_characteristic_two_boundaries_explicit': True,
    'extensive_AI_use': True, 'external_human_peer_review': False,
    'formal_proof_verification': False,
    'source_manifest_sha256': g['source_manifest_sha256'],
    'final_readiness_sha256': freeze['readiness_sha256'],
    'pr_completion_percent': 100, 'shard_completion_estimate_percent': 92,
}
entry = (
    '\n## ' + now + ' — PR789 accepted, published, merged and native acceptance verified\n\n'
    'Completed the full process for PR789/problem30001478. The four-page note and closed '
    'source/verification archive are published at DOI10.5281/zenodo.23423736, with exact '
    'canonical metadata and no normalization, public payload SHA checks, DOI HTTP200, and '
    'one verified tracker row A131:D131. Four distinct fresh whole-preprint reviews completed; '
    'the final exact V4 package has zero issues. The single administrative branch integration '
    'and exact approved-head merge preserve all58 original scientific blobs and all unrelated '
    'paths; independent and root full-tree checks pass. Present-day native acceptance '
    + native['commit'] + ' changes exactly seven own paths, preserves other JSON value bytes '
    'and ordering, all other queue/ranking rows, and the entire historical prefix; one '
    'contemporary event is appended with original1/5 budget and zero new proof-search turns. '
    'Source151 and all six publication artifacts remain unchanged. The native-bound '
    'FINAL_READINESS remains frozen at98%; completion100% is recorded here separately. '
    'Historical priority is UNRESOLVED, with exact Nevins-Sierra, Campbell and characteristic-two '
    'limitations retained throughout. Extensive AI use, unrefereed status and no external '
    'human/formal verification are explicit. Final published PDF copied with identical bytes '
    'to final_delivery/pr789-paper.pdf. Next is799, only after a fresh immutable-head '
    'claimed_solved eligibility gate. No unrelated-shard communication or Git checkout changes.\n\n'
    'Case100%; shard92% (11 of12 initial eligible cases completed; final rescreen pending).\n'
)
updates = {delivery.relative_to(R).as_posix(): pdfraw}
for folder in ['root-receipts', 'verification_recipes']:
    for p in (T / folder).rglob('*'):
        if p.is_file():
            assert not p.is_symlink() and p.stat().st_nlink == 1
            updates[p.relative_to(R).as_posix()] = p.read_bytes()
for attempt in range(3):
    remote = Remote(head_oid())
    u = dict(updates)
    state = json.loads(remote.read(D.name + '/STATE.json'))
    assert len(state['processed']) == 10 and 789 not in [x['pr'] for x in state['processed']]
    state['processed'].append(case)
    state.update(updated_at=now, current_pr=799,
                 current_stage='NEXT_PR799_FRESH_IMMUTABLE_CLAIMED_SOLVED_GATE_REQUIRED',
                 overall_completion_estimate_percent=92)
    u[D.name + '/STATE.json'] = json.dumps(state, indent=2) + '\n'
    for name in ['RESEARCH_LOG.md', 'audits/pr789_30001478/RESEARCH_LOG.md']:
        u[D.name + '/' + name] = remote.read(D.name + '/' + name) + entry
    results = remote.read(D.name + '/RESULTS.md')
    before_next = results.split('\nNext:')[0].rstrip()
    before_next += ('\n| [#789](https://github.com/AlecKriebel/Math/pull/789) | '
                    'Accepted the exact projective-line quotient refuting both historical '
                    'Rogalski–Sierra assertions; characteristic and priority bounds explicit. | '
                    '[Preprint](https://doi.org/10.5281/zenodo.23423736) |\n')
    before_next = before_next.replace(
        'Updated ' + before_next.split('Updated ', 1)[1].split('. This is a progress index;', 1)[0],
        'Updated ' + now, 1)
    tail = ('\nNext: **#799 /30002364**, subject to a fresh exact claimed_solved PR-head gate.\n\n'
            'Overall process completion estimate: **92%**. Eleven initial eligible PRs completed; '
            'one initial eligible PR remains. Final eligibility reconciliation remains pending. '
            'This percentage measures the processing program, not proof novelty.\n\n'
            'The accepted papers disclose extensive AI use, unrefereed status, no external '
            'human peer review and no proof-assistant certification. Historical firstness and '
            'current worldwide openness are not certified; each paper states its exact source '
            'and priority bounds.\n\n[Research log](RESEARCH_LOG.md) and '
            '[machine-readable state](STATE.json) contain scope, immutable source identities, '
            'audit checkpoints and receipts. Final published files and metadata are bound '
            "in each problem's audit folder.\n")
    u[D.name + '/RESULTS.md'] = before_next + tail
    log = remote.read(D.name + '/checkpoint_receipts.jsonl')
    for name in ['MERGE_READINESS_CHECKPOINT_RECEIPT.json', 'NATIVE_ACCEPTANCE_RECEIPT.json']:
        receipt = json.loads((M / name).read_text())
        if not any(json.loads(line).get('commit') == receipt['commit'] for line in log.splitlines() if line):
            log += json.dumps(receipt) + '\n'
    u[D.name + '/checkpoint_receipts.jsonl'] = log
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        receipt = commit_updates(remote, u, 'Complete PR789 verified publication, exact merge and native acceptance')
    (M / 'COMPLETE_CHECKPOINT_RAW.txt').write_text(captured.getvalue())
    if receipt:
        break
else:
    raise RuntimeError('Three main races; reconcile before retry')
(M / 'COMPLETE_CHECKPOINT_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
assert hashlib.sha256((T / 'FINAL_READINESS.json').read_bytes()).hexdigest() == freeze['readiness_sha256']
print(json.dumps({'result': 'PR789_COMPLETE', 'commit': receipt['commit'],
                  'native': native['commit'], 'doi': native['doi'], 'case_percent': 100,
                  'shard_percent': 92, 'next_pr': 799}))
