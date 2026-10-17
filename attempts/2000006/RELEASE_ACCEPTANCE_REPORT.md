# Independent release acceptance: E-6322 checkpoint, revision 2

16 October 2026.

## Verdict

**Accepted for release at the exact identity below.** The optimization-disabled verification blocker in the earlier candidate is closed. No release blocker remains in this reviewed revision.

This is acceptance of preservation, packaging, publication boundaries and the stated computational reproduction. It is not a new mathematical pass, a proof of E-6322, a counterexample, a novelty determination or formal proof certification. The mathematical status remains **UNSOLVED 5/5**.

## Accepted frozen identity

- Public files: **126**
- Total uncompressed public-file bytes, including the manifest: **858,703**
- `PACKAGE_MANIFEST.json` SHA-256: `104655a3116633b2e46c2b49252bfb896bed6b8576ffcce0051363e51ce91ac3`
- Archive: `elasticity_1791_checkpoint_v2.tar.gz`
- Archive bytes: **288,749**
- Archive SHA-256: `8947f3d63d14a7a4c3a545cbbe1ec6d80d2cdfddc526786340d674ae1627d572`

Every archive entry was independently checked against the frozen public files, byte-for-byte. There are no additional archive members or missing payload files. Manifest identities and file contents remained unchanged through the review. The earlier candidate identified by manifest SHA-256 `f4d4451d1a7573be583d474ebec2bb88ce1f2178745b67231cab30eec4f04b9a` remains held; this acceptance applies only to revision 2.

## Resolution of the release blocker

The reviewer inspected the repaired wrappers and independently exercised their failure behavior.

- Public verification and replay gates now use explicit exceptions. AST inspection confirms no removable Python assertion statements in `verify.py`, `replay.py` or `test_release_guards.py`.
- Historical checkers are launched without optimization flags, with interpreter-environment flags ignored and an explicit optimization-level-zero check before execution.
- `PYTHONOPTIMIZE` is removed from the child environment. The unchanged final exact checker's nested historical subprocesses therefore retain assertions as well.
- Expected generated output files are removed before direct checker execution in disposable copies. A zero exit without new output is rejected rather than credited using a saved historical result.
- Child failures, output mismatches and changed adapted-check lists raise errors. The public checkpoint is checked before and after replay.

The preserved original historical scripts remain assertion-based. Their supported verification route is the guarded public replay. The documentation explicitly warns against treating direct optimized invocation of an original checker as valid verification.

## Independent reproduction and adversarial controls

The reviewer reran the entire supplied 72-control matrix with the control harness itself launched using `-OO` and inherited `PYTHONOPTIMIZE=2`. It passed and produced **byte-identical** results to the frozen `RELEASE_GUARD_RESULTS.json`:

`723a6985f060c9a4c940ec03608f66265e71a35ac3ef24893be89129bc3d2cc9`

The matrix includes six clean full replay modes and 66 rejected negative cases:

- Normal, `-O`, `-OO`, inherited optimization levels 1 and 2, and combined flag/environment execution
- Same-length terminal-status corruption; unexpected and missing files
- Malformed or wrongly typed manifests and false manifest status
- False final and nested exact mathematical identities
- Nonzero child exit, zero child exit without output, and changed child output

The semantic negative fixtures deliberately reseal their isolated file and audit-chain records. Their integrity checks pass first; their computations or execution are then rejected for the expected reason. This demonstrates that active mathematical/execution gates, rather than stale hashes alone, reject the invalid cases.

The reviewer also authored and passed **36 additional independent negative controls**, covering duplicate manifest paths, parent traversal, symlinks, wrong Boolean types, incorrect byte counts and original-artifact hash corruption across six normal/optimized/inherited modes. All rejected invalid inputs with nonzero status and no successful verification output.

Finally, the reviewer extracted the sealed archive into a fresh temporary location and ran replay from a working directory outside the extracted package using `-OO` plus `PYTHONOPTIMIZE=2`. It passed, left every extracted file unchanged, and reproduced the saved replay bytes exactly:

`09ff79e6bcd18bbb7089a93c5008aada63feb8b42edcf68d7ff027d6cfaefabc`

