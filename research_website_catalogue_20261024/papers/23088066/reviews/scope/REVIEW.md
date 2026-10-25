# Publication-scope review — 23088066

**Disposition:** no publication-scope defect identified in this bounded review. Candidate content awaits separate mathematical gates. Historical audit-opinion exposure is disclosed; this report must not count as a strictly independent mathematical gate.

## Source, edition and independence

Fresh [Zenodo 23088066](https://zenodo.org/records/23088066), concept 23088065, DOI 10.5281/zenodo.23088066. Version 1.0 and 1 October 2026 agree between metadata and printed manuscript. All published files were acquired directly, checksum-bound and safely extracted. The PDF is 75,140 bytes, SHA-256 `5325fceeed4352f74b531a033e8474ca1fabeeff0a6b6ecb54337e17dadb4dd6`; the ZIP is 120,059 bytes, SHA-256 `b1e4a1c22fc3eec24c9d8f479b48110ddf6d72052181995037de64b99d46791f`.

Read all five actual manuscript pages, including the PL construction, random obstruction, adaptive cleanup, bounds and references. Read the full 55-line `PL_SUBDIVISION_LEMMA.md`, 243-line `probability_derivation.md` and original exact-bound code. The abstract, edition and theorem were visually inspected and cross-checked with `paper.tex`. No checker execution is claimed by this reviewer.

**Independence exception:** despite its derivation filename, `probability_derivation.md` is a historical independent probability audit and includes a PASS assessment. Reading the relevant support exposed that assessment before the own 60% conclusion. The PL supplement also contains a historical AI-review status sentence. Exposure was promptly disclosed to root. These assessments were not used as validation; strict archived-opinion exclusion nevertheless cannot be claimed. No current sibling mathematical findings or dedicated additional archived priority/audit reports were consulted.

`source_integrity.json` verifies both assets against live-record MD5, size and receipt SHA-256, ZIP CRC and all 41 manifest entries against archive and extracted bytes. No internal PDF or nested ZIP is present. There is no omitted reader supplement.

## Exact claim and contribution

The theorem concerns a **finite general two-dimensional simplicial complex**, without a manifold or surface hypothesis. Its least PL embedding dimension is three and its least dimension for a map affine on every original simplex is five. The first barycentric subdivision embeds linearly in R³. The abstract subdivision vertices may be assigned freely; they are not prescribed arithmetic barycenters of original vertex images.

This exact pair addresses Brehm's minimum-dimension question. PL embeddability without linear embeddability in one **fixed ambient space** does not automatically establish the pair (3,5). The paper credits Brehm–Sarkaria for fixed-ambient separation, Newman for the balanced-Radon/order-type/probability mechanism and Lee–Nevo for PL hypergraph embeddability. It does not originate those ingredients.

The added step is an obstruction uniform over **every** deletion set of size at most m. Independent variables select whole triangles. Distinct crossing-pair indicators depend only when they share a whole triangle, with joint probability p³. A Janson bound, unioned over order types and all small deletion sets, permits cleanup after observing the random sample. A fixed-deletion estimate alone would be insufficient.

Deleting one triangle per edge-sharing pair leaves a linear triangle family, meaning facets meet in at most one vertex. The obstruction survives, excluding R⁴ linear embeddings, including nongeneric ones by perturbation. The six-triangle fan construction embeds the first subdivision in R³. More than n retained triangles yield over 3n distinct edges, forcing a nonplanar one-skeleton and PL minimum at least three. A five-dimensional moment-curve placement supplies the original-linear upper bound.

The finite parameters n=2²⁵⁶, p=2⁻³⁸⁴, m=2³²⁰ establish finite existence with exact inequalities. They do **not** generate a facet list, practical small model or efficient construction algorithm. The universal probability and geometry arguments are not certified by finite numerical samples. No larger-gap, manifold-restricted, optimal-size or odd-dimensional threshold theorem is claimed.

## Direct primary-literature comparison

Primary PDFs were freshly acquired with URL/hash/page receipts in `primary-sources/`; caches are locally ignored. Past archived priority verdicts were not adopted.

- [Brehm, Oberwolfach Report 12/2006](https://ems.press/content/serial-article-files/46044): read the complete contribution, printed pp. 701–702 / PDF pp. 49–50. Its open problem asks whether the **minimum** dimensions can differ by more than one, specifically mentioning dimensions two and three. No manifold restriction is imposed. Theorem 2 gives earlier fixed-ambient separation.
- [Brehm–Sarkaria, MPI/92-52](https://archive.mpim-bonn.mpg.de/id/eprint/1946/1/preprint_1992_52.pdf): read definitions, Theorems A/B and introductory mechanism. A gives separation in R^(2n) after any prescribed number of subdivisions; B treats a manifold with boundary in R^(2n−1). Those statements do not alone supply (3,5). No full verification of all fourteen predecessor pages is claimed.
- [Newman, arXiv 2212.09576v3](https://arxiv.org/abs/2212.09576v3): read introduction/main theorem, Section 4's balanced-Radon, order-type and Janson statements, the dense-side conclusion and Section 5. Theorem 16 gives an even-dimensional separation. Section 5 explicitly withdraws an earlier odd-dimensional threshold claim; the target uses the retained R⁴ mechanism and adds the deletion-set union.
- [Lee–Nevo v3](https://arxiv.org/abs/2307.14195v3): read Lemma 3.1 and its full proof. It concerns linear (d+1)-uniform hypergraphs in Rᵈ for d≥3. The triangle consequence follows by adding a private vertex to each facet, applying d=3 to a linear 4-uniform hypergraph and restricting. The target also supplies a direct first-subdivision construction. The same lemma statement was checked in [July 2023 v1](https://arxiv.org/abs/2307.14195v1), so the later journal date does not determine priority of this mechanism.
- [Goodman–Pollack, DCG 1 (1986)](https://doi.org/10.1007/BF02187696): read Theorem 1 on printed p. 220, its simple-numbered-configuration definition and proof framework. The finite bound n^{d(d+1)n} gives n^{20n} here. This is not an unspecified asymptotic constant.
- [Frieze–Karoński, Introduction to Random Graphs](https://www.math.cmu.edu/~af1p/BOOK.pdf): acquired the current 854-page book and read Section 34.6, printed pp. 712–714, Theorem 34.13 and proof. The denominator's ordered dependencies and diagonal are confirmed by the proof's sum_i E(Y_i I_i). Taking t=μ gives the conservative target bound. The original Janson 1990 body was not acquired directly; the author-hosted book supplies the inspected theorem and proof.

A bounded current search did not supply a separately inspected theorem already asserting (3,5). This is not exhaustive first-priority certification. The validity of the new estimate, PL geometry and exact minima remains for the independent mathematical gates, regardless of the archived support assessments.

## Candidate content and completion

`content.json` preserves the full original abstract and keeps AI/status separate. It explains both embedding rules, exact minima, prior credit, the adaptive-deletion step and missing explicit facet list. It includes concise mechanism and a professional collaboration invitation without an authorship promise, outreach or dated internal verification replay. Original filenames remain intact; `additional_assets` is empty.

`follow_up` is null. Smaller explicit witnesses, manifold variants and larger gaps are natural, but no fresh construction or unusually supported conjecture is established here.

**Completion:** source-bound scope/content work 100%; not a strictly independent mathematical gate. No repairs or website, spreadsheet, Git, Zenodo or outreach changes.
