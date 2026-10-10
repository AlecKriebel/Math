# Independent audit of the EP377 carry depth partial result

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

## Verdict and scope

**ACCEPTED AS A PARTIAL RESULT. No mathematical correction is required.**

This audit accepts the elementary carry and cutoff theorems, the fixed-shell limit derived from the cited Sander estimate, and the stated liminf and limsup consequences in the accepted original result, reproduced editorially as `PROOF.md`. Acceptance does not prove or disprove the absolute-bound problem

\[
\sup_{n\ge1}\sum_{\substack{p\le n\\p\nmid\binom{2n}{n}}}\frac1p<\infty.
\]

That problem remains unresolved by the audited work. This is an independent mathematical review with independently written finite tests, not a formal proof verification, a novelty certification, or a replication of an advertised computation through \(10^8\).

The originally reviewed result has SHA256 `3413fbcddc7b9bd3a65f8d23be462777d02d67573fe1abb5a0f9b47534e89a21` and 14,047 bytes. Its containing manifest has SHA256 `1a4935d4a9366c47d5e5d0db1431c5d4f51403e05c778575dfc3ae1859ce5798` and 11,481 bytes. At the original audit, all 53 listed files matched their recorded lengths and hashes, and the external candidate seal agreed. The independent auditor did not modify or execute candidate files. These original identities are distinct from the editorial edition identities recorded in ACCEPTANCE.json and MANIFEST.json.

## Exact predicate and shell obstruction

For \(B_n=\binom{2n}{n}\), factorial valuations give

\[
v_p(B_n)=\sum_{j\ge1}\left(\lfloor 2n/p^j\rfloor-2\lfloor n/p^j\rfloor\right)
         =\sum_{j\ge1}\lfloor2\{n/p^j\}\rfloor.
\]

The terms are nonnegative and vanish once \(p^j>2n\). Consequently nondivisibility means every residue lies strictly below half its modulus. The strict inequality in the candidate is correct, including the prime 2. If \(n>0\), its highest nonzero binary digit violates the criterion, so 2 never contributes.

For odd \(p\), an allowed digit is at most \((p-1)/2\). If every digit is allowed, the first \(j\) digits have value at most \((p^j-1)/2\). If a digit is too large, its own contribution already exceeds \(p^{j}/2\) at the corresponding level. This proves both directions without reliance on the OCR of a divisibility symbol. The result agrees with EGRS75, printed page 84, and Sander93, equation (10), printed page 227.

The shell condition is exactly

\[
p^r\le n<p^{r+1},\qquad r=\lfloor\log_p n\rfloor\ge1.
\]

Every eligible prime belongs to precisely one shell. At \(n=q^r\), with \(q\) odd, the base-\(q\) expansion is a single 1 followed by zeros. Therefore \(F_r(q^r)\ge1/q\). In particular every proposed uniform envelope must satisfy \(a_r\ge1/3\), which rules out a summable envelope, \(A/r\), and \(A\rho^r/r\) for fixed \(A>0\), \(0<\rho<1\). Deleting finitely many primes does not repair this: choose a fixed odd \(q\) outside the deletion set.

This is a moving fixed-size contribution. It supplies neither an unbounded sequence of exact values \(f(n)\) nor simultaneous nondivisibility for arbitrarily many prescribed primes.

## Common carry cutoff theorems

### Sublogarithmic cutoff

Fix a nonempty finite set \(S\) of odd primes, put \(Q=\prod_{p\in S}p\), and take \(n=Q^m\). If \(L(n)=o(\log n)\), then

\[
L(Q^m)/m=\log Q\,L(Q^m)/\log(Q^m)\longrightarrow0.
\]

Eventually \(L(Q^m)\le m\), and all tested residues for each \(p\in S\) vanish. Thus \(H_L(Q^m)\ge\sum_{p\in S}1/p\). Divergence of the reciprocal-prime sum makes \(H_L\) unbounded. The order of quantifiers is correct: first fix a desired bound and the finite set \(S\), then let \(m\) grow. Neither monotonicity of \(L\) nor a threshold uniform in \(S\) is required.

