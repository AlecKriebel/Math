# Fresh literature, scope, and attribution audit (2026-08-27 package)

## Status

**PASS.** I found no unsupported load-bearing attribution, no material overstatement of the cited literature, and no scope claim that silently enlarges the theorem beyond the stated physical, graph-theoretic, or inferential regime. The search evidence is consistent with the submission occupying a new K2P level-2 niche, but it is not—and cannot be—an exhaustive priority guarantee.

This was a fresh audit of the 20260827 package, not an adoption of a prior referee conclusion. I inspected:

- `article/main.tex`: 85,978 bytes, SHA-256 `d1344711d3d85ce5936574ccf54bcfbea1bf4164a0d2b6f5d25d5ecb483991bb`;
- `article/references.bib`: 6,960 bytes, SHA-256 `781dd3503c00d9bbd9c1a7d551786fc4be393e883f7ac4c0b0fd712943a9e5c6`.

The bibliography has 16 entries. The article has 21 citation occurrences using all 16 keys, with no missing and no uncited bibliography keys. All 16 recorded links resolved to the intended primary record on 2026-08-27/28; three publisher sites returned access-control HTTP 403 to automated retrieval after the DOI resolved, not a broken DOI. Current versions were checked explicitly for the time-sensitive sources: Englander et al. bioRxiv v4, Brits et al. arXiv v3, and Kriebel JC Zenodo v1.1.7.

## Load-bearing attribution matrix

