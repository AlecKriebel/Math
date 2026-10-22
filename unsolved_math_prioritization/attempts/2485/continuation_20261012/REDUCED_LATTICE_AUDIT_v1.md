# Independent audit: reduced-lattice bound for the Erdős–Selfridge minimum

Date: 12 October 2026.

## Verdict and frozen scope

**PASS.** The complete frozen proof `REDUCED_LATTICE_BOUND_v1.md` was read and independently reconstructed: **13,527 bytes**, SHA-256 **7bcf11dfe2cc43082d71932ae3dbf6ec5a608db21f0e1fef9ab8f0cb3095f418**.

It proves, with the prime number theorem as a standard input,

\[
\limsup_{k\to\infty}\frac{\log g(k)}k\le\frac{813}{875}<\frac{93}{100}<1,
\]

for the actual minimum

\[
g(k)=\min\{n>k+1:\ p\nmid\tbinom nk\text{ for all primes }p\le k\}.
\]

Consequently **\(g(k)<\exp(0.93k)<L_k\) for every sufficiently large integer \(k\)**, with \(L_k=\operatorname{lcm}(1,\ldots,k)\). This includes the eventual strict lcm comparison, rather than only a smaller density estimate. The proof supplies no explicit numerical onset and does not settle the comparison at every integer, subexponential growth, or the successive-ratio conjectures. The audit does not certify novelty or priority.

This is a separate principal-exponent result. It does not retrospectively change the accepted square-root secondary-overhead theorem, whose full-lcm construction cannot by itself imply the present conclusion.

## 1. Lattice, valuations, and the strict domain

The proposed multiplier lattice is

\[
M_k=L_k\left(\prod_{p\le\sqrt k}p\right)\left(\prod_{6k/7<p\le k}p\right)^{-1}.
\]

For \(k\ge9\), the forced, retained, and omitted prime intervals are disjoint and exhaustive. Since every omitted prime exceeds \(\sqrt k\), it occurs exactly once in \(L_k\), and division removes its entire valuation. The extra forcing product cannot put it back. Thus \(M_k\) is an integer, and its valuations are exactly:

- \(a_p+1\) when \(p\le\sqrt k\), where \(p^{a_p}\le k<p^{a_p+1}\);
- one when \(\sqrt k<p\le6k/7\);
- zero when \(6k/7<p\le k\).

The base-\(p\) coefficient identity included in the manuscript proves the Lucas criterion used, including zero digits above the highest digit of \(k\). No condition at a smaller prime or a higher prime-power digit is omitted.

The domain argument is especially strong. Both 2 and 3 are forced for \(k\ge9\). The relatively prime integers \(2^{a_2+1}>k\) and \(3^{a_3+1}>k\) divide \(M_k\); their product therefore divides it and exceeds \(k^2\). Consequently every \(t\ge1\) gives \(tM_k-1>k+1\). Survival in the sieve really produces a competitor in the definition of \(g(k)\), not one of the excluded trivial values.

## 2. Exact local counts and mixed-modulus CRT

For forced primes, all relevant digits of \(tM_k-1\) equal \(p-1\), and the local criterion always passes.

For retained primes write \(M_k=pc_p\), with \(p\nmid c_p\). The units digit is \(p-1\) and the next digit is \((tc_p-1)\bmod p\). This identity also covers \(tc_p\equiv0\), giving digit \(p-1\). Hence precisely the classes

\[
tc_p\bmod p\in\{1,\ldots,\lfloor k/p\rfloor\}
\]

are forbidden. The modulus is \(q_p=p\), the cardinality is \(\beta_p=\lfloor k/p\rfloor\), and \(0<\beta_p<p\).

For omitted primes, \(p\nmid M_k\), so multiplication by \(M_k\), followed by subtraction of one, is a bijection modulo \(p^2\). Here \(k=p+(k-p)\) has high digit 1 and units digit \(k-p\). An admissible residue has \(p-1\) choices for its high digit and \(2p-k\) choices for its units digit. Therefore

\[
q_p=p^2,\quad
\beta_p=p^2-(p-1)(2p-k)=p(k-p)+2p-k,
\]

\[
w_p=\beta_p/p^2=k/p-1+(2p-k)/p^2.
\]

Both digits are essential. At the endpoint \(p=k\), the units restriction disappears but the leading digit still excludes \(p\) classes; the exact weight is \(1/p\), not zero.

All active moduli are powers of different underlying primes. They are pairwise coprime even though some equal \(p\) and others equal \(p^2\). CRT yields exactly \(\prod_{p\in J}\beta_p\) simultaneous forbidden classes modulo \(\prod_{p\in J}q_p\). Each individual class on \([1,T]\) has discrepancy less than one, so the aggregate discrepancy is at most \(\prod_{p\in J}\beta_p\). This remains true when a joint modulus is much larger than \(T\).

