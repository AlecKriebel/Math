# Independent audit: fitness-two dual and local extremality

## Scope and standard of review

This file records an independent audit of the fitness-two duality and local-extremality claims in the disposable referee package. Package prose and software are treated as untrusted claims. No source or declared package payload was edited. (One imported verifier initially generated three ordinary `__pycache__` files; those exact generated files and their two now-empty directories were removed immediately, and the package manifest was then rechecked successfully.) No external contact, commit, or push was made. Delivered software was not executed until its source and wrapper chain had been inspected.

The target claim is Theorem 1 (manuscript p. 5, equations (2.6)--(2.8)): for every fixed `n >= 3`, the uniform complete replacement kernel is a strict nondegenerate local maximizer at mutant fitness two on the full loopless row-stochastic tangent space. The audit separately checks the representation lemmas, the stationary perturbation and sign conversion, the tangent-space representation theory, and each of the three Hessian-sector certificates.

## Timestamped sub-log

- 2026-08-22 12:28 PDT -- Began audit; inventoried the 30-page manuscript, TeX source, and certificate programs; extracted the manuscript by page. Delivered code has not been executed. Best-guess completion: 10%.
- 2026-08-22 12:30 PDT -- Completed static source audit of the package launcher, replay/build/bootstrap chain, every fitness-two/local verifier to be run, and all transitive Python imports. The individual verifiers are read-only exact-arithmetic programs. The all-in-one launcher is intentionally not used because its bootstrap creates a virtual environment and performs a network package installation; the build path also writes generated artifacts. No delivered code had yet been executed at this checkpoint. Best-guess completion: 25%.
- 2026-08-22 12:34 PDT -- Replayed the audited exact-arithmetic fitness-two/local programs individually. All claimed finite ranges, displayed eigenvalues, phase margins, polynomial identities, and normalization bridges passed. Independently solved forward, union-dual, and rectangular active chains on nonsymmetric directed kernels of orders three and four. Best-guess completion: 65%.
- 2026-08-22 12:39 PDT -- Finished hand derivations, an independently written literal-active Hessian computation at `n=3,4,5`, an exact symbolic forward-fixation perturbation check, endpoint/range auditing, and visual inspection of manuscript pp. 5--12 and 17--26. Restored the disposable package after removal of generated caches; `verify_referee_package.py` then reported all 80 package payloads and all 70 archive members matching their manifests. Best-guess completion: 95%.
- 2026-08-22 12:42 PDT -- Completed the written audit and final gap analysis. Best-guess completion: 100% of the assigned fitness-two/local scope.

## Findings

### Executive conclusion

I found no mathematical error, missing population-size range, normalization mismatch, or counterexample in the assigned fitness-two/local argument. Subject to the normal trust placed in exact rational arithmetic libraries, Theorem 1 is independently supported as stated: for every fixed `n >= 3`, the complete kernel has zero first variation and a negative-definite fixation Hessian in every loopless row-zero direction, including directed column-imbalance and circulation directions.

The crucial quantifiers and hypotheses are correctly limited. The proof uses strictly positive off-diagonal kernels, but this loses no tangent direction at the interior point `J_n`; the neighborhood and its radius are allowed to depend on `n`; and nothing in the result proves global fitness-two maximality. The package itself repeatedly labels the global collision inequality as open.

### Evidence map

