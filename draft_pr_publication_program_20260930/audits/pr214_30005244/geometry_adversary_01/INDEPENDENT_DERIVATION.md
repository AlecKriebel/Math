# Independent geometric and pole certificate — PR214 / 30005244

This derivation was made after freezing PLAN_01.md, and after Root's native-custody clearance. It does not rely on earlier review verdicts or on the submission's executable controls. It verifies a mathematical theorem, not historical priority or an administrative release.

## 1. Normalization and the intrinsic ball space

Let N be convolution with (4π|x|)^(-1), and let L=-grad div N on the whole-space complex Hilbert space. Fourier transformation gives the real symmetric multiplier ξξᵀ/|ξ|². Thus L is an orthogonal projection, and D=L-I/3 is bounded selfadjoint with form bounds -I/3 and 2I/3. Restricting the distributional kernel to x≠0 gives K0=(I-3eeᵀ)/(4πr³); the omitted delta term is +Iδ0/3. Consequently the zero-diagonal scheme compares with Sκ=Aκ-I/3, not Aκ. This normalization agrees with the complete OWR operator and matrix definitions and with CDN (3.39) and (3.42).

First work on H_B=L²(B;C³), B the open unit ball. The closed subspace grad H¹(B) is closed because the gradient norm on potentials modulo constants is equivalent to the H¹ quotient norm by Poincare. Within it, solving the Dirichlet variational problem splits any potential into H0¹ plus a weakly harmonic H¹ potential, orthogonally in gradient norm. Therefore

H_B = grad H0¹(B) ⊕ grad H_harm¹(B) ⊕ (grad H¹(B))⊥.

For u=grad φ with φ∈H0¹, its zero extension is the whole-space gradient of the zero-extended H¹ potential; L fixes it. For u in the last summand, its zero extension has distributional divergence zero: test against the restriction of every compact smooth whole-space scalar function. L annihilates it. These arguments impose the weak normal-flux condition automatically and do not assume a pointwise boundary trace for an arbitrary L² vector.

For a solid spherical harmonic Hℓ=r^ℓYℓ, ℓ≥1, distributional divergence of its zero-extended gradient is -ℓYℓδ∂B. The Newton single-layer potential with density Yℓ has the form c r^ℓYℓ inside and c r^(-ℓ-1)Yℓ outside. Continuity and the normal-derivative jump -(2ℓ+1)cYℓ=-Yℓ give c=1/(2ℓ+1). Hence A0 grad Hℓ=ℓ/(2ℓ+1) grad Hℓ, with a positive sign. Orthogonality follows from Green's identity. Completeness of the spherical-harmonic trace expansion in H^(1/2)(∂B), equivalently convergence of harmonic expansions in Dirichlet energy, supplies all of the middle gradient subspace. The squared Dirichlet energy of an individual mode is ℓ||Yℓ||². No unlisted harmonic sector is left.

It follows that σ(A0) is {0,1} together with ℓ/(2ℓ+1), ℓ≥1, and its accumulation point 1/2. Thus S0 has precisely three zero modes, the constant vectors. The next shifted harmonic value is (ℓ-1)/(3(2ℓ+1)); it equals 1/15 at ℓ=2 and increases since successive differences are 1/((2ℓ+1)(2ℓ+3)). All remaining spectral values are at least 1/15 from zero. On |z|=1/30, ||(z-S0)^(-1)||≤30. This rank-three statement belongs to the intrinsic ball space. Extending S0 by zero to all of L²(R³) before taking the zero-mode contour would invalidate it by adding infinitely many zero modes; the submitted proof explicitly avoids that error.

## 2. Independent dynamic expansion and finite-frequency bounds

Expand gκ(r)=Σ_(n≥0)(iκ)^n r^(n-1)/(4π n!). For a radial monomial r^p,

D²r^p = p r^(p-2) I + p(p-2) r^(p-2) eeᵀ.

Combining this Hessian term with the separately indexed -κ²gκ I term gives, after factoring (4πr³)^(-1), the normalized coefficients

I: i^n (n-1)²/n!,     eeᵀ: -i^n(n-1)(n-3)/n!.

The order-one term vanishes. Orders two and three give

Cκ = κ² C2 - iκ³ J/(6π) + Eκ,

where C2 has kernel -(I+eeᵀ)/(8πr), while Ju is the constant field ∫_B u. In particular, the cubic imaginary term has a minus sign for the source's e^(+iκr) convention. The calculation comes directly from radial monomials, independently of multiplying out the submitted closed kernel; the 73 exact finite controls check both derivations against each other and check the ensuing rational inequalities.

