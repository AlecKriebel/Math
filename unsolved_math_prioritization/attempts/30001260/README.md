# S5 rank-one isotropy: accepted partial results

Problem **30001260 / OWR-3477-004**, rank **970**. Disposition: **unsolved, 5/5 substantive author approaches**.

The [full independent audit](audit/AUDIT_REPORT.md) accepts all five approaches within their stated scope, with no mathematical correction. No smooth action and no nonexistence theorem is proved. This is AI-assisted mathematical work and an independent AI audit, not journal peer review or a novelty claim.

## Accepted results

1. [Linear obstruction](author/TURN_1_LINEAR_OBSTRUCTION.md): every nonzero real S5 representation has fixed vectors for a Klein four subgroup. This reproduces the known obstruction, credited to Hambleton–Pamuk–Yalçın.
2. [Necessary fixed-set geometry](author/TURN_2_FIXED_SET_CONSTRAINTS.md): a hypothetical smooth action has n = 3r + 2, r >= 0; all involution fixed sets have dimension r; the fixed sets of each four-cycle and its square coincide. Orientation and complex normal-bundle constraints follow.
3. [Compatible Sylow data](author/TURN_3_LOCAL_CHARACTERS.md): explicit fusion-stable complex representations of common dimension 12. These are local models, not a global smooth action.
4. [Induction and joins](author/TURN_4_INDUCTION_AND_JOINS.md): the specific induction from the S4 rotation model has forbidden fixed sets; joins cannot erase them.
5. [Conditional thickening](author/TURN_5_THICKENING_AND_SURGERY.md): even granting a suitable equivariant thickening, its raw boundary has extra intermediate homology. Further equivariant surgery and smooth-structure work remain unproved.

The existing finite S5-CW complex homotopy equivalent to a sphere is credited to Hambleton, Pamuk and Yalçın, [Theorem A](https://doi.org/10.4171/CMH/289). Its category is different from a smooth standard sphere. The May 2026 Hambleton–Yalçın [survey, Remark 8.2](https://arxiv.org/html/2605.02760v1#S8), retains the smooth question. This is dated literature evidence, not an exhaustive present-day status certificate.

## Preservation and scope

All 14 author files, all 11 audit files, and both original ZIPs are byte-for-byte preserved. The audit also retains its embedded original author ZIP. Historical pre-audit and no-publication statements in these immutable originals retain their original meaning; [publication status](PUBLICATION_STATUS.json) records the later disposition. The entire audit is included, not only its acceptance summary.

This portable packet contains authored mathematics, programs and reports plus public verification/citation metadata. It contains no copied scholarly source document, source extraction, dataset contents, or private coordination material. The publication check replays frozen evidence and does not claim a new source retrieval or literature audit.

## Source-free verification

Python 3.10 or later; standard library only. Obtain PUBLIC_MANIFEST.json's SHA-256 from the separate PR description or trusted publication receipt. From any working directory run:

    python -I /path/to/packet/verify_publication.py EXTERNAL_MANIFEST_SHA256
    python -I -O /path/to/packet/verify_publication.py EXTERNAL_MANIFEST_SHA256
    python -I /path/to/packet/mutation_tests.py EXTERNAL_MANIFEST_SHA256

The verifier checks exact recursive inventory, safe regular files, sizes and hashes, externally pinned immutable archive/manifests, exact ZIP/expanded equivalence, and isolated normal/optimized mathematical replay. Mutation tests challenge both Python modes and restore nothing in the frozen packet because they work in temporary copies.

Hashes are integrity checks, not signatures. The finite programs do not prove Smith theory, Borel's formula, manifold duality or smooth realizability, and do not reauthenticate omitted scholarly sources. Passing these checks is not a solution or a CI pass. A missing CI run must be reported as unverified, not successful.
