# Independent scope and regression review of revision 2

Checkpoint: 2026-09-17T15:00:52Z. Completion estimate: 100% of this bounded source/interface/documentation review. Clean compilation and independent reviews of the new moment, residual, and relabeling proofs are separate workstreams.

Reviewed target: `snapshot/lean_formalization` in this review folder. Comparison baseline: Git `9af7dbae1`, plus the actual previously audited extracted package in `lean_independent_review_2026-09-16/package/lean_formalization`. Current HEAD at comparison was `aae0f2fd9a4dda90c265b4258ca09149be350217`. I did not edit the snapshot or run a build. Package self-reports were treated as claims to inspect, not independent evidence.

## Verdict

**No blocker found in the preservation of previously reviewed claims, the expanded completion interfaces, or the revised scope documentation.** The changes are additive mathematical coverage. They do not weaken existing model definitions or principal conclusions. Subject to successful independent compilation and the separate new-proof reviews, this is honestly describable as a ready-to-share **principal-results Lean companion with explicit coverage boundaries**.

It should not be described as an exhaustive formalization of every derivation or as external human peer review. The remaining supplied-polar-factor boundary is real, clearly disclosed, and does not make the principal value theorems conditional on arbitrary polar-decomposition existence.

## Independently checked source preservation

I compared file bytes directly rather than trusting `verification/source_preservation.json`.

| Check | Result |
| --- | --- |
| Existing `CyclicBell/*.lean` files in the previously audited extracted package | 105 |
| Existing files byte-identical in revision 2 | 104 |
| Existing files changed | Only `CyclicBell/AxiomAudit.lean` |
| Existing files deleted | None |
| New files | `GeneralSecondMoments.lean`, `GeneralSecondResiduals.lean`, `GeneralOutcomeRelabeling.lean`, `GeneralSecondCompletionStatements.lean` |
| Same comparison against Git `9af7dbae1` | Again, only the existing `AxiomAudit.lean` differs |
| Bundled manuscript source | Byte-identical |
| Lean toolchain and dependency manifest | Byte-identical |
| Current snapshot versus live package | 155 inspected source, interface, script, reference, configuration, and main-documentation files compared; no mismatches |

In particular, the actual physical models and the scalar, first/second upper-bound, source polar, three-model value, and rigidity modules reviewed previously have not changed. Their import source files are also among the preserved modules. The modified axiom file only adds imports and reports for the additions; it does not change an old theorem statement or proof.

The library root imports the new statement module at `CyclicBell.lean:1`. `CyclicBell/AxiomAudit.lean:68,83–85` imports the new modules and adds their dependency queries. `scripts/static_audit.py:13–14` now requires all four new modules. `validation/AcceptGeneral.lean:1` imports the expanded interfaces and adds the d=2 extra-Bob correlator example at lines 20–23. Thus the new statements are connected to the advertised build/check path rather than merely stored as unbuilt files. The old compiler/checking runner is unchanged; the package version changes from 0.1.0 to 0.1.1, and packaging updates its expected named-declaration count and output filename.

This byte-preservation evidence supports carrying forward the earlier semantic reviews. It is not a substitute for the coordinator's fresh build and dependency validation.

## Expanded completion interfaces

The following line references are to `snapshot/lean_formalization/CyclicBell/GeneralSecondCompletionStatements.lean`.

| Interface | What is actually required by its type | Result |
| --- | --- | --- |
| Lines 13–17 | The literal Born sum `Σ_ab χ(a+b)p(a,b|l,y)` for every `l,y : Ix d`, every permutation, and every d≥2 equals `λ_l χ(−ly)` | Covers all d Alice inputs, not just the old generic two-input construction. The sign and complex coefficient are visible. |
| Lines 19–23 | The same actual Born sum for Bob's added input equals `if l=0 then 1 else 0` for every l | Includes every entry of the added column. |
| Lines 25–30 | Equality of the entire two-index Born-correlator functions between arbitrary permutations | Checks the complete first-harmonic array, not merely equality of Bell scores. |
| Lines 32–37 | Both families of complex local traces using the strategy's actual density and encoded effects vanish | All Alice inputs and all Bob inputs, including the added one, are quantified. This is a complex moment assertion, not only a real-part assertion. |
| Lines 39–44 | The literal `d λ_l I − A_l ⊗ Bhat_l` matrix applied to the actual maximally entangled vector is zero | Checks residual annihilation as a vector; no scalar attainment or maximality premise is present. |
| Lines 46–51 | The literal `I − A_0 ⊗ B_none` matrix kills that same vector | Covers the additional aligned residual independently of a scalar Bell value. |
| Lines 53–55 | The sum of `χ(b)M_(−b)` equals the adjoint of the original encoded observable for arbitrary finite-dimensional measurements | Makes the relabeling/adjoint correspondence visible. |
| Lines 57–65 | The expanded transported functional on the relabeled strategy equals the original `secondValue` | Both Fourier and added Bob observables are explicitly adjointed; the original functional is not falsely held fixed. Local dimensions are unrestricted finite coordinate types. |
| Lines 67–71 | Every actual probability of the relabeled permutation strategy equals the original probability at Bob outcome −b | Checks the full behavior convention, not just a designated target table. |

