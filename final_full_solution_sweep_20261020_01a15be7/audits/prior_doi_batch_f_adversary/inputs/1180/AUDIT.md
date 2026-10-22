# Prior-result audit: prime-factor barriers (Erdős problem 413)

Audit date: 10 October 2026.

## 1. Disposition and scope

**ACCEPTANCE WITH AUTHORED CORRECTIONS of the prior logarithmic omega/Omega theorem and its all-endpoints fixed-positive-epsilon consequence. No resolution claim for the coefficient-one problem.**

The primary manuscript states the logarithmic backwards-shift result with a genuine exclusion of shift 1. Its source and version are authenticated. The printed proof has invalid intermediate reasoning in its Fourier-kernel integration, growing-moment prime sum, parameter choices, and signed CRT inequalities. These points were not ignored: this package supplies complete replacements in KERNEL_REPAIR.md, DISTINCT_OMEGA_RECONSTRUCTION.md and MULTIPLICITY_REPAIR.md. The corrected full chain, including all multiplicity contributions, has been independently checked by a second reviewer.

Acceptance applies to that corrected proof, not to every formula or every broad-parameter lemma as printed. The false prime-sum estimate remains false; it is bypassed by fixing a sufficient moment schedule with a uniform error margin. The separate distinct-omega reconstruction is retained as an independently valid projection.

No novelty is claimed. The scope is the identified prior result, its proof corrections and exact implications. It is not a new attempt on an open problem, an exhaustive literature review, or an audit of unrelated conjectures in the paper. The finite terminal window for coefficient one remains unresolved.
## 2. Sources and exact statement

The original statement inspected is P. Erdős, *Some unconventional problems in number theory*, Acta Mathematica Academiae Scientiarum Hungaricae 33(1–2) (1979), 71–80, PDF page 1, printed page 71. Its original scan shows the weak inequality

    m + omega(m) <= N  for every positive integer m < N,

and explicitly describes omega as the number of **distinct** prime factors. It asks whether there are infinitely many such N, and also whether the same is true with epsilon*omega for some one fixed epsilon>0. Use omega(1)=Omega(1)=0. The distinction between omega and the multiplicity-counting Omega is essential. For example, omega(12)=2 whereas Omega(12)=3. Original source: https://users.renyi.hu/~p_erdos/1979-23.pdf .

The source theorem is Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors of Consecutive Integers*, arXiv:2604.15042v2, 24 June 2026, Theorem 1.3, PDF page 3:

    There is C>0 and an unbounded set of positive integers n such that
    omega(n-k) <= Omega(n-k) <= C log k for every integer 2 <= k < n.

Here and throughout this audit log is the natural logarithm. The inspected source is https://arxiv.org/pdf/2604.15042v2 , 717637 bytes, SHA256 90443d4ebbdfe9e05052e1a8115b8acd9d29d3ce7269d7e9c71cb09716c718d1. The whole 37-page v2 text was read; selected statement and proof displays were checked against rendered pages. The complete 32-page v1 and the complete 10-page Erdős original were also read. Version 1 contains the same problematic Fourier identity on PDF page 25 and does not provide an independent fallback proof. Version 2 substantially revises the prime-power treatment, so an argument from one version cannot silently fill a gap in the other.

The live arXiv abstract page checked on the audit date listed v2 as its current version. The page's descriptive comment still says 32 pages, while the authenticated v2 PDF has 37 pages. This audit uses the actual PDF page numbers and version pin. No journal-ref or peer-review acceptance was established by this audit. Lau's bibliography also lists a distinct same-title Erdős item in Mathematics Magazine; the original statement used here is specifically the authenticated Acta scan, not an inferred identification of those two items.

## 3. The endpoint transfer is completely checked

Let L(C) denote the backwards-shift assertion just stated, considered as a hypothesis. For each of its witnesses n>=3 put

    N = n-1,    epsilon = 1/(C log 2).

For every positive m<N set j=N-m. Then 1<=j<N and

    k=n-m=j+1,
    2<=k<=n-1<n,
    m=n-k=N-j.

Consequently L(C) applies to this m. The elementary inequality j+1<=2^j holds for every integer j>=1: it is an equality at j=1, and induction uses j+2<=(j+1)+1<=2^j+2^j. Taking logarithms yields

    epsilon*Omega(m) <= log(j+1)/log 2 <= j.

