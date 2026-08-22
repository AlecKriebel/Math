# Claim-to-code inspection map

This is a navigation index for a referee.  It states intended roles only; it
does not certify that a program is correct, independent, or sufficient.  All
source paths below are relative to
`source_and_certificates/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/`.

| Mathematical component | Manuscript location | Programs to inspect | Boundary |
|---|---|---|---|
| Model, baselines, graph construction, and theorem quantifiers | Sections 2--3 | `verify_paper_claims.py` | The program checks selected text markers only; review the definitions and quantifiers analytically. |
| Finite labelled transition aggregation and orbit fibres | Section 4 | `certificates/verify_hybrid_lumping.py` | Exact audit for one nine-vertex rational instance: 512 configurations and 108 fibres under both rules.  It is not the general strong-lumping proof. |
| Pair and pendant leading response coefficients | Sections 6--7 | `certificates/verify_hybrid_coefficients.py`; `verify_paper_claims.py` | Exact symbolic and rational identities; population-error estimates remain analytic. |
| Sextic root, feasibility gap, tangency, and fixed-parameter optimum | Sections 3 and 7 | `certificates/verify_leading_algebra.py`; `certificates/verify_hybrid_coefficients.py`; `verify_paper_claims.py` | Exact algebra and Sturm checks; the referee should independently derive the encoded expressions. |
| Rational-edge specialization | Section 7 | `certificates/verify_hybrid_coefficients.py`; `verify_paper_claims.py` | Exact endpoint margins and algebraic threshold. |
| Effective dyadic diagonal | Section 4 | `verify_paper_claims.py` | Only marker-level integration checking is automated; nonsingular-M-matrix and real-algebraic arguments require proof review. |
| Weak-cut trace and compact-uniform limit | Section 4 | none | Entirely analytic finite-state perturbation proof. |
| Establishment, confinement, cleanup, and pendant initialization | Section 5 | `verify_paper_claims.py` | Only regression markers are automated; all stopped-process and coupling estimates require line-by-line review. |
| Reciprocal killed-Green and hub-renewal bounds | Section 5 | `verify_paper_claims.py` | Only regression markers are automated; the two-stage limit is analytic. |
| Gate rates, adverse reversals, and complete satellite sweep | Section 6 | `certificates/verify_hybrid_coefficients.py`; `verify_paper_claims.py` | Gate algebra is audited; stochastic sweep errors and quantifier transfer are analytic. |

The executable replay entry point is `replay.sh`.  It runs, in order,
`verify_leading_algebra.py`, `verify_hybrid_lumping.py`,
`verify_hybrid_coefficients.py`, and `verify_paper_claims.py`.  There are no
other imported project modules in this four-program replay, but the referee
should verify that fact rather than assume it from this index.
