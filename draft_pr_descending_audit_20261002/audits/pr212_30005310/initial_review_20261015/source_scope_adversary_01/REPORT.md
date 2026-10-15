# Independent source-scope adversarial report: PR212 / 30005310

Audit completed 2026-10-15, UTC. Completion estimate: 100% of the assigned source-scope audit, not a claim of historical priority certification or of resolving a different algebraic conjecture.

## Verdict

**PASS for the narrowly stated source-literal numerical counterexample.** The connected colored `K4,4` construction is in the original written domain. It satisfies `I(G,3) != 0`, `I(G,4)=0`, and `WMLT(G)=2`. It also satisfies the second antecedent of the source's Proposition 3 at `n=3`, whose displayed conclusion requires `WMLT(G)=3`. Thus it directly disproves a numerical assertion actually printed in the primary source; that assertion was not invented by the cleaned database record. It also disproves an exhaustive classification that retains the complete printed mechanism-and-threshold scenarios.

**Do not state that this example falsifies the bare SOS/intersection exhaustiveness conjecture.** The example satisfies the positive-definite-intersection alternative. The one-sentence original Conjecture 4 refers back to Proposition 3 without separating its mechanisms from its numerical conclusions. Consequently the strongest interpretation-independent conclusion is the explicit counterexample to Proposition 3's second numerical implication. A claim simply labeled “Conjecture 4 solved” would be insufficiently precise. The existing proof's express numerical-scenario qualification is substantive and must remain attached to any disposition.

I found no support for an omitted four-cycle-only restriction. Insulating the general printed numerical assertion by imposing that restriction would invent an assumption. Conversely, taking the numerical error as a refutation of the antecedents-only alternative would overstate what was proved. The existing distinction is therefore required by logic, not a concession to either the candidate or a later queue interpretation.

## Independent sequence and source control

I first read only the submitted `source_record.json` as a lead. Before candidate access I downloaded the official OWR PDF, verified its supplied SHA-256, read the entire Homs/Kuznetsova contribution, and rendered/viewed all four contribution pages, physical PDF pages 26-29 / printed pp. 3146-3149. The independently dated `TARGET_FREEZE_20261015.md` was written at `2026-10-15T09:35:40Z`; its SHA-256 is `6c71c66be2e07fc01abb6a9360694a48bf7b910b46c427bcd7ef7e6763de71c3`.

Only then did I read the full submitted proof, publication status, sources, verifier, receipts, logs and metadata. I independently reconstructed the key arguments before reading `independent_review/FINAL_REVIEW.md` last. Its earlier PASS was treated as a claim to test, not as an audit premise. I did not replay either submitted checker because the author's checker writes into its own submitted folder; I instead wrote and ran a separate exact checker within this audit folder.

Official original source: <https://ems.press/content/serial-article-files/46992>, DOI `10.4171/owr/2022/55`, downloaded SHA-256 `56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`.

## Source-defined target and the curation comparison

The source defines a colored graphical model using arbitrary partitions of the vertices and edges of an undirected graph. The concentration matrix is real positive definite, has zeros on nonedges and equal entries within color classes. No regularity, proper-coloring, connectivity, fixed vertex count, or requirement for nontrivial colors is added. Both singleton coloring and the submitted equality `K11=K22` are legal. The latter constraint changes the statistic from separate covariance diagonals to their sum; it does not require equal covariance diagonals.

The source's real sufficient-statistic map records vertex diagonal sums and edge entry sums. It defines `I(G,n)` by eliminating a generic symmetric matrix from these linear statistic equations and *all* `(n+1)`-minors. These are algebraic rank constraints, without PSD inequalities. The source distinguishes positive probability (WMLT) from probability one (MLT), and associates `n` observations with rank-at-most-`n` sample covariance. Its elimination criterion gives an upper bound for the almost-sure threshold when the ideal is zero.

On p. 3148, Proposition 3 assumes the last two ideals are nonzero at `n` and zero at `n+1`. Its signed-SOS case states `(WMLT,MLT)=(n+1,n+1)`. Its real-PD-intersection case states `WMLT=n`, `MLT=n+1`. On p. 3149 Conjecture 4 says that its two cases exhaust the possibilities. Therefore the database did not add the false minimum equality. The database's phrase “exactly one” is a formalization absent as an explicit phrase from the source, but is not the cause of this counterexample. At any real PD point in the ideal variety every ideal member vanishes, so the two given antecedents cannot both hold if the signed-SOS certificate is required to be nonvanishing on that entire domain.

