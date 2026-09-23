# Publication-priority review

**Audit completed:** 2026-09-23 UTC (2026-09-22 America/Los_Angeles).
**Scope:** a bounded independent literature search for Gromov's 2017 question [?24](i), and for the explicit deformation of small unitary-valued maps proposed in this project.
**Checkpoint:** 100% of this bounded audit completed; absolute publication priority remains undetermined.

## Outcome and permitted claim

No earlier publication explicitly resolving [?24](i), or stating this exact quantitative map-space deformation, was located in the sources and searches below. This is a **qualified no-conflict finding**, not a certification of novelty or an exhaustive priority clearance. The underlying Cayley and operator Möbius transformations are classical. The proof uses elementary consequences of their algebra. The literal topological conclusion also follows from a standard matrix chart, as explained below.

A suitable publication claim is: “We give an elementary explicit deformation that answers Gromov's question [?24](i) and, more strongly, never increases the Lipschitz constant.” Do not claim the first use or discovery of the matrix transformation, a new theory of operator Lipschitz functions, or that this audit proves no previous solution exists. A concise note with the exact theorem, proof, references, and this audit is appropriate; a large novelty narrative is not supported.

This review addresses priority separately from mathematical correctness. The proof review and verification artifacts must supply the latter. No person was contacted, and no outreach was prepared.

## Claim compared

Fix a basepoint p of the round sphere and write A = Φ(p), W = A*Φ. The proposed formula is

    H_t(Φ)(x) = A (W(x) + tI) (I + tW(x))^(-1),  0 ≤ t ≤ 1.

For the unnormalized Hilbert–Schmidt Riemannian distance, and also the operator-norm length distance, the proposed conclusion is a strong deformation retraction of the Lipschitz sublevels Lip < 1/2 and Lip ≤ 1/2 onto the constant maps, continuous in the uniform topology, with

    Lip(H_t(Φ)) ≤ ((1 - t²)/(1 + t²)) Lip(Φ).

The distinction between a single map's null-homotopy, a parameter-continuous family, and a deformation preserving the specified Lipschitz sublevel is essential in comparisons.

## Primary sources checked and comparison

1. **Misha Gromov, _101 Questions, Problems and Conjectures around Scalar Curvature_, October 1, 2017, printed pp. 35–36, §13(f)–(g), [?24](i).** [Author-hosted PDF](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf). The question is indeed about sphere maps into U(N), with Lipschitz constant below 1/2, and a contraction to constants continuous in the map. Its preceding discussion specifies a standard bi-invariant metric with shortest nonconstant closed geodesic length 2π. It already states individual null-homotopy below 1 and discusses families for the circle. It does not explicitly require the homotopy to remain inside the original Lipschitz sublevel. Our reading of the proposed theorem is therefore a quantitative strengthening of the printed assertion. The problem-list URL supplied by the user failed to load in this audit, so the primary PDF is the authority for these details.

