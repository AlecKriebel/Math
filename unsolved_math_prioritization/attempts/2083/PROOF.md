# Nondividing primes in a central binomial coefficient: a carry-depth barrier

This prose-only edition is AI-assisted and unrefereed. “Accepted” means an
independent internal AI audit of the stated partial results. No external human
peer review, journal acceptance or formal proof-assistant certification is
claimed. No novelty or priority is claimed. The absolute-bound target remains
unresolved by this work.

Source inspection and finite computations described below are historical
activities of the original proof and independent audit, not new work performed
to prepare this edition. No new mathematical test or scholarly-source inspection
was performed during edition preparation. Executable code, raw datasets,
detailed receipts, full computational certificates and copied third-party
sources are excluded. This is not an executable reproduction package.

## Status and exact target

**Partial result only. No proof or counterexample to Erdős problem 377 is claimed. No novelty is claimed.**

For a positive integer n put

\[
 B_n=\binom{2n}{n},\qquad
 f(n)=\sum_{\substack{p\le n\\p\text{ prime},\ p\nmid B_n}}\frac1p.
\]

The target is whether \(\sup_{n\ge1}f(n)<\infty\). Every sum in this note is unweighted unless a logarithmic weight is explicitly written. Neither a finite search nor a mean-value theorem establishes the target.

The main elementary conclusions are:

1. There is **no summable pointwise majorant indexed only by digit-depth shells**, even after any fixed finite set of primes is removed.
2. A relaxation that tests only \(L(n)=o(\log n)\) common carry levels is necessarily unbounded. In contrast, testing \(\lfloor c\log(2n)\rfloor\) levels, for any fixed \(c>0\), is equivalent to the target up to a bounded finite-prime error.
3. An application of Sander's published exponential-sum estimate gives the expected unweighted limit for every **fixed** shell, for all n. This cannot be summed uniformly over the shell index. It also gives \(\liminf f(n)=c_0\), while a fixed-prime contribution forces \(\limsup f(n)\ge c_0+1/3\).

The first two conclusions have complete elementary proofs below. The third is proved from a precisely stated published analytic input, not asserted as a new theorem or as an elementary result.

## 1. Exact carry criterion

Write \(v_p\) for the p-adic valuation. Counting multiples of each prime power in a factorial gives

\[
 v_p(B_n)=\sum_{j\ge1}\left(\left\lfloor\frac{2n}{p^j}\right\rfloor
       -2\left\lfloor\frac n{p^j}\right\rfloor\right)
 =\sum_{j\ge1}\left\lfloor2\left\{\frac n{p^j}\right\}\right\rfloor.
 \tag{1}
\]

Each summand is either 0 or 1 and the sum is finite. Consequently

\[
 p\nmid B_n\quad\Longleftrightarrow\quad
 2(n\bmod p^j)<p^j\quad\hbox{for every }j\ge1. \tag{2}
\]

For odd p this is equivalent to every base-p digit of n being at most \((p-1)/2\). Indeed, if all lower j digits obey that bound, their value is at most \((p^j-1)/2\); conversely, if digit \(a_i\ge(p+1)/2\), then \(n\bmod p^{i+1}\ge a_ip^i>p^{i+1}/2\). For p=2, the highest nonzero binary digit violates (2), so 2 never contributes for positive n.

This proves the criterion rather than relying on an OCR transcription of a divisibility symbol. It agrees with EGRS75, printed page 84, and Sander93, equation (10).

## 2. A uniform summable shell bound is impossible

For integers \(r\ge1\), define the exact shell

\[
 F_r(n)=\sum_{\substack{p\text{ prime}\\p^r\le n<p^{r+1}\\p\nmid B_n}}\frac1p.
 \tag{3}
\]

The shells are disjoint and \(f(n)=\sum_{r\ge1}F_r(n)\); only finitely many terms are nonzero for each n.

**Theorem 1.** For every odd prime q and every integer \(r\ge1\),

\[
 F_r(q^r)\ge\frac1q. \tag{4}
\]

In particular \(\sup_n F_r(n)\ge1/3\) for every r. There is no nonnegative sequence \((a_r)\) with \(\sum_r a_r<\infty\) and \(F_r(n)\le a_r\) for all n,r.

