# Reduced-denominator growth in the factorial-minus-one series

**Review scope.** These AI-assisted authored documents and their independent internal AI audit are unrefereed. “Accepted” means only the stated partial mathematical scope. No external human peer review, journal acceptance, formal proof-assistant certification, novelty, or current worldwide open-status certification is claimed. This prose edition omits executable checkers, detailed test outputs, source documents, extracted text, and page images. Its verification statements describe historically recorded checks; edition preparation performed no new scholarly-source retrieval or inspection.

## Status and scope

Let

\[
S=\sum_{n=2}^{\infty}\frac1{n!-1},\qquad
H_N=\sum_{n=2}^{N}\frac1{n!-1},\qquad Q_N=\operatorname{den}(H_N),
\]
where `den` means the positive denominator after reduction and \(H_1=0,Q_1=1\).
This note proves an unconditional growth theorem for the **reduced** denominators of the partial sums. It does not prove or disprove the irrationality of \(S\). In particular, large reduced denominators are not an irrationality criterion. No novelty or exhaustive literature-search claim is made.

**Theorem.**

1. \(\displaystyle \limsup_{N\to\infty}\frac{\log Q_N}{N^{3/2}\log N}\ge\frac13.\)
2. For every real \(c\) with \(0<c<1/3\), the set
   \[
   A_c=\{N\ge2:\log Q_N\ge cN^{3/2}\log N\}
   \]
   has lower asymptotic density at least \(1/2\).
3. For each such \(c\),
   \[
   Q_N(S-H_N)\longrightarrow+\infty\quad\text{as }N\to\infty\text{ through }A_c.
   \]

The proof is elementary and self-contained. Its starting factorial-gap estimate and terminal-block strategy are also present in Cook's inspected manuscript [2, Lemma 3.2 and Section 3]. That manuscript applies them to the **unreduced lcm**. Here a separate cancellation lemma applies to the reduced denominator of a block sum, and a pairing argument transfers it to many reduced prefix denominators. The manuscript is acknowledged as a source of the starting strategy; its computational and formal claims are not prerequisites.

## 1. A cancellation lemma for reciprocal sums

**Lemma 1.** For positive integers \(d_1,\ldots,d_k\), put

\[
P=\prod_{i=1}^k d_i,\qquad
G=\prod_{1\le i<j\le k}\gcd(d_i,d_j),\qquad
D=\operatorname{den}\left(\sum_{i=1}^k\frac1{d_i}\right).
\]
Then \(P\mid DG^2\), and consequently \(D\ge P/G^2\).

**Proof.** Fix a prime \(p\) and arrange \(a_i=v_p(d_i)\) so that
\(a_1\ge a_2\ge\cdots\ge a_k\ge0\). For \(k=1\) the assertion is immediate, so assume \(k\ge2\). We have

\[
v_p(P)=\sum_i a_i,\qquad v_p(G)=\sum_{j=2}^k(j-1)a_j.
\]

If \(a_1>a_2\), exactly one summand has \(p\)-adic valuation \(-a_1\). Clearing by \(p^{a_1}\) and a denominator coprime to \(p\) leaves exactly one numerator term nonzero modulo \(p\); hence \(v_p(D)=a_1\). Therefore

\[
v_p(DG^2)-v_p(P)=\sum_{j=2}^k(2j-3)a_j\ge0.
\]

If \(a_1=a_2\), then

\[
v_p(P)-2v_p(G)
=a_1-a_2-\sum_{j=3}^k(2j-3)a_j\le0\le v_p(D).
\]

These cases include \(a_1=0\) and prove divisibility at every prime. This argument does not assume that primes of the common denominator survive reduction. ∎

The square on \(G\) cannot be uniformly replaced by its first power: for \(d_1=3,d_2=6\), the sum is \(1/2\), so \(P=18,D=2,G=3\); \(P\nmid DG\), while \(P=DG^2\). This is a limitation of that proposed general lemma, not an optimality assertion for the factorial sequence.

## 2. Exact finite block inequality

Write \(d_n=n!-1\). For \(2\le i<j\), subtraction gives

\[
\gcd(d_i,d_j)\mid \frac{j!}{i!}-1,
\qquad
\gcd(d_i,d_j)\le\frac{j!}{i!}-1<j^{j-i}.
\tag{1}
\]

