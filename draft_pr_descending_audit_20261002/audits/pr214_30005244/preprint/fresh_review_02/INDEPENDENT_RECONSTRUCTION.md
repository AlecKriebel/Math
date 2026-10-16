# Independent reconstruction

Frozen before reading earlier manuscript review or acceptance records. The proposed claims are spectral correctness for the actual zero-diagonal cubic matrices outside J under (G), at fixed complex frequency, plus existence of a single pathological compact support with a nonreal continuum eigenvalue and only one sampled null anchor on every rational mesh.

## Normalization and embedding

For g0=1/(4πr), -D²g0 has off-origin value (I-3eeᵀ)/(4πr³). Its rotationally invariant delta term is cIδ; taking the trace gives 3c=1. The Hessian of gκ-g0 is locally integrable O(1/r), with zero residual delta flux, so Sκ=Aκ-I/3 has the printed decomposition. Direct differentiation gives (5); the r^-2 coefficient cancels, leaving -κ²(I+eeᵀ)/(8πr)-iκ³I/(6π)+O(r).

The sequence norm is h³Σ|u_m|², hence J_h* is cell averaging with no missing factor. J_hTJ_h* on cell constants acts by ΣK0(m-n)u_n=Σh³K0(h(m-n))u_n. Occupancy compression gives exactly the finite static matrix. The dynamic kernel constant on a distinct-cell product contributes exactly h³Rκ(x_m-x_n)u_n. Setting same-cell products to zero reproduces the sampled zero diagonal without inserting a self term. Scalar h³ rescaling leaves matrix operator norms unchanged.

## Static strong consistency

For sampled smooth compactly supported φ, subtract φ(x_m) under a compact radial cutoff. Every finite cubic orbit of K0 cancels: reflections cancel off-diagonal entries, permutations equalize the diagonals, and trace zero annihilates them. Continuum angular cancellation is identical. The near residual is bounded by C h³Σ(0<|hj|≤2δ)|hj|^-2≤Cδ by integer-annulus counting, including empty sums. The continuum near residual is O(δ). For fixed δ, far summands are smooth and uniformly compactly supported for bounded center locations, giving uniform Riemann convergence for translated grids. Outside twice the support radius, both outputs are O(|x|^-3), using the uniformly bounded sampled L¹ norm. Squared tails are O(R^-3). Thus whole-space L² convergence follows, then replacement of sampled φ by φ and extension by density follow from the established uniform lattice bound. Under (G), ∫_(Ω_h△Ω)|u|²→0 proves strong mask convergence; products give B_h→B strongly. Compression preserves the lattice form interval since 0∈J. The continuum multiplier has eigenvalues -1/3 and 2/3. Neither eigenfunction smoothness nor static norm convergence was used.

## Actual sampled dynamic HS convergence

Physical differences lie in one bounded box, giving ||Rκ||F≤Cκ/r for each fixed complex κ. Its square is locally integrable. On |x-y|<δ, distinct cell centers differ by at most δ+√3h, giving sampled squared integral ≤C h⁶ N_hΣ|hj|^-2≤C(h³N_h)(δ+h). Occupancy volume is bounded. The omitted same-cell part has no surviving HS mass. Away from the diagonal, centers are uniformly separated and the kernel is uniformly continuous; product-mask errors occupy volume ≤2|B_*||Ω_h△Ω|. Taking h→0 then δ→0 gives HS convergence and hence norm convergence to a compact correction. Ordinary fieldwise consistency alone would not prove this.

## Nonnormal spectral conclusion

R_h(z)=(z-B_h)^-1 is bounded by dist(z,J)^-1. Resolvent identity gives strong convergence, and selfadjointness supplies strong convergence of adjoints at conjugate z. Finite nets give uniformity on compact z sets on each vector. Finite-rank approximation proves ||(X_h-X)K||→0 for bounded strong convergence and compact K. Taking adjoints proves ||K(X_h-X)||→0 when adjoints also converge strongly. This distinction is essential: X_n=e1⊗en converges strongly to zero but (e1⊗e1)X_n has norm one.

Thus F_h=R_hC_h→RC in norm uniformly on compact off-J sets. The factorization z-S=(z-B)(I-F) and compact analytic Fredholm reduction on connected C minus J give isolated finite-type poles, since large |z| is invertible. Locally a finite-rank compression makes the complementary block small; a finite Schur determinant then controls invertibility and yields finite-rank principal Laurent parts. Continuation excludes the identically singular alternative. Resolvent Laurent identities identify Riesz ranges with full generalized eigenspaces.

