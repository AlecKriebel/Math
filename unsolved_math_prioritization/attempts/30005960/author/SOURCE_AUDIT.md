# Source scope and mathematical audit

## Checked inputs

The short OWR contribution on printed p.1818 was read in the primary report and visually checked. The official MFO PDF and the TIB-hosted PDF have different byte hashes, but their full `pdftotext -layout` outputs match exactly, including the relevant page. Neither PDF nor its extracted text is included in this packet.

For Vilches's arXiv:2508.07019v1, the used statements are Theorem 1.3, Lemma 3.1, Conditions 4.1 and 5.5, the strict-chain part of Section 4, the support-property conclusion of Section 5, and the heart/degree-threshold description in Corollaries 3.9 and 3.12. In particular, the support-property restriction is stronger than merely avoiding integral single-curve charges; the explicit example verifies it for every connected interval.

Chou's source is the revised v2 dated 29 September 2025, not the original v1. The introduction, exact single-ADE hypotheses of Theorems 1.1–1.2, Lemma 3.15 placing O_E(-1)[1] in the fixed heart, and the separation between ordinary and weak stability were inspected. Langer's Theorem 0.2 is contextual and is not used to infer resolution compatibility.

## Dependency boundary

The existence assertion for P(1,3,8)'s resolution is an application of a stated prior theorem. The authored numerical proof verifies its geometric and chamber hypotheses. It does not independently certify every categorical argument in the source, or convert an unrefereed preprint into a refereed publication.

In particular:

- Existence of a nonzero central charge on every nonzero object of the relevant heart uses Vilches's construction, rather than only the finitely many line-bundle tests.
- The Harder–Narasimhan property uses the cited categorical argument.
- The full support property uses the source's global estimates for all semistable objects. The exceptional-factor quadratic inequality here is narrower.
- Convergence in the stability-manifold topology is part of the cited theorem. Convergence of the displayed central charges alone would not suffice.
- Chou's weak endpoint is not silently promoted to a stability condition on the resolution.

## A D4 warning in a part of the source not used here

Vilches's Remark 4.2 on p.13 identifies every positive full-support exceptional cycle of square -2 with the fundamental cycle. This is false for a D4 configuration. The following computation is self-contained.

Label the central -2 curve C0 and the three -2 leaves C1,C2,C3, with C0·Cj=1 and all leaf pairings zero. The intersection matrix is

M_D4 = [[-2,1,1,1], [1,-2,0,0], [1,0,-2,0], [1,0,0,-2]].

Consider

R=C0+C1+C2+C3 and Theta=2C0+C1+C2+C3.

Both have all coefficients positive, and

R^2=-8+6=-2,

Theta^2=-8-6+12=-2.

They are different. Furthermore

(R·C0,R·C1,R·C2,R·C3)=(1,-1,-1,-1),

(Theta·C0,Theta·C1,Theta·C2,Theta·C3)=(-1,0,0,0).

Thus R is not anti-nef, while Theta is. To see that Theta is the fundamental cycle, any positive integral anti-nef cycle must have all leaf coefficients at least one. A central coefficient one would make its central intersection at least -2+3=1, impossible. Hence its central coefficient is at least two, and Theta is componentwise minimal among positive anti-nef cycles.

This also distinguishes the finite hyperplane tests in the printed Condition 4.1. Choose a rational divisor beta with beta·Ci=1/4 for all four curves, which is possible because the intersection matrix is invertible. Every proper connected support is a chain with at most three curves and has fundamental cycle with all coefficients one. Its beta pairing is 1/4, 1/2, or 3/4. The full-support fundamental cycle has beta·Theta=5/4. These are all nonintegral, so the fundamental-cycle tests printed there pass, whereas beta·R=1 is integral. The missing reduced-root hyperplane is real, rather than an equality of notation. The exact checker verifies all eleven connected supports.

This is a counterexample to the root-theoretic remark and a warning against treating its stated tests as all-root avoidance in branching ADE types. It is not, by itself, a counterexample to the existence statement for general beta: a stronger genericity condition excluding every positive-root hyperplane is available as a possible repair, but its entire categorical implementation is not asserted here.

Neither the [-2,-2] nor the [-3,-3] chain in the selected application uses this false branching-root identification. Every selected component satisfies the strict-chain hypotheses, and its six interval tests are explicit. Chou is cited separately for the singular single-ADE example. We make no claim that the warning has been newly discovered historically, or that the full ADE statement has been independently resolved in this packet.

## Reproduction

`check_exact.py` uses only integer and rational arithmetic. It checks the fans, Cartier pullback, polygon, intersection matrices, beta, chamber inequalities, constant-volume identity, ample path samples, exceptional line-bundle charges, point-sheaf charge additivity, and the D4 warning. The general ample-path and integer-degree statements have proofs in the written example; finite samples are supplementary controls.

The program's output includes an explicit scope limit. Independent acceptance should first inspect the source statements and reconstruct the application, then run the controls. No external publication was made in preparing this packet.
