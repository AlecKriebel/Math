# Independent audit of the finite-gap interval LCM result

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

## Decision and scope

**Accepted as a finite-gap, all-starting-points theorem.** For
\(M(n,k)=\operatorname{lcm}(n+1,\ldots,n+k)\), the audited certificate proves

\[
M(n,k)\ne M(n+d,k)
\quad\text{for all integers }n\ge1,\quad 1\le k\le20,\quad k\le d\le256.
\]

The separation boundary \(d=k\) is included. The starting point has no upper
cutoff. All prime-power exponents in the two LCMs are covered. This audit
accepts neither a resolution for arbitrary lengths and gaps nor a novelty,
priority, or improvement-over-prior-work claim. No mathematical correction to
the submitted finite-gap argument is required.

The audited report is identified by SHA-256
`4bae1f261f110eae96235fe1e811ae1d23940bfac0899c8db310e0878432f2ac`
(9,312 bytes). Its sealed input manifest is identified by SHA-256
`01f436cfeef59db867911d8db2a1d38f9e105e3344980a6dca3c4d79977f57de`
(9,045 bytes). All 35 listed members were independently hashed and sized;
the actual file membership matched exactly. The input was checked again
after each exhaustive run and remained unchanged.

## Mathematical audit

### Product divided by full LCM

Put
\[
F_k(x)=\prod_{i=1}^k(x+i),\quad L_k=\operatorname{lcm}(1,\ldots,k),
\quad T_k=k!/L_k,\quad C_k=L_k/k.
\]
Both displayed quotients are positive integers: every integer from 1 through
\(k\) divides \(k!\), and \(k\) divides \(L_k\).

Fix a prime \(p\), let \(e=\max\{r\ge0:p^r\le k\}\), and let \(N_r\)
count the multiples of \(p^r\) in the length-\(k\) block. The valuation of the
product is \(\sum_{r\ge1}N_r\), whereas the valuation of its LCM is
\(\sum_{r\ge1}\mathbf1_{N_r>0}\). For \(r>e\) the interval contains at
most one multiple, so those terms cancel. For \(1\le r\le e\), there is
at least one multiple and
\[
N_r=\lfloor k/p^r\rfloor+\epsilon_r,\qquad \epsilon_r\in\{0,1\}.
\]
When \(p^r\mid k\), the count is exactly \(k/p^r\), hence
\(\epsilon_r=0\). Therefore
\[
v_p(F_k(n)/M(n,k))
=v_p(k!)-e+\sum_{r=1}^e\epsilon_r,
\qquad 0\le\sum\epsilon_r\le e-v_p(k).
\]
The fixed part is \(v_p(T_k)\); the upper bound for the variable part is
\(v_p(C_k)\). Primes exceeding \(k\) contribute zero. Thus, without any
restriction on \(n\),
\[
F_k(n)/M(n,k)=T_kh_k(n),\qquad h_k(n)\mid C_k.
\]
The audit found no missing large-prime or higher-prime-power case.

### Complete rational candidate set

If the two LCMs are equal and \(d\ge1\), division of the preceding
identities gives
\[
F_k(n+d)/F_k(n)=h_k(n+d)/h_k(n)=a/b>1
\]
in lowest terms. Reducing a quotient of two divisors of \(C_k\) leaves,
at every prime, an exponent on at most one side, of magnitude no larger than
its exponent in \(C_k\). Hence \(a>b\), \(\gcd(a,b)=1\), and \(ab\mid C_k\).
Conversely every pair with these properties is a quotient of two divisors,
namely \(a\) and \(b\). This converse concerns the divisor superset; it
does not claim that both divisors occur as actual values of \(h_k\) at the
required starts.

For \(C_k=\prod p^{e_p}\), the signed exponent vectors of reduced divisor
quotients number \(\prod(2e_p+1)\). Only the zero vector is fixed by
inversion. Exactly half the remaining vectors give a ratio exceeding 1:
\[
\#\mathcal R_k=(\prod(2e_p+1)-1)/2.
\]
In particular \(C_1=C_2=1\), so those lengths have no candidate ratios and
are excluded directly by the reduction. No numerical records are needed for
them. Omitting them from a count of nonempty ratio cases does not omit their
length-gap slices.

