# Five approaches to high-frequency coercivity

Problem 30003533 / OWR-15576-002. Author investigation, 8 October 2026.
Status: **unsolved after five substantive approaches**. The results below are scoped auxiliary results, not a solution or a claim of historical novelty. They are proved here; previously published ingredients are identified in SOURCES.md. A separate mathematical audit has not yet taken place.

## 0. Target, notation, and quantifier discipline

Let Ω− be a bounded obstacle in R^d, d=2 or 3, with connected exterior Ω+=R^d\overline{Ω−}; Γ=∂Ω− and n points into Ω+. For k>0, the outgoing fundamental solution is Φ_k(x,y)=i H_0^(1)(k|x−y|)/4 in dimension two and e^(ik|x−y|)/(4π|x−y|) in dimension three. Put

S_k v(x)=∫_Γ Φ_k(x,y)v(y)ds_y,
D′_k v(x)=∫_Γ ∂_{n(x)}Φ_k(x,y)v(y)ds_y,
A_k=(1/2)I+D′_k−ikη S_k, η>0 fixed.

The Hilbert space is complex L²(Γ,ds), with inner product (v,w)=∫v overline(w). Define

β_Γ,η(k)=inf_{||v||=1}|(A_kv,v)|.

The primary question concerns positivity of β at all sufficiently large frequencies, possibly with polynomial loss, on an appropriate class of strongly nontrapping nonconvex domains, explicitly including smooth star-shaped domains. The precise proposed polynomial property is

(P) There are c>0, α≥0 and k0>0 such that β_Γ,η(k)≥c k^(−α) for every real k≥k0.

Here Γ and η are fixed before k varies; c, α and k0 may depend on them. Neither constants uniform over geometries nor a bound for all positive η is asserted. One may additionally ask whether η can be selected depending on Γ, or whether every η above a geometry-dependent threshold works. The report does not settle these parameter variants. Its phrase “strongly nontrapping” is not formally defined. A concrete core testing class used below is smooth strictly star-shaped obstacles, i.e. (x−x0)·n(x)≥a>0. This is a stated restriction, not a claim that it is the entire intended class.

The display on source p.2085 leaves k free on the right after a liminf as k→∞ and introduces an unused γ. It cannot literally be used as a quantified estimate. Property (P) is the explicit polynomial-rate reading of the preceding prose. Equivalently, liminf_{k→∞} k^α β_Γ,η(k)>0 after adjusting c; this equivalence follows immediately from the definition of liminf. The report's later informal kernel expression also drops the prime and the k in the coupling; equation (2), not that mnemonic, fixes our operator.

All results concern this modulus coercivity, unless a stronger real-part inequality is explicitly assumed. Invertibility, an inf-sup estimate, coercivity after multiplying the equation by a different operator, and coercivity of the star-combined formulation are different assertions.

## 1. Approach 1: repair the normal Morawetz multiplier with a variable weight

### Aim

The published convex proof uses a vector field equal to a positive constant times n on Γ and having nonnegative symmetric derivative. Instead of merely reusing its known constant-weight obstruction, we tried to remove that obstruction by allowing a positive boundary weight a(x), possibly depending on k. The following differential calculation shows exactly why this enlargement still fails at a negatively curved boundary point.

### Proposition 1.1 (variable-weight obstruction and quantitative defect)

Let Γ be C² near p, let Z be C¹ up to Γ from either side, and suppose Z=a n on Γ with a C¹ positive scalar function. For every unit tangent ξ at p,

ξ·DZ(p)ξ=a(p) ξ·D_ξ n(p).

Consequently, if the outward shape operator has a direction with ξ·D_ξ n(p)=−κ<0 and a(p)≥a0>0, then the least eigenvalue of sym DZ(p) is at most −a0 κ. A nonnegative symmetric derivative in the adjacent open region is impossible by continuity. Even the relaxed bound sym DZ≥−ε(k)I fails whenever ε(k)<a0 κ.

Proof. Differentiate Z=a n along a boundary curve with tangent ξ. Then D_ξ Z=(D_ξ a)n+aD_ξ n. Taking the scalar product with ξ removes the first term because ξ·n=0. A quadratic form equals that of its symmetric part. Rayleigh's variational inequality gives the eigenvalue estimate. The boundary value is a limit of values from the open side, so a lower bound in that side persists at p. This proves every assertion. ∎

This does not rule out all Morawetz methods: tangential boundary terms, matrix/pseudodifferential multipliers, or controlled integrated negative terms are outside these hypotheses. Nor does it prove noncoercivity of A_k.

