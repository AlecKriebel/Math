# Real rational maps with only real periodic points have nonempty interior

**Status recommendation: already solved in the cited literature. No new discovery is claimed.** For every degree $d\ge2$, the locus in the exact question has nonempty interior in the full real degree-$d$ rational-map space. Kozhasov–Kummer explicitly proved this in April 2020. The August 2026 imported assessment saying that only lower-dimensional families were known is incorrect.

Checked 30 September 2026. Model: gpt-6-astra, xhigh. This is verification and exposition of a known result, with separate source/mathematical review required before publication of this correction.

## 1 Exact source and version history

The original contribution is Khazhgali Kozhasov, *On morphisms of the projective line with only real periodic points*, in [Oberwolfach Report 12/2020](https://ems.press/content/serial-article-files/46848), printed pp. 668–669. The workshop took place on 1–7 March 2020. Question 1 asks for existence in every degree $d\ge2$ and the contribution answers it using Chebyshev polynomials. Question 2, on p. 669, asks whether the locus has nonempty interior in the entire real space of degree-$d$ morphisms. It is this second question that the selected record retains.

The subsequent paper of Khazhgali Kozhasov and Mario Kummer, [*Rational functions with only real periodic points*, arXiv:2004.10003v1](https://arxiv.org/pdf/2004.10003v1), submitted 21 April 2020, resolves that question explicitly:

- Its introduction, p. 1, states nonempty interior in the $(2d+1)$-dimensional real rational-map space.
- **Theorem 2, p. 2**, asserts the required nonempty open subset for every degree.
- Its proof is in Section 2.2, p. 6, using strict interlacing and positive coefficients.

The [current v2](https://arxiv.org/pdf/2004.10003), revised 27 October 2020, retains the same conclusion in **Example 1, p. 3**, and the proof of Theorem 3, p. 6. Example 1 uses strictly interlacing polynomials with an attracting real fixed point. Its wording mentions fixed points in one sentence, but its explicit conclusion is interior membership in the all-periodic-points locus; Theorem 2 and Lemma 9 establish the all-period assertion. We do not replace periodic points by fixed points.

The current arXiv record has no verified journal reference or withdrawal notice. This package therefore describes an existing **preprint result**, not a newly discovered theorem or a verified journal publication. The nonempty-interior assertion occurs in both versions, so it is not an obsolete claim present only in the first draft.

The same v1 also constructs a separate lower-dimensional family related to Chebyshev polynomials. That family does not exhaust the locus and does not negate Theorem 2's ambient open subset. The Hermite-polynomial question and the higher-projective-dimensional question are separate and are not resolved by this package.

## 2 Ambient space and an explicit open family

Let $\operatorname{Rat}_d(\mathbb R)$ be the open subset of $\mathbb P^{2d+1}(\mathbb R)$ represented by coprime homogeneous pairs $(P,Q)$ of degree $d$. This is the space of morphisms in the source, before quotienting by conjugacy. Work in the coefficient chart in which the leading coefficient of $q(z)=Q(z,1)$ is $1$.

As in the known construction, start with

$$p_d(z)=\prod_{j=1}^{d}(z+2j-1),\qquad q_d(z)=\prod_{j=1}^{d}(z+2j),\qquad f_d=p_d/q_d.$$

The zeros are negative, simple, and strictly interlacing, and all coefficients are positive. These are strict conditions: sufficiently small real coefficient perturbations preserve the simple real roots, their strict order, their negativity, and coefficient positivity. Coprimality persists as well. Thus there is a nonempty open neighborhood $U_d$ of $f_d$ in the entire $(2d+1)$-dimensional chart where both numerator and denominator have degree $d$, positive coefficients, and strictly interlacing simple real zeros.

This is ambient openness, not merely relative openness in a $d$-parameter root family, a polynomial subspace, or a subspace fixing infinity. In particular, both degree-$d$ leading coefficients remain nonzero throughout the chosen chart neighborhood.

## 3 Verification that every map in the open family has only real periodic points

The following details unpack the known positive-coefficient/interlacing proof. They give an all-period argument; the finite checks below are not its foundation.

### Interlacing and real fibers

For $f=p/q\in U_d$, let $b_1<\cdots<b_d$ be the poles. In the partial fraction expansion

$$f(z)=a+\sum_{j=1}^{d}\frac{A_j}{z-b_j},$$

strict interlacing implies that all nonzero residues $A_j=p(b_j)/q'(b_j)$ have the same sign. Consequently, for $z=x+iy$ with $y\ne0$,

$$\operatorname{Im}f(z)=-y\sum_{j=1}^{d}\frac{A_j}{(x-b_j)^2+y^2}\ne0.$$

Thus $f$ is real fibered: precisely the real projective points map to real projective points. Also, it has no critical point on the real projective line. At a finite nonpole,

$$f'(x)=-\sum_j\frac{A_j}{(x-b_j)^2}\ne0.$$

At a pole use the target coordinate $1/f$, whose derivative there is $1/A_j\ne0$. At infinity use the domain coordinate $w=1/z$; the coefficient of $w$ in $f(1/w)$ is $\sum_jA_j\ne0$. These cover all real points.

Both properties persist under composition: a composite is real fibered, and its differential at a real point is a composite of nonzero one-dimensional differentials.

### Positive coefficients persist under every iterate

Write the homogeneous representatives as

$$P(X,Y)=\sum_{j=0}^d p_jX^jY^{d-j},\qquad Q(X,Y)=\sum_{j=0}^d q_jX^jY^{d-j},$$

with every $p_j,q_j>0$. Homogeneous substitution gives positive coefficients for both members of every iterated pair $(P_n,Q_n)$. No common factor is introduced: a common projective zero would map under the preceding iterate to a common zero of $(P,Q)$, which does not exist. Hence the $n$th iterate $g=f^n=p_n/q_n$ has degree $e=d^n$, and both affine polynomials $p_n,q_n$ have degree $e$ with positive leading and constant coefficients.

The real-fibered and unramified properties imply that the $e$ poles of $g$ are distinct real points. They are finite because $q_n$ has degree $e$, and negative because it has positive coefficients. Between consecutive poles, $g'$ is nonzero, and the limits at the two simple poles have opposite infinite signs. Thus $g(x)-x$ has a zero in each of the $e-1$ bounded intervals between poles.

There is one more real fixed point on the positive axis: $g(0)>0$, whereas $g(x)-x\to-\infty$ as $x\to+\infty$, since $\deg p_n=\deg q_n$. Therefore the real polynomial

$$p_n(z)-zq_n(z)$$

of degree $e+1$ has at least $e$ distinct real roots. Any nonreal roots would occur in a conjugate pair, leaving room for at most $e-1$ real roots counted with multiplicity. This is impossible. All its roots are real. No pole is an extraneous root since $p_n,q_n$ are coprime, and infinity is not fixed by $g$ because its image is finite.

This holds for every $n\ge1$. Hence **all** periodic points of every $f\in U_d$ are real, and

$$\varnothing\ne U_d\subset\mathcal R_d\subset\operatorname{Rat}_d(\mathbb R).$$

This verifies the affirmative answer to the exact nonempty-interior question. The construction and result are credited to Kozhasov–Kummer, not to this investigation.

## 4 Reproduction and disposition

`verify.py` performs modest exact checks of the displayed representatives, coefficient positivity under homogeneous iteration, coprimality, and real-root counts for small degrees and periods. These tests detect normalization or indexing mistakes; the proof for every degree and period is Section 3.

**Recommended disposition:** remove 30004438 from the novel-proof queue as `already_solved`, preserving the source correction and the existing authors' credit. No claim is made that all of $\mathcal R_d$ is open, that every Chebyshev map is an interior point, or that either the Hermite conjecture or the analogous question on higher-dimensional projective space is settled here. Separate review is pending.