**Proof.** The base-q expansion of \(q^r\) consists of a single digit 1 and zeros. Since q is odd, these are allowed digits. Thus \(q\nmid B_{q^r}\), and \(q^r\le q^r<q^{r+1}\) places the contribution \(1/q\) in shell r. Any pointwise majorant must therefore satisfy \(a_r\ge1/3\) for every r, contradicting summability. ∎

The same argument works after deleting any fixed finite set E of primes: choose an odd prime \(q\notin E\). Then every shell still has supremum at least \(1/q\).

**Consequence for a proposed strategy.** An estimate of the form

\[
 F_r(n)\le A\rho^r/r\qquad(A>0,\ 0<\rho<1)
 \tag{5}
\]

uniformly in both n and r is false, not merely unproved. Even a uniform bound \(F_r(n)\le A/r\) is false. An all-n proof of boundedness must allow fixed-prime mass to move to arbitrarily deep shells. This is not a counterexample to boundedness of f: (4) supplies one fixed amount of mass, not arbitrarily large total mass.

## 3. A sharp common-depth truncation dichotomy

For an integer-valued function \(L(n)\ge0\), define

\[
 H_L(n)=\sum_{\substack{3\le p\le n\\p\text{ prime}\\
 2(n\bmod p^j)<p^j\ (1\le j\le L(n))}}\frac1p.
 \tag{6}
\]

An empty set of conditions means all odd primes p≤n are admitted. Always \(f(n)\le H_L(n)\).

**Theorem 2 (sublogarithmic-depth obstruction).** If \(L(n)=o(\log n)\), then \(H_L(n)\) is unbounded. More precisely, for every finite set S of odd primes, there are arbitrarily large n with every p∈S admitted by (6).

**Proof.** If S is empty, the assertion is vacuous for every n. Otherwise S is nonempty. Set \(Q=\prod_{p\in S}p\) and take \(n=Q^m\). As m→∞,

\[
 \frac{L(Q^m)}m=
 \frac{L(Q^m)}{\log(Q^m)}\log Q\longrightarrow0.
\]

For all sufficiently large m, \(L(Q^m)\le m\). Each \(p\in S\) divides Q, so \(p^j\mid Q^m\) for \(j\le m\). Every tested residue is therefore zero. Also p≤n. Hence

\[
 H_L(Q^m)\ge\sum_{p\in S}\frac1p.
\]

The sum of reciprocals of odd primes diverges. For completeness, if the sum over all primes converged, then \(\prod_{p\le x}(1-1/p)^{-1}\) would remain bounded, since \(-\log(1-1/p)\le 1/p+C/p^2\). Expanding the finite product as geometric series includes \(\sum_{k\le x}1/k\), a contradiction. Removing p=2 does not change divergence. Choose S with reciprocal sum exceeding any prescribed number. ∎

No monotonicity of L is needed. The construction does not claim that its primes are actual nondivisors: carries beyond the tested levels may eliminate them. For example, at n=225, primes 3 and 5 pass the first two levels, but both divide \(B_{225}\).

**Theorem 3 (logarithmic-depth equivalence).** Fix \(c>0\), and set \(L_c(n)=\lfloor c\log(2n)\rfloor\). Then for every n≥1,

\[
 0\le H_{L_c}(n)-f(n)
 \le\sum_{\substack{3\le p<e^{1/c}\\p\text{ prime}}}\frac1p. \tag{7}
\]

Thus \(H_{L_c}\) is bounded if and only if f is bounded.

**Proof.** If \(p\ge e^{1/c}\), then

\[
 p^{L_c(n)+1}>p^{c\log(2n)}\ge2n.
\]

For every untested level \(j\ge L_c(n)+1\), one has \(n/p^j<1/2\). All these conditions are automatic. Therefore the truncated and full predicates agree for every such prime. Only the finitely many odd primes below \(e^{1/c}\) can differ, and each discrepancy contributes at most 1/p. ∎

These theorems distinguish a genuinely weaker, provably unbounded relaxation from a logarithmic-depth restatement of the original question. They do not turn a sublogarithmic failure into a counterexample to the exact target.

## 4. The all-n fixed-shell limit

The analytic result in this section is a consequence of published machinery. The dependence of constants on the fixed shell index is allowed throughout. There is no claim of uniformity as r→∞.