### Proposition 1.2 (an explicit smooth strictly-star-shaped obstruction)

In R² take Γ parametrized by x(θ)=r(θ)(cosθ,sinθ), r(θ)=1+(1/4)cos3θ, and take its radial interior. Γ is a smooth embedded boundary, strictly star-shaped with respect to a ball about the origin, and nonconvex. At θ=π/3 its outward curvature, with the convention D_t n=κt, is −8/3.

Proof. Since r≥3/4, the polar parametrization is injective modulo 2π and regular; the curve and radial interior are smooth. The outward unit normal is (r e_r−r′e_θ)/sqrt(r²+(r′)²), so

x·n=r²/sqrt(r²+(r′)²)≥9/(4sqrt34)>3/8.

The last inequality follows from 36>34. The support-normal criterion for star-shapedness with respect to a ball therefore gives the claim, with any ball radius at most 3/8. For completeness, the criterion here follows by following segments from a point z with |z|≤3/8: at any boundary crossing their outward component is (x−z)·n>0. A segment starting inside cannot exit and then re-enter, since a re-entry would require a nonpositive outward component. Thus every segment from z to an interior point stays inside.

Writing c=cos3θ, the curvature numerator is

r²+2(r′)²−rr″=17/8+(11/4)c−(1/2)c².

At c=−1 it is −9/8, while r=3/4 and r′=0, giving κ=(−9/8)/(27/64)=−8/3. Negative curvature excludes convexity. ∎

Applied at that point, Proposition 1.1 forces a bulk negativity defect at least 8a0/3, independent of frequency. Letting the weight itself tend to zero can avoid this numerical obstruction, but then the boundary coercivity term also degenerates and the PDE identity must be re-estimated; no such estimate has been established here.

### Geometric control against misusing the known two-flat-face counterexample

Suppose there are points p=(a1,y), q=(a2,y), a1<a2, with n(p)=e1 and n(q)=−e1. There is no point x0 for which both (p−x0)·n(p)>0 and (q−x0)·n(q)>0: the first forces x0,1<a1 and the second x0,1>a2. Thus the facing-flat-patch geometry of the published smooth nontrapping example cannot simply be called strictly star-shaped. This observation does not exclude other counterexamples.

Remaining gap for Approach 1: construct an admissible multiplier outside this normal positive-weight class, and prove the needed boundary quadratic-form estimate with all high-frequency error terms controlled.

## 2. Approach 2: deform a coercive convex obstacle

### Aim

Transfer the known convex estimate by operator-norm continuity under a smooth deformation. We prove a frequency-explicit continuity estimate, rather than assume a continuity neighborhood uniform in k.

### Proposition 2.1 (three-dimensional geometric perturbation estimate)

Let M be a fixed compact C² surface without boundary, with a fixed reference measure dμ. Suppose X_t:M→R³, 0≤t≤t*, is a C¹ path in C² embeddings bounding obstacles, with uniformly nondegenerate induced metrics, uniformly controlled C² norms and C² t-derivatives, and positive surface Jacobians J_t bounded above and below. The normals are chosen continuously. Write Γ_t=X_t(M) and let

(U_t f)(p)=J_t(p)^(1/2) f(X_t(p)).

This is unitary from L²(Γ_t) to L²(M,dμ). For fixed η>0, put B_t(k)=U_t A_{Γ_t,η}(k)U_t^(−1). There is a finite C depending on the family, reference surface and η, but not on k≥0 or t, such that

||B_t(k)−B_0(k)||≤Ct(1+k²).

Proof. Fix a finite atlas and a reference distance ρ(p,q) comparable with coordinate distance near the diagonal. Compactness and embedding imply uniformly in t that r_t=|X_t(p)−X_t(q)| is comparable with ρ near the diagonal, and is bounded away from zero off a fixed diagonal neighborhood. The mean-value theorem gives |∂_t r_t|≤Cρ near the diagonal, and the corresponding uniform bound away from it. All estimates below can therefore be written with ρ, extended to a positive bounded reference separation off the diagonal.

Set a_t=n_t(p)·(X_t(p)−X_t(q)). Taylor expansion in surface coordinates, using n_t(p)·DX_t(p)=0, gives |a_t|≤Cρ². Differentiating the orthogonality identity gives ∂_t(n_t·DX_t)=0. Differentiating the Taylor expansion therefore also gives |∂_t a_t|≤Cρ². These are uniform because the path and its t-derivative have bounded C² norms. Both J_t^(1/2) and its t-derivative are bounded.

The pulled-back S kernel is

J_t(p)^(1/2) J_t(q)^(1/2) e^(ikr_t)/(4πr_t).

