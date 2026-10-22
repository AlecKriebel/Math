# Independent exact, endpoint, and exponent audit

Row 1795, shared pass 1/5. Authored mathematical verification. This audit uses the explicitly corrected contract, `0 < psi <= phi < 1`, and does not claim that the remaining arithmetic conjecture is proved. Finite tests below are regression support; the arguments establish the assertions.

## Executive findings

1. The prescribed Ramanujan density is holomorphic at the four-shift collisions and its four mixed numerator/denominator derivatives give exactly the Hardy–Littlewood density, with signs `(+,−,−,+)`.
2. The reverse proof in `../reverse/REVERSE_THEOREM.md` passes this independent line-by-line audit, including its exact Cauchy constant, prime powers, odd gaps, endpoint atoms, non-even weights, and density-convention bound.
3. Sharp Fourier support and the forward error exponents pass. The corrected parameter range is nonempty, for example `(phi,psi,lambda)=(3/4,1/4,6/5)`.
4. The original hypothesis is inconsistent if `psi > phi`; a self-contained proof appears in `NONVACUITY_OBSTRUCTION.md`. The contract's explicit restriction is necessary, not just a simplification.
5. Independent local algebra confirms the correction to CK2016 v2: the Ramanujan Mellin expression produces `B_{−beta,−alpha−s,gamma+s,delta}(1)`, not the printed `B_{−beta,−alpha,gamma,delta}(1+s)`. The subsequently completed full Euler/Mellin artifact has also passed this independent audit, including its required whole-line low-time term; see the dated acceptance section below.

## 1. Exact finite coefficients and all four signs

Write `A=p^(−alpha)` and `C=p^(−gamma)`. Since the only nonzero Möbius terms in a prime-power divisor sum have `e=1,p`,

`I_(alpha,gamma)(1)=1`, and `I_(alpha,gamma)(p^k)=A^k−CA^(k−1)` for every `k>=1`.

The divisor definition is multiplicative. At a common real shift `r`,

`I_(r,r)(n)=n^(−r) 1_(n=1)`.

The convolution identities `mu * 1 = epsilon` and `mu * log = Lambda` give, exactly,

`partial_alpha I|_(r,r) = −n^(−r)Lambda(n)`,

`partial_gamma I|_(r,r) = +n^(−r)Lambda(n)`.

For the second identity, use `log e=log n−log(n/e)`; the leftover term is `log n * 1_(n=1)=0`. In particular a prime power `p^k` contributes `log p`, not `k log p`, and `n=1` contributes zero to either derivative.

The four cross-pair derivatives `(alpha beta, alpha delta, gamma beta, gamma delta)` of the finite ratios integral consequently produce `(+,−,−,+)` times the prime-power second moment. This is exact for finite `N`; there is no infinite-series differentiation or quotient-of-zeta approximation. The un-differentiated ratios functional at the collision is `T w_hat(0)`.

## 2. Normal convergence and Hardy–Littlewood local factors

Choose a sufficiently small fixed `eta>0`, with `eta<1/8`, such that `g(v)=1/zeta(1+v)` is holomorphic for `|v|<2 eta`. Existence follows from the removable analytic function `v zeta(1+v)`, whose value at zero is 1. On `max|shift|<eta`,

`|F_(alpha,gamma)(p) F_(beta,delta)(p)|/p^2 <= C_eta p^(−2+4 eta)`.

For a fixed positive gap `h`, `c_p(h)=-1` except at the finitely many primes dividing `h`, where `c_p(h)=p−1`. Thus the squarefree Ramanujan series and its Euler product converge absolutely and normally on this fixed neighborhood. The vanishing of a local factor creates no singularity: no logarithm or division by that factor is taken. The microscopic polydiscs lie in this neighborhood for all sufficiently large `T`, uniformly in `a`.

At a collision,

`F_(r,r)(p)=−p/(p−1)`, and `F_(r,r)(q)^2/q^2=mu(q)^2/varphi(q)^2`.

