# PR570 / problem 30006605: independent historical-priority audit

Audit date: 2026-10-14 America/Los_Angeles. Source-first checkpoint: 2026-10-15T04:23:51.202450Z, before candidate access. This is a new source-based audit; no historical or sibling assessment was consulted. Only this audit directory was written, and no Git/index/canonical/original mutation or external outreach occurred.

## Disposition

**No explicit earlier full-target resolution was found in the inspected primary literature. Historical firstness remains unestablished.** The frozen candidate is best described as a short threshold transformation and an exact all-dimension consequence of credited prior algorithms. On this evidence, it should neither be rejected as an already explicitly recorded solution nor advertised as historically first. The candidate already makes these distinctions; this audit identifies no priority-blocking correction.

The important distinction is between a result that follows from existing tools and a result explicitly recorded in an earlier source. The independently saved source-first deduction already yields the candidate's O(n log^5 n) conclusion from BDH's additive eccentricity algorithm and Ducoffe's generic optimization reduction. That observation limits the amount of new algorithmic machinery here. It does not establish that either earlier paper states the complete multiplicative median-graph solution.

## Exact target and strongest supported claim

I read Ducoffe's entire *Radius functions in median graphs* contribution, pp.504-507 of [OWR8/2026](https://doi.org/10.4171/OWR/2026/8), and visually inspected all four source pages. Open problem1 is on p.505; the multiplicative profile definition is on p.504. The finite algorithmic target is a nonempty explicit promised median adjacency graph with unit edges and arbitrary finite nonnegative real vertex weights. The output is a vertex minimizing max_u w(u)d(c,u), in almost-linear time for fixed cube dimension. Returning the optimum and all centers, with no dimension restriction, is a stronger finite result. Infinite encodings, continuous facilities and arbitrary edge lengths are separate questions.

The candidate's theorem matches this target. Its imported additive oracle takes bounded nonnegative integers, so arbitrary real arithmetic does not enter that oracle. Comparing bounded integer multiples of input weights suffices for the rest. No recognition, embedding or pairwise-distance table is required by the stated mathematical algorithm.

## Primary-source comparison

