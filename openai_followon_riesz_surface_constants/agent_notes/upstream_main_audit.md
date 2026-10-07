# Independent audit of the main family-090 dependency

Audit date: 2026-10-06 (America/Los_Angeles). Source reviewed at upstream commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The source clone `/Users/alec/Desktop/math` was kept read-only. This report concerns the core positive-energy theorem of **Universal optimality of the triangular lattice**; it does not certify that paper's renormalized/jellium extensions, the atomic companion, or the new finite-surface theorem.

## Exact dependency and conventions

All line references below are to files under `preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/build/sections/` at the pinned commit unless otherwise indicated.

`01-uniform-gaussian-theorem.tex:10-28` defines the triangular lattice `A=b^(-1/2){j(1,0)+k(1/2,b)}`, `b=sqrt(3)/2`, of covolume one; centered disk density is `#(C cap B_R)/(pi R^2) -> 1`. Energy is the **liminf of ordered off-diagonal pair sums within the same disk**, divided by its point count. There is no separation or bounded local occupancy requirement.

Theorem 1 at `01-uniform-gaussian-theorem.tex:31-41` asserts, for every smooth nonnegative completely monotone `g:(0,infinity)->[0,infinity)`, the extended-real inequality `E_g(C) >= sum_{a != 0} g(|a|^2) = E_g(A)` for every locally finite set of centered disk density one. For `g(t)=t^(-s/2)` and `s>2`, all potential hypotheses hold and the lattice sum converges. This theorem alone is an infinite-configuration statement; a finite-to-infinite bridge is still required to identify `C_(s,2)`.

## Scope actually examined

I read the repository README and manuscript README, main TeX and bibliography references as needed, full sections 1--7, and the parts of the arithmetic appendix needed for interpolation/signs. I inspected both supplied interval checker programs and their integrity helper, checked formula correspondence at their pivotal matrix/sign construction steps, and reproduced their runs in a project-local copy. I read `lean/docs/090.md` for its stated scope but did not inspect/build actual Lean declarations in this audit. The catalogue does not constitute formal verification evidence for this report.

No attempt was made to validate the separate conditional floor-rounded finite-matrix route. The main manuscript explicitly uses exact-array Arb enclosure instead (`03-quadrature-finite-data.tex:623-640`; `08-arithmetic-verification.tex:13-24`), so failure to execute the optional floor route is not a gap in the selected proof route.

## Mathematical audit of the mechanism

1. **Shells and spectral realization.** `02-cardinal-fourier.tex:18-55` gives the radial coordinate `s=b|x|^2`, node superset `12 Z + {0,1,3,4,7,9}`, and `A*=JA`. The form residues follow from modulo 3 and modulo 4 restrictions; dual covolume and rotation are correct. The sine product has nonnegative double zeros (`103-160`). The cardinal measure derivation (`183-263`) correctly cancels the constant/linear subtractions using `P(n)=P'(n)=0`; variation bounds are unweighted and independent of input-node location. Absolute summability yields uniform convergence of every derivative on compact sets and hence genuine entire functions and exact cardinal jets.

2. **Genuine Fourier transform, rather than a formal profile operation.** At `02-cardinal-fourier.tex:269-361`, the parameter `gamma=b(h-it)` has fixed positive real part. Its planar Fourier transform is `gamma^(-1) exp(-pi |xi|^2/gamma)`. Substituting the manuscript's `z(t)` and `lambda(t)` gives the stated transformed profile with all dimension-two factors intact. Compact frequency support and finite spectral variation justify integrations, derivatives and polynomial weights. The transformed Gaussian real part also has a positive lower bound, giving Schwartz functions. Fourier involution is used for actual radial Schwartz functions, not incorrectly for a folded contour integral; `292-305` explicitly addresses that distinction.

