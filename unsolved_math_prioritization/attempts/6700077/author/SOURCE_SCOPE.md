# Source identity, conventions and inspection limits

## Target and access

The requested URL is https://www.unsolvedmath.com/problems/6700077 . An ordinary web opening failed; a direct retrieval returned a 59-byte Forbidden response. The live page's contents were not inspected. No access restriction was bypassed. The available descriptor identifies AMR-066-0077 and points to the primary source below. Its raw underlying AI report was unavailable and was not inspected; an older descriptor note describes that report as addressing density instead. That note is not treated as a checked mathematical result.

The source is M. Gromov, *101 Questions, Problems and Conjectures around Scalar Curvature*, incomplete and unedited version dated October 1, 2017:
https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf
Section 26, printed pp.79–83, was inspected in extracted text; printed pp.80–81 were also visually inspected. A fresh download matched the locally available source bytes. The problem is closure of continuous positive-definite Riemannian tensors under C0 approximation at a fixed scalar lower bound. The statement adds neither compactness nor a dimension restriction. The S2 comparison presupposes n >= 2. Our auxiliary compact-manifold statements are explicitly narrower.

## Why the printed definition needs a convention warning

The displayed definition on p.80 prints an upper-bound sign where the ball comparison expresses a lower bound, a radius threshold inconsistent with its own scalar normalization Sc(S2(R)) = 2/R^2, and an infimum of lower thresholds where the surrounding smooth-compatibility claim requires a supremum. These are visible in the PDF, not merely OCR errors. This investigation does not claim a trivial solution by exploiting those inconsistencies.

For positive thresholds we use the standard, explicit interpretation also used by Deng (Definitions 2.1–2.3): for each 0 < lambda < kappa, sufficiently small balls have volume less than that in

P_lambda = S2(sqrt(2/lambda)) x R^(n-2).

The radius is locally positive in the center, may depend on lambda and the metric, and is not assumed uniform across a convergent sequence. Let M_lambda(r) denote the model-ball volume. Its smooth expansion is

M_lambda(r) = omega_n r^n [1 - lambda r^2/(6(n+2)) + O(r^4)].

The source's negative-threshold prescription uses product with S2(sqrt(-2/lambda)) for lambda < 0 and asks for locally smaller balls than Euclidean space in dimension n+2. We retain that prescription rather than replacing it by hyperbolic n-space. At zero, the relaxed numerical lower bound and the stronger condition V(x,r) <= omega_n r^n on a positive radius interval should be distinguished. Deng adopts the latter at zero. Our zero-threshold auxiliary results explicitly prove this stronger inequality. They do not assert that every smooth scalar-flat metric satisfies it.

The smooth small-ball expansion used in the proofs needs only C2 regularity with remainder o(r^2) after volume normalization. An O(r^4) remainder is not asserted for general C2 metrics. The topology is local uniform convergence of tensor coefficients on the fixed manifold, equivalently local uniform relative quadratic-form convergence. On a compact manifold this is uniform C0 convergence. It is much stronger than arbitrary Gromov–Hausdorff convergence and does not imply derivative bounds.

## Primary literature checked

- J. Deng, *Curvature-Dimension Condition Meets Gromov's n-Volumic Scalar Curvature*, SIGMA 17 (2021), 013, https://sigma-journal.com/2021/013/sigma21-013.pdf . Definitions 2.1–2.3 and proof of Theorem 3.5 inspected. The stability theorem assumes a common positive SC-radius, compactness, and an n-dimensional normalization of the limit. Its abstract omits hypotheses that matter here. We independently prove the fixed-manifold version rather than invoking it without those hypotheses. No endorsement of every other statement in this paper is intended.
- P. Burkhardt-Guim, *Defining Pointwise Lower Scalar Curvature Bounds for C0 Metrics with Regularization by Ricci Flow*, SIGMA 16 (2020), 128, https://arxiv.org/abs/2007.14967 . Theorems 4.1 and 4.3 and Section 5 inspected. Their weak Ricci-flow definition is closed and agrees with smooth approximation on closed manifolds. The comparison in Section 5 with Gromov concerns his cube/dihedral formulation; it is not an established equivalence with the volumic definition.
- M.-C. Lee, *Quantification of scalar curvature under C0 convergence using smoothing*, arXiv:2604.17759v1, https://arxiv.org/abs/2604.17759 . Introduction and Theorems 1.1–1.3 inspected. This current preprint compares smooth metrics and supplies no volumic-to-Ricci-flow equivalence.
- M. Fogagnolo, G. Gatti, A. Pluda, *Scalar curvature bounds for 3D continuous metrics through the Inverse Mean Curvature Flow*, May 26, 2026 version, https://cvgmt.sns.it/media/doc/paper/7731/FGP-Scalar-curvature-bounds.pdf . Introduction, Theorem 1.1, definitions and final proof sketch inspected. The theorem uses IMCF scalar curvature, dimension three, completeness, H2=0 and a uniform global isoperimetric inequality. The paper explicitly defers technical details of parts of its program. It is not cited as a proof of this target.

Targeted public searches included the exact ID, title, volumic closure/stability, continuous metrics, and recent smoothing/IMCF work. No exact general resolution was verified in the inspected sources. This is a bounded search result, not a global-openness or priority assertion. Downloading a full PDF does not mean its entire proof was reviewed; the inspected portions are listed above.

## Prior-attempt checks

On 2026-10-05, live AlecKriebel/Math PR searches for 6700077, AMR-066-0077 and volumic returned no matches; a scalar-curvature search returned other identified problems. Branch searches for the ID and volumic returned no matches. Default-branch code searches for the ID and AMR identifier returned no matches. Requests for the target attempt directory and its README returned 404. The main queue row was still queued, 0/5; this was not used as proof of no earlier attempt. Available conversation search found only unrelated problems and no verified attempt for this target. Unindexed, renamed, deleted or otherwise inaccessible work is not excluded.
