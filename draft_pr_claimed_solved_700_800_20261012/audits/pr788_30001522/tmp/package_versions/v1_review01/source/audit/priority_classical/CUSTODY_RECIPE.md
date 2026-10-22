# Classical priority custody recipe

The caller must retain the final MANIFEST.json and custody_check.py SHA256 pins outside this packet. MANIFEST.json is the sole authored self-hash exception. The initial and provisional independent positions are separately hard-pinned by the checker.

Set T to /Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp, W=T/priority_classical, I=T/intake and S=T/priority_classical_scratch. Replace the two placeholders with the final caller-held pins:

    python3 -B W/custody_check.py --packet W --input-root I --expected-manifest-sha MANIFEST_SHA --expected-checker-sha CHECKER_SHA --source-root S
    python3 -B -O W/custody_check.py --packet W --input-root I --expected-manifest-sha MANIFEST_SHA --expected-checker-sha CHECKER_SHA --source-root S

Exact expanded argument arrays and results are preserved outside the packet in S/FINAL_CUSTODY_REPLAY.json. It is safe to rehome the three roots together while keeping the same relative files and caller-held pins.

The checker closes all authored flat files, the full selected/prior record, eligibility/head/source identity, all48 original SHA256/Git blobs and51 protected source inputs. The sole excluded intake process file is ongoing RESEARCH_LOG.md; no original or record is excluded. It also binds10 full primary PDF artifact identities,31 external scratch evidence-file rows, exact query count/read-scope limitations and bounded verdict. With --source-root, every external row is rehashed; without it, source hashes remain recorded but the missing bodies are not claimed independently replayed. Full bodies and renders stay outside this authored packet.

Own copied-input controls:

    python3 -B W/test_custody.py --packet W --input-root I --scratch S

This writes only temporary copies in S and removes them. For storage economy, copied external baselines use read-only hardlinks, and all tampering uses replacement/unlink. Original byte identities are rechecked. It does not mutate the sealed W or original I/source bodies. Negative controls must fail with the checker's CUSTODY_FAIL diagnostic; the checker tamper is valid Python comment text and specifically exercises the caller-held checker pin. Nonregular controls have a5-second timeout. No hostile concurrent-filesystem security certificate is claimed.

CUSTODY_TEST_RESULTS records the earlier testing manifest before that receipt/final log were included. The final manifest includes that receipt. Final positive normal/optimized immutable replays and the external pin are outside the closed packet to avoid circular hashes.

This is a priority evidence/custody audit, not a fresh mathematical proof turn, firstness certificate or comprehensive predecessor exclusion. Reused-session exposure and inaccessible/unread literature are explicit. RAM staging is the actual location. Root handles durable preservation and publication.