Thus m+epsilon*omega(m)<=m+epsilon*Omega(m)<=N for every positive m<N. The same one epsilon works for every witness because C is fixed before the witnesses are chosen. The map n -> n-1 is injective and takes an unbounded set to an unbounded set, so infinitely many N result.

Every endpoint is included. The closest integer m=N-1 corresponds to Lau's allowed k=2, not his forbidden k=1. The farthest endpoint m=1 corresponds to k=n-1 and has omega(1)=Omega(1)=0. Nothing is asserted about Lau's uncontrolled m=n-1; that integer equals the new endpoint N and is excluded from the barrier's required m<N domain. The transfer is equally valid for multiplicity-counting Omega, and hence for omega. It proves an existential fixed positive epsilon, not all prescribed epsilon>0, and does not give a numerical epsilon without a numerical source constant C.

This implication is independently accepted. The source hypothesis L(C) is also accepted through the corrected reconstruction in this package, including its stronger Omega statement. Inserting k=1 into C log k would be invalid and would require Omega(n-1)<=0 for large n.

## 4. What remains for coefficient one

At an unshifted witness n, L(C) gives omega(n-k)<=k whenever C log k<=k. Since log k/k tends to zero, choose one finite K0>=2 such that this holds for every k>=K0. Only the existence of a sufficiently large fixed cutoff is needed; no numerical cutoff is inferred without a numerical C.

The original barrier still requires the entire terminal window

    1 <= k < K0.

This includes k=1, at which for n>2 the distinct-prime condition demands that n-1 be a prime power, while the stronger Omega condition demands that n-1 be prime. Neither condition follows from the stated logarithmic theorem. A finite number of missing inequalities is not harmless when the demand is that all of them hold simultaneously at infinitely many witnesses.

At the shifted witnesses N=n-1, one instead knows omega(N-j)<=C log(j+1), so coefficient one is controlled only for all sufficiently large j; the small-j window again remains. The epsilon rescaling is precisely what pays for that window and must not be erased. The full coefficient-one question therefore remains unresolved by this prior-result implication also after accepting the corrected proof of L(C).

## 5. Reconstructed dependency chain

### 5.1 Global existence from local tail bounds

Proposition 5.1 asks for one probability distribution on n in [x,2x], valid simultaneously for 2<=k<=x^(1/100), with

    P(Omega(n+k)>C log k) < 6/(pi^2 k^2).

The actual constructed weight is independent of the queried k and moment orders; hence the quantifier required for the union bound is the right one. Summing from k=2 gives at most 1-6/pi^2<1. Positive probability leaves a simultaneous good n. For k>x^(1/100), the deterministic inequality Omega(a)<=log(a)/log 2 supplies a constant multiple of log k, first for k<=2x and then for k>2x. One fixed C is chosen before arbitrarily large x; n in [x,2x] is therefore unbounded. This top-level implication is sound, conditional on Proposition 5.1.

### 5.2 The four prime-factor contributions

Write w=.15 log x, K=(log x)^(1/1000), and

    R_k=x^(1/(100 k^50)) for k<=K, and R_k=w otherwise;
    T=x^(1/(10 A log k)).

The distribution is supported on n divisible by p^4 for every p<=w. The decomposition separates:

1. Distinct primes w<p<=R_k dividing n+k.
2. The centered distinct-prime sum for R_k<p<=T, subtracting 1/p.
3. Extra prime powers p^a|n+k with p>w, p<=T, a>=2.
4. Excess small-prime valuations (v_p(n+k)-v_p(k))_+ for p<=w with p^4|k.

For p<=w and v_p(k)<4, the valuations of n+k and k agree. Baseline small-prime valuations sum to at most Omega(k)<=log k/log 2. Prime factors above T, counted with multiplicity, contribute at most log(3x)/log T=O(A log k). The reciprocal-prime mean in (2) is O(log k), from the prime harmonic estimate and the definition of R_k. When T<=R_k the associated sum is empty and must be treated as zero rather than bounded by a negative logarithm.

Thus a tail bound of order k^(-2), with a sufficiently small coefficient, for each of the four contributions yields Proposition 5.1. This deterministic architecture is sound. The printed numerical constants are not independently certified. The accepted replacement uses a fixed parameter and moment schedule and does not claim a numerical value for the final absolute C.

### 5.3 Moment estimates and the transition to tails

Lemma 5.3 aims at the following bounds for suitable integer moment orders s_i of size log k:

    E X1^s1 << (2 C3 s1)^s1;
    E |X2|^(2s2) << (132 A log k)^(2s2);
    E X3^s3 << (max(4 e^2 C3, 968(A log k/s3)^2) s3)^s3.