2. **Yurii A. Neretin, _Lectures on Gaussian Integral Operators and Classical Groups_, European Mathematical Society, 2011, §1.7.9, Theorem 7.5, printed p. 42.** [Author-hosted PDF](https://www.mat.univie.ac.at/~neretin/lectures/ems.pdf). This gives the Cayley correspondence between self-adjoint matrices B and unitaries W avoiding −1, using iB = (I−W)(I+W)^−1. In these coordinates the proposed F_t is precisely multiplication of B by (1−t)/(1+t). Thus both the chart and its linear shrinking are standard constructions. The cited section does not state the sphere-map deformation or its Lipschitz coefficient. This is a convenient short reference for attribution in the paper.

3. **Luis Velázquez, _Spectral methods for orthogonal rational functions_, J. Functional Analysis 254 (2008), 954–986; [arXiv:0704.3456](https://arxiv.org/abs/0704.3456).** The preprint dates to 2007 and studies operator linear-fractional transformations of unitary matrices. A particularly accessible displayed version is equation (1.3) of **J. S. Christiansen, B. Eichinger, and T. VandenBoom, _Finite-gap CMV matrices: Periodic coordinates and a Magic Formula_, [arXiv:1902.05850v2](https://arxiv.org/pdf/1902.05850), pp. 2–3**. Specializing the scalar parameter to tI gives F_t(W) for t < 1: the auxiliary square-root scalar factors cancel. The paper also notes preservation of unitarity. These sources establish prior use of the transformation itself, in a spectral-theory context. No assertion about Gromov's question, the map-space retraction, or the semicircle contraction coefficient was located there.

4. **Esteban Andruchow and Gabriel Larotonda, _The rectifiable distance in the unitary Fredholm group_, [arXiv:0812.4475](https://arxiv.org/abs/0812.4475), first posted 2008.** This studies convexity of the operator-norm rectifiable distance along unitary geodesics under a π/2 distance restriction, and related Schatten metrics. It is relevant geometric background, not an identified competing resolution. Distance-to-a-fixed-point convexity along geodesics alone should not be cited as a proof that a simultaneous radial homotopy is nonexpansive in its moving endpoint.

5. **Martin Miglioli, _Circumcenters in Finsler unitary groups_, [arXiv:2108.05031](https://arxiv.org/abs/2108.05031), first posted 2021.** In the PDF version accessed, Propositions 3.4–3.5 give geodesic convexity of appropriate unitary balls at radii up to π/2; Corollary 3.6 treats lower bounds on the Hermitian part along geodesics. These propositions concern the same spectral semicircle region as the candidate. They do not state this deformation of a Lipschitz mapping space. **Miglioli, _Geometry of infinite dimensional unitary groups: convexity and fixed points_, [arXiv:2203.06315v2](https://arxiv.org/pdf/2203.06315), 2022**, develops analogous operator-norm and Hilbert–Schmidt geometry. Text searches for “contract” in both retrieved papers found no matches. This negative text result is narrower than a proof that no equivalent corollary follows from their results.

6. **Andrea Seppi, Graham Smith, and Jérémy Toulisse, _On complete maximal submanifolds in pseudo-hyperbolic space_, [arXiv:2305.15103v1](https://arxiv.org/pdf/2305.15103), 2023, Lemma 8.2, pp. 48–49.** This gives a homotopy of sphere-valued 1-Lipschitz maps without antipodal image points to constants, with a decreasing Lipschitz bound. The proof uses geodesic coordinates on a hemisphere. It is a close analogy for the type of conclusion, but the target is a sphere rather than U(N), and it does not give this matrix formula or the stated map-space retraction.

7. **A. B. Aleksandrov, _Operator Lipschitz functions and linear fractional transformations_, Zap. Nauchn. Sem. POMI 401 (2012), 5–52; English translation, J. Math. Sci. 194(6) (2013), 603–627.** [Publisher/institute abstract and bibliography](https://www.mathnet.ru/php/archive.phtml?jrnid=znsl&option_lang=eng&paperid=5224&wshow=paper). The verified abstract concerns closure properties of operator-Lipschitz classes under weighted composition with linear-fractional transformations. This is relevant prior theory, not a direct identification of the exact bound used here. The English survey PDF retrieved through Math-Net timed out; consequently this audit does not claim a full-text exclusion for this literature. The candidate's resolvent identity directly proves its special estimate, so no general theorem from this literature is required for correctness.

8. **Gromov, _Four Lectures on Scalar Curvature_, author-hosted [2019 version](https://www.ihes.fr/~gromov/wp-content/uploads/2019/08/scalar-lectures-IHES-2019-1.pdf) and [July 8, 2021 version](https://cims.nyu.edu/~gromov/lectures%20on%20Curvature%202025/Scalar-Jul-8-2021.pdf).** Searches within the retrieved full texts for “contractible”, “U(N)”, and “unitary group” did not locate a discussion resolving [?24](i). These were targeted searches of long surveys, not a line-by-line audit of all their mathematics. The 2025 directory name of the second URL is not treated as the manuscript's date.

## Why the elementary overlap matters

The following is an inference by this audit, not an attributed theorem from a source. For Lip(Φ) < 1, the diameter estimate gives d(I,A*Φ(x)) < π. Therefore the normalized image avoids eigenvalue −1. Applying the classical Cayley chart, scaling its self-adjoint coordinate to zero, and applying the inverse chart gives a contraction to Φ(p) depending continuously on Φ. Equivalently one can use the principal logarithm. Thus the literal topological assertion of [?24](i) has a standard chart proof, under either metric specified in the candidate.

That observation does **not by itself** verify the sharper uniform estimate or preservation of the Lipschitz sublevel. In the candidate these follow from the noncommutative resolvent identity and the spectral lower bound on I+tW. Both are elementary matrix algebra; the coefficient is an immediate consequence once that region and transformation are chosen. No source explicitly recording that precise combination was found. Its elementary nature and the possibility that it is folklore substantially limit any novelty claim, even when no conflicting paper has been located.

## Reproducible search log

All searches below were run on 2026-09-23 UTC using the available web search engine, with no date restriction. Quotation marks shown below were part of the queries. Search snippets were used to identify documents; substantive comparisons above use author-hosted, arXiv, journal, or institute sources. Search ranking and availability can change. Irrelevant hits (quantum evolution, neural networks, coarse geometry, and unrelated numerical identifiers) were excluded after reading their context.

| Batch | Queries | Material result |
|---|---|---|
| 1 | `"Gromov" "Lipschitz" "1/2" "unitary" homotopy`; `"Gromov" "101" "problems" "unitary" Lipschitz`; `"AMR-066-0025"`; `"unitary group" "space of" "Lipschitz" contraction` | Original Gromov PDF; no direct later resolution. |
| 2 | `"Gromov" "Lipschitz" "unitary" "contracted"`; `"unitary" "Lipschitz" "constant maps" Gromov`; `Gromov "Four Lectures" "Lipschitz" "unitary"` | Later Gromov surveys; sphere-valued analogy. |
| 3 | `"unitary group" "Lipschitz" "deformation"`; `"unitary group" "Cayley" "contractive"`; `Gromov "canonically contractible" unitary`; `"Lipschitz" "unitary" "half" homotopy` | Neretin's Cayley-transform section. |
| 4 | `"unitary group" "geodesic" "convexity" "pi/2"`; `"unitary group" "radial" "contraction"`; `"Gromov" "unitary" "small" "Lipschitz maps"`; `"Lipschitz" "unitary group" "homotopies"` | Andruchow–Larotonda and Miglioli. |
| 5 | `"Circumcenters in Finsler unitary groups" arxiv`; `"Geometry of infinite dimensional unitary groups" Miglioli arxiv`; `"unitary" "Möbius" "Lipschitz"`; `"unitary" "Mobius" "homotopy"` | Primary arXiv versions; no competing mapping-space theorem. |
| 6 | `"Gromov" "Lipschitz" "retraction"`; `"unitary" "semicircle" "contraction"`; `"unitary" "Cayley" "Lipschitz" homotopy` | No direct relevant new source. |
| 7 | `"Gromov" "maps" "U(N)" "1/2"`; `"Gromov" "unitary" "24" contractible`; `"Lip" "U(N)" "constant" "contractible"` | Exact original question; no identified resolution. |
| 8 | `"unitary" "right semicircle" Mobius`; `"unitary" "nonexpansive" "Cayley"`; `"unitary" "Lipschitz" "fractional linear"` | No direct competing theorem. |
| 9 | `"Gromov" "small Lipschitz" unitary maps`; `"AMR-066-0025" solution`; `"6700025" math`; `"maps" "unitary group" "Lipschitz" "contractible"` | Original source or unrelated identifiers. |
| 10 | `"unitary" "1-t^2" "1+t^2" Lipschitz`; `"unitary" "W+tI" homotopy`; `"unitary" "Möbius" "contraction" semicircle`; `"Gromov" "Lipschitz" "Cayley"` | Christiansen–Eichinger–VandenBoom operator Möbius transform. |
| 11 | `"Finite-Gap CMV Matrices" "arxiv"`; `"Mobius Transformations in Noncommutative Conformal Geometry" arxiv` | Exact CMV preprint identified; broader operator Möbius background. |
| 12 | `"Spectral methods for orthogonal rational functions" arxiv`; `"fractional linear transformations" "Lipschitz" operators unitary`; `"Cayley transform" "non-expansive" matrices` | Velázquez preprint; Aleksandrov literature lead. |
| 13 | `"Operator Lipschitz functions and linear fractional transformations"`; `"operator Lipschitz" "fractional" Aleksandrov Peller` | Verified Aleksandrov abstract/bibliography; survey PDF fetch failed. |

Primary documents were also searched internally as detailed in the comparisons. All dates in bibliographic entries were taken from manuscripts or bibliographic records, not search-engine crawl dates.

## Limitations and release language

This audit did not search subscription MathSciNet or zbMATH databases, inspect every citing paper, read every relevant monograph, or rule out unpublished notes, seminar knowledge, alternate terminology, or unindexed literature. It did not verify the problem aggregator's current status. Public availability in Gromov's 2017 list is evidence that he posed that question there, not evidence that it remained unresolved in September 2026.

The mathematical note may be released with a clearly stated affirmative theorem and references to the classical machinery. Its abstract and metadata should say that it supplies an explicit answer and quantitative strengthening, while the priority statement should remain “no earlier explicit resolution located in the documented search.” A DOI records a deposited version; it does not establish first discovery, peer review, or exhaustive priority verification.
