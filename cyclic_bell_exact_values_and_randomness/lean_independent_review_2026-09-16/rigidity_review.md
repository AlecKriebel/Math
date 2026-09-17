# Independent support-rigidity and literal-source review

Reviewed 2026-09-16 (Pacific), against the extracted delivered package at `package/lean_formalization`, not the active development directory. This is an independent source/statement review; the coordinating reviewer owns clean compilation and axiom auditing. Completion of this assigned review: 100%.

## Verdict

No mathematical statement mismatch or circular assumption was found in the support-rigidity chain. The final theorem genuinely starts from an arbitrary finite-dimensional mixed-state tensor-product PVM strategy and the literal augmented first-family value, then proves that Alice's actual reduced-state support reduces the relative unitary, has every equality root with the same positive multiplicity, and has dimension divisible by d. The proof deliberately changes some intermediate machinery, but the inspected changes preserve the manuscript's scope and conclusion.

The additional literal-source strategy inspection likewise found actual matrix coefficients, derived unitarity and measurement order, real PVM construction, canonical positive modulus identification, full simple spectra, and a literal Bell-value attainment theorem. This is not merely an unrelated permutation witness renamed as the source strategy.

This verdict is restricted to these modules. It does not certify complete manuscript coverage or substitute for the coordinating reviewer's build result.

## Exact statement correspondence

Manuscript `reference/manuscript/main.tex:548` states the equal-supported-multiplicities theorem; its proof begins at line 1511. Its assumptions are attained finite-dimensional tensor strategies with order-d observables and value `M_d+1`; it explicitly excludes commuting-model rigidity, approximate maximizers, and conclusions on the unused orthogonal complement.

`CyclicBell/GeneralRigidity.lean:176`, `supported_multiplicity_rigidity`, has inputs `2 ≤ d`, `StrategyOn d (Fin 2) (AugmentedInputs d) ι κ`, and `firstValue s = 2 / sin (π/(2*d)) + 1`. The arbitrary finite coordinate types `ι` and `κ` are not fixed to d and need not be equal. Its conclusion is:

- preservation of the actual `aliceSupport s.state` by both `U=A₀†A₁` and `U†`;
- an integer `r>0` such that the intersection of the support with each equality-root eigenspace has dimension r;
- support dimension `d*r`.

`supported_dimension_divisible` at line 230 derives divisibility from this complete theorem. There is no input prescribing the equality spectrum, supported dimension, root multiplicities, reflection equations, faithful state, maximally entangled state, or cyclic/irreducible representation. The absence of a separate explicit “no other spectral values” clause is not a weakening: the proof has the equality-support projection identity and a complete orthogonal decomposition, and the final d positive equal eigenspace dimensions sum to the entire supported dimension.

The PVM formulation is an appropriate presentation of finite order-d unitary measurements. `GeneralCoverageSpectralMeasurement.lean:30` constructs the converse PVM from any such unitary and line 41 recovers its encoding, so restricting the theorem's syntax to PVM-encoded observables does not hide a physical assumption.

## Physical support and saturation are derived

`GeneralModel.lean:14–45` defines states by positive semidefinite density and trace one, measurements by positive orthogonal complete idempotent effects, and strategies by a state and two measurement families. No target conclusion is a field.

`GeneralSupportAlgebra.lean:86` chooses the actual positive square root of the density. Lines 88–116 prove its Gram identity, normalization, and the equivalence between zero positive residual expectation and zero residual applied to the purification amplitude. `partialTraceBob` is the literal coordinate partial trace (line 129); `aliceSupport` is its range (line 174), not a convenient designated subspace. Lines 176–194 identify that support with the amplitude range and prove it nonzero from normalization. This handles mixed and nonfaithful states without assuming full support.

`GeneralSupportSaturation.lean:61` proves an explicit local sum-of-squares identity. `firstValue_operator` (line 107) links the strategy's actual Bell value to the operator being decomposed. `first_saturation_equations` (line 117) adds the aligned-observable positive residual and derives individual residual annihilation from positivity and exact saturation. Its output gives the scalar-gap equation, the augmented stabilizer, and all polar residual equations for the actual purification amplitude.

## Kernel and spectral steps

`GeneralFiniteSpectrum.lean:28` uses genuine continuous functional calculus on the finite matrix spectrum. Arbitrary scalar functions are continuous on this finite spectrum; this is not silently used on an infinite spectrum. `finiteCalc_zero_transfer` at line 83 is proved with a scalar quotient, explicitly splitting the zero-denominator case. It does not assume that a singular operator has an inverse.

`GeneralSupportedPhases.lean:29` uses scalar equality to derive `equalitySupport U*T=T` from the vanished gap. `supportedHalfInverse` at line 89 is zero outside the equality set and a reciprocal only on that set; `supportedHalfInverse_cancel` (line 92) proves its product with the half-modulus is the equality projection, not the global identity. This is a finite-dimensional support pseudoinverse, consistent with the paper's kernel-safe cancellation even though the informal paper uses a range/kernel argument rather than explicitly writing the pseudoinverse.