For |κ|≤1/2 and r≤2, put z=κr. In each scalar numerator the absolute coefficient after order three is at most n²/n!. The exact tail identity Σ_(n≥4)n²/n!=2e-9/2 is less than one. A rational certificate is e≤8877691/3265920<11/4, obtained by summing through n=8 and bounding the remaining ratios by 1/10. Hence each scalar remainder is bounded by |z|⁴. Since ||I||F+||eeᵀ||F=√3+1<3, the matrix remainder kernel is bounded by 3|κ|⁴r/(4π).

The Frobenius numerator of I+eeᵀ has squared norm six. Also ∫_(B×B)r^(-2)≤|B|∫_(|z|≤2)|z|^(-2) dz=32π²/3. Thus ||C2||HS²≤1. The remainder estimate and r≤2 give ||Eκ||HS²≤4|κ|⁸. On the constant-vector space, J=|B|I, and on all H_B its norm is |B|=4π/3. Therefore ||J/(6π)||=2/9. Altogether

||Cκ|| ≤ |κ|²(1+(2/9)|κ|+2|κ|²) ≤ (29/18)|κ|² < 2|κ|².

These bounds are valid for complex κ in the stated disk; the trace-sign step below uses real positive κ.

## 3. A true nonreal ball eigenvalue at κ=1/10000

Let ε=||Cκ||≤1/60. The resolvent Neumann estimate on |z|=1/30 is at most 60. The contour length is 2π/30, so the resolvent identity gives ||Pκ-P||≤(1/30)·60·ε·30=60ε≤120|κ|²=:η. If η≤1/2, the perturbed range has rank three. The orthogonal projection P restricts to an isomorphism from ran Pκ to the constant-vector space V, and its inverse is v↦v+Γκv with Γκv∈V⊥. This follows from ||(I-P)w||≤η||w|| and ||Pw||≥(1-η)||w||. Therefore ||Γκ||≤η/(1-η)≤240|κ|². Orthogonality of Pκ is unnecessary.

In these coordinates the invariant restriction of Sκ is Hκ=P Sκ(I+Γκ)|V. Because PS0=0, its difference from κ²PC2|V-iκ³PJ|V/(6π) has norm at most 2|κ|⁴+(2|κ|²)(240|κ|²)=482|κ|⁴. C2 is selfadjoint, so its compressed trace is real. Taking a trace on the three-dimensional normalized constant space yields

Im tr Hκ ≤ -(2/3)κ³+1446κ⁴.

At the exact rational κ=1/10000, ε≤1/50000000, η≤3/2500000, and the trace upper bound is exactly

-7831/15000000000000000 < 0.

The finite-dimensional trace is the sum of the three eigenvalues with algebraic multiplicity. At least one has negative imaginary part (indeed at most one third of this upper bound). These are actual eigenvalues of the bounded continuum operator on its invariant Riesz range, not approximate numerical values or frequency-plane resonances. Rank three of the Riesz projection makes the cluster finite; a chosen nonreal eigenvalue is isolated with finite algebraic multiplicity. It lies outside every real static interval, including J_lat. No simplicity, semisimplicity, or rotational-degeneracy assertion is needed.

## 4. Compact support and exact grid nodes

Choose any enumeration q_k of Q³∩closure(B), with every point appearing. For j≥1 let U_j=∪_(k≥1) B(q_k,2^(-j-k-4)), F_j=closure(B)\U_j, and Ω_j=F_j∪{0}. The set U_j is open, so F_j is compact. Since each rational point in closure(B) lies in its own deleted ball, F_j contains no rational point. Density of Q³ precludes any nonempty open subset of F_j. Adding one point preserves empty interior and compactness.

Using subadditivity, without assuming the balls disjoint,

|B\F_j| ≤ |U_j| ≤ (4π/3)Σ_(k≥1)2^(-3j-3k-12)
          = |B|·2^(-3j-12)/7.

This is strictly below |B| for every j≥1. Thus F_j has positive volume. The radii shrink with j, so F_j increases; the measure deficit tends to zero. Consequently the indicators converge to 1_B almost everywhere, apart from a null set and the sphere, and strongly as multiplication operators on L². The claim does not require the set-theoretic union of F_j to be all irrational points.

The enumeration contains 0 at some finite k0. Its deleted ball gives dist(0,F_j)≥2^(-j-k0-4)>0. Hence the restored anchor is isolated and has zero volume. It changes membership sampling but does not change the continuum volume operator or its spectrum.

