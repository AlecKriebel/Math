# Independent review: Saito's Möbius–totient eta product

**Verdict: PASS — exact known affirmative resolution.** The recommendation
**already_solved**, with **zero fresh proof attempts**, is justified for
30000166 and its duplicate 30000167. Berkovich and Garvan prove the displayed
product has nonnegative Fourier coefficients for every positive integer.
No unresolved composite case survives, and this package makes no new-discovery
claim. No mathematical correction to the frozen artifact is required.

Reviewed artifact: SOURCE_STATUS.md, SHA-256
**46b114d041624894c9e248e262703e58751c68f68969b3e4ba1a5ca11f23ac62**.
Review date: 2026-09-30. This is a separate adversarial AI review using
gpt-6-astra at xhigh reasoning effort, not human peer review.

## 1. Exact source and publication identification

Ibukiyama's contribution to [Oberwolfach Report 1/2005](https://doi.org/10.4171/owr/2005/01),
printed pp. 54–55, explicitly asks for nonnegative Fourier coefficients of

\[
S_h(\tau)=\eta(h\tau)^{\varphi(h)}
          \prod_{d\mid h}\eta(d\tau)^{-\mu(d)}.
\]

The quantifier is every natural number \(h\), with the unhandled case in that
2005 report being integers divisible by at least two different primes. The
nearby discussion of regular systems of weights is distinct. The pinned
30000166 statement reproduces the formula; the pinned 30000167 statement and
its source verification identify the repeated composite case of the same
source question. Neither record requires strict positivity.

