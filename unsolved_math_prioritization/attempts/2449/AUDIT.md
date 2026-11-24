# Audit of the proposed resolution of Erdős Problem 1038

## Disposition

The full proposed resolution remains unaccepted in this audit. Its matching lower bound, unique minimizing parameter, and nonattainment assertion depend on two computational certificates that were not executed or independently reproduced. No counterexample to the proposal was found.

A substantive part is independently established: independent rational arithmetic and the complete recovery proof show

    inf |{x : |f(x)|<1}| < 1.834430475762662

for nonconstant monic real polynomials with all roots in [-1,1]. This is a reproduction of the proposal's one-cut upper construction, with attribution to Wang and Tao; it is not a new resolution. The complete argument and exact rational witnesses are in INDEPENDENT_UPPER_BOUND.md. CHECK_SUMMARY.json gives aggregate verification metadata; checker code and raw computational output are outside this report.

The public proposal explicitly labels itself proposed. Its use of interval arithmetic should not be described as ordinary sampled floating-point optimization. Conversely, its statement that an interval verifier certifies all remaining signs is not an independent verification receipt.

## Target and sources

The target is database problem ID 2449, EP-1038: determine both extrema of the Lebesgue measure of the strict sublevel set of a nonconstant monic real polynomial whose roots are all real and in [-1,1]. EHP's original Problem 1, printed page 131, has the same root-location and measure target. The original introductory notation defines a monic product and the strict inequality |f|<1. For finite nonconstant polynomials, changing the boundary convention to <= does not change the measure, since f^2-1 has finitely many real zeros; no analogous blanket substitution is made for continuous root measures.

Primary sources inspected:

- Shouqiao Wang, A Proposed Complete Solution to Erdős Problem 1038, [PDF](https://multiscalar.ai/results/erdos-1038/paper.pdf). 29 pages, 488289 bytes, SHA256 3a7e857b12e59f24af17f36a30030b0ad6368c2d59955ef58e643400917565ad. Captured 2026-10-11 at 22:56:31 UTC. PDF metadata states creation on 2026-07-22; this is metadata, not an independent publication date.
- The proposal's [public result page](https://multiscalar.ai/results/erdos-1038/), inspected 2026-10-11. It labels the result Proposed and links the PDF, numerical verifier, and Lean project.
- The companion [numerical_verifier.py](https://multiscalar.ai/results/erdos-1038/numerical_verifier.py), captured 2026-10-11. 3335 lines, 110762 bytes, SHA256 e84b94b40a27d2f3e254d4d14393a49c79ac4db57e4b55010441d4e04eff9616. Static inspection only.
- Terence Tao, Superlevel sets of logarithmic potentials, note dated 2025-12-27, [PDF](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf). 359077 bytes, SHA256 7ef1d231d1689873bafba3bbe5e70710bc605eee245d71614f3abd0917824d41. Theorem 2.1 supplies the already-known supremum and equality characterization. The present audit checked its statement and specialization, not its entire proof or numerical scalar inputs.
- P. Erdős, F. Herzog, and G. Piranian, Metric properties of polynomials (1958), [PDF](https://users.renyi.hu/~p_erdos/1958-05.pdf). 4304732 bytes, SHA256 5d20ad770563e425ac3343e31581859a24facabf744f10489b8f8d201b0ec12a. Introductory definitions and original Problem 1 inspected; printed page 131 visually checked.

## Actual inspection and confidence limits

The entire extracted text of the 29-page proposal was read. The endpoint-adjoint coefficient calculation on page 14 and the circle energy/rearrangement calculation on page 18 were additionally inspected as rendered pages. Algebra, signs, and the interfaces between Sections 2-9 were checked as described below. The proof's cited rearrangement theorem and Pringsheim theorem remain standard external mathematical inputs; their original publications were not independently re-proved here.

Static verifier inspection covered the driver and dependency routing, core conversion functions and Family data class, the proposal-only crossing solver, the one-cut certificate section, the exact small-k section, affine prerequisites, the affine/constant scalar cover, and both terminal scalar sections. Most of the older mixed-interval machinery embedded in lines 60-1007 is not called by these final certificate paths and was not reviewed line by line. The optional Tao upper-scalar certificate was not audited because it is not a logical input to the paper's lower-bound proof.

Neither the author's Python file nor the linked Lean project was executed. No Lean acceptance claim is made. The only mathematical program executed was an independently developed exact-rational checker. It imports no author code. The final standard-library replay uses explicit exception checks and passed under normal Python, -O, and -OO with byte-identical output; the implementation-only change and aggregate receipts are recorded in CHECK_SUMMARY.json. The report preparation also replayed the same checker in all three modes with unchanged output. Checker code and raw output are excluded; exact mathematical witnesses remain in the proof appendix.

## Analytic reductions

### Finite atomization and normalization

The empirical-potential identity is exact: for degree n, the root probability mu satisfies V_mu=(1/n)log|f|. The sublevel set lies in (-2,2).

The component-collapse argument has the correct direction. Outside each old component, t -> log|x-t| is concave on that component; Jensen raises the potential when its roots collapse to their barycenter. Therefore the new negative set is contained in the old one. Each old component contains a root, since otherwise strict concavity and zero boundary values would preclude negativity. The new potential has a single pole in each old component, and concavity on each side of that pole prevents additional components without poles. This gives one cluster per new component, not merely a local decrease in width.

The mean orientation is also valid. For x in (-1,0), |x-t|<=1-xt and Jensen imply V_mu(x)<=log(1-xm)<=0 when m<=0. Equality throughout is impossible. The leftmost cluster c can then be translated to -1 without moving any root outside [-1,1] or making the mean positive. At the translated main-component boundary beta, the weighted geometric/arithmetic mean argument gives A>=1/2. The beta=0 case must be treated separately; the paper does so, forcing the residual roots to 1 and using the nonpositive mean. Thus the normalized form is

    W(x)=k log|x|+sum_i q_i log|x-d_i|,
    k>=1, 1<=d_1<...<d_N<=2, q_i>0, sum_i q_i=1.

The residual components are distinct from the main one, including the possible single-point contact case. This distinction is essential later.

The residual radius bound has the correct reversed inequality after division by -q_i. Removing the self-pole leaves a strictly concave background on the residual component. If its left/right distances from d_i are s,u and T=s+u, concavity yields

    R_i <= s^(u/T)u^(s/T) <= T/2.

The main component contains (-rho(k),1), where rho^k(2+rho)=1, hence its width is at least 1+rho(k)>=sqrt(2). These reductions are valid for the finite configurations to which the proof applies.

### Elementary range

For 1<=k<=K=29/20, separation gives b with W(b)>=0. Writing y_i=2-d_i, Jensen yields

    sum q_i y_i <= 2-b-b^(-k)
                  <= epsilon_K=2-(K+1)K^(-K/(K+1))<1/25.

Here b>=1 follows from b^k(2-b)>=1. The maximum of 2-b-b^(-K) occurs at K^(1/(K+1)). The exact bound on epsilon_K follows from exp(3/8)>29/20 and the cubic lower Taylor bound for exp(-87/392). The independent checker reproduces the positive rational margin 522631/245862400 in that step.

Let Q=sum q_i^2, t=1-Q, S=sum R_i. Concavity of log and |d_i-d_j|<=y_i+y_j give

    2 sum_{i<j} q_i q_j log|d_i-d_j| <= t log(2epsilon_K/t).

For t=0, the pair sum and its continuous limiting expression are zero. The definition of R_i gives

    sum q_i^2 log R_i
       = -k sum q_i log d_i -2sum_{i<j}q_iq_j log|d_i-d_j|.

Since d_i<=2, weighted AM-GM with weights q_i^2/Q implies

    Q log(3S) >= log 3-k log 2-t log(6epsilon_K/t).

The bound t log(c/t)<=c/e, epsilon_K<1/25 and e>8/3 bound the final term strictly by 9/100. Exact atanh estimates give log3>263/240 and log2<1123/1620. The remaining margin is

    263/240-(29/20)(1123/1620)-9/100=11/16200>0.

Therefore S>1/3, and the total width is greater than sqrt(2)+2/3>2. The independent exact checker verifies all finite rational constants. No global interval certificate is needed for this range.

### Supporting inequality and contact

The Lagrange inverse expansion for the main width has nonnegative odd coefficients. At finite equal-mass partitions each term is a positive sum of monomials product d_i^(-gamma_i) with gamma_i>0. Its directional Hessian divided by the monomial is

    (sum gamma_i v_i/d_i)^2+sum gamma_i v_i^2/d_i^2>=0.

Thus every finite truncation is convex. The passage to a continuous reference is made at a fixed truncation first; its coefficients and derivatives depend on finitely many inverse moments and the geometric mean, for which bounded convergence applies because all coordinates are in [1,2]. This avoids silently assuming convexity on an unproved infinite-dimensional domain.

The first-positive-critical-value argument is consistent with Pringsheim's theorem: nonnegative inverse coefficients cannot have a nearer singularity invisible on the positive axis. On a closed smaller disk, the bound |Phi(z)|<=Phi(|z|)<a gives room for the analytic implicit-function argument and material differentiation. At contact, the Abel parameter lambda<1 is necessary; the paper uses it and passes to the endpoint monotonically. I found no sign or contact-case omission in this step. Its scope is separated or contact atomized targets and a strictly separated reference, not arbitrary targets.

### Endpoint correction

The derivative pairing is not simply equal to the adjoint integral. The paper explicitly includes

    Mdot - integral g dxi = -A_density(2) v(2) (sigma_minus/K_minus+sigma_plus/K_plus).

The cosine coefficient calculation on pages 13-14 gives the constant coefficient -Gamma and coefficients -2Gamma for even indices and +2Gamma for odd ones, precisely -Gamma F(2). Since v(2)=d_N-2<=0, the correction is nonnegative and the required one-sided bound has the right direction.

For atomic targets the velocity has finitely many interior jumps. The paper's regularization argument treats those jumps with logarithmic singularity estimates; its continuous piece has cosine coefficients O(n^-2). Those bounds are integrable against the adjoint angular density. This is a material limiting step, not something any of the numeric signs checks. The displayed estimates are consistent with the needed limit; no independent execution could substitute for this analytic argument.

### Block reduction and circle comparison

The off-block tangent inequality is used only when source and target differences have the same sign, as monotone quantiles guarantee. Within a target block the difference quotient is -1. The remaining radius expression is minimized over R_i>0 at R_i=q_i r_i/2. Substitution gives exactly

    E(I_i)-q_i r_i log(q_i r_i/2)-C r_i.

Summation requires r_i>0 and total adjoint mass R0>0; these follow from the displayed positive adjoint density for every nonempty block.

The circle normalization was checked explicitly. The chord identity and even extension give the factor 1/(2QR), and the centered-arc normalized energy is

    A(Q,R)=-sum_{n>=1} sin(nQ)sin(nR)/(n^3 Q R).

Completing the square yields the nonnegative sum of (sinc(nQ)-sinc(nR))^2/n. The self-energy correction h(Q)=A(Q,Q)-log(Q/pi) decreases to h(pi)=0. Subject to the cited circle rearrangement theorem, the signs and factors 2 and pi in the resulting bound are consistent. The use of the theorem is for a nonnegative integrable even decreasing kernel log2-log|e^{it}-1|, first truncated, and bounded densities in [0,1]; its stated hypotheses fit that use.

### One-cut family, recovery, and upper extremum

The algebraic exterior equation and the classification of its two roots were checked. The soft endpoint has A=s; the nontrivial plus branch merges with 1 there. Global minimization of Lambda is not an analytic consequence of these root classifications.

The positive-platform recovery is valid and necessary: weak convergence alone at a zero platform does not control lengths from above. The independent proof gives a full construction for a fixed admissible q, followed by equal empirical measures and monic polynomials. It does not assume a global minimizing parameter exists.

The specialization of Tao's Theorem 2.1 gives the claimed supremum 2sqrt(2), with the empirical equality case f=(x^2-1)^m. That source theorem is an external input in this audit. Directly, these examples do have strict-sublevel measure 2sqrt(2); the missing point x=0 does not affect the measure.

## The unresolved numerical obligations

### Certificate 6.1

Required: a gap-free global derivative cover for the one-cut width, including both singular ends; one unique stationary point; and validated enclosures for q_s, q_star and L.

The source divides the domain into:

1. The entire tail 0<=rho<=1/50, rho=1/(-log q), using z_plus=q u_plus and z_minus=q u_minus and nonsingular endpoint limits (1/2,3/2).
2. Left bulk up to rho_c-1/200 with Lambda_rho<0.
3. The stationary tube rho_c+-1/200 with Lambda_rho_rho>0, plus opposite derivative signs at rho_c+-10^-30.
4. Right bulk through rho=1/log10 with Lambda_rho>0.
5. The regular soft chart 1/10<=q<=c_s-10^-5 with Lambda_q>0.
6. The endpoint soft chart through a rigorously isolated q_s, with y=(log u_plus)^2, the deflated plus equation, and Lambda_q>0.

The code uses mpmath.iv with declared 90-digit precision, interval jets, opposite branch endpoint signs, strict root derivative signs, and parametric interval-Newton contractions. The soft chart truncates positive factorial/atanhc series at degree 32 and supplies remainder and first-derivative bounds. These are genuine intended enclosure tests, not a grid-minimum test. The actual generated boxes, all acceptance signs, output enclosures, coverage and rounding behavior were not independently reproduced.

### Certificate 7.1

Required: for every k>=29/20, a valid nonnegative reference, correct simple main crossings and positive adjoint, and the strict block inequality for every nonempty quantile interval. The finite-parameter cover is:

- k in [36/25,21/10], a=1153/500-k/4; source claims 264 slabs and margin >0.036.
- k in [21/10,21/5], a=9/5; source claims 840 slabs and margin >0.036.
- q in [26631/10^6,41542/10^6], zero platform; source claims 20 rho-slabs and margin >0.046, with k(41542/10^6)<21/5.
- q in (0,26631/10^6], zero platform; source claims the tail plus 26 rho-slabs and margin >0.0056.

The affine path retains the n=1 Fourier square and checks a scalar derivative on 32 Q-subintervals. The constant-edge path discards that square. Both bound h using an 80-term Fourier sum with tail at most 1/(2*80^2 Q^2). The refined terminal path uses Arb's complex trilogarithm to evaluate h. The final terminal path proves a denominator is increasing and remains below 1, after algebraically cancelling small-q factors. The effective platform term is discarded in the terminal paths only after invoking the global minimum from Certificate 6.1.

The finite ranges cover all remaining k if their endpoint and overlap tests succeed. The strict margins are what would justify strictness for every finite polynomial and therefore nonattainment. Without this certificate, neither strictness nor the global lower bound is accepted here.

### Arithmetic and software acceptance boundary

The companion lists mpmath, python-flint and scipy as dependencies. It uses fresh subprocesses, fails on nonzero child exit, and refuses optimized Python because assertions are proof gates. SciPy and ordinary mpmath roots supply starting proposals, after which the reviewed paths perform interval checks. Code sections not used in those paths must not be mistaken for logical inputs.

A reproducibility acceptance still needs a pinned interpreter/package environment, audit of every proof-relevant conversion and remainder bound, actual completed logs for the pinned file, and independent confirmation that the reported interval bounds imply the claimed statements. Fixed padding of 1e-85 or 1e-65 around printed/parsed endpoints must be justified against the package versions and working precision; padding by itself is not an abstract proof of enclosure. The endpoint and tail computations use some high-precision ordinary arithmetic to construct such padded intervals, another reason to inspect this boundary rather than relying on a PASS banner alone.

The verifier prints several numerical enclosures rather than mechanically comparing every one against the concise theorem decimals. Those comparisons belong on the acceptance checklist.

## A one-sided comparator linkage independently resolved

The affine/constant code hardcodes

    LSTAR_LO=1.83443047576266171109075363512055343651186425665,
    LSTAR_HI=1.83443047576266171109075363512901884952989750747.

The separate one-cut verifier prints its L enclosure, and the master neither passes that enclosure to the affine code nor checks containment in this hardcoded interval. Therefore a suite PASS, by itself, does not establish that particular data linkage.

The independent rational candidate check proves Lambda(q_c)<LSTAR_HI. If Certificate 6.1 establishes L as the global minimum, then L<=Lambda(q_c)<LSTAR_HI. This is the one-sided linkage actually needed: for fixed reference and block, the normalized margin is decreasing in the target L, since C_eff=C+(L-M0)/R0 and the margin contains -C_eff/q. A successful interval calculation for the entire hardcoded target interval includes its upper endpoint, and hence proves the desired bound at any smaller L. Thus the independent comparison supplies a sufficient mathematical bridge without claiming that L belongs to the full hardcoded interval.

This does not establish L>=LSTAR_LO, the asserted digits of the global minimum, any actual affine PASS, or the global one-cut minimization. It resolves only the stated one-sided comparator issue.

## Recommended acceptance state

- Accept the independent fixed-candidate upper-bound reproduction and its finite-polynomial recovery proof.
- Preserve the cited existing supremum result as an external theorem, with attribution.
- Retain proposed/verification-dependent status for the full resolution.
- Do not infer the lower bound, q_star uniqueness, or global nonattainment from agreement of ordinary numerical approximations with the proposed decimal.
- The next bounded mathematical task is independent certificate reproduction and source-to-checker mapping for the two computational gates, with the pinned source and precise one-sided comparator bridge above. This audit does not authorize or perform author-code execution.
