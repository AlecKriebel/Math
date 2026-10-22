# Source gate: exact higher-order matrix decomposability

Checked 21 October 2026. Queue row 1834, catalogue ID 30004154, source key OWR-16938-002.

## Verdict

The primary problem is recovered. It asks for useful conditions for exact coordinate-supported positive-semidefinite decompositions with block size greater than two. This is factor-width-at-most-k membership. A generic SDP characterization was already explicitly available in the authors' original work; restating it is not a new solution. No complete general structural characterization for 2 < k < n was verified in this search. That is a bounded literature finding, not proof that none exists.

## Primary provenance and mathematical scope

Antonio Frangioni, joint work with Claudio Gentile and James Hungerford, **Perspective Reformulations Beyond the Separable Case**, printed pp.1593–1596, especially p.1595, in *Mixed-integer Nonlinear Optimization: a hatchery for modern mathematics*, Oberwolfach Reports 16 (2019), no.2, 1573–1637, DOI 10.4171/OWR/2019/26. Workshop 2–8 June 2019; report published 4 June 2020. [Official record](https://ems.press/journals/owr/articles/16938), [official PDF](https://ems.press/content/serial-article-files/46805).

Formalization of the intended target: let Q be a real symmetric positive-semidefinite n-by-n matrix and 2 < k <= n. For each k-element subset S of {1,...,n}, let E_S select the corresponding coordinate columns. Determine when there exist PSD k-by-k matrices P_S such that

    Q = sum_{|S|=k} E_S P_S E_S^T.

The approximate version allows an additional PSD residual Phi; exactness means Phi=0. Blocks may be zero or singular, and supports may have fewer than k nonzero coordinates. They need not be principal submatrices of Q itself. The supports overlap. No change of basis, nonnegativity of factor entries, prescribed graph, fixed rank, or positive definiteness is assumed. The case k=n is automatic; k>n is outside the natural indexing convention. The request's structural intent follows from its contrast with the explicit k=2 characterization, but the informal source does not impose a formal complexity or closed-form requirement.

## Catalogue audit

The catalogue identifies the right source and target, but omits the real symmetric PSD hypothesis, embedding convention, zero-residual meaning, and overlap of blocks. Its terminology must not be read as tensor decomposition or block diagonalization. Its 2019 proposed year is the workshop year, not the report's 2020 publication year. The clean statement's claim that definitions were restored is stronger than the actual self-contained detail supplied. Its dated open-status assessment cites only the OWR report and is not independent evidence of current completeness of the literature.

## Existing criteria and novelty boundary

The companion paper is Frangioni–Gentile–Hungerford, *Decompositions of Semidefinite Matrices and the Perspective Reformulation of Nonseparable Quadratic Programs*, Mathematics of Operations Research 45(1) (2020),15–33; online 16 October 2019, DOI [10.1287/moor.2018.0969](https://doi.org/10.1287/moor.2018.0969). The inspected [author manuscript](https://pages.di.unipi.it/frangio/papers/2x2D4PR.pdf) is dated 1 November 2019.

Section 5 connects exact 2-by-2 decomposition to weak scaled diagonal dominance and cites Boman–Chen–Parekh–Toledo, *On factor width and symmetric H-matrices*, LAA405(2005),239–248, DOI 10.1016/j.laa.2005.03.029. Appendix A, equation (37), explicitly supplies the residual-minimizing SDP for triples, states that zero optimum characterizes exact decomposition, and extends the construction to general k. Consequently neither generic feasibility nor a residual-zero SDP is a resolution of the intended structural problem. Numerical small residual is not exact certification. Likewise diagonal normalization must first separate zero diagonal coordinates, whose rows and columns vanish for PSD Q.

## Later literature checked and scope warnings

- Johnston–Moein–Plosker, *The Factor Width Rank of a Matrix*, LAA716(2025),32–59, DOI [10.1016/j.laa.2025.03.016](https://doi.org/10.1016/j.laa.2025.03.016); inspected [arXiv:2405.11556v2](https://arxiv.org/abs/2405.11556v2), revised 2 April 2025. Section 2.1 explicitly identifies coordinate-supported PSD sums with factor width and discusses SDP computation. It supplies rank bounds and structured cases, not a full elementary membership characterization. Factor-width-k rank minimizes the number of sparse rank-one terms and differs from factor width and ordinary matrix rank.
- Johnston–Moein–Pereira–Plosker, *Absolutely k-Incoherent Quantum States and Spectral Inequalities for Factor Width of a Matrix*, PRA106:052417(2022), [arXiv:2205.05110v2](https://arxiv.org/abs/2205.05110v2). The inspected primary abstract addresses membership guaranteed by eigenvalues, hence absolute incoherence, not arbitrary fixed-coordinate membership. These two problems must not be conflated.
- Gouveia–Kovacec–Saee, *On sums of squares of k-nomials*, [arXiv:1912.01371v2](https://arxiv.org/abs/1912.01371v2), revised 12 January 2021. The inspected primary abstract describes geometry of factor-width cones and duals and restrictions on polynomial multiplier certificates. It is relevant prior literature for any dual-cone proposal; no full membership resolution was established from that abstract.
- Naomi Shaked-Monderer, *On factor-width ranks*, DOI [10.1016/j.laa.2026.09.011](https://doi.org/10.1016/j.laa.2026.09.011), LAA752,308–331, January 2027 issue. Primary ScienceDirect preview is already accessible in search retrieval. Crossref registration was created 11 September 2026; the metadata returned no separate online-publication date. Do not exclude it merely for the future issue date. Preview describes a complete factor-width-2 rank formula, bounds for width-3 rank of width-2 matrices, distinct-support minimal factorizations, and graph-specific results. This is not the same as an arbitrary ordinary-rank-two membership theorem. Full-text retrieval was unavailable (direct ScienceDirect open returned 403), so its complete overlap with any proposed rank-two finite-cone theorem remains unverified. No novelty claim should rely on absence from the preview.

## Verification and limitations

CORPUS_VERIFICATION.json contains fresh local rehashes of the recovered corpus copies: one matching problem record and no matching research-results entry. These are not fresh upstream downloads. SOURCE_METADATA.json records downloaded PDF hashes, byte counts, public URLs, and inspection history. Source texts, PDFs, corpus excerpts, and raw metadata are retained separately, not included in the public source-gate prose. No queue or GitHub mutation was performed.
