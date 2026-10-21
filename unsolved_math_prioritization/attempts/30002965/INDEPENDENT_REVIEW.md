# Independent mathematical audit: Boolean quadric volume, ID 30002965

## Verdict and scope

**ACCEPT as literature-resolved for the good-bounds alternative.** The transfer of Avis–Devroye–Deza's September 2026 preprint to the complete-graph Boolean quadric polytope is valid. It supplies an explicit positive lower bound, an asymptotically much stronger upper bound than the bound quoted in the original problem, and the leading logarithmic volume asymptotic. This is not an exact general volume formula, an original new solution, or a claim of peer review.

The original Jon Lee problem is in Oberwolfach Report 46/2015, printed pages 2737–2738. Its alternatives explicitly include a significant upper-bound improvement and/or a nontrivial lower bound. Thus the acceptance does not depend on weakening an exact-formula-only question.

Sources: https://doi.org/10.4171/OWR/2015/46 and https://arxiv.org/abs/2604.16735v2 . The arXiv abstract and HTML were independently reopened on 21 October 2026; the version is dated 2 September 2026 and names David Avis, Luc Devroye, and Antoine Deza. Local complete PDF text was inspected for the definitions, covariance map, elliptope recurrence, Proposition 5.2, Theorem 5.3, and remaining open problem.

## Citation correction

The covariance determinant identity is **unnumbered**, following Definition 2.5 on PDF page 5. Calling it “Proposition 2.6” is incorrect for the inspected v2 PDF. Cite Section 2, Definition 2.5 and the ensuing covariance-map identity instead. Theorem 5.3 is numbered correctly.

## Normalization and affine transfer

Set m=n+1, r=n(n−1)/2, and d=n(n+1)/2. All volumes below use ordinary Lebesgue measure in the listed distinct coordinates, not ambient symmetric-matrix Frobenius measure or normalized lattice volume.

P_n has coordinates (x_i,y_ij), with vertices y_ij=x_i x_j and x_i in {0,1}. The map z_i,m=x_i and z_ij=x_i+x_j−2y_ij sends every vertex onto its corresponding 0/1 cut vector, and all cut vectors arise by fixing the new vertex outside the cut. Ordering singleton coordinates first makes its derivative block triangular with diagonal blocks I_n and −2I_r. Its absolute determinant is 2^r. Therefore vol(P_n)=2^(−r) vol(Cut_m).

Let E_m consist of positive semidefinite correlation matrices represented only by their off-diagonal entries, and write V_m=vol(E_m). The coordinate transformation z=(1−e)/2 has absolute determinant 2^(−d), giving vol(I_m)=2^(−d)V_m. Consequently, with U_n=2^(−r−d)V_(n+1)=2^(−n²)V_(n+1),

(2/π)^d U_n ≤ vol(P_n) ≤ U_n.

No additional factor from diagonal coordinates, graph suspension, or symmetric duplicate entries is missing.

## Independent check of the main bound's proof

For a correlation matrix represented by unit vectors v_i, select an isotropic Gaussian vector g and cut according to the signs of g·v_i. The probability that vertices i and j are separated is arccos(v_i·v_j)/π. Thus the coordinatewise map f(t)=arccos(1−2t)/π sends I_m into the convex hull of cut vectors. This supplies the inclusion directly without relying on a facet description or an optimization-ratio argument.

On (0,1), f is strictly increasing and smooth with f'(t)=1/[π sqrt(t(1−t))]≥2/π. The product map is injective, and its Jacobian determinant in d coordinates is at least (2/π)^d. Applying change of variables on the open cube gives vol(f(I_m))≥(2/π)^d vol(I_m). Endpoint-coordinate slices and their images lie in finitely many coordinate hyperplanes and have zero d-dimensional volume, so the unbounded derivative at endpoints does not invalidate the argument. Finally, f(I_m)⊆Cut_m⊆I_m. This proves both volume inequalities for all n≥2.

The lower bound does not assert that f(I_m) is convex or equals the cut polytope; neither assertion is needed.

## Independent derivation of the elliptope recurrence

For a≥0 let F_k(a) be the integral of det(R)^a over the positive definite correlation matrices R of size k, in their distinct off-diagonal coordinates. Set F_1(a)=1. Write R in block form with principal block A of size k−1 and last column vector b. Schur complementation gives det(R)=det(A)(1−b^T A^(−1)b). Substitution b=A^(1/2)u, followed by the standard unit-ball radial integral, gives

F_k(a)=π^((k−1)/2) Γ(a+1)/Γ(a+(k+1)/2) · F_(k−1)(a+1/2).

Iteration at a=0 proves

V_m = π^(m(m−1)/4) [product over j=2,...,m of Γ(j/2)] / Γ((m+1)/2)^(m−1).

The singular correlation matrices have measure zero, so this equals the full elliptope volume. Taking successive ratios and using Gamma duplication yields

V_2=2,
V_m/V_(m−1)=[sqrt(π) Γ(m/2)/Γ((m+1)/2)]^(m−1)
             =2^((m−1)²) B(m/2,m/2)^(m−1).

This independently verifies the source recurrence, including its exponent and index shift.

## Asymptotic improvement

The Gamma-ratio estimate gives

log(V_m/V_(m−1))=((m−1)/2) log(2π/m)+O(1).

Summing yields log V_m=−(m²/4) log m+O(m²). Both transferred bounds therefore have logarithm −(n²/4) log n+O(n²), since r+d=n² and d=O(n²). Squeezing gives the same asymptotic for vol(P_n).

For the quoted older relaxation bound Q_n=2^(2n−d)n!/(2n)!, Stirling gives log Q_n=−(log 2)n²/2+O(n log n). Hence

log(U_n/Q_n)=−(n²/4) log n+O(n²),

and U_n/Q_n tends to zero. This is a rigorous substantial asymptotic improvement, not a numerical inference. The elliptope upper bound is not better at every small n. A uniformly no-worse presentation should use min(Q_n,U_n).

## Small-case checks

For n=2, V_3=π²/2. The bounds are 1/(4π)≤vol(P_2)≤π²/32. Independently, P_2 is the tetrahedron with vertices (0,0,0), (1,0,0), (0,1,0), (1,1,1), whose edge determinant is 1, hence volume 1/6. Numerically: 0.0795775≤0.166667≤0.308425. The old bound is exact here and should not be described as improved.

For n=3, V_4=32π²/27, giving lower bound 4/(27π⁴) and upper bound π²/432. The transferred source-table exact cut volume gives vol(P_3)=1/180, inside this interval.

Direct recurrence evaluation gives U_n/Q_n approximately 1.85055, 2.74156, 2.31047, 0.897297, 0.138086, 0.00748954, and 0.000130128 at n=2,...,8 respectively. At n=10 it is approximately 9.45958×10^(−10). These numerical values are checks, not the proof of asymptotic improvement.

## Claims that must remain open

The method does not determine exact vol(P_n) for arbitrary n. It does not determine the quadratic-order logarithmic gap between cut and elliptope volumes; the inspected source explicitly retains that limit as Open Problem 2. It does not prove a novelty claim or establish journal acceptance. The upper bound should be called asymptotically improved, or combined with the older bound by a minimum.

No mathematical blocker was found. No QUEUE changes, publication, commits, or pushes were performed in this audit.
