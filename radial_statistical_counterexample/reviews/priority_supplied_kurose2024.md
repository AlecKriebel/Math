# Supplied full-text audit: Kurose 2023/2024

Checkpoint: **2026-09-24 04:18:02 UTC**. **100%** of this bounded,
article-specific audit completed; this is not a percentage estimate of worldwide
priority clearance. Independent review by the proof-audit agent. No contact with
the author or other individuals, manuscript changes, or Git operations.

## Source and coverage

Takashi Kurose, *A certain ODE-system defining the geometric divergence*,
Information Geometry **7** (2024), S541–S554,
[DOI 10.1007/s41884-023-00110-3](https://doi.org/10.1007/s41884-023-00110-3).
The first page records online publication on **5 June 2023**.

User-supplied source: `A-certain-ODE-system-defining-the-geometric-divergence.pdf`.
SHA-256:
`6f1d4ee3a360ebd22a652a7be4d3d4f4cb2e0c42de8329ce8d6ea74ffeb7be3d`.

All **14 pages**, including every theorem, proof, example, and the 11-entry
bibliography, were read in extracted text. Printed pages S544, S546–S548,
S550–S551 were also checked against rendered page images, including the
curvature identity, bundle connection, ODE, initial conditions, Proposition 7,
Corollary 8, and Theorem 9. Renderings are local scratch files under
`tmp/priority_supplied_pdfs/kurose2024_agent/`.

## Finding

**No explicit earlier negative answer to FMU1998 Question 3(e), no stated
equivalent counterexample theorem, and no exhibited sphere-times-line example
were found in this complete article.** Its general contrast-function existence
theorem does not imply the radial level-set property in that question. The
article nevertheless supplies established curvature machinery from which the
product obstruction can immediately be recovered; that machinery is prior art.

The precise comparison is:

| Location | Actual statement | Consequence for this audit |
|---|---|---|
| S543, Definitions 1 and Proposition 2 | A contrast function induces the statistical structure through derivatives of order at most three on the diagonal. | Existence of a contrast function is weaker than requiring its differential to annihilate all terminal-velocity orthogonal planes away from the center. |
| S544, Definition 2, equations (1)–(4) | A curvature criterion for 1-conformal flatness, with `S = σ/(n−1) Id − Ric♯`. | The necessary curvature identity used in the candidate is established theory, attributed here to earlier Kurose work. |
| S546–S547, Proposition 5 | The auxiliary bundle connection is flat exactly in the 1-conformally flat case. In that case its parallel section has components `(ρq, dρq, g)`. | The identification of the covector component with `dρq` is asserted with the flatness hypothesis. |
| S547–S550, equations (8), (12)–(17) | The ODE can always be solved separately along selected rays; its scalar endpoint defines a function. Equation (17) identifies only the contraction of its differential with the radial vector. | It does not identify the whole endpoint covector with the differential of the endpoint scalar as the ray varies. |
| S550–S551, Proposition 7 and Corollary 8 | Along a dual geodesic the ODE covector annihilates the terminal orthogonal plane. Corollary 8 adds 1-conformal flatness before replacing this covector by the geometric-divergence differential. | This is the known sufficient direction. Neither statement proves or disproves the converse by itself. |
| S551–S553, Theorem 9 and Corollary 10 | Smooth families of selected rays produce contrast functions on arbitrary statistical manifolds; normal-coordinate choices give the family `ρα`. | Their proofs establish the diagonal derivatives, not the missing radial level-set condition. |

The article's sole numbered example, Example 1 on S545–S546, constructs
1-conformally flat structures by affine immersions of convex graphs. It does
not exhibit the candidate's Levi–Civita product or its non-self-dual deformation.
The 1998 problem collection does not occur in the bibliography.

## Direct check separating the two endpoint objects

This computation is our comparison of the source construction with the
candidate, **not a computation stated in Kurose's article**. Two reviewers independently derived and compared it.

On the unit cylinder `S² × R` with the product Levi–Civita connection, fix a
center, let `r` be the spherical distance to the endpoint and `b` its signed line
displacement in a normal neighborhood. Put `E = (r²+b²)/2`. The scalar curvature
is 2 and the Ricci operator is `diag(1,1,0)`, so Kurose's equation (1) gives
`S = diag(0,0,1)`. Along the affine geodesic with parameter `s ∈ [0,1]`, its
velocity `T` and metric dual are parallel, and `h(T,ST)=b²`.

Equation (8) with initial condition `(f,λ,g)=(0,0,1)` therefore has the solution

\[
\lambda(s)=\frac{\sin(bs)}b h(T(s),\cdot),\qquad
g(s)=\cos(bs),\qquad
f(s)=(r^2+b^2)\frac{1-\cos(bs)}{b^2}.
\]

Substitution checks all three ODE components and initial conditions. At `b=0`
the smooth limits are `λ(s)=s h(T(s),·)`, `g(s)=1`, and `f(s)=r²s²/2`.
All α-connections coincide in this Levi–Civita example, so these formulas apply
to every normal-coordinate choice in Corollary 10.

As endpoint fields, with `a(b)=sin(b)/b` and `c(b)=(1−cos b)/b²`, they give

\[
\lambda_{\rm end}=a(b)\,dE,\qquad
\widehat\rho_q=2E c(b),\qquad
d\widehat\rho_q=2c(b)\,dE+2E c'(b)\,db.
\]

For sufficiently small `b`, `a(b)` is nonzero, so the covector's kernel is
exactly `ker dE` and is integrable. Nevertheless

\[
d\lambda_{\rm end}=a'(b)\,db\wedge dE,
\qquad
d\widehat\rho_q\wedge dE=2E c'(b)\,db\wedge dE.
\]

These are generally nonzero: `a'(b)=−b/3+O(b³)` and
`c'(b)=−b/12+O(b³)`, while `db ∧ dE` is nonzero at points with `r>0`.
Thus the ODE covector has an integrable kernel without being closed, and the
constructed contrast function generally does not have the radial spheres as
level sets. There is no contradiction with Proposition 7, Corollary 8, or
Theorem 9. Nor does this assert that the cylinder lacks a suitable radial
potential: its ordinary energy `E` is exactly such a potential.

## Priority boundary and bibliographic note

This full-text inspection closes the specific access gap recorded in the
earlier citation audit for this article. It finds no matching published
resolution within these 14 pages. It does **not** establish first discovery:
the product obstruction follows by applying established curvature criteria,
and radial integrability of Levi–Civita structures is classical. Determining
whether someone previously made and recorded that combination requires other
sources or evidence beyond this article. No novelty probability is assigned.

Reference [7] on S554 prints Kurose's 1999 paper as pages **201–219**. Earlier
author-record metadata encountered in this project gave **209–219**. This
audit preserves that bibliographic discrepancy and does not silently resolve
it from the 2024 bibliography alone.