**Published input (Sander93, Lemma 1, printed page 226).** Let k≥1 be fixed; let \(1\le j_1<\cdots<j_s\le k\), with real coefficients \(m_1\ge1\), and \(M=\max_i|m_i|\). Put \(e(x)=\exp(2\pi ix)\). There are positive constants \(C_k,c_k\) such that, for \(2\le t\le n^{1/k}\),

\[
 \left|\sum_{p\le t}e\!\left(n\sum_{i=1}^{s}\frac{m_i}{p^{j_i}}\right)\right|
 \le C_k\left(t^{1-c_k(\log t/\log(Mn))^2}
       +t^{(k+2)/2}n^{-1/2}+t^{5/6}M^2\right)(\log(Mn))^{4k}. \tag{8}
\]

The lemma is quoted there from Sander92. The more precise Sander92 Theorem 2 uses the least exponent j₁ in the middle term and permits t≤n^(1/j₁); (8) is a weakening on t≤n^(1/k). The proof through Sander92, Sections 2–3, printed pages 2–14, has been inspected. It uses standard derivative estimates and Vaughan's identity. Those antecedent analytic theorems are accepted published inputs, not re-proved here.

We also use Mertens' theorem \(\sum_{p\le x}1/p=\log\log x+B+o(1)\).

**Theorem 4.** For every fixed integer r≥1,

\[
 \lim_{n\to\infty}F_r(n)=2^{-r}\log\left(1+\frac1r\right). \tag{9}
\]

**Proof.** Choose a fixed \(\delta>0\) so small that

\[
 a=1/(r+1)+\delta<b=1/r-\delta.
\]

On the trimmed interval \(n^a<p\le n^b\), for all sufficiently large n one has \(p^r<n\) and \(p^{r+1}>2n\). Hence nondivisibility is exactly the conjunction of the first r conditions \(\{n/p^j\}<1/2\).

For any fixed nonzero integer vector \(h=(h_1,\ldots,h_r)\), remove its zero coordinates and, if necessary, conjugate the exponential sum to make its first nonzero coefficient positive. Apply (8) with k=r. Uniformly for \(n^a\le t\le n^b\), the three terms on the right of (8), divided by t, are bounded by a negative power of n times a fixed power of log n. Indeed:

- \(\log t/\log(Mn)\ge a/2\) eventually, so the first ratio is at most \(n^{-c_ra^3/4}\).
- The second ratio is \(t^{r/2}n^{-1/2}\le n^{-r\delta/2}\).
- The third ratio is at most \(M^2n^{-a/6}\).

Therefore, for some \(\eta>0\) depending on r,δ,h, the cumulative phase sum \(S_h(t)\) satisfies

\[
 |S_h(t)|\ll_{r,\delta,h}t n^{-\eta}(\log n)^{4r}.
\]

Partial summation on \((A,B]=(n^a,n^b]\) gives the exact identity

\[
 \sum_{A<p\le B}\frac{e(n\sum_jh_j/p^j)}p
 =\frac{S_h(B)}B-\frac{S_h(A)}A+
 \int_A^B\frac{S_h(t)}{t^2}\,dt=o(1). \tag{10}
\]

Thus all nonconstant Fourier coefficients of the finite measures

\[
 \mu_n=\sum_{n^a<p\le n^b}\frac1p\,
 \delta_{(\{n/p\},\ldots,\{n/p^r\})}
\]

on the r-dimensional torus tend to zero. Their total masses tend, by Mertens, to \(\log(b/a)\). It follows that the mass of the box \([0,1/2)^r\) tends to \(2^{-r}\log(b/a)\). Here is the standard boundary justification: bound its indicator above and below by products of continuous periodic functions in [0,1] whose one-dimensional integrals differ from 1/2 by at most ε; approximate the continuous functions uniformly by trigonometric polynomials, use (10), and then send ε→0. The box boundary has zero Lebesgue measure.

The omitted portions of the original shell \((n^{1/(r+1)},n^{1/r}]\) have total reciprocal-prime mass tending to

\[
 \log\frac{a}{1/(r+1)}+\log\frac{1/r}{b},
\]

which tends to zero as δ→0. These masses dominate the omitted nondividing-prime contributions. Squeezing and then sending δ→0 proves (9). ∎

**Corollary 4.1.** With

\[
 c_0=\sum_{r\ge1}2^{-r}\log(1+1/r)
     =\sum_{k\ge2}\frac{\log k}{2^k},
\]

one has

\[
 \liminf_{n\to\infty}f(n)=c_0. \tag{11}
\]

