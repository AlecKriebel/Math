# Logarithmic deletion: audited partial results

Problem 30003081 / OWR-14222-009, rank 992. **Unsolved, 5/5 approaches.**

Read [publication acceptance](PUBLICATION_ACCEPTANCE.md), the [authored result](original/RESULT.md), all five authored approaches and the [full independent mathematical audit](independent_audit/REPORT.md). The broad primary-source question is higher-dimensional logarithmic deletion. The historical catalogue title about unexpected curves is preserved only as catalogue metadata.

The credited Abe–Kawanoue seven-plane example obstructs one natural unrestricted quotient. Conditional positive theorems and defect criteria are accepted; they do not settle the source's general request. Trok's separate codimension-two result is not a general-fat-point characterization in dimension greater than two. There is no mathematical correction patch. The separate corrected slice adopts only an optional SyntaxError diagnostic improvement; originals already fail closed. The frozen audit patch has an off-by-one hunk header. `HARDENING_REPLAY.patch` repairs only its declared start offsets, and exact header derivation plus patch replay are verified.

## Reproduce

Use Python 3 with the standard library. Obtain the outer-manifest and verifier SHA-256 pins from a separately trusted publication record, and authenticate `VERIFY_PUBLICATION.py` before running it. A verifier cannot establish its own initial trust merely by reading hashes shipped beside itself.

After authentication:

    python3 -I -B VERIFY_PUBLICATION.py --packet . --expected-manifest TRUSTED_OUTER_SHA256
    python3 -I -B -O VERIFY_PUBLICATION.py --packet . --expected-manifest TRUSTED_OUTER_SHA256
    python3 -I -B -OO VERIFY_PUBLICATION.py --packet . --expected-manifest TRUSTED_OUTER_SHA256

Each default invocation replays all three child optimization modes. `--mode ordinary`, `--mode optimized` or `--mode double_optimized` selects one child mode; `--check-only` authenticates bytes and exact patch derivation without executing the finite suites.

After authenticating the mutation program through the pinned inventory:

    python3 -I -B TEST_MUTATIONS.py --packet . --expected-manifest TRUSTED_OUTER_SHA256 --expected-verifier TRUSTED_VERIFIER_SHA256

The mutation program runs the externally pinned verifier through an independent bootstrap. This rejects a replaced or symlinked verifier before executing it. The original and audit finite mutation suites use a writable disposable staging copy, so a read-only checkout can be reproduced without altering its bytes. No proof corpus or source PDF is needed or distributed. Exact source reverification is NOT_RUN unless the optional checker is explicitly supplied with matching source bytes. Omitted input does not count as a source-check pass.

The frozen manifests and all publication members are pinned. The 16-file original and 16-file independent audit are byte-for-byte preserved; the 16-file corrected slice differs only in the diagnostic catch and its manifest. `MUTATION_RESULTS.json` records deterministic publication-level fault controls; the full audit contains the earlier independent controls and written review. Test logs and remote verification receipts are separate from this immutable packet.

Integrity and finite replay are distinct from mathematical acceptance. These AI-assisted, unrefereed partial results make no human-peer-review, formal-verification, novelty or worldwide-literature-completeness claim.