Indeed, multiply \(i!-1\) by \(j!/i!\) and subtract \(j!-1\); the result is \(1-j!/i!\), a nonzero integer.

Fix integers \(N\ge2\) and \(1\le k\le N-1\), set \(u=N-k+1\), and let

\[
B_{N,k}=\operatorname{den}(H_N-H_{N-k}).
\]

For this block, define \(P_{N,k}=\prod_{n=u}^N d_n\) and
\(G_{N,k}=\prod_{u\le i<j\le N}\gcd(d_i,d_j)\).
Lemma 1 gives the exact divisibility

\[
P_{N,k}\mid B_{N,k}G_{N,k}^2.
\tag{2}
\]

Also \(B_{N,k}\mid Q_NQ_{N-k}\), because writing the two rational prefix sums over the product denominator produces their difference. Consequently

\[
P_{N,k}\mid Q_NQ_{N-k}G_{N,k}^2.
\tag{3}
\]

Using (1) and

\[
\sum_{u\le i<j\le N}(j-i)
=\sum_{h=1}^{k-1}h(k-h)=\binom{k+1}{3},
\]

we obtain the finite, real-valued inequality

\[
\boxed{\quad
\log Q_N+\log Q_{N-k}
\ge \sum_{n=u}^N\log(n!-1)
-2\binom{k+1}{3}\log N.
\quad}
\tag{4}
\]

For \(k=1\), \(G=1\) and the binomial coefficient is zero, so the same statement holds. One must not replace \(G^2\) in the divisibility (3) by \(N^{2\binom{k+1}{3}}\): (1) supplies a numerical bound, not such a divisibility. The corresponding **numerical inequality** with that power of \(N\) is valid.

## 3. Asymptotic constant

Take \(k=\lfloor\alpha\sqrt N\rfloor\) for a fixed positive real \(α\). Uniformly for \(u\le n\le N\), we have \(n=N+O(\sqrt N)\) and

\[
\log(n!-1)=n\log n-n+O(\log n).
\]

This last estimate follows, for example, by bounding the sum \(\sum_{j=1}^n\log j\) between its neighboring integrals, and using
\(\log(n!-1)-\log(n!)=O(1)\). It needs no unproved asymptotic input. Thus

\[
\sum_{n=u}^N\log(n!-1)
=\alpha N^{3/2}\log N+o(N^{3/2}\log N),
\]

whereas

\[
2\binom{k+1}{3}\log N
=\frac{\alpha^3}{3}N^{3/2}\log N+o(N^{3/2}\log N).
\]

Equation (4) implies

\[
\log Q_N+\log Q_{N-k}
\ge\left(\alpha-\frac{\alpha^3}{3}+o(1)\right)N^{3/2}\log N.
\tag{5}
\]

The displayed coefficient is maximized at \(α=1\), giving \(2/3\). This optimizes this particular estimate only. Since \((N-k)^{3/2}\log(N-k)\sim N^{3/2}\log N\), at least one endpoint has normalized logarithmic denominator at least \(1/3-o(1)\). Both endpoints tend to infinity. This proves part 1 of the theorem.

## 4. The density refinement

Fix \(0<c<1/3\). Partition the sufficiently large positive integers into disjoint intervals

\[
I_m=\{m^4,m^4+1,\ldots,(m+1)^4-1\},\qquad k_m=m^2.
\]

Uniformly for \(N\in I_m\), we have \(k_m/\sqrt N\to1\) as \(m\to\infty\). The same estimates proving (5), now with \(k=k_m\), therefore give uniformly

\[
\log Q_N+\log Q_{N-k_m}
\ge(2/3+o(1))N^{3/2}\log N.
\tag{6}
\]

For all sufficiently large \(m\), two indices \(N,N-k_m\) belonging to the same \(I_m\) cannot both lie outside \(A_c\). Otherwise their logarithmic denominators would have sum strictly less than

\[
cN^{3/2}\log N+c(N-k_m)^{3/2}\log(N-k_m)
\le2cN^{3/2}\log N,
\]

contradicting (6), since \(2c<2/3\).

