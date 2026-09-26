# Review findings and resolutions

Submission revision: 25 September 2026. This ledger records task-specific AI adversarial reviews and exact computations, not human peer review or formal verification. Original archived v1.2.0 was preserved. Final manuscript source SHA-256: `ff1f4c7e3a696a2f0c899db6827625f81d386601f22dbd9e065a2de2a5846e05`.

## Material correction

**A1: the older GHR generalized-matrix comparison silently used a different prefactor from the accessible primary preprint. Closed.** Independent visual transcription and exact calculation found literal-source residual norms squared `(30,60)` and Hecke residual squared `18`, whereas the common-prefactor matrix encoded by the old verifier has `(0,48)` and zero Hecke residual. The old package's successful tests could not establish its asserted literal source fidelity.

The submission manuscript removes that unnecessary residual/same-spectrum comparison. Its own active operator still has intrinsic residual norms `(24,0)`, independently checked. The new supplement explicitly defines the auxiliary common-prefactor matrix, separately checks the accessible preprint's literal mixed-prefactor matrix, and claims neither author intent nor an unverified journal typo. The original construction, all-n localization, minimum dimension, and comparison to the newer ordinary Galindo–Rowell operator do not depend on the removed assertion. The algebra reviewer independently approved the repair and challenged both new safeguards with mutations.

## Complete disposition

| Finding or recommendation | Resolution |
|---|---|
| A1: source-to-code mismatch | Corrected as above; independently closed in round 2. |
| L1: Wenzl parameter citation | Added Theorem 3.6(b), p. 379; retained Eq. (3.2) for trace uniqueness. |
| L2: unverified journal/preprint definition and conjecture numbering | Removed the uncertain pinpoint numbers; preserved the attribution and checked source content. GHR convention remark now expressly refers to the checked preprint; fixed-v1 URL supplied. |
| R1: mutation harness could count infrastructure failure as scientific rejection | New harness requires the deliberate mutation's explicit `AssertionError` diagnostic. All 26 retained scientific tests pass. Six original archival/package-metadata tests are not misrepresented as tests of the new supplement; the unchanged original 32-test suite was run separately. |
| R2/N7: shared implementation dependencies and unavailable discovery code | Added explicit shared-arithmetic/import boundaries. Retained admission that numerical search code/seeds are unavailable; no discovery-reproduction, exhaustive-search, or whole-paper formal-verification claim. |
| N1: title and early contribution statement | Title now leads with five-word normal form; Introduction states the distinctive certificate/direct proof/comparison contribution. |
| N2: long chronology footnote | Kept date and release link; moved full identifiers into supplement PROVENANCE.md. Fresh release API, tag, and historical Git PDF checks match the recorded identifiers. No private-priority conclusion. |
| N3: abstract emphasis and classification dependency | Rewritten around normal form, certificate, tower and exact comparison; known dimension-three classification dependency explicitly stated. |
| N4: inherited global consequences | Concurrent and classical attribution retained; no new image group, invariant or topological evaluation advertised. Added a direct proof of the known finite-image fact in the present scalar normalization. |
| N5: older GHR comparison | Closed by A1 repair; no bare-matrix similarity or literal-source claim survives in the paper. |
| N6: circle completeness and five-word support | Explicitly restricted completeness to the chosen circle; no minimum-support or all-solution classification claim. |
| N8: substantial AI use | Retained research/derivation roles and actual historical tools; disclosed Codex revision/reviews; no human-referee or whole-paper formal-proof claim. |
| N9: repetitive related-work discussion | Condensed repetition after moving the contribution statement forward; all substantive limitations retained. |
| FR1 / second-round stale-text finding | Deleted the remaining reference to the removed older-GHR residual table and unused symbol. |
| Second-round abstract ambiguity | Braid relation now explicitly belongs to the associated Hecke operator, not to the reflection (which satisfies a modified cubic identity). |
| Optional empty-link boundary clarification | Added the convention that the links considered are nonempty and oriented. |
| Optional alternative four-strand minimality proof | Deliberately retained as research evidence only. It is not needed to repair the valid proof and would add a new projector-certificate obligation. No manuscript claim relies on it. |
| Direct finite-image proof | Added finite Pauli-automorphism action plus explicit finite scalar-kernel bound, lambda^(3·4^n)=1. Independently checked in round 2, including n=2. |
| Submission formatting | Confirmed author location/email; six keywords; numbered, captioned tables; Statements and Declarations; numbered references with DOI URLs; source archive and numbered Online Resource. |

## Validation scope

The original package passed five exact routes, 32 negative tests, 43 internal checksums, and byte-identical repackaging. The revised scientific supplement passed five routes, 26 stronger negative tests, and its 14-entry hash manifest. Independent new evidence includes a complete polynomial cubic residual and converse, dense local/quaternionic checks, 511 trace-versus-finite-field link checks, and finite tests of Garside conjugacy and Pauli-label independence. Finite samples support, but do not replace, the printed universal arguments.

The proof continues to use accurately identified external theorems: Wenzl's trace/quotient theory, GHR's category identification and two-dimensional exclusion, Lechner's character/classification input for dimension three, and the stated classical link evaluation and exact-evaluation algorithm. These full external theories were not re-proved. Remaining dimensions 6,10,14,..., uniqueness, minimum support, a direct local equivalence without opposite, and all-n image-group isomorphism types remain outside the result.

All substantive findings raised during the completed reviews have a documented repair or justified scope disposition. That statement records the review outcome, not a guarantee that no future referee can find another issue.
