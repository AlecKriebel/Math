# Equal-length disjoint interval LCMs: general reductions and a reported finite-gap verification

## Publication edition: finite numerical certificates omitted

This prose-and-verification-metadata edition preserves the complete general
divisor, ratio, monotonicity, root-bound and cross-difference proofs. It also
reports the accepted computational claim: for all integers n>=1, 1<=k<=20 and
k<=d<=256, the two complete LCMs M(n,k) and M(n+d,k) differ. The starting point
is unrestricted and the inclusive separation boundary is retained.

Raw certificates, individual brackets, numerical witness packages, executable
code and dataset contents are omitted. The finite verification cannot be
independently reproduced from this edition alone. This is not a complete
self-contained proof of the finite claim or a full computational reproduction
package. Published hashes, byte counts, aggregate counts and match results
identify separately audited evidence; hashes alone do not prove the omitted
arithmetic. The general proofs are written out in full and do not depend on
finite regression tests. Their application to the stated finite range relies
on the reported exhaustive numerical verification.

## Verdict and exact scope

Write

\[
 M(n,k)=\operatorname{lcm}(n+1,\ldots,n+k),\qquad n,k\ge1.
\]

The target asks whether \(M(n,k)\ne M(m,k)\) whenever \(m\ge n+k\).
This report does **not** establish the assertion for arbitrary lengths and gaps.
It gives a self-contained finite-gap reduction, an exact cross-difference
criterion, and a computer-verified consequence:

> For every positive integer \(n\), every \(1\le k\le20\), and every
> \(k\le d\le256\), one has \(M(n,k)\ne M(n+d,k)\).

The starting point \(n\) is unrestricted. The boundary \(d=k\) is included.
The statement concerns complete LCMs, including every prime-power exponent.
It is not a claim about prime supports, unequal lengths, or ordering of LCMs.
The arbitrary-\(k\), arbitrary-\(d\) problem is unresolved by this attempt.
No priority is claimed for the reduction, the computation, or any previously
reported small-length or adjacent-block case.

## 1. A small divisor contains all variation in the product/LCM quotient

For \(k\ge1\), define

\[
 F_k(x)=\prod_{i=1}^k(x+i),\quad
 L_k=\operatorname{lcm}(1,\ldots,k),\quad
 T_k=\frac{k!}{L_k},\quad C_k=\frac{L_k}{k}.
\]

Both \(T_k\) and \(C_k\) are positive integers.

**Lemma 1.** For every positive integer \(n\), there is an integer
\(h_k(n)\mid C_k\) such that

\[
 \frac{F_k(n)}{M(n,k)}=T_k h_k(n).
 \tag{1}
\]

**Proof.** Fix a prime \(p\). Let \(e\) be the largest nonnegative integer with
\(p^e\le k\), with \(e=0\) when \(p>k\). Let \(N_a\) count the multiples of
\(p^a\) in \(n+1,\ldots,n+k\). Counting valuations by layers gives

\[
 v_p\!\left(\frac{F_k(n)}{M(n,k)}\right)
 =\sum_{a\ge1}\bigl(N_a-\mathbf 1_{N_a>0}\bigr).
\]

When \(p^a>k\), at most one such multiple occurs, so its summand is zero.
When \(a\le e\), every block contains a multiple and

\[
 N_a=\left\lfloor\frac{k}{p^a}\right\rfloor+\varepsilon_a,
 \qquad \varepsilon_a\in\{0,1\}.
\]

Moreover, \(\varepsilon_a=0\) if \(p^a\mid k\). Thus

\[
 v_p\!\left(\frac{F_k(n)}{M(n,k)}\right)
 =v_p(k!)-e+\sum_{a=1}^e\varepsilon_a,
 \qquad
 0\le\sum_{a=1}^e\varepsilon_a\le e-v_p(k).
\]

The first fixed term is \(v_p(T_k)\); the last upper bound is
\(v_p(C_k)\). The case \(p>k\) gives zero throughout. This proves (1)
prime by prime. \(\square\)

The valuation identity is the standard product/LCM bookkeeping used in the
literature on the periodic functions of Farhi and Kane. Their index counts one
fewer than the number of terms. The proof above is supplied in full so no
period theorem or unverified small-case solution is needed.

