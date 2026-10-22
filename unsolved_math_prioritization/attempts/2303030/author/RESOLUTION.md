# Finite rank double layer operators on smooth Jordan curves

## Conclusion

**Literature resolved: the circle is the only possibility.** For a smooth planar Jordan curve Γ, the operator in Hayman and Lingham's Problem 3.30 has finite rank if and only if Γ is a circle; in that case its rank is one. This is a previously known rigidity result. The contribution of this report is a checked status correction and the explicit reduction of the question's conventions and function space to that result, not a new proof of the underlying rigidity theorem.

## The source question and its update

Problem 3.30 of [Hayman and Lingham, Research Problems in Function Theory, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed page 69 (PDF page 70), asks whether a noncircular smooth Jordan curve can have a finite-rank double-layer boundary operator acting on continuous functions. Its 2018 update records that the authors had received no progress. That update is a report of information received; it cannot establish that the problem was then unresolved.

The relevant finite-rank characterization had already been stated in the literature before the 2018 problem compilation. In particular, it is explicitly recorded in a paper coauthored by the problem's proposer.

## Published result and attribution

1. [Khavinson, Putinar and Shapiro, On Poincaré's variational problem in potential theory](https://web.math.ucsb.edu/~mputinar/poincare.pdf), §8.2, page 75 of the inspected author manuscript, states that only a disk can have a finite-rank planar Neumann–Poincaré operator. Its reference [39] is Shapiro's 1992 monograph. The related [journal article](https://doi.org/10.1007/s00205-006-0045-1) appeared in Archive for Rational Mechanics and Analysis 185 (2007), 143–184. The page locator here belongs to the author manuscript, not the journal pagination.
2. [Miyanishi and Suzuki, Eigenvalues and Eigenfunctions of Double Layer Potentials, arXiv:1501.03627v1](https://arxiv.org/abs/1501.03627v1), page 6, independently records the same finite-rank characterization, referring to Shapiro as [S]. Its operator is defined on L² of a C² boundary. This is the general finite-rank statement following Corollary 2.8, not merely the nearby rank-one or singular-value criterion.
3. [Miyanishi, Weyl's law for the eigenvalues of the Neumann–Poincaré operators in three dimensions: Willmore energy and surface geometry, arXiv:1806.03657v1](https://arxiv.org/abs/1806.03657v1), Corollary 5.1, page 11, explicitly says that a bounded C^{2,α} region, α>0, in dimension two or three can have finite-rank Neumann–Poincaré operator only in dimension two, with circular boundary. The two-dimensional ingredient is identified as the earlier known result; the paper's additional work concerns dimension three. The notation S¹ is understood up to translation and scaling, as is necessary for this scale-invariant rank statement.

The original proof in [Shapiro, The Schwarz Function and Its Generalization to Higher Dimensions, Wiley, 1992](https://www.wiley-vch.de/en/areas-interest/mathematics-statistics/the-schwarz-function-and-its-generalization-to-higher-dimensions-978-0-471-57127-8) was not independently inspected. Attribution to that book is supported by the two inspected papers above. No book theorem number or proof reconstruction is claimed.

## Exact operator reduction

Let Ω be the bounded component enclosed by Γ. A smooth Jordan curve is the connected smooth boundary of a bounded simply connected planar domain. In particular it meets the C^{2,α} hypothesis of the cited corollary for, for example, α=1/2.

Write y for the integration point, x for the evaluation point, n(y) for the outward unit normal, and ν(y)=−n(y) for the inward normal. With the directed chord from y to x, the question's kernel is

    k(y,x) = ν(y)·(x−y)/|x−y|²
           = n(y)·(y−x)/|x−y|².

Thus

    (Tf)(x) = ∫_Γ k(y,x) f(y) ds_y.

Miyanishi–Suzuki use

    (K_MS f)(x) = (1/π) ∫_Γ f(y) ∂_{n(y)} log(1/|x−y|) ds_y.

Differentiating with respect to the source variable y gives

    ∂_{n(y)} log(1/|x−y|) = −n(y)·(y−x)/|x−y|² = −k(y,x),

so K_MS=−T/π. Multiplication by a nonzero scalar preserves rank. The normal is at the integration variable in both definitions; no transpose or adjoint is being silently substituted. Reversing an overall normal convention also only changes the operator's sign.

A translation and dilation x↦c+ax, with a>0, multiplies this planar kernel by 1/a and arclength by a. Pullback by that map therefore conjugates the boundary operators. Their ranks coincide, so the circular conclusion does not fix a center or radius.

### Continuity at the diagonal

Take a local arclength parametrization γ(s). Taylor's formula, uniformly on a compact smooth curve, gives

    γ(s+h)−γ(s) = hγ′(s) + (h²/2)γ″(s) + o(h²).

The inward normal is orthogonal to γ′(s). Hence

    k(γ(s),γ(s+h)) → (1/2)ν(γ(s))·γ″(s).

The right-hand side varies continuously with s; the uniform remainder gives a continuous extension to Γ×Γ. This also follows from the diagonal-kernel discussion on page 4 of Miyanishi–Suzuki. No singular principal-value issue remains in this smooth two-dimensional setting.

### Passing between continuous and square-integrable densities

Here is a direct finite-rank argument; equality of spectra alone would not suffice.

Let A be any continuous-kernel integral operator on the compact curve Γ with arclength measure, and let A_C and A_2 denote its actions on C(Γ) and L²(Γ). Put

    M = sup_x (∫_Γ |k(y,x)|² ds_y)^(1/2) < ∞.

Cauchy–Schwarz gives ||A_2 f||_∞ ≤ M||f||_2. Continuity in x follows from continuity of k, so A_2 maps L²(Γ) into C(Γ).

Suppose F=A_C(C(Γ)) is finite dimensional. For f∈L²(Γ), choose continuous f_j→f in L²(Γ). The estimate gives A_C f_j→A_2 f uniformly. A finite-dimensional subspace F of C(Γ) is closed in the uniform norm. Therefore A_2 f∈F. Conversely, every member of F is in A_2(L²(Γ)), since C(Γ)⊂L²(Γ). Thus the two ranges coincide as spaces of continuous functions, and their finite ranks agree.

In the other direction, if A_2 has finite rank, restricting its domain to C(Γ) gives finite rank for A_C; equality of the finite ranges then follows from the preceding paragraph. Continuous functions that agree almost everywhere agree everywhere because every nonempty open arc has positive arclength. Consequently the L² identification loses no dimension here.

Apply this lemma to T. Finite rank in the exact C(Γ) formulation therefore gives finite rank for K_MS on L²(Γ). The cited planar rigidity theorem forces Ω to be a disk and Γ to be a circle.

### Converse and rank

For Γ={c+Ru: |u|=1}, write y=c+Ru and x=c+Rv. Then ν(y)=−u and, for u≠v,

    ν(y)·(x−y) = R(1−u·v),
    |x−y|² = 2R²(1−u·v).

It follows that k(y,x)=1/(2R), including on the diagonal by continuity. Therefore

    (Tf)(x) = (1/(2R)) ∫_Γ f ds,

a nonzero constant-valued operator. Since T1=π, its image is exactly the one-dimensional space of constant functions. This proves the converse and fixes the normalization.

## What is and is not established

The result resolves the exact smooth-Jordan-curve question by an explicitly cited known theorem. The normalization, continuity, function-space transfer, and circle calculation are proved above. The classical finite-rank rigidity theorem remains an external mathematical dependency. This report neither reproduces that theorem's original proof nor claims a new solution, historical priority, exhaustive literature coverage, formal verification, or human peer review. It makes no assertion about rough boundaries or unrelated finite-rank approximation problems.
