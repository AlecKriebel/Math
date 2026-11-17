# No single polynomial inequality defines a real binary Gram locus

Alec Kriebel, independent researcher. ORCID 0009-0001-9320-500X.
Version 1.0.0, 12 October 2026. CC BY 4.0.

The manuscript proves that for every n>=3 the determinant Gram locus of real binary tensors in the closed Frobenius unit ball cannot be defined by one polynomial inequality inside its cube or its known convex hull. For higher factors the proof uses exact zero-determinant faces. It does not claim the stronger positive-domain theorem in Ferudun's October2 preprint. A strictly positive rational four-factor counterexample also refutes Seigal's specific proposed polynomial.

The proof credits the established marginal polygon criterion and real constructions. The single-polynomial theorem was present in the original September30 GitHub PR170, before the overlapping October2 Zenodo record. This formal preprint is not backdated. "Contemporaneous separate disclosures" describes the documented chronology, without certifying mutual independence, literal simultaneity, exclusive firstness or a complete historical absence of earlier work. Current public visibility is not an independent archive of historical visibility. The timeline receipt and priority reports record evidentiary limits.

## Reproduction

Python 3.11 or later, standard library only, is sufficient:

    python3 -E -S -B -P verify_exact.py
    python3 -E -S -B -P -O verify_exact.py
    python3 -E -S -B -P verify_controls.py

The driver writes verification.normal.json, verification.optimized.json and negative_controls.json. Run it in a copy to preserve deposited files. It requires byte-identical baseline outputs and rejects deliberately broken parity weights, reflection, normalization and full-sign Q2 variants in both modes. All checks raise explicit exceptions; they do not depend on Python assert statements.

The 46,274 finite checks include exact real parity marginals, boundary and reflected-plane identities, integer-tensor determinant bounds, and the rational four-factor counterexample. They do not prove the all-polynomial theorem: its universal justification is the written multiplicity and exact-slice proof. Hashing the manuscript beside the runs identifies the version; it does not formally verify prose.

Files: gram_locus_note.tex (standalone source); verify_exact.py (exact finite controls); verify_controls.py (baseline and negative driver); the three diagnostic outputs; metadata.json (intended deposit metadata); TIMELINE_RECEIPT.json; SOURCE_LOCATORS.json; priority_reviews/ (namespaced exact allowlisted own audit outputs); SUPPORT_INDEX.json (included, excluded and unverified reference mapping); MANIFEST.json (archive member sizes and SHA256, excluding itself). The PDF is deposited separately.

Original weak assert-based controls are preserved in the repository's historical audit, with their optimization defect documented; the published controls use explicit exceptions. Third-party source bodies, HTTP headers, server cookies and private retrieval material are excluded.

AI tools were used extensively in solving, drafting, source comparison, reproduction and adversarial verification. This work is unrefereed and has not undergone conventional human peer review. The author is responsible for the contents. No outside individual was contacted on behalf of the project.

The support index resolves references in the historical audit reports. Original report and first-seal bytes are unchanged; excluded private inventories, source bodies and review-only stronger hypotheses are explicitly identified. The R1 first assessment had accidental prior-summary exposure and is qualified; it is not presented as a clean independent first-seal review. Its two presentation/evidence issues are addressed in this internally revised V2 package, while the paper remains the same formal version1.0.0. Historical pending-status statements are dated snapshots, not assertions about a later deposit. A fresh review is required before publication.
