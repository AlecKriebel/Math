# Independent review of the dipole scope continuation

## Verdict

**PASS: the frozen turn-2 construction proves the stated counterexample for arbitrary compact measurable supports.** Together with the unchanged reviewed turn-1 theorem, it gives a complete source-aware pair of conclusions:

- Geometrically consistent cubic particle discretizations have the proved off-static-interval spectral correctness, including algebraic multiplicity and embedded Riesz projections
- Without a geometric restriction, a compact positive-volume support can have an isolated nonreal continuum eigenvalue while every sampled matrix on the specified mesh sequence is a nonempty 3×3 zero matrix

The counterexample's support has **empty interior**, and its sole sampled point is a measure-zero anchor. It is not a counterexample for bounded Lipschitz particles or for the valid theorem under (G). The brief source does not formally specify which irregular supports it intends; publication must preserve both readings rather than say that the physical DDA observation is false. No novelty or priority is certified.

Reviewed TURN_2.md SHA-256:
`9ba109c7e67f4bfa69406212c84b447812ac94b4235b38c14c6b87acda365310`

Reviewed scope MANIFEST.json SHA-256:
`f8a2f4225fcd82b81f6c00de55494e342f2d7c05b9e4dfb20d804563ac2cca1d`

All five manifest-bound continuation files match. The prior candidate remains unchanged at SHA-256 `7e767f169f37d7285946ea19264bed7ea658f2d01aeb3ffcf16fa1e0d4622538`; my prior scope-qualified review remains preserved at SHA-256 `de2a29b529a7588047374bb47ddcc40b12416f53e77b2b58a0887d81dd1088de`. I did not devise or contribute the new ball-mode/counterexample route before this freeze. No mathematical revision is required.

## 1. Intrinsic ball spectrum

The decomposition is on **L²(B; C³)**, not on the whole-space zero extension. Poincaré's inequality makes the gradient subspace closed. The variational Dirichlet projection splits it into gradients of H¹_0 and harmonic H¹ potentials. Orthogonality to all H¹ gradients means divergence zero with zero weak normal trace, so the zero extension has divergence zero.

The Fourier projection gives A_0=I on gradients of H¹_0 and A_0=0 on the orthogonal complement. For a solid harmonic r^ℓY_ℓ, the zero-extension divergence is the negative boundary normal derivative. Thus the minus sign in A_0 converts it into the positive gradient of the Newton single layer. Matching the interior r^ℓ and exterior r^(−ℓ−1) solutions gives the single-layer multiplier 1/(2ℓ+1), with the correct derivative-jump sign. Hence A_0 acts by ℓ/(2ℓ+1) on harmonic gradients.

The solid harmonics are complete in the Dirichlet norm of the harmonic H¹ subspace; Green's identity makes different degrees orthogonal. There are no missing vector modes, because the other two Helmholtz summands have already been treated. The degree-one gradients are exactly the three constant vector fields. After subtracting I/3, their eigenvalue is zero, and the next harmonic-gradient eigenvalue is 1/15. The other two summands have eigenvalues −1/3 and 2/3. The limiting harmonic value is 1/6. Therefore the zero mode is intrinsically isolated with rank three and gap 1/15.

As an additional independent check, the Newton potential of unit density on B is 1/2−|x|²/6. Its negative Hessian is I/3, confirming the constant-field mode and its sign. The average quadratic dynamic correction on constant fields is −4I/15; only its real trace is needed by the candidate.

## 2. Explicit nonreal perturbation

I checked the entire dynamic expansion and the numerical constants symbolically and with exact rational arithmetic. The two numerator coefficient formulas hold. The bound on the exponential tail follows from 2e−9/2<1; a finite sum plus a geometric tail proves the needed elementary upper bound for e.

For |κ|≤1/2 and r≤2, the scalar fourth-order remainders are at most |κr|⁴. The tensor Frobenius factor is at most √3+1<3. The resulting kernel bound integrates to an operator bound 2|κ|⁴. The coefficient C_2 has Hilbert–Schmidt norm at most one: the squared Frobenius numerator is six, and the stated r^(−2) double integral bound gives exactly that constant. The constant kernel J/(6π) acts on the constant-vector space as 2I/9 and has norm 2/9. Together these give ||C_κ||≤2|κ|².