| Article lines | Assertion tested | Primary-source check | Status |
|---|---|---|---|
| 130–134 | Kimura introduced a two-rate transition/transversion model with the usual symmetric stationary setting; group-based Fourier treatment follows Evans–Speed and Sturmfels–Sullivant. | The bibliographic metadata and paper scopes match: [Kimura 1980](https://doi.org/10.1007/BF01731581), [Evans–Speed 1993](https://doi.org/10.1214/aos/1176349030), and [Sturmfels–Sullivant 2005](https://doi.org/10.1089/cmb.2005.12.204). The submission derives its own inverse Fourier formulas at lines 303–344, so the citation is contextual rather than a substitute for a load-bearing calculation. | **PASS** |
| 134–140 | Invariant, Jacobian, and algebraic-matroid methods distinguish single-cycle/level-1 classes; three-sunlet group-based varieties have been studied. | [Gross–Long 2018](https://doi.org/10.1137/17M1134238), [Hollering–Sullivant 2021](https://doi.org/10.1016/j.jsc.2020.04.012), and [Gross et al. 2021](https://doi.org/10.1007/s00285-021-01653-8) have exactly the claimed network-identifiability scope. Gross et al.'s abstract states generic identifiability for triangle-free level-1 networks with fixed reticulation count under JC/K2P/K3P. [Cox–Gross–Martin 2025](https://doi.org/10.1007/s11538-025-01506-1) directly studies group-based models and dimensions on 3-sunlets. | **PASS** |
| 137–139 | Brits et al. prove full K2P identifiability for level-1 networks modulo triangle redirection. | The cited, current [arXiv v3](https://arxiv.org/abs/2607.12919v3), dated 25 August 2026, states in Theorem 4.9 that distinct level-1 semi-directed networks modulo reticulation placement in triangles have disjoint restricted physical model images for JC, K2P, and K3P. This is stronger than generic separation and supports the sentence as written. | **PASS** |
| 141–144 | Prior level-2 work gives invariant calculations for simple/semisimple networks and quartet reconstruction for outer-labeled planar galled networks. | [Ardiyansyah 2021](https://arxiv.org/abs/2104.12479v1) explicitly studies distinguishability of simple and semisimple nice level-2 networks via Fourier invariants, with stated restrictions. [Holtgrefe et al. 2025](https://doi.org/10.1007/s11538-025-01549-4) characterizes the canonical information recoverable from displayed quartets for outer-labeled planar, galled level-2 networks and develops the inter-taxon quartet distance. Calling these “complementary partial classifications” is accurate and appropriately qualified. | **PASS** |
| 146–148 and 940–943 | Huber et al., Lemma 4.2 and Figure 8, classify exactly two semi-directed level-2 generators underlying simple strict level-2 networks. | The publisher paper [Huber et al. 2025](https://doi.org/10.1007/s11538-025-01510-5) says at Lemma 4.2: the semi-directed level-2 generators are precisely the two mixed graphs in Figure 8, and proves exhaustion from the three-path undirected generator. The article uses this only after giving its own directed four-event-placement derivation at lines 896–943. | **PASS** |
| 148–153, 432–466 | Englander et al. Propositions 2.9–2.10 and Theorem 2.11 give JC/K2P displayed-quartet separation; Corollary 2.12 recovers the tree of blobs; their main level-2 algebraic classification is JC. | The current [bioRxiv v4 primary record](https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4) has exactly those proposition/theorem statements. Theorem 2.11 assumes positive mixing weights and proves disjoint JC/K2P model images when a four-leaf restriction has a different displayed-quartet set. Corollary 2.12 states disjointness for nonisomorphic trees of blobs. The level-2 theorem is JC-only. The submission's strict inheritance domain satisfies the positivity hypothesis and lines 432–462 independently recompute the specialized K2P pullback/sign table. | **PASS** |
| 155–161 | The companion JC work uses the same directed ported refinement and records incoming/event/repair/ordered-word data. | Zenodo record [Kriebel JC v1.1.7](https://doi.org/10.5281/zenodo.22089373) identifies the cited version and supplies the paper. Its Sections 3–4 explicitly use the four directed theta cores, incoming roles, path-sink child ports, minimum strong repairs, and ordered subdivision words. The self-citation is transparent and the claim is accurate. | **PASS** |
| 236–238 | Semple–Steel and Holtgrefe et al. are standard references for rooted and semi-directed conventions. | [Semple–Steel 2003](https://doi.org/10.1093/oso/9780198509424.001.0001) is an appropriate rooted-network/tree reference. [Holtgrefe et al. 2026](https://doi.org/10.1007/s12064-025-00453-8) defines semi-deorientation, rootings, and weak/strong membership in rooted classes. The submission clearly declares its narrower one-step, simple fixed-mixed-graph convention before citing these references; it does not misattribute that exact convention to them. | **PASS** |
| 780–795, 1418–1419, 1457–1460 | Finite semialgebraic covers, Tarski–Seidenberg, and equality of semialgebraic dimension with the real Zariski closure. | The citations point to the correct standard locations in [Bochnak–Coste–Roy, *Real Algebraic Geometry*](https://doi.org/10.1007/978-3-662-03718-8): Section 2.8 for semialgebraic dimension/cell consequences, Theorem 2.2.1 for projection/Tarski–Seidenberg, and Proposition 2.8.2 for Zariski-closure dimension. The article also spells out the finite-cover consequence and supplies the rank/stratification argument it needs. | **PASS** |

### Note on the Englander v4 source text

The v4 JATS paragraph immediately after Theorem 2.11 contains obvious sign/inequality typographical corruption (literal equality symbols where the theorem statement and the following case analysis require inequalities). This is in the external preprint's converted source, not in this submission. It does not create a gap here: the external theorem statement and subsequent cases are unambiguous, and `main.tex` lines 432–462 independently derive the exact K2P identities and signs before invoking the theorem-level consequence. No submission remedy is required.

## Scope audit

The scientific scope is consistently bounded in the abstract, theorem statements, proofs, and final status section:

| Boundary | Where the article says it | Assessment |
|---|---|---|
| Principal physical K2P component only | lines 84–110, 336–346, 1803–1807 | `D_plus` is explicit; mixed-sign components are excluded. **PASS** |
| Strict stochastic interior only | lines 315–318, 345–346, 1587–1588, 1803–1806 | No zero/one inheritance, boundary, or singular-edge theorem is implied. **PASS** |
| Binary, standard semi-directed, strongly tree-child, level at most two | lines 81–110, 202–299, 1332–1345, 1803–1806 | Definitions and admissible-rooting convention are explicit. **PASS** |
| Ordinary-triangle structural quotient, not equality of complete stochastic images | lines 289–299 and 1535–1538 | The distinction is stated twice. **PASS** |
| Regular source-relative analytic germs, not arbitrary complex-variety inclusion | lines 163–170 and the observational-relation definitions; reiterated at 1806–1809 | No silent promotion to pointwise full-image containment. **PASS** |
| Generic topology recovery, not pointwise parameter identifiability | lines 1382–1478 | Exceptional sets and bridge-incidence gauges are explicit. **PASS** |
| Exact-oracle reconstruction, not bit complexity or numerical stability | lines 1488–1493, 1522–1532 | Exact field/sign/QE assumptions and exclusions are explicit. **PASS** |
| Strict continuous-time cone only | lines 1540–1588 | Boundary `g=s^2` and other boundary cases are expressly excluded. **PASS** |
| Weak class: only a sharpness family, not weak-class classification | lines 1590–1799, especially 1797–1799 | The article says it does not claim every weak network is ambiguous. **PASS** |
| No noisy-data, conditioning, finite-sample, or model-selection theorem | lines 1803–1809 | Explicitly excluded. **PASS** |
| Computer-assisted finite residue remains load-bearing | lines 194–200 and 1811–1820 | The article does not disguise replay as an independent human proof. **PASS** |

I found no wording that claims mixed-sign, stochastic-boundary, singular-edge, higher-level, general weak-class identifiability, numerical stability, bit complexity, or finite-sample inference.

## Fresh novelty/search evidence

I searched primary-index records on 2026-08-27/28 with combinations of “K2P,” “Kimura two-parameter,” “level-2,” “strongly tree-child,” “directed containment,” and “phylogenetic network identifiability.” The most relevant results were:

1. [Englander et al. v4](https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4): K2P only for the displayed-quartet/tree-of-blobs layer; its central level-2 classification is JC.
2. [Brits et al. v3](https://arxiv.org/abs/2607.12919v3): full K2P classification at level one, not level two.
3. [Ardiyansyah v1](https://arxiv.org/abs/2104.12479v1): restricted invariant distinguishability for nice simple/semisimple level-2 networks, not this all-strong-class physical-germ containment theorem.
4. [Holtgrefe et al. 2025](https://doi.org/10.1007/s11538-025-01549-4): model-independent displayed-quartet canonical recovery for outer-labeled planar galled level-2 networks, not K2P stochastic containment.
5. [Kriebel JC v1.1.7](https://doi.org/10.5281/zenodo.22089373): the closely parallel theorem for JC, transparently cited as a companion.

An arXiv title/abstract search for `phylogenetic level-2 K2P` returned only Brits et al., whose K2P result is level one. A Crossref title query for `K2P level-2 phylogenetic network identifiability` returned Englander et al. as the only directly relevant phylogenetic-network record near the top; its title and theorem scope are JC for the central level-2 result. I located no independent earlier paper asserting the same all-strongly-tree-child level-2 K2P physical-germ containment classification, reconstruction theorem, continuous-time transfer, or `4n-3` weak sharpness family.

This is **search evidence, not a priority guarantee**: indexing can lag, unpublished manuscripts may exist, and phrase-based searches cannot prove nonexistence. The article appropriately avoids an absolute “first-ever” priority sentence.

## Findings and required action

1. **No theorem-fatal, proof-blocking, computational-completeness-blocking, or reproducibility-blocking literature finding.**
2. **No unsupported load-bearing attribution.** The most important imported claims—Huber's two generators and Englander's quartet/tree-of-blobs separation—match the cited primary sources and are also substantially rederived or specialized in the article.
3. **No material scope inflation.** The exclusions requested by the referee protocol are either stated in the theorem domains or explicitly listed in the status section.
4. **Required action: none for scientific attribution or scope.** Optional editorial action only: preserve exact source-version labels for Brits v3 and Englander v4 through submission, because both are recent and version-sensitive.