## 3. First-survivor bound, including every endpoint error

For even \(r\), the truncation through degree \(r-1\) is an odd Bonferroni lower bound. A point rejected by \(\nu\ge1\) primes contributes

\[
\sum_{j=0}^{r-1}(-1)^j\binom\nu j=-\binom{\nu-1}{r-1}\le0;
\]

a survivor contributes one. The empty intersection has exactly \(T\) members and contributes no error. Taking absolute values of all nonempty intersection errors gives precisely

\[
E_{r-1}=\sum_{j=1}^{r-1}e_j(\beta).
\]

The odd/even bounds on one full period yield \(Q_{r-1}\le\rho\le Q_{r-1}+e_r(w)\). Positivity of coefficients gives \(e_r(w)\le4^{-r}\prod_p(1+4w_p)=R_r(4)\). Thus

\[
N(T)\ge T(\rho-R_r(4))-E_{r-1}.
\]

When \(R_r(4)\le\rho/2\), the exact integer choice \(T=\lfloor2E_{r-1}/\rho\rfloor+1\) makes the lower bound strictly positive, including the case when \(2E_{r-1}/\rho\) is an integer. The theorem proves survival in the specified initial interval. It does not replace its counting function by full-period density.

The finite lemma also correctly handles empty forbidden sets and truncation orders beyond the list length under its zero-coefficient conventions.

## 4. Prime-sum asymptotics and truncation order

The lattice identity

\[
\log M_k=\psi(k)-\theta(k)+\theta(6k/7)+\theta(\sqrt k)
\]

is exact, including prime-square boundaries. The elementary estimate for \(\psi(k)-\theta(k)\) is more than sufficient. PNT gives \(\log M_k=(6/7+o(1))k\).

For retained primes, the manuscript controls every leading digit: \(w_p\le k/p^2\) and \(1-w_p\ge1/p\). On \((\sqrt k,2\sqrt k]\), summation even over all integers costs at most \(O(\sqrt k\log k)\); above that interval, \(w_p\le1/4\) and the convergent integer square tail costs \(O(\sqrt k)\). Hence the combined logarithmic contribution is \(o(k/\log k)\). There is no hidden uniform PNT requirement near \(\sqrt k\).

On the omitted interval, the replacement

\[
w_p=(p/k)^{-1}-1+O(1/k)
\]

is uniform, and its limiting weight is at most \(1/6\). The derivative of \(\ell(w)=\log((1+4w)/(1-w))\) is bounded on a fixed neighborhood of these weights. The total replacement error is therefore \(O(1)\), even with the coarse bound of \(k\) primes. Weighted PNT is used only on the fixed compact interval \([6/7,1]\), with a continuous integrand, and the manuscript's step-function argument justifies it.

Independent integration gives

\[
K=\int_{6/7}^{1}\log\frac{4-3u}{2u-1}\,du
=\frac{10}{21}\log\frac{10}{7}+\frac5{14}\log\frac57.
\]

With fixed \(A=9/250\) and \(r=2\lceil Ak/(2\log k)\rceil\), rounding changes \(r\) by less than two, so

\[
\log(R_r(4)/\rho)=[K-A\log4+o(1)]k/\log k.
\]

The exact positive margin verified below ensures this tends to minus infinity, not merely that its leading formal expression is negative. Also \(-\log\rho=O(k/\log k)\), as separately needed for the multiplier bound.

## 5. The larger prime-square endpoint budget

Every \(\beta_p\) is at most \(k^2\), and there are at most \(k\) active primes. Hence \(B=\sum\beta_p\le U=k^3\). The expansion of \(B^j\) gives \(e_j(\beta)\le U^j/j!\). For \(m=r-1\), eventually \(U\ge r\), so all terms up to \(m\) are increasing and

\[
E_{r-1}\le mU^m/m!\le m(eU/m)^m=V.
\]

Because \(m=(A+o(1))k/\log k\),

\[
\log V=(2A+o(1))k.
\]

The factor **2** is correct and necessary for this bound: \(\log U-\log m=2\log k+\log\log k+O(1)\). The argument retains the entire growing sum of errors and the full \(p^2\)-residue cardinalities. It does not undercount errors by substituting modulus-\(p\) costs.

The selected \(T\) satisfies \(T\le3V/\rho\) eventually, hence \(\log T\le(2A+o(1))k\). Combining with the lattice cost gives \(6/7+2A=813/875\). This bounds the actual witness \(tM_k-1\), so the corresponding upper bound on the minimum follows.

## 6. Independent exact rational certificate

The author's displayed 40-term logarithm sum was independently evaluated with rational arithmetic. All four checks passed:

1. \(23004153/10^{11}<D_{40}\).
2. \(D_{40}<23004154/10^{11}\).
3. The displayed rational tail bound is less than \(10^{-18}\).
4. \(D_{40}\) minus that tail bound is greater than \(1/5000\).

