# Independent audit: Function Theory 6.38

Date: 2026-10-03 UTC. Problem ID: 2306038; code: AMR-022-6038.

## Verdict

**Pass. The proposed `already_solved`, `1/5` disposition is supported.**

The reviewed deduction correctly applies V. I. Milin's 1981 Theorem 2 to obtain the requested convergence, and indeed convergence for every positive exponent. No mathematical correction is required. This is an independent AI-assisted review, not human peer review, formal verification, or a new resolution of the problem.

The reviewed artifact manifest has SHA-256

`7e8014501eac1508b685c502304b8d502711d99ad87c8e25c9966041b0d4cb0b`.

All eight entries in that manifest passed checksum verification. The reviewed artifacts were left unchanged.

## Primary-source scope

The review used the complete relevant source material, rather than an abstract or a search-result summary:

1. Hayman–Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2: printed p. 131, including Problems 6.37–6.38 and both updates, and printed p. 237, reference [576]. Both pages were visually checked.
2. V. I. Milin, *O sosednikh koeffitsientakh nechetnykh odnolistnykh funktsii*, Sibirsk. Mat. Zh. 22:2 (1981), 149–157: all of pp. 149–155 were read from page images and checked against the extracted text. The relevant chain ends at Corollary 1, equation (34), on p. 155; Corollary 2 and the endpoint example were also checked. The separate starlike-function argument is not a dependency of this conclusion.
3. I. M. Milin, *Adjacent coefficients of univalent functions*, Dokl. Akad. Nauk SSSR 180:6 (1968), 1294–1297: all four pages, including the proofs of both theorems, were read visually.