The fourth contribution is instead controlled by a joint p-adic geometric tail. Markov's inequality with orders proportional to log(C2 k) is the mechanism turning these estimates into C2^(-2)k^(-2) tails. There is no need for independence of the prime-divisibility indicators.

There are additional explicit bookkeeping problems in the printed transition. On page 9, A is fixed in terms of C2,C3, but s1 is chosen proportional to C1 log(C2 k) while C1 is permitted to be arbitrarily large; the asserted s1<=A log k then fails for fixed k. The step e^(-s1)<=C2^(-2)k^(-2) also requires s1>=2 log(C2 k), not merely the stated weakest threshold. These problems are locally repairable if the moment bounds themselves hold: choose the moment orders first as, for example, ceil(2 log(C2 k)), choose A large enough for their uniform upper bound, and only then choose the threshold C1 sufficiently large. Those formal adjustments alone do not settle the moment and Fourier issues; the companion corrections supply the needed substantive estimates.

The use of Proposition 5.5(B) for a 2s2-th moment needs a divisor estimate through 2s2 prime factors, although the proposition as printed states j<=s2. A revised parameter budget is required when applying the stronger order. Page 12 also changes 1000 log k to 3A log k, requiring A>=1000/3, and its falling-factorial numerator/denominator are printed with different reference integers. These are genuine obligations in any full corrected proof, not accepted steps in this audit.

### 5.4 Divisibility estimates behind the moments

Proposition 5.5 collects:

(A) Support on multiples of W=product_{p<=w} p^4.

(B) Joint divisibility by j distinct primes above R_k, bounded by an absolute exponential in the allowed order divided by their product.

(C) A summed joint-divisibility bound for primes in (w,R_k], of order (C3 log s)^s.

(D) Reduction of higher prime powers at primes above w to first-power divisibility, with an O(x^(-.1)) error.

(E) A geometric upper bound for excess valuations at primes p<=w that divide k to at least the fourth power, with O(x^(-.3)) error.

Grouping repeated prime indices into set partitions explains the Stirling-number factor in X1 and X2. For X3, repeated occurrences of one prime require the maximum exponent, not a sum of those exponents; v2 uses maxima, unlike v1's displayed treatment. The combinatorics then produces block-size weights and a generating-function bound. Summing the O(x^(-.1)) terms over prime powers is delicate because the moments grow. That sum is where the uniform estimate analyzed in Section 7 is used.

The standard inputs at this level are the Stirling-number bound and falling-factorial identity, elementary set-partition enumeration, the prime harmonic estimate, the prime number theorem for W=x^(.6+o(1)), and ordinary calculus. The earlier Tao–Teräväinen and Maynard methods are acknowledged as inspiration; v2 presents its purported sieve proof rather than making those works a black-box theorem implying its new logarithmic conclusion. Section 7 of the paper, which uses random-model conjectures and a Tenenbaum estimate, is not a dependency of Theorems 1.1/1.3. No conjecture there is used to support this audit's acceptance or hold.

### 5.5 Construction, CRT, and Fourier factorization

The nonnegative weight is a product, over r<=K, of squared Mobius sums in divisors of n+r, multiplied by 1_{[x,2x]}(n) and 1_{W|n}. The divisor cutoff uses tilde-eta(u)=exp(-u)eta(u), where eta is a fixed nonnegative even compactly supported Gevrey-2 function with eta(0)=1 and nonnegative Fourier transform h.

Expanding the squares gives congruence counts. Primes greater than w>K cannot divide two distinct shifts among 1,...,K. Compatible CRT systems have one residue class; incompatible ones contribute zero. The product of sieve levels is x to a small fixed power. The exact assertion W<=x^.6 is stronger than what the prime number theorem directly gives; W=x^(.6+o(1)) suffices if the stated power margins are tracked with a small slack.

Lemma 6.1 expresses the weighted count P_k(d*) as an Euler-product Fourier integral. Its dominant tensor kernel in each coordinate pair is

    a(t,u)=(1+it)(1+iu)/(2+i(t+u)).

For a prime p|d*, the extra factor is 1/p times (1-exp(-(1+it)a_p))(1-exp(-(1+iu)a_p)) in its unique compatible shift coordinate, where a_p=log p/log R_r, or simply 1/p if it has no compatible shift. The remainder in equations (6.2) and (6.7) is a frequency-dependent pointwise multiplicative error of size O((log x)^(-.69)) in the no-divisor case, with the displayed higher-order analogue when d* has several primes. Fourier tails have much stronger decay exp(-c(log x)^(.1)).

