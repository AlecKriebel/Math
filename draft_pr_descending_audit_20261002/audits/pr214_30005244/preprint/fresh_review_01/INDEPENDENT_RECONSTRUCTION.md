# Independent mathematical reconstruction

Review input: standalone source SHA-256 `88b73801644a373782997b82fc49ebc3856627e0885740a9c4d52514d5910f53`. This reconstruction was developed from the new manuscript before adopting inherited verdicts. It records the substantive checks behind fresh review 01. Its equations are deductions, rather than finite numerical evidence.

## 1. Normalization and the actual sampled operator

With `g0=1/(4πr)`, the distribution `-D²g0` equals its spherical principal value away from zero plus `I δ0/3`. Reflection/rotation invariance forces a scalar delta coefficient and the trace `-Δg0=δ0` fixes it to `1/3`. The local expansion `gκ-g0=iκ/(4π)-κ²r/(8π)+O(r²)` has an integrable Hessian and no delta. Consequently the omitted-diagonal comparison is precisely `Sκ=Aκ-I/3`, not `Aκ`.

Radial differentiation gives the two tensor coefficients printed in equation (5). The first nonstatic terms are `-κ²(I+eeᵀ)/(8πr)-iκ³I/(6π)`. This also proves the square-integrable `O(1/r)` correction on every bounded physical difference set, for arbitrary fixed complex κ. There is no reliance on a bounded dynamic full-lattice convolution.

Equip sequences with inner product `h³Σ u_m·conj(v_m)`. Then `J_h` is an isometry onto cell constants and its adjoint is exactly averaging, with factor `h^-3`. Thus `J_h T J_h*` takes a constant cell field to `Σ K0(m-n)u_n=Σ h³K0(x_m-x_n)u_n`. For the dynamic integral kernel, integration on each input cell supplies exactly `h³`. Both operators annihilate the orthogonal complement of occupied cell constants. This proves that their sum is the matrix in the question, including zero diagonal; no Galerkin cell integration has been substituted.

The finite matrix norm in weighted and ordinary Euclidean coordinates is identical because the scalar weight multiplies domain and range norms equally. Compression preserves the real form bound, and extension by zero preserves it because `0∈J_lat`. The continuum Fourier multiplier `ξξᵀ/|ξ|²-I/3` has eigenvalues `2/3,-1/3,-1/3`; its mask compression has the same bound and hence lies in `J_lat`.

## 2. Static consistency: cancellation, translation and tails

A full integer shell is invariant under each coordinate reflection and permutation. The numerator `|j|²I-3jjᵀ` has off-diagonal sums zero; all diagonal sums agree and their total trace is zero. Multiplication by any radial cutoff preserves these facts. The finite cut-off lattice sum vanishes exactly, as does its spherical principal-value integral. This is the correct cancellation for the specified cubic point sampling; no infinite conditionally convergent sum is rearranged.

For smooth compactly supported φ, subtract φ at the evaluation center in the near part. The Lipschitz difference supplies a factor `|hj|`, leaving `h³Σ |hj|^-2`. In the integer annulus `q≤|j|<q+1`, the number of points is bounded by `C(q+1)²`, with no point below radius one. Therefore the sum up to physical radius R is at most `CR`, including `R<h`. The near contribution is bounded by `Cδ` uniformly over centers and translations.

Fix δ for the far part. The regularized kernel times `φ(x-y)` ranges over a uniformly smooth compactly supported family when x is bounded. Riemann-sum errors tend uniformly to zero regardless of translation. Sampled interpolation differs from φ by at most `C h` on a fixed enlarged support. Passing from a center to a point of its cell changes the smooth continuum convolution by a vanishing error. This establishes local convergence.

For `|x|` outside twice the support radius (and with a fixed extra cell allowance), every contributing sampled center y has `|x_m-y|≥c|x|`. The sampled mass `h³Σ|φ(x_m)|` is uniformly bounded, because the number of centers in a fixed box is `O(h^-3)` for every translation. Hence the discrete and continuous outputs have size at most `C|x|^-3`. Squared tail mass is `O(R^-3)`; local convergence therefore gives convergence in whole-space L². Uniform boundedness of `T` and density extend it from smooth fields to every L² field.

Under (G), absolute continuity of `∫|u|²` gives `M_hu→Mu`, even for boundary-irregular measurable representatives. Expand the three-factor products, or use the elementary strongly-convergent product rule, to obtain `M_hD_hM_h→MDM` strongly. Selfadjointness also gives strong adjoint convergence. Small removed volume is not asserted to give norm convergence of these static compressions.

## 3. The actual dynamic Hilbert–Schmidt limit