### Infinite starting points and exact endpoints

For fixed positive \(k,d\),
\[
R(x)=F_k(x+d)/F_k(x)=\prod_{i=1}^k(1+d/(x+i))
\]
is positive and strictly decreasing for real \(x\ge1\), and tends to 1.
Thus \(R(x)=a/b\), where \(a/b>1\), has at most one solution on that domain.
The sign of
\(H(x)=bF_k(x+d)-aF_k(x)\) is the sign of \(R(x)-a/b\).
The polynomial \(H\) itself need not be decreasing.

For the proposed explicit bound, if
\(x+1\ge kda/(a-b)\), set \(u=d/(x+1)\). Then
\(0<ku\le(a-b)/a<1\), and
\[
R(x)\le(1+u)^k<\sum_{j\ge0}(ku)^j
=1/(1-ku)\le a/b.
\]
The middle inequality is strict because the finite binomial coefficients are
bounded by the corresponding powers of \(k\), and the geometric series has
positive terms beyond degree \(k\). This works also for \(k=1\).
Consequently a root must satisfy \(n+1<kda/(a-b)\). Since
\(b<a\) and \(ab\le C_k\), one has \(b<\sqrt{C_k}\), and
\[
a/(a-b)=1+b/(a-b)\le1+b\le1+\lfloor\sqrt{C_k}\rfloor.
\]
Both constants and the strict inequality are correct.

A recorded zero is valid precisely when \(H(1)<0\), which excludes every
positive starting point. A recorded positive integer \(t\) is valid when
\(H(t)\ge0\) and \(H(t+1)<0\). Strict decrease of \(R\) then excludes
all positive integers other than a possible root at \(t\). In the audited
run every left endpoint was strictly positive, so no such root exists.
The integer \(\lceil kda/(a-b)\rceil\) is a safe negative upper endpoint
for binary search. The audit checked its sign in every ratio case as well.
These arguments, not a finite scan of starting points, establish the
unrestricted quantifier on \(n\).

### Cross difference equivalence

For \(d\ge k\), set
\[
D_i=\operatorname{lcm}_{1\le j\le k}(d+j-i),\qquad
E_j=\operatorname{lcm}_{1\le i\le k}(d+j-i).
\]
For every prime power \(p^r\) dividing \(n+i\), there is a later term
\(n+d+j\) divisible by \(p^r\) exactly when there is a difference
\(d+j-i\) divisible by \(p^r\). Taking every prime power in \(n+i\)
proves
\[
n+i\mid M(n+d,k)\ \Longleftrightarrow\ n+i\mid D_i.
\]
Reversing the fixed term gives
\[
n+d+j\mid M(n,k)\ \Longleftrightarrow\ n+d+j\mid E_j.
\]
All the first conditions express one LCM divisibility; all the second
conditions express the reverse divisibility. Their conjunction is therefore
necessary and sufficient for equality of the full LCMs. Different primes may
be witnessed by different terms, which is valid for LCM divisibility.

The differences lie in \([d-k+1,d+k-1]\); in particular none vanishes when
\(d=k\). Every common LCM consequently divides the LCM of that interval of
differences. The criterion is correct, but no general nonexistence conclusion
follows from it alone. The finite-gap acceptance does not depend on treating
this criterion as a sufficient obstruction without checking its conditions.

## Historical independent computation

The independent audit program did not inspect, import, or execute the
candidate program source. Candidate program files were read as bytes solely
for the sealed-member integrity check. Certificate semantics were taken from
the documented data format and checked against the mathematical argument.

The independently authored implementation used:

- Trial division to enumerate every divisor of each independently calculated
  \(C_k\), followed by every reduced quotient of two such divisors. It then
  checked the coprime-product characterization and the closed cardinality
  formula. It did not use the candidate's signed-exponent generator or its
  divisor-pair filter as its enumeration algorithm.