The empty-set case in the theorem is vacuous; one may choose any arbitrarily large integers rather than using \(Q=1\). This was a harmless omitted trivial case in the original proof, not a defect in the nonempty construction or the conclusion. PROOF.md now states it explicitly as an editorial clarification.

The explicit warning at \(n=225\) is correct. In base 3, \(225=(22100)_3\); the first failing residue level is 4, and \(v_3(B_{225})=2\). In base 5, \(225=(1400)_5\); the first failing level is 3, and \(v_5(B_{225})=1\). Both primes pass the first two tests but are actual divisors.

### Logarithmic cutoff

Let \(L_c(n)=\lfloor c\log(2n)\rfloor\) with fixed \(c>0\). Since \(L_c(n)+1>c\log(2n)\), for \(p\ge e^{1/c}\),

\[
p^{L_c(n)+1}>p^{c\log(2n)}\ge2n.
\]

All untested conditions are automatic for these primes. Hence the candidate's exact error bound is valid:

\[
0\le H_{L_c}(n)-f(n)\le\sum_{3\le p<e^{1/c}}1/p.
\]

The exceptional set uses a strict upper bound; a prime exactly equal to \(e^{1/c}\) is not exceptional. The bound can grow when \(c\downarrow0\); no uniformity in \(c\) is asserted. For \(c\ge1/\log3\), the exceptional set is empty and the two sums are identically equal.

The title's cutoff dichotomy should be read as the two proved statements for \(o(\log n)\) and fixed positive logarithmic depth. It is not a classification of arbitrary oscillating depth functions.

## Analytic input and all integer fixed shell limit

The relevant published input is Sander93, Lemma 1, printed page 226, rather than merely that paper's final logarithmically weighted asymptotic. Its parameters, powers, and logarithmic factor agree with equation (8) of the candidate. In particular the real coefficient belonging to the least retained exponent is at least 1, the largest exponent is at most fixed \(k\), and the domain is \(2\le t\le n^{1/k}\).

Sander92, Theorem 2, printed pages 13–14, uses the least exponent \(j_1\) in the middle error term and permits \(t\le n^{1/j_1}\). Replacing \(j_1\) by the larger \(k\) weakens the term and restricts the domain, exactly as the candidate says. The proof chain in Sander92 Sections 2–3, printed pages 2–14, was inspected, including the coefficient hypotheses, derivative estimates, bilinear estimate, use of Vaughan's identity, and partial summation to primes. Its cited antecedent analytic theorems remain accepted published inputs; this audit does not claim to reprove them from first principles.

Here is an independent check of every limiting step. Fix \(r\ge1\), then fix

\[
0<\delta<1/(2r(r+1)),\quad a=1/(r+1)+\delta,\quad b=1/r-\delta.
\]

For \(n^a<p\le n^b\), eventually \(p^r<n\) and \(p^{r+1}>2n\). Thus only the first \(r\) residue conditions matter on this trimmed interval.

Fix a nonzero \(h\in\mathbb Z^r\). Delete zero coordinates and, if needed, negate all coordinates and conjugate. The first retained coefficient is then a positive integer, so Sander's coefficient hypothesis is satisfied. Set \(M=\max_j|h_j|\ge1\). Because \(h\) is fixed, eventually \(\log(Mn)\le2\log n\). For \(n^a\le t\le n^b\), the three terms in the exponential-sum bound divided by \(t\) are at most a constant times

\[
n^{-c_ra^3/4},\qquad n^{-r\delta/2},\qquad M^2n^{-a/6},
\]

respectively, apart from \((\log n)^{4r}\). All three exponents give a positive power saving. The second term, in particular, would lose this saving at the untrimmed upper endpoint; the fixed trimming is doing necessary work.

Writing the cumulative exponential sum as \(S_h(t)\), partial summation therefore gives

\[
\sum_{n^a<p\le n^b}\frac{e(n\sum_{j=1}^rh_j/p^j)}p
=\frac{S_h(n^b)}{n^b}-\frac{S_h(n^a)}{n^a}
 +\int_{n^a}^{n^b}\frac{S_h(t)}{t^2}\,dt=o(1).
\]

The integral costs at most one additional factor of \(\log n\), which the power saving absorbs. There is no need for an estimate below \(n^a\), nor for a bound uniform in the Fourier frequency.

