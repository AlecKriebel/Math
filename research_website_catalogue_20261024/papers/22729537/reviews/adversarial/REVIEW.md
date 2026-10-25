# Independent adversarial review — Zenodo 22729537

**Verdict: no substantive defect found in the reviewed published version.** The central all-length sequence–genealogy equivalence and the complementary compact finite-determination/unbounded-epoch obstruction are supported by the stated proofs. The graph statements must retain their explicit incidence-separation and scalar-separator-faithfulness hypotheses. This is an AI-assisted mathematical review, not human peer review, formal proof certification, or novelty certification.

Review completed 2026-10-25 UTC (2026-10-24 America/Los_Angeles). No archived reviewer verdict, other current reviewer verdict, or companion-paper result was consulted in reaching this conclusion. No source manuscript was modified, no defect repair was attempted, and no external individual was contacted.

## Exact reviewed artifacts

Record: [Zenodo 22729537](https://doi.org/10.5281/zenodo.22729537), version 1.0.0, *Direct Sequence Laws under the Network Multispecies Coalescent: A genealogy equivalence, canonical coalescent-response behavior, and finite determination with an epoch-complexity obstruction*.

| Artifact | SHA-256 |
|---|---|
| `NMSC_Paper_A_Main.pdf` — 37 pages | `734dd6701b62bb913ae1b7c0d48361dc8fdb94128173c4882a7d2bfc59319304` |
| `NMSC_Paper_A_Supplement.pdf` — 27 pages | `8d125e118d2ca5859f91136181cdca30b792dc1a1b25f2458b486105bf8befb0` |
| `NMSC_Paper_A_Source.zip` | `87417fe7910997557d5c193a53739a96f06fec3afd874a8b8094ebc1a2d06654` |
| `NMSC_Paper_A_Reproducibility.zip` | `fdfe0b69bb63d3ef6faf2502541889300c0e1c5f1ad28bd9f4de89b4f3825dc5` |

Read the entire main and supplement through their delivered TeX sources (1,393 and 1,093 lines), including the qualifications and supporting proofs; extracted the delivered PDFs and crosschecked their theorem statements, numbering, and page coverage. The review addresses both published PDFs together. A byte-identical source-to-PDF rebuild was not performed; the downloaded PDFs and source archive are individually hash-bound above.

## Claim-by-claim adversarial assessment

**Theorems 4.1, 5.2, 6.2, and 7.1: all indexed locus laws recover the normalized triple.** The moment argument correctly uses the law of the random *conditional* site-pattern vector, rather than the population-averaged site matrix. All ordered alignment probabilities supply monomial moments; trailing-site marginalization supplies lower moments. Compact-simplex moment determinacy is sufficient. The determinant identity reconstructs the normalized additive metric independently of the substitution eigenbasis. Contemporaneous sampling then locates the root at the ultrametric center. The reversible similarity ensures that a positive-distance realized conditional pair matrix has a real principal logarithm equal to its normalized generator times the determinant distance. This handles repeated eigenvalues and connected zero-conductance faces. The proof does not divide by an eigenvalue gap.

I checked the quantifier boundary carefully: the input is the exact population-law family indexed by every locus length, with known nonrecombining boundaries, iid sites conditional on genealogy, one shared stationary reversible generator, and labelled contemporaneous samples. This is not a finite alignment reconstruction algorithm. The determinant-zero limit at infinite age has no probability mass and is explicitly handled as a null complement. Physical time retains the usual scalar conversion ambiguity. The Borel inverse relies on compact moment-map inversion and measurable selection of positive-determinant support points, not on an unproved uniqueness of a species graph.

**Section 8: finite response behavior and equality testing.** Finite partition–occupancy states give finite exact complete-history density products. The prefix-span and backward-nullity arguments use analytic continuation on connected chronological simplexes; they correctly concern spans, not equality of individual earlier/later prefixes. The supplement supplies the missing substantive step for deleting invisible boundaries: both residual transport isomorphism and analytic marked-map gluing. The Sylvester recurrence acts on raw adjacent matrix dimensions, so the bound is not mistakenly inferred from small residual rank. The finite mixed derivative box determines all Taylor coefficients. Exact proposed-system comparison explicitly assumes a terminating equality domain and does not claim an algorithm for unrestricted black-box real inputs. The intrinsic positive cone is not advertised as a stochastic occupancy basis or an NMSC realization.

**Theorem 12.2: finite determining length on compact charts.** The proof works in the ring of analytic germs along the entire compact parameter-pair set. It avoids the invalid inference that infinitely many pointwise local analytic identities share one fixed neighborhood. Each fixed locus probability admits its own analytic neighborhood; this suffices for membership in the compact-germ ring. Positive root absorption gives the needed locally stable transient resolvent. Repeated hazards and eigenvalues do not require denominator cancellation. The main paper and supplement impose finite presentation size, compactness, semianalyticity, fixed event-order charts, and strict physical parameters. No effective bound or unrestricted noncompact fixed-presentation theorem is claimed.

The imported real-analytic result was checked in the original [Siu 1969 reprint, Theorem 2 on printed p. 488 and final Remark on p. 489](https://people.math.harvard.edu/~siu/siu_reprints/siu_noetherian_stein_ring_proc_ams1969.pdf). It gives the asserted Noetherian criterion on coherent real-analytic spaces. Compact semianalytic intersections supply finite connectedness. The application is consistent with the primary source; it is not inferred merely from the article's holomorphic title.

**Theorem 12.4: no order bound that omits demographic epoch complexity.** The Laplace first derivative has the stated positive sign and factor `s exp(-(s+lambda0) a_j)/(s+lambda0)^2`. Removing positive row and column factors produces a Vandermonde matrix with distinct nonzero nodes. Its first L rows have full row rank; the next row is independent. The implicit-function theorem produces a curve matching the first L moments while changing the next. Every coordinate of its tangent is nonzero because each L-column minor is nonzero. Choosing two small nonzero parameters therefore retains genuine rate changes, positive cumulative hazards, and positive durations. The conversion from JC pair pattern probabilities to moments uses affine probabilities with a nonzero highest-order coefficient. This establishes exact existence for every L; numerical root solves below are supporting controls only.

**Graph results and reductions.** The sample-unary funnel replacement has no possible merger or side entry and fixed elapsed time, so its entire local genealogy response is invariant. Species-tree inversion uses pair support thresholds and hazards; terminal singleton rates remain explicitly unexposed. The one-reticulation coefficient quotient is a complete encoding of all marked histories split at a common law-defined time; it does not improperly compare raw reticulation cuts with different reachable partition dimensions. Pair co-occupancy recovery via shifted Hankel moments handles coincident rates after combining their atoms. The private-side and pair-exposed assumptions are essential for the incidence result. The balanced parent-word example correctly prevents an overclaim of raw demographic word linkage.

The level-1 conclusion is conditional: proper-cluster separator faithfulness and local incidence separation are hypotheses, not consequences established for every level-1 network. The full-sample argument separately uses strict routing and survival to retain the Cartesian support of all no-merger route assignments; a frozen process with a split population assignment cannot have Kingman completion probability tending to one. The occurrence records preserve repeated clusters and full-sample corridors. Nothing in this review supports dropping those hypotheses or advertising general network topology recovery.

**Statistics and local fibers.** The increasing-order consistency proof directly compares the approximate minimizer with the eventually available true model and controls the product-metric tail; it does not require compactness of the union of sieves. McDiarmid plus Borel–Cantelli gives the stated almost-sure control under `d^L/K -> 0`. First-variation jet bounds are enlarged using the augmented Sylvester operator. The paper distinguishes the derivative kernel from the real arc tangent cone, so singular points are not wrongly assigned a fiber dimension by naive Jacobian nullity.

**Other primary import check.** The divided-difference sign and confluent scaling agree with [de Boor, *Divided Differences*, formula (52), printed p. 64](https://pages.cs.wisc.edu/~deboor/sat/papers/2/2.pdf). The paper's attribution that metric genealogy ambiguity precedes this work is consistent with the sampling-dependent examples discussed by [Zhu and Degnan 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5837799/). This limited check is not a systematic novelty search.

## Reproduction and independent controls

The public runner verified its complete 25-file inventory and ran all six groups successfully using SymPy 1.14.0 and mpmath 1.3.0. See `replay-full.json`:

- 384 exact first-variation recurrences and the rejected undoubled negative control.
- 26 grouped intrinsic port-reanchoring checks.
- 972 block-tree occurrence reconstructions.
- 14 moment fixtures, 24 boundary fixtures, and 3,130 child/port predicates.
- 40 symbolic regressions and 13 negative controls.
- 10 independently recomputed anchors and 13 killed mutants.

I independently wrote `independent_controls.py`, importing none of the paper implementation. Its output is `independent-controls.json`:

- Three reversible-generator cases (generic unequal stationarity, connected zero-conductance path, JC repeated eigenvalues), each at four coalescence ages. Maximum determinant-distance error was `8.9e-16`; maximum recovered-generator entry error was `1.75e-13`.
- A nonreversible directed-cycle control preserved the determinant identity but failed reversible generator inversion, as expected. This confirms the importance of the theorem's reversibility boundary.
- At 90 decimal digits, independent piecewise-exponential Laplace integration and moment differentiation verified the Jacobian formula and constructed numerical collision pairs for L=1,...,6. Lower-moment residuals were below `1.6e-90`; each next moment and the corresponding all-diagonal next-length probability differed. All cumulative rates stayed positive and every step increment was nonzero. These are high-precision numerical witnesses, not exact certificates replacing the analytic existence proof.
- Shifted-Hankel co-occupancy checks passed for repeated rates, three distinct rates, and nearly coincident rates.
- Conditioning controls exposed the expected numerical difficulty: the L=6 moment Jacobian had double-precision condition number about `1.69e8`; a near-coincident decoder matrix had condition number about `1.81e15`; saturated JC determinant distances eventually lost substantial floating-point accuracy. The paper claims population identifiability, Borel inversion, and qualified consistency, not uniform stable estimation, so these are limitations rather than counterexamples.

## Remaining limits and publication-facing wording

No established substantive error requires deferral on this adversarial review. Universal claims were checked by mathematical argument, not formally verified. I did not run a complete new network enumerator, reproduce a typesetting build, verify the companion manuscript, prove all cited classical theorems afresh, or certify priority. The supplied bounded suites cannot establish universal graph completeness or a practical sample-size bound.

A public synopsis can accurately emphasize that complete within-locus sequence laws determine mutation-scaled genealogy behavior under the model, while literal species networks can remain ambiguous; compact fixed-complexity classes admit a finite determining length, but demographic epoch complexity cannot be ignored. It should preserve the strict model assumptions, distinguish identifiability from stable inference, and retain the qualified graph scope.

No follow-up conjecture is recommended for public listing by this review. Establishing an effective, quantitatively stable finite-length inference theorem would require a separately scoped research program and should not be presented as a quick corollary.