For each n≥1 every node of n^(-1)Z³ is rational and 0 is a node, so Ω_j∩n^(-1)Z³={0}. There are three vector degrees of freedom, and the only 3-by-3 block is the omitted diagonal block. Thus the actual matrix is exactly zero, not just a small approximation. No singular kernel is evaluated at the anchor.

This is a universal statement over n for each fixed j, before the spectral choice of j. It even holds for any positive rational mesh with zero translation. It does not say that every translated grid has one node: the rational translate (1/2,0,0)+Z³ has no anchor and no support nodes, hence the zero-dimensional matrix. The manuscript restricts its negative theorem to a_h=0 and h=1/n, so that boundary case is a scope check rather than a defect.

## 5. Persistence under small volume removal without false static norm control

Fix κ=1/10000 and choose the nonreal ball eigenvalue λ obtained above. Take an isolating disk with nonreal closed disk (radius less than |Im λ|/2 and small enough to isolate λ). Now extend each support operator by zero to H=L²(R³;C³); at this stage the contour avoids zero, so the extra zero eigenspaces are harmless.

Let M_j and M_B be the masks. Then M_j→M_B strongly. Since D is bounded, B_j=M_jDM_j→B_B=M_BDM_B strongly. These are selfadjoint, with common form and spectral bounds [-1/3,2/3], including their zero complements. There is no assertion that ||B_j-B_B||→0; in general small removed measure does not give such a conclusion for this singular part.

The dynamic kernels Rκ are square-integrable on B×B, since they are O(1/r) and dimension is three. Dominated convergence applied to |Rκ(x-y)|F² times the changing product masks gives ||C_j-C_B||HS→0. This controls only the compact correction.

Here is the independently checked abstract step. For z outside the common real interval, R_j(z)=(z-B_j)^(-1) has a uniform bound. The resolvent identity gives strong convergence to R_B(z), uniformly on a compact contour on each fixed vector. Because B_j are selfadjoint, the adjoints converge strongly as well. Finite-rank approximation then gives norm convergence of R_j(z)C_j to R_B(z)C_B. The factors I-R_jC_j are invertible on the contour for all large j by the Neumann estimate against the limiting inverse.

Write F_j=R_jC_j and G_j=(I-F_j)^(-1)F_j. Then G_j→G_B in norm and these operators are compact. The full resolvent is R_j+G_jR_j. The term R_j is analytic throughout the nonreal disk and integrates to zero. For the remaining term,

||G_jR_j-G_BR_B|| ≤ ||G_j-G_B||·||R_j|| + ||G_B(R_j-R_B)|| →0.

The second convergence specifically uses strong convergence of adjoints and compactness of G_B. Without that adjoint fact, this right-product argument would be invalid. All estimates are uniform on the compact contour. The Riesz projections consequently converge in norm. Once their difference has norm below one, their restrictions to each other's ranges are injective, so their finite positive ranks agree. Thus every sufficiently large finite j gives a nonreal eigenvalue for F_j in that disk.

Choose any one such finite j. This choice is made once and does not depend on n. Since restoring 0 changes no volume operator, Ω=Ω_j has the continuum nonreal eigenvalue while all of its matrices on n^(-1)Z³ are zero. The support index is existential: the proof gives no computable threshold, no explicit eigenvalue location, and no certificate for a particular finite enumeration prefix. None is claimed.

## 6. Relation to geometric consistency and the source question

The anchor has a fixed deleted neighborhood for the chosen j. For all sufficiently small h=1/n, its occupied cube lies inside that neighborhood, and its intersection with Ω has volume zero. Thus |Ω_h△Ω|=|Ω|+h³ eventually; its limit is |Ω|>0. Condition (G) fails. This does not refute the regular-particle theorem.

For a bounded set with null boundary, any discrepancy between a point and its cell center is contained in a boundary neighborhood of radius at most √3h. Boundedness and continuity from above of volume make that neighborhood shrink to zero volume, uniformly over translations. This independently validates the manuscript's inclusion of bounded Lipschitz or null-boundary particles under (G).

OWR pp. 2580–2582 states the compact-set physical setup, the omitted-diagonal matrix, the I/3 shift and the observed off-interval approximation question. Its Section 4 asks for an accurate description and proof of the observed behavior; it does not explicitly quantify over every irregular measurable compact support or require a necessary-and-sufficient geometric criterion. Therefore the strongest responsible reading is: a sufficient affirmative theorem for (G), plus a valid obstruction to extrapolating it to unrestricted compact point-membership masks. The pathology is mathematical, not evidence of failure for regular physical particles. No novelty or priority follows from this proof check.
