# PR1129 geometric proof audit — PASS

Audit completed 17 October 2026 UTC. Target: problem 30005461 / OWR-12697710-007. Original PR head supplied for this audit: `26fed29c1130e539ba018a37200f133870f0e036`.

**PASS for the complete essential geometric argument.** For each fixed real $c<3$, the proof correctly establishes that all sufficiently large odd powers of

\[
f_c=x^4y^2+x^2y^4+1-cx^2y^2
\]

are sums of squares of real polynomials. It therefore correctly proves \(\lim_k c_k=3\) for the thresholds in the original question. I found no mathematical repair needed in the audited principal argument. This verdict imports Scheiderer's published theorem and the standard sheaf/cohomology framework; it is not a formal verification or a reproof of the entire foundational literature.

This geometric verdict is independent of the previous acceptance wording. It does not audit the separate mixed-exponent proof or optional real-delta appendix, and does not certify historical originality. The former is expressly credited to Blekherman–Kozhasov–Reznick in the supplied record. The geometric application is not identified with an explicitly credited prior complete answer merely because it uses a published general theorem or carries a generic no-novelty disclaimer. No inspected primary body explicitly supplied the full target-specific prior answer. This limited source inspection cannot establish novelty or exhaustive priority clearance.

## Frozen material and source boundary

I read the entire principal `PROOF.md`, original `MATHEMATICAL_AUDIT.md`, `SOURCE_REVIEW.md`, and `SOURCE_METADATA.json`. The principal proof is 10,963 bytes, SHA-256 `46af7394ebfee7b0de9861693f84ab684502da3be208c626411f24e2538c7d15`; the original audit is 13,253 bytes, SHA-256 `f9faede12ad50034f5620f4576c621dc275a6ddbbf29bb3e13096d778a094cce`. `INPUT_PINS.json` fingerprints the ten frozen inputs. No other current review reports were read.

I freshly fetched the actual primary source bodies, rather than accepting the input's source descriptions:

- [Reznick's OWR contribution](https://ems.press/content/serial-article-files/47007): complete printed pp.778–780, physical PDF pp.38–40; physical p.40 visually inspected. Its coefficient perturbation and threshold interval are exactly the family above. The separate later perturbation by a positive multiple of \((x^2+y^2+z^2)^3\) is a different question. The downloaded 72-page PDF is 734,622 bytes, SHA-256 `5a9bdc9f9daa12ef35185ceae208c0f2f75e191875827f78b7b6ad0f5cdbf240`.
- [Scheiderer's author manuscript](https://www.math.uni-konstanz.de/~scheider/preprints/ppss.pdf): sign conventions §2.4–2.5, all of Theorem 4.1 and its proof on pp.9–11, Corollary 4.2, and relevant neighboring remarks; pp.9 and 11 visually inspected. The fresh 14-page, 5 April 2011 manuscript is 275,091 bytes, SHA-256 `686cfde78b5472be2f6a0185873822098f61006ba78b79ecfaccdd3365882cb0`, exactly the historical input pin. I did not inspect a publisher-typeset full-text PDF. The [current publisher abstract and bibliographic record](https://link.springer.com/article/10.1007/s00229-011-0484-3) independently confirm the needed general theorem and its published identity: *Manuscripta Mathematica* 138 (2012), 73–88; online 6 August 2011. The [author's publication list](https://www.mathematik.uni-konstanz.de/scheiderer/publikationen/papers/) agrees.
- [Stacks Project tag 01XS](https://stacks.math.columbia.edu/tag/01XS): Lemma 30.8.1 and its full proof, including the monomial Čech decomposition. The inspected formula applies over \(\mathbb R\), in every twist, with no smoothness hypothesis on the later hypersurface. Downloaded HTML fingerprint is recorded in `FETCH_FINGERPRINTS.json`.

`FETCH_FINGERPRINTS.json` records URLs, redirects, UTC times, sizes and digests. All downloaded bodies, derived source text, and page images remain under ignored `sources/private/`; no such source content is copied into the authored deliverables. The source version boundary is the freshly retrieved manuscript plus current publisher theorem abstract, not an asserted comparison of every sentence against the subscription typeset article. The published abstract states the exact scope needed here.

## Exact imported interface

The needed consequence of Corollary 4.2 is: on a reduced projective real scheme with dense real locus and no curve components, positive sections of squares of line bundles $L,M$, with $M$ ample, give an SOS $fg^N$ in the square bundle of $L\otimes M^N$ for every sufficiently large integer $N$. The sums involve global real sections. Neither smoothness nor an initial SOS representation of $g$ is required. I checked the entire proof route: its auxiliary square factor is canceled before the conclusion; its initial two applications cover both exponent parities. The theorem is over the usual real numbers, exactly the base field used here. Those published foundational results are imported, not independently reproved in this audit.

## Adversarial reconstruction

### 1. The surface has every required scheme property

Set $R=\mathbb R[A,B,C,D]$, $G=ABC-D^3$, and $S=\operatorname{Proj}(R/(G))\subset\mathbb P^3_{\mathbb R}$. Viewed in \(\mathbb R[A,B,D][C]\), $G$ is primitive: no irreducible factor divides both $AB$ and $D^3$. It has degree one over \(\mathbb R(A,B,D)\), so Gauss's lemma makes it irreducible in $R$. Since $R$ is a UFD it is prime. The graded quotient is a domain, of Krull dimension three, and its Proj has dimension two. Thus the projective scheme is integral and reduced with one surface component. No hidden curve or nonreduced component can violate the theorem.

On $D\ne0$, normalize $D=1$. Its coordinate algebra is \(\mathbb R[a,b,c]/(abc-1)\cong\mathbb R[a^{\pm1},b^{\pm1}]\). Inverses exist already in the quotient, for example $a^{-1}=bc$. A Laurent polynomial vanishing at every \((a,b)\in(\mathbb R^*)^2\) is zero: clear a monomial denominator, then apply the polynomial identity principle in each variable. Hence the real torus is dense in this chart, which is dense in integral $S$. This proves the full real-density condition without a claim about the substitution map's image.

As a further adversarial check, the gradient is

\[
\nabla G=(BC,AC,AB,-3D^2).
\]

Its projective vanishing locus consists precisely of \([1:0:0:0],[0:1:0:0],[0:0:1:0]\). At $D=0$, the boundary is the union of the three coordinate lines $ABC=0$ in the coordinate plane. The proof must cover that whole boundary, not only the singular vertices; it does. The hyperplane sheaf \(H=\mathcal O_S(1)\) is the restriction of an invertible very ample sheaf along the given closed embedding. At a point with $T\ne0$, the coordinate $T$ is a local generator. Thus singularity neither destroys its invertibility nor changes its ampleness.

These checks validate principal PROOF lines 35–57.

### 2. Positivity holds on the full real locus in the correct bundle

For every nonzero real coordinate vector on $G=0$, AM–GM applied to the squares gives

\[
A^2+B^2+C^2\ge3(A^2B^2C^2)^{1/3}=3D^2.
\]

There is no assumption that $A,B,C,D$ are positive. Squaring $ABC=D^3$ makes the last equality valid for all real sign patterns. If $D\ne0$, then $q_c=A^2+B^2+C^2-cD^2\ge(3-c)D^2>0$. If $D=0$, the expression is the positive sum $A^2+B^2+C^2$, since the projective vector is nonzero. This also covers every real singular point. It works for arbitrary real $c<3$, including nonpositive parameters.

In the local frame $T$ of $H$, the coefficient of $q_c\in H^0(S,H^2)$ is $q_c/T^2$. Its sign is unchanged. This is the precise square-bundle positivity required by the source, not only positivity of an affine rational function. At $c=3$, the point \([1:1:1:1]\) has $q_3=0$; at $c>3$ that value is negative. Thus the chosen strict inequality is essential and correctly respected.

These checks validate principal PROOF lines 61–76.

### 3. The output really includes odd powers with the right real global square roots

Take $X=S$, $L=M=H$, and $f=g=q_c\in H^0(S,H^2)$. Every imported hypothesis has now been checked. For a fixed parameter $c<3$, there is an integer $N_0(c)$ so that

\[
q_c^{N+1}=\sum_j s_j^2,\qquad
s_j\in H^0(S,H^{N+1}),\quad N\ge N_0(c).
\]

Choosing $N$ even yields $m=N+1$ odd. The equality lies in $H^0(S,H^{2m})$; no degree has been halved incorrectly. These are real vector spaces and real sections on an \(\mathbb R\)-scheme. No complex or Hermitian notion of squares is substituted. The source has no remaining auxiliary factor in this identity. It permits all large $N$, so every sufficiently large odd $m$ follows, with parameter-dependent threshold. Merely producing large even powers would be vacuous; the actual quantifier excludes that failure.

These checks validate principal PROOF lines 80–93.

### 4. All square roots lift, with no saturation or denominator gap

The nonzero cubic $G$ is a nonzerodivisor on projective space. Its ideal sheaf gives, after an arbitrary integer twist $t$,

\[
0\to\mathcal O_{\mathbb P^3}(t-3)
\xrightarrow{G}\mathcal O_{\mathbb P^3}(t)
\to i_*\mathcal O_S(t)\to0.
\]

The checked cohomology formula gives $H^1(\mathbb P^3,\mathcal O(t-3))=0$ for every $t$. The global-section sequence therefore gives both surjectivity and kernel:

\[
H^0(S,\mathcal O_S(t))\cong R_t/G R_{t-3},\qquad t\ge0,
\]

with $R_u=0$ for $u<0$. Apply it at $t=m$ to lift every $s_j$ to a real homogeneous $H_j\in R_m$, and at $t=2m$ to conclude

\[
q_c^m-\sum_j H_j^2=G K,\qquad K\in R_{2m-3}.
\]

This is a polynomial equality. In particular, lifting only the roots without checking the second kernel would be incomplete; the proof explicitly checks both. No normality, projective normality, normalization map, resolution, rational section, eventual-only lifting assertion, or clearing of denominators is needed.

Independent exact reconstruction of the all-twist vanishing is supplied computationally by the 16 possible negative supports in the degree-weighted standard Čech complex. Each monomial weight contributes the same finite complex for its negative support; every such complex has zero first cohomology. This universal reduction, together with the exact rational ranks in `CHECK_RESULTS.json`, checks all twists rather than a bounded list of twist values. It agrees with the inspected primary proof.

These checks validate principal PROOF lines 97–127.

### 5. The substitution transfers the exact identity at the base points too

Define the polynomial algebra map

\[
\Phi(A,B,C,D)=(x^2y,xy^2,z^3,xyz).
\]

Directly, \(\Phi(G)=x^3y^3z^3-(xyz)^3=0\), and

\[
\Phi(q_c)=x^4y^2+x^2y^4+z^6-cx^2y^2z^2=M_c.
\]

Applying this homomorphism to the preceding polynomial equality gives

\[
M_c^m=\sum_j\Phi(H_j)^2
\]

in \(\mathbb R[x,y,z]\). Every \(\Phi(H_j)\) is homogeneous of degree $3m$, unless zero. Dehomogenization $z=1$ is another polynomial homomorphism and gives exactly $f_c^m$. There is no multiplier, denominator, scalar correction, or change to the target coefficient family.

The common zero locus of the four substitution forms in \(\mathbb P^2\) is exactly \([1:0:0],[0:1:0]\): $z^3=0$ implies $z=0$, and the remaining two forms force $xy=0$. So the projective map is indeed undefined there. The proof never uses a global morphism or an illicit section pullback across these points. Polynomial substitution sends a polynomial equality to an equality everywhere; at either base point all positive-degree substituted roots and $M_c^m$ vanish. This is why the two persistent zeros of $M_c$ do not contradict positivity of $q_c$ on the surface.

A separate algebraic check makes the mechanism particularly transparent. Two source monomials have identical image exponents exactly when their exponent difference satisfies

\[
2u+v+w=0,\quad u+2v+w=0,\quad3r+w=0.
\]

Hence \((u,v,r,w)=n(1,1,1,-3)\). Reducing $D^3$ to $ABC$ therefore gives unique image-distinct normal monomials with $D$-exponent below three. This independently confirms the substitution has precisely the expected cubic relation. The proof needs only \(\Phi(G)=0\), so this stronger check does not conceal an additional assumption.

These checks validate principal PROOF lines 131–157.

### 6. Limit passage and quantifier order

The original question supplies \(\{c:f_c^{2k+1}\text{ SOS}\}=(-\infty,c_k]\). For each fixed $c<3$, the proof gives an integer $K(c)$ such that $c\le c_k$ whenever $k\ge K(c)$. Consequently \(\liminf_k c_k\ge c\) for every $c<3$, hence the liminf is at least three. For $c>3$, $f_c(1,1)=3-c<0$, so no odd power can be SOS; thus every $c_k\le3$. The two bounds force the limit three.

There is no exchange of \(\forall c\,\exists K(c)\) with \(\exists K\,\forall c\). A second independent tail argument is purely algebraic: if one odd power $f_c^m=\sum h_j^2$ is known, then for every larger odd $m'$, \(f_c^{m'}=\sum(h_jf_c^{(m'-m)/2})^2\). Neither argument asserts an odd SOS power at $c=3$, a uniform exponent, a rate, or an effective certificate. The interval property is explicitly present on the checked original printed p.780, so using it is not circular reliance on the sought limit.

These checks validate principal PROOF lines 161–179.

## Reproducible checks and attempted falsifications

Run `python3 verify_geometry.py` in this review directory. The independent, dependency-free checker uses exact integer and rational arithmetic, explicit exceptions rather than removable assertions, and records its summary in `CHECK_RESULTS.json`. Under Python 3.14.6 the ordinary and `-O` runs gave byte-identical results:

| Interface | Checked result |
|---|---|
| All 16 Čech negative-support types | $H^1=0$; differential squared is zero; exact cohomology dimensions |
| Source degrees 0–36 | 91,390 monomials; all collisions are generated by $ABC=D^3$; expected hypersurface Hilbert function |
| Real signed torus | 9,600 exact samples satisfy the cubic and strict bound for parameters through 2.999999 |
| Full coordinate boundary sample | 756 exact cases have positive section value |
| Parity and grading | Source section degrees and cubic substitution degrees agree |
| Invalid-shortcut controls | 10 explicit refutations, including both projective base points |

There were 335,180 explicit checked requirements. These numbers are supplementary evidence about vulnerable interfaces, not a numerical proof of existence of any SOS roots. The universal positivity, density, lifting and transfer arguments above are the proof; Scheiderer's theorem supplies existence.

The falsifications reject extending strictness to $c=3$, accepting an above-endpoint odd power, treating an even-power SOS as evidence about the base, selecting odd $N$, applying positive-definite projective-space SOS directly to $M_c$, claiming the substitution is a projective morphism, changing the cubic coefficient, deleting the target parameter term, or changing the degree of the $D$ substitution. Each attempted shortcut fails while the actual route survives.

## Decision and remaining boundaries

The strongest verified target-specific result is exactly the universal statement in the first paragraph and its threshold limit. No central mathematical gap remains in the essential geometric argument, relative to the imported published theorem. All six approach interfaces above are verified; none transfers the difficulty to an unsupported equivalent claim. No repair is requested.

Historical full-prior-answer status, the separate mixed-exponent proof, the optional appendix, effective exponents, endpoint stubbornness proofs, and a formal proof-assistant implementation remain outside this assigned geometric audit. No statement here upgrades an unrefereed derivation to external human peer review. No external communication or Git/index/ref/remote/PR/publication/tracker mutation was performed by this review.