For each fixed R, nonnegativity and (9) give \(\liminf f\ge\sum_{r=1}^R2^{-r}\log(1+1/r)\); send R→∞. Conversely, EGRS75 Theorem 2 proves that the Cesàro mean of f tends to c₀. A liminf strictly larger than c₀ would contradict that mean limit. This proves equality.

**Corollary 4.2.**

\[
 \liminf_{m\to\infty}f(3^m)\ge c_0+1/3,
 \qquad\limsup_{n\to\infty}f(n)\ge c_0+1/3. \tag{12}
\]

For fixed R and m>R, the prime 3 contributes 1/3 in shell m, outside the first R shells. Apply (9) along n=3^m, then send R→∞. Thus all-n convergence to c₀ is false, even though every fixed shell converges and f converges to c₀ in density.

For completeness, EGRS75 Theorem 1, with bases 3,5 and digit bounds 1,2, gives infinitely many n for which both primes are nondivisors. The theorem's hypothesis is **≥1**, as checked in the PDF. Applying the same argument along that sequence gives the stronger sourced consequence

\[
 \limsup f(n)\ge c_0+\frac13+\frac15=c_0+\frac8{15}. \tag{13}
\]

No claim is made that this bound is sharp.

## 5. What remains, and what was ruled out

Mertens implies that, for each fixed \(0<\alpha<1\), the contribution from \(n^\alpha<p\le n\) is bounded uniformly in n. Consequently the exact target is equivalent to bounding

\[
 \sum_{\substack{p\le n^\alpha\\p\nmid B_n}}\frac1p
\]

for any one fixed α∈(0,1). Theorem 4 identifies the deterministic limit of each fixed-depth part but does not bound this remaining mass. In particular:

- Exchanging the all-n limit and the infinite shell sum is invalid; (12) proves a concrete failure.
- A summable depth-only pointwise envelope is impossible by Theorem 1.
- An upper bound obtained solely by discarding all carry conditions above a common sublogarithmic depth cannot work, by Theorem 2.
- The weighted asymptotic \(\sum_{p\le n,p\nmid B_n}(\log p)/p=(1-\log2)\log n+o(\log n)\) is Sander93's theorem. It still leaves the small-prime unweighted contribution uncontrolled.

The remaining question is an all-n upper bound allowing deep, sparse fixed-prime contributions while controlling their aggregate reciprocal mass. No such argument or unbounded exact-target construction was obtained in this attempt.

## Sources

- **EGRS75:** P. Erdős, R. L. Graham, I. Z. Ruzsa, E. G. Straus, *On the prime factors of (2n choose n)*, Mathematics of Computation 29 (1975), 83–92. [Original complete PDF](https://www.renyi.hu/~p_erdos/1975-27.pdf). All 10 pages read and visually inspected. Target on p.83; digit criterion and two-base theorem pp.84–86; full first- and second-moment proofs pp.86–89; divergent uniform upper-bound context p.90.
- **Sander93:** J. W. Sander, *On primes not dividing binomial coefficients*, Mathematical Proceedings of the Cambridge Philosophical Society 113 (1993), 225–232, DOI [10.1017/S0305004100075927](https://doi.org/10.1017/S0305004100075927). [Complete institutional PDF](https://repo.uni-hannover.de/server/api/core/bitstreams/5c4a6a87-c5d9-445c-8fc1-07c8323829a0/content). All 8 pages read and visually inspected, including the entire weighted proof. Lemma 1 on p.226 is input (8), not the final weighted theorem.
- **Sander92:** J. W. Sander, *Prime power divisors of binomial coefficients*, Journal für die reine und angewandte Mathematik 430 (1992), 1–20, DOI [10.1515/crll.1992.430.1](https://doi.org/10.1515/crll.1992.430.1). [Complete German National Library PDF](https://d-nb.info/1211032906/34). The exponential-sum proof in Sections 2–3, pp.2–14, was read and visually inspected. Pages 14–16 of the related distribution argument were also inspected. No claim is made to have independently re-proved every cited antecedent analytic theorem.

The authored proof and historical finite tests are independent of the advertised finite 10^8 computation. That computation was not executed or accepted by this work. The historical checks summarized in AUDIT.md and VERIFICATION.json corroborate finite identities only; the universal statements rest on the proofs. The complete test programs and receipts are not distributed in this prose-only edition.