Differentiating in t bounds its absolute value by C(ρ^(−1)+k). The pulled-back D′ kernel, with the same Jacobian factors, is

e^(ikr_t)(ikr_t−1)a_t/(4πr_t³).

Differentiate the exponential, the factor ikr_t−1, a_t, the denominator, and the Jacobian factors separately. The above estimates bound their sum by

C(ρ^(−1)+k+k²ρ).

Multiplication of the S difference by kη thus gives the combined bound

|∂_t K_t(p,q)|≤C[(1+k)ρ^(−1)+k+k²+k²ρ]≤C′(1+k²)(1+ρ^(−1)).

On a compact two-dimensional surface, sup_p∫(1+ρ(p,q)^(−1))dμ(q) and its version with p,q exchanged are finite: in a chart the singular integral is bounded by C∫_0^ε r^(−1)r dr. Integrating the derivative from 0 to t and applying the Schur test proves the claimed operator-norm bound. The identity half is unchanged by unitary transport. The weak diagonal singularity causes no omitted distributional term because the separate jump term is already exactly (1/2)I. ∎

### Corollary 2.2 (coercivity only on a shrinking deformation scale)

For bounded operators B,C on the same Hilbert space, |β(B)−β(C)|≤||B−C||. Indeed, the reverse triangle inequality for each unit vector gives one side, and interchange gives the other. Consequently if β(B_0(k))≥c0 for k≥k0, then

β(B_t(k))≥c0−Ct(1+k²).

In particular β(B_t(k))≥c0/2 whenever t≤c0/[2C(1+k²)]. ∎

The conclusion is genuine geometric stability for a frequency-dependent family. It is not a fixed-domain high-frequency theorem. A fixed t>0 eventually violates this sufficient inequality. In addition, sufficiently small C² deformations of a uniformly convex surface remain convex, so this transfer alone does not even guarantee a nonconvex example in its shrinking neighborhood. Neither obstacle is repaired by saying merely “continuity.”

Remaining gap for Approach 2: obtain a significantly different comparison estimate valid for a fixed nonconvex deformation, or recover coercivity by a continuation argument whose accumulated error stays below the numerical-range gap uniformly at high frequency.

## 3. Approach 3: transfer resolvent or weighted energy control

### Aim

Nontrapping gives strong PDE resolvent and integral-equation inverse estimates. Try to turn this into a bound on the original numerical range using an equivalent energy norm or symmetrizer. The following exact transfer criterion identifies the missing information; its explicit countermodel shows that norm equivalence is insufficient.

### Proposition 3.1 (near-scalar weighted transfer)

Let A be bounded on a complex Hilbert space, and let P be bounded and self-adjoint. Suppose Re(PAv,v)≥c||v||². For λ>0 and δ=||P−λI||,

Re(Av,v)≥[c−δ||A||]/λ ·||v||².

Proof. λ(Av,v)=(PAv,v)−((P−λI)Av,v). The absolute value of the latter term is at most δ||A||||v||². Take real parts and divide by λ. ∎

Thus a coercive weighted form transfers only if this sufficient condition c>δ||A|| is verified. Two-sided bounds on P alone do not imply it. A frequency-dependent phase can be inserted by replacing A with e^(−iθ)A, with exactly the same proof.

### Proposition 3.2 (uniform inverse and an equivalent coercive metric do not suffice)

On C² let

A=[[1,2],[0,1]], P=[[1,−1],[−1,3]].

Then A is invertible with A^(−1)=[[1,−2],[0,1]], P is positive definite, and Re(PAv,v)=||v||² for all v. Nevertheless β(A)=0. All these statements remain true for the constant family A_k=A, P_k=P, so every relevant norm and inverse norm is uniformly bounded in k.

Proof. Direct multiplication gives PA=[[1,1],[−1,1]], whose Hermitian part is I. The leading principal minors of P are 1 and 2, hence P>0; its eigenvalues are 2±sqrt2. For the nonzero vector v=(1,−1), Av=(−1,−1), and (Av,v)=0. The inverse formula follows by multiplication. ∎

The eigenvalues of A are both 1, so spectral location does not repair the argument. A_k^*A_k is also coercive whenever A_k has a bounded inverse, but replaces the operator and the Galerkin form. Likewise a coercive star-combined equation is not by itself a proof about A_k.

Remaining gap for Approach 3: identify a geometrically justified weight/phase with a small enough defect relative to ||A_k||, or derive a numerical-range estimate directly. None of the available inverse estimates supplies this missing near-scalar control.

## 4. Approach 4: finite escape and the boundary-interaction chain

