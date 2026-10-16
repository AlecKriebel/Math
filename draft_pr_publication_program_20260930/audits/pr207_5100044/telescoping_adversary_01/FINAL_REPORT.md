# Sealed independent adversarial assessment

Sealed 2026-10-16T23:33:26Z. Completion estimate: 100% of this scoped verification.

**Verdict: no substantive mathematical defect found in the new direct telescoping route.** The pinned alternate derivation establishes the stated constancy under its exact real physical hypotheses, including least period divisible by four, all primitive star windings represented by `0<tau<N/2`, reversal, either focus, and `N=4`.

This is a fresh scoped assessment, not whole-package publication approval or a novelty/priority conclusion. The original complex proof, other audit reports, previous reviews, and root's assessment were not read before sealing. No source files outside this audit folder were changed, no submitted checker was executed in its original location, and no Git/service write or outreach was performed.

## Pinned reviewed inputs

- `direct_algebra_counterexample_01/DIRECT_TELESCOPING_PROOF.md`, 10,407 bytes, SHA-256 `43919a9d6d2f8b8daa51dca6bea7fb302df6121d815acc725bb3b349a900d4ed`.
- `direct_algebra_counterexample_01/telescoping_certificate.py`, 2,258 bytes, SHA-256 `24749b17530d1745363ae457a5217ae90cef49971d4b93031aae8667a9575a9d`.
- Primary source only: exact Stachel published PDF, SHA-256 `9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8`, printed p.1614 / PDF p.13. Theorem 4.3 and (4.9) were read directly and agree with the imported canonical coordinates, modulus, shift, closure and axes.
- Primary mathematical inputs independently opened: [DLMF 22.8](https://dlmf.nist.gov/22.8), [22.11.3](https://dlmf.nist.gov/22.11.E3), and [22.2.1–3](https://dlmf.nist.gov/22.2).

## Proof-level findings

1. **Euclidean area normalization is correct.** Independent reduction of the addition formulas yields the focal distance product, focal and original endpoint determinants, inverse side half-cross-product, and antipodal pair exactly. Summing original side half-determinants gives `A=2 C_A S`, and the inverse edge centers are `w+v+j delta`, giving `A_+^dagger=R(w+v)`. The unit focal inverse coordinates in the draft differ from literal inverse vertices by a translation only. Every factor of two and the area-product prefactor `4 C_A C Lambda/kp` are correct.
2. **The rational decomposition is checkable and valid.** Independently solving the three polynomial coefficient equations recovers the same `a0`, `a1`, `a2`, and `Lambda`. Exact re-substitution gives zero. The derivative is the derivative of `F(u+delta)-F(u-delta)`, with the displayed positive sign; its conversion factor is `4k^2 h cn(v)dn(v)V`. Shifted `F` sums reindex the same finite cycle; shifted derivative sums cancel. This gives exactly `R(u)=(2 C Lambda/kp) S(u+K)`.
3. **The entire strict real domain is covered.** `U=1-k^2+k^2(1-t)^2>0`, `W>0`, `U-V=2t kp^2>0`, and `U^2-k^2V^2=kp^2W^2>0`. Hence all displayed coefficient denominators are nonzero and all real inverse areas are defined. `Lambda>0` follows from its bracket decreasing in `t` to `2(1-k^2)^2>0`. No positivity of the sign-changing coefficients `a1,a2` is required.
4. **The `V=0` exception is regular.** There is no division by `V` in the actual coefficients. This case has `delta=K`; primitivity forces `N=4,tau=1`. The coefficients reduce to `b0=t`, `d0=0`, `a0=q/U^2`, and finite `a2=-t/(4h cn(v)dn(v)U)`. The derivative difference vanishes identically. Direct Euclidean axial areas are `2ab` and `2/(ab)`, giving product `4` without a limiting argument.
5. **The Fourier normalization and convergence are correct.** DLMF's real dn coefficients are `pi/(2K)` and `(2pi/K) q_e^r/(1+q_e^(2r))`, with frequency `r pi w/K`. Absolute uniform convergence follows by a geometric bound. Coprimality makes the finite cycle a uniform grid and retains only indices divisible by `m`. Matching every coefficient gives exactly `S(w)=lambda dn(lambda w,kappa)` with nome `q_e^m` and `lambda=m K(kappa)/K`. The real nome map is onto `(0,1)`, so the required `kappa` exists; DLMF's inverse theta formulas confirm both its parameter and the stated theta constant.
6. **The final half-shift and physical controls are correct.** `lambda ell/2=K(kappa)`, so the dn quarter shift gives the positive constant. For `N=4n`, `(K+v)/ell=(m+tau)/2` is a half-integer. Central negation is the ordered shift by `m`, either focal inverse polygon has the same signed area, reversal negates both signed areas, and positive similarity cancels the two area scale factors. The least-return argument correctly excludes repeated lower-period orbits labeled with a divisible-by-four period.

The full reconstructed equations and justifications are in `INDEPENDENT_DERIVATION.md`. These are proof-level checks of the alternate argument, separate from the numerical evidence below.

## Reproducible computation

Run inside the case directory:

```
/opt/homebrew/bin/python3.11 -E -S -B -P telescoping_adversary_01/independent_exact.py
/opt/homebrew/bin/python3.11 -E -S -B -P telescoping_adversary_01/independent_numeric.py
```

Both scripts explicitly load the known package directory and import neither the submitted checker nor any prior diagnostics.

- SymPy 1.14.0: **23/23 exact checks passed**, including Euclidean focal algebra, reciprocal shifts, polynomial decomposition from an independent solve, closed cyclic coefficient, derivative conversion and `N=4` reductions. Results: `independent_exact.json`.
- mpmath 1.3.0 at **240 decimal digits**: **101 configurations / 505 phases passed**. Checks include actual squared-distance Euclidean inversion, original/inverse areas, the explicit constant, pointwise telescoping, Fourier-filtered dn, half-shifts, either focus, reversal, caustic tangency, and reflection. Inputs include nonunit caustic scale `2.37`, every primitive forward winding for `N=4,8,12,16,20,28` at five moduli, selected `N=64,128`, and `k=1-10^-40`. Worst normalized discrepancy: `1.84e-125` in the pointwise decomposition; explicit full-product discrepancy: `1.75e-163`. Results: `independent_numeric.json`.
- Negative controls have relative phase variation `0.105697652...` for least period six and `0.006161527...` for least period ten at `k=.99`. A period-twelve label with `tau=2` has least period six and reproduces the nonconstant result, validating the least-period guard.

**Numerical limitation:** at 110 digits the intentionally extreme `k=1-10^-40` test lost enough precision in the cancellation-sensitive pointwise decomposition to fail by order one. The same test passes at 240 digits, retaining the unchanged `1e-55` tolerance. The draft explicitly disclaims a uniform condition bound near `k=1` or `v=0`; this is a confirmed numerical-conditioning limitation, not a missing proof hypothesis. These computations are high-precision diagnostics, not interval certificates. Exact symbolic algebra and the analytical argument supply the proof.

**Remaining gap in this scoped claim: none found.** Zero caustic minor axis and `k=1` remain excluded, as stated. The circular formula is separately consistent by direct regular-star area calculation. No inference is made about novelty, historical priority, other proofs, or publication readiness beyond the reviewed alternate route.
