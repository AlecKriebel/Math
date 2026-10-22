# Independent adversarial review: 30005244

## Verdict

**PASS for the complete stated spectral theorem under geometric consistency (G), with a mandatory source-scope qualification.** The proof establishes off-interval absence of spectral pollution, approximation with algebraic multiplicity and norm convergence of embedded Riesz projections. It applies to every bounded Lipschitz particle and, more generally, every bounded particle whose voxel masks converge in measure.

**This is not an unqualified approval for every compact measurable support.** The original short report does not print a boundary regularity assumption. The condition (G) and the standard particle classes covered must remain explicit in any result claim, queue status and PR description. If “full original target” is interpreted as all compact supports without grid consistency, this packet is only a qualified theorem and that unrestricted interpretation remains unproved. No novelty or priority is certified.

Reviewed CANDIDATE.md SHA-256:
`7e767f169f37d7285946ea19264bed7ea658f2d01aeb3ffcf16fa1e0d4622538`

Reviewed MANIFEST.json SHA-256:
`42486090c5f0cc03d8b7cfa8b10e62ab1c540efd54ae0a469f8fe299f0a56526`

All eleven manifest-bound files match. I did not coauthor the candidate or supply its proof route. No mathematical correction is required for the stated theorem.

## Analytical checks

1. **Normalization and static input.** Cartesian differentiation verifies the kernel and its signs. The distributional delta term is +I/3 in −D²(1/(4πr)); the principal-value multiplier is the orthogonal rank-one Fourier projection minus I/3. The continuum static spectrum lies in [−1/3,2/3], contained in the exact CDN lattice interval. The finite matrix is a compression of the bounded selfadjoint static lattice convolution. Extending it by zero is harmless outside this interval because zero belongs to it.

2. **Static consistency.** For every radial cutoff, the finite lattice sum cancels exactly by cubic reflections, permutations and trace zero. The same cancellation holds for the principal-value integral. Subtracting the test function's value leaves an integrable near kernel bounded by a constant times r^−2. Its lattice shell sum is uniformly O(δ), including the case in which there is no lattice point in the cutoff. Far sums converge uniformly on bounded sets for compactly supported smooth tests. The uniform r^−3 output tail is square-integrable in dimension three. Sampling then density and uniform boundedness give strong convergence on the common L² space. No unjustified static norm convergence is used.

3. **Changing grids and domains.** The cellwise map is an isometry for the h³-weighted sequence norm, and its adjoint is cell averaging. The voxel multiplication operators commute with cell averaging. Condition (G) gives strong mask convergence by absolute continuity of the integral, so the compressed static parts converge strongly. Bounded boundary-measure-zero sets satisfy (G) uniformly over arbitrary lattice translations: misclassified cells lie in a shrinking boundary neighborhood. A general compact positive-measure set need not satisfy this, which is why the scope limitation is mandatory.

4. **Dynamic correction.** Independent Cartesian derivatives recover the radial and transverse coefficients. The difference from the static kernel begins with −κ²(I+eeᵀ)/(8πr), followed by −iκ³I/(6π). Its square is locally integrable in dimension three. In the sampled kernel, the removed diagonal cell block contributes no hidden finite self term; the entire near-diagonal Hilbert–Schmidt mass is O(δ+h). The bounded far kernel converges through uniform continuity and mask convergence. Thus the dynamic corrections converge in Hilbert–Schmidt norm, hence operator norm, for each fixed complex κ. No assumption at infinity is needed because all supports are bounded.

5. **Fredholm reduction and pollution.** Static resolvents have uniform off-interval bounds and converge strongly, uniformly on compact spectral sets on each vector. Selfadjointness supplies the analogous strong adjoint convergence. Multiplication on the right by the compact dynamic operator converts the first convergence into norm convergence of the analytic Fredholm factors. Their invertibility at large spectral parameter and connectedness of the complement of a finite real interval justify the analytic Fredholm conclusion. Uniform norm convergence of the factors gives the claimed uniform resolvent bounds away from the continuum spectrum.

6. **Algebraic multiplicity and projection norm.** The factored resolvent identity has the order `(I−R_h C_h)^−1 R_h`, as required. The purely static term integrates to zero around an isolating contour outside the interval. For the compact correction multiplied on the right by a static resolvent, **strong adjoint convergence** is essential and is explicitly used. It gives uniform operator-norm convergence of the contour integrand. The two Riesz projections therefore approach in norm; once their difference is less than one, the elementary two-way injection argument proves equal ranks even for nonorthogonal projections. These ranks count algebraic, not merely geometric, multiplicities. Smaller contours yield convergence of all enclosed eigenvalues. The zero-complement extension contributes nothing to the off-interval contour.

## Source judgment

The exact open question is descriptive rather than a formally quantified theorem. The candidate supplies a rigorous complete description of the requested off-interval behavior for the standard particle class, under an explicit geometric assumption absent from the brief report. It is reasonable to present this as a **source-aware qualified resolution**, provided the condition is part of the result itself. I do not certify the unrestricted compact-support interpretation, nor claim that (G) is necessary and sufficient. The author's pathological-support illustration only demonstrates a failure of volume sampling; it is correctly not advertised as an off-interval eigenvalue counterexample.

The static lattice theorem and standard compact-operator/Riesz theory are credited classical inputs. No literature-wide novelty determination was attempted in this review.

## Reproducibility

The supplied author checker was inspected and replayed; its JSON is byte-identical to the frozen output. It reports 301 exact algebra/symmetry assertions and separate floating-point mesh diagnostics. I independently authored `independent_check.py`, using Cartesian differentiation, rational cubic-orbit sums, Fourier projection identities, integrability exponents and nonnormal finite-dimensional controls with a defective double eigenvalue and moving Riesz projection. Its output is recorded alongside this review. These finite checks are supporting controls, not substitutes for the analytical proof above.