`polar_cancel_on_support` (line 126) proves both the half-modulus annihilation and equality-support membership of the difference before cancelling it. The support premise for the shifted amplitude is obtained from the augmented stabilizer, not assumed. `quantum_supported_routing` (line 153) derives all routing equations from exact physical saturation. In particular `U*T=T*W`, where W is a product/square of genuine transpose-lifted Bob observables, supplies support invariance. The adjoint intertwiner in `GeneralRigidity.lean:129` supplies the adjoint invariance, so reduction does not rest on an omitted one-sided-invariance argument.

Adjacent polar signs, including modular wraparound, are proved in `GeneralEqualityPhases.lean` and transferred to the equality support by `supported_adjacent_reflection` (`GeneralSupportedPhases.lean:197`).

## Rank argument and completeness

`GeneralReflectionRank.lean:38` proves a rectangular-amplitude rank bound by telescoping powers. The final relative form (line 69) assumes the two intertwining relations and their right-hand power relations; these are intermediate algebraic hypotheses, not the inputs of the physical rigidity theorem. `quantum_root_rank_lower` (`GeneralRigidity.lean:137`) supplies them from `quantum_supported_routing`, the adjacent phase reflection identity, and Bob's measurement order. Thus the conclusion has not been transferred into an assumed reflection condition.

The rectangular telescoping proof is a valid generalization of the manuscript's unitary reflection-product lemma. It avoids needing global invertibility of the polar factors away from the state support, rather than imposing it.

`projectionRangeEquiv` (`GeneralReflectionRank.lean:85`) builds the actual linear equivalence between the supported space and all projected components, with preservation, orthogonality, and completeness explicit. `rootProjection_range_eigenspace` (`GeneralRigidity.lean:103`) identifies each component with the supported eigenspace, not just a spectral label. The rank sum plus all d lower bounds gives equality and constant rank (`GeneralReflectionRank.lean:133`). Positivity of the common rank is derived from the support's nonzero trace-one state. This closes the essential dimension-counting step.

## Literal source strategy check

The source appendix begins at `reference/manuscript/main.tex:1635`, fixes positive clock Z and forward shift X, and then gives the source cosecant expansion around line 1695.

`GeneralSourceFourier.lean:13–35` defines that positive clock, integer triangular exponent, literal coefficient `(-1)^k * chi(k(k+1)/2) * chi(-y(k+1)) / (d*sin(π(k+1/2)/d))`, mode `X^(k+1)*Z^k`, and their sum `sourceBob`. Their signs, transpose convention, and multiplication order match the manuscript.

`GeneralCoverageSourceWeyl.lean:83` derives the exact transpose/polynomial bridge from those matrices. `GeneralCoverageSourceLiteralInterpolation.lean` proves the polynomial's value on each equality root, including the k=d−1 wrap term. `GeneralCoverageSourceFactors.lean:58` then derives unitarity of the literal source Bob matrix, without an assumed coefficient-to-polar correspondence or assumed valid strategy. `GeneralCoverageSourceOrder.lean:51` derives its d-th power identity, for composite d as well.

Although `sourceCanonicalPolar` is defined through the source Bob matrix, its name is supported by proofs: `GeneralCoverageSourceCanonical.lean:77` identifies the modulus with the actual CFC positive square root, line 85 constructs its genuine two-sided inverse, and line 137 proves the polar factorization and unitarity. Since the modulus is invertible here, the canonical identification is mathematically justified, not a circular naming convention. The inverse formula for `Q_y` is separately obtained at line 122.

`GeneralCoverageSourceSpectrum.lean:210` and 224 prove the complete equality-root spectrum of the relative unitary and complete d-th-root spectrum of source Bob, respectively, with every eigenspace dimension one. `GeneralCoverageSourceStrategy.lean:30` constructs an actual normalized entangled state and PVM strategy, line 35 proves the literal encodings (Z, X, source Bob, extra Z†), and line 91 proves its actual first-family value equals `2/sin(π/(2*d))+1`.

## Divergences that are acceptable

1. Finite purification amplitude/range calculations replace some Schmidt-support language. They identify the same reduced density support and include arbitrary mixed states.
2. A finite spectral pseudoinverse on the equality set replaces the paper's range/kernel polar cancellation. Its inverse property is proved only on the correct support, with all possible outside kernels retained.
3. A rectangular telescoping-power rank argument replaces the conjugated-reflection product. It proves a sufficiently strong rank statement and derives its physical premises.
4. Literal source attainment is computed through exact coefficient Fourier sums after physical validity is proved; this is an alternative to summing polar trace norms. The literal matrix identities and canonical polar bridge are nevertheless separately established.

No repair is requested in these audited modules. Whole-package coverage and trusted-kernel replay remain separate conclusions to be made by the coordinating reviewer.