| Claim | Manuscript location | TeX/source location | Principal verifier location |
|---|---|---|---|
| Theorem 1 and curvature conversion | p. 5, (2.5)--(2.8) | `sections/02_model_results.tex`, lines 35--83 | `paper_db_extremality/verify_paper_claims.py`, lines 285--296 |
| Fair-geometric OR and union dual | pp. 6--7, (3.1)--(3.5), Lemma 6 | `sections/03_duality_collision.tex`, lines 6--60 | `r2_marked_lift_v2/verify_marked_lift.py`, lines 28--80 and 83--136; its exact subset solver is in `verify_resolvent_identities.py`, lines 32--88 |
| Coverage, complete alternation, `rho=m/n` | pp. 7--8, (3.6)--(3.9), Proposition 7 | `sections/03_duality_collision.tex`, lines 62--106 | independently reconstructed in this audit; complete-law bridge also in `verify_paper_claims.py`, lines 40--86 |
| Rectangular spaces, phase order, stationary laws, collision | pp. 8--9, (3.10)--(3.18) | `sections/03_duality_collision.tex`, lines 108--230 | `verify_paper_claims.py`, lines 89--117; `verify_marked_lift.py`, lines 83--155, 240--313, and 422--463 |
| Perturbation and vanishing first variation | p. 10, (4.1)--(4.6) | `sections/04_local_hessian.tex`, lines 1--60 | literal active-chain implementations in `verify_hessian_sectors.py`, lines 89--202, and `verify_paper_claims.py`, lines 285--296 |
| Three tangent sectors | pp. 10--11, (4.7)--(4.10b) | `sections/04_local_hessian.tex`, lines 62--105 | `verify_paper_claims.py`, lines 120--171 |
| Standard sector | pp. 18--21, (A.4s)--(A.23s) | `appendices/A_sector_certificates.tex`, lines 47--245 | `verify_physical_standard_phase.py`, lines 30--143, 186--228, 231--349, and 352--428 |
| Antisymmetric sector | pp. 21--22, (A.4)--(A.10) | `appendices/A_sector_certificates.tex`, lines 247--328 | `verify_antisymmetric_hessian.py`, lines 31--76 and 79--157 |
| Symmetric sector | pp. 22--26, (A.11)--(A.36), Lemma 15 | `appendices/A_sector_certificates.tex`, lines 330--607 | `verify_true_inverse_rank_symmetric_phase.py`, lines 61--167 and 204--359; hash binding in `verify_paper_claims.py`, lines 240--252 |
| Displayed normalized eigenvalues | p. 12, (4.12) | `sections/04_local_hessian.tex`, lines 134--144 | `verify_hessian_sectors.py`, lines 205--225 |

### 1. Fair-geometric OR representation and finite-union dual

The calculation on manuscript p. 6 is exact. For `x=P_{vS}` and `P(L=ell)=2^{-ell}`,

`E[(1-x)^L] = sum_{ell>=1} 2^{-ell}(1-x)^ell = (1-x)/(1+x)`.

Therefore the probability that at least one potential parent is mutant is `1-(1-x)/(1+x)=2x/(1+x)=f_2(x)`, proving (3.2)--(3.3). This representation concerns the mutant-type set (which is all the fixation problem requires); it need not identify the single biological parent chosen by the original update.

The transpose-set map (3.4) satisfies the pointwise Boolean identity underlying (3.5): the forward image hits a query set `A` if and only if the original mutant set hits the transpose image of `A`. Iterating with reversed graphical marks gives the stated distributional duality. Because `L` is finite almost surely, each event has a finite union even though its support is unbounded in `ell`.

The loopless condition is used correctly: all sampled sources differ from the active target `v`, so an update of a proper ancestral set removes `v`, never returns it in that burst, remains nonempty, and cannot become all of `V`. Positivity of every off-diagonal entry is the substantive ergodicity hypothesis. A set of size at least two can be shrunk one vertex at a time with an `L=1` event sampling another current member. From a singleton, one can move to a singleton `{x}` outside any desired proper destination `B`, then use a finite burst at `x` whose samples cover exactly `B`. A passive target outside the current proper set supplies a self-loop. Thus Lemma 6 is valid. The implicit zero-step case when the singleton already equals `{x}` is harmless.

The forward mutant-set chain absorbs almost surely: from every nonabsorbing set, repeatedly choosing a resident target and a positive-weight mutant source gives a positive-probability path to `V`, so no nonabsorbing closed class exists in the finite chain. Starting the dual at `V`, its first update is `V\{v}` and hence enters the irreducible proper-set class. The limiting duality then proves (3.7).

For fixed `A`, the mixed difference of the hit indicator is exactly `(-1)^{|T|+1}` on the event `A cap S=empty, T subset A` and zero otherwise, proving (3.9). Averaging the singleton coverages gives

`rho_dB(P,2) = (1/n) sum_i P(i in A) = E|A|/n = m(P)/n`,

so (3.8) has no missing exchangeability or reversibility assumption.

### 2. Rectangular phases, ordering, stationary laws, and collision

The typing in (3.10) is essential and correct. `Z_n` includes an empty cache; one loopless sample maps every `(C,v)` in `Z_n` to a nonempty `(B,v)` in `Y_n`. The `R` channel maps `Y_n` back to `Z_n`, with the stop branch allowed to empty a singleton. With row laws acting on the right, `K=RA` is retarget-then-sample on `Y_n`, while `M=AR` is sample-then-retarget on `Z_n`. The explicit two-branch description of `K` on p. 8 matches this convention.

