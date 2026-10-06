# Independent audit: Ricci-flow scalar/Weyl cones

Problem 30001006 (OWR-2045-003), rank 817. Audit date: 2026-10-06 UTC.

## Verdict

**ACCEPT the scoped PDE/ODE equivalence theorem. The general problem remains UNSOLVED HERE.**

For every integer n ≥ 4 and real d > 0, let K_d be the closed algebraic-curvature cone defined by scal(R) ≥ d‖W(R)‖, with Hilbert–Schmidt curvature-operator norm. Preservation of K_d by the Hamilton ODE is equivalent to preservation under every smooth Ricci flow on every closed n-manifold, throughout the flow's smooth existence interval. Moreover, an ODE failure produces an initial smooth metric on S^n satisfying the condition everywhere whose Ricci flow violates it.

The submitted proof establishes this statement. No mathematical correction to its main theorem is required. The accompanying ESTIMATE_SUPPLEMENT.md expands the constant choices and jet argument to remove possible ambiguities; it does not change the frozen author packet. The converse is specific to this conformally covariant family, not a converse to the tensor maximum principle for arbitrary curvature cones.

This is an independent mathematical review, not a proof-assistant certificate, journal acceptance, claim of historical novelty, or exhaustive literature review. Exact computations supplement the written proof; they do not establish analytic existence or compact gluing.

## Artifact authentication and replay

The actual frozen archive was inspected and its bytes authenticated:

- File: RICCI_INVARIANT_CONES_30001006_AUTHOR_SAFE_FREEZE.zip
- Size: 17,241 bytes; 11 members
- SHA-256: c7b2700050482bec8b74874b61ed050c07b3a08e1a8d06eee52d794682b1d8c1
- MANIFEST.json: 1,442 bytes; SHA-256 aa66b61301537ca3f73388ae7505c802a5dfce6e67b628ee76926e3b15e6f51d

All ten manifest-listed content members match their recorded sizes and hashes. The full proof, source/overlap account, metadata, checkers, and saved results were read. Normal and optimized author-verifier runs passed. The author integrity harness reproduced its saved result, including four positive modes, twelve rejected package mutations, and six rejected mathematical-code mutations. No author member was edited.

## 1. Cone, covariance, and the analytic germ

K_d is closed, convex, O(n)-invariant, and contains the sectional-one operator I in its interior. Its smooth boundary consists of F_d = 0 with W ≠ 0. The remaining boundary locus is scal = 0, W = 0, with arbitrary traceless Ricci component.

The conformal identity has the correct coefficient and weights:

F_d(v^(4/(n−2))h) = v^(−(n+2)/(n−2)) [−a_n Δ_h v + F_d(h)v],

a_n = 4(n−1)/(n−2).

The Weyl norm scales as v^(−4/(n−2)); this statement is valid even at W = 0 and does not require differentiation there. The sign convention Δ = div grad agrees with the stated scalar-curvature transformation. Switching from full-tensor norm to curvature-operator norm merely changes the fixed d coefficient.

At a smooth boundary point R_*, the quadratic normal metric h has h(0) = δ, first and third metric derivatives zero, R_h(0) = R_*, and ∇R_h(0) = 0. These last assertions are compatible with differential Bianchi: the zero first covariant curvature derivative obeys the required identities, and an actual metric supplies the higher compatibility automatically.

Because h is analytic and positive definite near 0, its curvature and squared Weyl norm are analytic. Since ‖W_*(0)‖² > 0, the positive square root is analytic after shrinking the neighborhood. Thus F_d(h) is an analytic coefficient, with F_d(h)(0) = 0 and dF_d(h)(0) = 0.

The equation Δ_h v = a_n^−1 F_d(h)v is linear analytic. The hypersurface x_n = 0 is non-characteristic because its normal principal coefficient is h^{nn} > 0. Cauchy data v = 1 and ∂_n v = 0 are analytic. Cauchy–Kowalevski applies locally; it is not being misused as a smooth elliptic Cauchy well-posedness result. Positivity follows from continuity and v(0) = 1.

The 3-jet argument is valid. Cauchy data annihilate derivatives with zero or one normal index. The equation at 0 determines v_nn = 0. One differentiation of the equation, followed by the vanishing already obtained and dF_d(h)(0) = 0, determines v_nnk = 0 for every k. In normal coordinates h^{ij}(0) = δ_ij, so tangential differentiated terms vanish separately. This includes v_nnn. Hence v = 1 + O(|x|^4); multiplying h by v^(4/(n−2)) changes neither its metric 3-jet nor R(0), ∇R(0). The transformed germ has F_d identically zero.

