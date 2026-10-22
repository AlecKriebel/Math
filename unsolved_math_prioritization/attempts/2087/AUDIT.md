# Mathematical audit: EP-385 / 2087 composite overshoot

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the partial density theorem, with no external human peer review, journal acceptance, or formal proof-assistant certification claimed. The complete substantive mathematical proof and audit are retained. Only an inline-math formatting typo was corrected before the original candidate was sealed; no mathematical correction is required. Eventual positivity and pointwise divergence remain unresolved by this work. The variance estimate is classical, recorded by Montgomery (2010) and attributed there to Hausman and Shapiro (1973); no novelty or priority of the density corollary is claimed. Executable programs, raw datasets, detailed execution receipts, full computational certificates, and copied source documents are omitted. This is not an executable reproduction package. Edition preparation performed byte-integrity and publication-structure checks, with no new mathematical test execution or scholarly-source retrieval or inspection.

## Verdict and exact acceptance boundary

**ACCEPT AS A PARTIAL RESULT.** With

\[
 F(n)=\max_{4\le m<n,\ m\text{ composite}}(m+p(m)),\qquad G(n)=F(n)-n,
\]

where \(p(m)\) is the least prime divisor, the submitted proof correctly establishes

\[
 \lim_{X\to\infty}\frac{\#\{5\le n\le X:G(n)\le K\}}X=0
 \quad\text{for every fixed real }K\ge0.
\]

For negative fixed \(K\), the same conclusion is immediate from \(G(n)\ge0\).
Thus acceptance can be phrased for every fixed real \(K\), but the nontrivial
theorem is the submitted \(K\ge0\) statement.

This is convergence to infinity in natural density. Neither eventual
positivity for every integer nor pointwise divergence is established. The
audit does not certify a finite exceptional set, a final exception, a new
solution of EP-385, or priority for the density corollary. The finite bounds,
fixed-prime obstruction, and endpoint/scale identities are also correct.

The original accepted candidate manifest has SHA-256
`345aca10acf06aa5a28b54b6b5bce341ef641853162cd759ba2a20d9468f7ca3`
(2,304 bytes, 13 members). The original accepted proof has SHA-256
`4db93534418431268d4a8c54366666141fbb6fcbb29dcf412a02f469308cca44`
(12,064 bytes). The original audit applies to these exact bytes. This edition retains its complete substantive mathematical reasoning; ACCEPTANCE.md and ACCEPTANCE.json bind the edition proof and audit separately.

## 1. Definition, domain, and endpoints

The maximum is nonempty for \(n\ge5\), since \(m=4\) is admissible.
Compositeness is never replaced by merely being coprime to a primorial.
In the witness argument, the interval is exactly \(m=n-h\) with
\(1\le h\le H\), so \(m<n\) is strict. Restricting to \(n>H+1\) ensures
\(m>1\); hence every survivor is either prime or composite, with no
unhandled survivor \(m=1\), zero, or negative integer. A composite survivor
automatically satisfies \(m\ge4\).

The plus sign and least-prime-factor convention agree with the original
1979 definition and with the 1980 formulation. The 1979 scan's apparent
reversal of the elementary square-root bound is correctly rejected rather
than used. No EP-430 equivalence or change of convention is needed.

## 2. Exact reduced-residue variance

Let \(Q\ge2\) be even and squarefree, \(v=\varphi(Q)/Q\), and
\(S(a)=\sum_{h=1}^H1_{(a-h,Q)=1}\). Uniform averaging over all residue
classes gives \(\mathbb ES=Hv\) by translation invariance. Independence
is neither available nor assumed.

For two positions at distance \(d\), a prime divisor \(p\) of \(Q\)
excludes one residue if \(p\mid d\) and two otherwise. CRT therefore gives
exactly the stated product for \(J(d)\). At \(p=2\), odd \(d\) forces
\(J(d)=0\). For even \(d\), dividing by \(v^2\) contributes 2 at 2;
at an odd prime it contributes \(p(p-2)/(p-1)^2\) if \(p\nmid d\),
and \(p/(p-1)\) if \(p\mid d\). Their ratio is
\((p-1)/(p-2)=1+1/(p-2)\). Expanding the latter factors proves (3),
including the empty-sum interpretation for odd \(d\). In particular,
\(d\equiv0\pmod Q\) gives \(J(d)=v\), as it must.

There are \(2(H-d)\) ordered distinct-position pairs at absolute distance
\(d\). This proves the first line of (4). All divisor weights are
nonnegative and all sums are finite, so their rearrangement is legitimate.
The second line follows by writing \(d=2r\ell\).

For every integer \(r\ge1\), the nonincreasing function
\(f(t)=\max(H-2rt,0)\) satisfies
\(\sum_{\ell\ge1}f(\ell)\le\int_0^\infty f(t)\,dt\).
The integral is \(H^2/(4r)\). The strict endpoint \(2r\ell<H\) is
consistent; including an equality endpoint would only add zero.
Thus (5) holds for empty sums, exact divisibility, and every \(H\).

For each odd \(p\mid Q\),

\[
 \frac{p(p-2)}{(p-1)^2}\left(1+\frac1{p(p-2)}\right)=1.
\]

Consequently the full finite divisor sum in (6) cancels exactly. Applying
the integral bound in (4) gives
\(\mathbb E[S(S-1)]\le H^2v^2\), and therefore
\(\operatorname{Var}(S)\le Hv\). No assumption \(H<Q\) is needed:
distinct positions may repeat residues, and the CRT joint count already
handles that possibility. The case \(Q=2\) uses only empty products and
is valid.

The zero-survivor bound follows by restricting
\(\mathbb E(S-Hv)^2\) to \(S=0\). The half-mean bound follows by
restricting it to \(S<Hv/2\). Since \(Hv>0\), division is legitimate;
the strict inequality in the second event is sufficient for the stated
weak upper bound. An upper bound above 1 causes no problem.

## 3. Elementary product estimates

For integer \(y\ge2\), every odd prime at most \(y\) is among the
odd integers \(3,5,\ldots,2R+1\), where \(R=\lfloor(y-1)/2\rfloor\).
Adding the missing odd composite factors to a product of numbers in
\((0,1)\) decreases it. This establishes the direction of the initial
inequality in Lemma 3. The factor inequality is precisely
\(4j^2\ge(2j-1)(2j+1)=4j^2-1\). After multiplication,
\(\prod_{j=1}^R(2j-1)/(2j+1)=1/(2R+1)\ge1/y\).
Taking nonnegative square roots yields \(v_y\ge1/(2\sqrt y)\).
For \(y=2\), \(R=0\) and the empty-product argument still applies.

For Lemma 4, fix integer \(z\) first. Apart from finitely many primes
at most \(z\), all primes lie in reduced residue classes modulo \(Q_z\),
whose exact density is \(v_z\). Hence
\(\limsup\pi(X)/X\le v_z\). The finite Euler product is an absolutely
convergent sum over integers whose prime factors are at most \(z\);
unique factorization ensures that every \(1/j\), \(1\le j\le z\),
is present once. The harmonic sum diverges, so \(v_z\to0\). This proves
prime density zero without the prime number theorem or uniformity in a
growing modulus.

## 4. Transfer and order of limits

Fix \(K\ge0\). Choose an integer \(H\ge\max(1,\lceil K\rceil)\)
and put \(y=2H\). For a composite survivor \(m=n-h\), coprimality with
\(Q_y\) implies \(p(m)>y\). Therefore

\[
 G(n)\ge p(m)-h>y-h\ge y-H=H\ge K.
\]

The displayed abbreviated inequality (7) is valid, including \(h=H\)
and \(K=H\), because \(p(m)>y\) is strict. If a bad integer has any
survivor, all its survivors must instead be prime. The submitted set
inclusion (8) is consequently valid; the union of shifted-prime sets is
a harmless enlargement.

For fixed \(H\), the zero-survivor set is periodic modulo the fixed
\(Q_{2H}\), so its natural density exists. Each shifted-prime set has
density zero, and there are only \(H\) such sets. The finitely many
small integers have density zero. Thus the bad set has upper density at
most \(1/(Hv_{2H})\le2\sqrt2/\sqrt H\).

Only now does \(H\) tend to infinity. More explicitly, for any
\(\varepsilon>0\), choose a single sufficiently large \(H\), depending
on \(K,\varepsilon\), so that this bound is below \(\varepsilon\);
then take the upper \(n\)-density with that \(H\) held fixed. The upper
density is zero. Nonnegativity of the counting ratio supplies its lower
limit, so the natural density exists and is zero.

There is no exchange of a growing modulus with an unproved prime-counting
estimate, no intersection of density-one sets used as a pointwise claim,
and no inference that a density-zero set is finite.

## 5. Finite inequalities

With integer \(y\ge\max(2,\lceil H+K\rceil)\), the same witness chain
gives \(p(m)-h>y-H\ge K\). A periodic set of residue proportion at
most \(b\) has at most \((X+Q)b\) members up to integer \(X\), by
counting complete periods and one remainder period. Applying this with
\(b=1/(Hv)\), bounding each shifted-prime set by \(\pi(X)\), and
allowing \(H+1\) initial integers gives (10).

For (11), use the half-mean exceptional set with proportion
\(4/(Hv)\). At every remaining bad \(n>H+1\), at least \(Hv/2\)
survivors are prime. The number of ordered incidences \((n,h)\) with
\(n\le X\), \(1\le h\le H\), and \(n-h\) prime is at most
\(H\pi(X)\): each \(h\) permits at most one \(n\) per prime.
Thus this class has size at most \(2\pi(X)/v\). The claimed (11)
follows. These bounds may be numerically weak for large \(Q\), but are
correct finite inequalities and expose the relevant dependencies.

## 6. Obstruction and scale statements

If \(Q_y\mid n\) and \(p=p(m)\le y\), both \(n\) and \(m\)
are divisible by \(p\). Their positive difference is at least \(p\),
so \(m+p\le n\). Every fixed finite set of least prime factors can
be placed below a fixed cutoff. Therefore this method cannot provide
positive-gap witnesses at all primorial multiples. It does not show
that those multiples are actual counterexamples, because larger least
prime factors remain available.

If \(Q_y\mid n\) and \(1\le H\le y\), \(h=1\) is coprime to
\(Q_y\), whereas every \(2\le h\le H\) has a prime divisor at most
\(y\). Thus \(S(n)=1\) exactly. The primality or compositeness of
\(n-1\) is still decisive.

For odd \(n\ge5\), \(m=n-1\) is an even composite and gives
\(F(n)\ge n+1\). For even \(n\ge6\), \(m=n-2\) is an even
composite and gives \(F(n)\ge n\). Every admissible \(m+p(m)\) is
even: use \(p(m)=2\) for even \(m\), and odd plus odd otherwise.
When even \(n\) has composite \(n-1\), its least factor is at least
3, giving \(F(n)\ge n+2\). Hence equality \(F(n)=n\) requires
\(n-1\) to be an odd prime.

Compositeness gives \(p(m)\le\sqrt m\), proving
\(F(n)\le n-1+\lfloor\sqrt{n-1}\rfloor<n+\sqrt n\).
At \(n=q^2+1\), the prime-square witness attains this upper bound
exactly: \(F(n)=q^2+q\), \(G(n)=q-1\). Infinitely many primes and
the global upper bound imply \(\limsup G(n)/\sqrt n=1\). This
subsequence observation supplies no uniform lower bound.

## 7. Sources and attribution

The source review uses primary sources and distinguishes inspected
content from bibliographic attribution:

- H. L. Montgomery, [The combinatorics of moment calculations](https://hrj.episciences.org/168/pdf),
  Hardy-Ramanujan Journal 33 (2010), 2–22. The relevant displayed
  second-moment formula and variance bound are on printed p. 7 / PDF
  page 6, immediately after (15). The page image was visually inspected;
  the official PDF text and journal metadata were also checked. The
  Hausman–Shapiro reference is on printed p. 21 / PDF page 20.
- M. Hausman and H. N. Shapiro, [On the mean square distribution of primitive roots of unity](https://doi.org/10.1002/cpa.3160260407),
  CPAM 26 (1973), 539–547. Historical attribution was checked in
  Montgomery. The original 1973 article was not independently inspected;
  its DOI open did not return content. No proof step depends on accepting
  an uninspected external theorem.
- P. Erdős, [Some unconventional problems in number theory](https://users.renyi.hu/~p_erdos/1979-23.pdf),
  Acta Math. Acad. Sci. Hungar. 33 (1979), 71–80. Printed p. 73 / PDF
  page 3 was visually checked for the composite definition and apparent
  reversed trivial bound.
- P. Erdős and R. L. Graham, [Old and new problems and results in combinatorial number theory](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf),
  1980. The actual formulation was visually checked at printed p. 74 /
  PDF page 70. This location is preferable to repeating the different
  pagination cited in Tao's blog.
- T. Tao, [Erdos problem #385, the parity problem, and Siegel zeroes](https://terrytao.wordpress.com/2024/08/19/erdos-problem-385-the-parity-problem-and-siegel-zeroes/),
  19 August 2024. Its primorial short-window obstruction and proposed
  semiprime-gap route support the submitted contextual attribution.
  They are not used as unconditional hypotheses.

The proof's variance inequality is classical and is correctly credited.
Its direct density consequence has no verified priority claim, and none
is made. Montgomery's nearby informal statement of a Bernoulli variance
omits the factor \(1-v\); the audited proof neither adopts that statement
nor assumes independence. Its self-contained CRT argument proves the
actual bound used.

Full local PDF byte counts and hashes were checked. Public web tools were
used to inspect the official sources, but this audit does not describe
those web opens as independent full-file byte acquisitions. Original
source texts and page images are excluded from this audit packet.

## 8. Independent exact checks

The original auditor authored an independent verifier using only the Python
standard library, without executing or importing candidate code. Its explicit
gates remained enabled under normal Python, `-O`, and `-OO`. All three historical
runs passed and their output bytes were identical. Programs, detailed receipts,
and full computational certificates are omitted here. The following records
historical independent checks, not a new execution or executable reproduction
from this edition.

- All 16 even squarefree moduli formed from 2 and subsets of
  \(\{3,5,7,11\}\), including non-primorial moduli.
- 9,264 direct full-residue joint counts against both the CRT product
  and nonnegative divisor expansion, including \(d=Q\) and \(d>Q\).
- 185 exact moment cases, 55,226 residue-count values, repeated-residue
  intervals \(H\ge Q\), mean/factorial-moment identities, variance,
  and both exceptional-proportion bounds.
- 33,153 exact triangular-sum checks and 749 totient/harmonic product
  checks, including the empty-product endpoint.
- A descending-overwrite factor sieve and strict-prefix maximum through
  \(10^6\), with fresh trial-division literal maxima through 2,500.
  The canonical \((n,F(n))\) digest independently matches
  `b901d58b820468153d3b362af820d0f7a09b2b30d46d210353148896fb3b3f82`.
- 69,730 transfer cases, including fractional \(K\); 560 instances of
  the two finite inequalities; 280 prime-incidence threshold checks;
  110,846 fixed-prime obstruction pairs; and 168 prime-square equalities.

The finite computation finds 100 zero-gap integers through \(10^6\),
with the largest in that range equal to 267680. This reproduces only the
stated finite range and is not evidence that there are no later exceptions.
None of these finite checks replaces the analytic proof.

## 9. Integrity and corrections

An independently authored fail-closed inventory verifier authenticated
all 13 final candidate members against the externally supplied manifest
pin, in normal, `-O`, and `-OO` modes. It checks unique keys and member
paths, exact byte counts and hashes, path containment, no symlinks, and
complete inventory membership. Synthetic disposable fixtures exercised
42 negative controls and 3 positive controls across the three modes.

The only requested correction was an inline-math formatting typo in the
definition of \(v_y\). It was corrected before the candidate was sealed.
There are no remaining required mathematical corrections. The original audit's
manifest and external seal bind its original deliverables and check receipts.
This edition retains verification metadata while omitting executable programs,
raw datasets, detailed receipts, full computational certificates, and source
copies. Edition preparation did not rerun mathematical tests or newly inspect
scholarly sources.

**Final boundary:** valid density theorem and valid supplementary
lemmas; the two original universal questions remain unresolved by this
work.