No optimization mode silently skipped verification or counted a skipped computation as passed.

## Preservation of accepted research

All **109 original artifacts, totaling 720,572 bytes**, independently compare byte-for-byte to the accepted research originals. These include 63 complete authored mathematical Markdown reports plus the frozen target, original tests and results, public source metadata and all five original audit manifests. No accepted original was edited for the repair.

The original audit-chain record counts remain 19, 21, 23 and 22 for passes 1–4, totaling 85, and 30 for pass 5. These are record occurrences, including repeated chain references, not counts of independent mathematical evidence.

Relative to the held candidate, revision 2 adds only the portability explanation, reproducible release-control script and public control results. Changes to existing files are confined to the portable verifier, replay wrapper, their records/manifest and reproduction documentation. The mathematical narratives, original scripts, original audit artifacts and PDF-check adapters remain unchanged.

## Mathematical and source-check scope

The benchmark remains the arbitrary-positive-coefficient, three-dimensional 6,3,2,-2 density with the full finite-energy competitor class, arbitrary allowed smooth diffeomorphic full-boundary data and an individual-minimizer positive essential determinant bound over the entire domain. Neither an unconditional theorem nor a compliant globally minimizing counterexample is claimed.

The accepted auxiliary results retain their regularity, admissibility, determinant-sign, scaling and comparison hypotheses. Boundary-only degeneration, missing tangent existence, remaining singular profiles and the absent uniform high-level repair estimate are not represented as resolved. Ball's original broader adequate-growth question remains explicitly distinguished from this fixed benchmark.

Fresh replay retains the verified scope:

- 12 direct jobs and four nested earlier exact replays
- 201 exact checks and 14 quadrature comparisons
- All five positivity outputs, including 28 final checks
- Original pass-1 scaling and audit outputs
- 57 final audit controls
- 15, 27 and 39 retained mathematical audit checks from passes 2, 3 and 4

Exactly 12 historical PDF byte/hash checks remain explicitly outside fresh replay: nine from pass 2, two from pass 3 and one from pass 4. The adapters and their declared omitted-block hashes were reviewed in the preceding release review and are unchanged. These are historical source-document verification omissions, not removed mathematical checks. Their earlier metadata is retained, and they are not counted as freshly passed. No external source download is required or performed.

## Publication boundary

The frozen archive contains the complete authored research/audit deliverables, public bibliographic and verification metadata, and portable reproduction additions. Review of the retained payload and the revision's exact changes found no copied third-party PDFs, extracted source texts, rendered source pages, dataset contents, private sources, personal data, private coordination files, secrets, private chat links or workspace paths in the mathematical payload.

Build scripts, staging receipts, raw queue fetches, held release files and review working files are outside the approved mathematical payload. This acceptance report is also external to the frozen package. Adding it or any other file inside that package changes its identity and requires resealing; it may instead accompany the exact package separately.

## Separate queue preview

The previously reviewed queue proposal is unchanged. It changes only row 1791's `Status`, `Turns` and `Findings` cells, preserving every unrelated byte, existing note and existing link. Lowercase `unsolved` and `5/5` follow repository conventions. Its finding correctly describes the accepted partial progress and the unresolved benchmark and broader-source scope.

- Reviewed base Git blob SHA-1: `3bad7c6098ceed14505338d8f5ceba882eeaa1d8`
- Base SHA-256: `06c381c98bdd85b3187b4e16b5eeac8c6e3ba2918042259712c57f666305c321`
- Proposed SHA-256: `d643cb95664ce90a75049e5a50063e0d934ce30d7d5e420b600033c12b50cfc9`

This accepts the reviewed queue edit's scope and wording, not a blind overwrite of a later repository version. The current destination must still be checked before applying the three-cell change.

## Final determination

**Revision 2 accepted at manifest SHA-256 `104655a3116633b2e46c2b49252bfb896bed6b8576ffcce0051363e51ce91ac3`. E-6322 remains UNSOLVED 5/5.**

No frozen payload was modified by the reviewer. No publication or other external write was performed.
