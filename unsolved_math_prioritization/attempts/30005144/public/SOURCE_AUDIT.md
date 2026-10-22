# Source, scope, and literature audit

Checked 3 October 2026.

## Original source

The catalogue identifier is **30005144 / OWR-10252937-007** and its descriptive title is **CMC Min–Max Width Under Nonnegative Scalar Curvature**. The code and descriptive title are catalogue metadata; neither is a numbered problem heading in the original report.

The actual source contribution is Liam Mazurowski, *Prescribed Mean Curvature Min-Max Theory in Some Non-compact Manifolds*, pp. 1574–1576 in *Geometrie*, Oberwolfach Report **28/2022**, DOI [10.4171/OWR/2022/28](https://doi.org/10.4171/OWR/2022/28). The report's title page gives the workshop dates 12–18 June 2022. The conjecture is the last paragraph on p. 1576, referring back to Theorem 2 and equation (1) on p. 1575. The official report PDF was inspected: [EMS source](https://ems.press/content/serial-article-files/46965).

Equation (1) is the strict width bound \(\omega<(4\pi/3)(2/c)^2\). The hypotheses carried from Theorem 2 are completeness, asymptotic flatness, dimension three, no boundary, and \(c>0\). The conjecture adds nonnegative scalar curvature and exclusion of Euclidean space. The following paragraph defines the width using paths from the empty set to a negative value of area minus \(c\) times volume. Thus this is a CMC mountain-pass inequality, not a conjecture about the existence of a minimal hypersurface.

The public catalogue page was tried first but was inaccessible through the web tool. The pinned catalogue was used to recover metadata; its August 2026 'open' assessment was not treated as authoritative. The official source independently confirms the mathematical target. No matching research-results record was found under the ID, code, or title in the pinned report corpus.

## Relevant primary literature

1. **Mazurowski (2022 preprint).** [arXiv:2204.07493v1](https://arxiv.org/abs/2204.07493v1). Definitions 5–6 specify \(\mathbf F\)-continuous compactly supported Caccioppoli-set paths. Definition 26 (p. 18) prints smooth convergence at infinity plus \(h=O(r^{-1})\) and \(\partial h=O(r^{-2})\). The later article's verified bibliographic record is *Advances in Mathematics* 464 (2025), 110133, [DOI](https://doi.org/10.1016/j.aim.2025.110133); its final full text was not verified.
2. **Mazurowski–Zhu (2025 preprint).** [arXiv:2502.18455v1](https://arxiv.org/abs/2502.18455v1), submitted 25 February 2025. Section 2's weighted-C³ condition, Proposition 2.1, and the proof of Theorem 4.3 give the strict-width result for that asymptotic class. Theorem 1.5 and Corollary 2.6 provide smooth point-emerging flow and uniform spatial control without global scalar-curvature nonnegativity; Lemma 2.3 supplies the initial Hawking-mass limit. These are the decisive imported inputs. Only v1 and no journal reference were present on the arXiv record checked here.
3. **Positive mass rigidity.** Agostiniani–Mazzieri–Oronzio, *A Green's Function Proof of the Positive Mass Theorem*, Theorem 2.1, *Communications in Mathematical Physics* 405, 54 (2024), [DOI](https://doi.org/10.1007/s00220-024-04941-8). This is used only to rule out an eventually flat, non-Euclidean original manifold, never on the auxiliary patched metric.
4. **Smooth Geroch monotonicity.** Huisken–Ilmanen, *The Inverse Mean Curvature Flow and the Riemannian Penrose Inequality*, *J. Differential Geometry* 59 (2001), 353–437; [primary PDF](https://www2.math.ethz.ch/EMIS/journals/NYJM/jdg/p/2001/59-3-1.pdf). The local equality argument needed here is also written out in `PROOF.md` rather than simply asserting strictness.

## Hypothesis reconciliation

- **Curvature:** scalar curvature, not Ricci curvature; zero scalar curvature is included.
- **Dimension:** exactly three. No higher-dimensional conclusion is claimed.
- **Boundary:** the original has no boundary. Mazurowski–Zhu allow boundary in their existence theorem, but a Euclidean end can coexist with nontrivial interior boundary. That larger class is not substituted into this strict-width claim.
- **Connectedness:** the standard connected-manifold interpretation of the source is used. Arbitrary disconnected unions with compact extra components are not claimed as an extension.
- **Asymptotics:** the original referenced preprint's unweighted smooth convergence is not silently equated to the later weighted-C³ hypothesis. Section 3 of `PROOF.md` constructs one auxiliary metric satisfying the stronger conditions, then transfers one trapped smooth flow back isometrically. That reduction is part of the candidate requiring audit.
- **Euclidean case:** the width equals \(16\pi/(3c^2)\), so exclusion of Euclidean space is necessary. A non-strict bound alone does not settle the question.
- **Path class:** smooth positive-time leaves, collapsing continuously at the empty endpoint, furnish the cited \(\mathbf F\)-continuous mountain-pass paths with common compact support.
- **Strictness:** positivity of Hawking mass and compactness of the path parameter both matter. Pointwise strict isoperimetry alone does not justify a strict supremum on a noncompact parameter set.

## Prior-attempt and duplicate checks

The live `main` queue showed rank 484 as `queued`, `0/5`, with blank Chat, Findings, and DOI cells. The current `history.jsonl`, `state.json`, and `review_v2/related_target_groups.json` had no target match. The live `attempts/` directory and the commit history for `attempts/30005144` had no record for this target. GitHub PR searches for the ID, `CMC` with `width`, and `Mazurowski` had no matches; `mean curvature` returned an unrelated conical-flow source-repair package. Searches for `scalar curvature` returned unrelated ball-map and capacity–volume problems. These are not mathematically identical prior attempts.

A semantic scan of the pinned catalogue for asymptotically flat min–max questions and curvature-width questions found this exact CMC target once; band-width, intrinsic-flat stability, Bartnik extension, and minimal-graph questions are different. No prior mathematically identical attempt was found. GitHub code search returned no indexed matches, and a recursive-tree fetch failed, so this is not represented as an exhaustive audit of every historic branch.

## Disposition and credit

The standard weighted-C³ problem is a consequence of prior literature. The explicit original-convention reduction is submitted for fresh independent audit. Until that audit succeeds, this packet is a **candidate**, not a certified full resolution. If it succeeds, the proposed disposition is `already_solved` as a credited literature-based finding, with `1/5` substantive research attempt recorded. The principal mathematical advance is Mazurowski–Zhu's theorem. This work makes no first-resolution or historical-priority claim and does not claim human peer review.
