# Source and literature audit

Initial audit checked on 30 September 2026 (UTC); source verification supplemented on 1 October 2026 (UTC). Historical retrieval limitations are distinguished below.

## First requested source and original statement

The first external retrieval attempted was [UnsolvedMath problem 30002867](https://www.unsolvedmath.com/problems/30002867). Both web retrieval and a direct request failed; the latter returned a short `Forbidden` response. No statement was inferred from that failure. The pinned dataset record was then read from the campaign's manifest-verified cache.

The complete relevant original contribution was checked in the [official Oberwolfach PDF](https://ems.press/content/serial-article-files/46567), printed pages 1182–1184, PDF pages 44–46. The central page is printed p. 1183 (zero-based PDF page 44): equation (1), Definition 5, and Problem 2. The source defines a complete intersection by generation by d polynomials in d variables. The separate Hermite-projector conjecture and the special no-roots-at-infinity theorem supply context; neither is an extra part of this record's target.

## Prior attempts and duplicate records

- Read repository `AGENTS.md`, `unsolved_math_prioritization/AGENTS.md`, `README.md`, `QUEUE.md`, `policy.json`, the selected short review, and `review_v2/related_target_groups.json` through the connected read-only GitHub API.
- The base main commit was `01358d66fc67d1c462bddf31c0d4ee5b120e6737`. QUEUE.md listed rank 28, status queued, 0/5 substantive attempts.
- `state.json` was empty. Searches for problem 30002867 in all-state PRs, commits, and branches returned no matches. Code search returned queue/shortlist/review entries, not an attempt.
- The corresponding searches for 30002868 also found no prior PR, branch, or commit. All-state PR search for “complete intersection” returned no matches.
- The manifest-verified `research_results.json` contains no report keyed by `OWR-13678-008` or `OWR-13678-009` and no OWR report keys at all. There is therefore no earlier detailed upstream proof report for this target to audit in that pinned file. The desk-review suggestion is only a planning hypothesis.
- Record 30002868 is an explicitly identified duplicate extraction of the same question. Its presence is preserved in `source_records.json`; it is not a second research attempt or independent discovery.
- `related_target_groups.json` did not list this pair. That shared file was not modified; the duplicate is explicitly documented here.

This supports treating 30002867 as previously unattempted in the checked project record. It is not a guarantee that unpublished or unindexed attempts do not exist elsewhere.

## Relevant literature and precise role

1. **Shekhtman (OWR 2015/21), pp. 1182–1184:** original source and exact global affine definition. [Official PDF](https://ems.press/content/serial-article-files/46567)
2. **Shekhtman, Some tidbits on ideal projectors, commuting matrices and their applications, ETNA 36 (2009), 17–26:** cyclicity of multiplication tuples and their relation to ideal projectors; not a general CI test. The author-uploaded article text was inspected, notably formula (1.3) and Proposition 4.2. [Author-uploaded text](https://www.researchgate.net/publication/253145781_Some_tidbits_on_ideal_projectors_commuting_matrices_and_their_applications). The dataset's EuDML link and a publisher-mirror request were unavailable.
3. **Mohan Kumar (1978), Theorem 5:** the valid stable-range efficient-generation theorem required to turn local counts into global generation. [Original publisher metadata](https://link.springer.com/article/10.1007/BF01390276). The initial publisher route did not provide the full original article. The present primary-source audit recovered the institutional GDZ scan and directly viewed Theorem 5 and its proof on printed pp.234–235. It permits a field or PID base, with the inclusive stable-range inequality; the candidate uses its field specialization. [Original article](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0046/LOG_0020.pdf).
4. **Das, On two conjectures of Murthy, Theorem 1.2, p. 1; reference [23]:** explicitly states that μ(I/I²)≥dim(R/I)+2 implies μ(I)=μ(I/I²) for ideals in polynomial rings over a field. The reproducible reference is arXiv:1710.04281v4, submitted 14 December 2017. The checked PDF internally reads November 11, 2021, from a current-date TeX command; this is a compilation date, not a version or theorem revision date. In the present zero-dimensional case, d≥2 guarantees the bound. [Versioned author preprint](https://arxiv.org/pdf/1710.04281v4)
5. **Kreuzer–Long–Robbiano, Algorithms for checking zero-dimensional complete intersections, J. Commut. Algebra 14 (2022), 61–76:** Section 3 gives Wiebe/Fitting-ideal tests for local complete intersection, including Proposition 3.2, Proposition 3.3, and Algorithm 3.4; Sections 4–5 address strict complete intersection and border bases. This supplies substantial prior art for effective characterization. The full relevant sections of the author preprint were read. [Author preprint](https://arxiv.org/pdf/1903.09563), [journal DOI](https://doi.org/10.1216/jca.2022.14.61)
6. **Bertone–Cioffi–Orth–Seiler, Cohen-Macaulay, Gorenstein and complete intersection conditions by marked bases:** recent primary-source check. Section 6, beginning p. 21 of the author PDF, describes linear-algebra minimization for homogeneous Artinian marked bases and strict/projective CI loci. It is close methodological prior art, though not the identical full-matrix spectral formula here. [Author PDF](https://www.mathematik.uni-kassel.de/~seiler/Papers/PDF/Loci.pdf)

## Errata checked and avoided

A search initially exposed the 2016 statements of a much stronger general solution of Murthy's conjecture. These must not be used without the corrections:

- Jean Fasel's [2017 official erratum](https://annals.math.princeton.edu/2017/186-2/p07) explains that the proof in the 2016 article no longer holds
- Satya Mandal's [2018 official erratum](https://www.sciencedirect.com/science/article/pii/S0021869317305392) identifies related inconsistencies

The candidate uses neither broad claim. The older stable-range theorem, explicitly retained in Das's later account, suffices.

## Current priority conclusion

Two independently initiated extensive priority families establish earlier methods sufficient for the original matrix-input/global-affine characterization. One route combines the matrix-to-ideal reconstruction of Abbott–Kreuzer–Robbiano (2005), the local CI algorithm of Kreuzer–Long–Robbiano (2019 preprint/2022 journal), and Mohan Kumar's verified 1978 global theorem. A second direct matrix-algebra route uses Wiebe's original 1969 Satz 3, p.260, through a coefficient-kernel presentation of the maximal ideal and its zeroth Fitting ideal, then Mohan Kumar's Theorem 4, p.234. Recovering the generated faithful algebra requires no supplied coordinates for the unit. Nilpotents, multiple support points and the fixed regular representation are preserved.

This is a checkable composition deduction from published primary results, not an assertion that these sources announced a resolution of the named 2015 problem. No prior identical D_2 formula was located in the bounded search. That absence does not clear a first-resolution or novel-theorem claim. Current classification is **already_solved by equivalent prior methods**, with the correct rank presentation retained as a credited partial research outcome. No paper is appropriate. Full details and access limits appear in [PRIORITY.md](PRIORITY.md) and the independently authored audit-family reports.

## Current audit reconciliation

The exact target, original 1978 Theorem 5/proof dependencies, scoped errata and pinned duplicate pass independent source review. Full homological/global proof and exact computational families pass. The source and attribution wording is repaired; a fresh complete acceptance adversary remains pending. Original snapshot, turn evidence, and reviews remain immutable. The dated dataset's `open` status is preserved as source provenance, not asserted as current.
