# Independent audit: reduced denominators of the factorial-minus-one series

**Review scope.** These AI-assisted authored documents and their independent internal AI audit are unrefereed. “Accepted” means only the stated partial mathematical scope. No external human peer review, journal acceptance, formal proof-assistant certification, novelty, or current worldwide open-status certification is claimed. This prose edition omits executable checkers, detailed test outputs, source documents, extracted text, and page images. Its verification statements describe historically recorded checks; edition preparation performed no new scholarly-source retrieval or inspection.

## Verdict and exact scope

**ACCEPT the three partial-theorem conclusions in the authenticated candidate, without a required mathematical correction.** In particular, with

\[
H_N=\sum_{n=2}^N\frac1{n!-1},\qquad Q_N=\operatorname{den}(H_N),\qquad
S=\sum_{n=2}^{\infty}\frac1{n!-1},
\]

and \(H_1=0,Q_1=1\), the candidate proves

\[
\limsup_{N\to\infty}\frac{\log Q_N}{N^{3/2}\log N}\ge\frac13.
\]

For each fixed \(0<c<1/3\), the set
\(A_c=\{N\ge2:\log Q_N\ge cN^{3/2}\log N\}\)
has lower asymptotic density at least \(1/2\), and
\(Q_N(S-H_N)\to+\infty\) through \(A_c\).

This is an audit of that partial theorem. It neither proves nor disproves irrationality, does not certify novelty or a current exhaustive literature status, and does not certify a proof-assistant formalization.

The reviewed candidate inventory was authenticated independently: 18 members; inventory size 4012 bytes; inventory SHA-256 `9529c51acdf8919fe403e84f4fb2841d344b088ee0d54673ef34d7111cfee154`. The 4012-byte count is the inventory's size, not the payload's total size. All member sizes and hashes and closed-world coverage matched. The proof under review has SHA-256 `602a72e1fb1e5bc43a449c2a0ee0e1706f9b94ec45dbb5f84eeb930df653de0c` and 10070 bytes.

## 1. Reciprocal-sum cancellation: complete valuation audit

Let \(d_1,\ldots,d_k\) be positive integers and define
\(P=\prod d_i\), \(G=\prod_{i<j}\gcd(d_i,d_j)\), and
\(D=\operatorname{den}(\sum_i1/d_i)\).
The precise lemma needed is \(P\mid DG^2\). It is true including repeated denominators and denominators equal to one.

For \(k=1\), the statement is equality. For \(k\ge2\), fix a prime \(p\) and order the exponents \(a_i=v_p(d_i)\) decreasingly. Then

\[
v_p(P)=\sum_{i=1}^k a_i,
\qquad
v_p(G)=\sum_{j=2}^k(j-1)a_j.
\]

The second identity counts exactly the \(j-1\) pairs whose smaller exponent is the \(j\)-th exponent; ties do not invalidate the count.

If \(a_1>a_2\), multiply the reciprocal sum by \(p^{a_1}\). It is a rational number with denominator coprime to \(p\), and exactly one summand is a unit modulo \(p\); all other summands vanish modulo \(p\). Thus the sum has valuation \(-a_1\) and \(v_p(D)=a_1\), without any assumption that other prime powers survive. Therefore

\[
v_p(D)+2v_p(G)-v_p(P)
=\sum_{j=2}^k(2j-3)a_j\ge0.
\]

If \(a_1=a_2\), no denominator-survival claim is needed: directly,

\[
v_p(P)-2v_p(G)
=a_1-a_2-\sum_{j=3}^k(2j-3)a_j\le0\le v_p(D).
\]

This also covers the all-zero exponents. Divisibility follows prime by prime. Since \(P,D,G\) are positive, \(D\ge P/G^2\) follows as an ordinary real inequality, even when the right side is below one.

The square is genuinely necessary for the proposed general lemma: \(1/3+1/6=1/2\) gives \((P,D,G)=(18,2,3)\), so \(P\nmid DG\) while \(P=DG^2\). The tied-maximum case cannot be replaced by a survival assertion: \(1/2+1/2=1\) completely cancels the maximal power of two.

**Audit finding:** the valuation coefficients, cases, directions, and endpoint hypotheses are correct. No cancellation hypothesis is missing.

## 2. Factorial gap, terminal block, and prefix transfer

For \(2\le i<j\), write \(r=j!/i!\). This is a positive integer greater than one, and
\(r(i!-1)-(j!-1)=1-r\). Hence

