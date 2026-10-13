# Saito's Möbius–totient eta product: an already proved theorem

**Target:** 30000166 / OWR-782-007; duplicate target 30000167.  
**Classification:** known affirmative answer; recommended `already_solved`, 0/5 fresh proof attempts.  
**Credit:** Alexander Berkovich and Frank G. Garvan, 2006 preprint, expanded 2007 preprint, published 2008. This is a publication-free known-result reconciliation, not a new discovery. Two fresh independent mathematical families reviewed the exact original body on 2026-10-03 with no mandatory science correction. This preparer is not an independent third mathematical reviewer. Native changes, acceptance, merge and publication remain unapproved here.

## 1. Exact source and resolution

In Tomoyoshi Ibukiyama's contribution to [Oberwolfach Report 1/2005](https://doi.org/10.4171/owr/2005/01), printed pp. 54–55, the conjecture is the nonnegativity of every Fourier coefficient of

$$S_N(\tau)=\eta(N\tau)^{\varphi(N)}\prod_{d\mid N}\eta(d\tau)^{-\mu(d)}\qquad(N\ge1).$$

The report proves prime-power cases and leaves the case with at least two distinct prime factors open. This is precisely the present target. The report also discusses eta products from regular weight systems; that broader terminology must not replace this explicit formula. Pinned record 30000167 repeats the same remaining composite case and is covered by this one audit.

