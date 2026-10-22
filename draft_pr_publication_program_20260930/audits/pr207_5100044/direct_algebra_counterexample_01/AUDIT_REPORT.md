# Independent direct-algebra, Euclidean dynamics and counterexample audit

**Assigned case:** PR207 / 5100044. **Audit date:** 2026-10-16 UTC. **Conclusion:** no critical algebraic defect or target counterexample found in this assigned approach family. An independently derived exact telescoping-plus-Fourier proof of the stated target is preserved separately and requires fresh adversarial review before promotion. Novelty and priority are unestablished.

## Independence and inspected target

The first assessment was sealed at `2026-10-16T23:17:35.195932+00:00`, after reading only the submitted `PROOF.md`. No root sealed assessment or other reviewer findings/reports were read. The submitted `verify.py` was later read as text to understand its finite-test scope, but no submitted code was executed. No submitted files, global views, native MAIN/PR/Zenodo/Sheets records, or Git state were changed. No external individual was contacted. Work is contained in this folder.

The accepted snapshot still has 20 files totaling 61,131 bytes. Submitted proof SHA256: `d92e9a82674b1562e0b980c78088fc48319f9fc3d9d46ec55a1a46c893e372b8`. Full local source pins and captures of mathematical inputs are in `source_pins.json`. The source theorem used is [Stachel, Theorem 4.3 and Eq. (4.9)](https://doi.org/10.1007/s40879-021-00524-2), whose canonical-coordinate and closed-star formulas were checked directly against the primary text.

The exact audited claim assumes an outer noncircular ellipse, a strictly nested nondegenerate confocal **elliptical** caustic, and **least** period `N` divisible by four with any admissible coprime star turning number. Areas are signed straight-edge shoelace areas, including after vertex inversion in a unit circle about a focus. Hyperbolic and degenerate caustics are excluded. The circular endpoint is separately elementary.

## Exact verification

`algebra_check.py` independently reduces the focal distance, distance-product factorization, translated endpoint determinant, ordinary endpoint determinant, double-angle relations, antipodal pairing, confocal normalization, N4 reduction, and axial N4 inverse area. All recorded symbolic residuals vanish. In particular:

- The translated focal determinant and squared distance-product divide to exactly the submitted Eq. (10). There is no missing factor of two or sign.
- Eq. (14) is the exact antipodal sum; the residual vanishes as a rational identity.
- For real phases, `U>0`, `U^2-k^2V^2=kp^2W^2>0`, `D>0`, `1+k sn(u)>0`, and `a-c>0`. The inversion denominators do not vanish anywhere in the target regime.
- The signed ordinary area is exactly `2 C_A S(w)`. Summing an edge's endpoint average counts every vertex twice, yielding the stated factor.
- The two foci have equal signed inverse areas by ordered antipodal cyclic shift and central reflection. Reversing orientation changes both signs, preserving the product.
- `gcd(N,tau)=1` gives least period exactly `N`; more generally the least period is `N/gcd(N,tau)` because the real canonical map is injective modulo `4K`.
- N4's axial signed inverse area is exactly `2/(ab)` and the product is exactly `4`.

These are deductions and symbolic certificates, not floating-point evidence.

## Independent alternative mechanism

The strongest new artifact from this audit is `DIRECT_TELESCOPING_PROOF.md`, supported by `telescoping_certificate.py/.json`. With the submitted `C,U,V,W,t,q`, put `F=1/dn` and

```
Lambda=U(k^4 t^3+k^4 t^2-5k^2 t+k^2+2)/(2 kp^4 W^3),
a0=q/(U-V)^2,
a1=(Lambda-a0)/2,
a2=(V^2-U^2t)/(4 sn(v)cn(v)dn(v)(U^2-k^2V^2)(U-V)).
```

The exact identity is

```
B(u)/(2C)=a0 F(u)+a1[F(u+delta)+F(u-delta)]
                    +a2[F'(u+delta)-F'(u-delta)].
```

The derivative difference telescopes over the finite orbit. It follows directly that

```
R(u)=(2C Lambda/kp) S(u+K).
```

No coefficient divides by `V`; at `V=0` the shifted derivative difference is identically zero, so the identity remains valid for N4 with finite coefficients. All real nonvanishing conditions are spelled out in the derivation. The certificate verifies the underlying generic rational polynomial identity, the reciprocal addition formula, coefficient conversion and specialization exactly.

For the remaining cyclic product, finite-grid Fourier filtering of the standard [DLMF 22.11.3 dn expansion](https://dlmf.nist.gov/22.11.E3) gives `S(w)=lambda dn(lambda w,kappa)`, where the nome of `kappa` is the original nome raised to `m=N/2`, and `lambda=mK(kappa)/K(k)`. The half-grid shift becomes the new quarter period, so the ordinary Jacobi quarter-shift identity gives `S(w)S(w+ell/2)=lambda^2 sqrt(1-kappa^2)`. The nome and theta normalization is [DLMF 22.2](https://dlmf.nist.gov/22.2).

Combined with the signed-area identities and `(K+v)/ell=(m+tau)/2`, this is a complete deduction of the stated theorem from the published canonical parametrization and standard Jacobi identities. It avoids complex divisor counting and residue matching. It is independent mathematical support for the target, not a verdict on every step of the submitted complex proof, and not a claim of originality for this mechanism.

## Independent Euclidean diagnostics

`euclidean_check.py` constructs each first outgoing chord by elementary tangency to the caustic, then generates all subsequent vertices by line/outer-ellipse intersection and specular Euclidean reflection. Jacobi functions determine the family axes; they do not generate the successor vertices. Optional canonical-point comparisons are independent output checks.

At 90 decimal digits the sweep includes **every coprime admissible turning number for N=4,8,...,64**, at each `k` in `{10^-8,0.6,0.999,0.9999999999}`. This is 444 families and 2,220 initial-phase orbits. Six additional stress families include N256/N1024 near the caustic boundary, N128/tau63 close to the half-turn boundary, near-circular `k=10^-24`, and very thin caustic `k=1-10^-24`. Across target and stress cases:

| Diagnostic | Maximum error |
|---|---:|
| Relative area-product phase spread | `2.012e-51` |
| Equality of focal inverse areas | `2.037e-51` |
| Normalized closure | `6.010e-52` |
| Caustic tangency | `2.952e-55` |
| Outer ellipse equation | `1.350e-89` |
| Canonical point / ordinary area comparison (checked subset) | `2.529e-54` |
| Cyclic half-shift product spread | `3.747e-89` |

The worst errors occur in a thin-caustic case with substantial cancellation. Recomputing the hardest two families at 140 digits reduces relative product spread to at most `1.191e-101`, consistent with precision loss rather than a counterexample. Orientation reversal is exact to recorded precision. Near-return distances, direction closure and accumulated winding numbers are recorded for every case.

`meromorphic_check.py` independently tests nonreal phases for Eqs. (4), (9)–(12), (14), (17)–(19), including points near singular divisors, at 100 digits. The maximum scaled substitution error is `2.704e-91`. These checks support the meromorphic formulas but are not analytic proofs of Eq. (17) or the submitted pole argument.

`telescoping_numeric.py` checks the new local identity, cyclic reduction, Fourier multiplication formula, half-shift constant and explicit invariant value against Euclidean orbits in seven normal/extreme families at 120 digits. The worst scaled error is `9.626e-81`; exact certificates, rather than these substitutions, justify the local rational identity.

All numerical claims are floating-point diagnostics. There are no interval enclosures, and no finite grid proves a universal theorem.

## Negative controls and exact scope

Eight wrong-parity primitive families at `k=0.8` have nonconstant products. Relative spreads range from `0.1179` for N3 to `6.669e-8` for N14/tau3. The latter would falsely appear constant under a coarse `10^-6` tolerance. Even periods congruent to two modulo four retain equal focal inverse areas, while their product varies, as expected from the exact phase shift.

Two false period-twelve labels were tested: `(N,tau)=(12,2)` is least period six and varies by `0.004090`; `(12,4)` is least period three and varies by `0.1179`. Their early returns are approximately `10^-100`. Valid period-twelve/four families repeated under period-twenty-four labels remain constant, so constancy alone does not establish primitivity. The exact gcd argument supplies the decisive classification.

Circular regular stars match `(N sin(2pi tau/N)/2)^2`. Physical similarity factors from `10^-8` to `10^8` preserve the product. No claim is made at the excluded degenerate endpoint `k=1` or for hyperbolic caustics.

## Reproduction and remaining gap

Run:

```
/opt/homebrew/bin/python3.11 /absolute/path/to/this/folder/reproduce.py
```

The installed interpreter is Python 3.11.8, SymPy 1.14.0 and mpmath 1.3.0. No package installation or network-fetched code is needed. `reproduction_run.json` pins the executed owned programs; `run_logs/` preserves their output. Only primary mathematical source HTML was downloaded as inert data.

The assigned direct-algebra/counterexample audit is complete. No unsupported bridge remains within the independent telescoping/Fourier deduction once the explicitly cited standard inputs are accepted. The new derivation itself still needs a fresh adversarial reviewer, the submitted complex-pole proof is the responsibility of its separate reviewer, and novelty/priority has not been investigated. These distinctions must remain explicit before any promotion.
