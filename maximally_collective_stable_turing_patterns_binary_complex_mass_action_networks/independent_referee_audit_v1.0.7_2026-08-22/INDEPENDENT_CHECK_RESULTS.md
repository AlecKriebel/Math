# Independent mathematical checks

The script `independent_checks/independent_exact_checks.py` imports no submitted module and reconstructs the source and target complexes directly from the displayed reaction list. Exact sections use SymPy integers/rationals. Sections explicitly labeled numerical use double precision and are falsification evidence, not proof.

## Exact reconstructions

- For each `m=3,...,7`, independently constructed `Y_m` and `Gamma_m` have shape `(m+1) x (m+2)`, every complex is binary, `rank Gamma_m=m`, the displayed `c` annihilates `Gamma_m`, the kernel dimension is two, and the displayed homogeneous right nullvector is annihilated by `A_m(a,b)`.
- Exhaustive induced-subgraph enumeration for `m=3,...,7`, both with a generic boundary edge (`a=1,b=3`) and on the deletion hypersurface `b=2a`, found no SCC outside the three manuscript classes and no nonnegative singleton block.
- For `m=3,...,7`, all `m+1` order-`m` omission minors were computed as exact determinants with nontrivial rational `a,b,H`; every entry matched the claimed one-negative/two-zero/interior-positive table.
- For `m=3,...,7`, direct exact matrix multiplication verified the printed right and left critical kernels, the two transversality-pair signs, the printed `w_0` equation and conservation gauge, and the exact `w_2` equation. Direct rational linear solves—rather than the submitted closed-form helper—gave negative cubic coefficients in all five dimensions.
- The four source modulus polynomials were independently expanded from `F,G,P,R`:

| Certificate | Exact nonzero term count | Coefficient result | Equality check |
|---|---:|---|---|
| Unit homogeneous `E_35` | 35 | every coefficient strictly positive | no constant term; positive pure `x` and `z` terms, so equality only at `x=z=0` |
| Unit spatial `E_77` | 77 | every coefficient strictly positive | no constant term; positive pure `x,z,s` terms, so equality only at `x=z=s=0` |
| Scaled homogeneous `E_22` | 22 | every coefficient polynomial has nonnegative coefficients in `U`; at `U=0`, positive pure `x^2` and `z^2` terms remain | equality only at the origin throughout `U>=0` |
| Scaled spatial `E_84` | 84 | every nonzero coefficient polynomial has nonnegative coefficients in `A` and is positive for `A>0` | no constant term; positive pure `x,z,s` terms for `A>0`, so equality only at the origin |

These checks independently establish the certificate equality cases; they do not merely infer uniqueness of equality from “all displayed coefficients are nonnegative.”

## All-dimensional cubic bridge

The submitted short cubic verifier evaluates the full contraction only at `m in {3,4,5,6,8,10}` and compares it with a hard-coded `N_formula`; that program alone is finite regression. An independent symbolic derivation closes the all-dimensional bridge:

- The printed `w_2` recurrence implies `w_{i-1}-w_i=4w_i/K_i+sigma`.
- The factor identity `T_i/(K_{i-1}K_i)=K_{i-3}K_{i-2}/(K_{-1}K_0K_1K_2)` reduces the interior contraction to the printed polynomial sum plus the harmonic sum `\mathfrak h_m:=\sum_{j=1}^{m-2}(91m-181-j)^{-1}`.
- Substitution of the independently derived boundary solve and `w_0` identities makes `N_m-[R_m+C_m \mathfrak h_m]` factor identically to zero for symbolic `m`.
- The boundary determinant, its shifted-positive denominator, and `S_m=ell^T B(r,rho)` were also verified symbolically.

Thus the all-dimensional cubic theorem is supported, while the semantic description of the finite entrypoint as an all-dimensional verifier is too strong.

## Numerical falsification (not proof)

- 80 log-uniform positive parameter trials for each `m=3,...,8`, including `b=2a`, exhaustively tested every principal block of order below `m`: 76,560 block instances produced no counterexample. Extreme scaling drove the smallest normalized spectral margin to about `6.9e-16`, so the sample is deliberately not promoted to an exact Hurwitz proof.
- At both certified scaled-family endpoints for `m=3,4,5,10,149`, direct eigenvalue computations found exactly the expected homogeneous conservation zero and first-mode critical zero, with the complementary spectra left of the imaginary axis for damping `t=0,1,4,9,25`. At `m=149,L=L_1`, the smallest reported complementary margin was about `7.3e-4`; the check remains floating-point provenance.
- Independently computed endpoint contrasts agreed with the exact fixed-product formula to displayed double precision in every tested case, including `m=149`.

## Interpretation

The exact checks directly support representative formulas, boundary cases, exceptional dimensions, certificate equality cases, and the internally delicate cubic contraction. The random/eigenvalue campaign is an active counterexample search only. Uniform theorems still rest on the manuscript's graph, recurrence, coefficient-sign, and standard functional-analytic arguments rather than on sampling.