Berkovich–Garvan's [July 25, 2006 preprint](https://arxiv.org/abs/math/0607606) states this exact formula as Conjecture 1.1 and proves it for every positive integer. Their [expanded February 1, 2007 paper](https://arxiv.org/abs/math/0702027), also Conjecture 1.1, gives the necessary theta identity in Theorem 1.2 and the full proof in Section 3 (printed pp. 5–6). The published reference is *Journal of Number Theory* **128** (2008), no. 6, 1731–1748, [DOI 10.1016/j.jnt.2007.02.002](https://doi.org/10.1016/j.jnt.2007.02.002), independently confirmed by the [author's publication list](https://qseries.org/fgarvan/publist.html). The mathematical audit below uses the full accessible 2007 preprint rather than claiming a line-by-line comparison with the typeset journal version.

The original archive's version/search statements are historical. The two 2026-10-03 reviews accessed both versioned primary manuscripts and recorded bounded access/version limits; no exhaustive correction absence is asserted. Their SOURCE observations distinguish readable primary text from unavailable inspectable pixels and an unobtained typeset journal proof. Yasuda's [2010 paper](https://ems.press/content/serial-article-files/41111) treats the regular-weight-system conjecture and explicitly credits Berkovich–Garvan for the distinct eta-product family here (p. 563); it is not necessary to substitute that later theorem for the exact resolution.

## 2. Fourier normalization

Put $q=e^{2\pi i\tau}$ and $E(q)=\prod_{m\ge1}(1-q^m)$. Then

$$S_N(\tau)=q^{A_N}\widetilde S_N(q),\qquad
A_N=\frac{N\varphi(N)-\sum_{d\mid N}d\mu(d)}{24},\qquad
\widetilde S_N(q)=\frac{E(q^N)^{\varphi(N)}}{\prod_{d\mid N}E(q^d)^{\mu(d)}}.$$

Thus it suffices to prove $\widetilde S_N\in\mathbb Z_{\ge0}[[q]]$. A possibly fractional leading exponent does not change coefficient signs. For $N=1$ the product is exactly 1. For a prime $p$, $A_p=(p^2-1)/24$.

The historical archive claims visual inspection of a denominator-12 prime display. Fresh accessible primary text was read by the preparer and new families, but their screenshot requests did not supply inspectable pixels; none of those fresh reads revalidates the historical PDF hashes or visual receipt. Direct substitution in $\eta=q^{1/24}E(q)$ gives $(p^2-1)/24$, agreeing with Berkovich–Garvan (1.6). Examples are $A_2=1/8$, $A_3=1/3$ and $A_6=5/12$. Fractional shifts are permitted, and this local normalization issue does not change coefficient signs.

## 3. The imported positive identities

We use two explicit identities from Berkovich–Garvan, with their original attribution. For every integer $t\ge1$,

$$\frac{E(q^t)^t}{E(q)}=\sum_{m\ge0}a_t(m)q^m,$$

where $a_t(m)$ counts $t$-core partitions. This is their equation (1.5), credited to Littlewood and to the combinatorial proof of Garvan–Kim–Stanton. In particular all coefficients are nonnegative, including the case $t=1$.

For $a\ge2$, let $\Lambda_a=\{n\in\mathbb Z^a:\sum_i n_i=0\}$ and

$$Q_a(n)=\frac a2\sum_{i=0}^{a-1}n_i^2+\sum_{i=0}^{a-1}i n_i,
\qquad [z;q]_\infty=\prod_{m\ge0}(1-zq^m)(1-z^{-1}q^{m+1}).$$

Their Theorem 1.2 states

$$C_a(z;q):=\sum_{n\in\Lambda_a}\sum_{j=0}^{a-1}q^{Q_a(n)}z^{a n_j+j}
=E(q)E(q^a)^{a-2}\frac{[z^a;q^a]_\infty}{[z;q]_\infty}.$$

This is a convergent theta identity for $|q|<1$ and $z\ne0$, interpreted by removable continuation when necessary. Its proof in Section 2 is available in full: both sides satisfy $F(qz)=z^{-(a-1)}F(z)$; the theta summands are permuted by cyclic lattice changes of variables; equality at the $a$th roots of unity follows from cancellation and the known core theta identity at 1. The standard theta uniqueness step then establishes the identity. We rely on this credited theorem, rather than presenting it as newly proved here.

### Specialization is legitimate and preserves positivity

For integers $M>r>0$, the exponent after substituting $z=q^r$ and the base $q^M$ is

$$e(n,j)=M Q_a(n)+r(a n_j+j).$$

Here are explicit checks that this is a genuine nonnegative-power series, not merely a formal substitution in an uncontrolled Laurent series. On $\Lambda_a$,

$$Q_a(n)=\sum_{i=0}^{a-1}\left(\frac a2 n_i(n_i-1)+i n_i\right)\ge0.$$

Each individual summand is a nonnegative integer: this is immediate for $n_i\ge0$, while $n_i=-k<0$ gives $k(a(k+1)/2-i)>0$.

Let $T_jn=(n_1,\ldots,n_{a-1},n_0)+e_{j-1}-e_{a-1}$ for $j\ge1$, and let $T_0n=(n_1,\ldots,n_{a-1},n_0)$. These are bijections of $\Lambda_a$, and direct expansion gives

$$Q_a(T_jn)-Q_a(n)=a n_j+j.$$

Consequently

$$e(n,j)=(M-r)Q_a(n)+r Q_a(T_jn)\ge0.$$

The positive-definite quadratic part also makes each sublevel set finite. Hence the specialized theta series belongs to $\mathbb Z_{\ge0}[[q]]$, with finitely many summands contributing to each coefficient.

Define

$$D_a(z;q)=\frac{E(q^a)^a}{E(q)}C_a(z;q)
=E(q^a)^{2a-2}\frac{[z^a;q^a]_\infty}{[z;q]_\infty}.$$

The two identities now imply $D_a(q^r;q^M)\in\mathbb Z_{\ge0}[[q]]$ whenever $0<r<M$.

## 4. Factorization covering every positive integer

This is the factorization in Section 3 of the cited paper, with its parameter coverage made explicit. First, Möbius inversion gives

$$\prod_{d\mid M}E(q^d)^{\mu(d)}
=\prod_{\substack{k\ge1\\(k,M)=1}}(1-q^k),$$

since the exponent of $1-q^k$ on the left is $\sum_{d\mid(M,k)}\mu(d)$.

Suppose $N=pM$, where $p$ is prime, $M>1$ is odd, and $p\nmid M$. Pair the reduced residue classes $r$ and $M-r$. With

$$R_M=\{r:1\le r\le(M-1)/2,\ (r,M)=1\},$$

there are $\varphi(M)/2$ pairs and

$$\prod_{d\mid M}E(q^d)^{\mu(d)}=\prod_{r\in R_M}[q^r;q^M]_\infty.$$

The divisors of $pM$ split into $d$ and $pd$, with $\mu(pd)=-\mu(d)$ for $d\mid M$. Therefore

$$\boxed{\widetilde S_{pM}(q)=\prod_{r\in R_M}D_p(q^r;q^M).}$$

Indeed, the numerator's exponent of $E(q^{pM})$ is $(2p-2)|R_M|=(p-1)\varphi(M)=\varphi(pM)$, and the bracket quotient gives precisely the ratio of the two Möbius products. Every factor has nonnegative coefficients by Section 3.

For $N=p^\alpha M$ with $p\nmid M$, let $N'=pM$ and $t=p^{\alpha-1}$. The nonzero Möbius terms depend only on the prime divisors, so $N$ and $N'$ have the same denominator product. Also $\varphi(N)=t\varphi(N')$. Hence

$$\boxed{\widetilde S_N(q)=
\left(\frac{E((q^{N'})^t)^t}{E(q^{N'})}\right)^{\varphi(N')}
\widetilde S_{N'}(q).}$$

The first factor is a positive integral power of a $t$-core generating function. If $M=1$, begin instead with

$$\widetilde S_p(q)=E(q^p)^p/E(q),$$

and the same lifting formula handles all prime powers. Finally, every $N>1$ is covered: when $N$ is even choose $p=2$ and remove its full prime-power factor, leaving odd $M$; when $N$ is odd choose any prime divisor and again remove its full power, leaving odd $M$. Together with $N=1$, this proves the exact all-$N$ statement using the known identities.

## 5. Scope and reproducibility

There is no remaining mathematical case of targets 30000166 or 30000167 under the displayed formula. The conclusion is nonnegative, not strictly positive, coefficients. For instance zeros in core-partition series are permitted. No claim about all conceivable regular-weight eta products is made.

The unchanged original `verify.py` and saved `verification.json` are historical finite diagnostics. Original preparation actually replayed them and the old review checker with exact bytes and recursive JSON types/keys/values: 2,837 author assertions and 35,980 historical-review assertions. That replay is not a new independent family. The two fresh families separately report 324,186 algebra assertions and 140,708 geometry assertions; these remain diagnostics, not the infinite proof. Their checkable universal derivations independently expose the core/theta foundation, analytic uniqueness and all-N factorization. All dated original PASS, PDF, model, runtime, pending-review and publication-readiness claims are qualified globally in `GLOBAL_QUALIFICATIONS.json`; literal originals remain under `../original_head_archive`.

Original accounting stays one JSON object, zero proof attempts, budget 5, two source-audit events, with no separately supplied source-verification response count. Both source records omit `prior_report`; selected SQL reports contain text `{}` rather than NULL. Duplicate 30000167 shares this result and budget. Its absent native queue row is not invented. No new theorem, paper, DOI or tracker result is recommended.