By Mertens, the reciprocal-prime mass on the trimmed interval tends to \(\log(b/a)\). Its nonconstant Fourier coefficients tend to zero, so the corresponding measures converge to \(\log(b/a)\) times Haar measure on the fixed \(r\)-torus. Continuous periodic majorants and minorants of the half-box, followed by finite trigonometric approximations, justify the discontinuous indicator. Their values can be kept in \([0,1]\), and the half-box boundary has Haar measure zero. Thus the accepted trimmed limit is \(2^{-r}\log(b/a)\).

The reciprocal mass discarded from the shell tends to

\[
\log\frac{a}{1/(r+1)}+\log\frac{1/r}{b},
\]

which goes to zero with \(\delta\). Nonnegativity permits squeezing the nondividing contribution between the trimmed mass and that mass plus the discarded bound. Consequently

\[
\boxed{\lim_{n\to\infty}F_r(n)=2^{-r}\log(1+1/r)\quad\text{for every fixed }r.}
\]

The limit is over all positive integers \(n\), not an almost-everywhere assertion. The order is fixed \(r\), fixed trimming, fixed finite Fourier approximations, \(n\to\infty\), approximation refinement, and finally \(\delta\downarrow0\). None of these steps allows \(r\) to grow with \(n\). In particular \(c_r\), the implied constants, thresholds, and approximation complexity need not be uniform in \(r\).

## Constants and consequences

The constant identity is correct:

\[
c_0=\sum_{r\ge1}2^{-r}\log(1+1/r)
   =\sum_{k\ge2}2^{-k}\log k
   \approx0.50783392286843839219.
\]

Both series converge absolutely, so shifting and subtracting the logarithm series is legitimate. For the first series, its tail after \(R\) is bounded by \(2^{-R}/(R+1)\), using \(\log(1+1/r)\le1/r\).

For every fixed \(R\), nonnegativity gives

\[
\liminf_{n\to\infty}f(n)\ge\sum_{r=1}^{R}2^{-r}\log(1+1/r).
\]

Sending \(R\to\infty\) proves the lower inequality. EGRS75 Theorem 2, printed pages 86–87, gives the Cesàro mean \(c_0\). If the liminf were strictly larger, all sufficiently late terms would exceed \(c_0\) by a fixed positive amount, contradicting that mean. This proves \(\liminf f(n)=c_0\), as claimed.

At \(n=3^m\), the prime 3 lies in shell \(m\). For fixed \(R\) and \(m>R\), its \(1/3\) contribution is disjoint from the first \(R\) shells. Applying the all-integer shell limits along this sequence and then increasing \(R\) gives

\[
\liminf_{m\to\infty}f(3^m)\ge c_0+1/3.
\]

For the stronger limsup bound, EGRS75 Theorem 1, printed pages 84–86, has hypothesis \(A/(p-1)+B/(q-1)\ge1\), with allowed digits at most \(A,B\). The non-strict comparison was checked directly in the page image; OCR incorrectly renders it in some extracts. Substitution \((p,q,A,B)=(3,5,1,2)\) gives equality, so the theorem applies. Along its infinite sequence, both fixed primes eventually lie outside any fixed finite set of shells. Therefore

\[
\boxed{\limsup_{n\to\infty}f(n)\ge c_0+8/15
\approx1.04116725620177172552.}
\]

There is no justified extension here from two specified primes to an arbitrary finite prime set. The truncation construction does not supply that missing extension.

The density-convergence remark agrees with EGRS75 Theorem 3 and its corollary, printed pages 87–89. It can also be recovered without that second-moment input once the audited lower limit is known: for each \(\varepsilon>0\), eventually \(f(n)-c_0+\varepsilon\ge0\), while its mean tends to \(\varepsilon\). Markov's inequality bounds the upper density of \(f(n)\ge c_0+\eta\) by \(\varepsilon/(\eta+\varepsilon)\); then let \(\varepsilon\downarrow0\). Lower deviations eventually disappear. Thus density convergence and failure of ordinary convergence are compatible.

## What this does not establish

For fixed \(0<\alpha<1\), Mertens gives