3. **Continuum quadrature error.** `03-quadrature-finite-data.tex:36-87` derives exact polynomial moments through degree 383 and positive weights summing to one. The integrand disk estimates at `94-199` hold for all scaled derivative orders, all output radii `m<=168`, all `|y|<=3/2`, and all 171 basis inputs. The singular transformed parameter stays outside the disk. The Cauchy tail and the two positive functionals give the error `4*10^83*2^(-384)<10^(-31)`, covering the actual exact spectral integrals rather than only sampled values.

4. **Exact simultaneous contacts.** `04-exact-interpolation.tex:70-195` imposes the full infinite operator equation in paired unweighted `ell^1`. The finite matrix inverse follows from `||D^64||<.004`, norm-bounded power sums and `D^512`; the quadrature perturbation uses all 168 output coordinates. The Schur complement uses small distant **output** norm `delta=1.1e-14`, a finite inverse bound 40 and the possibly large finite-tail input norm 4000. Its bound `delta*(1+40*4000)<1` is a genuine invertibility argument, not a presumed small full operator. The residual estimates at `225-335` establish a full-list correction below `2e-8`, including the omitted target jets, exact/quadrature discrepancy and power-sum residual.

5. **Global signs and exact zeros.** `05-global-signs.tex:68-171` subtracts values and slopes before division by squared distance; it never divides a raw nonzero interpolation residual by a vanishing square. The exact slack jets from the infinite system justify the final square multiplication. The target support cases (`175-243`) handle unbounded `k` by monotonicity and fixed left-endpoint Taylor polynomials; the `m=3` Jensen support has the correct direction. Bernstein coefficients and containing parameter boxes yield whole intervals, not merely parameter sampling (`247-284`). In the tail (`354-493`), the signed low-node rational part remains `>.002`, the high-node/remainder second derivative is bounded by `.0002`, and the remainder has double zeros at all distant nodes. The sine product lower bound `.68*(s-m)^2` is established by concavity and exact midpoint values (`295-352`); the comparison `.68*.002>.0001` closes the same quadratic scale at and between nodes.

6. **Centered-density lower bound.** `06-gaussian-energy-transfer.tex:25-128` proves the density-only positive-definite LP inequality. The cross term error is bounded uniformly in every point by the integrable Schwartz tail outside `epsilon R`. Cauchy--Schwarz in the positive Fourier form, together with overlap convergence for the area self-term, gives `liminf Q(mu_R,mu_R)/N_R >= fhat(0)` after `R->infinity`, then `epsilon->0`. It does not assume occupancy bounds or periodicity of the competitor. Removing exactly `N_R` diagonal terms gives the stated ordered energy bound.

7. **All Gaussian scales and the lattice identity.** `06-gaussian-energy-transfer.tex:139-215` applies the normalized pair for `alpha>=1`, where `k=pi(alpha/b-h)>2.36`, then Fourier complementation for `0<alpha<1`. The dimension-two reciprocal factor is correct. Radiality and `A*=JA` correctly transfer contacts. Schwartz Poisson summation is applied only to the lattice, so exact contact values imply the Gaussian lattice value `fhat_alpha(0)-f_alpha(0)`.

8. **Liminf and singular potential transfer.** `07-shifted-mixtures.tex:21-134` supplies a finite positive measure for every shifted completely monotone potential. The weak-limit construction keeps mass at both endpoints, and the estimate for real exponents permits a subsequence chosen before the exponent. `158-208` takes an arbitrary radius sequence before Fatou. Each normalized Gaussian sum is nonnegative; Tonelli and Fatou therefore remain valid for infinite limits. The `v=1` endpoint correctly gives `N_R-1 -> infinity`. The final shift is removed only in the lattice sum by monotone convergence, avoiding an unjustified configuration-liminf interchange. Lattice attainment, including divergent sums, is then checked at `211-233`.

## Source and checker binding

The pinned source was copied without alteration to `audit_runs/upstream_main/pinned_source/`. Important SHA-256 values:

| File | SHA-256 |
|---|---|
| `paper.pdf` | `50daa477c52b1f3e179764794506f0037d26c2ec130d1d6e817626f4e0b689f3` |
| `verification/CERTIFICATE-INPUTS.json` | `7f5ff0bafbe83b4c06d83daa3c953f6130dadfca65f1e06df79034567478d539` |
| `verification/numeric_balls.py` | `d5725fe0b1946e3213ae4bdfdb8e3abc99102d1564677665dd0d9e89bdcfab01` |
| `verification/arithmetic_bounds.py` | `d6dd618f5d67f16a96c385d78f6362c6af81cd5e2b8bec003b91029f356c91e5` |

The manifest binds 13 exact mathematical source files and four checker sources; its input hashes were validated before and after numerical execution. The helper explicitly labels this integrity-only, and I separately checked formula correspondence. In `verification/numeric_balls.py`, `build():98-194` implements the stated weights, folded mass matrix, transformed jets, projection signs, finite geometric sums, extras, target matrix and column norms. `check_signs():205-279` implements every signed half-gap, the order-40 deleted Taylor quotient, parameter-box vertex minimization, target support cases, Bernstein conversion, and grouped low-node rational tail. Strict Arb comparisons prove every inequality; conversion to float only chooses diagnostic minima after proof (`257-258`).

## Reproduction status

Environment: CPython 3.14.6, `python-flint==0.9.0`, without optimization. The source tree and output path use no parent traversal or symlink components. Runs use the supplied command-line interface. Output paths are under `audit_runs/upstream_main/certificate_results/`. Both runs completed and were checked by 2026-10-06 21:13:55 PDT (2026-10-07 04:13:55 UTC).

- `arithmetic_bounds.py`: **PASS**, exit 0, complete JSON and log; scalar assertions certified with 512-bit Arb balls or exact integer/Fraction arithmetic. It also checks error budgets for the optional floor scheme; that does not mean the floor matrix scheme was executed.
- `numeric_balls.py`: **PASS**, exit 0, complete success JSON and log, all 37,310 Bernstein and ten tail comparisons certified with 256-bit Arb balls; elapsed 87.29 seconds. The certified minimum Bernstein value is enclosed by `[0.0012061126419378479840360722746555951 +/- 3.42e-38]` (function 2, center 15, half-length .5, coefficient 40, parameter interval [2.36,2.65]). The smallest displayed tail value is enclosed by `[0.0022677195895931693828171025963536304 +/- 1.56e-39]`. Both exceed the strict manuscript margins.

Output SHA-256 bindings:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `numeric_balls_results.json` | 15380 | `d073712180ff38742fabd12c3074f6bc1504f653d97e913a1946cedfedf47635` |
| `numeric_balls_run.log` | 16396 | `8b251e398e37d423df3bc82c1d3faaf9afa530ab0385b595a00945bc056b6365` |
| `arithmetic_bounds.json` | 25194 | `0bb906b0ae21fc3dea59b46f3448665a0c274c95378da27a19841224a29f1c2e` |
| `arithmetic_bounds.log` | 20541 | `23c86bc8c618b0aecc9eea17ef3ffee95545c316f1fba6581644e56dec957c9f` |

## Verdict and remaining work

No substantive analytic flaw was identified in the reviewed core proof route, and its supplied finite interval/scalar certificates reproduced successfully. No numerical agreement has been treated as evidence for an exact constant: the arithmetic is interval enclosure of explicit strict inequalities, with separate analytic proofs connecting them to exact entire functions and all radii/parameters.

The strongest result supported by this audit is the main manuscript's infinite-configuration universal positive-energy theorem, with the exact centered-density, ordered-pair and liminf conventions above. The follow-on constant still requires its own finite periodization bridge, lattice upper construction, precise Hardin--Saff theorem application and attribution/priority audit. This audit supplies neither a claim of microscopic crystallization nor a uniqueness result, and it does not certify a full follow-on theorem in Lean.
