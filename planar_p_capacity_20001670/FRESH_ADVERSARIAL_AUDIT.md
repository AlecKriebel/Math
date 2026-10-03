# Fresh adversarial audit: planar homogeneous p-capacity

Problem 20001670, rank 457. Audited 2026-10-03. Scope: the ten frozen public files, plus the already supplied local source copy and the linked primary sources. No new author search, repository mutation, or remote write was performed. The frozen public files were not modified.

## Verdict

**PASS for the stated partial mathematical results, with two minor rigor clarifications below. HOLD for any promotion to a solution of the original conjecture.**

I found no theorem-blocking error in the area–diameter bound, elliptic-coordinate bound, non-colliding or endpoint-colliding thin-triangle comparison, or affine bulk identities. In particular, the endpoint theorem is supported by the cited primary sector result with its actual hypotheses. The global squeezing inequality is unproved, as the package explicitly acknowledges. The original problem remains unresolved.

The two clarifications are:

1. In Attempt 3, for the enlargement lemma stated for an arbitrary compact K, replace the argument using only the interior of K by the Sobolev level-set fact that the gradient of v vanishes almost everywhere on {v=1}. Since v=1 quasi-everywhere on K, it equals one almost everywhere there. This proves the integral over all of K, including compact sets with positive measure and empty interior. For the triangles actually used, their boundaries have zero area and the written interior argument already suffices.
2. In Attempt 5, identify uniform convexity of the L^p energy, or its Radon–Riesz property after the fixed linear change of gradient, as the reason minimizing gradients converge strongly. Strict convexity alone does not imply strong convergence in a general variational problem. Here the required stronger property holds for every 1<p<2, so this is a missing name/argument, not an obstruction.

## 1. Integrity and computational scope

The manifest SHA-256 is exactly

9f91143a5283e666038b1d256f7a209c4ba2e99dece5a30c86d9630b5c3f4215.

All ten public file byte counts and SHA-256 digests match the manifest. Running verify_constants.py produces checks.json byte-for-byte, including 6,145 rational Heron checks. I did not independently query the remote commit or reproduce historical queue/prior-branch searches. Those are provenance claims, not hypotheses of the mathematics.

The rational grid is only a finite test. The continuum Heron inequality has an elementary exact certificate: if a+b+c=2 and a is the largest side, then

A² − (1−a)²(2a−1) = (1−a)(a−b)(a−c) ≥ 0.

Thus no extension from 6,145 samples to all triangles is being made. The Machin alternating-series enclosure and the polynomial sign tests certify the stated rational bracket for rho. For the lower endpoint the script uses pi_lo, and for the upper endpoint pi_hi; those directions are correct because the polynomial decreases with the squared geometric coefficient. The p=4/3 bisection uses exact rational arithmetic. The gamma table is floating-point illustration only.

## 2. Normalization and imported hypotheses

The functional is the unnormalized homogeneous variational p-capacity in R², for 1<p<2. Its scaling degree is q=2−p, and the Brunn–Minkowski root is 1/q. For the width-integral perimeter, a segment of length ell has perimeter 2 ell. Thus perimeter two corresponds to a unit segment, and a same-perimeter segment has capacity c_p(P/2)^q. All later comparisons use that normalization consistently.

The disk value is correct: the exterior radial minimizer r^(−q/(p−1)) gives

b_p = 2 pi [q/(p−1)]^(p−1).

A nontrivial segment has positive capacity for this range; for example the homogeneous trace inequality with exponent p/(2−p) provides a lower bound, and a smooth cutoff provides finiteness. The neighborhood C_c^1 definition agrees with the relaxed homogeneous-Sobolev definition using quasi-everywhere constraints. The distinction between smooth competitors and the actual equilibrium potential is respected throughout. At p=2 the displayed homogeneous capacity vanishes; no logarithmic-capacity conclusion is inferred from it.

