# Source credit, formulation and review scope

The accepted conclusion for problem 30006113, also represented by IDs 30004905 and 30006114, is source-credited to Karthekeyan Chandrasekaran, Chandra Chekuri and Shubhang Kulkarni, *An iterative rounding 2-approximation for Feedback Vertex Set via AI-assisted proof of an extreme point property*, arXiv:2609.04414v1, submitted 3 September 2026. The original question is attributed to Samuel Fiorini.

- Version-specific source: https://arxiv.org/abs/2609.04414v1
- Public landing page checked historically on 10 October 2026: https://arxiv.org/abs/2609.04414
- Source status: unrefereed AI-assisted September 2026 preprint. The checked submission history listed only v1; no journal acceptance or later version was established.

The full structural dependency chain for Theorem 1 in Section 2 was read and audited, including Proposition 1, Lemmas 1-8, Theorem 3, both corollaries and the final counting contradiction. The elementary corrections are displayed completely in CORRECTIONS.md and integrated in the authored reconstruction in AUDIT_REPORT.md. Theorem 2's complete structural proof in Section 3 was checked as a cross-check with its distinct edge-set formulation preserved. Section 1, Section 4 and Appendix A were read for formulation/dependency scope, without certifying the whole paper's algorithms or orientation extension.

## Original question and published formulation

1. Samuel Fiorini, *Open Problem: Iterative rounding for feedback vertex set*, Oberwolfach Reports 53/2021, printed p. 2944 / PDF p. 52. The displayed formulation has nonnegativity and the induced-subgraph density inequalities, without upper bounds. https://doi.org/10.4171/owr/2021/53
2. Chandra Chekuri, *Open Problem: Rounding Algorithms for Feedback Vertex Set and Subset Feedback Vertex Set*, Oberwolfach Reports 50/2024, printed pp. 2993-2995. It reiterates the unresolved question as of that report. https://doi.org/10.4171/owr/2024/50
3. Karthekeyan Chandrasekaran, Chandra Chekuri, Samuel Fiorini, Shubhang Kulkarni and Stefan Weltge, *Polyhedral aspects of feedback vertex set and pseudoforest deletion set*, Mathematical Programming. Equation (1), PDF p. 4, has the original nonnegative formulation; Conjecture 1 includes the cycle qualification. https://doi.org/10.1007/s10107-024-02179-9
   Author-hosted full text: https://chekuri.cs.illinois.edu/papers/fvs-polyhedral-mpa.pdf

## Exact bridge and limitations

The preprint's Definition 1 restricts the original polyhedron P to B = P intersect [0,1]^V. If an extreme point of P had every coordinate below 1/2, it would lie in B and remain extreme there, because a decomposition within B is a decomposition within P. Theorem 1 therefore proves the full original assertion. No optimum or cost-vector restriction is introduced. The conclusion is that SOME coordinate is at least 1/2, not that every coordinate is half-integral. The graph must contain a cycle; disconnected graphs and isolated vertices are allowed.

The corrected proof uses decreasing total set cardinality for refinement termination, the endpoint weak comparison, the factor two for intersection degrees, the all-component disconnected inequality, and isolated-vertex elimination before nonnegative tree rows. The audit preserves the strict-below-half premises and the distinction between induced-set density, edge-set density and ordinary cycle-cover LPs. No broader algorithmic claim is needed for acceptance.

All four source PDF identities and historical retrieval/inspection limitations are recorded in SOURCE_METADATA.json. The PDFs were inherited and rehashed rather than downloaded again by the audit. The Springer DOI open returned an access error; a pinned full source and the author-hosted citation were used. This publication preparation rechecked frozen identities and replayed the supplementary arithmetic checks but did not retrieve new scholarly sources, inspect source text anew or conduct a new literature search. Historical status checks are bounded evidence, not exhaustive literature clearance.

The audit and publication edition are AI-assisted and unrefereed. Mathematical acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. The contribution here is a source-credit audit, explicit elementary corrections and an explicit formulation bridge; source theorem credit remains with Chandrasekaran, Chekuri and Kulkarni. No novelty or priority is claimed. Programs, raw outputs, generated certificates, datasets, source copies and private coordination are not distributed; the accepted argument does not depend on omitted computational evidence.
