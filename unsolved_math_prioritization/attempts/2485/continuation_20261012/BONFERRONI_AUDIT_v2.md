# Independent mathematical audit: square-root overhead for the Erdős–Selfridge minimum

Date: 12 October 2026.

## Status and scope

**PASS, within the explicit mathematical and source-credit scope below.**

The complete proof in `BONFERRONI_BOUND_v1.md` was read, independently reconstructed, and checked against its frozen bytes: 14,344 bytes, SHA-256 `6f948bfa1d352a7cc00ec62f22c321b7901cafea32ff8476676e8cc713139962`.

The finite Bonferroni/CRT theorem and its general asymptotic consequence are correct. In particular, they prove

\[
\limsup_{k\to\infty}\frac{\log g(k)-\log L_k}{\sqrt{k}}\le\frac{13}{5},
\qquad
L_k=\operatorname{lcm}(1,\ldots,k),
\]

where the actual minimum retains the condition \(n>k+1\). No numerical-density heuristic replaces a first-survivor argument. This is an improvement of the stated secondary overhead, with the main exponential upper-bound scale still \(\exp((1+o(1))k)\). It does not prove the proposed subexponential scale, \(g(k)<L_k\), either successive-ratio conjecture, or novelty.

The accompanying frozen `CONSTANT_CERTIFICATE_v1.md` was also fully read and independently verified: 2,809 bytes, SHA-256 `b9704cd641649f094371664b31ba57e15cdac5f3c99ac6841cb182955c00a95e`. It supplies a self-contained exact rational certificate in authored prose. The proof and this supplement together do not require access to executable diagnostics.

## 1. Independent finite-count argument

Write \(a_p=\max\{a:p^a\le k\}\), \(b_p=\lfloor k/p^{a_p}\rfloor\), and \(M=L_k\prod_{p\in S}p\), with \(S\) an arbitrary subset of the primes at most \(k\). For every prime outside \(S\), the exponent of \(p\) in \(M\) is exactly \(a_p\). If \(M=p^{a_p}c_p\), its inverse factor \(c_p^{-1}\pmod p\) exists.

The lower \(a_p\) digits of \(tM-1\) in base \(p\) are all \(p-1\). The digit in position \(a_p\) is \((tc_p-1)\bmod p\), including the case \(tc_p\equiv0\), when the digit is \(p-1\). Consequently exactly the \(b_p\) classes satisfying \(tc_p\bmod p\in\{1,\ldots,b_p\}\) are forbidden. For \(p\in S\), the extra factor of \(p\) forces all relevant digits to \(p-1\), so the condition is automatic. These assertions also follow directly from the coefficient identity for \((1+X)^n\) modulo \(p\) used in the proof.

For any nonempty set of unforced primes \(J\), CRT gives exactly \(\prod_{p\in J}b_p\) forbidden joint classes modulo \(\prod_{p\in J}p\). For integer \(T\), each class count on \([1,T]\) differs from its expected size by less than one. Hence the joint-count error is bounded in absolute value by \(\prod_{p\in J}b_p\). This is deterministic endpoint counting, without probabilistic independence assumptions on the initial interval.

For even \(r\), the truncation at degree \(r-1\) is odd. On a point rejected by \(\nu\ge1\) primes its value is

\[
\sum_{j=0}^{r-1}(-1)^j{\nu\choose j}=-{\nu-1\choose r-1}\le0;
\]

on a survivor its value is one. Summing yields

\[
N(T)\ge TQ_{r-1}-E_{r-1},\qquad
E_{r-1}=\sum_{j=1}^{r-1}e_j(b).
\]

The absent \(j=0\) error is appropriate because the empty-set count is exactly \(T\). Taking the worst allowed error separately for each sign is valid and gives precisely this sum. The even truncation bounds the full-period survivor proportion from above, so

\[
Q_{r-1}\le\rho\le Q_{r-1}+e_r(w),
\qquad \rho=\prod_p(1-w_p),\quad w_p=b_p/p.
\]

Finally \(e_r(w)\le z^{-r}\prod_p(1+zw_p)\) for every \(z>0\), by positivity of coefficients. This proves the exact sufficient test stated in the manuscript, including the strict inequality on integer \(T\). Empty prime lists and truncations longer than the list cause no exception under the given zero-coefficient convention.

