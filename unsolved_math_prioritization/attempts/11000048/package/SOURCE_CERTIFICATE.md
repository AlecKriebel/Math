# Source certificate: the whole cone occurs

## Target and scope

Farb's **Problem 4.11**, in Chapter 2, Section 4.4 of *Problems on Mapping Class Groups and Related Topics*, asks which part of the g-dimensional Euclidean sector Cone(A_g) is determined by the Schottky locus. Here A_g is the moduli space of complex principally polarized abelian varieties, equipped with its locally symmetric Riemannian distance; the locus consists of Jacobians of smooth compact genus-g curves. The author-hosted source was checked in text and visually at PDF page 42, printed page 35. [Original source](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=42).

The catalogue extraction continues through explanatory prose introducing distortion. On the original page, the actual distortion question is separately labelled **Problem 4.12**. It also has its own catalogue identity, 11000049 / AMR-109-0049. Likewise, the preceding algorithmic question is Problem 4.10, ID 11000047. This certificate answers the complete numbered Problem 4.11; it does not collapse these distinct questions.

## Prior theorem and attribution

Ji and Leuzinger's Theorem 1.1 in arXiv:0811.4059v1 states that the Jacobian locus determines **all of Cone(A_g)**. More strongly, for each fixed genus there is a finite constant δ_g such that every point of A_g is within δ_g of that locus. The metric is the locally symmetric quotient metric, not the intrinsic path metric on the locus. The paper explicitly identifies Farb's Problem 4.11 as the problem being solved. [Preprint, pp. 3–4](https://arxiv.org/pdf/0811.4059#page=4).

The paper appeared in *Geometric and Functional Analysis* **19** (2010), 1693–1712, published online 6 February 2010. The publisher's abstract confirms the same conclusion. [Publisher](https://link.springer.com/article/10.1007/s00039-010-0049-8).

The checked preprint's Section 4.1 proves the density theorem using two inputs: a reduction-theoretic Weyl-chamber net in A_g, and approximation of diagonal period matrices by smoothings of compact-type curves made from elliptic components. Approximation is pointwise; a common plumbing parameter over the noncompact chamber is unnecessary. These are the cited authors' arguments, not new results of this investigation. [Preprint, pp. 11–12](https://arxiv.org/pdf/0811.4059#page=11).

## Why this answers the cone question

For clarity, the elementary scaling implication is recorded explicitly. Suppose a subset S of a metric space X satisfies

\[
\forall x\in X,\qquad d(x,S)\leq\delta<\infty.
\]

Given points x_n representing any point in a rescaling limit with factors r_n tending to infinity, choose s_n in S with d(x_n,s_n) less than δ+1. This is possible even when S is not closed and the infimum is not attained. Then

\[
\frac{d(x_n,s_n)}{r_n}\leq\frac{\delta+1}{r_n}\longrightarrow0.
\]

Thus s_n and x_n have the same limiting point. The triangle inequality also ensures that s_n stays at bounded rescaled distance from the basepoint whenever x_n does. Every ambient cone point is therefore represented by S; the reverse inclusion is immediate. Applying the cited theorem with S equal to the Jacobian locus gives the required equality, including the cone vertex and all chamber faces. Genus is held fixed throughout this limit.

## Cross-checks and nonclaims

Ji's 2019 paper *Metric distortion in the geometric Schottky problem*, Theorem 1.3, restates the coarse-density result and credits the joint 2010 paper. Its Remark 1.7 repairs speculative arguments concerning **distortion** in the older paper's Section 8; it does not retract the coarse-density theorem. This is important because the catalogue extraction includes the transition toward distortion. [2019 primary paper, pp. 2213–2215](https://cdn.sciengine.com/doi/pdf/9D3C71BECF314AF3ABFCA33F0E461337).

- No genus-independent bound, effective value of δ_g, or membership algorithm is claimed.
- Finite ambient distance does not establish an intrinsic-path-metric assertion.
- This certificate does not claim equality of compactification boundaries.
- The theorem number **1.1** here refers to the checked 2008 preprint. The 2019 article refers to the published result as Theorem 1.2; numbering across versions is not conflated.
- The genus-one case is also immediate: an elliptic curve is its own principally polarized Jacobian.
- This is a credited prior resolution, with no novel mathematical contribution and no substantive proof-attempt turn charged.