The common bounded occupied-cell box has `h³#I_h≤C` without any boundary regularity. On `|x-y|<δ`, differing cell centers satisfy `|x_m-x_n|<δ+√3h`. Squaring the `C/r` bound, counting ordered input cells by lattice displacements, and then applying the preceding shell estimate gives

`∫∫_{|x-y|<δ} ||c_h||_F² ≤ C h⁶ #I_h Σ_{0<|hj|<δ+√3h}|hj|^-2 ≤ C'(δ+h)`.

The continuum near mass is at most `Cδ`. In particular, every omitted same-cell block lies within `|x-y|≤√3h` and its continuum mass tends to zero; it cannot create an extra self interaction.

Off the δ neighborhood, center displacements remain at least δ/2 for small h. Kernel uniform continuity handles center replacement. The two product masks disagree only on two slabs whose total measure is at most `2|B_*| |Ω_h△Ω|`. Boundedness of the far kernel makes their squared L² contribution tend to zero. Taking h to zero and then δ to zero proves actual Hilbert–Schmidt convergence. Convergence of cellwise kernels also proves compactness and norm convergence of their operators.

## 4. Off-interval spectral argument and deliberate false shortcuts

Strong static convergence plus the common real bound gives strong resolvent convergence at `z∉J` by the resolvent identity. Uniform resolvent bounds and finite nets make this uniform on compact z sets on each fixed vector. Selfadjointness supplies strong adjoint resolvent convergence at conjugate z.

For compact K, finite-rank approximation proves `||(X_n-X)K||→0` from uniform boundedness and strong convergence. Applying this to adjoints proves `||K(X_n-X)||→0` only when adjoints converge strongly as well. This is substantive: on ℓ², `X_n=|e_1><e_n|` converges strongly to zero, but for compact `K=|e_1><e_1|`, `KX_n=X_n` has norm one. The manuscript includes the missing adjoint hypothesis at exactly the necessary multiplication.

Thus `F_n(z)=R_n(z)C_n→R(z)C` uniformly in norm on compact subsets of `C\J`. These are compact analytic families. A finite-dimensional projection can make the complementary compact block have norm below one at any base point. Analytic block elimination then reduces local invertibility to a finite analytic Schur determinant. Invertibility at large z and connectedness of the complement of a bounded real interval exclude the identically singular alternative. Laurent principal parts and the Riesz projections have finite rank. Laurent coefficient identities identify the projection range with the generalized eigenspace; no normality of `B+C` is required.

Uniform invertibility of `I-F_n` on compact continuum resolvent sets proves stability and excludes pollution there. The full resolvents need not converge in norm: for `B_n=|e_n><e_n|→0` strongly, their gap at z=2 is exactly `1/2`. The manuscript instead integrates the analytic static term to zero and controls the compact remainder `G_nR_n`. Its norm convergence uses the adjoint argument just proved.

Two projections at distance less than one have injective restrictions to one another's ranges, even when nonorthogonal. Their finite ranks therefore agree. Smaller contours and stable annuli force convergence of the enclosed cluster, with total algebraic multiplicity. For a unit vector in either range, applying the other projection bounds its distance to the other range by the projection norm difference. This proves both generalized-subspace gaps, without preserving individual Jordan block sizes.

## 5. Intrinsic ball completeness and rank

Choose mean-zero representatives of H¹ functions. Poincare's inequality makes the gradient range closed. The Dirichlet energy variational projection decomposes each gradient into `∇H_0¹` and a harmonic gradient. A vector orthogonal to all H¹ gradients has distributionally divergence-free zero extension: test against restrictions of global smooth functions. The full longitudinal projection therefore vanishes on it. Conversely the zero extension of an H_0¹ gradient is a global gradient, so the longitudinal projection is identity there.

For a harmonic H¹ function in the ball, write its boundary trace in spherical harmonics as `Σ a_{ℓm}Y_{ℓm}`. The harmonic extensions are `r^ℓY_{ℓm}`. Green's identity gives the Dirichlet energy `Σ_{ℓ≥1,m} ℓ|a_{ℓm}|²`; equivalently obtain it first on concentric radius-ρ balls and pass monotonically to ρ=1. Finite harmonic sums are consequently dense in harmonic gradients. This verifies completeness, rather than inferring the full spectrum from a list of sample modes.

The zero-extended gradient of a degree-ℓ harmonic has divergence `-ℓYδ_{S²}`. Matching inside `a r^ℓY` and outside `a r^-ℓ-1Y` Newton potentials with derivative jump `-Y` gives `a=1/(2ℓ+1)`. Thus the longitudinal compression acts on the harmonic gradient by `ℓ/(2ℓ+1)`. Orthogonality and completeness give the whole static spectrum, including the accumulation point `1/2`.