On compact continuum-resolvent sets, Neumann estimates stabilize I-F_h. On an isolating circle write the resolvent as R_h+G_hR_h, where G_h=(I-F_h)^-1F_h is compact and norm-convergent. The analytic R_h integrates to zero; ||G_hR_h-GR||≤||G_h-G||||R_h||+||G(R_h-R)|| tends to zero using adjoint strong convergence for the second term. Hence Riesz projections converge in norm for defective and nonnormal clusters too. Distance below one makes each restricted projection map injective, so finite ranks agree without orthogonality. Smaller circles and compact annuli give convergence with total algebraic multiplicity. Both subspace gaps are bounded by the projection norm difference. Static bounds plus norm-convergent corrections give bounded matrix norms.

## Intrinsic ball certificate

The closed H¹ gradient space splits by the Dirichlet variational projection into H0¹-gradients and harmonic gradients; its orthogonal complement has divergence-free zero extension. The longitudinal projection is identity on the first and zero on the last. For r^lY_l, integration by parts gives zero-extension divergence -lY_lδ_surface. Matching the interior a r^l and exterior a r^(-l-1) single layers with derivative jump -1 gives a=1/(2l+1). Thus A0 has eigenvalue l/(2l+1) on this gradient. Completeness is an infinite argument: harmonic H¹ boundary traces have harmonic expansions with Dirichlet norm Σl||Y_l||²; finite partial sums converge in energy modulo constants. Orthogonality follows by Green's identity.

After the 1/3 shift, l=1 is exactly the three constant vectors; l≥2 yields (l-1)/(3(2l+1))≥1/15, and the other static values are -1/3,2/3 and accumulation 1/6. The radius-1/30 circle has resolvent bound 30. This must be intrinsic to H_B; ambient zero extension would make zero infinite dimensional.

For C2, eigenvalues (2,1,1) of I+eeᵀ give Frobenius square6, and ∫∫r^-2≤32π²/3, yielding HS norm≤1. J/(6π) has norm2/9. Taylor numerator coefficients are i^n(n-1)²/n! and -i^n(n-1)(n-3)/n!. For n≥4 and |κr|≤1 each tail≤|κr|⁴(2e-9/2)<|κr|⁴. Matrix Frobenius factor<3 gives remainder kernel≤3|κ|⁴r/(4π), hence HS norm≤2|κ|⁴. Therefore ||Cκ||≤(29/18)|κ|²<2|κ|² for |κ|≤1/2.

If ε≤1/60, the perturbed resolvent is bounded by60 and contour integration gives ||Pκ-P||≤60ε≤120κ². Rank3 persists. Its graph norm≤η/(1-η)≤240κ² for η≤1/2. The coordinate restriction differs from κ²PC2-iκ³PJ/(6π) by ≤482κ⁴. Real κ gives imaginary trace≤-2κ³/3+1446κ⁴. At κ=1/10000 the coefficient is -7831/15000 times κ³, strictly negative, with every smallness condition satisfied. Hence at least one algebraically counted eigenvalue is nonreal. No simplicity or diagonalization is required.

## Fixed compact support

The removed radius cubes sum to 2^(-3j-12)/7 relative to ball volume. Every rational point is removed, so F_j is compact with positive volume and empty interior. Shrinking radii give increasing F_j converging to B in measure and almost everywhere. Restoring the origin adds an isolated null anchor because its own removed neighborhood has positive radius. Every rational mesh samples exactly that point.

Keep κ and a nonreal ball eigenvalue fixed. Choose an isolating closed disk wholly off the real line. Ambient F_j compressions of D converge strongly with common static interval [-1/3,2/3], while their dynamic kernels converge in HS norm by domination. The same spectral lemma preserves positive finite Riesz rank for all large finite j. Select any one such j. This is one fixed support with nonreal spectrum and 3×3 zero rational-mesh matrices. No effective finite index is derived. Its voxel volume tends to zero while its true volume stays positive, so (G) fails.

## Limiting and falsification checks

At κ=0, correction zero leaves all spectra in J; no off-J eigenvalue is invented. Empty I_h uses the zero-dimensional convention and ambient zero operator. Null Ω satisfying (G) has trivial intrinsic space; occupied volumes tend to zero and dynamic norms vanish, while possible static matrix spectra remain in J. For boundary-null bounded sets every classification error lies in a shrinking bounded boundary neighborhood, uniformly in translations; inclusion/exclusion of the null boundary remains admissible. Arbitrary null modifications can alter center membership and still need (G). Fixed complex κ causes no infinity issue on bounded differences. Full static/resolvent norm convergence, interior-J behavior, rates, varying frequency and individual Jordan blocks are neither required nor obtained.

No central mathematical gap or counterexample to the stated claims was found. The primary static lattice theorem is an explicit external input to check next. Finite controls cannot establish these analytic limits or priority.