The proposed normalization and joint-divisor bounds come from integrating this expression. This is precisely the invalid inference analyzed in Section 6; the weaker pointwise error estimate cannot simply be taken outside a complex integral. KERNEL_REPAIR.md replaces it by a coefficient-norm integration argument for the exact Euler product.

### 5.6 The higher-power and small-prime CRT arguments

Lemma 6.4 uses the squarefree support of the Mobius coefficients: at any p>w the base congruence modulus contains p at most once. Imposing p^a then multiplies the compatible progression's modulus by p^(a-1), relative to imposing p. The density terms cancel when the higher-power indicator is compared with the rescaled first-power indicator, leaving an O(1) interval-count error for each divisor configuration. This supplies the intended error after summing absolute coefficients and dividing by a valid normalization. Some printed substitutions drop an invertible progression coefficient; CRT counting, rather than that literal substitution, is the valid way to justify the cancellation. The normalization is supplied by KERNEL_REPAIR.md; MULTIPLICITY_REPAIR.md gives the complete uniform CRT argument.

In Lemma 6.5, adding congruences modulo p^(v_p(k)+h_p) for p<=w has the indicated geometric density factor because v_p(k)>=4. However, the printed page 35 termwise inequalities multiply interval-count upper bounds by signed Mobius coefficients; those inequalities are not justified as written. A valid route is to retain signed main terms but bound the O(1) errors by the sum of absolute coefficient values, then divide by a proven normalization. The elementary congruence-density idea is valid; the printed signed inequalities are not accepted. The signed-main/absolute-error correction and its error budget are provided in MULTIPLICITY_REPAIR.md.

## 6. Fourier-kernel issue: exact derivation and correction

Let

    c0 = integral over R^2 of a(t,u)h(t)h(u) dt du,
    D  = integral over R^2 of |a(t,u)|h(t)h(u) dt du.

All these integrals converge because h has the stated rapid decay. Algebra gives

    Re a(t,u)=(2+t^2+u^2)/(4+(t+u)^2)>0,
    Im a(t,u)=(1+tu)(t+u)/(4+(t+u)^2).