These examples apply named proof results, but their expected types expose the relevant sums, traces, operators, and quantifiers rather than merely restating a theorem name with an unspecified type. The remaining shared definitions—`behavior`, `encoded`, `secondPermutationStrategy`, `generalLambda`, and the entangled vector—were checked in the earlier review and are byte-identical here. This is useful interface regression coverage; it is not an independent second proof or a guarantee that arbitrary future coordinated changes to every shared definition would be detected.

The anonymous examples do not individually appear in the named axiom-query inventory. They are compiled through the library import and are straightforward applications of the named new declarations, whose transitive dependencies are queried. I found no trust-boundary problem in that arrangement. The revision adds one concrete acceptance example but does not claim a new exhaustive negative-control suite for each completion clause.

## Documentation accuracy

The revised documentation addresses the previous scope ambiguity directly:

- `COVERAGE.md:37–38` and `REVIEWER_GUIDE.md:39` label the old generic permutation package as a **two-Alice-input, first-harmonic** result. They explicitly explain that “all harmonics” in some retained theorem names means all first-harmonic entries, not every Fourier order.
- `COVERAGE.md:45–50` separately maps the actual d-by-(d+1) second-family matrix, local first moments, and residuals to the new files. Its formulas and input domains match the expanded interfaces.
- `COVERAGE.md:51` explicitly transports the Bell functional as well as Bob's measurements. The corresponding expanded interface at lines 57–65 supports that statement.
- `COVERAGE.md:52` distinguishes the observed maximum entry and explicit fixed-guess transport from an exact worst-case Eve optimum. The new interfaces do not claim an optimum they have not proved.
- `reference/paper_claim_ledger.json` corrects the source polar wording from “Bob matrix is the polar factor” to “Bob matrix is the entrywise conjugate of the polar factor.” This agrees with the unchanged actual theorem and the manuscript convention. It also corrects stale entries about the already-existing closure inclusion and source canonical-polar identification.
- `README.md` describes added correlator, convention-transport, and residual statements against the same pinned manuscript; that description matches the actual diff.
- `verification/STATEMENT_REVIEW.md` explicitly says the assessment was AI-assisted and not external human peer review. It describes the prior issues as statement omissions rather than a failed principal endpoint; the preserved-source comparison supports that distinction.

The retained verification receipt and its reported 1,894 named declarations remain execution claims for the independent build reviewer to check. The changes from 1,852 to 1,894 match the 42 added named declarations/queries shown in the diff, but agreement of counts alone is not kernel evidence. Documentation correctly says so.

One **nonblocking navigation nit**, flagged by the coordinator and independently confirmed here: `COVERAGE.md:88` lists `standard_behavior_formula` in a row linked only to `GeneralPhaseTables.lean`, but its declaration is actually at `CyclicBell/GeneralPhaseBounds.lean:168`. The row could link that name to its actual file. The theorem exists; this is not a missing proof, a new regression, or a reopened principal-coverage issue. The snapshot was left unchanged.

## Remaining polar boundary and honest release description

`COVERAGE.md:100` still discloses that the general polar identity assumes factorization and initial-isometry properties, and does not separately construct arbitrary canonical polar decompositions, prove uniqueness, or derive their strong-limit representations. The mathematical source is unchanged:

- `GeneralCoveragePolarCanonical.lean:77–83` takes only supplied-factor properties, unitarity of Bob's operator, and commutation; it proves the literal positive-square-root residual identity.
- `GeneralCommuting.lean:46–78,96–125,160–174` constructs continuous half-polar factors and the global gap independently. Its actual arbitrary-Hilbert upper bound has no canonical-polar existence premise.
- `GeneralCoverageSourceCanonical.lean:57–105,121–145` constructs and identifies the source factor and its actual positive modulus, including a two-sided inverse for these nonsingular explicit pencils.

Consequently, the omitted general polar existence/strong-limit derivation does not undermine the companion's principal value claims. The manuscript's arbitrary-shift cosecant-square intermediate identity and external cited results also remain outside a line-by-line translation; the relevant coefficient normalization and endpoints are proved by alternative routes. Revision 2's documentation does not claim to eliminate those boundaries.

Recommended description: **“A Lean companion covering the paper's principal mathematical results and the explicit second-family first-harmonic, residual, and convention-transport clauses, with a pinned manuscript, reproducible checks, and documented exclusions.”** Avoid “every statement and proof step in the paper is formalized” or “independently human-peer-reviewed.”

No mandatory correction identified within this workstream. Final readiness should incorporate the coordinator's clean execution result and the separate independent checks of the newly added mathematical proofs. No external communication occurred, and no snapshot/package source was changed.