The local factor is therefore `1+c_p(h)/(p−1)^2`. If `p|h`, this is `p/(p−1)`; otherwise it is `p(p−2)/(p−1)^2`. These are precisely `(1−nu_p(h)/p)/(1−1/p)^2`. At `p=2` an odd gap gives zero. For an even gap,

`S(h)=2 C2 product_(p|h,p>2) (p−1)/(p−2)`,

where `C2=product_(p>2)(1−1/(p−1)^2)>0`. Hence `S(h)>=2 C2` for every positive even gap. The valuations of primes dividing `h` are irrelevant, as required by the residue-class obstruction. This argument does not apply at `h=0`: the diagonal is kept exact and is not represented by this divergent zero-gap Ramanujan series.

Because `g(v)=v+O(v^2)`, both reciprocal-zeta factors in the cumulative profile vanish at a collision. Only the terms differentiating both of these factors survive any of the four cross-pair derivatives. The result is

`(+,−,−,+) S(h) x^(1−2r)/(1−2r)` for the cumulative profile,

and `(+,−,−,+) S(h) x^(−2r) dx` for its density.

No derivative of the Ramanujan product or of the `x` power contributes to these particular derivatives. All signs and collision values are established before using a finite test.

## 3. Mean singular-series bound and density convention

For odd squarefree `d`, set `a(d)=product_(p|d)(p−2)^(−1)`; set it to zero otherwise. Expanding the positive factors gives

`S(2k)=2 C2 sum_(d|k) a(d)`, and `S(2k+1)=0`.

Consequently, for every real `H>=0`,

`sum_(1<=h<=H) S(h) = 2 C2 sum_d a(d) floor(H/(2d)) <= H`,

because `C2 product_(p>2)(1+1/[p(p−2)])=1`, prime by prime. This is an exact inequality, not merely an asymptotic average.

Put `eta_T=exp(2 pi A/T)−1` and `W=||w_hat||_infinity`. For `r>=0`, `x>=1`,

`0 <= x^(−2r)−x^(−r)(x+h)^(−r) <= r h/x`.

The kernel has magnitude at most `W/x` and is zero below `L_h=h/eta_T`. Thus one orientation contributes at most

`W r h integral_(L_h)^infinity x^(−2) dx = W r eta_T`.

After both orientations, the factor `T`, and the singular-series sum, the difference of the two explicit prime main terms is at most

`2 T W r eta_T H_T = O_(A,w,a0)(N/(T log N)) = o(T)`.

At `r=0` the density conventions agree exactly. This proof requires neither a prime number theorem nor a fixed-gap prime-pair conjecture. It also shows why the harmless near-diagonal kernel convention error cannot justify using the same approximation over an arbitrarily large arithmetic `h` range.

## 4. Sharp support, endpoints, and orientations

The Fourier sign convention in the gate gives the positive orientation when the second index is `n+h`, and the negative orientation when the first is `n+h`. No conjugation is inserted for general complex shifts. For real `w`, the two Fourier kernels are conjugates, even when `w` is not even.

For either orientation, nonzero support requires

`T log(1+h/x)/(2 pi) < A`, hence `x > L_h=h/eta_T`.

Retaining equality is harmless because a smooth compactly supported Fourier transform vanishes at `+A` and `−A`, with all derivatives. Combining `x<=N−h` gives exactly

`h <= N eta_T/(1+eta_T) = N(1−exp(−2 pi A/T))`.

Thus the specified floor `H_T` is correct, including an exact equality at its boundary. Since the unfloored value is strictly less than the integer `N`, always `H_T<=N−1`. Empty sums and intervals are zero. The coefficient cutoff remains sharp.

For `T>2 pi A/log 2`, `L_h>1` for every gap. Consequently `n=1` off-diagonal terms vanish, and either convention for a possible profile atom at `1` gives zero. A fixed small-`x` exception `x<x0` in the arithmetic hypothesis is bypassed once `T>=2 pi A/log(1+1/x0)` (with equality again a zero kernel).

