# Source and prior-attempt gate: 30003472

Checked 2026-10-02 UTC. Target code OWR-15427-014, queue rank 321 at allocation.

## Exact source and interpretation

The requested [UnsolvedMath page](https://www.unsolvedmath.com/problems/30003472) could not be retrieved. The approved immutable dataset fallback was inspected, including the complete record and available report entry. Its substantive source is Xavier Goaoc's question in [Discrete Geometry, Oberwolfach Report 19/2017](https://ems.press/content/serial-article-files/46683), printed p.1198, item 6; [official article and DOI](https://ems.press/journals/owr/articles/15427). The workshop was in April 2017; the report was published in 2018. The PDF page was downloaded, rendered, and visually inspected.

The source prints an absolute constant `c>0`, the power `c^n`, and the quantifiers “for every μ, there exist two n-point order types.” It does **not** supply an explicit quantifier or lower range for n. The dataset changes the constant to `c>1`, while describing the edit as presentational. That change is mathematically substantive but captures the nontrivial exponential-gap intent. Taking `c<1` and equal types would trivialize the literal wording; demanding `c>1` for n≤3 would fail because there is just one unlabeled type. Neither observation is treated as a resolution of the intended research question.

For research we distinguish:

* **Uniform asymptotic target:** there exist absolute c>1 and N such that for every line-null planar Borel probability measure μ and every n≥N, two realizable simple unlabeled n-types have probabilities differing by a factor strictly greater than c^n.
* **Measure-dependent-threshold target:** there exists an absolute c>1 such that for every such μ there is N(μ), and the same conclusion holds for every n≥N(μ).

The first implies the second. A proof of the first would settle either reading; a proof merely in a special class, or with a measure-dependent threshold, must identify that limitation. The source alone does not distinguish the two readings. The intended constant is independent of μ. Zero-probability types are not excluded in the source. Labels are forgotten after iid sampling, and equivalence is by orientation-preserving bijection, as in the cited order-type paper.

## Pinned provenance

Dataset `ulamai/UnsolvedMath`, revision `37e53eabe540fb458758e198be61634bd02ee008`, 15,458 records. The following complete source files were verified against the repository manifest before selecting this record:

* `problems.json`: 68,931,837 bytes, SHA256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
* `research_results.json`: 80,334,822 bytes, SHA256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`

The selected problem-record export has SHA256 `9788d69e4d999b63509efe776862769df7b36bedf747df47290ebd5806394a4c`. No associated substantive upstream research report was found under this numeric ID or its problem-code lookup. The record's dated literature assessment was read as a lead, not accepted as a proof or current-status certificate.

Current imported review hash: `b872e1513c8bae1cd12eb33c25a6852dea5fb588f037da6e980e17e35dd32baa`.
Statement hash: `1bae62333545cd91005fb420f4442cea517c8967fe0eadbb1402e685fbb1e384`.

## Primary literature and limits of this check

1. Goaoc, Hubard, de Joannis de Verclos, Sereni and Volec, [Limits of Order Types](https://arxiv.org/pdf/1811.02236), inspected full-paper version dated September 8, 2021. Proposition 2 gives a factor exceeding 1.8208 at size six; Corollary 8 connects line-null measures to order-type limits. The paper also constructs singular measures with extremely small convex-position probabilities. These are useful distinctions, not a universal exponential-gap theorem. The [2015 conference version](https://drops.dagstuhl.de/storage/00lipics/lipics-vol034-socg2015/LIPIcs.SOCG.2015.300/LIPIcs.SOCG.2015.300.pdf) is the source cited by the OWR question.
2. Goaoc and Welzl, [Convex Hulls of Random Order Types](https://arxiv.org/pdf/2003.08456), 2022 version, published in JACM 70 (2023), [DOI 10.1145/3570636](https://doi.org/10.1145/3570636). Theorem 1.1 proves concentration for several standard distributions. Section 1.4 formulates broader concentration conjectures and explicitly notes the insufficiency of the fixed-size bias for concentration. Concentration in their definition and the pointwise max/min exponential gap here are different assertions; neither is silently substituted for the other.
3. Devillers, Duchon, Glisse and Goaoc, [On Order Types of Random Point Sets](https://arxiv.org/abs/1812.08525), 2020 version: experiments and coordinate-bit complexity for uniform-square sampling. Its entropy/encoding barrier does not settle the present comparison.
4. Caraballo et al., [On the Number of Order Types in Integer Grids of Small Size](https://idus.us.es/server/api/core/bitstreams/0c61b06a-f1a4-46b7-b3b1-b6e520e0dac0/content), opening lower-counting discussion; and Scheucher, [Many Order Types on Integer Grids of Polynomial Size](https://www.sciencedirect.com/science/article/abs/pii/S0925772122000670). These record the classical labeled n^(4n+O(n)) counting scale and elementary arrangement-extension mechanism. Turn 1 reproves a convenient explicit lower bound, so its quantitative conclusion does not depend on an unstated constant from these sources.

Searches through the check date for the exact title/code and combinations of Goaoc, order types, exponential probability, bias and concentration did not locate a full resolution. This is a bounded literature search, not an exhaustive novelty guarantee. Search-engine crawl dates were not treated as publication dates.

### Caution concerning a possible regularity extension

The complete proof of Lemma 3.16 in the inspected Limits of Order Types version, pp.28–29, was examined. In its area-measure argument it passes from absolute continuity to a continuous Radon–Nikodym density and then to a square with a positive lower density bound. Absolute continuity by itself does not imply continuity of that density. No intervening approximation or Lusin argument is supplied in that proof to justify this step. This is an identified unfilled inference in that presentation, **not** a counterexample to the lemma's conclusion or a claim that no repair exists. Turn 1 uses the explicit stronger area-domination hypothesis and proves its estimate directly. Extending it to arbitrary absolutely continuous measures remains a separate task.

## Repository and duplicate gate

Read the current root AGENTS.md and unsolved_math_prioritization/{AGENTS.md,README.md,QUEUE.md}, and the selected full source context. At the gate the canonical queue showed queued, 0/5. GitHub checks found:

* no branch, all-state PR, or commit matching 30003472;
* no all-state PR matching OWR-15427-014 or the target-title phrase;
* no commit history for `attempts/30003472` or `attempts/owr_15427_014`;
* code-search hits only in the assignment catalog, with no prior proof attempt.

The related-target-group file has no entry for this target. A full pinned-record search for “order type” returned IDs 2205, 2713, 7500122, 30000380, 30003472, 30003692, and 30004525. The other titles concern different combinatorial, topological, ordinal, computability, or algebraic targets; no duplicate of the present random planar-type comparison was identified. No earlier substantive author turn was recovered for this target.

**Gate decision:** eligible for a fresh five-turn attempt, with the source quantifier ambiguity recorded above. No full-solution disposition is authorized by the special case proved in Turn 1.