\[
\gcd(i!-1,j!-1)\mid r-1,
\qquad
\gcd(i!-1,j!-1)\le r-1<j^{j-i}.
\]

The final strict inequality remains true for adjacent indices because subtracting one is essential when \(r=j\). No claim that the gcd divides a power of \(j\) follows.

For \(N\ge2\) and \(1\le k\le N-1\), every term of the terminal block has index at least two. Set \(u=N-k+1\), let \(P\) and \(G\) be its product and pairwise-gcd product, and put \(B=\operatorname{den}(H_N-H_{N-k})\). The cancellation lemma yields \(P\mid BG^2\). The difference of two reduced rational numbers can be written with denominator \(Q_NQ_{N-k}\), so

\[
B\mid Q_NQ_{N-k},\qquad
P\mid Q_NQ_{N-k}G^2.
\]

There is no assumed coprimality of the prefix denominators. A stronger intermediate statement is that \(B\) divides their lcm, but the product bound is sufficient.

For each distance \(h\in\{1,\ldots,k-1\}\), the block has exactly \(k-h\) pairs at distance \(h\). Therefore

\[
\sum_{u\le i<j\le N}(j-i)
=\sum_{h=1}^{k-1}h(k-h)
=\frac{k^3-k}{6}=\binom{k+1}{3}.
\]

Taking logarithms of the positive numerical inequalities gives exactly

\[
\log Q_N+\log Q_{N-k}
\ge\sum_{n=u}^N\log(n!-1)
-\frac{k^3-k}{3}\log N.\tag{A}
\]

Empty pair products for \(k=1\) are one, and the loss term is zero. The case \(N-k=1\) is covered by the convention \(Q_1=1\).

A finite negative control distinguishes the numerical conclusion from the tempting divisibility substitution: for \((N,k)=(8,5)\), the remainder of
\(Q_NQ_{N-k}N^{2\binom{k+1}{3}}\) modulo \(P\) is 17383209419401, which is nonzero. The ordinary inequality still holds. A second control shows why the endpoint product cannot simply be replaced by \(Q_N\): 139 divides \(137!-1\) but does not divide \(Q_{137}\).

**Audit finding:** the factorial estimate and every divisibility-to-inequality transfer are valid. The candidate already warns correctly against the false numerical-to-divisibility substitution.

## 3. An independent explicit bound and the limiting constant

The asymptotic argument can be checked without importing Stirling's formula. For \(n\ge2\), monotonicity of the logarithm gives

\[
\log(n!)\ge\int_1^n\log x\,dx=n\log n-n+1,
\qquad n!-1\ge n!/2.
\]