For the corrected range `0<psi<=phi<1`, on the kernel support,

`h/x^psi <= eta_T x^(1−psi) <= eta_T N^(1−psi) = O(T^(lambda(1−psi)−1))`.

The strict exponent condition therefore puts every required point inside the arithmetic hypothesis for all sufficiently large `T`. A hypothesis that only controls real shifts would not suffice for the later Cauchy step.

Writing `M*=||w_hat||_infinity+A||w_hat'||_infinity`, direct differentiation gives `|K'_h(x)|<=M*/x^2`: the Fourier-argument derivative uses `y/(1+y)<=log(1+y)` on support. Stieltjes partial summation of an error `|E(x,h)|<=C x^phi` then costs at most

`C M* L_h^(phi−1)/(1−phi)` per orientation.

The upper-endpoint term is included in this bound; it is combined with the derivative integral, not silently dropped. Since `sum_(h<=H) h^(phi−1)<=H^phi/phi`, the total is at most

`2 C M* T eta_T^(1−phi) H_T^phi/[phi(1−phi)] = O(N^phi)`.

This verifies the forward proof's endpoint and power calculation independently.

## 5. Cauchy loss and nonempty length range

If the holomorphic finite-ratios error is bounded by `epsilon` on the closed four-polydisc of radius `rho`, two ordinary Cauchy circles give

`|partial_alpha partial_beta E(Delta_r)| <= epsilon/rho^2`.

The exact constant is 1 and there is no factorial beyond `1!1!`. The example `E=epsilon(alpha−r)(beta−r)/rho^2` shows the general bound cannot be improved. The remaining two variables may be frozen at the center. The other three mixed derivatives satisfy the same bound.

Under `epsilon=O(N^phi)`, this is `O(c^(−2)N^phi(log N)^2)=o(T)` by `lambda phi<1`. It is an absolute error, so no positivity of `w`, lower bound on a main term, or relative asymptotic is assumed.

For `0<psi<=phi<1`, set `U=min(2,1/phi,1/(1−psi))`. Every number in `(1,U)` is admissible, and `U>1`. In the explicit example `(3/4,1/4,6/5)`, both controlling products equal `9/10`. No uniformity up to the strict boundaries is asserted.

## 6. Independently audited correction to the printed Mellin shifts

Let `v=alpha+beta+s`. Initially where the `h`-Dirichlet series converges absolutely,

`sum_(h>=1)c_q(h)h^(−v)=zeta(v)q^(1−v) product_(p|q)(1−p^(v−1))`.

Multiplication by `chi(1−v)` replaces `zeta(v)` by `zeta(1−v)`. Put

`t1=p^(−1+alpha−gamma)`, `t2=p^(−1+beta−delta)`, `u=p^(−1−gamma−delta−s)`.

After including the two reciprocal-zeta factors, the numerator of each local factor is exactly

`(1−t1)(1−t2)+u−t1*t2 = 1−t1−t2+u`.

Together with `zeta(1−alpha−beta−s)`, this is the Rankin–Selberg series

`B_(−beta,−alpha−s,gamma+s,delta)(1)`.

The printed `B_(−beta,−alpha,gamma,delta)(1+s)` instead has `s` in the two cross denominators and the opposite placement in the numerator-sum zeta factor. The local factors are not identical. For example at `p=2`, all original shifts zero, and `p^(−s)=2/3`, the corrected local factor is `4/3` and the printed one is `1`.

There is also a global meromorphic sanity check away from pole intersections: when all four original shifts are zero, every positive-gap Ramanujan profile is zero, so its convergent `h`-Dirichlet transform is zero and its continuation remains zero. The printed `B_(0,0,0,0)(1+s)` equals 1 identically. At `s=0` joint meromorphic pole intersections require special handling; this audit does not assert continuity of the separated swap pieces there.