The contour |z|=1/30 has static resolvent norm at most 30 by the proven ball gap. The smallness assumption yields a perturbed norm at most 60 and projection difference at most 120|κ|². Distance below one preserves rank three. Writing the invariant range as a graph over the static constant modes is valid even though the perturbed Riesz projection need not be orthogonal.

The graph representation is a genuine similarity of the restricted operator, so its finite-dimensional trace counts the eigenvalues with algebraic multiplicity. Since P S_0=0, the graph correction has norm at most 480|κ|⁴; adding the direct remainder gives 482|κ|⁴. The trace error is at most three times that. The quadratic trace is real, while the cubic imaginary trace is −(2/3)κ³. At κ=1/10000, the displayed upper bound is strictly negative using exact fractions. Thus at least one isolated cluster eigenvalue is nonreal. No eigenvalue approximation, simplicity, diagonalizability or numerical spectral calculation is assumed.

This perturbation argument is correctly performed on the intrinsic ball Hilbert space. A globally zero-extended static ball operator would have an infinite zero eigenspace, so replacing the intrinsic rank-three mode by that global zero eigenspace would invalidate this step. The author explicitly avoids that mistake.

## 3. The compact support and sampling

The open balls around the enumeration of Q³ have total volume bounded by the displayed convergent geometric series. Their removal leaves a compact positive-volume F_j. The holes are nested as j increases; their total volume tends to zero. Every rational point of the closed ball is removed by its own positive-radius hole. Adding {0} changes no L² volume operator and leaves exactly one point of each grid (1/n)Z³.

Accordingly the DDA matrix has dimension three and is exactly zero because the only diagonal block is omitted. This is stronger than an empty-matrix example and is exact for every positive integer n. All continuum eigenvalues used are nonreal, so neither zero nor the alternative +I/3 normalization can approximate them.

Because rational points are dense, F_j is nowhere dense; adding an isolated point does not create interior. This pathology is part of the construction and must be disclosed. The example demonstrates the dependence of point sampling on representatives of a volume support. It says nothing negative about the consistency of ordinary boundary-measure-zero particles.

## 4. Persistence under continuum mask approximation

Small removed volume alone is not used to assert static norm convergence. The masks converge strongly and the compressed static operators remain selfadjoint with common spectral bound [−1/3,2/3]. Their adjoints therefore converge strongly too. The dynamic kernels have an integrable square on B×B; monotonicity of the masks and vanishing removed volume yield almost-everywhere convergence, so dominated convergence gives Hilbert–Schmidt convergence.

These are precisely the hypotheses of the earlier reviewed compact-resolvent/Riesz argument. It applies away from the real lattice interval, including to a small circle around a chosen nonreal ball eigenvalue. The global zero complement is now harmless because that contour excludes zero. Norm convergence of the Riesz projections gives equal positive finite ranks for all sufficiently large j. The continuum operator on one fixed F_j, and therefore on Ω_j=F_j∪{0}, has a nonreal eigenvalue in the circle. The sampled matrices never have any eigenvalue there.

The existence of a sufficiently large finite j is a rigorous existential choice. The candidate does not claim an explicit effective j or a computable numerical location for the nonreal eigenvalue. Neither is needed for the stated counterexample.

## 5. Scope closure and credit

The first review withheld approval for an unrestricted arbitrary-compact-support reading. The new proof now settles that reading negatively rather than assuming (G) was printed in the original report. The two conclusions are compatible and should be presented together. The positive result does not claim (G) is necessary and sufficient for each individual support, and the negative example does not refute the standard regular-particle interpretation of the source.

The normalization and original-source findings in the earlier review remain in force: compare T_κ^h to S_κ=A_κ−I/3, and define the static lattice interval through the established Costabel–Dauge–Nedaiasl operator theorem rather than conjectural decimal endpoints. The Helmholtz decomposition, spherical harmonics, compact perturbation theory and projection arguments are classical tools. This audit certifies the mathematical construction and exact source distinction, not historical originality.

## Reproducibility

The author scope checker was inspected and rerun. Its 482 exact controls reproduce byte-for-byte. A separate reviewer program derives Cartesian ball-potential identities, the constant-mode quadratic coefficient, spherical jump/gap identities, Taylor coefficients, Hilbert–Schmidt constants, contour and graph inequalities, the strict trace sign and the removed-volume series. The output is stored in `independent_scope_output.json`. These finite controls supplement the Hilbert-space proof; they do not replace the completeness or convergence arguments, and no numerical eigenvalue was computed.
