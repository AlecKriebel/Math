# 6700077: volumic scalar-curvature closure

**Outcome: unresolved here after five substantive approaches (5/5).** This is an authored research record, not a proof of the general conjecture and not a claim of historical novelty. Independent mathematical review is pending. Nothing has been published remotely by this investigation.

The target is AMR-066-0077, Gromov's closure question in Section 26, printed p.81 of the 2017 *101 Questions*. The similarly numbered question on printed p.78, the smoothing question on p.81, and the density question on p.83 are different problems.

Retained results:

1. A complete elementary fixed-witness-radius closure theorem for continuous metrics.
2. An explicit smooth radial, uniformly convergent sequence whose small-ball comparisons succeed at one center but fail elsewhere; this refutes a proof shortcut, not the conjecture.
3. A second-order-contact transfer lemma, with an exact sharpness example.
4. A complete closure theorem for two-dimensional warped metrics whose approximants have locally finitely many smooth pieces, including corners.
5. A closed-hull/regularization reduction with both missing implications stated separately.

The decisive unresolved issue is control of small-ball volume inequalities when their witnessing radii collapse with the approximant. C0 convergence controls each fixed-radius comparison but supplies neither the required common radii nor the missing equivalence with Ricci-flow scalar curvature.

Read SOURCE_SCOPE.md before the proofs: the original definition contains visible inconsistent signs/normalization, and zero-endpoint formulations must not be interchanged silently. The general problem remains unresolved even under the usual positive-threshold interpretation.

Run `python3 -B verify_controls.py` for exact auxiliary identities and negative controls. They supplement the written proofs and do not certify the conjecture. Run `python3 -B verify_packet.py --self-test` for exact file-set and hash verification.

This packet contains authored analysis, code and public-source verification metadata only. No source PDFs, full extracts, screenshots, raw dataset records or private correspondence are included. AI tools were used extensively. The work is unrefereed and has not undergone human peer review.