I rederived the current identities (3.13)--(3.16). For fixed target `v`, `sigma_v(C)=Pi(C union {v})` is the pre-burst active mass and `eta_v(C)` is exactly the nonnegative active incoming mass to an output not containing `v`. Averaged stationarity gives

`sum_{v notin B} eta_v(B)=|B| Pi(B)`.

The geometric resolvent is `eta_v=((sigma_v+eta_v)/2) A_v`, so `lambda=(sigma+eta)/2` satisfies `lambda A=eta`. Under `R`, the continue contribution to `(B,v)` is `eta_v(B)/2`, while all stop contributions to `(B\{w},w)` total `Pi(B)/2=sigma_w(B\{w})/2`. Hence `eta R=lambda`, `lambda AR=lambda`, and `eta RA=eta`. Both unnormalized laws have total mass `m(P)`.

The active chain is irreducible: a stop/sample event shrinks any cache of size at least two; from a singleton, one or two stop/sample events reach any desired singleton-target pair; continue events add the desired remaining elements. A continue sample already in `B` is a self-loop. Thus `nu=eta/m` is the unique active stationary law. Dividing the current identity by `|B|` yields `nu H=1/m`, proving (3.12).

The collision interpretation uses `M=AR`, as the manuscript carefully emphasizes. The sampled label `I` belongs to the post-sampling cache `B`, which has law `nu`; conditional on stopping, `R` independently chooses `W` uniformly in that same cache. Therefore `P(W=I|B,stop)=1/|B|`, giving (3.18) with the required factor `1/2` before conditioning on stop.

At `J_n`, rank increases with probability `(N-k)/(2N)` and decreases with probability `(k-1)/(2N)`. Its stationary rank law is `binom(N-1,k-1)/2^{N-1}`; conditional uniformity on each transitive rank orbit then gives

`nu_0(B,v)=|B|/[n N 2^{N-1}]`.

Summation gives `c_0=(2^N-1)/(N2^{N-1})=1/m_n`, exactly (3.17).

Independent check: I wrote a separate standard-library rational implementation from the model definition, with no imports from the package. On positive nonsymmetric directed kernels of orders three and four it independently solved (i) the forward fixation equations, (ii) the geometric-union stationary equations, and (iii) both rectangular phase chains. It found exact equality `rho=m/n`, exact `nu H=1/m=1/(n rho)`, and exact phase transport `lambda A=nu`, `nu R=lambda`. For the directed order-three rows `((0,1,4),(2,0,3),(5,7,0))`, for example, it obtained `rho=268034/618135`, `m=268034/206045`, and `nu H=206045/268034`.

### 3. Perturbation expansion and fixation sign

Linearity of `K(P)` makes `Delta` linear in the tangent direction. For the irreducible finite chain, the group-inverse normalization

`G=(I-K_0+1 nu_0)^{-1}`

is valid. Differentiating stationary row laws with normalization `nu_e 1=1` gives coefficient-by-coefficient

`nu_1=nu_0 Delta G`, `nu_2=nu_0 Delta G Delta G`,

where `nu_2` is the coefficient of `epsilon^2`, not the second derivative. This is exactly (4.5).

The rank projection calculation is sound. Applied to a rank function, the continue branch of `Delta` is `(f_{k+1}-f_k)/2` times the signed mass sampled outside `B`; the stop branch is `(f_{k-1}-f_k)/(2k)` times the signed mass sampled inside `B\{w}`. Uniform fixed-rank averaging reduces these to row sums of `delta`, so `S Delta S=0`. Since `q`, `Gq`, and `nu_0` are rank-symmetric, the first variation vanishes without reversibility.

Thus

`1/(n rho_e)=c_0+R_n^(2)(delta) epsilon^2+O(epsilon^3)`.

Inverting, with `m_n=1/c_0`, gives the coefficient of `epsilon^2` in fixation as `-(m_n^2/n)R_n^(2)(delta)` and the second derivative as `-2m_n^2 R_n^(2)(delta)/n`, exactly (2.8). There is no lost factor of two.

Adversarial exact check: for `n=3` and the genuinely directed tangent

`delta=((0,1,-1),(2,0,-2),(3,-3,0))`,

an independently constructed symbolic forward chain gives

`rho(J_3+epsilon delta,2)=4/9-(12352/8019)epsilon^2+O(epsilon^3)`