## 2. Exact reduction to finitely many strictly decreasing ratios

Define the finite set

\[
 \mathcal R_k=\{(a,b)\in\mathbb Z_{>0}^2:
       a>b,\ \gcd(a,b)=1,\ ab\mid C_k\}.
\]

**Theorem 2.** If \(d\ge1\) and \(M(n,k)=M(n+d,k)\), then some
\((a,b)\in\mathcal R_k\) satisfies

\[
 bF_k(n+d)-aF_k(n)=0.
 \tag{2}
\]

For each fixed \(k,d,a,b\), equation (2) has at most one positive integer
solution. Every solution obeys

\[
 n+1<\frac{kda}{a-b}
 \le kd\bigl(1+\lfloor\sqrt{C_k}\rfloor\bigr).
 \tag{3}
\]

**Proof.** Equality of the LCMs and (1) give

\[
 \frac{F_k(n+d)}{F_k(n)}=\frac{h_k(n+d)}{h_k(n)}=\frac ab>1
\]

in lowest terms. Since both \(h\)'s divide \(C_k\), the reduced numerator
and denominator are coprime divisors whose product divides \(C_k\): for each
prime, cancellation leaves an exponent of magnitude at most its exponent in
\(C_k\), on only one side. This proves (2).

For real \(x\ge1\),

\[
 R_{k,d}(x)=\frac{F_k(x+d)}{F_k(x)}
          =\prod_{i=1}^k\left(1+\frac d{x+i}\right)
\]

is strictly decreasing and tends to 1. This proves uniqueness. Only this
auxiliary product ratio is being used as a monotone function; no monotonicity
of \(M(n,k)\) is assumed or inferred.

If \(x+1\ge kda/(a-b)\), put \(u=d/(x+1)>0\). Then \(ku<1\) and

\[
 R_{k,d}(x)\le(1+u)^k
 <\sum_{j=0}^{\infty}(ku)^j
 =\frac1{1-ku}\le\frac ab.
\]

The strict inequality follows by comparing the finite binomial expansion
with the geometric series, whose further terms are positive. Thus equality
requires the first bound in (3). Finally, \(b<a\) and \(ab\le C_k\) imply
\(b<\sqrt{C_k}\); hence

\[
 \frac a{a-b}=1+\frac b{a-b}
 \le1+b\le1+\lfloor\sqrt{C_k}\rfloor.
\]

This proves the remaining bound. \(\square\)

If \(C_k=\prod p^{e_p}\), the exact number of candidate ratios is

\[
 |\mathcal R_k|=\frac{\prod_{p\mid C_k}(2e_p+1)-1}{2}.
 \tag{4}
\]

Indeed, each prime is assigned exponent \(-e_p,\ldots,e_p\); inversion
pairs every nonidentity ratio with its reciprocal. For \(k=1,2\), the set is
empty. These familiar elementary cases are not presented as new results.

### Certificate format and completeness

For each \((k,d,a,b)\), a certificate records an integer \(t\ge0\).
Let \(H(x)=bF_k(x+d)-aF_k(x)\).

* If \(t=0\), the verifier requires \(H(1)<0\).
* If \(t\ge1\), it requires \(H(t)\ge0\) and \(H(t+1)<0\).
* In the latter case, the only possible integer root is \(t\). If
  \(H(t)=0\), the actual two LCMs must additionally be compared.

These conditions are exhaustive because the sign of \(H(x)\) is the sign of
\(R_{k,d}(x)-a/b\), and \(F_k(x)>0\). The polynomial \(H\) itself is not
asserted to be monotone. An exact binary search finds \(t\), with the upper
endpoint \(\lceil kda/(a-b)\rceil\) justified by (3).

The implication to (2) is only a necessary condition. A product-equation root
cannot be accepted as an LCM counterexample without checking the actual
LCMs. In the stated run there were no positive integer roots at all.

## 3. Reported finite-gap verification

The complete domain was \(1\le k\le20\), \(k\le d\le256\), and
\(n\ge1\) without an upper cutoff. It contains 4,930 length-gap slices.
After enumerating every ratio in (4), the run produced and verified
3,072,678 exact integer brackets. There were zero positive integer roots of
(2), and therefore zero equal-LCM pairs in this domain.

