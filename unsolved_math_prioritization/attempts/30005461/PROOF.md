# The Motzkin odd-power thresholds tend to 3

Target: problem 30005461 / OWR-12697710-007, Motzkin threshold clause.
Date: 10 October 2026 (UTC).

## Result and credit

For

\[
f_c(x,y)=x^4y^2+x^2y^4+1-cx^2y^2,
\]

**every real parameter \(c<3\) has an odd sum-of-squares power. In fact, all sufficiently large odd powers of \(f_c\) are sums of squares. Consequently \(\lim_{k\to\infty}c_k=3\).**

The proof below is a direct application of Claus Scheiderer's published projective Positivstellensatz. It does not depend on the 2026 preprint *Stubborn Polynomials*, resolution of singularities, or a weak Del Pezzo classification. It is not an elementary explicit SOS certificate: existence of the exponent and of the square roots is supplied by Scheiderer's theorem. No bound on the exponent or rate of convergence is asserted. No priority or novelty claim is made for this application.

The other clause of the original bundled problem has an affirmative answer: for arbitrary real polynomials \(p,q\) and nonnegative integers \(i,j\), if \(p^{2i+1}\) and \(q^{2j+1}\) are SOS, then \((p+q)^{2i+2j+1}\) is SOS. This is the published Blekherman--Kozhasov--Reznick mixed-exponent theorem (Forum of Mathematics, Sigma 14 (2026), e65, [Theorem 5.3](https://doi.org/10.1017/fms.2026.10221); arXiv:2407.21779v1, Theorem 44). Its ingredient is credited there to Iosif Pinelis. That result, including the two indexing/display corrections documented in [CREDITED_MIXED_EXPONENT_PROOF.md](CREDITED_MIXED_EXPONENT_PROOF.md), retains its existing authorship and is not rediscovered here.

## 1. The published input and its exact scope

We use the unconstrained case, Corollary 4.2, of C. Scheiderer, *A Positivstellensatz for projective real varieties*, Manuscripta Mathematica 138 (2012), 73--88, DOI [10.1007/s00229-011-0484-3](https://doi.org/10.1007/s00229-011-0484-3). In paraphrase:

Let \(X\) be a reduced projective real scheme, with no irreducible component of dimension one and with Zariski-dense real points. If \(L,M\) are invertible sheaves, \(M\) is ample, and \(f\in H^0(X,L^{\otimes2})\), \(g\in H^0(X,M^{\otimes2})\) are strictly positive at every real point, then for every sufficiently large integer \(N\), \(fg^N\) is a sum of squares of global sections of \(L\otimes M^{\otimes N}\).

The full statement and proof of Theorem 4.1, its Corollary 4.2, and the sign convention in Section 2.4--2.5 were inspected in the [author's manuscript](https://www.math.uni-konstanz.de/~scheider/preprints/ppss.pdf), specifically PDF pages 9--11 and page 4. The theorem and corollary statements on pages 9 and 11 were also visually inspected. The publisher's abstract independently states exactly the unconstrained result used here; its record confirms online publication on 6 August 2011 and issue publication in May 2012. The author's PDF is dated 5 April 2011 and has 14 pages; it is not represented as the publisher's 16-page typeset PDF.

There is no smoothness assumption in this result. In particular, real singular points do not prevent its application when the section is strictly positive there. We do not use its different nonnegative-section extension for nonsingular surfaces.

## 2. A cubic surface with a strictly positive quadratic section

Work over \(\mathbb R\). Put

\[
G=ABC-D^3,\qquad S=V(G)\subset\mathbb P^3_{\mathbb R},
\qquad q_c=A^2+B^2+C^2-cD^2.
\]

### Scheme and density hypotheses

The polynomial \(G\) is irreducible: as a polynomial in \(C\) over the unique-factorization domain \(\mathbb R[A,B,D]\), it is primitive, since \(\gcd(AB,D^3)=1\), and is linear and nonconstant over its fraction field. Gauss's lemma therefore gives irreducibility in \(\mathbb R[A,B,C,D]\). Irreducibles are prime in that polynomial UFD. Thus \(S\) is an integral, in particular reduced, projective surface, with its single irreducible component of dimension two.

The nonempty open chart \(D\ne0\) is, after setting \(D=1\), the surface \(ABC=1\). Its coordinate ring is

\[
\mathbb R[A,B,C]/(ABC-1)\simeq\mathbb R[A^{\pm1},B^{\pm1}],
\]

where \(C=(AB)^{-1}\). Its real points are parametrized by

\[
(a,b)\in(\mathbb R^*)^2\longmapsto[a:b:(ab)^{-1}:1].
\]

These points are Zariski dense: a Laurent polynomial vanishing for every nonzero real \(a,b\) becomes, on multiplication by a monomial, a polynomial vanishing on the open set \((\mathbb R^*)^2\); fixing one variable and then the other shows that polynomial is zero. The open chart is dense in integral \(S\), so \(S(\mathbb R)\) is Zariski dense in \(S\). This directly verifies the density hypothesis without an assumption about image-surjectivity of a rational map.

Let \(\mathcal H=\mathcal O_S(1)\). It is an invertible very ample sheaf, being the restriction of the hyperplane bundle of \(\mathbb P^3\). This remains true at the singularities of \(S\). The quadratic \(q_c\) is a section of \(\mathcal H^{\otimes2}\).

### Positivity, including all sign patterns and the boundary

Let \([A:B:C:D]\) be any real projective point of \(S\). AM--GM on the three nonnegative real numbers \(A^2,B^2,C^2\) gives

\[
A^2+B^2+C^2\ \ge\ 3(A^2B^2C^2)^{1/3}
=3|ABC|^{2/3}=3D^2.
\]

The last equality uses \(ABC=D^3\), with absolute values, and therefore applies also when \(A,B,C\) have mixed signs or \(D<0\). If \(D\ne0\) and \(c<3\), then

\[
q_c\ge(3-c)D^2>0.
\]

If \(D=0\), then \(q_c=A^2+B^2+C^2>0\), because a projective point has at least one nonzero coordinate. Consequently \(q_c\) is strictly positive everywhere on \(S(\mathbb R)\), including every singular point.

This is positivity as a section of a square line bundle: on any standard coordinate chart with nonzero coordinate \(T\), the local representative is \(q_c/T^2\), which has the same sign. Thus it is precisely the positivity required by Scheiderer, not merely positivity on an affine subset.

## 3. Produce an odd SOS power on the surface

Apply Corollary 4.2 with

\[
X=S,\qquad L=M=\mathcal H,\qquad f=g=q_c.
\]

All hypotheses have just been checked. There exists an integer \(N_0(c)\) such that, for every \(N\ge N_0(c)\),

\[
q_c^{N+1}=\sum_j s_j^2,
\qquad s_j\in H^0(S,\mathcal O_S(N+1)).
\]

Choose \(N\) even, and put \(m=N+1\). Then \(m\) is an odd positive integer and the displayed identity has degree \(2m\) as a section of \(\mathcal O_S(2m)\). The theorem permits all sufficiently large \(N\), not only odd \(N\); this is essential, since even powers of \(q_c\) alone would give no information.

## 4. Lift the square roots to homogeneous polynomials

For every integer \(t\), the cubic hypersurface exact sequence, twisted by \(t\), is

\[
0\longrightarrow\mathcal O_{\mathbb P^3}(t-3)
\mathrel{\mathop{\longrightarrow}^{\cdot G}}
\mathcal O_{\mathbb P^3}(t)
\longrightarrow i_*\mathcal O_S(t)\longrightarrow0.
\]

The usual cohomology of projective space gives

\[
H^1(\mathbb P^3_{\mathbb R},\mathcal O(t-3))=0
\quad\text{for every integer }t.
\]

For a primary reference with proof, see [Stacks Project, Lemma 30.8.1](https://stacks.math.columbia.edu/tag/01XS). Its formula vanishes in every intermediate cohomological degree \(0<q<3\), for all twists. Taking global sections of the exact sequence thus proves, for every \(t\ge0\),

\[
H^0(S,\mathcal O_S(t))
\simeq
\mathbb R[A,B,C,D]_t\big/G\mathbb R[A,B,C,D]_{t-3}.
\]

Negative polynomial degree is interpreted as the zero vector space. In particular each \(s_j\) lifts to a real homogeneous polynomial \(H_j\) of degree \(m\). Applying the same exact sequence in degree \(2m\) shows that the section equality is the polynomial congruence

\[
q_c^m-\sum_jH_j^2\in(G).
\]

Thus no rational square roots, local-only sections or denominators are introduced. Normality or projective normality of \(S\) need not be assumed: the displayed exact sequence establishes exactly the surjectivity and kernel used here.

## 5. Substitute back to the exact Motzkin family

Use the ring homomorphism

\[
\Phi:\mathbb R[A,B,C,D]\longrightarrow\mathbb R[x,y,z],
\quad(A,B,C,D)\longmapsto(x^2y,xy^2,z^3,xyz).
\]

It has the two exact identities

\[
\Phi(G)=x^3y^3z^3-(xyz)^3=0,
\]
\[
\Phi(q_c)=x^4y^2+x^2y^4+z^6-cx^2y^2z^2=:M_c.
\]

Therefore the polynomial congruence gives

\[
M_c^m=\sum_j H_j(x^2y,xy^2,z^3,xyz)^2.
\]

Each square root is homogeneous of degree \(3m\), so its square has the required degree \(6m\). This is an SOS of the exact odd power \(M_c^m\), with no additional factor. Setting \(z=1\) gives an SOS of \(f_c^m\) in \(\mathbb R[x,y]\).

The four cubic substitution forms have base points in the projective plane. That causes no issue: we substitute a polynomial identity through a ring homomorphism. We never claim the cubics define a globally defined projective morphism or pull back a section across an undefined point. The resulting identity is valid at all \((x,y,z)\), including the base points.

The same argument works for every sufficiently large even \(N\), hence for every sufficiently large odd \(m\). Alternatively, once one odd power \(f_c^m\) is SOS, every larger odd power is obtained by multiplying it by the square \((f_c^{(m'-m)/2})^2\).

## 6. Take the threshold limit

Let \(c_k\) be the thresholds from the original question, so that

\[
\{c:f_c^{2k+1}\text{ is SOS}\}=(-\infty,c_k].
\]

For every fixed \(c<3\), the result just proved gives \(f_c^{2k+1}\) SOS for all sufficiently large \(k\). Therefore \(c_k\ge c\) eventually, and

\[
\liminf_{k\to\infty}c_k\ge c\qquad(c<3).
\]

On the other hand, if \(c>3\), then \(f_c(1,1)=3-c<0\), so every odd power is negative there and cannot be SOS. Hence \(c_k\le3\) for every \(k\). Taking \(c\uparrow3\) now proves

\[
\boxed{\displaystyle\lim_{k\to\infty}c_k=3.}
\]

The proof does not assume an SOS odd power at \(c=3\): indeed \(q_3\) is zero at \([1:1:1:1]\), so the strict-positivity argument intentionally stops below that endpoint. Nor is a uniform exponent for all \(c<3\) needed. The interval property of the thresholds is supplied in the question and established in Blekherman--Kozhasov--Reznick, published Theorem 6.3. Monotonicity also follows by multiplying an SOS odd power by \(f_c^2\), but is not needed for the liminf/limsup argument.

## Verification boundary

This is a complete target-specific derivation relative to Scheiderer's published Positivstellensatz and standard projective-space cohomology. Those results are expressly imported, not claimed to have been formally re-proved here. The applicability hypotheses, section-lifting argument, parity, exact pullback, and limiting argument are supplied in full. Historical exact symbolic checks tested transcription and negative controls; they are not a replacement for the proof or a formal proof-assistant certification. The independent [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the full two-clause target without a material correction. This AI-assisted manuscript and audit are unrefereed; acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.