with zero linear term. Its column-sum vector is `(5,-2,-3)`. The standard component has squared norm `76/3`, the antisymmetric-balanced remainder has squared norm `8/3`, and the table eigenvalues give

`R_3^(2)(delta)=(1/11)(76/3)+(1/9)(8/3)=772/297`.

Since `m_3=4/3`, the predicted fixation coefficient is `-(m_3^2/3)(772/297)=-12352/8019`, exactly matching the direct forward solve.

### 4. Tangent decomposition, dimensions, and norm conversions

The tangent dimension is `n(n-1)-n=n(n-2)`. If `s_j=sum_i delta_ij`, then `sum_j s_j=0`. Direct summation of (4.8) shows that `E(s)` has zero row sums and column-sum vector `s`. Therefore `B=delta-E(s)` is row- and column-balanced, and its symmetric and antisymmetric parts remain balanced.

The three pieces in (4.9) are Frobenius-orthogonal. `E(s)` is orthogonal to every balanced matrix because its inner product is a linear combination of that matrix's row and column sums; symmetric and antisymmetric matrices are mutually orthogonal. Their dimensions are respectively

`n-1`, `n(n-3)/2`, `(n-1)(n-2)/2`,

which sum to `n(n-2)`. The symmetric kernel is absent at `n=3`. The stated Specht modules are pairwise nonisomorphic (including the low-order degeneration), so the polarization of the invariant quadratic form has no cross-sector terms and is scalar on each sector.

The standard embedding norm is

`||E(s)||_F^2=(n-1)||s||^2/[n(n-2)]`.

Combining this with (A.12s) gives the Frobenius-normalized standard eigenvalue `Phi_N/[4N(N+1)]`; the conversions `2/33 -> 1/11` at `n=3`, `261/5120 -> 87/640` at `n=4`, and `3434/85971 -> 8585/57314` at `n=5` are exact. The symmetric formula (A.17) is already divided by `||delta||_F^2`; the antisymmetric formula (A.10) explicitly factors out `T=||delta||_F^2`.

An independently written literal-active exact calculation (building `K_0`, `Delta`, and `G` directly) reproduced the complete table (4.12):

| `n` | standard | symmetric | antisymmetric |
|---:|---:|---:|---:|
| 3 | `1/11` | absent | `1/9` |
| 4 | `87/640` | `3/208` | `57/640` |
| 5 | `8585/57314` | `359/26660` | `143/2100` |

### 5. Standard-sector certificate and all ranges

The signed `P/Q/R` quotient, reward, and normalization are mutually consistent. The physical feature conjugacy `T(a,b)=(P=a,R=b,Q=a-b)` is checked symbolically in `verify_physical_standard_phase.py` lines 186--228 and 243--263; its source/output scales give (A.12s), rather than merely preserving sign.

The radial recurrence (A.3) follows from the complete rank chain. Solving it gives (A.3a). I checked the binomial-tail formula and both bounds independently, including `N=2`. The proof of the lower bound covers `k=1` separately, `k<=N/2` using the full binomial sum, and `k>N/2` by binomial symmetry; no endpoint is omitted.

For the phase proof:

- `(I-Q)W>=q` is established for `N>=6`; the `k=2` lower margin is `2(N-2)(N-6)/(3N)`, so equality at `N=6` is allowed.
- The shifted interior polynomial (A.16s) is positive for integer `a=k-3>=0` and `m=N-k>=0`: the only visibly signed part `6m^2-22m+32` has discriminant `-284`, and `2am(m-1)>=0` for integral `m`.
- The return bound is `A1 <= 2/(N+1) 1`.
- The lower first-phase barrier is available for `N>=7`; the final tail estimate is used only for `N>=10`.
- For `N>=10`, the exact lower bound is `Phi_N >= 2N(N-9)/(N-1)>0`; at the analytic endpoint `N=10` it equals `20/9`.
- The exact rational solves cover every omitted order `2<=N<=9`, with

  `Phi_2=24/11`, `Phi_3=261/40`, `Phi_4=343400/28657`, `Phi_5=2268275/128288`,

  `Phi_6=5758562957/248448224`, `Phi_7=141339691089527/4988552903680`,

  `Phi_8=15468663676289/466560376100`, and `Phi_9=19782952499295763/524622207176704`.

Hence the standard sector is positive for all `N>=2`, equivalently all `n>=3`, with no range gap.

### 6. Antisymmetric-sector certificate