The four-cycles on p. 3147 are examples with threshold illustrations. The paragraph after Proposition 3 describes an application to four-cycles, and Fig. 3 illustrates a specific graph from an earlier table. Neither displayed result has a four-cycle hypothesis, and the full contribution contains no enclosing four-cycle-only assumption. Nor does the preceding contribution transfer any such assumption: it ends before Homs's title and initial definitions.

One minor notation issue in the source is immaterial here: Proposition 3 names a lower triangular Cholesky factor, while the displayed example uses entries above the diagonal. The candidate's obstruction to every nonvanishing certificate uses `I8`, which is valid under either triangular convention.

## Independent mathematical checks against scope escape routes

### Exact ideal hypotheses

For both colorings the sixteen cross-block entries remain individual statistics. Their `4 x 4` determinant is a nonzero polynomial (value one at cross block `I4`) and is an actual, generally nonprincipal, minor of the full symmetric matrix. Substitution through the statistic equations puts it in the exact rank-three elimination ideal. This proves `I(G,3) != 0` without needing a radicality or PSD-image assertion.

For the rank-four condition, let the eight-by-four data matrix be `[I4; V]`, with rows of `V` equal to `e1+e2`, `e2+e3`, `e3+e4`, `e4+e1`. I used the adjoint of the Gram-statistic differential rather than the submitted pivot calculation. A possible adjoint kernel matrix has diagonal blocks `diag(a)`, `diag(b)` and cross block `C`. Its product with `[I4;V]` vanishes only if

```text
C = -V^T diag(b),        diag(a) = V^T diag(b) V.
```

The four off-diagonal entries at unordered pairs `12,23,34,14` of the right side are respectively `b1,b2,b3,b4`. They force `b=0`, then `C=0` and `a=0`. Hence the differential is onto all 24 singleton statistics. Composing with the surjective sum-of-first-two-diagonals map gives surjectivity for the 23 colored statistics. The image of rank-at-most-four real Gram matrices contains a real open set. Every polynomial in `I(G,4)` vanishes on this set, so is identically zero. The witness has rank four because its upper block is the identity even though `V` itself is singular. This proves the exact ideal assertion over `R`; complex coefficients give the same conclusion by taking real and imaginary parts.

### The weak threshold is a minimum

The eight-by-two matrix with left rows `e1` and right rows `e2` has covariance `diag(J4,J4)`. Its observed diagonal and cross statistics equal those of `I8`. More than one isolated witness is needed for positive probability. In the entire data box of radius `1/100` around it, retain the diagonal and cross Gram entries and fill unobserved within-part off-diagonals by zero. Every diagonal is at least `9801/10000`; each of its four cross entries has absolute value at most `202/10000`. The completion has strictly positive row margin `8993/10000`, and is PD by symmetric strict diagonal dominance. Both colorings have the required matching statistics. Every nondegenerate zero-mean Gaussian distribution has positive density throughout the two-observation data space; this box therefore has positive probability. Scaling covariance by `1/2` changes none of the existence conclusions.

The matching-PD-completion implication can be checked directly without relying on the disputed proposition. If `M` is such a completion and `K` is any feasible concentration matrix, the statistic equalities give `tr(SK)=tr(MK)`, including for the tied diagonals. The negative log likelihood is `tr(MK)-log det(K)`. The strictly positive minimum eigenvalue of `M` makes it tend to infinity when `K` grows without bound; on bounded sets it tends to infinity at the singular boundary. It attains a unique minimum in the PD concentration cone by strict convexity.

For one observation use edge `3-5`, whose endpoints have singleton diagonal colors even in the tied model. If the observed values there are `x3,x5`, the vector supported at those endpoints with coordinates `(x5,-x3)` annihilates the observation. Its nonzero rank-one PSD outer product is allowed in the concentration subspace. Along `K=I+t vv^T`, the sample trace term is constant and `log det(K)` grows without bound, so no MLE exists. If both endpoint values vanish, choose the coordinate vector at vertex 3 instead. This directly checks the one-sample failure in all cases. Hence `WMLT=2`, not merely `WMLT<=2`.