The three series parameters are exactly \(3/5,3/17,-1/6\); the negative parameter causes no issue because the error bound is absolute. The tail bound is approximately \(3.5958587\times10^{-20}\). Independently using 80 terms also certifies

\[
0.0002300415<\Delta=(9/250)\log4-K<0.0002300416.
\]

These are exact rational checks. Floating-point values are descriptive only. The finite sums and error bound are fully specified in the frozen proof, so its mathematical acceptance does not depend on access to diagnostic software.

## 7. Strict eventual lcm comparison and effective scope

The limsup coefficient is strictly smaller than \(0.93\). Thus \(\log g(k)<0.93k\) for all sufficiently large \(k\), by the definition of limsup. Separately, PNT gives \(\log L_k/k\to1\), so \(\log L_k>0.93k\) eventually. Intersecting these two eventual ranges proves precisely

\[
g(k)<\exp(0.93k)<L_k.
\]

No step requires the same initial thresholds or an explicit value for either threshold. This is an unconditional eventual statement using the standard proven PNT, not a conditional density heuristic. The finite sieve test is effectively computable for any specified parameters; the present asymptotic analysis does not calculate an effective universal onset. Finite diagnostics do not fill that gap, and no all-\(k\) claim is accepted.

## 8. Independent finite diagnostics

The independently written standard-library program imports none of the author's code. Its completed checks include:

- 859 omitted-prime pairs for \(3\le k\le120\), covering **3,515,998** residues modulo \(p^2\), with both digit conditions and exact cardinalities checked.
- Every upper-half omission subset for \(3\le k\le22\): **126 configurations**.
- **37,180** joint intersection endpoint checks; **3,150** finite Bonferroni interval bounds; **12,600** generating-function checks; **119** certified initial survivor intervals.
- **4,368** exact binomial candidates and **48,032** primewise comparisons for the preliminary and all-subset constructions.
- The final \(6/7\) construction for **112 values**, \(9\le k\le120\): **3,584** exact binomial candidates, **64,576** primewise comparisons, **960** finite interval bounds, and **36** certified survivor intervals.
- Six negative controls: missing leading digit, missing units digit, the \(p=k\) endpoint, an excluded trivial-domain survivor, wrong Bonferroni parity, and omitted endpoint errors.

The program passed under normal Python, `-O`, and `-OO`, with byte-identical output. Explicit exception checks, rather than Python assertions, remain active in every mode. The frozen proof's specific rational certificate was separately replayed. These are regression diagnostics supporting the full proof review, not proofs of the asymptotic threshold.

The separate author-written checker was fully inspected and independently rerun in all three Python modes. All three replay outputs matched the author's frozen receipts byte for byte. Those additional tests covered 5,360 exact-binomial candidates, 653 local residue counts, 251,576 prime-square residues, 1,675 finite lower bounds, 2,133 joint CRT discrepancies, and ten certified initial-interval witnesses. The author's three stated negative controls and exact Section 6 rational certificate also passed.

## 9. Source-credit and literature scope

The [1974 Ecklund–Erdős–Selfridge paper](https://www.renyi.hu/~p_erdos/1974-01.pdf), printed pages 648–649, was freshly inspected. It supplies the original lcm lattice and principal coefficient-one upper bound, and explicitly identifies the then-unproved comparison with \(L_k\). The new proof's attribution and eventual-only qualification are accurate.

[Ford's 2023 notes](https://ford126.web.illinois.edu/sieve2023.pdf), Theorem 1.5 and Lemma 1.6, and [Tao's sieve notes](https://terrytao.wordpress.com/2015/01/21/254a-notes-4-some-sieve-theory/), Exercise 9, were freshly checked. They support the manuscript's attribution of its finite truncation to the classical Brun pure sieve; the general sieve lemma is not presented as new.

The inspectable [15-page 2020 author conference version](https://www.math.auckland.ac.nz/~sgal018/ANTS/papers/Sorenson-Sorenson-Webster.pdf), marked submitted 3 June 2020, was checked in §§1 and 5–6. Its actual-minimum comparison is UDH-conditional, while its unconditional density estimate counts full periods for sufficiently large \(x\). These do not substitute for the new first-survivor proof. The publisher endpoint was attempted but did not provide inspectable PDF text on this audit retrieval.

The [2021 arXiv v3 PDF](https://arxiv.org/pdf/1907.08559v3) and corresponding [HTML](https://arxiv.org/html/1907.08559v3) were freshly retrieved. The actual document is a six-page **addendum**, despite stale abstract metadata describing 25 pages. Its stated additions concern computed values and the reciprocal-density approximant. It is not a newly inspected proof of a principal-exponent bound for the actual minimum.

These bounded checks support the source distinctions above. They do not establish that no stronger theorem exists elsewhere or certify a publication-priority claim. No remote mutation or publication was performed during this audit.
