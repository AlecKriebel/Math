# Independent nonlinear and PDE referee report: v1.0.10

Reviewed commit: `953c836a12b9d9d474521feb4a96e218c1155203`.

Scope: main manuscript Sections 6–8 and the nonlinear/scaled-family, certificate, near-threshold, and semilinear-stability arguments in Supplement S5–S10. This report rereads and reconstructs the arguments rather than treating the previous referee's conclusion or the editing AI's validation claim as proof.

**Recommendation within this scope: accept. No correction is required to the nonlinear or PDE claims.** This is a scoped scientific conclusion; it does not certify unrelated packaging, submission metadata, literature claims, or every other theorem in the package.

## Source comparison

The main-source changes since v1.0.9 are three release-metadata lines. The supplement changes only the sentence explaining how rational coefficients multiplying a parameter are printed. The scientific arguments examined here are unchanged. A fresh check is still useful because unchanged text can contain an undetected mistake.

## Independent checkable evidence

Run from the repository root using an environment containing SymPy 1.14.0:

```text
.venv/bin/python maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_preprint_rereview_v1.0.10_2026-09-06/pde/independent_nonlinear_checks.py
.venv/bin/python maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_preprint_rereview_v1.0.10_2026-09-06/pde/independent_near_threshold.py
```

Both scripts pass. Neither imports a submitted verifier, certificate JSON, generated table, or prior referee's derivation.

`INDEPENDENT_NONLINEAR_RESULTS.json` records 453 exact checks. These include independent expansion of the 35-, 77-, 84-, and 22-term modulus polynomials, coefficient signs, and the strict zero set. The zero-set check explicitly checks a positive pure-axis term on every nonnegative coordinate axis; absence of the constant term and nonnegative coefficients alone would not have established the claimed strictness.

The same script checks symbolic identities in the unrestricted dimension parameter for the zero-mode correction, its conservation gauge, the second-harmonic interior recurrence, its initial value, and its four-row boundary determinant. It independently clears the rational lower bound for the reference cubic numerator, verifies the gauge derivatives and endpoint-clearing identity, and checks the signs used in the gauge argument.

In dimensions `m = 3, 4, 5, 7, 12, 25`, it additionally constructs the reaction field from the listed reactions, differentiates it to obtain the Jacobian and Hessian, solves both correction equations directly, and compares the resulting cubic numerator with the printed formula. For each dimension it solves the transformed physical-mass constraint at two rational values of `L` inside the certified interval, including its upper endpoint. It confirms the row-scaled left vector, transformed denominator, kernel-gauge correction, dynamic cubic identity, positive crossing, and negative cubic. These finite checks are consistency tests of the reaction-to-formula chain, not a proof for all dimensions or all `L`.

`INDEPENDENT_NEAR_THRESHOLD_RESULTS.json` records 12 exact positivity certificates. The S9 calculation is rebuilt from the four-species reactions and its specified critical vector. Direct correction solves recover

```text
c_3(epsilon) = 6/1379 + (421985/11409846)*epsilon + O(epsilon^2).
```

The script proves positivity of the cubic, crossing coefficient, four diffusion entries, and the six quartic-Routh quantities on the full stated domain. It expands in `s=t-1` and uses exact Bernstein coefficients on `0 <= epsilon <= 1/1000`, removing only positive powers of epsilon where the open endpoint requires that. This is independent of the submitted reciprocal-epsilon coefficient mechanism. The certificates prove signs throughout the interval, rather than testing a finite collection of epsilon values.

## Adversarial mathematical checks

**Mass constraint and phase space.** Reaction-wise conservation gives `c^T f(x)=0`. The diffusion contribution to the integral mass derivative vanishes componentwise under Neumann boundary conditions, even when diffusion coefficients differ. Only the homogeneous Fourier coefficient has a mass restriction; nonzero cosine modes have zero spatial integral. The semipositive covector does not bound all concentrations, but the proof only claims local existence, positivity, and stability near a strictly positive equilibrium. It does not rely on an unproved global bound.

