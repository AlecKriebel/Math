# Acceptance report: reduced complex smoothness component

Problem: 2100502 / AMR-020-0502. Date: 2026-10-11.

Decision: ACCEPT_REDUCED_COMPLEX_SMOOTHNESS_COMPONENT.

This AI-assisted, unrefereed prose edition presents one internal AI mathematical reconstruction of a prior candidate. It is not human peer review or formal proof-assistant certification, and is not a computational reproduction package. AUDIT.md records editorial checks of that same reconstruction; it is not a second independent mathematical audit. The prior candidate receives explicit credit; no novelty or priority is claimed.

The accepted statement is: for a general finite-dimensional complex alternating pencil, the reduced bi-Lagrangian variety is smooth if and only if every Jordan pencil block has dimension 2; Kronecker blocks are unrestricted. In the smooth case it is the product of LG(m_lambda,2m_lambda), with dimension sum m_lambda(m_lambda+1)/2. The zero regular part gives a point.

This accepts a prior candidate, not our novelty: Anonymous, *A sharp smoothness criterion for bi-Lagrangian Grassmannians*, 0.2.0-candidate, 12 September 2026, at ipitchford/sharp-bilagrangian-smoothness commit 855d8cc512b7cd51af437b6e033ec0e0ae8b32ed. The criterion was proposed in Kozlov's Problem 14.8 and Remark 14.4. The originating bundled question is Bolsinov-Matveev-Miranda-Tabachnikov, arXiv:1804.03737v2, Problem 5.3, PDF page 25.

PROOF.md retains the complete all-n reconstruction, including the core/eigenvalue reductions as algebraic isomorphisms, the precise reduced hypersurface chart and the completed-local-ring fixed-subscheme argument. AUDIT.md describes editorial logical and scope checks of this same reconstruction.

Required source correction: Kozlov v1 Lemma 3.3(1)'s arbitrary-subspace isotropy/invariance equivalence is false. The explicit line U=C e in the dimension-4 block is simultaneously isotropic but not P-invariant. Its Lagrangian specialization is valid and is the only version used. This baseline error does not invalidate the accepted complex theorem.

The arbitrary-pencil orbit-classification problem remains unresolved by this edition. No acceptance is given to reducedness of the original incidence scheme, a full singular-locus classification, an ambient mixed-block normal form or every statement of any cited paper. Real arguments in Section 9 retain their separately bounded review; a full real-form canonical-decomposition audit is not claimed.

The original finite symbolic tests and actual normal/-O/-OO controls are supplementary evidence, with bounded coverage explicitly recorded in VERIFICATION.json. They are not a formal all-n proof. The external source inventory and the present eight-file manifest authenticate bytes and do not establish mathematical correctness. No source-author executable was run, and this edition distributes no scripts, raw outputs, copied third-party text/PDFs/images, dataset contents or private coordination. No new source inspection or proof search was undertaken for this editorial edition. No priority or current-openness determination is made.
