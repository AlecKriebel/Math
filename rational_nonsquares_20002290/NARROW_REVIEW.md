# Narrow re-review: rank 463 / problem 20002290

Date: 2026-10-03 UTC

## Verdict: PASS

The revised freeze resolves all five issues identified in the full audit through the seven declared text replacements. The previous textual HOLD is discharged for this revised freeze. The substantive verdict remains **unresolved with partial progress after five attempts**, not a solution of the original problem.

Reviewed source manifest: SHA-256 identified below. Its portable file inventory is REVISED_MANIFEST.json.

Manifest SHA-256: 8c6094abd41583782bab57a2a4a4ba03583d472f4afcbb15497d13d9ef46c18b

Reviewed file inventory: 12 files before adding this narrow review and publication metadata.

## Repairs verified

1. README counting summary now requires that the one-square-atom disjunct contain no rational square. This correctly excludes all-Q branches before asserting the O(sqrt(H)) bound.
2. The one-equation restriction is explicit in the README, Attempt 3's opening, and its theorem application: at most one independent equation total, with no additional witness-only constraints. The value-set presentation is correctly limited to the nonzero free-parameter-coefficient case; parameter-independent branches are handled separately.
3. Attempt 5 now states individual-test avoidance only, explicitly withholding finite satisfiability of the restricted positive type and the full homomorphism counterexample.
4. SOURCE_GATE now states the equivalence to positive-existential definability of both complements together.
5. Attempt 1 now uses the correct 2-adic unit square criterion modulo 8 and removes the problematic root-lifting aside.

No new mathematical claim, argument, attempted resolution, or change to the unresolved boundary was introduced.

## Integrity and control checks

- Original freeze: all 10 listed files still match their original byte counts and SHA-256 hashes.
- Revised freeze: all 12 files match their revised byte counts and SHA-256 hashes; the listed file set equals the directory's file set.
- The original-manifest hash recorded in both revised metadata files matches the actual original manifest.
- Applying exactly the seven RELEASE_CHANGE_MAP.json replacements to the original ten files reproduces every corresponding revised file byte for byte. No undeclared changes were found.
- All old/new file hashes and changed/unchanged flags in the change map are correct.
- INDEPENDENT_AUDIT.md is byte-identical to the original full audit, with SHA-256 43f64f1f42fb6d01571fdf96e493548a2b45fad43138ac58a521f2f5484bdd19. Its HOLD describes the original freeze; this narrow review records clearance of the repairs in the revised freeze.
- verify_identities.py and verification.json are byte-identical to their original versions. A fresh run from a temporary copy passed all eight groups and produced byte-identical JSON.
- Original, revised, and change-map metadata all retain outcome unsolved_with_partial_progress and turns 5.

The controls remain controls, not proofs of uniformity, definability, or nondefinability. Existing conditional hypotheses, restricted-fragment boundaries, prior-credit qualifications, and absence of a full nonsquare formula/counterexample are preserved.

No new mathematical research or proof attempt was performed in this re-review. The two reviewed sets of source files remained unchanged.
