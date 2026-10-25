# Independent derivation, package review 04

Written 2026-10-13 UTC from the current TeX alone and first principles, before opening prior package verdicts, prior independent derivations, or root mathematical audit conclusions. External theorem statements below are obligations to verify against primary sources, not assumed established by this review's finite computations.

## Exact target and assumptions

Let X be the two-orientation unit simple real four-vectors in Λ⁴R¹², and C their convex hull. The claim is that C has no finite spectrahedral shadow with arbitrary affine equations, finite matrix size and auxiliary variables. The reduction uses the external no-lift theorem for normalized **complex** Sep(3,3). Deductions are an existential failure of affine SOS of degree at most one modulo the **full real vanishing ideal**, a rational coefficient unnormalized failing functional, and an existential constant closed comass-one four-form without any finite pointwise/local norm completion. Explicit coefficients, computable exact comass, rational normalized coefficients, minimal ambient dimension, and global priority are not target claims.

## Geometry and signs

1. On a real four-plane with an oriented orthonormal frame, the restriction of the Kähler form has two skew blocks with moduli at most one. The value of Φ=ω²/2 is their signed product. Attaining +1 forces both singular moduli to be one. Equality in the contraction estimate for every vector forces Jv to belong to the plane. The orientation is the positive complex orientation. Conversely (a,Ja,b,Jb) for a complex orthonormal pair evaluates to +1. A convex combination of unit simple vectors with average Φ=1 must consist only of maximizers: every summand has Φ≤1. Thus C∩{Φ=1} is exactly the convex hull of complex two-plane volumes.

2. Put u_j=(e_j−if_j)/√2. For a complex coordinate vector a, its underlying real vector is (â+conj(â))/√2, and Ja=i(â−conj(â))/√2; hence a∧Ja=−i â∧conj(â). Then
   a∧Ja∧b∧Jb=â∧b̂∧conj(â)∧conj(b̂): the scalar (−i)²=−1 is canceled by one swap of one-vectors. This fixes the **positive** projector normalization.

3. The map A(H)=Σ H_IJ u_I∧conj(u_J), for I,J pairs, is real when H is Hermitian. Conjugation exchanges I,J and the exchange of two exterior degree-two factors has sign +1. The (2,2) basis has 15·15=225 complex coordinates. Thus no kernel exists on the 225-dimensional real Hermitian domain. Replacing u by w=e−if inserts 1/4, so the usual real Hermitian basis yields rational real coefficients. The diagonal basis vector maps to e_i∧f_i∧e_j∧f_j; off-diagonal terms have no diagonal four-coordinate component. Therefore Φ(A(H))=tr H. Projectors zz* of unit simple complex bivectors give exactly the complex oriented plane generators. A unit decomposable bivector admits a complex orthonormal factorization by Gram–Schmidt and phase adjustment. So F=A(K), with K the trace-one mixed simple fermion projector body.

4. In C⁶=U⊕Z with dim U=dim Z=3, Λ²C⁶=Λ²U⊕(U∧Z)⊕Λ²Z. For H=Σ λ_t z_tz_t*, λ_t>0, tr(P_D H)=Σ λ_t ||P_Dz_t||². Zero implies that **each** generator lies in B=U∧Z; positivity of each summand is indispensable. Merely demanding support or imposing Q=0 outside F would not suffice.

5. Write a=u_a+z_a and b=u_b+z_b. If a∧b is nonzero and mixed, u_a∧u_b=z_a∧z_b=0. Each projected span has dimension at most one, and neither can have dimension zero (otherwise the original wedge lies purely in the other block and vanishes). Choose nonzero generators x∈U,y∈Z of those two lines. Then a=αx+γy, b=βx+δy, and a∧b=(αδ−βγ)x∧y with nonzero coefficient. This proves precisely the rank-one tensor/simple mixed bivector equivalence without a dimension-specific algebraic assumption. The mixed basis map T:U⊗Z→U∧Z is unitary because its basis is orthonormal. Unit simple mixed bivectors may be written with both factors of norm one by redistributing modulus/phase. Under T, their projectors are xx*⊗yy*. Thus K∩{tr(P_D H)=0} is exactly the normalized complex Sep(3,3).

6. Q=(ω_U²+ω_Z²)/2 reads precisely the diagonal pure-block projector coordinates, so Q(A(H))=tr(P_D H). The affine section C∩{Φ=1,Q=0}, **inside C**, is A(Sep(3,3)). Q need only be nonnegative on F. The two equations alone are not a separability description. An arbitrary finite lift of C can be intersected with preimages of both equations. A real linear left inverse to A exists on its image and extends to all of Λ⁴R¹² by choosing a complement. Applying it and T* gives a finite lift of Sep(3,3). Fawzi's no-lift theorem would therefore forbid the proposed lift of C. If the external theorem uses Hermitian PSD cones, this still forbids real symmetric lifts, because a real symmetric PSD matrix is a Hermitian PSD matrix, and conversely Hermitian LMIs can be realified with finite doubling.