The domain check is also sound: for \(k\ge3\), \(L_k\ge k(k-1)\), and \(k(k-1)-1>k+1\). Thus every constructed candidate already exceeds both excluded initial values. The theorem intentionally does not use this argument for \(k=1,2\).

## 2. Prime-power and weighted-PNT checks

Put \(x=\sqrt{k}\) and force primes at most \(k^{1/3}\), together with those in \((x,cx]\), for a fixed \(c>1\). The unforced primes are exactly the disjoint sets

\[
k^{1/3}<p\le x,\qquad cx<p\le k.
\]

The first set has \(a_p=2\), including \(p=x\) if that endpoint is prime. The cube-root endpoint itself is forced. The second set has \(a_p=1\). Therefore the proof neither omits nor misassigns prime-square and prime-cube boundaries.

For the first set, \(w_p\le k/p^3\) and \(1-w_p\ge1/p\). The interval up to \(2k^{1/3}\) contributes at most \(O(k^{1/3}\log k)\) to \(-\log\rho\), even when counted over all integers. Above that cutoff, \(w_p\le1/8\), so elementary power-sum estimates give \(O(k^{1/3})\). The positive logarithm has the same or a smaller bound. Since

\[
\frac{k^{1/3}\log k}{\sqrt{k}/\log k}=k^{-1/6}(\log k)^2\longrightarrow0,
\]

the asserted negligibility is justified.

For the second set, \(w_p=k/p^2+O(1/p)\), and both logarithms have uniformly bounded derivatives because \(w_p\le c^{-2}<1\). The entire floor replacement costs \(O_{c,z}(\log k)\), which is negligible on the required scale. No fractional-part equidistribution is assumed.

The weighted PNT formula is valid. On a fixed interval \([c,R]\), PNT gives convergence of the scaled prime measure after division by \(x/\log x\). Both weights are continuous. Their tails are \(O_{c,z}(u^{-2})\), and partial summation of \(\pi(t)\ll t/\log t\) gives a normalized tail \(O_{c,z}(1/R)\), uniformly as \(x\to\infty\). This also handles the moving upper endpoint \(x^2\). Taking first \(x\to\infty\), then \(R\to\infty\), proves both asserted integral constants. All constants \(c,z,A\) stay fixed throughout these steps.

The extra prime product has logarithm

\[
\theta(k^{1/3})+\theta(cx)-\theta(x)=(c-1+o(1))x.
\]

The coefficient \(c-1\), rather than \(c\), is correct because the interval below \(\sqrt{k}\) is not wholly forced.

## 3. Growing truncation and complete endpoint budget

For fixed \(A>2(I(c)+J(c,z))/\log z\), the even rounding

\[
r=2\left\lceil\frac{A\sqrt{k}}{2\log k}\right\rceil
\]

changes \(r\) by less than two, a negligible error. It gives a strictly negative coefficient in \(\log(R_r/\rho)\) on the diverging scale \(\sqrt{k}/\log k\). Therefore \(R_r\le\rho/2\) eventually, with a genuine fixed margin.

The endpoint bound is not left as a fixed-order estimate. With \(m=r-1\) and \(U=k(1+\log k)\), the manuscript proves

\[
E_{r-1}\le m\frac{U^m}{m!}\le m(eU/m)^m=:V,
\qquad
\log V=(A/2+o(1))\sqrt{k}.
\]

Here \(U\ge r\) eventually ensures monotonicity of the displayed factorial terms. The coefficient \(A/2\) comes from \(\log U-\log m=\frac12\log k+O(\log\log k)\). The bound is on the full sum of all errors, including a growing number of subsets.

The exact integer choice \(T=\lfloor2E_{r-1}/\rho\rfloor+1\) strictly exceeds the sufficient threshold, even if \(2E_{r-1}/\rho\) is an integer. The estimate \(T\le3V/\rho\), together with \(-\log\rho=O(\sqrt{k}/\log k)\), proves \(\log T\le(A/2+o(1))\sqrt{k}\). This certifies an actual survivor in the initial multiplier interval.

Thus the general coefficient \(c-1+(I+J)/\log z\) follows by taking the limsup for each fixed \(A\), then decreasing \(A\) to its threshold. There is no unjustified moving-parameter substitution.