\[
\sum_{n^\alpha<p\le n}\frac1p=\log(1/\alpha)+o(1).
\]

This is bounded uniformly over all sufficiently large \(n\), and the finitely many remaining \(n\) can be absorbed into the bound. Hence restricting the target to \(p\le n^\alpha\) is indeed equivalent to the original boundedness problem.

The weighted result in Sander93 uses \((\log p)/p\), not \(1/p\). Its normalization does not control the aggregate reciprocal mass of very small primes. Likewise, fixed-shell convergence does not permit interchanging an infinite shell sum and the limit; the prime-3 subsequence already disproves that exchange. The accepted material excludes two particular upper-bound strategies and identifies precise asymptotic components. It supplies no uniform bound on the remaining deep-shell mass and no unbounded exact-target construction.

## Historical independent computational checks

The audit's standard-library program was written independently and does not import or execute the candidate's scripts or any third-party code. Normal Python, `-O`, and `-OO` runs produced byte-identical successful receipts.

- All \(1\le n\le5000\) and all primes \(p\le n\): 1,797,533 comparisons of factorial valuations, base-\(p\) digits, and prime-power residues.
- All \(n\le700\): 48,013 additional direct reductions of the literal integer \(\binom{2n}{n}\).
- Exact shell partitions through \(n=5000\).
- Cutoffs with \(c=1/\log a\), \(a\in\{2,3,4,5,7,10,11,97\}\): 14,340,272 comparisons, with \(L=\lfloor\log_a(2n)\rfloor\) evaluated by integer arithmetic. No floating threshold comparisons are used.
- Moving-atom witnesses for primes 3, 5, 7, 11, 101 at depths 1, 2, 3, 10, 50, 100.
- The \(n=225\) cutoff counterexample and primorial-power witnesses for \(L(n)=\lfloor\sqrt{\log_2 n}\rfloor\).
- Twenty-six simultaneous 3-and-5 examples occur through 5000; the first are 10, 12, 27, 30, 31. These examples corroborate the predicate, not infinitude.

The largest numerically evaluated value in this finite scan occurred at \(n=3250\), approximately 1.1792429057944813. This is a finite numerical observation, not a universal maximum or an asymptotic estimate. The decimal constant evaluations are approximations, not interval-arithmetic certifications.

The independently authored inventory verifier checks an externally pinned manifest digest, exact file membership, member lengths and hashes, duplicate keys and paths, canonical relative paths, symlinks, and regular-file types. Sixteen synthetic acceptance/rejection controls pass in all three Python modes. Inventory success authenticates bytes and finite receipts; it does not replace the mathematical reasoning above.

## References and inspection limits

- P. Erdős, R. L. Graham, I. Z. Ruzsa, E. G. Straus, *On the prime factors of (2n choose n)*, Mathematics of Computation 29 (1975), 83–92. [Original PDF](https://www.renyi.hu/~p_erdos/1975-27.pdf). Relevant definitions, two-base argument, first moment, second moment, and density statement were inspected; printed pages 84–89 were checked visually.
- J. W. Sander, *On primes not dividing binomial coefficients*, Mathematical Proceedings of the Cambridge Philosophical Society 113 (1993), 225–232. [DOI](https://doi.org/10.1017/S0305004100075927); [institutional PDF](https://repo.uni-hannover.de/server/api/core/bitstreams/5c4a6a87-c5d9-445c-8fc1-07c8323829a0/content). Printed pages 225–227 were checked visually, especially Lemma 1 and equation (10); extracted text of the weighted proof was consulted for context.
- J. W. Sander, *Prime power divisors of binomial coefficients*, Journal für die reine und angewandte Mathematik 430 (1992), 1–20. [DOI](https://doi.org/10.1515/crll.1992.430.1); [German National Library PDF](https://d-nb.info/1211032906/34). Printed pages 2–14 were inspected visually and in extracted text. Earlier analytic references cited within the paper are accepted as published inputs.

Source hashes, byte counts, public URLs, and the original proof and audit inspection histories are recorded in `SOURCES.json`. Copied source PDFs, page images, and extracted source text are not included in this edition. Full computational receipts and programs are also excluded; the counts and match results above are historical verification metadata.
