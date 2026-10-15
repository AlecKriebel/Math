# Priority audit of the biconstrained symmetry candidate

Audit date: 3 October 2026 UTC. Candidate: problem 30004048, frozen TURN_3.md SHA256 cf1c7a7078a8bc29ef775fe0bf9298fe052017e25b1da363c1dd20643b1ff3b4.

**Finding:** no earlier equivalent theorem, or source theorem contradicting the candidate, was found in the bounded primary corpus checked. This supports describing the boundary formula and its asymmetry deduction as proposed contributions subject to proof review and the stated priority limits. It does not certify global novelty. The inaccessible 2019 Princeton senior thesis is a specific unresolved coverage gap.

The independent source-first conclusion was sealed at 2026-10-03T20:24:26.263151Z, before reading the candidate's analyses and prior-review notes. Afterward, all 41 frozen target files were read in full. Their source framing and matrix transcription agree with the independent reading; no mandatory attribution or source-scope correction was identified.

## Exact question and proposed contribution

The [2019 Oberwolfach question](https://ems.press/content/serial-article-files/46780), printed pp.46–47, adds both reverse degree requirements and asks whether the resulting universal function is symmetric. The detailed [joint paper](https://doi.org/10.37236/8451) uses finite simple tripartite graphs with four degree constraints. Its ψ is the infimum, over all admissible graphs, of the largest fraction of distinct A vertices reachable from a C vertex through B. Reversing one graph exchanges its degree parameters, but does not exchange its direction-specific reach maxima or establish equality of the two universal infima.

For rational 0<θ<1 the candidate claims
ψ(1−θ,θ)=1−θ/d(θ),
where d minimizes the unweighted maximum row degree of finite binary incidence matrices with distinct columns and positive rational probability vectors b,q satisfying Mq=θ1 and Mᵀb=θ1. This is a degree invariant of weighted-regular incidence patterns; it differs from the minimum matrix order studied in the joint paper.

The proposed new mechanism is boundary rigidity: a graph with no full-reach C vertex has exact regularity on B–C, and its missed A classes force an integer-degree bound. A separate finite rational construction gives the matching bound. Conditional on that proof, the credited matrix and its complement imply
|ψ(13/27,14/27)−ψ(14/27,13/27)|≥1/108.
The actual two values, their ordering, and the invariant minima are not evaluated. The displayed 162-vertex graphs give upper bounds only.

## Prior results and exact distinctions

The [published 2022 paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v29i2p47/pdf/) by Maria Chudnovsky, Patrick Hompe, Alex Scott, Paul Seymour and Sophie Spirkl is the principal authority. Definitions, the complete §§2.1–2.3, §4, §12 and the open symmetry discussion were read, together with relevant parts of §§5–6. Figure 1 on printed p.6 and the symmetry remark on p.10 were visually checked. The corresponding required sections of [arXiv v3](https://arxiv.org/pdf/1902.10878v3) were also read.

The paper proves symmetry of φ in Theorem 2.3. That reweighting argument does not preserve the extra biconstraints automatically. Its diagonal ψ formula and Theorem 12.2, which characterizes the symmetric minimum-value regime ψ(x,y)=x, are narrower statements. They neither yield the candidate boundary formula nor force general ψ symmetry. The apparently asymmetric plot records proved bounds, and the paper expressly does not deduce asymmetry of ψ from it. Theorem 6.5 and its proof were checked directly; its two bounds do not separate the universal values. The rational-boundary φ observation and irrational-boundary full reach are also different from the proposed exact rational ψ formula.

Figure 1 already supplies the 7×7, 13/27-regular weighted matrix. Both side weight vectors, every incidence entry, and the maximum row degree 4 agree exactly with the candidate. The complement is 14/27-regular. The matrix, weighted graph/linear programming framework and source regular-matrix theory require explicit joint-author credit. The boundary reduction and integer quantization deduction are the proposed contributions.

[Hompe's 1908.07453](https://arxiv.org/abs/1908.07453) was withdrawn in June 2022 because its results were edited and incorporated into the joint paper. The full pre-withdrawal v1 was read, and v2 was obtained independently: their extracted text differs only in cover version/date. Its general graph-attachment lemmas and fixed threshold results do not supply the asserted universal swap or the boundary degree formula. It should be cited as incorporated earlier work, not a later independent resolution.

## Search coverage and plausible near-misses

The exact query record is in SEARCH_COVERAGE.json: 64 queries in 16 search calls, plus two source-navigation calls, all on 3 October 2026 UTC. Searches covered exact ψ symmetry/asymmetry, rational boundary, weighted regular matrices and maximum degree, 13/27 and 14/27, both paper titles, thesis names, the five authors, subsequent work, publisher/arXiv and bibliographic venues. Current primary publication lists of Scott, Chudnovsky, Seymour and Spirkl were inspected; Hompe's primary later work was followed. These are bounded retrieved lists, not a claim that every author publication was inspected.

Crossref, OpenAlex and Semantic Scholar records were fetched. The retrieved direct citation endpoints returned no citing work for the joint paper; OpenAlex's withdrawn-Hompe endpoint returned the incorporating joint paper. Such index counts are incomplete discovery aids and provide no novelty certificate. OpenAlex's fuzzy title query was limited to its first 100 returned records.

References and promising near-misses were checked beyond snippets. Full relevant statements and proofs were read in the nonuniform degree/rainbow work, Hompe–Qu–Spirkl's triangle result, Hompe–Spirkl's corrected short rainbow cycle paper, Clinch et al.'s notes, Hompe–Huynh's additive-error paper, Nguyen–Scott–Seymour's distant domination paper, and relevant sections of the short bipartite directed-cycle and pure-submatrix papers. Their objectives or necessary hypotheses differ: reciprocal outdegree sums, rainbow girth, whole-graph kernels, or forbidden ordered matrices. None of the relevant theorems checked transfers to the generic four-constraint ψ boundary objective. The supplementary coverage record identifies the exact read scope and exclusions.

The 2022 Waterloo MMath thesis *Cycles and coloring in graphs and digraphs* was inspected for identity and relevant results/references. It is a different thesis from Hompe's 2019 Princeton senior thesis *Girth in digraphs*. Searches found citations to the latter, but no accessible full primary text; Princeton DataSpace search required authorization. No individual was contacted.

## Supported preprint framing and limits

A defensible framing, conditional on the separate mathematical audit, is: “We prove an exact formula for ψ on the rational boundary x+y=1, expressed through a minimum incidence degree. Applying the weighted regular matrix of Chudnovsky, Hompe, Scott, Seymour and Spirkl gives a negative answer to their symmetry question.” Credit the old construction directly. Do not describe the matrix as new or describe the two example bounds as exact ψ evaluations.

No equivalent earlier theorem was identified in this audit. The conclusion remains limited by the inaccessible senior thesis, incomplete citation indexing, language and terminology variation, unpublished or unindexed work, and the bounded author/reference search. A genuinely equivalent earlier theorem would change the priority disposition to already_solved. This audit supports a checkable contribution claim with transparent limits; it does not replace proof validation or historical priority certification.