For antisymmetric balanced `delta`, the first perturbation reduces to `(d_k/2)x(B,v)`. The heat-bath coupling proof of `d_1>...>d_{N-1}>0` is valid: two rank chains differing at one distinguished bit coalesce on its first refresh, and adding a second occupied common bit strictly reduces every pre-coalescence forcing difference.

The feature Poisson recurrence (A.8) implies by backward induction

`0<=r_{k+1}<r_k<=N d_k/(N+1)`.

In (A.10), every term is nonnegative, and for every nonzero direction at least one positive-rank contribution is strict. The denominator `N-1` is harmless at the smallest case `N=2`. Thus this sector is proved for every `N>=2` analytically, with no finite extrapolation. The exact package solver additionally checks the recurrence through `n=40`, its listed values through `n=12`, and literal active chains through `n=7`; all passed.

### 7. Symmetric-sector certificate and all ranges

The symmetric source `(d_k/2, d_{k-1}/(2k))` follows directly from (4.3a). I independently checked the fixed-count moments in (A.17a): zero row sums give

`E[x^2|v]=k(N-k)R_v/[N(N-1)]`,

and separating the two coincidence patterns from the all-distinct ordered triples gives

`E[xz|v]=-2k(k-1)(N-k)R_v/[N(N-1)(N-2)]`.

This validates the sign and factor two in the physical normalization (A.17). The literal active-chain calculation above agrees with that normalization at `n=4,5`; the package's independent labelled orbit implementation checks it through `n=12`.

The Schur identity (A.19) correctly retains the alternating inverse `(I+A)^{-1}` and the bad-channel debt; it does not make the invalid inference that a first excursion alone controls all returns. For the phase bounds:

- The supersolution (A.22) is valid from `N=24`. For `N>=25`, the cubic `P_N(k)` has positive leading coefficient, positive value at zero, and negative discriminant, hence its unique real root is negative; the isolated `N=24` physical minimum is exactly `24`.
- The contraction is `c_N=(2N-5)/[2N(N-2)]` and the occupation row `ell_bar` is positive in the range where used.
- Exact solves cover every `3<=N<=39` (the sector begins at `N=3`, i.e. `n=4`).
- Exact rational phase checks cover all 248 integers `40<=N<=287`. I independently recomputed these margins from (A.20), (A.30), and (A.32); the minimum is uniquely attained at `N=40` and equals

  `639304267467075678841 / 115369588296792467144716`, approximately `0.00554136`.

- For `N>=288`, `sqrt(N/2)<=N/24` (equality at `N=288`), leading to the lower bound on `t_j`. The shifted discriminant polynomial in (A.35) has all positive coefficients. Because `G_N` has positive leading coefficient and positive value at zero, its unique real root is negative, so `beta_N<19/20` on every physical rank. Separately, `epsilon_N<1/20` follows from `22N^2-1066N+2555>0` for `N>=46`, hence certainly for `N>=288`.

These ranges are contiguous and exhaustive: `3--39`, `40--287`, and `>=288`. The source hash printed in the manuscript is correct: `b4d45a83ce5f21a1fd3e09403b376e071330290a01affff64711574b69e024bc`.

### 8. Software audit and replay results

Before execution I inspected the package-level checker and launcher, all shell wrappers, every local verifier used here, and every transitive imported module. The individual mathematical programs import only standard-library exact arithmetic, SymPy, and python-flint; they make no network calls, spawn no subprocesses, and contain no filesystem writes. The release/build/bootstrap utilities do write outputs, and `bootstrap_replay.sh` performs a pinned package installation, so I did not invoke the all-in-one launcher. I created a disposable environment outside the package with the declared versions (`sympy 1.14.0`, `python-flint 0.9.0`, `mpmath 1.3.0`) and ran the audited mathematical programs individually.

Successful exact replays:

- `verify_paper_claims.py`: active law, phase typing, tangent decomposition, norm conversion, and curvature sign all passed.
- `verify_r2_determinant.py`: exact order-three active determinant passed; it correctly labels the all-order global determinant sign as open.
- `verify_marked_lift.py`: union/active stationary factorization and collision normalization passed; it correctly labels global fitness-two maximality as open.
- `verify_antisymmetric_hessian.py`: all analytic recurrence checks and literal small-chain checks passed.
- `verify_physical_standard_phase.py`: all symbolic identities, barriers, normalizations, and `N=2--9` values passed.
- `verify_true_inverse_rank_symmetric_phase.py`: exact `N=3--39` solves, all `N=40--287` margins, and the `N>=288` polynomial certificates passed.
- `verify_hessian_sectors.py`: literal labelled orbit reductions for all three physical sectors through `n=12` passed.
- `verify_local_complete_hessian.py`: the independent regular/symmetric slice passed.
- `verify_complete_refresh_forest.py`: its triangle proof and finite hostile screens passed, while correctly retaining its unrelated all-order forest-coefficient question as open.