The generator enumerated signed prime exponents and evaluated binomial
coefficients, using \(F_k(n)=k!\binom{n+k}{k}\). A separately authored
verifier enumerated coprime divisor pairs and evaluated the rising products
directly. It checked every bracket, every domain size, every certificate
length, and the compressed and uncompressed hashes. Both computations used
exact integers; no floating-point decisions were used.

The verifier passed in normal, optimized, and double-optimized Python
modes. Additional controls checked the divisor bound directly for 40,000
length/starting-point pairs and the cross-difference criterion below for
16,400 disjoint triples. Six altered-certificate controls were rejected,
including an arithmetically false bracket whose hashes were recomputed.

Historical scope controls included an actual overlapping equality, which is
outside the target; a disjoint same-prime-support pair with unequal full LCMs;
and a disjoint example with decreasing LCM. The numerical examples are omitted
from this edition. None of these different notions was substituted for the
target.

The separately audited evidence establishes a finite computational corollary
of Theorem 2, not a general resolution. This edition reports the verification
outcome without distributing the certificates needed to reproduce it. Increasing the bounds gives further finite checks, not a proof
for all lengths or all gaps.

## 4. A second exact obstruction from cross-differences

**Proposition 3.** Suppose \(d\ge k\). Define positive integers

\[
 D_i=\operatorname{lcm}(d+1-i,\ldots,d+k-i),\quad 1\le i\le k,
\]
\[
 E_j=\operatorname{lcm}(d+j-k,\ldots,d+j-1),\quad 1\le j\le k.
\]

Then \(M(n,k)=M(n+d,k)\) if and only if

\[
 n+i\mid D_i\quad(1\le i\le k),\qquad
 n+d+j\mid E_j\quad(1\le j\le k).
 \tag{5}
\]

**Proof.** Fix \(i\). A prime power \(p^a\mid n+i\) divides some
\(n+d+j\) if and only if it divides the difference \(d+j-i\). Consequently
\(n+i\mid M(n+d,k)\) if and only if \(n+i\mid D_i\). Applying the same
argument with a fixed later term proves the second family of conditions.
The two families say that the two LCMs divide one another, proving (5).
All differences are positive, including when \(d=k\). \(\square\)

In particular, any common LCM would divide
\(\operatorname{lcm}(d-k+1,\ldots,d+k-1)\). This is another complete
prime-power obstruction, although its elementary size bound is usually much
weaker than (3). Proposition 3 is not sufficient by itself to exclude every
possible \(k,d,n\).

## Sources and limits

* P. Erdős, *Some Unconventional Problems in Number Theory*, Acta Math.
  Acad. Sci. Hungar. 33 (1979), printed p. 78, states the equal-length
  question with the inclusive separation boundary:
  <https://users.renyi.hu/~p_erdos/1979-23.pdf>.
* B. Farhi and D. Kane, *New results on the least common multiple of
  consecutive integers*, Proc. Amer. Math. Soc. 137 (2009), 1933–1939.
  The author's manuscript, especially its valuation identity (12), supplies
  relevant background: <https://cseweb.ucsd.edu/~dakane/lcm.pdf>.
  The exact-period theorem is not needed for the proof here.

Reported solutions of selected small lengths and the adjacent case are not
being independently established as prior results in this report, nor is
their rediscovery claimed. The different length-\(k\) versus length-\(k+1\)
question plays no role. Integrity checks establish agreement with the stated
certificate procedure; they do not establish priority or resolve the
unrestricted problem.

## Edition and review statement

This AI-assisted work is unrefereed. Acceptance refers to an independent
internal AI audit of the original report and its separate numerical evidence.
No external human peer review, journal acceptance or formal proof-assistant
certification is claimed. No mathematical correction was required. No novelty,
priority or full solution is claimed. The arbitrary-length, arbitrary-gap
problem remains unresolved by this work.

This edition preserves the general proofs, exact finite claim and substantive
scope qualifications. Historical verification and scholarly-source inspection
are reported as such. Edition preparation checks byte integrity, exact
editorial changes and publication structure only; it performs no new
mathematical computation or scholarly-source retrieval/inspection. The
original sealed candidate and audit packages are unchanged. Copied source
documents, source text, page images, dataset contents, raw certificates,
executable code and private coordination material are not distributed.