After subtracting `1/3`, only ℓ=1 is zero. This is exactly the three-dimensional space of constant vector fields. For ℓ≥2 the shifted eigenvalues are `(ℓ-1)/(3(2ℓ+1))`, increasing from `1/15`. The other blocks are `-1/3,2/3` and the accumulation `1/6`. This justifies the intrinsic spectral gap and static resolvent bound 30 on radius `1/30`. The whole-space zero extension is deliberately introduced only afterwards: it would otherwise add an infinite zero eigenspace and invalidate the rank-three argument.

## 6. All quantitative perturbation bounds

For each n≥2, multiplying the exponential coefficients gives `i^n(n-1)²/n!` for the identity numerator and `-i^n(n-1)(n-3)/n!` for the rank-one numerator. For n≥4 both absolute numerators are at most n². When `|κ|≤1/2` and r≤2, the tail is bounded by `|κr|⁴(2e-9/2)<|κr|⁴`. The elementary bound `e<11/4` suffices. Frobenius norms `||I||_F=√3`, `||eeᵀ||_F=1` give a remainder kernel at most `3|κ|⁴r/(4π)`.

The manuscript's estimates follow from `∫∫r^-2≤32π²/3`, `r≤2` and `|B|=4π/3`: `||C2||_HS≤1`, `||Eκ||≤2|κ|⁴`, and `||J/(6π)||=2/9`. An independent stronger check uses the overlap of two unit balls at distance r, `V(r)=π(4+r)(2-r)²/12`. Radial integration gives

- `∫∫ r^-2 =4π²`, hence actual `||C2||_HS²=3/8`;
- `∫∫ r^-1 =32π²/15`, hence `PC2|_V=-4I/15` by rotational symmetry;
- `∫∫ r² =32π²/15`, hence the remainder estimate actually yields `||Eκ||²≤(6/5)|κ|⁸`.

These stronger constants are corroboration; the manuscript's weaker constants suffice. The dynamic norm is bounded by `κ²(1+(2/9)|κ|+2|κ|²)≤(29/18)|κ|²<2|κ|²`.

On radius `1/30`, if ε≤1/60 the perturbed resolvent bound is 60. Contour length times the resolvent identity gives `||Pκ-P||≤60ε≤120|κ|²=η`. Projection distance below one preserves rank three. The restriction of P to `ran Pκ` is invertible onto V, so that range is a graph with norm at most `η/(1-η)≤240|κ|²` when η≤1/2. This also works for nonorthogonal Pκ.

The graph coordinate operator is similar to the invariant restriction. Because `PS0=0`, its error from the quadratic and cubic compression has norm at most `(2+2·240)|κ|⁴=482|κ|⁴`. The quadratic compression is selfadjoint for real κ. On V, J is multiplication by `4π/3`, so the trace imaginary part is at most `-(2/3)κ³+3·482κ⁴`. At κ=1/10000, ε≤1/50000000, η≤3/2500000, and the strict upper trace bound is `-7831/15000000000000000`. At least one algebraic eigenvalue is nonreal. The Riesz cluster has finite rank three, so these are isolated eigenvalues; no simplicity or floating eigenvalue claim is needed.

## 7. Fixed support, persistence, boundary cases

The radius cubes sum to `2^-3j-12 Σ_{k≥1}2^-3k=2^-3j-12/7`. This is smaller than the unit-ball volume ratio, so each compact F_j has positive volume. Removing every rational point from the closed ball makes F_j have empty interior. Decreasing deleted radii makes F_j increase and its missing volume tend to zero; almost-everywhere convergence follows, including an irrelevant null sphere discrepancy. The deleted ball centered at zero leaves positive distance from zero to F_j, so restoring zero gives an isolated null anchor.

All rational meshes see exactly zero, not an empty matrix: there is one sampled vector degree of freedom and its diagonal block is zero. The continuum operator is unchanged by the null anchor. To choose one fixed support, first isolate one nonreal ball eigenvalue in a closed disk avoiding the real axis. Static mask compressions converge strongly, remain selfadjoint with common bound `[-1/3,2/3]`, and their corrections converge in Hilbert–Schmidt norm by dominated convergence. The already proved abstract lemma makes the contour projection converge in norm with its positive rank preserved. A sufficiently large finite j therefore works at the original fixed frequency; the construction never lets j depend on mesh n. No effective j is obtained or claimed.

Empty I_h gives the zero-dimensional matrix. A null-volume Ω has the zero Hilbert space but may have many sampled points; under (G) the same estimates still apply, giving off-interval stability and no false finite-rank continuum projections. At κ=0 the dynamic correction is identically zero. Boundary inclusion for bounded boundary-null sets changes membership but still satisfies (G). Arbitrary translations are covered by the uniform local quadrature/tail estimates. No statement is proved about frequencies depending on h, interval-interior correctness, every irregular compact representative, or necessity of (G).