Berkovich–Garvan's [2006 paper](https://arxiv.org/abs/math/0607606v1),
Conjecture 1.1 and Section 3, and their
[expanded 2007 paper](https://arxiv.org/abs/math/0702027v1), Conjecture 1.1
and Section 3, have exactly this numerator, denominator, and all-positive-integer
quantifier. The word “Conjecture” labels the historical statement being proved;
it is not evidence that the paper leaves it open. The expanded paper supplies
the necessary theta identity as Theorem 1.2 and proves it in Section 2.

The published article is *Journal of Number Theory* **128** (2008), no. 6,
1731–1748, [DOI 10.1016/j.jnt.2007.02.002](https://doi.org/10.1016/j.jnt.2007.02.002).
The [publisher's indexed article record](https://www.sciencedirect.com/science/article/pii/S0022314X07000820)
and [Garvan's publication list](https://qseries.org/fgarvan/publist.html)
agree on the title, authors, and bibliographic details. The author list links
a full manuscript with the same proof. Yasuda's published
[2010 paper](https://ems.press/content/serial-article-files/41111), p. 563
and reference [1], also explicitly credits their theorem and distinguishes
its eta-product family from regular-weight-system products.

I checked the full portions of the accessible 2007 primary proof needed here,
including the proof of Theorem 1.2 and all of Section 3. I did not obtain the
typeset journal PDF: the direct publisher article fetch returned HTTP 403.
Thus the publication identification is independently corroborated, while
the line-by-line mathematical audit uses the full primary manuscript, as the
artifact accurately states. Both arXiv records currently list a single
version and no withdrawal. A bounded current search revealed no relevant
correction; this is not a claim of exhaustive bibliographic searching.

## 2. Normalization and endpoint cases

Substituting \(\eta(d\tau)=q^{d/24}E(q^d)\) gives exactly

\[
S_N=q^{A_N}\widetilde S_N,\qquad
24A_N=N\varphi(N)-\sum_{d\mid N}d\mu(d).
\]

The normalized series has integer powers; the eta product can have a
fractional leading exponent. Multiplication by \(q^{A_N}\) only shifts the
exponents, so it does not change coefficient signs. In particular,
\(A_1=0,\ A_2=1/8,\ A_3=1/3,\ A_4=3/8\). For \(N=1\), the original product
is \(1\), not an exceptional limiting formula.

Direct visual inspection confirms the original report prints
\((p^2-1)/12\) in its prime-case display on p. 54, despite defining
\(\eta=q^{1/24}E(q)\) above it. The correct shift is
\((p^2-1)/24\), as in Berkovich–Garvan (1.6). The artifact correctly identifies
this local discrepancy without altering the original conjecture.

The identity \(E(q^t)^t/E(q)=\sum a_t(n)q^n\) is valid for every positive
integer \(t\), including composite \(t\) and \(t=1\). Its coefficients count
\(t\)-core partitions. Strict positivity would be false in general:
the 2-core series has zero coefficient at degree 2.

## 3. Theta identity and specialization audit

Theorem 1.2 has \(a\ge2\). Its summation lattice is
\(\sum_i n_i=0\), its quadratic expression is
\(Q_a(n)=a\sum n_i^2/2+\sum i n_i\), and its monomial exponent is
\(a n_j+j\). These indices, signs, and factors agree with the artifact.

The functional-equation proof has the required analytic hypotheses.
The lattice sums converge normally on compact subsets of
\(\mathbb C^\times\) for fixed \(0<|q|<1\). The apparent poles of the
bracket quotient at \(z=q^k\) are removable because the numerator vanishes
there too. The cyclic affine lattice maps used in the manuscript are
bijections of the zero-sum lattice and give the stated functional equation
\(F(qz)=z^{-(a-1)}F(z)\) for both sides.

Here is an independent check of the uniqueness step. A nonzero holomorphic
function on \(\mathbb C^\times\) satisfying
\(F(qz)=z^{-d}F(z)\) has exactly \(d\) zeros, with multiplicity, in an annulus
\(|q|R<|z|<R\) whose boundary is zero-free. This follows from the argument
principle: its logarithmic-derivative integral on the inner boundary equals
the outer integral minus \(d\). Choose \(1<R<|q|^{-1}\) with zero-free
boundaries. The difference of the two candidate functions vanishes at all
\(a\) distinct \(a\)-th roots of unity, whereas \(d=a-1\). Therefore the
difference must be zero. At nontrivial roots the inner geometric sum
vanishes; at \(1\) the equality is the credited Klyachko/core theta identity.
This validates the standard uniqueness argument without importing an
unexamined zero-count assumption. The core generating function and core
theta identity remain explicitly credited existing identities.

The potentially delicate substitution \(z=q^r\), with the theorem's base
replaced by \(q^M\), is also valid formally. On the zero-sum lattice,

\[
Q_a(n)=\sum_i\left(\frac a2n_i(n_i-1)+i n_i\right).
\]

Each displayed summand is a nonnegative integer. For a negative coordinate
\(-k\), it is \(k(a(k+1)/2-i)>0\). For nonnegative coordinates the assertion
is immediate. The affine bijection \(T_j\) in the artifact obeys

\[
Q_a(T_jn)-Q_a(n)=a n_j+j.
\]

Consequently, whenever \(0<r<M\),

\[
M Q_a(n)+r(a n_j+j)
 =(M-r)Q_a(n)+rQ_a(T_jn)\ge0.
\]

The positive quadratic part makes every exponent sublevel finite. Thus no
negative powers or infinite coefficient sums appear after specialization.
This also covers \(r=M/2\) when it is integral; the two bracket progressions
then have multiplicity two. The factorization below itself uses odd \(M\)
and avoids that endpoint. Multiplying the specialized theta series by the
positive core series gives precisely the claimed positivity of \(D_a\).

## 4. All three factorization cases

The elementary identity

\[
\prod_{d\mid M}E(q^d)^{\mu(d)}
 =\prod_{\gcd(k,M)=1}(1-q^k)
\]

holds for arbitrary \(M\), not just squarefree \(M\), by the divisor sum
for the Möbius function.

For \(N=pM\), with \(p\nmid M\) and odd \(M>1\), the reduced residue classes
split into distinct pairs \(r,M-r\). There are \(\varphi(M)/2\) pairs.
The numerator exponent in the product of \(D_p(q^r;q^M)\) is therefore
\((2p-2)\varphi(M)/2=\varphi(pM)\). Its bracket ratio is the quotient of
the Möbius products with bases \(q^p\) and \(q\). This proves exactly the
artifact's boxed factorization. Divisors with \(\mu(d)=0\) cause no problem:
\(\mu(pd)=-\mu(d)\) remains true when \(p\nmid M\).

For \(N=p^\alpha M\), let \(N'=pM\) and \(t=p^{\alpha-1}\).
The nonzero Möbius divisor terms for \(N\) and \(N'\) are identical, and
\(\varphi(N)=t\varphi(N')\). Cancelling the common denominator gives exactly
the boxed lifting identity. Its extra factor is a core series at base
\(q^{N'}\), raised to the nonnegative integer \(\varphi(N')\).
It works for \(\alpha=1\) as well, with \(t=1\).

When \(M=1\), the residue-pair formula is not used: the base case is
\(\widetilde S_p=E(q^p)^p/E(q)\), followed by the same lift. This handles
all prime powers. Finally, choose \(p=2\) for even \(N\), or any prime
divisor for odd \(N\), and remove its full power. The remaining \(M\) is
odd and coprime to \(p\). Together with \(N=1\), this exhausts every
positive integer. There is no hidden restriction on the other prime
powers dividing \(M\), or on the number of distinct primes.

## 5. Reproducible independent checks

The author's standard-library verifier reproduced **2,837 assertions**
and the saved JSON output **byte-for-byte**. All three source PDF hashes
match the package's provenance manifest.

Run the separate checker from this review directory:

    python3 independent_checks.py

It performs **35,980 exact assertions**, using an independently implemented
logarithmic-derivative recurrence for product coefficients and direct
hook-length enumeration:

- 7,338 partitions through degree 24; core counts for \(t=1,\ldots,8\),
  and the core lattice identity for \(t=2,\ldots,8\)
- 250 parameter values for normalization, Möbius exponents, and the full
  factorization split, including 64 higher-power mixed cases and several
  integers with three or four distinct primes
- normalized coefficient checks through degree 80 for \(N\le80\)
- 540 lattice vectors testing every affine index and specializations near
  both ends of \(0<r<M\)
- nine complete bounded theta comparisons through degree 32, including
  composite \(a\), coincident bracket progressions, and \(r=M-1\)
- negative controls for the incorrect denominator-12 shift, a reversed
  bracket quotient, misuse of residue pairing at \(M=2\), and substitution
  of the wrong target product

The lattice truncations are certified by the nonnegative coordinate
summands and the lower bound \((M-r)Q_a(n)\), not by an arbitrary box.
These finite checks support transcription and boundary-case accuracy.
They are not the proof of the infinite theorem.

## Disposition

The frozen source-status package passes without mandatory changes.
**already_solved** is the justified mathematical/source status for both
30000166 and 30000167. Credit belongs to Berkovich–Garvan and the earlier
core/theta identities they use. This review establishes coverage of the
explicit Möbius–totient product, not a new theorem or an unrestricted
classification of eta products.