### Aim

The source proposes a phase-space/billiard description of the oscillatory quadratic form. We worked out an exact Hilbert-space version of the hoped-for implication: a contractive interaction that vanishes after finitely many steps gives coercivity. The calculation also isolates why mere absence of loops is insufficient.

### Proposition 4.1 (nilpotent contraction estimate)

Let T be a bounded contraction on a complex Hilbert space H, and suppose T^N=0 for some integer N≥1. Then

Re((I−T)v,v)≥[1−cos(π/(N+1))]||v||².

The constant is sharp, attained by the N-dimensional unilateral shift. Hence if

A=(1/2)(I−T)+E, ||E||≤ε,

then β(A)≥(1/2)[1−cos(π/(N+1))]−ε whenever the right side is positive.

Proof. Put D=(I−T^*T)^(1/2) and Vv=(Dv,DTv,…,DT^(N−1)v) in H^N. Telescoping gives

||Vv||²=Σ_{j=0}^{N−1}(||T^jv||²−||T^(j+1)v||²)=||v||².

If L(w0,…,w_(N−1))=(w1,…,w_(N−1),0), then VT=LV. Thus (Tv,v)=(LVv,Vv). The real symmetric N×N matrix (L+L^*)/2 has off-diagonal entries 1/2. Its vectors with jth coordinate sin(jmπ/(N+1)), j=1,…,N, have eigenvalue cos(mπ/(N+1)), m=1,…,N, by the addition formula for sine and the two zero endpoint values. These N distinct eigenvalues give a basis, and its largest eigenvalue is cos(π/(N+1)). This proves the estimate, also for H-valued coordinates by an orthogonal change in the finite coordinate index. Equality follows from a top eigenvector of the shift's Hermitian part. Subtracting the error ε||v||² proves the last claim. ∎

This is the standard nilpotent-contraction numerical-radius phenomenon, reconstructed here; no novelty is claimed.

### Corollary 4.2 (explicit polynomial target for such a model)

Since 1−cos x=2sin²(x/2) and sin y≥2y/π on [0,π/2] (concavity above its chord),

1−cos(π/(N+1))≥2/(N+1)².

If N(k)+1≤Ck^p and ε(k)≤[2(N(k)+1)²]^(−1), the model has β(A_k)≥[2C²]^(−1)k^(−2p). ∎

### Proposition 4.3 (acyclicity alone is insufficient)

For T=2L on C², T²=0, so the interaction has no cycle. But I−T=[[1,−2],[0,1]] has zero quadratic form on v=(1,1) and is invertible. More generally the numerical range of I−cL on C^N is the disk centered at 1 of radius |c|cos(π/(N+1)); in particular its distance from zero is max(0,1−|c|cos(π/(N+1))).

For the claim needed here it suffices to prove the radius and disk assertions. Diagonal phase conjugation rotates L by any unit complex scalar. Proposition 4.1's eigenvector computation gives the extremal real part cos(π/(N+1)). The numerical range is convex (the classical Toeplitz–Hausdorff theorem); rotation invariance and this extremum give exactly the disk. Translation and scaling give the formula. The explicit N=2 zero vector independently verifies the stated countermodel without requiring that theorem. ∎

Remaining gap for Approach 4: construct the interaction T_k and remainder E_k for the actual, unpreconditioned A_k on L²(Γ), including glancing directions and arbitrary boundary densities, prove contractivity in that very norm, and justify a finite/polynomial-step escape estimate with a sufficiently small remainder. The exterior billiard escape condition alone has not supplied these statements. The matrix countermodel is an obstruction to an inference, not a scattering-domain counterexample.

## 5. Approach 5: certify a finite compression and control the compact tail

### Aim

For a fixed smooth boundary and fixed frequency A_k is a compact perturbation of (1/2)I. Try to reduce positivity to a certified finite block and prove a rate uniform in k, instead of treating plots of a discretized numerical range as a proof.

For completeness, the fixed-frequency compactness used here can be seen directly. On a compact C² surface in dimension three, the two layer kernels are bounded by C_k/|x−y| near the diagonal, since n(x)·(x−y)=O(|x−y|²). In dimension two the single layer is logarithmic and the double layer has at worst the same integrable bound. Cut out a strip |x−y|<ε. The remaining bounded kernels define Hilbert–Schmidt operators. The omitted operators tend to zero in norm by the Schur test: their row and column integrals are O_k(ε) in dimension three and O_k(ε(1+|log ε|)) in dimension two. Thus the layer operators are norm limits of compact operators for each fixed k. The constants may depend on k, which is precisely the issue in this approach.

