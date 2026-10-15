# Independent review of 30005310: literal threshold-classification counterexample

**Verdict: PASS, for the exact source-literal numerical classification. No mathematical correction is required.** Recommended disposition: claimed_solved, author 1/5, expressly credited as a source correction/classical consequence without a novelty claim. This is an independent adversarial AI review, not human peer review. The parent retains publication authority.

## Frozen version and independence

- Author `PROOF.md`: SHA-256 `69ffeade6c2ee758e3c2869d9c5b7dd607c9a1b6782f7ecebfb81d0812fdb676`
- Author `MANIFEST.json`: SHA-256 `afe2da4b788a54b26c2f0a6c7b0b97562d0fc41431eacbdd4020d5c4be8748cb`
- All ten manifest entries and all three primary PDFs matched their hashes
- All 188 author assertions replayed, with a byte-identical receipt in an isolated copy
- A separately authored exact checker passed 1,808 assertions, including an explicit right inverse for the statistic-map derivative

The reviewer did not contribute to this Gaussian candidate, its witness, or its derivation. The author and reviewer are concurrently assigned unrelated kinetic-proofreading work with separate roles; that does not supply any Gaussian proof ingredient. No author file was changed during this review.

## 1. Source and quantifiers

I read the complete Homs–Kuznetsova contribution, printed pp.3146–3149 of [OWR55/2022](https://ems.press/content/serial-article-files/46992), and visually inspected the exact Proposition 3 and Conjecture 4 pages. The colored-model definition permits arbitrary vertex and edge partitions. It therefore includes singleton colors and the candidate's genuine equality between two concentration diagonals. Neither the displayed definition nor Proposition 3 restricts the graph to a four-cycle.

The report defines the sufficient statistics as color-class sums and the elimination ideal using **all** rank minors of a symmetric matrix. Its two numerical scenarios at the last nonzero elimination ideal prescribe weak threshold n or n+1. The example's weak threshold 2 at n=3 refutes those prescribed values. The supplied cleaned question retains the same numerical conclusions. Its original scraped text contains neighboring example material; the primary-page inspection, rather than that scrape, supplies the relevant proposition.

The surrounding examples do concern four-cycles. The candidate properly disclaims an unstated four-cycle-only interpretation. Equally importantly, the example satisfies the positive-definite-intersection hypothesis of the second case. It refutes that case's threshold conclusion, **not** a repaired assertion asking only for one of two Boolean certificate mechanisms. These limitations are mandatory and already explicit in the frozen proof. No claim about authors' intended unstated restrictions is warranted.

## 2. Colored model and likelihood criterion

In the singleton K4,4 model the 24 statistics are eight diagonals and sixteen cross-block entries. Merging vertices 1 and 2 replaces two individual diagonal statistics by their sum, leaving 23 coordinates. This is the dual sufficient-statistic constraint for K11=K22, not a requirement that the covariance diagonals themselves be equal. The candidate uses the correct distinction. Every edge remains singleton-colored.

The positive-definite completion criterion is also independently consistent with the likelihood optimization, without relying on the disputed Proposition 3. For a matching positive-definite completion M, the trace pairing with every feasible concentration K agrees with that of the sample covariance. The negative log likelihood is therefore tr(MK)-log det K. The positive minimum eigenvalue of M makes its sublevel sets bounded, and approach to a singular boundary sends the objective to infinity. An interior minimizer exists; strict convexity gives uniqueness. Conversely, at any interior optimum the score equations force the inverse concentration to have the specified color-sum statistics. Thus a forbidden positive-definite completion obstructs an MLE.

The source uses the rank-indexed scatter convention, and the cited primary rigidity paper explicitly defines iid sampling from N(0,Sigma). Two observations give XX^T up to a harmless positive scalar. Estimating an unknown mean would change the observation-count indexing; the frozen proof correctly excludes that different convention. Nondegenerate Gaussian models have positive density on all of the two-observation data space, even when the concentration matrix has zeros or color equalities.

## 3. Exact elimination-ideal claims

The cross-block determinant is a genuine nonprincipal 4-by-4 minor of the full symmetric matrix. It is a nonzero polynomial in observed coordinates, and belongs to the rank-three elimination ideal after substitution using the linear statistic equations. It survives the diagonal-color merge unchanged. This establishes I(G,3) nonzero for both models; no rank test based only on principal minors was used.

For rank four, I independently reconstructed the derivative at the author's U=I4, V with consecutive cyclic-pair rows. For an arbitrary output direction, set Dii to half the desired left diagonal derivative, set dV^T=H-DV^T for the desired cross block H, and then choose D12,D23,D34,D41 to achieve the right diagonal derivatives. These choices do not overlap or alter the already fixed diagonal entries. I checked each output basis vector by differentiating the actual Gram-statistic polynomial, rather than merely reproducing the author's pivot columns. The resulting right inverse proves surjectivity. The merged-color map is a surjective linear projection, and its 23 basis directions were separately checked.

The real submersion yields an open subset of the full statistic space in the image of rank-at-most-four Gram matrices. Every member of the exact elimination ideal vanishes there, hence must be the zero polynomial. This suffices for I(G,4)=0, without radical-ideal assumptions, generic-completion/MLT equality, or a claim that every point of a Zariski closure has a real positive-semidefinite preimage. If one extends coefficients to C, the same real-open vanishing argument applies to real and imaginary parts and again forces zero. The argument is not confused by the symmetry of the full matrix or by V itself being singular: U=I4 guarantees Gram rank four.

## 4. Weak threshold and positive probability

The rank-two Gram matrix diag(J4,J4) and I8 have identical singleton statistics and therefore identical merged-color statistics. More importantly, the author's entire data box of radius 1/100 admits its explicit completion: retain every sampled diagonal and cross entry, set the unobserved within-part off-diagonals to zero. The diagonal lower bound is 9801/10000, the magnitude bound for each of four cross entries is 202/10000, and the uniform row margin is 8993/10000. Symmetric strict diagonal dominance with positive diagonal implies positive definiteness. This is an open set in the original 16-dimensional data space, so its probability is strictly positive. There is no reliance on an exceptional zero-probability witness or on openness in an inappropriate statistic-space dimension.

For one observation, edge 3–5 fixes a singular 2-by-2 principal block in every matching completion. Both endpoints have singleton diagonal colors in both proposed models. Positive definiteness is impossible. This also handles zero observed coordinates and establishes the lower bound for all single observations. Therefore the weak threshold is exactly two in both models.

The data-box two-column rank check is correct: the indicated left/right row determinant is at least 1-2/100. It is not essential to positive probability, but confirms that the box genuinely contains rank-two data throughout.

## 5. Literal contradiction and credited MLT

At n=3 the ideal hypotheses hold, and I8 has statistics in the rank-three elimination variety, since those same statistics have an actual rank-two PSD preimage. Every polynomial in the ideal vanishes at this positive-definite point. Thus no ideal generator can be everywhere nonvanishing on the positive-diagonal Cholesky domain. The example satisfies the second intersection condition, yet its WMLT is two, below the asserted n=3. That is a complete negative answer to the literal numerical question.

I checked Blekherman–Sinn's primary author text, Theorem 2.7 and its theorem-proof context, including the matching lower/upper bounds, and visually inspected the theorem page. The [prior complete-bipartite formula](https://arxiv.org/abs/1703.07849v2) gives MLT(K4,4)=4 because 3*4/2<8≤4*5/2 and the other bound is 5. This is a credited existing theorem, not an independently novel Gaussian threshold result. The current source is the complete author PDF; no access to a publisher PDF is claimed. No exact ordinary MLT is transferred to the tied-diagonal model.

The failure has the correct logical explanation: a success configuration at rank n does not imply that success first becomes possible at rank n. The frozen proof does not infer equality of a statistical threshold merely from the first zero elimination ideal.

## 6. Checks, limitations, and disposition

The independent checker verifies 1,105 right-inverse entries, 54 lower-rank cross-block obstructions, all 16 extreme corners of the bilinear cross-entry bound, and 32 rational perturbations with exact statistics, strict diagonal dominance and all leading principal minors positive. It also checks the surviving singleton edge and classical numerical formula. These are controls supporting the written universal arguments, not statistical simulations or a finite substitute for them.

No mandatory correction was found. Preserve all source-scope caveats, the zero-mean convention, the genuine-color variant, and published-theorem credit. Do not describe this as disproving a pure SOS-versus-intersection dichotomy, as solving a four-cycle-only question, or as a new historical discovery. Under those boundaries the exact frozen candidate passes full independent review.