Let \(f(x)=x\log x-x\). Since \(f'(x)=\log x\), for \(u\le n\le N\),
\(f(n)\ge f(N)-(N-n)\log N\). Summing and applying (A) gives the following explicit lower bound, valid for every admissible \((N,k)\):

\[
\boxed{
\log Q_N+\log Q_{N-k}
\ge k(N\log N-N+1-\log2)
-\left(\frac{k(k-1)}2+\frac{k^3-k}3\right)\log N.
}\tag{B}
\]

This is a supporting derivation, not a required correction or an additional target claim. It shows directly that when \(k=\lfloor\alpha\sqrt N\rfloor\), with fixed \(\alpha>0\), the lower bound divided by \(F(N)=N^{3/2}\log N\) tends to
\(\alpha-\alpha^3/3\). The linear factorial error has size \(O(N^{3/2})\); the quadratic loss has size \(O(N\log N)\); floor errors have size \(O(N\log N)\). All are negligible relative to \(F(N)\).

The derivative of \(\alpha-\alpha^3/3\) is \(1-\alpha^2\), so its maximum on \(\alpha>0\) is \(2/3\), attained at one. This is only the optimum of this estimate, not a best-possible growth theorem.

With \(k=\lfloor\sqrt N\rfloor\), both \(N\) and \(N-k\) tend to infinity and \(F(N-k)/F(N)\to1\). More explicitly, if the normalized logarithm at every sufficiently large index were below any fixed \(c<1/3\), then both endpoints would satisfy
\(\log Q_N+\log Q_{N-k}<c(F(N)+F(N-k))\le2cF(N)\), contradicting (B). This proves the claimed limsup lower bound. There is no covert assumption that \(Q_N\) is monotone or divides \(Q_{N+1}\).

## 4. Uniformity and lower-density count

For \(I_m=[m^4,(m+1)^4-1]\cap\mathbb Z\), put \(k_m=m^2\). Uniformly for \(N\in I_m\),

\[
\left(\frac m{m+1}\right)^2
<\frac{k_m}{\sqrt N}\le1.
\]

Thus \(k_m/\sqrt N\to1\) uniformly. Formula (B) proves the same uniform \(2/3+o(1)\) lower bound for the endpoint sum normalized by \(F(N)\). The omitted terms are uniformly negligible; in particular \(1/\log N\to0\) uniformly on these intervals. The admissibility condition \(1\le k_m\le N-1\) holds for all sufficiently large \(m\).

Fix \(0<c<1/3\). Eventually the lower bound is strictly larger than \(2cF(N)\). Since \(F\) is increasing on integers at least two, two endpoints \(N,N-k_m\) lying in the same \(I_m\) cannot both lie outside \(A_c\). All such pairs are covered by the uniform estimate.

Partition the interval into its \(k_m\) residue-class chains, separated by \(k_m\). If a chain has \(s\) vertices and no adjacent pair is simultaneously bad, at least \(\lfloor s/2\rfloor\) vertices are good. The floor is necessary: the pattern bad-good-bad is admissible. Summing gives

\[
|A_c\cap I_m|\ge\frac{|I_m|-k_m}{2}.
\]

Here \(|I_m|=4m^3+6m^2+4m+1\). For a cutoff \(X\in I_M\), completed intervals cover all integers from a fixed starting interval to \(M^4-1\). Their chain losses satisfy
\(\sum_{m<M}k_m=\sum_{m<M}m^2=O(M^3)\).
Discarding the current partial interval costs at most \(|I_M|=O(M^3)\). Since \(X\ge M^4\), both losses are \(o(X)\). Finitely many initial exceptions contribute only a constant. Consequently

\[
|A_c\cap[1,X]|\ge\frac X2-O(X^{3/4}),
\]

where the eventual starting point and constant may depend on \(c\). This establishes lower asymptotic density at least one half. The displayed rate is merely the same counting proof with its losses retained, not a necessary strengthening of the accepted statement.

**Audit finding:** the count works for every sufficiently large cutoff, not only fourth powers. It therefore proves lower density rather than just positive upper density. Neither density exactly one half nor density one is established, and no claim at the boundary \(c=1/3\) is justified by this argument.

## 5. Tail, rationality hypothesis, and prohibited inferences

The series converges because \(0<1/(n!-1)\le2/n!\) for \(n\ge2\). Its tail has infinitely many positive terms, so

\[
S-H_N>\frac1{(N+1)!-1}.
\]

For \(N\in A_c\), this implies

\[
\log\bigl(Q_N(S-H_N)\bigr)
>cN^{3/2}\log N-\log((N+1)!-1)
>cN^{3/2}\log N-(N+1)\log(N+1)\to+\infty.
\]

This needs no rationality hypothesis. Only the subsequent interpretation assumes hypothetically that \(S=a/q\), with \(q\ge1\). If \(H_N=P_N/Q_N\) in lowest terms, then
\(qQ_N(S-H_N)=aQ_N-qP_N\)
is a positive integer. On each \(A_c\), it tends to infinity for any fixed \(q\), so the standard contradiction \(0<qQ_N(S-H_N)<1\) is unavailable there eventually.

This does not exclude a successful subsequence outside \(A_c\), different rational approximants, more complicated linear forms, or another irrationality argument. It gives no positive evidence of rationality. Even monotone rational approximants can have extremely large reduced denominators and a rational limit: \(1-2^{-n^2}\uparrow1\). Hence the candidate's unresolved-target disclaimer is mathematically essential and correct.

## 6. Source hypotheses and attribution boundary

Two primary documents were inspected as context. Erdős's 1988 article identifies the historical question; Cook's dated manuscript supplies the acknowledged factorial-gap/terminal-block strategy and discusses the distinction between lcm and reduced denominators. Neither source is needed as an unproved theorem input: every fact used in sections 1-5 above has been independently proved.

- Paul Erdős, *On the irrationality of certain series: problems and results*, in A. Baker (ed.), *New Advances in Transcendence Theory* (1988), pp. 102-109. The exact series beginning at \(n=2\) was visually checked on PDF page 1, corresponding to the article's first page. Public primary PDF: https://renyi.hu/~p_erdos/1988-22.pdf . A fresh web opening succeeded. Authenticated inspected PDF: 553229 bytes; SHA-256 `b2bfc375d04b65332d6b8817633ff3968283a3f33c1f1ace366b03ac9fab8c88`.
- Will Cook, *Factorial Linear Forms and Denominators: Detailed Proofs and Rationality Criteria*. The inspected 51-page PDF dates itself September 1, revised October 7, 2026. Public PDF: https://wcook04.github.io/plectis/papers/erdos68-factorial-reasoning-surface.pdf . Authenticated copy: 323997 bytes; SHA-256 `415cb5beab327bc915f604ea62220ac9edb96708e43ee3ca2037f3445fa706e4`.

The Cook title/date and §3 formulas were visually inspected on PDF pages 1 and 16; §§2-3 and references were read in the authenticated full-file text. The relevant gcd hypothesis is exactly \(2\le i<j\). The lcm segment argument requires a terminal block inside indices at least two. The candidate separately proves its reduced-denominator cancellation lemma and includes the one-term block. It does not import Cook's computational exclusions, claimed formalizations, polynomial-shift extensions, or any prime-distribution theorem.

Cook §3 explicitly acknowledges earlier subtraction relations. Accordingly, attribution to Cook describes the inspected immediate source of the strategy, not priority for the gcd identity. No priority claim for the general cancellation lemma or the resulting theorem is certified. The source's disclosed AI assistance and incomplete independent checking were verified on its first page. Its claims beyond the limited comparison are not accepted by this audit merely because they appear in the manuscript.

A fresh opening of Cook's PDF failed; a fresh opening of the associated HTML page returned a cache miss. The candidate records an October 5 HTML search-result revision; this audit did not independently recover that search result and does not treat it as the October 7 PDF. Fresh text extraction from both inspected PDFs reproduced the candidate text hashes exactly; source images remain outside this deliverable. The current Erdős-problem catalogue fetch returned HTTP 403. Thus “target unresolved” here describes the result of this attempt, not a newly certified comprehensive present-day literature status. No copied source document or extracted source passage is included in the audit deliverable.

## 7. Historically recorded independent finite verification and what it establishes

The audit checker was authored separately and imports no candidate code. This section reports checks recorded during the review; the executable checker and detailed outputs are omitted from this prose edition. General reciprocal sums are reduced by an lcm-plus-integer-numerator implementation; prefix sums use a hand-coded gcd recurrence; selected cases are checked again with `Fraction`. The exact run covers symmetric reciprocal multisets, arbitrary composite tuples, valuation patterns, factorial-gap pairs, terminal blocks, chain patterns, quartic interval counts, and the source's two modular cancellation examples. Exact coverage: 74,612 reciprocal multisets with entries 1-16 and lengths 1-6; 157,676 unique-maximum valuation equalities; 75,570 sorted valuation patterns with entries 0-10 and lengths 2-8; 1,200 seeded composite tuples; 60,726 factorial-gap pairs through index 350; 2,516 terminal blocks with prefixes computed through 420; 17,709 admissible binary-chain patterns of lengths 0-18; and 250 quartic-interval counts. These counts include no claim that finite sampling verifies an infinite limit.

Seven negative controls reject: omitting the square on \(G\); universal maximal-power survival; replacing a denominator by a corrupted value; promoting a numerical bound to divisibility; assuming each new factorial denominator survives in the prefix; replacing the chain floor by a ceiling; and inferring irrationality from denominator growth alone. None tests an asymptotic statement by finite sampling.

Normal, `-O`, and `-OO` exact-check runs all passed and produced byte-identical outputs. The fail-closed inventory verifier is also independently authored. Its 60 tests use synthetic fixtures only: one accepted baseline and nineteen rejected mutations in each of the three modes. It rejects stale pins, altered sizes, extra/missing content, symbolic links, unsafe paths, duplicate JSON keys or members, malformed member metadata, self-reference, and wrong schemas. Explicit exceptions rather than `assert` preserve behavior under Python normal, `-O`, and `-OO` execution.

## 8. Required corrections and final acceptance conditions

**Required mathematical corrections: none.** The independent derivations support all three statements as written, including their quantifiers and restrictions.

The review required any later prose-only edition omitting executable checks to replace wording that a Python program “accompanies” the edition with an accurate historical verification description. PROOF.md implements that editorial condition. It does not change any mathematical assertion or proof.

Keep the reduced-denominator notation, the square on the gcd product, the distinction between numerical inequality and divisibility, the restriction \(0<c<1/3\), the lower-density qualifier, source attribution, and the explicit irrationality/novelty limitations. No broader conclusion is approved by this audit.