| Prior source | Exact verified statement and locator | Collision assessment |
| --- | --- | --- |
| [Berge-Ducoffe-Habib, arXiv:2410.10235v1](https://arxiv.org/abs/2410.10235v1), 2024-10-14; [SODA2025 DOI](https://doi.org/10.1137/1.9781611978322.52), published2025-01-07 | arXiv p.2 defines max_v(d(u,v)+omega(v)); p.3 Theorem1 gives O(n log^4 n); p.6 specifies nonnegative integer weights. p.4 expressly distinguishes the multiplicative center question and treats it as future work. Algorithm1 p.22; complexity proof pp.23-24. | Exact imported component. The primary full arXiv version does not explicitly solve multiplicative centers. Publisher metadata confirms conference identity, but the publisher PDF was unavailable; no full-version identity assumption is made. |
| [Ducoffe, ESA2026](https://doi.org/10.4230/LIPIcs.ESA.2026.133), published2026-08-25; [arXiv:2607.04287v1](https://arxiv.org/abs/2607.04287v1), submitted2026-07-05 | ESA p.133:6 Lemma2; full version pp.5-6 Lemma2.2: generic exact weighted-center optimization from a witness-producing threshold oracle in O((T+n)log n). Uses weighted medians of implicit candidate-row midpoints. | Explicitly prior optimization mechanism. Its concrete algorithms concern hyperbolicity and other named graph families. It does not state the general finite median-graph or general bounded-cube-dimension multiplicative conclusion. |
| [Chalopin-Chepoi-Dragan-Ducoffe-Vaxes, arXiv:2503.15011v1](https://arxiv.org/abs/2503.15011v1), 2025-03-19 | Section2.3 defines nonnegative real multiplicative profiles; TheoremE p.5 / Theorem7.8 p.28 gives O(n log^2 n) exact center for cube-free median graphs. | Explicitly prior dimension<=2 special case, already acknowledged by OWR. Does not settle bounded cube dimension generally. |
| [Berge-Habib, arXiv:2105.12150v1](https://arxiv.org/abs/2105.12150v1), 2021-05-25 | O(2^{O(d log d)}n) all unweighted eccentricities for cube-dimension d; unit-edge definitions and Sections4-5 algorithms. | Prior fixed-dimension unweighted result. Internal weighted-set labels do not equal multiplicative demand weights. |
| [Ducoffe, MFCS2021](https://doi.org/10.4230/LIPIcs.MFCS.2021.43), 2021-08-18 | Theorem1 pp.43:4-43:5 assumes a supplied embedding into a bounded number of trees; Theorem5 pp.43:7-43:8 is its range-query framework. Theorem10 addresses the absolute center of cube-free median graphs. | Related embedding/continuous-center mechanisms, not the general exact target. OWR p.505 attributes a weighted-center extension to the bounded-tree-dimension line of work; the inspected conference text itself does not state that multiplicative theorem. |

A source-first exact scope table is preserved in SOURCE_FIRST_CHECKPOINT.md. Its mistaken full-version lemma number is corrected transparently in SOURCE_FIRST_CORRECTIONS.md: the optimization lemma is 2.2, not 2.1. This was my locator error, not a candidate error.

## Claim-by-claim candidate comparison

Only the frozen original bundle's PROOF.md was opened after the source-first checkpoint. Its SHA256 is recorded in SOURCE_LEDGER.json.

| Candidate locator | Assessment |
| --- | --- |
| lines3,108: no historical-priority claim; prior components not novel | Appropriate. Retain this qualification. No source evidence here supports stronger firstness language. |
| lines7-15: exact multiplicative finite unit-edge target; O(n log^5(2n)) all dimensions | Matches the source question and is stronger in dimension scope. This does not assert an edge-weighted or infinite-encoding result. |
| lines21-27: additive BDH oracle | Correct domain/interface: all additive eccentricities for nonnegative integer weights. Candidate uses only 0,...,n-1. |
| line29: credit to D26 optimization lemma | Necessary and already present. It is an actual prior generic component, not just a similar theme. Candidate's sorting/bounded-search variant has weaker overhead but the same final bound. |
| lines33-55: clipped threshold transformation | Independently recovered before reading candidate. For D=n-1 and b_R(u)=max{k in [0,D]:kw(u)<=R}, a_R(u)=D-b_R(u) is a legal BDH input and r_w(x)<=R iff max_u(d(x,u)+a_R(u))<=D. Zero weights and R=0 are handled. This is a pointwise decision identity, not equality of additive and multiplicative objectives. |
| lines61-94: implicit candidate search | Its weighted-median pruning is credited prior machinery. The displayed strict-pruning/incumbent invariant handles duplicated values and zero rows. It does not enumerate the quadratic set. No historical novelty should attach to this mechanism. |
| line98: composition and all centers | The O(log n) calls to the O(n log^4 n) additive oracle produce O(n log^5 n). The final call at the optimum returns every minimizing vertex. Read-time is included by median sparsity. |
| lines102-108: exact real comparison model and limitations | Adequate scope distinction. Bit-cost independence is not claimed; quadratic controls do not validate the fast oracle's implementation. |

The strongest mathematically supported result of this priority audit is the exact reduction/composition under the cited BDH theorem. It is not a new implementation of BDH, a re-proof of that theorem, or a historical-novelty certificate.

## Adversarial controls and misleading comparisons ruled out

The independently authored controls.py imports no candidate code. Running it passed 143,170 threshold checks and 10,004 optimization cases over every connected labelled graph through four vertices (44 graphs, including 24 median graphs), with exact rational weights. All pointwise feasible sets, optimum values and complete center sets matched exhaustive distances; every pruning iteration met the asserted 3/4 mass bound. Additional controls covered 257-bit rational data. CONTROL_RESULTS.json records counts and the script hash. These checks support the finite transformation and search; they do not establish historical priority or the imported oracle's asymptotic implementation.

Several apparent priority collisions fail at exact scope:

- On the path0-1-2-3-4-5 with weights(1,0,0,0,0,3), multiplicative centers are {4}; raw additive centers are {3,4}. Calling the 2025 result itself a multiplicative solution confuses objectives.
- Four radius-one balls on C4 are pairwise intersecting but have empty total intersection. General median graphs cannot be silently treated as Helly graphs for ordinary graph balls.
- P_(L+1) x P_(L+1) has cube dimension2 while its four corners force hyperbolicity at least L. Taking its product with K2 gives the same obstruction at dimension3. Thus the 2026 bounded-hyperbolicity algorithms cannot be promoted to a bound depending only on cube dimension.
- Bounded tree dimension and a supplied tree-product embedding are stronger hypotheses than bounded cube dimension. The OWR source itself warns that tree dimension is unbounded at cube dimension2.
- Unimodality and local-search questions are distinct from the threshold decision reduction. A failure of a local-search route would not refute this global composition, and does not supply an earlier exact-target solution.

## Search coverage, remaining limits and actionable issues

SEARCH_LEDGER.json preserves 33 exact queries in nine batches, local audit date/timezone, forward-search subjects, exclusions and access limits. The search included multiplicative/weighted centers, ball intersections, additive-versus-multiplicative terminology, the two principal arXiv IDs, post2025/current2026 queries, and primary-domain searches. Current author bibliographies and source references were also inspected. Relevant full primary PDFs were obtained independently in the ignored .cache and hashed in SOURCE_LEDGER.json. The OWR DOI resolver and SODA full-PDF browser route returned Internal Error; those routes were not retried or bypassed. No outside person was contacted or asked for input.

Search absence is not proof of absence. The inaccessible full SODA proceedings chapter, incomplete citation-index coverage, recent indexing delays, and possible unindexed records prevent a historical-first conclusion. Secondary snippets, status datasets, and project-owned pages were excluded from the evidence supporting the verdict. I did not consult historical/sibling audit conclusions.

There are no mandatory priority repairs to the frozen proof. Recommended presentation improvements are minor:

1. Keep the result framed as the short threshold observation and its consequence; retain explicit prior-work and no-firstness qualifications.
2. For locator precision at candidate line27, cite Algorithm1 p.22 and Theorem1 proof pp.23-24 separately from Theorems3 and4 (which appear on pp.13 and19 and whose arguments continue beyond those pages). This is bibliographic, not a mathematical blocker.
3. Optionally cite the 2025 cube-free result directly when discussing novelty or background. A claim that arbitrary multiplicative centers were previously unknown even in dimension2 would be false; the frozen proof makes no such claim.

**Recommended disposition: priority audit passes with historical priority explicitly unresolved.** No explicit full-target collision established; no certification of novel machinery or historical firstness. Any later promotion that adds such claims needs additional evidence rather than relying on this negative search.