The imaginary part cancels under (t,u)->(-t,-u), while a Laplace representation of 1/(2+i(t+u)) gives

    c0=integral_0^infinity (tilde-eta'(v))^2 dv >=1.

The last inequality follows from Cauchy–Schwarz and tilde-eta(0)=1, tilde-eta(1)=0. These statements are sound.

The next displayed equality on v2 page 28 replaces the integral of Re a by that of |a|. It is false. The actual hypotheses make h continuous with h(0)>0, so h is positive near zero. At t=u=z one has exactly a(z,z)=(1+iz)/2. For every sufficiently small z>0 its imaginary part is nonzero and |a(z,z)|>Re a(z,z); the inequality persists on an open neighborhood. Hence **D>c0**, not D=c0.

The page 29 all-coordinate triangle-inequality argument thus produces D^K in place of c0^K. Setting rho=D/c0>1, this gives an extra rho^K. Since K=floor((log x)^(1/1000)) grows, that factor cannot be absorbed into a constant depending only on a fixed admissible k and moment order s. Rescaling eta or the probability weight does not fix this: D and c0 rescale together and their ratio is unchanged.

### A valid partial repair: exact main integral

It would be too strong to say that the wrong equality makes the desired main-term bound impossible. Put f=tilde-eta' on [0,infinity), and define S_a f(v)=f(v+a). Each S_a is a contraction of L2([0,infinity)); thus I-S_a has operator norm at most 2.

For a collection of extra prime factors assigned to one shift coordinate, the Laplace representation and Fourier inversion show that the exact, unperturbed two-variable integral equals the squared L2 norm of

    product over those primes of (I-S_{a_p}) f.

The sign from differentiating tilde-eta disappears on squaring. If that coordinate has r extra primes, its integral is at most 4^r c0. Untouched coordinates give exactly c0. Coordinates with no compatible shift only contribute 1/p. Therefore the whole exact main integral is nonnegative and bounded by

    (4^j/d*) c0^K,

where j is the number of imposed distinct primes. This avoids the D^K loss for the exact main term. The same observation gives the exact no-divisor tensor integral c0^K. This partial correction has been checked independently during the audit.

### What the printed proof lacks, and the supplied replacement

The approximation (6.2)/(6.7) multiplies the main integrand by a function of all Fourier variables. Its displayed bound is pointwise. The preceding contraction argument applies to the exact main term with its specified difference factors; it does not automatically apply to an arbitrary frequency-dependent perturbation.

For d*=1, the triangle inequality applied to the stated error alone gives an error, relative to c0^K, of at most a constant times

    (log x)^(-.69) rho^K.

That upper-bound scale does not tend to zero: its logarithm is K log rho-.69 log log x, which tends to infinity. This does not prove that the actual error is large. It shows exactly why the displayed sup bound does not establish the required o(1) after integration. Likewise, dropping the pointwise remainder before integrating untouched coordinates, as in the reduction on page 31, is unjustified without additional integrated control.

The genuinely strong Fourier-tail error is not the same problem; exp(-c(log x)^(.1)) dominates the slower products of logarithms and fixed constants to the power K. The part not controlled by the printed argument is the polynomial-in-log frequency-dependent Euler-product error.

A bound exploiting the actual structured Euler-product remainder is required. This package supplies it in KERNEL_REPAIR.md: factor the exact Euler product into K exact one-coordinate factors, paired divisor differences, and a coupling correction H_d. The correction has an absolutely summable expansion in nonnegative translations, with coefficient norm ||H_1-1||=O(K^2/w)=o(1) in the normalization case and ||H_d||<=(1+o(1))2^j for j divisor primes. Each translation is controlled before summing by the one-coordinate L2 estimate. The one-coordinate zeta approximations cost only (1+O((log x)^(-.7)))^K=1+o(1). This proves the required normalization and divisor bounds without a rho^K loss.

The preceding exact CRT/Fourier representation and its truncation error are also reconstructed, rather than assumed without review, in DISTINCT_OMEGA_RECONSTRUCTION.md §2. Its absolute CRT configuration error is at most x^.021; W=x^(.6+o(1)) and d*<=x^.1 leave enough room to absorb it. The genuinely decaying Fourier tail remains negligible after the normalizing product of logarithms. This complete replacement clears the Fourier proof-acceptance issue. The false printed equality itself is not endorsed.

## 7. A separate growing-moment estimate fails within the applied range

On v2 PDF page 16, after (5.16), the source uses

    sum_{R_k<p<=T} 1/(log p)^(m+1) << T/(log T)^(m+2)

uniformly for m>=1. In the application m is a block size and can be as large as s3, where log k<=s3<=A log k. The uniform assertion is false even in this parameter range.

Here is a countersequence requiring only the existence of arbitrarily large primes. Fix A=2. Along primes q tending to infinity put

    x=exp(10q/3),  L=log x,  w=.15L=q/2,
    y=L/(20 A log w),  k=ceil(exp(y)),
    m=s3=floor(A log k).

Then log k=y+o(1), and for sufficiently large q:

- k>(log x)^(1/1000), so R_k=w;
- k<=x^(1/100), because log k/log x~1/(20 A log w)->0;
- log k<=m<=A log k, so m is an allowed order and an allowed single-block size;
- T=x^(1/(10 A log k)) satisfies log T=2 log w+o(1), hence T~w^2;
- the prime q=2w belongs to (w,T].

The single q term in the left side, divided by the displayed right side without its implied constant, is

    (log T/T) * (log T/log(2w))^(m+1).

Its logarithm equals

    (m+1) log(log T/log(2w)) + log log T - log T
    = (log 2+o(1))m - 2 log w + O(log log w),

which tends to infinity since m~L/(20 log w) and L=(20/3)w. Therefore no absolute implied constant, or a constant depending only on the fixed A=2, can make the claimed bound uniform. The prime q construction avoids any reliance on a short-prime-interval estimate.

This is an error in an intermediate estimate, not a counterexample to the desired final X3 moment bound. The full expression retains factors such as x^(-.1) and factorial denominators; a correct bound on the combined expression could exploit them rather than the false separate prime-sum bound. The exact main-integral repair alone does not address this separate issue. MULTIPLICITY_REPAIR.md supplies the needed replacement: fix A=100 and s=ceil(4 log k), count all Q prime-power indicators, and prove Q^s<=x^.02 whenever the range is nonempty. Uniform CRT errors are at most x^(-.3), so their complete sum is negligible. The main terms are bounded by a set-partition generating function. This clears the multiplicity conclusion for the moment schedule actually needed in the theorem, while leaving the invalid standalone prime-sum assertion rejected.

## 8. Backwards shifts and theorem transfer inside the source

Theorem 1.3 is stated as obtainable by the same proof, not as a direct consequence of the forward theorem for the very same witnesses. The sign change is compatible with the intended architecture:

- Replace divisors of n+r in the sieve weight by divisors of n-r. For n in [x,2x] and r<=K the arguments remain positive.
- The congruences become n congruent to r, rather than -r. Compatibility still depends on p dividing differences k-r, so the local prime factors have the same form.
- At small primes, v_p(n-k)=v_p(k) whenever v_p(k)<4 and p^4|n. Excess-valuation congruences change sign consistently.
- The small-shift range 2<=k<=x^(1/100) has positive n-k. The deterministic large-shift range x^(1/100)<k<n has n-k<=2x, so Omega(n-k)<=log(2x)/log 2=O(log k).
- At k=n-1, n-k=1 is harmless. At k=1, log k vanishes; that point remains deliberately absent.

Accordingly, no independent sign or endpoint obstruction was found in transporting a *valid, uniform* sieve proof to Theorem 1.3. The uncorrected Fourier and growing-moment issues would survive the sign change. The companion reconstructions prove the backwards theorem directly with these issues repaired; no uncontrolled k=1 point is introduced.

## 9. Final acceptance and exact limits

Accepted through the complete corrected package:

1. The original problem concerns distinct factors and a weak inequality at every positive m<N.
2. The authenticated source states the strict 1<k<n logarithmic result.
3. The full corrected sieve proof yields one absolute C and infinitely many n with omega(n-k)<=Omega(n-k)<=C log k for every integer 2<=k<n.
4. The replacement keeps one distribution for all k, fixes its constants before x tends to infinity, and controls all CRT, Fourier and growing-moment errors uniformly.
5. The shifted-index argument gives one fixed positive epsilon and infinitely many barriers for epsilon*Omega and therefore for epsilon*omega, including every positive m below each barrier.
6. The separate distinct-only reconstruction is independently valid and does not rely on any prime-power estimate.

Printed steps rejected and replaced, rather than accepted unchanged:

- The page-28 equality between a complex-kernel L1 norm and its real integral.
- Taking a many-coordinate pointwise relative error outside its complex integral without integrated control.
- The page-16 standalone prime-sum bound claimed uniformly in the growing moment order.
- Inconsistent broad-parameter moment orders and the signed Mobius coefficient inequalities on page 35.

KERNEL_REPAIR.md provides the exact-Euler-product correction. DISTINCT_OMEGA_RECONSTRUCTION.md supplies its CRT/Fourier antecedent, the corrected summed prime bound, ordinary moments and full endpoint argument. MULTIPLICITY_REPAIR.md proves the arbitrary-prime-power comparison, the uniform total high-power error bound, the small-prime excess bound, and the final full Omega union bound. The latter two CRT arguments retain signed density main terms and sum absolute O(1) errors, avoiding the invalid signed inequalities. A separate reviewer independently checked the complete replacements, including the fixed parameter schedules and all endpoints.

The accepted conclusion is a prior-result theorem with authored proof corrections. No theorem of greater scope, no broad-parameter lemma not needed in the replacement, and no novelty or whole-problem solution is asserted. In particular, coefficient one still requires the finitely many terminal inequalities simultaneously at infinitely many witnesses. None of the corrected logarithmic theorem, the epsilon shift, or this audit supplies those missing inequalities.
## References

- P. Erdős, *Some unconventional problems in number theory*, Acta Mathematica Academiae Scientiarum Hungaricae 33(1–2) (1979), 71–80. https://users.renyi.hu/~p_erdos/1979-23.pdf
- Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors of Consecutive Integers*, arXiv:2604.15042v2 (24 June 2026). https://arxiv.org/abs/2604.15042v2 and https://arxiv.org/pdf/2604.15042v2
- Earlier version for comparison only: arXiv:2604.15042v1 (16 April 2026). https://arxiv.org/pdf/2604.15042v1

## Publication-edition review boundary

Acceptance means independent internal AI review of the stated corrected
mathematical arguments. This AI-assisted work is unrefereed. No external human
peer review, journal acceptance, formal proof-assistant certification, or
novelty is claimed. The fixed A=100 multiplicity repair and fixed-positive-
epsilon consequence are accepted; coefficient one remains unresolved.