After cleanup of the three generated interpreter cache files, the independent package checker reported:

- 80/80 package payload files match `PACKAGE_MANIFEST.sha256`;
- 70/70 source-archive members match the internal manifest;
- archive SHA-256 `b1b7b7c4c9393ee4fa85eeacd54cefc4bcc94a3eca759d500c9ee6a362eddd2b`;
- PDF SHA-256 `a6bda621b764ca8ee86658f6b68de0245790b84315eb77a6cc7ca45f7953bd2d`.

The rendered relevant pages (5--12 and 17--26) have no clipped equations, missing symbols, or visually ambiguous range endpoints.

### 9. Adversarial checks and boundary cases

- **Directed, nonreversible directions:** explicitly included in the independent nonsymmetric-kernel and mixed-sector perturbation checks; no reversibility was used in the dual/current derivation.
- **`n=2`:** the normalized loopless kernel space is a singleton, so tying the baseline is correct; Theorem 1 properly begins at `n=3`.
- **Absent symmetric sector:** its dimension `n(n-3)/2` is zero at `n=3`; the symmetric proof correctly begins at `N=3` (`n=4`).
- **Positive-kernel assumption:** essential for the simple irreducibility proof but harmless for local tangent coverage because `J_n` is relative-interior and every fixed tangent direction remains positive for sufficiently small two-sided `epsilon`.
- **Analytic versus global claim:** the proof supplies an `n`-dependent ball via finite-dimensional positive definiteness and a uniform third-derivative bound on a compact smaller ball. It supplies neither an explicit radius nor a radius uniform in `n`, and it never claims either.
- **Counterexample search:** exact random/extreme nonsymmetric kernels did not break `rho=m/n`, the phase identities, or collision normalization. A mixed standard/antisymmetric direction did not produce a linear term or an escaping Hessian direction. The package's own hostile examples refute stronger global/stochastic-domination routes but not the local theorem, and are appropriately labeled.

### Verdict within assigned scope

**Fully validated within the fitness-two dual/local-extremality scope.** I found no correction required for the theorem statement or proof. The computer-assisted symmetric finite range is finite, exact, correctly hashed, and joined without gaps to the analytic tail.

## Strongest verified result

For every fixed `n>=3` and every nonzero loopless row-zero matrix `delta`, the exact quadratic form

`R_n^(2)(delta)=nu_0 Delta G Delta G(H-c_0 1)`

is strictly positive. Its three Frobenius-orthogonal irreducible sector scalars are positive over all required population sizes: standard for `N>=2`, antisymmetric for `N>=2`, and symmetric for `N>=3`. Consequently

`d rho(J_n+epsilon delta,2)/d epsilon |_{0}=0`

and

`d^2 rho(J_n+epsilon delta,2)/d epsilon^2 |_{0}=-(2m_n^2/n)R_n^(2)(delta)<0`.

Finite-dimensional analyticity upgrades these directional statements to a strict, nondegenerate, `n`-dependent local maximum of fixation at `J_n` in the full directed normalized kernel space.

## Exact remaining gaps

There is no unresolved gap in the assigned theorem after this audit. The following are deliberately outside the proved claim or are ordinary limits of computer-assisted verification:

1. Global maximality `rho_dB(P,2)<=rho_dB(J_n,2)` remains open; neither the local Hessian theorem nor the replay claims otherwise.
2. The proof gives no explicit local radius and no radius uniform in `n`.
3. The symmetric finite range `3<=N<=39` ultimately relies on exact system solves implemented with python-flint. I inspected the construction and independently matched literal active chains at `n=3,4,5`; the package independently matches labelled orbit chains through `n=12`, but I did not author a second full solver for all 37 small symmetric orders. This is a reproducibility limitation, not an identified mathematical gap.
4. As usual for machine-checked rational certificates, correctness assumes the Python interpreter and exact-arithmetic libraries execute their documented integer/rational operations correctly. All input source, hashes, boundaries, and asserted outputs are available and replayed.
