# Postseal crosscheck replay

Keep caller-held final MANIFEST.json and custody_check.py SHA256 pins. The manifest is the sole self-hash exception. No old seal is rewritten.

Set T to /Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp, W=T/priority_classical_crosscheck and S=T/priority_classical_crosscheck_scratch. Replace placeholders with final caller-held pins:

    python3 -B W/custody_check.py --packet W --case-root T --expected-manifest-sha MANIFEST_SHA --expected-checker-sha CHECKER_SHA
    python3 -B -O W/custody_check.py --packet W --case-root T --expected-manifest-sha MANIFEST_SHA --expected-checker-sha CHECKER_SHA

Exact expanded CLI/results are outside the authored packet in S/FINAL_CUSTODY_REPLAY.json. The checker rehashes64 explicit external bindings,4 primary PDF artifacts,4 viewed renders, frozen peer report and old manifest/checker. It also invokes the externally pinned old read-only checker, closing all48 original Gitblobs/51original-source inputs/31old external files. Unrelated RAM folders are outside this scope.

Owned-copy controls:

    python3 -B W/test_custody.py --packet W --case-root T --scratch S

The controls use temporary copies/read-only hardlinks in S, tamper only by replacement/unlink and verify all protected originals afterward. No original or sealed packet is modified. Valid-comment checker tampering must reach explicit external-pin rejection; nonregular cases have5second timeouts. Hostile concurrent filesystem race resistance is not certified.

CUSTODY_TEST_RESULTS records the earlier testing manifest, before including that receipt/final log. The final manifest includes it. Final normal/O positive replays and external pins remain outside the packet to avoid circular hashes. Custody and semantic-flag checks do not formally prove mathematics or certify priority. See REPORT/SOURCE_LEDGER for source scopes, C1 requirement, version comparison and exposure limits. Full third-party bodies/text/renders are outside this flat authored packet. RAM staging requires root preservation.