Source locators: [Hayman–Lingham](https://arxiv.org/abs/1809.07200), [1981 article](https://www.mathnet.ru/eng/smj6431), [1968 article](https://www.mathnet.ru/eng/dan33933). Source PDFs, scans, and full extracted texts are not reproduced in this audit.

## Exact target and hypotheses

The question concerns an analytic, normalized, odd univalent function

\[
f_2(z)=z+\sum_{n\ge1}c_{2n+1}z^{2n+1},\qquad c_1=1,
\]

with

\[
d_n=|c_{2n+1}|-|c_{2n-1}|,
\qquad \beta_0=(\sqrt2-1)^2=3-2\sqrt2>0.
\]

The series is \(\sum_{n\ge1}n^{-\beta_0}d_n^2\). Thus the differences are signed real differences of moduli before squaring. They are not differences of the complex coefficients themselves. The question contains no positive-growth, starlikeness, or coefficient-reality hypothesis.

The 1981 paper defines \(S_2\) to be precisely the normalized odd subclass of \(S\), with \(f_2(z)=\sum_{k\ge0}b_kz^{2k+1}\). Consequently \(b_k=c_{2k+1}\), \(b_0=c_1=1\), and \(|b_k|-|b_{k-1}|=d_k\). There is no index offset or missing initial term.

Theorem 2, equation (30), pp. 153–154, states that an absolute constant \(A<50\) satisfies

\[
\sum_{k\ge1}\alpha_k k(|b_k|-|b_{k-1}|)^2
\le A\sum_{k\ge1}\alpha_k
\]

for every \(f_2\in S_2\) and every nonnegative, nonincreasing, summable sequence \(\alpha_k\). Choosing \(\alpha_k=k^{-1-\varepsilon}\) meets all three sequence hypotheses whenever \(\varepsilon>0\). The resulting weight on the squared differences is exactly \(k^{-\varepsilon}\), and the right side is finite by the integral test. This is also Corollary 1, equation (34), p. 155.

Taking \(\varepsilon=\beta_0\) proves the target. The 2018 update uses the parameterization \(n^{-2\beta}\); its parameter must therefore be set to \(\beta_0/2\), as the reviewed proof correctly explains.

## Adversarial check of the 1981 proof chain

### Logarithmic normalization and the odd transform

Equation (6) is \(\log(F(z)/z)=2\sum_{k\ge1}\gamma_kz^k\). For an arbitrary \(f_2\in S_2\), the associated function is

\[
F(w)=f_2(\sqrt w)^2=w\phi(w)^2,\qquad
\phi(w)=f_2(\sqrt w)/\sqrt w=\sum_{k\ge0}b_kw^k.
\]

These expressions are single-valued analytic power series. The transform belongs to \(S\): equality of two squared values of \(f_2\), followed by its injectivity and oddness, forces equality of the squared arguments. Thus the paper does not impose an additional univalence assumption on the original odd function.

Since \(\phi(0)=1\) and \(\phi\) has no zeros, its normalized analytic logarithm exists, and \(\log\phi=\sum\gamma_kw^k\). In equations (19)–(22),

\[
\psi=(1-tz)\phi=g(1-tz)^{1/2},\qquad
g=(1-tz)^{1/2}\phi,
\]

so the logarithmic coefficients of \(g\) are exactly
\(\mathcal A_k=\gamma_k-t^k/(2k)\). The factor \(1/2\) has not been lost or confused with the 1968 normalization.

### Phase choice, radial estimates, and coefficient bound

Theorem 1 uses the area estimate and distortion estimate to obtain (7). Its corollary (17) follows with the paper's parameters \(p=r\), \(h=1/2\); the term involving \(L\) vanishes. The phase has modulus one and may depend on the chosen radius.

Lemma 1 correctly chooses \(t=t_{\sqrt r}\) when its exponential-coefficient bound uses \(r^k\), rather than \(r^{2k}\). The coefficients \(D_k\) depend on this fixed phase. In applying area identities, the phase is fixed for the chosen radius; no derivative with respect to a radius-dependent phase is taken.

The generalized Lebedev–Milin inequality is used with \(\lambda=1/2\). The binomial coefficients \(d_k(\lambda)\), the intermediate estimates (25)–(29), and the special estimate

\[
\sum_{k\ge1}k|D_k|^2r^{2k}\le\frac{2r}{1-r}
\tag{24}
\]

are consistent. For the special case, the factor in (29) is bounded by
\(e^{\gamma/2}(1+\sqrt r)^2/(2\sqrt{1+r})\le e^{\gamma/2}\sqrt2<2\), where \(\gamma\) is Euler's constant. This confirms the stated constant rather than merely the order of growth. The proof of the general \(s>1/2\) estimate uses the elementary lower bound for \(1-r^m\) and the minimum of \(a^a\); only \(s=1\) is subsequently needed.

Differentiating \(\psi=g(1-tz)^{1/2}\) and using the squared triangle inequality yields (31). Parseval's area identity supplies the factor \(k\) on the squared coefficient differences. The standard uniform odd-function coefficient bound \(|b_k|^2<2\), explicitly used on p. 154, controls the remaining area integral. This gives

\[
\sum_{k\ge1}k|b_k-t_{\sqrt r}b_{k-1}|^2r^{2k}
\le \frac{8r}{1-r}+\sum_{k\ge1}\frac{r^{2k}}k.
\]

All series and area computations here are at \(r<1\), within their convergence disks. The reverse triangle inequality removes the phase in the correct direction:
\(\bigl||b_k|-|b_{k-1}|\bigr|\le|b_k-tb_{k-1}|\).

### Partial sums, constants, and passage to infinity

For \(k\le N\), \(r^{2k}\ge r^{2N}\). Also

\[
\sum_{k\ge1}\frac{r^{2k}}k
\le\frac{r^2}{1-r^2}\le\frac{r}{2(1-r)}.
\]

Taking \(r=1-1/(2N)\) therefore bounds the partial sum
\(S_N=\sum_{k=1}^Nk d_k^2\) by

\[
S_N\le17N\left(1+\frac1{2N-1}\right)^{2N-1}<17eN<50N.
\]

In particular, the claimed constant less than 50 is consistent throughout the proof.

For decreasing nonnegative weights, finite Abel summation gives

\[
\sum_{k=1}^N\alpha_k k d_k^2
=\alpha_NS_N+\sum_{k=1}^{N-1}(\alpha_k-\alpha_{k+1})S_k
\le A\sum_{k=1}^N\alpha_k.
\]

Both coefficient factors on the right before the estimate are nonnegative. Monotonicity is a genuine hypothesis here. The finite identity includes its terminal term, so there is no unjustified discarded boundary term. Nonnegative partial sums then increase to a finite limit because \(\sum\alpha_k<\infty\). This justifies the infinite series for every positive exponent, including arbitrarily small positive exponents.

The area theorem, distortion estimate, classical odd-function coefficient bound, and Lebedev–Milin inequality are established external inputs to the published proof. Their original foundational proofs were not independently reconstructed in this review. The deduction from them and from the cited theorem was checked, but not formally verified.

## Bibliographic distinction

The 1981 title page identifies **V. I. Milin**. The 1968 title page identifies **I. M. Milin**. The 2018 collection's [576] explicitly names the 1968 article.

The 1968 Theorem 1 bounds adjacent coefficient-modulus differences for general normalized univalent functions. Its Theorem 2, equations (18)–(20), concerns odd functions with a nonzero growth parameter and obtains an \(O(n^{-1/2})\) estimate by applying a logarithmic-coefficient estimate valid under that hypothesis. All four pages were checked; they do not state the universal weighted-summability theorem used in this note. The 1981 theorem supplies that unrestricted statement explicitly.

The reviewed correction is consequently supported. This audit makes no claim about the earliest possible proof, the origin of the 2018 bibliographic mismatch, or whether other publications contain related results.

## Endpoint and finite controls

The endpoint example \(f_0(z)=z/\sqrt{1-z^4}\) is admissible. The chosen analytic square root exists in the disk. For \(H(w)=w/(1-w^2)\), equality \(H(u)=H(v)\) gives \((u-v)(1+uv)=0\), so \(H\) is injective in the disk. Squaring \(f_0\), then using oddness and its unique zero, proves injectivity of \(f_0\).

With \(a_m=4^{-m}\binom{2m}{m}\), its coefficients obey \(b_{2m}=a_m\), \(b_{2m+1}=0\). The reviewed indexing \(d_1=-1\), \(d_{2m}=a_m\), \(d_{2m+1}=-a_m\) for \(m\ge1\) is correct. The recurrence yields \(a_m^2\ge1/(4m)\) by induction, so \(\sum d_n^2=\infty\). This establishes the endpoint failure analytically; finite tests alone would not do so.

The supplied verifier was inspected, run, and found to reproduce the supplied JSON exactly. A separately written `replay.py` also checks the artifact hashes, exponent identities, Abel coefficients and terminal term, coefficient recurrence, endpoint indexing, and exact finite constant bounds. It includes negative controls for an increasing-weight misuse and for replacing modulus differences by complex differences. These are auxiliary regression checks, not a proof of the analytic theorem or infinite convergence.

## Limits and disposition

No blocking issue or required amendment was found. The existing public mathematical exposition supports `already_solved`, with no original-result or priority claim. The `1/5` label is compatible with a single substantive literature-resolution attempt; it is bookkeeping rather than a mathematical invariant. The frozen status field recording a pending review is superseded by this separate audit, without altering the reviewed bytes.

This review did not repeat repository-wide prior-work searches, certify historical priority, or make any remote changes. Those claims are not needed for the mathematical disposition. All conclusions above concern the identified frozen artifacts and the stated primary-source reading scope.