### Algebraic versus real intersection and exact rank

`pi_G(I8)` belongs to the rank-three elimination variety because it has the actual PSD rank-two preimage just exhibited. This avoids any inference from algebraic closure to real PSD realizability. Even replacing “rank at most three” by “exactly three” cannot rescue the minimum equality: take eight-by-three rows `e1` at all four left vertices, `e2` at right vertices 5 and 6, and `e3` at right vertices 7 and 8. Its covariance has exact rank three, diagonal one, cross block zero, and statistics equal to `I8` for both colorings.

Every ideal member therefore vanishes at the PD covariance `I8`, with Cholesky factor `I8`. No ideal member can be nonvanishing throughout the positive-diagonal Cholesky domain, independently of the chosen generating set. Thus `B` holds and `A` fails. This also pinpoints why the example cannot be a counterexample to `A or B`.

## Imported theorem and sample conventions

I reused the complete primary author PDFs already present in the parent's private-reading folder rather than redownloading them. Blekherman-Sinn `arXiv:1703.07849v2` has SHA-256 `dd87cd09fd9a133f182e73a536233b12aaa6dd698e40f2a2da2a5406633a3572`. I read its projection and generic-rank setup, Definition 1.4, Proposition 1.5 with proof, and Theorem 2.7 with the complete matching-bound proofs of Lemmas 2.8-2.10; I rendered and visually read printed pp. 15-18. Theorem 2.7 uses `M=min{k: k(k+1)/2 >= a+b}` and gives ordinary `MLT(K(a,b))=min(M,a+1)`, `b>=a>=2`. At `(a,b)=(4,4)` it gives `4`. Its PSD/PD completion definition matches the candidate's convention. I did not re-prove all external results cited within that theorem. The exact MLT value is credited prior mathematics and is unnecessary for the numerical contradiction; it is not transferred to the colored variant.

The rigidity comparison PDF `arXiv:2108.02185v3` has SHA-256 `0dbdf21070738cf31179cb6ee4ebe9481e5d984fd88bb93dd9565ef7a03105a9`. Its pp. 1-2 explicitly use `N(0,Sigma)` and sample covariance `XX^T/d`, confirming the rank indexing. I also read its Section 8, pp. 23-24, including the definition of weak MLT and the chromatic-number upper bound credited there to Gross-Sullivant. This is consistent with weak threshold two for an ordinary bipartite graph. I did not use it to establish the colored claim or claim a full priority search. No publisher PDF, unavailable page, or unread dependency is represented as read.

## Check artifacts, disagreements, and disposition requirements

The separate `source_math_check.py` passes **16 exact assertions** using SymPy 1.14.0 from the workspace `.venv`, including the adjoint-stress equations, real witnesses of ranks two and three, statistics for both colorings, rational PD margin, direct one-sample likelihood ray, and the credited theorem arithmetic. `SOURCE_MATH_CHECK.json` records the run. These finite computations support the displayed universal arguments; they do not substitute for probability or source interpretation.

The inherited review's mathematical and scope conclusions agree with this independent reconstruction. Its claimed 188/1808 test counts were not relied on or independently recounted in this source-first audit. The submitted proof's stale “review pending” header is an editorial issue, not evidence against its mathematical conclusion.

No mathematical repair is required to make the scoped Proposition 3 counterexample valid. Promotion must retain the following concrete limitations:

1. Name the refuted claim as the printed numerical threshold implication / full literal numerical scenarios. State that the example satisfies the second intersection hypothesis and does not refute antecedents-only exhaustiveness.
2. Do not insert a four-cycle restriction into the source; if such a separate question is considered, mark it unresolved here.
3. Retain the zero-mean rank convention, the open-set probability argument and the one-sample lower bound.
4. Credit the ordinary MLT value as existing mathematics; make no new-discovery or historical priority claim. A full priority certification remains outside this audit.

The exact remaining research gap is a proof or counterexample for the bare mechanism alternative in the general source-defined model class, or a separately formulated restricted question. This candidate supplies neither, and no source-aware audit should silently relabel the current source correction as that result.

No external individual was contacted, no outreach was prepared, and no Git, PR, queue, tracker, cache/DB, or publication state was changed. All authored output is confined to this reviewer's assigned folder; full primary PDFs, extracted third-party text and rendered pages are private reading assets.
