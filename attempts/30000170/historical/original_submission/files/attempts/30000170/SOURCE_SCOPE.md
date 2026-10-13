# Exact source and scope gate: 30000170 / OWR-783-002

Checked 2026-10-01. Rank 283. The short imported title is *Prox-Regularity of Polynomial Stability Abscissas*.

## What the report actually asks

Adrian S. Lewis, joint work with James V. Burke and Michael L. Overton, *Local Structure and Algorithms in Nonsmooth Optimization*, in *Optimization and Applications*, OWR 2/2005, pp. 104–106, DOI 10.4171/owr/2005/02. The exact Question 1 is on printed p. 106 (PDF page 38). That page and the surrounding contribution were read, and the question page was visually checked.

The report defines stability by alpha(p)=max Re(root)≤0, including imaginary-axis roots. It asks whether every degree-k polynomial near s^k has a unique nearest stable polynomial. The preceding discussion describes local uniqueness of projection onto the abscissa epigraph and calls the stable-polynomial question an essential ingredient.

The imported clean statement inserts the word “Equivalently.” That word is not in the source. Neither an arbitrary equivalence between function prox-regularity and stable-set projection nor an unqualified sublevel-set theorem should be assumed.

## Coefficient field, normalization and metric

The short OWR question does not repeat the field, coefficient metric, or monic normalization. Its opening control example uses real polynomials, but the cited variational theory is explicitly over complex coefficients:

- Burke–Overton, *Variational Analysis of the Abscissa Mapping for Polynomials*, SIAM J. Control Optim. 39(6) (2001), 1651–1676, begins with complex polynomials and the affine space of monic polynomials of fixed degree.
- Burke–Lewis–Overton, *Variational analysis of functions of the roots of polynomials*, Math. Programming 104 (2005), 263–292, DOI 10.1007/s10107-005-0616-1, treats all exact-degree complex polynomials in an open subset of coefficient space. Its p. 266 specifies the Euclidean real inner product Re sum conjugate(a_j)b_j in the ordinary monomial basis at zero. Its Lemma 1 isolates the monic slice for tangent calculations; that lemma alone does not prove a nearest-projection theorem.
- Lewis's *Eigenvalues and nonsmooth optimization* explicitly defines the stable monic set in C^n. His 2007 *Nonsmooth optimization and robust control* again states the complex-monic regularity theorem before discussing prox-regularity.

Accordingly the current mathematical candidate treats complex coefficient space as a real Euclidean space, both on the monic slice and on the full exact-degree space, and in fact all fixed positive-definite coefficient inner products. It separately records that real monic quadratics are different. No complex example is represented as a real-coefficient counterexample.

The ambiguity of the short report must be retained in any final source verdict. A result about the real-only variant would require its own proof.

## Three distinct regularity statements

1. Local single-valued metric projection onto the closed stable-polynomial set
2. Prox-regularity of the entire abscissa epigraph as a set, including its horizontal limiting normals
3. Function prox-regularity at a specified finite subgradient, using a function-attentive localization

The first is equivalent to stable-set prox-regularity in finite-dimensional coefficient space by Poliquin–Rockafellar–Thibault, *Local differentiability of distance functions*, Trans. AMS 352 (2000), 5231–5249, Theorem 1.3, including clause (k). The candidate below establishes failures of (1) and (2) directly under the complex convention. It does not infer failure of (3) from a sequence of divergent unscaled gradients.

The 2005 roots paper cites Rockafellar–Wets Definition 13.27 for the function conjecture. This definition must not be silently replaced by the stronger whole-epigraph set statement. Poliquin–Rockafellar's *A Calculus of Prox-Regularity*, J. Convex Analysis 17 (2010), 203–210, also distinguishes function and set formulations.

## Later-status and access limits

The 2005 paper's concluding section states a function prox-regularity conjecture. The 2007 Lewis survey still describes abscissa prox-regularity as open. The later Burke–Eaton arXiv:1511.03687v4 (2016) was checked in full for its scope: it gives spectral max-function subdifferential regularity results, not a nearest-stable uniqueness theorem.

A primary UW seminar archive records Jonathan Cross's 10 November 2009 talk, *Puiseux Series and Prox-Regularity of the Spectral Abscissa Map*. UW's newsletter and the advisor's CV confirm the 2010 thesis *Spectral Abscissa Optimization using Polynomial Stability Conditions*. Its full text has not been recovered in this gate; a secondary abstract cannot establish its precise conclusions. No outside contact or access bypass is attempted.

Targeted current searches did not reveal a primary full resolution of the exact local projection statement. That is not a novelty certificate or proof of present historical openness. No novelty claim is made.

## Prior campaign gate and publication limits

Exact numeric/source-code and broader abscissa PR searches returned no earlier campaign attempt. Both established target-directory commit histories on main, the local all-ref target-path log and related-target groups are empty for this ID. The branch was absent and the queue was queued 0/5. The exact-key imported research report is null; the record's dated literature assessment is upstream triage, not a prior Alec attempt.

Only mathematical notes, code, receipts and provenance are candidates for public checkpoints. Source PDFs, extracted full texts, source images and complete imported records remain local reading copies. Source recovery itself consumed no substantive author turn.