Partition \(I_m\) into its \(k_m\) residue-class chains with successive indices separated by \(k_m\). Along each chain two consecutive vertices cannot both be outside \(A_c\). A chain with \(s\) vertices therefore has at least \(\lfloor s/2\rfloor\) vertices in \(A_c\). With \(L_m=|I_m|\), this yields

\[
|A_c\cap I_m|\ge\frac{L_m-k_m}{2}.
\tag{7}
\]

The cumulative loss through the intervals with \(m<M\) is at most
\(\sum_{m<M}m^2=O(M^3)\), while their total length is of order \(M^4\). For a cutoff \(X\in I_M\), discarding the unfinished last interval loses only
\(L_M=O(M^3)=o(X)\). Finitely many initial intervals have no effect. Therefore

\[
\liminf_{X\to\infty}\frac{|A_c\cap[1,X]|}{X}\ge\frac12,
\]

proving part 2. This is a lower-density conclusion; neither density exactly \(1/2\), density one, nor pointwise growth of every \(Q_N\) is asserted.

## 5. Why this does not settle the irrationality question

The tail is positive and its first term gives

\[
S-H_N>\frac1{(N+1)!-1}.
\]

For \(N\in A_c\),

\[
\log\bigl(Q_N(S-H_N)\bigr)
>cN^{3/2}\log N-\log((N+1)!-1)\longrightarrow+\infty.
\]

This proves part 3. Under a hypothetical rationality relation \(S=a/q\), with \(q\ge1\),

\[
qQ_N(S-H_N)=aQ_N-q\operatorname{num}(H_N)\in\mathbb Z_{>0}.
\]

A standard denominator-clearing proof would need that positive integer to be below one. The theorem shows that prefixes in \(A_c\), a set of lower density at least one half, cannot supply this contradiction for any fixed \(q\) once sufficiently large. It does not rule out a favorable sparse subsequence outside \(A_c\), different rational approximants, linear-form cancellation, or a different proof method.

A rational limit is fully compatible with rapidly growing denominators of rational approximants: for instance \(1-1/M_N\to1\) for any integers \(M_N\to\infty\). This observation is illustrative, not a replacement denominator sequence for Erdős's problem. No inference from the present growth theorem to rationality or irrationality is valid.

## 6. Sources, comparison, and validation boundary

[1] Paul Erdős, *On the irrationality of certain series: problems and results*, in A. Baker (ed.), *New Advances in Transcendence Theory* (1988), pp. 102–109. The exact sum beginning at \(n=2\) is visible on printed p. 102. Primary PDF: https://renyi.hu/~p_erdos/1988-22.pdf . Inspected copy: 553229 bytes; SHA-256 `b2bfc375d04b65332d6b8817633ff3968283a3f33c1f1ace366b03ac9fab8c88`. The first page was visually inspected because text extraction corrupts the formula.

[2] Will Cook, *Factorial Linear Forms and Denominators: Detailed Proofs and Rationality Criteria*, dated September 1, revised October 7, 2026 in the inspected PDF, 51 pages. PDF: https://wcook04.github.io/plectis/papers/erdos68-factorial-reasoning-surface.pdf . Inspected copy: 323997 bytes; SHA-256 `415cb5beab327bc915f604ea62220ac9edb96708e43ee3ca2037f3445fa706e4`. Sections 2–4, 6, and relevant appendices were read as comparison. The inspected Section 3 gives the lcm growth estimate, while Section 2 documents actual cancellation in reduced partial sums. The author explicitly identifies the paper as AI-assisted and states that not every claim was independently verified. No computational exclusion or claimed formalization from that paper is accepted here as a dependency.

The public HTML search result displayed an October 5 revision while the authenticated PDF displays October 7. These versions are not silently conflated. A fresh web opening of the PDF failed; the full locally available, hash-authenticated PDF supplied the inspected source. The bounded searches did not establish novelty or an exhaustive current literature status. Erdős's source establishes the historical question; this note's unresolved status means this attempt has not resolved it.

All mathematical assertions above have complete proofs in this note. Historically recorded Python checks tested the finite identities and the combinatorial pairing with exact integers and rational arithmetic; the independent internal AI audit records a separately authored exact-check suite. Executable programs and detailed test outputs are omitted from this prose edition, which is not an executable reproduction package. Those finite checks support implementation correctness only; they do not prove the asymptotic or density statements. No Lean or other proof-assistant verification is claimed.