**Dynamic versus stationary cubic.** With the convention `f(1+u)=Au+B(u,u)/2`, the quadratic corrections are correctly forced by `-B(r,r)/4`. At onset the reduced field begins at cubic order, so differentiating the quadratic center-manifold graph contributes first at fourth order and does not change the displayed cubic. Projection of `cos(xi) cos(2xi)` contributes the stated factor `1/2`. Reflection preserves the boundary conditions and mass class and reverses the critical amplitude, so the claimed odd reduced field and paired branches follow. This verifies the dynamic cubic convention rather than merely a stationary solvability sign.

**Scaled physical system.** The change of concentrations produces `H(A-t Delta)` and the transformed mass covector `H^{-1}c`. The adjoint is therefore `H^{-1}ell`. The second harmonic is unchanged, while the homogeneous correction must change by the conservation-kernel gauge. The text includes this change; simply reusing the unscaled zero mode would have been wrong. The displayed negative value of `ell^T H^{-1}r` excludes a generalized zero eigenvector. Both the transformed crossing and cubic numerator are paired with the correct dynamic adjoint.

**Onset, endpoints, and nearby modes.** The modulus certificates are strict away from the stated equality point. The derivative or adjoint-pairing calculation then establishes algebraic simplicity, which exclusion of other roots alone would not establish. The scaled lower endpoints remain covered: equality in the coarse modulus bound does not create another root because the expanded boundary polynomial retains strictness. The exceptional `m=3` homogeneous cubic is checked directly. For sufficiently small positive `mu`, higher Neumann modes still have damping parameters `k^2(1-mu)>1`; the first mode is the only critical one. No dimension-uniform or epsilon-uniform neighborhood is needed or claimed.

**Patterned-state stability and high frequencies.** Spatial variation of the patterned reaction Jacobian does not invalidate the stability step. On the fixed-mass `L^2` space the linearization has fixed Neumann `H^2` domain, positive diagonal diffusion bounded below, and a bounded multiplication perturbation. Along a sufficiently small branch these bounds are uniform. For an eigenfunction `u`, integration by parts bounds the real part of its eigenvalue from above by the reaction bound, and the imaginary part is bounded by the norm of the reaction multiplication operator because diffusion is self-adjoint. Consequently any spectrum threatening the imaginary axis is confined to a fixed compact region. Compact resolvent and resolvent continuity preserve the finitely many relevant isolated eigenvalues and projections there. The isolated center eigenvalue has the stated negative sign on the supercritical branches; the complement retains its gap. The one-dimensional `H^1` product and embedding properties provide the local smoothness required by linearized stability. An independent reciprocal review by the algebra referee reached the same conclusion.

**Robustness.** The perturbations stay on the positive-equilibrium realization manifold and retune one scalar diffusion multiplier using the nonzero crossing derivative. The proposition expressly claims retuned local persistence for each fixed system, so neither arbitrary nearby criticality nor a uniform large-dimension radius is being assumed. Changing the interval length only changes its discrete Neumann spectrum smoothly and preserves reflection symmetry.

**Near-threshold example.** The endpoint epsilon equal to zero is excluded. For every positive epsilon in the stated range, the reaction-derived quartic has the simple critical root, a stable cubic complement, positive crossing, and stable modes for every `t>1`; the fixed-mass homogeneous mode is stable as well. The positive cubic therefore supports the stated subcritical control example. It does not establish a universal nonlinear contrast bound, and the manuscript does not present it as one.

## Limits of this recommendation

The all-parameter conclusion combines the printed analytic inequalities with independently reconstructed symbolic identities. Selected-dimension matrix calculations are labelled as finite tests. No claim is made here to have formally verified an infinite-dimensional theorem in a proof assistant or to have run a new nonlinear simulation. Neither task is needed to close an identified gap in these arguments, because no such gap survived this reread.

The general principal-minor ray theorem is a positive-real-eigenvalue statement, not a wave exclusion theorem. A reciprocal exact check of the algebra referee's four-dimensional counterexample confirms that its separately stated wave limitation is necessary and correctly retained; it does not undermine the all-mode certificates used for these particular stable-pattern designs.
