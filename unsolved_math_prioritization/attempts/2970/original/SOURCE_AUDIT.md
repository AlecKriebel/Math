# Primary-source and scope audit

Checked 2026-10-08. This is a bounded literature inspection, not a guarantee that every later or unindexed work was found. Sources and tests count zero toward the five mathematical approaches.

## Problem recovery

The actual K3 book manuscript has 436 PDF pages. Problem 4.94 and its family descriptions were read in text and visually on pages 267–268. The AIM address ending `kirbylistrep.pdf` is a four-page workshop summary and does not itself contain this problem. The manuscript is an author's preliminary version; its public distribution restriction was respected by including only a citation and verification metadata here.

Normalize its notation to X_r=H(r), Y_r=H′(r), odd r≥3. The smooth orientation is forced by nonzero signature. The intended symplectic comparison is the canonical symplectic structure in the canonical class. It is not a statement about every possible symplectic form.

## Inspected primary material

1. Auroux, arXiv:math/0605692v2. The arXiv landing page identifies this as the published Geometry & Topology version. Inspected the introduction, Corollary 2.5, Section 2.3 (including Proposition 2.11), Section 2.4, Theorem 4.3, and the degree-doubling/Lagrangian discussion. Its explicit canonical-pencil and Luttinger-surgery comparisons concern the smallest pair r=3. The general-r integral computation in this report is proved independently from the same nodal-cover construction; it is not attributed to an explicit all-r theorem in that paper.
2. Catanese, arXiv:math/0608110v2. Inspected Theorems 1.1–1.3 and the canonical-form construction. The normal-singularity and smoothing-component hypotheses cannot be silently dropped when applying its symplectic gluing results.
3. Monreal–Negrete–Urzúa, arXiv:2410.02943v3. The landing page reports the latest revision as 7 July 2025; the PDF is internally dated 9 July. Inspected classification/smoothing statements, Theorem 5.8 with its component conclusion, and Theorem 5.12 with its proof. Apply the p_g≥10 and T-singularity restrictions. Theorem 5.8 describes the F_0 component precisely; merely repeating “nonspin component” is insufficient in the odd-r regime where both smooth components are non-spin. This remains a preprint on the inspected landing page.
4. Rana–Rollenske, published Algebraic Geometry PDF. Inspected Theorem A, Theorem 3.4 and its setup, Proposition 3.6, and Corollary 5.12. The abstract states ℓ>2; Theorem A states ℓ>1; Theorem 3.4 has K²=4n divisible by 8 and n≥3; Corollary 5.12's stronger local-moduli assertion uses ℓ>2. The counterexample in this report uses ℓ=3 and lies safely in all these ranges. The old arXiv copy was also inspected, but the published PDF controls these citations. No claim about normal-crossing structure at ℓ=2 is needed.
5. Akaike–Enokizono–Hattori–Koto, arXiv:2507.17633v1. This 218-page preprint is later than the MNU revision and materially updates the degeneration discussion. Inspected the definition of the normal smoothable moduli space, Theorem 1.17, Example 1.23's two smoothings, Section 1.5 on the Horikawa problem, and the cited proof endpoint. It supplies the exceptional normal log-canonical bridge at p_g=10, not a diffeomorphism. It must not be collapsed into the earlier T-singularity obstruction.

## Retrieval and status limits

The Harvard author PDF for Auroux was text-readable through the web tool but a direct byte retrieval returned HTTP 403. The verified arXiv published-version copy supplied the bytes instead. The RR publisher PDF initially timed out in the web tool; direct retrieval succeeded and was text-inspected. The AEHK HTML was too large for the web tool; its PDF was retrieved and the relevant portions inspected. These source-access fallbacks introduced no repository mutation or public source copies.

Targeted current searches included the Horikawa problem, diffeomorphism/symplectomorphism, Lagrangian spheres, and normal stable degenerations. The later AEHK paper was found and incorporated before freezing this candidate. None of the inspected sources verifies a positive or negative answer for an odd-r pair. The report therefore remains partial/unresolved.

## Independent checks performed

- Symbolic derivations in the report are separated from finite parameter checks for r=2 through 31.
- The exact finite-group script generates all 24 matrices in the relevant group, all 12 quotient classes, and the complete Hurwitz-plus-global-conjugation orbit of each of the two displayed tuples. The orbits have sizes 216 and 144 and are disjoint; all orbit entries retain their respective central lift product.
- Pencil arithmetic is checked at k=1,2,4,8 for each tested r; r=3,k=1 recovers 17,16,196.
- Normal, `-O`, and `-OO` executions produce identical outputs; a defective matrix is rejected in all modes; mode-0555 working-directory execution was checked as a non-root user.
- The public manifest contains only authored work and public verification metadata. Scholarly PDF bytes and extracted text are excluded.

These checks do not certify geometric representability, prove a Hurwitz obstruction for the actual canonical pencils, or identify a smooth or symplectic invariant beyond the conditional statements in the report.
