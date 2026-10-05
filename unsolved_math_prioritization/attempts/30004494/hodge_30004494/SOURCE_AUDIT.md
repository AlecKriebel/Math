# Source and hypothesis audit

Checked 2026-10-05. Mathematical statements are paraphrased and independently analyzed; no full source text is included. A repository/dataset status is evidence of earlier triage, not proof of an open-problem classification.

## 1. Primary target

The requested unsolvedmath URL was attempted first. Web retrieval was unavailable and a direct public request returned HTTP 403; no denied route was bypassed. The full selected record was instead inspected in a locally available byte-verified public dataset snapshot, and then checked against the official OWR PDF. The snapshot's report collection contains no matching report key or ID. The selected record asks for fixed nonnegative integer coefficients under logarithmic injectivity; its older status assessment lists the surface and irreducible-boundary cases.

The official [OWR24/2020](https://publications.mfo.de/bitstream/handle/mfo/3797/OWR_2020_24.pdf), Robles contribution, printed pp.1306-1308, is authoritative for the target. It describes the period map on the open base, the compactification, boundary, extended Hodge line and logarithmic Torelli condition. Printed p.1308 was visually checked against the extracted formula. The report is dated 2020 and was published July 2, 2021; neither date should be confused with the dataset's creation date.

## 2. Precise 2021 formulation and known restrictions

[GGR, *Natural line bundles on completions of period mappings*, arXiv:2102.06310v1](https://arxiv.org/abs/2102.06310v1) specifies the upper-half determinant product in (1.2). Conjecture 1.10(a), with generic immersion and nonnegative rational corrections, is a **semiampleness** question. Part (b) is the fixed-integral **ampleness** question. Proposition 1.11 requires one boundary component, injectivity of dPhi^1 on Phi^0-fibres, and finite generation of the effective curve cone. Theorem 1.12 is the surface result under everywhere ordinary immersion on U. Those are not identical hypotheses. Theorem 3.1 concerning K_X+Z is a different line-bundle question.

Its Lemma 2.3's assertion of a positive eigenvector for every negative-definite matrix with nonnegative off-diagonal entries needs a connectedness qualification: diag(-1,-2) disproves it literally. PROOFS.md uses the valid rational vector -A^(-1)1 instead, and explicitly supplies the global-threshold step. This is an elementary repair of a proof mechanism, not a new surface ampleness theorem.

## 3. Historical completion status

The [2021 progress report, arXiv:2106.04691](https://arxiv.org/abs/2106.04691), was withdrawn; the current arXiv notice identifies an incomplete proof of Theorem 1.7. Historical claims from its original PDF are not used as established results here.

The [GGLR arXiv:1708.09523v4](https://arxiv.org/abs/1708.09523v4) landing page describes a conditional general ampleness statement, with low-dimensional results. Only its landing-page status was inspected in this investigation; no current-v4 full-PDF audit is claimed. The 2021 precise source and the later corrected paper provide the detailed comparisons used here.

[GGR, *Analog of Satake-Baily-Borel for period maps*, arXiv:2010.06720v6](https://arxiv.org/abs/2010.06720v6), submitted April 6, 2025, corrects the earlier claim that individual det(F^p) descend. Appendix A gives a weight-five example where no positive power of the upper-half product descends to the specified completion, while a differently weighted product does. This is not automatically non-semiampleness on X, nor a counterexample to boundary-corrected ampleness. The inspected PDF is internally dated April 8, 2025; the generated HTML displayed a different date. The versioned arXiv record and hashed PDF are used for reproducibility.

## 4. Modern semiampleness theorem and exact bundle comparison

[BFMT, *Baily-Borel compactifications of period images and the b-semiampleness conjecture*, arXiv:2508.19215v2](https://arxiv.org/abs/2508.19215v2), December 18, 2025, proves Corollary 1.3 for the full Griffiths bundle of an integral polarizable pure VHS with unipotent local monodromy. Theorems 1.1-1.2 / 5.2 construct the projective period-image completion with an ample line bundle whose pullback is a sufficiently divisible power. Section 2.4 fixes the bundle; the CY-Hodge theorem has additional hypotheses and cannot be freely substituted. The authors' page lists this work as submitted. Its proof is cited as a primary preprint result; this packet has not independently reproved the 61-page theorem.

Here is the elementary comparison, in the unipotent canonical-extension convention. Let d_p=det(F_e^p), and T=det(V_e). The polarization gives an exact sequence

0 -> F_e^(n+1-p) -> V_e -> (F_e^p)^* -> 0.

Consequently d_p=d_(n+1-p) tensor T^(-1). The integral Q-preserving monodromy has determinant in {+1,-1}, so T is torsion; unipotent local monodromy makes its extension a flat torsion line bundle on X. Ignoring a torsion factor, which does not affect numerical ampleness, define G=product of d_p for p=1,...,n and L=product of d_p for p=ceil((n+1)/2),...,n. Pairing p with n+1-p gives:

- n=2r: G=L^2, up to torsion
- n=2r-1: G=(product for p=r+1,...,2r-1 of d_p)^2 tensor d_r = L^2 tensor d_r^(-1), up to torsion
- n=1: G=L

In even weight, BFMT thus also gives semiampleness of L: a positive power of a torsion twist of L^2 is globally generated, and a further power kills the torsion. In odd weight >=3 this formal inference is unavailable. Regardless of parity, semiampleness and an ample descent do not imply ampleness of the pullback on positive-dimensional fibres. Proposition 4.1 in PROOFS.md states exactly what additional boundary-relative-ampleness input would suffice.

## 5. Recent boundary geometry and its limits

[GGR, *Period maps at infinity*, arXiv:2509.08508v1](https://arxiv.org/abs/2509.08508v1), especially Theorem 5.1 and Corollary 5.4, relates theta bundles pulled back along the level-one extension map to integer linear combinations of boundary normal bundles on a compact graded-period fibre. This is a fibrewise relation, not a globally chosen effective correction on X. Its pairing Q-script is the bilinear form on the relevant Lie algebra; it should not be confused with simply reusing the original polarization Q on V.

A sign control matters: (5.2) prints a positive sum of Q-script(M,N_j)[Z_j]; Corollary 5.4 prints a negative sum of Q-script(M,N_j) times the **conormal** bundle. These are consistent because a conormal is the negative of a normal in additive notation. They do not authorize replacing the displayed right side by a negative sum of [Z_j] without a separate coefficient-sign argument. Definition 5.3 and the last sentence of section 5.3 warrant care about signs and normalization. The PDF page 29 and HTML were both inspected; no global sign conclusion is extracted here.

[Deng-Tsimerman, *On the generalized toroidal completion of period mappings*, arXiv:2506.10109v4](https://arxiv.org/abs/2506.10109v4), Theorem 2.8, constructs a completion after a modification of the base; Conjecture 2.12 asks for projectivity of the completed target in general. An analytic completion on a modified base is not the fixed-boundary ampleness asserted here.

## 6. Prior-attempt checks

Read-only GitHub checks found the selected queue row still queued, 0/5, and no directory at attempts/30004494 on the default branch. Exact-ID code/PR searches returned no prior matching attempt; broader Hodge PR results were unrelated. The repository root and queue-specific instructions, README, queue row and related-target groups were inspected. The related-target groups did not contain this exact ID. A targeted prior-conversation retrieval found no verified earlier attempt on this problem. These are bounded negative search results, not a claim to have exhaustively audited every historical branch.

## 7. Source-independent retained work

The general closed-null-face criterion, rationalization, surface matrix construction with uniform threshold, pullback controls, and finite linear alternative are proved in PROOFS.md. They depend on the explicitly named classical positivity theorems, not on the withdrawn completion claim or an inferred identity between different Hodge bundles. Abstract cone/matrix failures are labeled as proof-strategy controls; they are not promoted to examples of genuine variations of Hodge structure satisfying logarithmic Torelli.