### Proposition 5.1 (finite-block coercivity certificate)

Let A=(1/2)I+K be bounded on H, let θ be real, and put Hθ=Re(e^(−iθ)A)=(e^(−iθ)A+e^(iθ)A^*)/2. Let P be an orthogonal projection and Q=I−P. Suppose

(PHθP x,x)≥a||x||² for x∈PH,
(QHθQ y,y)≥d||y||² for y∈QH,
||PHθQ||≤b,

where a,d>0 and b≥0. If ad>b², then

Re(e^(−iθ)(Av,v))≥λ||v||²,
λ=(a+d−sqrt((a−d)²+4b²))/2>0.

In particular β(A)≥λ. One sufficient tail value is d=(1/2)cosθ−||Q Re(e^(−iθ)K)Q||.

Proof. Write v=x+y with x=Pv, y=Qv. The two off-diagonal terms are conjugates, so the form is at least a||x||²+d||y||²−2b||x||||y||. The least eigenvalue of the real 2×2 symmetric matrix [[a,−b],[−b,d]] is the displayed λ. It is positive exactly when the trace and determinant are positive, which follows from the hypotheses. The tail estimate is immediate from Hθ=(cosθ/2)I+Re(e^(−iθ)K). ∎

### Proposition 5.2 (compactness permits fixed-frequency tail certificates, not rates)

Suppose K is compact and P_n are increasing finite-rank orthogonal projections converging strongly to I. Then ||(I−P_n)K|| and ||K(I−P_n)|| tend to zero. If, for a fixed θ, Hθ≥γI with γ>0, Proposition 5.1 eventually supplies a positive certificate using P_n and exact block bounds.

Proof. Strong convergence of Q_n=I−P_n is uniform on each compact subset: cover that subset by a finite ε-net and use ||Q_n||≤1 to pass from the net to the whole set. Apply this to the closure of K's unit-ball image. This proves ||Q_nK||→0; apply the same argument to K^* and take adjoints for ||KQ_n||→0. Let C=Re(e^(−iθ)K), also compact. Then b_n=||P_nC Q_n||→0 and the tail norm ||Q_nC Q_n||→0. Since Hθ≥γI and H is infinite-dimensional, choosing unit vectors in Q_nH and passing to the tail limit shows (cosθ)/2≥γ. Thus a=γ, d_n=(cosθ)/2−||Q_nCQ_n||≥γ/2 eventually, and a d_n>b_n² eventually. In finite-dimensional H, simply take P_n=I and omit the tail. ∎

The premise already assumes the fixed-frequency rotated positivity; this proposition is a completeness property for certificates, not an existence proof of coercivity.

### Proposition 5.3 (pointwise compactness and even positive coercivity have no polynomial consequence)

On H=ℓ² let P be the rank-one orthogonal projection onto e1, and for k≥1 put

A_k=(1/2)I−(1/2−e^(−k))P.

Each A_k is a compact perturbation of (1/2)I, is self-adjoint positive and invertible, and β(A_k)=e^(−k). Therefore no c>0, α≥0 can make β(A_k)≥c k^(−α) for all sufficiently large k.

Proof. A_k acts by e^(−k) on e1 and by 1/2 on e1^⊥. Since e^(−k)<1/2 for k≥1, its least quadratic form on the unit sphere is e^(−k). For any fixed α, k^αe^(−k)→0, for example by bounding the exponential below by k^m/m! with integer m>α. This contradicts any proposed positive c. ∎

This model does not have a bounded inverse uniform in k. Proposition 3.2 separately shows why even uniform inverse bounds cannot restore modulus coercivity. Neither model is claimed to arise from boundary scattering.

Remaining gap for Approach 5: establish, for the actual boundary integral operator, finite-block lower bounds and tail estimates strong enough to yield c k^(−α) for all real sufficiently large k, with certified quadrature and discretization errors if numerical blocks are used. We have not computed or certified such blocks for the example in Proposition 1.2. Finite checks supplied with this packet test identities and scope only.

## 6. Disposition

All five routes performed mathematical derivations beyond source lookup. They leave precise distinct gaps: multiplier sign; fixed-geometry perturbation control; metric-transfer defect; contractive microlocal escape; and frequency-uniform finite-block/tail positivity. None proves (P) on an arbitrary smooth strictly-star-shaped nonconvex obstacle. None constructs a smooth counterexample with β(k)=0 or superpolynomial decay. Known smooth nontrapping O(k^(−1)) upper bounds and nonsmooth all-frequency failures are credited and kept separate. Recommended research status: **unsolved, 5/5**.