- Exact integer coefficient construction for \(F_k\) and Horner evaluation.
  This differs from the reported binomial generator and rising-product
  verifier. Direct product comparisons also tested the polynomial evaluator.
- A fixed domain loop for all 20 lengths and all inclusive gaps, rather than
  adopting the domain from untrusted certificate metadata.
- Exact record lengths and order, file membership, single-stream zlib
  termination, and compressed and expanded SHA-256 checks.
- Exact sign checks at both consecutive-integer endpoints and at the
  theoretical upper endpoint in every case. No floating-point decision and
  no assertion statement was used.

All **4,930 length-gap slices** are included. There are **3,072,678** ratio
cases, and every one passed. There were **zero positive integer roots** of
any required product equation. Equality of the LCMs implies one of these
product equations; exclusion of all such equations proves the stated LCM
result. The converse implication was neither assumed nor needed.

The complete audit passed under ordinary Python, `-O`, and `-OO`. The three
outputs agreed after removing only timing and optimization-mode fields.
The same three modes passed the following independently authored controls:

- 40,000 direct quotient-divisor checks, plus 60 additional checks at very
  large starting points.
- 16,400 disjoint triples for the cross-difference equivalence, including
  344,400 individual divisibility equivalences; 240,633 of the individual
  conditions were true, so this was not merely an all-false comparison.
- 150 brackets regenerated independently by binary search from the proved
  upper bound, without using the recorded bracket as a search seed.
- A valid negative-at-one case and a positive overlapping root whose actual
  LCMs are equal. This tests both certificate branches and root detection.
- Same-prime-support but unequal-full-LCM and decreasing-disjoint-LCM
  controls. Neither prime support nor LCM monotonicity was substituted for
  the claim.
- Ten malformed or false certificate controls, all rejected: a false zero
  bracket with both hashes recomputed; brackets shifted below and above the
  valid location; missing and extra records; wrong header; concatenated
  streams; trailing bytes; truncated compressed bytes; and a wrong declared
  count.

These controls strengthen implementation confidence but do not replace the
proof of the general reductions or the exhaustive endpoint check. Acceptance
remains a mathematical argument supported by an exact computational audit,
not a formal proof-assistant certification.

## Historical source verification and limitations

The following retrievals and inspections occurred during the independent
audit on 2026-10-10. They were not repeated for this publication edition.

The primary 1979 source was freshly retrieved and visually inspected at
printed page 78, PDF page 8. It states the equal-length LCM problem with the
inclusive boundary \(m\ge n+k\). Its separate prime-support question was
not substituted for the LCM problem. [Erdős 1979](https://users.renyi.hu/~p_erdos/1979-23.pdf)

The 1980 note was freshly retrieved, text-inspected on both pages, and
visually inspected on its first page. It restates a strict separation
condition. This does not narrow the inclusive target verified from 1979.
[Erdős 1980](https://users.renyi.hu/~p_erdos/1980-11.pdf)

The Farhi-Kane author-hosted manuscript was freshly retrieved. Its block
index convention and its valuation identity were text-inspected; PDF pages
6 and 7 were also visually inspected. Its \(g_r(s)\) has \(r+1\) terms,
so the quotient here corresponds to \(g_{k-1}(n+1)\). The manuscript is
background for valuation bookkeeping; its exact-period theorem is not a
premise of this acceptance. [Farhi and Kane](https://cseweb.ucsd.edu/~dakane/lcm.pdf)
The publication details, Proceedings of the American Mathematical Society
137 (2009), no. 6, 1933-1939, are confirmed by the author's bibliography.
[Author bibliography](https://cseweb.ucsd.edu/~dakane/cv.html)

PDF hashes, sizes, and inspection scope are recorded in the accompanying
SOURCES.json metadata. A DOI-page open returned HTTP 403; an attempt
to open the problem-index page returned an internal error. Neither page is
used as evidence for a stronger prior theorem or a current global status.

The unrestricted problem remains unresolved by this attempt and this audit.
No audit finding warrants upgrading the work to a complete solution.
No independent recovery of stronger small-length or adjacent-block prior
results, and no novelty assessment, is claimed.

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
