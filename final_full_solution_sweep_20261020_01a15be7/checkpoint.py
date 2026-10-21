#!/usr/bin/env python3
"""Publish only this sweep's explicit checkpoint paths onto live main.

Uses a private index and Git plumbing; never checks out, stages in the shared
index, resets, stashes, cleans, creates a branch, or force-pushes. A concurrent
main advance causes a normal push rejection and a safe retry from the new main.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import uuid
from urllib.parse import urlparse
from sweep_io import atomic_json

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
PRIVATE=ROOT/'private'
NAMES=['.gitignore','README.md','RESEARCH_LOG.md','STATE.json',
       'collect_inventory.py','collect_rest_inventory.py',
       'collect_eligibility_evidence.py','checkpoint.py','sweep_io.py',
       'rest_inventory.json','REST_INVENTORY_RECEIPT.json',
       'PR0009_PENDING.json','PR0009_DISPOSITION.json',
       'PR0009_PUBLICATION_LEAD_VERIFICATION.json','dispositions.jsonl',
       'CLASSIFICATION_POLICY.md','INCIDENT_RECOVERY.json','advance_clear_exclusions.py',
       'record_decision.py','publication_check.py','repair_ledger_identity.py','EVIDENCE_COMPACTION.json',
       'CURRENT_CANONICAL_QUEUE_SNAPSHOT.json',
       'advance_with_objects.py','PR0248_LEDGER_REPAIR.json',
       'PR0248_LEDGER_REPAIR_PROPOSAL.json',
       'reviews/range0097_0178_adversary/REVIEW.md',
       'reviews/range0097_0178_adversary/check_results.json',
       'reviews/early_classification_adversary/REVIEW.md',
       'reviews/early_classification_adversary/check_results.json',
       'reviews/early_classification_adversary/GWS_GENERATION_INCIDENT.json',
       'audits/pr0097_10300055/SOURCE_SNAPSHOT.json',
       'audits/pr0097_10300055/CORRECTED_SNAPSHOT.json',
       'audits/pr0097_10300055/DUPLICATE_CHECK.json',
       'audits/pr0097_10300055/ROOT_ORIGINAL_REPRODUCTION.json',
       'audits/pr0097_10300055/ROOT_CORRECTED_REPRODUCTION.json',
       'audits/pr0097_10300055/reviews/math_audit/REVIEW.md',
       'audits/pr0097_10300055/reviews/math_audit/independent_falsification.py',
       'audits/pr0097_10300055/reviews/priority_audit/REVIEW.md',
       'audits/pr0097_10300055/reviews/priority_audit/VERDICT.json',
       'audits/pr0104_600008/SOURCE_SNAPSHOT.json',
       'audits/pr0104_600008/DUPLICATE_CHECK.json',
       'audits/pr0104_600008/ROOT_REPRODUCTION.json',
       'audits/pr0104_600008/ROOT_ANALYTIC_ASSESSMENT.json',
       'audits/pr0104_600008/reviews/geometry_audit/REVIEW.md',
       'audits/pr0104_600008/reviews/geometry_audit/INDEPENDENT_DERIVATION.md',
       'audits/pr0104_600008/reviews/geometry_audit/independent_checks.py',
       'audits/pr0104_600008/reviews/geometry_audit/INDEPENDENT_CHECKS.json',
       'audits/pr0104_600008/reviews/priority_audit/REVIEW.md',
       'audits/pr0104_600008/reviews/priority_audit/DERIVATION.md',
       'audits/pr0104_600008/reviews/priority_audit/VERDICT.json',
       'audits/pr0104_600008/reviews/priority_audit/independent_priority_checks.py',
       'audits/pr0104_600008/reviews/priority_audit/INDEPENDENT_CHECK_RESULTS.json',
       'reviews/inventory_adversary_02/exclusion_review/FINAL_RECHECK.md']
# Explicit completed audit artifacts, selected without raw downloads or ledger snapshots.
NAMES += ['RAW_METADATA_COMPACTION.json', 'eligibility/pr0248.json', 'reviews/range0179_0253_adversary/RESEARCH_LOG.md', 'reviews/range0179_0253_adversary/check_evidence.py', 'reviews/range0179_0253_adversary/eligibility_checks.json', 'reviews/range0179_0253_adversary/canonical_checks.json', 'reviews/range0179_0253_adversary/publication_rechecks_compact.json', 'reviews/pr0248_ledger_repair_adversary/WRAPPER_FINAL_REVIEW.md', 'reviews/pr0248_ledger_repair_adversary/WRAPPER_FINAL_RECEIPT.json', 'reviews/pr0248_ledger_repair_adversary/test_repair_wrapper_revised.py', 'reviews/inventory_adversary_02/compact_inventory_review/REVIEW.md', 'audits/pr0280_30000156/original/FROZEN_MANIFEST.json', 'audits/pr0280_30000156/original/PROOF.md', 'audits/pr0280_30000156/original/RESEARCH_LOG.md', 'audits/pr0280_30000156/original/RESULT.md', 'audits/pr0280_30000156/original/REVIEW_REQUEST.md', 'audits/pr0280_30000156/original/SOURCE_AUDIT.md', 'audits/pr0280_30000156/original/TURN_STATE.json', 'audits/pr0280_30000156/original/checks/output.json', 'audits/pr0280_30000156/original/checks/verify.py', 'audits/pr0280_30000156/original/independent_review/AUTHOR_REPLAY.json', 'audits/pr0280_30000156/original/independent_review/HASH_CHECK.json', 'audits/pr0280_30000156/original/independent_review/INDEPENDENT_CHECKS.json', 'audits/pr0280_30000156/original/independent_review/INDEPENDENT_REVIEW.md', 'audits/pr0280_30000156/original/independent_review/REVIEW_MANIFEST.json', 'audits/pr0280_30000156/original/independent_review/SOURCE_AUDIT.md', 'audits/pr0280_30000156/original/independent_review/independent_check.py', 'audits/pr0280_30000156/original/source_manifest.json', 'audits/pr0280_30000156/SOURCE_SNAPSHOT.json', 'audits/pr0280_30000156/DUPLICATE_CHECK.json', 'audits/pr0280_30000156/ROOT_ANALYTIC_ASSESSMENT.md', 'audits/pr0280_30000156/reviews/arithmetic_falsification/ARITHMETIC_REVIEW.md', 'audits/pr0280_30000156/reviews/arithmetic_falsification/CHECK_RESULTS.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/DISTINCT_CHECKS_INITIAL_RUN.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/DISTINCT_CHECKS_INITIAL_STDERR.txt', 'audits/pr0280_30000156/reviews/arithmetic_falsification/DISTINCT_CHECKS_INITIAL_STDOUT.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/DISTINCT_CHECKS_RUN.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/DISTINCT_CHECKS_STDERR.txt', 'audits/pr0280_30000156/reviews/arithmetic_falsification/DISTINCT_CHECKS_STDOUT.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/FIRST_CHECKPOINT.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/INPUT_SNAPSHOT_VERIFICATION.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/ORIGINAL_RUNTIME_RECEIPT.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/OUTPUT_MANIFEST.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/OUTPUT_MANIFEST.sha256', 'audits/pr0280_30000156/reviews/arithmetic_falsification/RESEARCH_LOG.md', 'audits/pr0280_30000156/reviews/arithmetic_falsification/SOURCE_RECEIPTS.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/SUPPLIED_ANALYTIC_RUN.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/SUPPLIED_ANALYTIC_STDERR.txt', 'audits/pr0280_30000156/reviews/arithmetic_falsification/SUPPLIED_ANALYTIC_STDOUT.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/SUPPLIED_CHECKER_RECEIPT.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/SUPPLIED_FULL_FINITE_RUN.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/SUPPLIED_FULL_FINITE_STDERR.txt', 'audits/pr0280_30000156/reviews/arithmetic_falsification/SUPPLIED_FULL_FINITE_STDOUT.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/VERDICT.json', 'audits/pr0280_30000156/reviews/arithmetic_falsification/distinct_checks.py', 'audits/pr0280_30000156/reviews/arithmetic_falsification/distinct_checks_initial.py', 'audits/pr0280_30000156/reviews/arithmetic_falsification/supplied_analytic.py', 'audits/pr0280_30000156/reviews/arithmetic_falsification/supplied_full_finite.py', 'audits/pr0280_30000156/reviews/source_quantifiers/ARTIFACT_MANIFEST.json', 'audits/pr0280_30000156/reviews/source_quantifiers/DERIVATIONS.md', 'audits/pr0280_30000156/reviews/source_quantifiers/DIAGNOSTICS.json', 'audits/pr0280_30000156/reviews/source_quantifiers/INDEPENDENT_CHECKPOINT.md', 'audits/pr0280_30000156/reviews/source_quantifiers/INPUT_MANIFEST.json', 'audits/pr0280_30000156/reviews/source_quantifiers/RESEARCH_LOG.md', 'audits/pr0280_30000156/reviews/source_quantifiers/REVIEW.md', 'audits/pr0280_30000156/reviews/source_quantifiers/SOURCE_RECEIPTS.json', 'audits/pr0280_30000156/reviews/source_quantifiers/VERDICT.json', 'audits/pr0280_30000156/reviews/source_quantifiers/independent_diagnostics.py']
# Completed PR280 historical-priority evidence, excluding reading images.
NAMES += ['ELIGIBILITY_COLLECTION_RECEIPT.json', 'audits/pr0280_30000156/ROOT_PRIORITY_COMPARISON.md', 'audits/pr0280_30000156/ROOT_REVIEW_INTEGRITY.json', 'audits/pr0280_30000156/LIVE_PR_RECHECK.json', 'audits/pr0280_30000156/CURRENT_AUDIT_STATUS.json', 'audits/pr0280_30000156/reviews/priority_gap/CLASSICAL_COROLLARY_COMPARISON.md', 'audits/pr0280_30000156/reviews/priority_gap/FINAL_REVIEW.md', 'audits/pr0280_30000156/reviews/priority_gap/INPUT_MANIFEST.json', 'audits/pr0280_30000156/reviews/priority_gap/NEW_RETRIEVAL_RECEIPTS.json', 'audits/pr0280_30000156/reviews/priority_gap/OUTPUT_MANIFEST.json', 'audits/pr0280_30000156/reviews/priority_gap/READING_RECEIPTS.json', 'audits/pr0280_30000156/reviews/priority_gap/RESEARCH_LOG.md', 'audits/pr0280_30000156/reviews/priority_gap/VERDICT.json', 'audits/pr0280_30000156/reviews/priority_materiality_challenge/ASSESSMENT.md', 'audits/pr0280_30000156/reviews/priority_materiality_challenge/DERIVATION.md', 'audits/pr0280_30000156/reviews/priority_materiality_challenge/PINNED_HASH_CHECK.json', 'audits/pr0280_30000156/reviews/priority_materiality_challenge/RESEARCH_LOG.md', 'audits/pr0280_30000156/reviews/priority_materiality_challenge/SEARCH_LOG.md', 'audits/pr0280_30000156/reviews/priority_materiality_challenge/SOURCE_RECEIPTS.json', 'audits/pr0280_30000156/reviews/priority_materiality_challenge/SOURCE_SCOPE.md']
# PR292 pinned original and root reconstruction; active reviewer outputs excluded.
NAMES += ['audits/pr0292_30001608/SOURCE_SNAPSHOT.json', 'audits/pr0292_30001608/DUPLICATE_CHECK.json', 'audits/pr0292_30001608/ROOT_ORIGINAL_PACKAGE_INTEGRITY.json', 'audits/pr0292_30001608/ROOT_ANALYTIC_ASSESSMENT.md', 'audits/pr0292_30001608/original/ACCEPTED_MANIFEST.json', 'audits/pr0292_30001608/original/CURRENT_STATE.json', 'audits/pr0292_30001608/original/CURRENT_STATE_ACCEPTED.json', 'audits/pr0292_30001608/original/CURRENT_STATE_TURN_3.json', 'audits/pr0292_30001608/original/CURRENT_STATE_TURN_4.json', 'audits/pr0292_30001608/original/LATEST.md', 'audits/pr0292_30001608/original/RESEARCH_LOG.md', 'audits/pr0292_30001608/original/RESEARCH_LOG_TURN_2.md', 'audits/pr0292_30001608/original/RESEARCH_LOG_TURN_3.md', 'audits/pr0292_30001608/original/RESEARCH_LOG_TURN_4.md', 'audits/pr0292_30001608/original/RESULT.md', 'audits/pr0292_30001608/original/RESULT_ACCEPTED.md', 'audits/pr0292_30001608/original/SOURCE_AUDIT.md', 'audits/pr0292_30001608/original/SOURCE_RECHECK_TURN_4.md', 'audits/pr0292_30001608/original/TURN_1.md', 'audits/pr0292_30001608/original/TURN_1_MANIFEST.json', 'audits/pr0292_30001608/original/TURN_2.md', 'audits/pr0292_30001608/original/TURN_2_MANIFEST.json', 'audits/pr0292_30001608/original/TURN_3.md', 'audits/pr0292_30001608/original/TURN_3_MANIFEST.json', 'audits/pr0292_30001608/original/TURN_4.md', 'audits/pr0292_30001608/original/TURN_4_MANIFEST.json', 'audits/pr0292_30001608/original/TURN_STATE.json', 'audits/pr0292_30001608/original/checks/independent_review_portable.py', 'audits/pr0292_30001608/original/checks/turn1_checks.py', 'audits/pr0292_30001608/original/checks/turn1_output.json', 'audits/pr0292_30001608/original/checks/turn2_checks.py', 'audits/pr0292_30001608/original/checks/turn2_output.json', 'audits/pr0292_30001608/original/checks/turn3_checks.py', 'audits/pr0292_30001608/original/checks/turn3_output.json', 'audits/pr0292_30001608/original/checks/turn4_checks.py', 'audits/pr0292_30001608/original/checks/turn4_output.json', 'audits/pr0292_30001608/original/prior/SOURCE_AUDIT.md', 'audits/pr0292_30001608/original/review/ADVERSARIAL_REVIEW.md', 'audits/pr0292_30001608/original/review/REVIEW_MANIFEST.json', 'audits/pr0292_30001608/original/review/author_rerun.json', 'audits/pr0292_30001608/original/review/independent_check.py', 'audits/pr0292_30001608/original/review/independent_checks.json', 'audits/pr0292_30001608/original/source_manifest.json', 'audits/pr0292_30001608/original/verify_package.py']
DESTINATION='https://github.com/AlecKriebel/Math.git'
TRANSPORT_REMOTE='origin'
TRANSPORT=['git','-c','remote.'+TRANSPORT_REMOTE+'.url='+DESTINATION,
           '-c','remote.'+TRANSPORT_REMOTE+'.pushurl='+DESTINATION]


def run(args,*,env=None,input=None,check=True):
    p=subprocess.run(args,cwd=REPO,env=env,input=input,capture_output=True)
    if check and p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[:2000])
    return p


def live_main():
    p=run(['gh','api','--hostname','github.com','repos/AlecKriebel/Math/git/ref/heads/main'])
    return json.loads(p.stdout)['object']['sha']


def verify_destination():
    urls=run(TRANSPORT+['remote','get-url','--push','--all',TRANSPORT_REMOTE]).stdout.decode().splitlines()
    fetch_urls=run(TRANSPORT+['remote','get-url','--all',TRANSPORT_REMOTE]).stdout.decode().splitlines()
    def intended(url):
        if url.startswith('git@github.com:'):
            return url[len('git@github.com:'):].removesuffix('.git').lower()=='aleckriebel/math'
        parsed=urlparse(url)
        return (parsed.scheme=='https' and parsed.hostname=='github.com'
                and not parsed.username and not parsed.password and not parsed.query
                and not parsed.fragment and parsed.path.rstrip('/').removesuffix('.git').lower()=='/aleckriebel/math')
    if len(urls)!=1 or not fetch_urls or not all(intended(url) for url in urls+fetch_urls):
        raise RuntimeError('Effective push destination does not match the intended repository; no push attempted')
    return urls[0]


def ensure_commit(sha):
    p=run(['git','cat-file','-e',sha+'^{commit}'],check=False)
    if p.returncode:
        verify_destination()
        run(TRANSPORT+['fetch','--no-tags','--no-write-fetch-head',TRANSPORT_REMOTE,sha])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--message',default='Checkpoint exhaustive final-sweep inventory and ledger-access blocker')
    args=parser.parse_args()
    destination=verify_destination()
    selected=[]
    # Named per-PR receipts are authored only in this dedicated effort folder.
    # This is a filename whitelist, not a shared-worktree git add or broad glob.
    receipt_names=sorted(p.name for p in ROOT.iterdir()
                         if re.fullmatch(r'PR\d{4}_(?:DISPOSITION|PUBLICATION_VERIFICATION|LEDGER_REPAIR|LEDGER_REPAIR_PROPOSAL)\.json',p.name))
    for name in dict.fromkeys(NAMES+receipt_names):
        path=ROOT/name
        relative=Path(name)
        parts=[ROOT.joinpath(*relative.parts[:n]) for n in range(1,len(relative.parts)+1)]
        if (relative.is_absolute() or '..' in relative.parts
                or any(part.is_symlink() for part in parts)
                or not path.is_file() or not path.resolve().is_relative_to(ROOT.resolve())):
            raise RuntimeError(f'Unsafe or absent checkpoint path: {name}')
        selected.append((str(path.relative_to(REPO)),path.read_bytes()))
    parent=live_main()
    receipt={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),
             'remote_main_parent':parent,'execute':args.execute,
             'files':[{'path':p,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for p,b in selected],
             'completion_estimate_percent':json.loads((ROOT/'STATE.json').read_text())['completion_estimate_percent'],
             'mechanism':'private Git index; commit-tree on fresh live main; ordinary non-force push; shared index/worktree untouched'}
    if not args.execute:
        print(json.dumps(receipt,indent=2))
        return
    PRIVATE.mkdir(exist_ok=True)
    index=PRIVATE/f'checkpoint-index-{uuid.uuid4().hex}'
    env=os.environ.copy()
    env['GIT_INDEX_FILE']=str(index)
    try:
        for attempt in range(3):
            parent=live_main()
            ensure_commit(parent)
            run(['git','read-tree',parent],env=env)
            for path,content in selected:
                blob=run(['git','hash-object','-w','--stdin'],input=content).stdout.decode().strip()
                run(['git','update-index','--add','--cacheinfo','100644,'+blob+','+path],env=env)
            tree=run(['git','write-tree'],env=env).stdout.decode().strip()
            parent_tree=run(['git','rev-parse',parent+'^{tree}']).stdout.decode().strip()
            if tree==parent_tree:
                receipt.update(status='already_recorded',commit=parent)
                break
            commit=run(['git','commit-tree',tree,'-p',parent],input=(args.message+'\n').encode()).stdout.decode().strip()
            changed=run(['git','diff-tree','--no-commit-id','--name-only','-r',commit]).stdout.decode().splitlines()
            allowed={p for p,_ in selected}
            if not set(changed)<=allowed:
                raise RuntimeError('Commit unexpectedly modifies unowned paths')
            if verify_destination()!=destination:
                raise RuntimeError('Push destination changed during checkpoint; no push attempted')
            push=run(TRANSPORT+['push',TRANSPORT_REMOTE,commit+':refs/heads/main'],check=False)
            if push.returncode:
                error=push.stderr.decode(errors='replace')
                if attempt<2 and ('non-fast-forward' in error or 'fetch first' in error):
                    continue
                raise RuntimeError(error[:2000])
            after=live_main()
            ensure_commit(after)
            ancestry=run(['git','merge-base','--is-ancestor',commit,after],check=False)
            if ancestry.returncode:
                raise RuntimeError('Pushed commit ancestry could not be verified on live main')
            receipt.update(status='pushed_and_verified',commit=commit,
                           remote_main_parent=parent,live_main_after_push=after,
                           changed_paths=changed)
            break
        atomic_json(ROOT/'LATEST_CHECKPOINT_RECEIPT.json',receipt)
        print(json.dumps(receipt,indent=2))
    finally:
        index.unlink(missing_ok=True)
        Path(str(index)+'.lock').unlink(missing_ok=True)


if __name__=='__main__':
    main()

# PR292 completed-family and package checkpoint selection.
NAMES.extend(['audits/pr0292_30001608/reviews/foster_recheck_02/ANALYTIC_RECHECK.md', 'audits/pr0292_30001608/reviews/foster_recheck_02/FINAL_REVIEW.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/FINAL_REVIEW.md', 'audits/pr0292_30001608/reviews/foster_recheck_02/INDEPENDENT_INITIAL_DERIVATION.md', 'audits/pr0292_30001608/reviews/foster_recheck_02/REPLAY_AND_SOURCE_INTEGRITY.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/RESEARCH_LOG.md', 'audits/pr0292_30001608/reviews/foster_recheck_02/exact_falsification.py', 'audits/pr0292_30001608/reviews/foster_recheck_02/exact_falsification.stderr', 'audits/pr0292_30001608/reviews/foster_recheck_02/exact_falsification_output.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/original_independent_replay.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/original_independent_replay.stderr', 'audits/pr0292_30001608/reviews/foster_recheck_02/original_turn1_replay.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/original_turn2_replay.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/original_turn3_replay.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/original_turn4_replay.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/original_turn4_replay.stderr', 'audits/pr0292_30001608/reviews/foster_recheck_02/original_verify_package_replay.json', 'audits/pr0292_30001608/reviews/foster_recheck_02/verify_evidence.py', 'audits/pr0292_30001608/reviews/foster_recheck_02/EVIDENCE_MANIFEST.json', 'audits/pr0292_30001608/reviews/source_recheck_02/CONTROL_RESULTS.json', 'audits/pr0292_30001608/reviews/source_recheck_02/EARLY_SOURCE_MODEL_CHECKPOINT.md', 'audits/pr0292_30001608/reviews/source_recheck_02/LIMITING_DERIVATION.md', 'audits/pr0292_30001608/reviews/source_recheck_02/PRIMARY_INVENTORY.json', 'audits/pr0292_30001608/reviews/source_recheck_02/READING_LEDGER.json', 'audits/pr0292_30001608/reviews/source_recheck_02/REPORT.md', 'audits/pr0292_30001608/reviews/source_recheck_02/RESEARCH_LOG.md', 'audits/pr0292_30001608/reviews/source_recheck_02/SNAPSHOT_RECEIPT.json', 'audits/pr0292_30001608/reviews/source_recheck_02/VERDICT.json', 'audits/pr0292_30001608/reviews/source_recheck_02/WEB_ACCESS_RECEIPT.json', 'audits/pr0292_30001608/reviews/source_recheck_02/independent_controls.py', 'audits/pr0292_30001608/reviews/source_recheck_02/FINAL_SEAL.json', 'audits/pr0292_30001608/reviews/priority_recheck_02/REPORT.md', 'audits/pr0292_30001608/reviews/priority_recheck_02/DERIVATIONS.md', 'audits/pr0292_30001608/reviews/priority_recheck_02/READING_LEDGER.json', 'audits/pr0292_30001608/reviews/priority_recheck_02/QUERY_SCOPE.json', 'audits/pr0292_30001608/reviews/priority_recheck_02/DISPOSITION.json', 'audits/pr0292_30001608/reviews/priority_recheck_02/RESEARCH_LOG.md', 'audits/pr0292_30001608/reviews/priority_recheck_02/identity_controls.py', 'audits/pr0292_30001608/reviews/priority_recheck_02/identity_controls.stdout', 'audits/pr0292_30001608/reviews/priority_recheck_02/theorem_transfer_control.py', 'audits/pr0292_30001608/reviews/priority_recheck_02/theorem_transfer_control.stdout', 'audits/pr0292_30001608/reviews/priority_recheck_02/false_identity_result.json', 'audits/pr0292_30001608/CURRENT_AUDIT_STATUS.json', 'audits/pr0292_30001608/ROOT_REVIEW_INTEGRITY.json', 'audits/pr0292_30001608/preprint/main.tex', 'audits/pr0292_30001608/preprint/reproduce.py', 'audits/pr0292_30001608/preprint/PACKAGE_README.md', 'audits/pr0292_30001608/preprint/build_publication.py', 'audits/pr0292_30001608/preprint/PDF_VISUAL_QA.json', 'audits/pr0292_30001608/preprint/ROOT_REPRODUCTION.stdout.json', 'audits/pr0292_30001608/preprint/ROOT_REPRODUCTION_RECEIPT.json', 'audits/pr0292_30001608/preprint/build/BUILD_RECEIPT.json', 'audits/pr0292_30001608/preprint/publication/PACKAGE_BUILD_RECEIPT.json', 'audits/pr0292_30001608/preprint/publication/RELEASE_FILES.json', 'audits/pr0292_30001608/preprint/publication/zenodo-deposit.json', 'audits/pr0292_30001608/preprint/publication/dfc_stability_verification/MANIFEST.json', 'reviews/range0254_0279_finish/CHECKER_SAFETY_REVIEW.json', 'reviews/range0254_0279_finish/CLASSIFICATION_TABLE.json', 'reviews/range0254_0279_finish/FOLLOWUP_CHECK_RECEIPT.json', 'reviews/range0254_0279_finish/PRIMARY_SOURCE_RECHECK.json', 'reviews/range0254_0279_finish/PROVENANCE_ANNOTATIONS.json', 'reviews/range0254_0279_finish/PUBLICATION_IDENTITIES.json', 'reviews/range0254_0279_finish/REFRESH_SUMMARY.json', 'reviews/range0254_0279_finish/REPLAY_CHECK_RECEIPT.json', 'reviews/range0254_0279_finish/REPORT.md', 'reviews/range0254_0279_finish/RESEARCH_LOG.md', 'reviews/range0254_0279_finish/SOURCE_HASHES.json', 'reviews/range0254_0279_finish/SOURCE_SCOPE_REVIEW.json', 'reviews/range0254_0279_finish/check_followup.py', 'reviews/range0254_0279_finish/live_prs_refresh.json', 'reviews/range0254_0279_finish/protected_input_hashes_before.json', 'reviews/range0254_0279_finish/publications_refresh.json', 'reviews/range0254_0279_finish/refresh_readonly.py', 'reviews/range0254_0279_finish/replay_check_evidence.py', 'reviews/range0254_0279_finish/FINAL_ARTIFACT_MANIFEST.json'])

# Explicit reviewed PR292 binary asset and checkpoint-safety evidence selection.
NAMES.extend(['reviews/pr292_checkpoint_binary_safety/REPORT.md', 'reviews/pr292_checkpoint_binary_safety/RESEARCH_LOG.md', 'reviews/pr292_checkpoint_binary_safety/CONTROL_RESULTS.json', 'reviews/pr292_checkpoint_binary_safety/PAYLOAD_CONTROLS.json', 'reviews/pr292_checkpoint_binary_safety/API_EVENT_SUMMARY.json', 'reviews/pr292_checkpoint_binary_safety/ALLOWLIST_REVIEW.json', 'reviews/pr292_checkpoint_binary_safety/SOURCE_BINDING_INITIAL.json', 'reviews/pr292_checkpoint_binary_safety/SOURCE_BINDING_FINAL.json', 'reviews/pr292_checkpoint_binary_safety/DOCUMENTATION_SOURCES.json', 'reviews/pr292_checkpoint_binary_safety/independent_controls.py', 'reviews/pr292_checkpoint_binary_safety/reviewed_remote_checkpoint.py', 'reviews/pr292_checkpoint_binary_safety/reviewed_checkpoint.py', 'reviews/pr292_checkpoint_binary_safety/reviewed_sweep_io.py', 'reviews/pr292_checkpoint_binary_safety/FINAL_SEAL.json', 'audits/pr0292_30001608/preprint/publication/dfc_stability.pdf', 'audits/pr0292_30001608/preprint/publication/dfc_stability_verification.zip', 'audits/pr0292_30001608/prepublication_check.py', 'audits/pr0292_30001608/ACCOUNT_QUERY_PRELIMINARY.json', 'audits/pr0292_30001608/ACCOUNT_QUERY_BROAD_PRELIMINARY.json', 'audits/pr0292_30001608/BINARY_CHECKPOINT_ACCEPTANCE.json'])

# PR292 first full-package review and actual binary readback.
NAMES.extend(['audits/pr0292_30001608/reviews/package_adversary_01/INDEPENDENT_INITIAL_DERIVATION.md', 'audits/pr0292_30001608/reviews/package_adversary_01/PR_METADATA_READ_ONLY.json', 'audits/pr0292_30001608/reviews/package_adversary_01/QUERY_SCOPE.json', 'audits/pr0292_30001608/reviews/package_adversary_01/READING_LEDGER.json', 'audits/pr0292_30001608/reviews/package_adversary_01/REPORT.md', 'audits/pr0292_30001608/reviews/package_adversary_01/RESEARCH_LOG.md', 'audits/pr0292_30001608/reviews/package_adversary_01/VERDICT.json', 'audits/pr0292_30001608/reviews/package_adversary_01/input_hashes.json', 'audits/pr0292_30001608/reviews/package_adversary_01/own_exact_checks.py', 'audits/pr0292_30001608/reviews/package_adversary_01/own_exact_checks.stderr', 'audits/pr0292_30001608/reviews/package_adversary_01/own_exact_checks.stdout', 'audits/pr0292_30001608/reviews/package_adversary_01/own_priority_controls.py', 'audits/pr0292_30001608/reviews/package_adversary_01/own_priority_controls.stderr', 'audits/pr0292_30001608/reviews/package_adversary_01/own_priority_controls.stdout', 'audits/pr0292_30001608/reviews/package_adversary_01/package_consistency.json', 'audits/pr0292_30001608/reviews/package_adversary_01/paper.txt', 'audits/pr0292_30001608/reviews/package_adversary_01/reproduction.stderr', 'audits/pr0292_30001608/reviews/package_adversary_01/reproduction.stdout', 'audits/pr0292_30001608/reviews/package_adversary_01/snapshot_verification.json', 'audits/pr0292_30001608/reviews/package_adversary_01/wrapper_adversary.py', 'audits/pr0292_30001608/reviews/package_adversary_01/wrapper_adversary.stderr', 'audits/pr0292_30001608/reviews/package_adversary_01/wrapper_adversary.stdout', 'audits/pr0292_30001608/reviews/package_adversary_01/FINAL_SEAL.json', 'audits/pr0292_30001608/ROOT_PACKAGE_REVIEW_01_ACCEPTANCE.json', 'audits/pr0292_30001608/BINARY_CHECKPOINT_READBACK.json', 'audits/pr0292_30001608/MAIN_INTEGRATION_PRELIMINARY.json'])

# PR292 final complete-package review acceptance and publication readiness.
NAMES.extend(['audits/pr0292_30001608/reviews/package_adversary_02/BUILD_RECHECK.json', 'audits/pr0292_30001608/reviews/package_adversary_02/INDEPENDENT_INITIAL_DERIVATION.md', 'audits/pr0292_30001608/reviews/package_adversary_02/INTEGRITY_RECHECK.json', 'audits/pr0292_30001608/reviews/package_adversary_02/PACKAGE_READING_INVENTORY.json', 'audits/pr0292_30001608/reviews/package_adversary_02/PDF_QA_RECHECK.json', 'audits/pr0292_30001608/reviews/package_adversary_02/PRIORITY_AND_TRANSFER_DERIVATIONS.md', 'audits/pr0292_30001608/reviews/package_adversary_02/QUERY_SCOPE.json', 'audits/pr0292_30001608/reviews/package_adversary_02/READING_LEDGER.json', 'audits/pr0292_30001608/reviews/package_adversary_02/REPORT.md', 'audits/pr0292_30001608/reviews/package_adversary_02/REPRODUCE_REVIEW.md', 'audits/pr0292_30001608/reviews/package_adversary_02/RESEARCH_LOG.md', 'audits/pr0292_30001608/reviews/package_adversary_02/VERDICT.json', 'audits/pr0292_30001608/reviews/package_adversary_02/WRAPPER_MUTATION_RESULTS.json', 'audits/pr0292_30001608/reviews/package_adversary_02/ZENODO_PAPER_ACCESS.json', 'audits/pr0292_30001608/reviews/package_adversary_02/ZENODO_SOURCE_ACCESS.json', 'audits/pr0292_30001608/reviews/package_adversary_02/candidate_identity.json', 'audits/pr0292_30001608/reviews/package_adversary_02/independent_controls.py', 'audits/pr0292_30001608/reviews/package_adversary_02/independent_controls.stderr.txt', 'audits/pr0292_30001608/reviews/package_adversary_02/independent_controls.stdout.json', 'audits/pr0292_30001608/reviews/package_adversary_02/priority_controls.py', 'audits/pr0292_30001608/reviews/package_adversary_02/priority_controls.stderr.txt', 'audits/pr0292_30001608/reviews/package_adversary_02/priority_controls.stdout.json', 'audits/pr0292_30001608/reviews/package_adversary_02/reproduction.stderr.txt', 'audits/pr0292_30001608/reviews/package_adversary_02/reproduction.stdout.json', 'audits/pr0292_30001608/reviews/package_adversary_02/verify_review.py', 'audits/pr0292_30001608/reviews/package_adversary_02/wrapper_controls.py', 'audits/pr0292_30001608/reviews/package_adversary_02/wrapper_controls.stderr.txt', 'audits/pr0292_30001608/reviews/package_adversary_02/wrapper_controls.stdout.json', 'audits/pr0292_30001608/reviews/package_adversary_02/FINAL_SEAL.json', 'audits/pr0292_30001608/ROOT_PUBLICATION_CLEARANCE.json', 'audits/pr0292_30001608/ACCOUNT_INVENTORY_RECONCILIATION.json', 'audits/pr0292_30001608/ROOT_ACCOUNT_MODEL_RECONCILIATION.md', 'audits/pr0292_30001608/PLANNED_PR_PUBLICATION_UPDATE.json', 'audits/pr0292_30001608/PREPUBLICATION_BEFORE_INTEGRATION_322da7e39ffc4164ab2990451b971e3f.json'])

# Fresh PR292 integration identity gate and complete-inventory duplicate comparison.
NAMES.extend(['audits/pr0292_30001608/PREPUBLICATION_BEFORE_INTEGRATION_c863fb95cc0148199b85ec38c4f8d98b.json', 'audits/pr0292_30001608/CROSS_PR_DUPLICATE_RECHECK.json'])

# Exact PR292 integration, publication and unique tracker read-back evidence.
NAMES.extend(['eligibility/pr0292.json', 'PR0292_PUBLICATION_LEADS.json', 'audits/pr0292_30001608/PR_BRANCH_PUBLICATION_COMMIT.json', 'audits/pr0292_30001608/TEST_MERGE_PREFLIGHT.json', 'audits/pr0292_30001608/MERGE_INTEGRATION_ACCEPTANCE.json', 'audits/pr0292_30001608/MERGE_RECEIPT.json', 'audits/pr0292_30001608/ACCOUNT_BEFORE_STAGE_RECONCILIATION.json', 'audits/pr0292_30001608/ACCOUNT_BEFORE_PUBLISH_RECONCILIATION.json', 'audits/pr0292_30001608/ZENODO_STAGE.json', 'audits/pr0292_30001608/ZENODO_DRAFT_INSPECTION.json', 'audits/pr0292_30001608/ZENODO_PUBLISH.json', 'audits/pr0292_30001608/ZENODO_PUBLISHED_INSPECTION.json', 'audits/pr0292_30001608/record_publication_ledger.py', 'audits/pr0292_30001608/LEDGER_APPEND_INTENT.json', 'audits/pr0292_30001608/LEDGER_APPEND_RESPONSE.json', 'audits/pr0292_30001608/LEDGER_PUBLICATION_VERIFICATION.json', 'audits/pr0292_30001608/PR_METADATA_AFTER_PUBLICATION.json', 'audits/pr0292_30001608/PREPUBLICATION_BEFORE_STAGE_b23f213fb7d14ef88ddb83241360f6c7.json', 'audits/pr0292_30001608/PREPUBLICATION_BEFORE_PUBLISH_c687dccd21514d9f9e6b8123b3ec8731.json', 'audits/pr0292_30001608/PREPUBLICATION_BEFORE_PUBLISH_0c26584428c449b889d52698135b7fbb.json', 'audits/pr0292_30001608/PREPUBLICATION_BEFORE_LEDGER_f556ca372fdb48f2be6973e5b337cd70.json', 'audits/pr0292_30001608/PREPUBLICATION_BEFORE_INTEGRATION_710689889429445ba0ba386b4293208b.json'])