## 4. Self-contained rational certificate for 13/5

For \(c=8/5\) and \(z=4\), the required positive margin is

\[
\Delta=4\log4+\frac{16}{5}\log\frac{164}{39}
-2\log\frac{13}{3}-32\arctan\frac15
+8\arctan\frac1{239}-8\arctan\frac19.
\]

This is the manuscript's \(4\log4-2I-2J\), after using \(\arctan(5/4)=\pi/4+\arctan(1/9)\) and Machin's identity.

Define the rational finite sums

\[
\mathcal L(q)=2\sum_{j=0}^{39}\frac{v^{2j+1}}{2j+1},
\quad v=\frac{q-1}{q+1},
\qquad
\mathcal A(t)=\sum_{j=0}^{39}\frac{(-1)^jt^{2j+1}}{2j+1}.
\]

Let \(D\) be the preceding expression for \(\Delta\), replacing each logarithm by \(\mathcal L\) and each arctangent by \(\mathcal A\). Direct rational arithmetic gives

\[
\frac{402355317}{10^{10}}<D<\frac{402355318}{10^{10}}.
\]

For all three logarithms, \(0<v\le5/8\); for all three arctangents, \(0<t\le1/5\). The geometric logarithm-tail bound and alternating-series bound therefore give

\[
|\Delta-D|\le
\frac{46}{5}\frac{2(5/8)^{81}}{81(1-(5/8)^2)}
+\frac{48}{81\,5^{81}}<10^{-15}.
\]

Every number in the last two inequalities is rational, and the finite sum has been specified completely. It follows, without floating-point assumptions or an external executable, that

\[
0.0402355<\Delta<0.0402356.
\]

Taking the fixed value \(A=4\) is consequently valid, and \(c-1+A/2=13/5\). The more precise general theorem remains valid, but this audit makes no numerical-optimization claim.

## 5. Independent finite diagnostics

An independently written standard-library checker, which does not import the proof author's program, checks:

- Every forcing subset for every \(3\le k\le20\), covering 1,176 configurations.
- Five even truncation orders and five rational generating-function parameters, giving 29,400 coefficient and sign checks.
- Exact CRT-aggregate error bounds for ten initial intervals, giving 294,000 rounding checks.
- 10,307 sufficient-criterion intervals with \(T\le256\), each replayed directly to find a survivor.
- Direct exact binomial divisibility for five forcing choices, including the manuscript's selective set, all \(3\le k\le100\), and \(1\le t\le32\): 15,680 candidates and 234,240 primewise comparisons.
- Exact rational constant intervals and separate negative controls for wrong truncation parity, the omitted minus-one digit shift, missing endpoint errors, and the small-\(k\) domain restriction.

The independent checker completed under normal Python, `-O`, and `-OO`, with byte-identical results. Explicit exception checks remain active under optimization. The proof author's separate checker was fully inspected and replayed under all three modes; its outputs also matched its frozen receipts exactly. Those additional checks covered 12,720 exact-binomial candidates, 4,240 initial-interval inequalities, 3,711 individual CRT-subset discrepancies and 389 certified witness intervals.

These finite tests are regression diagnostics, not a substitute for the proof or an effective threshold for the asymptotic theorem. No diagnostic executable or raw result file is needed for the self-contained mathematical argument.

## 6. Source-credit and claim boundaries

The original [Ecklund–Erdős–Selfridge paper (1974)](https://www.renyi.hu/~p_erdos/1974-01.pdf), especially printed pages 648–649, was independently retrieved. It gives the earlier lattice construction and the principal exponential upper bound. The manuscript correctly credits that construction and limits its claimed change to selective forcing and a controlled finite sieve.

The [Sorenson–Sorenson–Webster updated author manuscript abstract](https://arxiv.org/abs/1907.08559v3) was independently inspected. It distinguishes a heuristic relationship with a density approximant from unconditional statements about counts. The abstract's update is dated 1 June 2021 and carries a work-in-progress title; this audit does not certify acceptance of that update, inspect the entire revised paper, or establish a literature-wide priority claim.

The proposed result concerns the actual minimum and leaves the named open problems unresolved. The proof's no-priority and no-resolution qualifications are accurate. No source text, dataset, private source, or coordination material is needed for the mathematical acceptance report.