The primary [Bucur–Fragala–Lamboley text](https://arxiv.org/html/1102.1887), Theorem 2.1 and Remark 2.4, explicitly supplies the possibly-degenerate-triangle reduction for planar p-capacity. Its continuity, rigid-motion and homogeneity hypotheses are satisfied. It is preferable to cite that stated corollary, rather than silently extend a full-dimensional equality characterization to arbitrary degenerate summands.

Hausdorff continuity is correctly sketched: an admissible neighborhood gives upper semicontinuity; for an interior limit, a small homothetic shrink lies in all sufficiently close convex sets; for a segment limit, endpoint chords give the lower bound; point limits have capacity zero. Width-integral perimeter is continuous, and P≥2 diameter gives compactness after translation. Attainment therefore includes flat limits legitimately.

The [official AIM report](https://aimath.org/pastworkshops/symmetrybreakingrep.pdf), page 3, identifies the same fixed-perimeter problem and triangle reduction. The original catalogue and AIM problem-list URLs again failed retrieval during this audit. The direct Colesanti–Salani DOI also did not retrieve. These access limits do not invalidate the independently accessible primary reduction statement. No new completeness or novelty claim has been established.

## 3. Attempt 1: area–diameter bound

PASS.

The area isocapacitary lower bound follows from rearrangement, while the longest side provides a contained segment. These give genuinely separate lower bounds. The distance-to-segment trial has parallel perimeter 2+2 pi r, and its one-dimensional integral evaluates to b_p pi^(−q). The bound direction is correct: an upper bound for c_p supplies a lower bound for b_p/c_p.

The general compact-set parallel bound in [van den Berg–Gavitone, Theorem 1(i)](https://arxiv.org/html/2412.06563v2) covers the segment and has a finite integral here. Alternatively, the written inner/outer-cutoff construction establishes the needed trial bound directly, without importing a smooth-boundary theorem for a slit.

For perimeter-two triangles, 2/3≤a<1 and (2−a)/2≤b≤a. Heron's formula, or the exact factorization in section 1, proves A≥(1−a)sqrt(2a−1). The derivative (2−3a)/sqrt(2a−1) has the required sign. The increasing a² and decreasing pi(1−a)sqrt(2a−1) cross once inside (2/3,1). Consequently the minimax factor rho is valid, and the triangle reduction transfers it to every compact convex set. Points, whose perimeter is zero, satisfy the resulting unnormalized inequality trivially.

No equality characterization for actual capacity follows from the minimax equality; none is claimed.

## 4. Attempt 2: elliptic trial and gamma constants

PASS.

The coordinate map with focal half-distance 1/2 covers the exterior exactly once for mu>0 and 0≤nu<2 pi. Both slit faces are accounted for; there is no missing factor of two. The Jacobian is h² and the gradient norm is |U'|/h, yielding the factor h^(2−p) and precisely the stated A_q.

Weighted Hölder gives the restricted minimum [integral A_q^(−1/(p−1))]^(1−p). Inner ellipses and finite outer ellipses give admissible smooth approximants, so coordinate degeneracy at the foci is harmless. Jensen applies to the concave power q/2, and both subsequent negative powers are handled in the correct direction.

With t=tanh(2 mu), followed by s=t², the integral is

J(k) = (1/4) B(1/2,k/2) = sqrt(pi) Gamma(k/2)/(4 Gamma((k+1)/2)).

This verifies every factor in U_p^ell. Taking the minimum with the distance bound gives kappa_p≥pi and hence a unique rho_p. At p=4/3, J(1)=pi/4, U_p^ell=(4 pi²)^(1/3), and (b_p/U_p)^3=4 pi, so kappa_p=4. The quartic and its selected interval are correct; positivity before squaring excludes spurious sign choices. The elliptical ansatz is only an upper trial bound and is not mistaken for a nonlinear equilibrium solution.

## 5. Attempt 3: enlargement defect and flat-side estimate

PASS, with the general-K clarification already stated.

A direct way to justify the potentially delicate finite-energy pairing is to avoid the measure extension altogether. In D^{1,p}, u and v equal one quasi-everywhere on S. Therefore u+s(v−u) remains admissible for S for every real s. Differentiating its energy at s=0 is justified by Holder and gives

integral |grad u|^(p−2) grad u · (grad v−grad u) = 0.

This proves the displayed Bregman-defect identity. Convexity gives nonnegativity, and D_p(0,b)=(p−1)|b|^p. No false uniform lower bound by |a−b|^p for p<2 is used. For arbitrary compact K, use the gradient-on-level-sets argument to conclude grad v=0 almost everywhere on K.

The Hopf argument is local to the open flat sides, a positive distance from either endpoint. Odd reflection of the zero-trace p-harmonic function gives local C^{1,alpha} regularity. A tangent-ball annular barrier gives a positive inward derivative, and compactness produces one m_p and eta_p for the central interval. One could alternatively use a flat-boundary lower distance estimate and vertical slices; endpoint regularity is not required here.

The rectangle has area h/8 and is contained in every triangle with projection alpha in [0,1]. The capacity gain coefficient (p−1)m_p^p/8 is correct. The perimeter excess is at most h²/[2 alpha(1−alpha)], and concavity then gives the displayed c_p q h²/[4 delta(1−delta)] bound. The strict-height threshold is algebraically correct. Its dependence on delta is retained rather than wrongly made uniform near collisions.

## 6. Attempt 4: slit theorem and all thin triangles

PASS.

The relevant primary source is [Lundström–Singh](https://arxiv.org/html/2111.02721). Lemma 3.1 explicitly includes nu=1/2 and 1<p<2; equation (1.6) gives lambda=(p−1)/p. The profile has the required bounded and nonzero face derivative. Lemma 2.5 applies to local half-plane neighborhoods of (R,0), separately above and below the slit. It is not being applied to the globally nonsmooth slit disk. No excluded-endpoint uniqueness theorem is needed.

Here is the complete boundary comparison check. Choose R<1/2. Away from (R,0), positivity and compactness bound w/Psi below on the outer circle. Near (R,0), take neighborhoods smaller than the distance to either segment endpoint and use the local half-plane comparison to bound the ratio below on each face. The minimum of the resulting positive constants works on the entire circle. On the slit faces both functions tend to zero. At the origin, c Psi tends to zero and liminf w≥0, sufficient for bounded-domain p-harmonic comparison. No unproved limit for w/Psi at the tip is required. Reducing the radius ensures the cone 0<y≤x remains in the disk and yields w≥A_p y x^(lambda−1).

The geometric strip M<x<R_p, 0<y<h/2 is contained in the triangle because M=max(alpha,h)≥alpha and its roof is at least h/2. The barrier applies at its top because h/2≤x. Vertical Sobolev slicing with zero bottom trace proves the energy lower bound; it does not differentiate a pointwise function inequality. The key exponent is exactly p(lambda−1)=−1, producing the logarithm.

All constants come from the fixed unit-segment potential, so they are independent of alpha and h. Choosing delta_p<R_p with [(p−1)A_p^p/2] log(R_p/delta_p)>c_p q gives a strict comparison simultaneously for alpha≤delta_p and h≤delta_p. Reflection covers the other endpoint. The fixed positive middle threshold from Attempt 3 closes the cover. Thus one epsilon_p works for every alpha in [0,1]. Normalizing a longest side loses no degeneration: an exterior third-vertex projection would make another side longer.

This is uniform over triangle shape at a fixed p, not uniform as p approaches 1 or 2. It excludes only thin triangles and does not control the remaining nonthin compact family.

## 7. Attempt 5: affine differentiation and remaining obstruction

PASS for the identities and diagnosis; HOLD for the unproved inequality (4).

Use the full-space homogeneous Sobolev formulation with the constraint v=1 quasi-everywhere on the fixed set. An invertible affine map preserves these constraints and capacity-zero exceptional sets; its pullback gives exactly F_t(v)=integral t(v_x²+t^(−2)v_y²)^(p/2). Extending by one inside a triangle is equivalent. This avoids any Hadamard boundary formula, boundary normal integration, or unproved regularity at vertices/slit tips.

For t in a compact positive interval, the transformed L^p norms are uniformly equivalent. Comparing at old and new minimizers gives continuity of the minimum and shows the new minimizers form a minimizing sequence for F_t at the limiting parameter. Weak closedness of the fixed trace class, uniqueness, and uniform convexity give strong gradient convergence. The derivative integrands are continuous and bounded by a constant times |grad v|^p. The two-sided envelope argument is therefore valid for t>0.

Transforming the derivative back to physical coordinates yields tC'/C=1−p M_y. The perimeter derivative and normalized derivative in (3) have the correct coefficients and signs. If (4) held for every longest-base triangle, it could be integrated on 0<t≤1 because shrinking the height preserves the longest-base property. Hausdorff continuity supplies the t→0 endpoint; no derivative at the singular value t=0 is asserted. Nothing in the proved estimates supplies (4).

For a horizontal segment the vertical affine map leaves the set fixed, so the same legitimate bulk variation gives E_y=c_p/p and E_x=(p−1)c_p/p. These identities do not impose smooth boundary hypotheses.

The equilateral calculation is also correct. Threefold symmetry cancels both second and fourth nonconstant angular harmonics. Hence integral |grad u|^(p−4)(u_y²−u_x²)²=C_p(T)/2, E''/C_p(T)=p(p+2)/2, and P''/P=3/2. The normalized transported upper bound has positive relative second derivative (p−1)(p+6)/2. Its sign says nothing sufficient about the relaxed objective's second derivative, exactly as the package warns.

## Final scope boundary

The audit supports the universal rho and rho_p lower comparisons, the fixed-p strict comparison for every sufficiently thin triangle including endpoint collisions, and the exact directional/affine identities. It does not certify novelty, a formula for segment capacity, a p-uniform or numerical thinness threshold, or global segment minimality.

The unresolved mathematical task is a global comparison for nonthin triangles, or another argument excluding their optimality. Attempt 5 inequality (4) is a sufficient candidate, not an established theorem. The existing UNRESOLVED labeling should be retained.