**Accepted:** analytic boundary germ, full 3-jet preservation, curvature realization, and vanishing first curvature derivative. No smoothness of ‖W‖ at W = 0 is assumed in this step.

## 2. Compact gluing: all regions checked

Put the germ in geodesic normal coordinates. The germ g and unit-round background b obey g_ij x^j = b_ij x^j = x_i. Their cutoff convex combination g_ε remains positive definite and in this same radial gauge. The coordinate r therefore has |∇r| = 1, although no global distance-function claim is needed.

For fixed smooth cutoffs 0 ≤ χ ≤ 1, the bounds g−b = O(r²), ∂(g−b) = O(r), and ∂²(g−b) = O(1) imply uniform second-derivative bounds after interpolation on 2ε ≤ r ≤ 3ε. The inverse metrics are uniformly bounded after choosing the fixed chart small enough. Curvature, scalar curvature, and Weyl norm are consequently uniformly bounded. This justifies B independent of ε. Radial gauge and the Cartesian volume formula give Δr = (n−1)/r + O(r), uniformly, justifying a fixed A ≥ 0.

The barrier derivative is nonpositive. Multiplication of the lower bound on Δr by v_ε′ ≤ 0 reverses the comparison in exactly the direction needed: Δv_ε ≤ −M φ(r/ε). This is the crucial sign; it is correct in the author text.

Choose M once with a_n M > B, then ε small. The source integral is O(ε^n). The near region contributes O(Mε²) to 1−v_ε; the tail contributes O(Mε^n) times the integral of r^(1−n), hence O(Mε²) since n > 2. Thus 1/2 ≤ v_ε ≤ 1 for sufficiently small ε. There is no growing negative tail that threatens positivity.

Every region is covered:

1. r ≤ ε: g_ε = g and v_ε = 1 exactly. The prescribed curvature and all local derivatives are untouched.
2. ε < r < 2ε: g_ε = g, so F_d ≥ 0; the conformal Laplacian correction is nonnegative.
3. 2ε ≤ r ≤ 3ε: the only potentially negative metric-cutoff region. Here φ ≥ 1, F_d(g_ε) ≥ −B, and v_ε ≤ 1. The conformal numerator is at least a_n M−B > 0.
4. 3ε < r ≤ r_0/2: the metric is round, and Δv_ε ≤ 0. This covers the remainder of the source support and its full tail.
5. The fixed outer annulus: g_ε = b; v_ε−1 = O(ε²), while v_ε′ and v_ε″ are O(ε^n). After the fixed η cutoff, all derivatives through order two are O(ε²). Since F_d(b) = n(n−1) > 0, the conformal numerator remains strictly positive there. Its error is bounded by a fixed constant times ε², not by a constant depending inversely on ε.
6. Outside the chart: the metric is exactly round.

The smooth source cutoff is flat at its support endpoints. The radial conformal factor is constant near the center, so it is smooth there as a Cartesian function. The metric and conformal factors match the background on open neighborhoods of the outer seams. The resulting metric is smooth and positive definite on the already closed sphere. It is therefore complete and admits a smooth short-time Ricci flow.

**Accepted:** the local-to-compact extension lemma for these F_d conditions. It is not merely an asserted gluing theorem; the estimates above control both transition regions. The construction uses positive scalar-curvature room on the fixed outer round annulus, so it does not incorrectly demand a globally nonconstant superharmonic function on a closed manifold.

## 3. Laplacian cancellation and actual flow failure

In orthonormal moving frames, curvature evolves by ∂_t R = ΔR + 2Q(R). At the selected center, W_* ≠ 0 makes F_d differentiable. The spatial chain rule is

ΔF_d(R) = DF_d(R)[ΔR] + Σ_i D²F_d(R)[∇_i R, ∇_i R].

The Hessian term vanishes because ∇R = 0, not merely because F_d is locally constant. Since the germ also has F_d identically zero, DF_d(R_*)[ΔR] = 0. Thus the time derivative is 2DF_d(R_*)[Q(R_*)], and a strictly outward ODE velocity gives a strictly negative time derivative under a genuine short-time flow on S^n. Continuity keeps W nonzero for sufficiently small times, permitting this differentiation.

No full curvature Hessian or curvature Laplacian is being set to zero. That stronger claim would require extra compatibility and is unnecessary here. The submitted distinction is sound.

## 4. Nonsmooth boundary and equivalence

At R_0 with scal = W = 0, the tangent cone is exactly the set of V with scal(V) ≥ d‖W(V)‖. Indeed, K_d is invariant under adding any traceless-Ricci operator, so translating by R_0 identifies the tangent cone with K_d itself.

If Q(R_0) violates this condition, scal(Q(R_0)) = |Ric(R_0)|² ≥ 0 forces W(Q(R_0)) ≠ 0. Let U be its unit direction. Then

