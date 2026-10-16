# PR885 / PID9700042: independent recent/direct-model priority audit

Audit date: 15 October 2026. The target is exclusively the Aldous–Lenderman oriented Bernoulli **edge-capacity** flow conjecture, with shared vertices permitted and fixed-p n→∞ followed by p↑1. No other problem or PR is assessed here.

## Principal finding

This audit found a substantive prior-estimate route to the **entire exact asymptotic**, not merely a paper with the same coefficient. BGT's 2021 weighted-list estimate, equation (33) and the subsequent displayed W bound in Section 3.3, suffices after a precise open-site construction and deterministic path comparison. The complete deduction is in [OLD_ESTIMATE_COROLLARY.md](OLD_ESTIMATE_COROLLARY.md). Its conclusion is

    1−v(1−q) ~ √(2q).

This is a deduction authored during this audit from older primary estimates. An explicit earlier published statement claiming to resolve this particular flow conjecture was **not located**. Those are different priority facts. The proposed C4 solution should not be framed as establishing firstness or as introducing the general rare-defect/Poisson or BK decomposition mechanism without addressing this deduction. The parent was asked to check the complete deduction independently before promoting a priority verdict. This report does not alter any shared classification.

The decisive source is Anne-Laure Basdevant, Jean-Baptiste Gouéré and Marie Théret, [*First-order behavior of the time constant in Bernoulli first-passage percolation*](https://arxiv.org/abs/2106.12266), submitted 23 June 2021; the authors' bibliographies identify its journal version as AAP 32(6) (2022), 4535–4567, [DOI 10.1214/22-AAP1795](https://doi.org/10.1214/22-AAP1795). The 2021 primary PDF, including its relevant statements and counting estimate, was retrieved and inspected.

## Why the strong conclusion is checkable

The naive argument is invalid: ordinary undirected Bernoulli FPP charges positive backward traversals, whereas the exact cut dual charges zero. In a common field their defects are respectively k_forward+k_backward−2b and k_forward−b. [FINITE_MODEL_DISTINCTION.json](FINITE_MODEL_DISTINCTION.json) gives a Q_2 witness with costs 2 and 1 respectively. Equal asymptotic coefficients in the two models are insufficient evidence by themselves.

The stronger deduction avoids that identification. At each dual vertex declare a site open if either outgoing E/N edge is marked; these are independent site events with r=2q−q². Write S_r for BGT's strict open-site chain score. The following verified steps close the model gap:

1. Every strict open-site chain can choose one marked outgoing edge per site and embed into a monotone dual path. Thus D_N≥S_r(N) pathwise.
2. For the upper bound, set the auxiliary endpoint to (N+1,N+1), so every confined path vertex is strictly below it. Apply BGT's exact monotone-subsequence notation to all visited open starting sites. At most one collected marked forward edge starts at each such site.
3. Local optimality of the actual nonnegative-cost dual path bounds a nonlast segment's backward steps by its number of intervening open sites. Strict endpoint separation permits the comparison path to take a marked first edge. Cycle removal makes replacement valid even when paths intersect elsewhere. The final segment uses the auxiliary terminal and a purely geometric boundary inequality.
4. Let G be the absolute variation in each gap's distinguished coordinate and H the **sum of individual negative increments** in its other coordinate. Actual backward variation obeys b≥G/2+H. A defect exceeding S_r(N+1)+ηN√q therefore yields precisely the m=0 admissible weighted-list inequalities of BGT's (33), with a fixed rescaling of η. The m=0 specialization imposes no absence of doubly-open sites; it uses only the weight r^p for p distinct open sites.
5. The printed W bound specializes to a summable geometric series. Its fixed-r bad-event probability tends to zero as N→∞. Boundedness of D_N then permits passage to expectations. BGT's already proved score scaling σ_r~2√r and the source-premised flow-density limit yield the exact ordered-limit conclusion.

No new interchange-of-limits lemma is assumed in that chain. The only substantial old inputs used by this deduction are the BGT strict-site score limit/scaling and its displayed weighted-list estimate. The finite directed-cut identity and original fixed-p limiting density remain the exact target contract supplied to this audit. [CLAIM_MAP.json](CLAIM_MAP.json) records each dependency and the previously blocked shortcut.

A standalone checker [verify_corollary_geometry.py](verify_corollary_geometry.py) tests the deterministic event inclusion and chain comparison on all 4,096 Q_2 edge fields, plus 1,440 fixed-seed extended fields on Q_3,Q_4,Q_6. All 5,536 pass; 372 selected minimizing paths use backward steps. [GEOMETRY_CHECKS.json](GEOMETRY_CHECKS.json) records the run. These are sanity checks; the infinite-volume argument is the written derivation and old estimate.

## Material prior mechanisms and attribution

| Source | Inspected contribution | Exact relation to C4 / target |
|---|---|---|
| Aldous–Lenderman problem page | Exact model, conjecture, 2004 history, interchange caveat | Source of the target. Continued online presence is not evidence of current openness. |
| Aldous, [June 2005 Ottawa talk](https://www.stat.berkeley.edu/~aldous/Talks/Ottawa.pdf), pp.18–19 | Rare marked edges, Poisson rescaling, Hammersley connection, unresolved interchange | The broad limiting heuristic predates C4 by two decades. The slides use a different flow normalization, so they are not used for the coefficient. |
| BGT 2021, Sections 2.2–2.5 and 3.3 | Strict-site score scaling and explicit detour-list enumeration | Supplies the substantive old estimates for the complete deduction above. The ordinary FPP theorem alone would not. |
| Julien Verges, [arXiv:2503.01484v1](https://arxiv.org/abs/2503.01484), Lemma 2.5 and Section 5.2 | BK product-tail bound for decompositions without a disjoint-region hypothesis; endpoint/length skeleton application | Independently establishes substantial method overlap with C4's overlapping-rectangle/disjoint-witness strategy. It is not by itself an exact lattice-flow theorem. |
| BGT, [arXiv:2402.07509v2](https://arxiv.org/abs/2402.07509), introduction and reward-model definitions | Rare inhomogeneities in continuous norm-based passage models | Relevant descendant and conceptual overlap; its continuum model is not identified with the lattice dual here. |

Verges's PDF is dated 4 March 2025; arXiv records submission on 3 March 2025. Its generated HTML displayed a 24 August 2026 heading, so the report uses the original PDF and arXiv history for chronology. The primary Lemma 2.5 statement and proof on PDF pp.10–11 were visually inspected. The lemma allocates the collected Poisson mass among components and uses disjoint occurrence, rather than treating overlapping regions as independent. C4's ratio-fixed lattice skeleton and bad-backtracking budget remain specialized constructions; this audit does not claim that Verges printed those exact constructions.

The Poisson-chain constant and large-deviation input, and BK itself, are older classical ingredients. Their existence never implied that the exact flow conjecture was already settled. The new priority issue is the complete BGT intermediate-estimate deduction, whose actual missing model bridge has now been supplied explicitly in the companion note.

## Coverage of recent and direct-model leads

The independent plan was frozen before any inherited priority report was read; none was subsequently read. [SEARCH_LOG.json](SEARCH_LOG.json) contains 80 exact queries in 26 batches, all on 15 October 2026. Searches covered names, exact page/title/URL, model variants, q=1−p, near-one and square-root formulas, Bernoulli time constants, Poisson/backtracking language, high-density flow, French variants, and 2025/2026 author and preprint leads. Search snippets were used as discovery aids only.

Direct primary trails inspected include the problem page and Aldous's related flow page/talk; Basdevant, Gouéré, Théret and Gerin publication lists; later BGT continuous FPP work; Verges's bibliography and recent greedy-path papers; and the March 2026 Point Processes and their Applications conference abstract. The latter explicitly concerns continuous Boolean FPP. Recent directed-FPP leads were checked at their model definitions: McKeown's 2025 strict-weak model allows only NE paths and has deterministic zero vertical weights; Hassler's 2024/2025 model gives vertical edges deterministic weight one. They are not silently equated with this cut dual. The 2025 atom-distribution Hammersley preprint was screened at its primary abstract/history only. A high-density oriented-percolation lead was likewise screened at its arXiv abstract/history; its latest version is withdrawn and was not used as technical evidence.

A metadata-only OpenAlex forward-citation query returned two entries for BGT at query time. One primary citing article's relevant discussion was inspected: Dembin–Elboim–Peled's 2024 coalescence paper cites BGT for rare-zero-edge limit-shape behavior, not for the exact flow problem. The other citing work was not available as a usable primary body in this audit and remains an explicit coverage gap. Semantic Scholar's citation endpoint returned HTTP 429. These services do not provide a complete citation census.

## Corrections, validation and limits

The parent independently caught a source-reading error in the first draft: H was initially defined as the negative part of a net increment rather than the sum of individual negative parts printed in BGT. The stronger quantity is bounded by actual backward variation interval by interval. The derivation and checker were corrected, rerun, and the change logged. This correction matters for the literal match to (33); the final note uses the correct form throughout.

This audit did not obtain a usable publisher body through the BGT DOI (HTTP 200 returned a challenge page), so it does not claim a line-by-line journal-version comparison. The earlier 2021 primary preprint suffices for the positive prior-estimate finding. No unpublished Lenderman manuscript or independent historical flow proof was recovered. Later sources were inspected to the exact scopes listed in [SOURCE_LEDGER.json](SOURCE_LEDGER.json); several were screened only at definitions or abstracts, rather than through every proof.

No finite web search can certify exhaustive absence, universal firstness, or current openness. The frozen 7 October 2026 author date is also not a first-publication certificate. This report offers positive, checkable old-source evidence and a complete deduction, while leaving the historical fact of first explicit recognition of the corollary undetermined. It does not claim formal verification, a full plagiarism or all-method novelty assessment, or independent revalidation of the whole C4 proof.

All writes were confined to this audit's dedicated folder. No individual was contacted; no outreach was prepared. No Git, branch, PR, publishing, release, DOI or spreadsheet mutation was performed. Raw primary bodies and renders are excluded from the explicit authored-file public manifest; only this audit's own inspected renders were removed.