## Moment obstruction and rationality

7. N=binomial(12,4)=495. For compact nonempty X⊂S^(N−1), let J₂ be the finite-dimensional full ideal component of degree at most two. Moment matrices M of size N+1=496 obey M≽0, M₀₀=1, and L_M(J₂)=0. The sphere relation 1−Σ p_i² belongs to J₂, so tr M=2. PSD then bounds each entry and the feasible set is closed, bounded and nonempty. It and its first-coordinate projection T are compact. Rank-one (1,p)(1,p)^T give conv X⊂T.

8. If every δ−c·p were an affine SOS on X, its degree-two discrepancy would belong to J₂. Applying L_M would give δ−c·x=Σ a_j^T M a_j≥0 for every x∈T. All supporting halfspaces would force T⊂conv X. Equality would give a finite exact lift, contradicting step 6. This implication does not invoke SDP dual attainment, Slater, or closure of a shadow. No description of a quadratic generating subset of the full ideal is silently substituted for J₂.

9. Therefore some x∈T\C exists. Closed convex C admits a strict separating c with gap g=c·x−h_C(c)>0. The sphere gives |h_C(c+d)−h_C(c)|≤||d||; moreover M≽0 and trace conditions imply ||x||≤1 by Schur complement, although only finite ||x|| is necessary. Thus gap perturbation is at most (||x||+1)||d||. Pick rational c′ sufficiently close, e.g. with norm distance <g/[2(||x||+1)]. The same x violates its supporting bound. c′ is nonzero because zero cannot have a strict gap. If δ−c′·p had an affine SOS, the feasible lifting matrix for x would contradict this strict inequality. This proves rational **unnormalized** coefficients only, without rational δ or rational c′/δ.

## Completion implication and optional converse

10. Signed coordinate wedges span Λ⁴R¹² and belong to X. For nonzero ℓ, δ=max_X ℓ=max_X |ℓ|>0. The constant φ=ℓ/δ is closed and has comass one. If finitely many pointwise linear four-forms ψ_j completed the squared mass on all simple four-vectors, evaluation on unit simple p gives φ(p)²+Σψ_j(p)²=1. Then
    1−φ(p)=½(1−φ(p))²+½Σψ_j(p)².
    Multiplying by δ yields a forbidden affine SOS for δ−ℓ. Any differential-form completion on a neighborhood has a pointwise linear completion at each point; hence it cannot exist for this constant φ. Smoothness or closedness of the auxiliary ψ_j is unnecessary to the obstruction. The exact Question 6.5 quantifiers and notion of norm completion remain primary-source verification obligations.

11. Optional converse: Write 1−φ(p)=||a+Bp||² on X. Comparing p and −p gives 4a^TBp=−2φ(p), and spanning yields B^Ta=−φ/2. Averaging gives ||a||²+||Bp||²=1. At a maximizer p₀, Bp₀=−a; at −p₀, 2=||2a||², hence ||a||²=1/2. Then 2||P_(a⊥)Bp||²=2(1/2−φ(p)²/2)=1−φ(p)². Scaling extends the homogeneous norm identity to all simple vectors, including zero. No smooth selection from independently existing pointwise decompositions is being asserted.

## Boundary/falsification obligations

- Reverse complex orientation gives Φ=−1, hence is excluded; reversing a complex bivector phase leaves its projector unchanged and its complex real volume unchanged.
- Two linearly dependent factors give zero wedge and cannot be unit generators. Pure-block wedges with vanishing mixed projection do not enter K₀.
- A nonzero mixed rank-two matrix is not simple; all complex mixed minors must vanish. Non-real phases must still yield real coefficients in A.
- Q is not a global supporting form: pure-orientation signs outside F may make it negative. This does not invalidate the simultaneous section argument.
- The quadratic projective Grassmann embedding p↦pp^T loses orientation and supplies a different body; its prior no-shadow results cannot be equated with step 6.
- Unprojected spectrahedron obstructions alone do not establish arbitrary no-lift conclusions.
- All theorem-level nonrepresentability remains conditional on the cited primary external theorem; finite arithmetic checks prove only their actual coordinate identities and hostile boundaries.

Initial independent mathematical verdict: no internal proof gap found. Primary-source interfaces and verification/publication claims have not yet been accepted or read from prior verdicts.