CK2016 v2 itself displays the shifted arithmetic factor `A_(−beta,−alpha−s,gamma+s,delta)` in its page-9 calculation. The correction above follows from independent algebra, not from treating that display as authority. Any source-based contour extraction requiring GRH must retain that qualification; the elementary finite coefficient, local factor, and reverse Cauchy arguments here do not require it.

## 7. Reproducible finite checks and limits of this audit

Run `python exact/verify_exact.py` from the witness directory without Python optimization; the package verifier supplies assertion-enabled isolated replay under every caller optimization mode. `EXACT_RESULTS.json` records passing exact tests of 2,000 coefficients, 5,200 Hardy–Littlewood local factors, 3,050 squarefree Ramanujan cases, 500 finite-product mean bounds, and 5,550 sharp-support cases. Prime powers, `n=1`, odd gaps, endpoint equality, the corrected nonempty exponent example, and an excluded original-range example are explicit. Formal logarithm vectors and rational arithmetic avoid floating-point cancellation.

The finite-prime mean test includes the matching finite reciprocal Euler product; truncating only `C2` would not by itself certify an inequality for the infinite singular series. All infinite products and their limits are justified in the arguments above.

This independently certifies the exact/reverse/endpoint components and the necessity of the contract correction. Acceptance of the separately supplied full correspondence follows in the final section.

## 8. Completed cross-artifact acceptance, 2026-10-16

The finalized `../forward/FORWARD_TRANSFER.md`, `../forward/SHARP_TO_LINEAR_COMPARISON.md`, `../reverse/REVERSE_THEOREM.md`, and `../euler/EULER_AND_MELLIN.md` were each read and mathematically checked. Their audited versions are pinned by SHA-256 in `AUDIT_RECEIPT.json`.

The strengthened sharp-to-linear comparison uses `sum_(h<=H)|D_z(h)| <= C H/(log N)^2`, obtained by the exact squarefree identity `|c_q(h)|=product_(p|q)(1+(p−2)1_(p|h))` and positive divisor expansion. It gives the uniform comparison `O(N/(T(log N)^2))` and mixed-derivative error `O(N/T)=o(T)`. All strips from replacing `N−h` by `N`, including the added gaps beyond `H_T`, are included. In the amended range, `lambda−1<lambda psi<=lambda phi`, so this comparison is also `o(N^phi)` before differentiation.

The Euler/Mellin audit checked the absolute interchange defining `J_z(k)`, its genuinely convergent product, its sole contour-crossing pole at `k=1`, the corrected `B*` variable allocation, the `T,N,2pi` scaling in Mellin inversion, the cosine-transform normalization, and the finite-height order-of-integration convention. The residue is exactly

`2 pi w(0) N^(1−alpha−beta) g(gamma−alpha)g(delta−beta)/(1−alpha−beta)`.

It is generally of order `N/(log N)^2` and cannot be dropped. Its mixed numerator derivative at the common collision is `2 pi w(0)N^(1−2r)/(1−2r)`. Both facts are correctly retained in the artifact. The ordinary `k=1/2` time moment is integrable; the corresponding `k=2` ordinary time moment is not incorrectly used. The vertical-tail and horizontal-segment bounds are sufficient and vanish with their height parameter. The diagonal's literal Perron formula uses `N+1/2`, which includes exactly the integers through `N` and avoids a half-weight endpoint error.

The direct frozen-density arithmetic identity is genuinely proved without GRH, by a nonempty absolute-convergence domain followed by meromorphic continuation. The separate claim identifying it with the original additive-twist double-residue object retains CK's GRH qualification and is not asserted unconditionally. Combined holomorphy is established on fixed contours, rather than by separately evaluating meromorphic pieces at a polar intersection.

No error was found in these completed mathematical components. The exact, reverse, forward, and corrected zero/one-swap proofs therefore pass this independent exact audit for the explicitly amended finite-polynomial witness. This is not a proof of the arithmetic hypothesis, an unrestricted source resolution, a novelty claim, or a statement of individual fixed-gap Hardy–Littlewood.
