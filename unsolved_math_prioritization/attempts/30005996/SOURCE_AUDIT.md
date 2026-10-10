# Primary-source audit

Checked 8 October 2026. This is a bounded source review, not proof of worldwide openness or novelty. No source bodies are included in this packet.

## 1. Controlling problem

Federico Franceschini, joint work with Alessio Figalli, “The dimension and behaviour of singularities of stable solutions to semilinear elliptic equations,” in Calculus of Variations, Oberwolfach Report 37/2024, pp. 2141–2144.

- Official PDF: https://ems.press/content/serial-article-files/50045
- DOI: https://doi.org/10.4171/owr/2024/37
- Inspected the setup, extremal branch, isolated-singularity question, and §3.1. The formula and hypotheses on printed pp. 2141 and 2143 were also visually inspected after local PDF rendering.
- The full target remains the pointwise limsup upper estimate, with the surrounding branch and nonlinearity assumptions restored in CLAIM_AND_SCOPE.md.

## 2. Averaged estimates do not supply the requested upper bound

Alessio Figalli and Federico Franceschini, “Stable Semilinear Elliptic Equations: epsilon-Regularity à la Brezis and Dimensional Bounds for the Singular Set.”

- Version inspected: arXiv:2606.21546v2, submitted 25 August 2026.
- Pinned PDF: https://arxiv.org/pdf/2606.21546v2
- Abstract/version history: https://arxiv.org/abs/2606.21546
- Theorem 1.4 bounds the limsup of the scale-invariant integral of V above and below at singular points. Remark 1.3 gives the cutoff-based averaged upper bound. Remark 1.5 extracts a sequence with V(x_k)>=c|x_k-x_0|^(-2), a pointwise lower conclusion.
- The theorem therefore does not furnish the target's pointwise upper estimate. This review does not certify every proof in the manuscript or assert journal acceptance.
- A web-indexed author-hosted PDF carried an inconsistent “upper bound” description beside a lower-bound inequality; direct retrieval of that author URL failed 404. The inspected v2 PDF has the mathematically correct lower-bound wording. A separately attempted v1 PDF retrieval failed 403. No byte-level claim is made for either unavailable version; the stable source for this report is the retrieved v2 PDF.

## 3. Radial case is prior work

Salvador Villegas, “Behavior near the origin of f'(u*) in radial singular extremal solutions.”

- Primary preprint: https://arxiv.org/abs/2005.14334
- PDF: https://arxiv.org/pdf/2005.14334
- Inspected Theorem 1.1 and its proof, especially the first-eigenfunction upper estimate. For a singular unit-ball extremal solution, it gives

    2(n-2)/lambda* <= limsup r^2 f'(u*(r)) <= lambda_1(B_1)/lambda*.

- Route 1 reproduces the elementary upper-bound argument with credit. This is not new work and does not settle arbitrary domains.

## 4. A recent related title addresses a different question

Bao Yu and Yang Zhou, “Singular Extremal Solutions on Thin Ellipsoids with Varying Nonlinearities,” arXiv:2609.06673v1,6 September 2026.

- PDF: https://arxiv.org/pdf/2609.06673
- Abstract: https://arxiv.org/abs/2609.06673
- Inspected the introduction and main theorem. The stated result constructs singular extremal solutions for selected nonlinearities on sufficiently thin ellipsoids in sufficiently large dimension. Its contrast with regular Gelfand solutions concerns dependence on the nonlinearity and domain, a different Brezis question. No target pointwise upper theorem is established by that abstract/main statement. This report does not audit the construction's full proof or claim journal acceptance.

## Provenance limit

SOURCE_METADATA.json records hashes, sizes, public URLs, and inspection descriptions for successfully retrieved PDFs. Hash equality confirms byte identity, not theorem correctness. A matching title or broad claim of solving a Brezis problem was never treated as a full-target resolution.