R_ε = R_0 + εI + [n(n−1)/d] εU

lies on the smooth boundary. Since W(R_ε)/‖W(R_ε)‖ = U exactly, continuity of the polynomial Q gives

DF_d(R_ε)[Q(R_ε)] → scal(Q(R_0)) − d‖W(Q(R_0))‖ < 0.

Thus every apex violation yields a smooth-boundary outward witness. The convex tangent-cone criterion applies to the locally Lipschitz polynomial Q. Its use is local along finite-time trajectories; no global-in-time existence of every quadratic ODE solution is needed. Conversely, ODE tangency implies PDE preservation by Hamilton's tensor maximum principle on closed manifolds. All its structural cone assumptions hold.

**Accepted:** the apex reduction and the claimed iff. The factor 2 in the PDE changes the speed, not tangency or the sign of failure.

## 5. Remaining problem and imported dependencies

The equivalence does not evaluate the algebraic extrema μ_n or β_n. The interval nβ_n ≤ d ≤ (n−2)/μ_n in the author packet is an imported consequence of the separate rank-815 ODE criterion. This audit checks the bridge and the elementary c = 2n(n−1)/d² conversion; it does not replay the rank-815 proof or its five approaches. Those archives were not available in this audit's current filesystem.

In particular, the claimed threshold n_0 = 12 and universal global Weyl-cubic bounds are not established. At n = 12, the stated remaining β_12² ≤ 55/36 bound is not proved by these checks. The bridge closes a logical PDE-to-ODE gap for this family; it does not solve the classification.

## 6. Source verification and limits

The 2008 primary PDF was freshly retrieved from [EMS Press](https://ems.press/content/serial-article-files/46179): 422,818 bytes, SHA-256 70d07d22627a077dce6979e9f142b3d79515dbddb184d5c341b0fbf4d2879363. Page 1942 was rendered and visually inspected. Both the preservation theorem and its necessity conjecture contain closure bars. The closed-cone scope is correct.

[Richard–Seshadri, Noncoercive Ricci flow invariant curvature cones](https://arxiv.org/pdf/1308.1190), Definition 1.5, Remark 1.6, Theorem 1.7, and Remark 1.8 were read. They support the ODE tangency/maximum-principle conventions and explicitly distinguish literal PDE preservation from their definition. They do not supply the present converse.

[Tataru course notes by Ning Tang](https://math.berkeley.edu/~ning_tang/files/notes/graduate/Math222B_Spring2023.pdf), Theorem 13.10 and its non-characteristic definition, were checked. The analytic-coefficient, analytic-data hypotheses hold in the present application.

[Branca–Catino–Dameno–Mastrolia](https://link.springer.com/article/10.1007/s10455-025-09996-x), equations (2.9)–(2.11), confirms the modified scalar-curvature transformation. The gluing proof was checked directly rather than attributed to that source.

[Xu, preprint v1](https://arxiv.org/html/2412.13633v1), Conjecture 1 and Theorem 1.1, were read in the current rendering. They give a partial near-spherical parameter range, not the target a = 0 endpoint. At n = 12 the displayed lower endpoint is 35/12. The [published landing page](https://link.springer.com/article/10.1007/s12220-025-02158-2) was opened; no fresh full version-of-record body review is claimed. This is bounded source checking, not proof that no later complete result exists.

The three full corpus files and rank-815 archives were unavailable. Their hashes and record-review claim in the frozen PUBLIC_METADATA.json are **historical author-reported metadata, not freshly replayed corpus verification**. Current full-corpus parsing, exact-record serialization, and prior-audit replay are NOT_RUN. No private corpus content or copied source documents are included in this audit package.

## 7. Independent executable checks

The separate independent_checks.py uses all symmetric pair-matrix generators followed by Bianchi projection in dimensions 4 and 5. It verifies 39,751 normal-metric-jet components across 76 spanning generators, supplementing the author's three examples. It also checks Cauchy-data jet recursion, the possible fourth-jet change, radial signs and ε² tail algebra, the norm-Hessian term, and an abstract apex/smooth-boundary limit.

Four negative controls demonstrate failure when the coefficient has a nonzero constant term, a nonzero first derivative, the radial derivative sign is reversed, or the curvature first jet is nonzero. The CK recursion is an exact local polynomial diagnostic, not a computational proof of CK solvability for variable coefficients. The apex check tests the scalar/norm tangent algebra, not Hamilton Q on arbitrary curvature tensors.

The audit package has its own external manifest anchor and fail-closed verifier. Integrity checks provide byte accountability, not mathematical certification. No publication, remote mutation, or outreach was performed.
