# Hostile geometry and reference audit: cube-component exit

Audit time (UTC): `2026-07-26T08:01:10Z`

## Verdict

The elementary coordinate theorem is **PASS**, including every rank and
pivot boundary:

\[
 f=C+\ell^3+Q_2+L_1\in k[x,y,z],\qquad
 \nabla f\ne0
 \quad\Longrightarrow\quad
 f\text{ is a coordinate},
\]

provided that \(k\) is algebraically closed of characteristic zero,
\(\ell\ne0\), and \(Q_2,L_1\) are homogeneous of degrees two and one.
The containing coordinate automorphism and its inverse can both be chosen
of degree at most three.  A nonzero scalar multiplying \(\ell^3\) is harmless
over \(k\), after absorbing a cube root into \(\ell\).

The target-linear-combination passage is **PASS**.  If a nonzero row
\(\alpha\in(\mathbf C^3)^*\) has
\(\alpha F=C+\ell^3+Q_2+L_1\), one must first choose
\(T\in\operatorname{GL}_3(\mathbf C)\) whose third row is \(\alpha\), set
\(H=TF\), apply the coordinate theorem to \(H_3=\alpha F\), and only then
change source coordinates.  With this explicit ordering, all determinant,
degree, and invertibility statements are valid.

The degree-only corollary

\[
 \deg F=d\le35\quad\Longrightarrow\quad F\in\operatorname{Aut}(\mathbf A^3)
\]

is **PASS conditional on accepting the 2022 Guccione--Guccione--Horruitiner--Valqui
preprint as the plane-degree input**.  Its exact proved safe range is
maximum plane degree \(<108\), not \(\le108\).  Thus
\(3d\le105<108\) for \(d\le35\), whereas \(d=36\) only gives
\(3d\le108\) and is not covered.  No peer-reviewed publication of that
preprint was located in this audit.

The fibrewise-injectivity argument is **PASS**.  The phrase
“Ax--Grothendieck makes the map an automorphism” is mathematically sound
here but suppresses one step: Ax gives surjectivity, while the Keller
(étale) condition upgrades the injective map to an open immersion; a
surjective open immersion is an isomorphism.

No exact prior-art collision with the displayed cube-leading coordinate
criterion was located.  This is **not** a worldwide novelty finding.
Several close but hypothesis-distinct results are listed below, and a
specialist database search remains necessary before making a priority
claim.

## 1. Exact hypotheses and normalization

The theorem needs all of the following.

1. The cubic homogeneous part is a nonzero cube of one linear form.  It is
   not a statement about arbitrary nonsingular cubics.
2. The field is algebraically closed and has characteristic zero.  The
   proof uses diagonalization of a symmetric quadratic form, a nonzero
   coefficient \(3\), and roots of residual quadratics.
3. “Nonsingular” means that the three partial derivatives have no common
   zero.  Over an algebraically closed field this is equivalent to the
   gradient row being unimodular.
4. The constant \(C\) is irrelevant, but should be retained when the
   theorem is applied to a target-linear combination of a map that was not
   translated to the origin.

After an invertible linear source change and a translation of the value of
\(f\), write

\[
 f=p^3+Ap^2+p\,c^ty+\frac12y^tMy+ap+d^ty,\qquad
 y=(q,r)^t,
\]

where \(M=M^t\), \(c,d\in k^2\).  Then

\[
 \nabla_y f=My+cp+d,\qquad
 f_p=3p^2+2Ap+c^ty+a.
\]

The rank of \(M\) gives a division-safe exhaustive atlas.

## 2. Hostile audit of the rank atlas

### Rank two

If \(M\) is invertible, the equations \(\nabla_yf=0\) give

\[
 y=-M^{-1}(cp+d).
\]

After substitution, \(f_p\) is a quadratic in \(p\) with leading
coefficient exactly \(3\), since \(c^ty\) is only linear in \(p\).  It has a
root over \(k\), producing a critical point.  Therefore this rank cannot
occur under the nonsingularity hypothesis.

### Rank one

By congruence in the transverse variables, put

\[
 M=\begin{pmatrix}m&0\\0&0\end{pmatrix},\qquad m\ne0,
\]

and write

\[
 f=p^3+Ap^2+p(c_u u+c_vv)+\frac m2u^2+ap+d_uu+d_vv.
\]

There are exactly three boundary-disjoint cases.

* If \(c_v\ne0\), the equation \(f_v=0\) fixes
  \(p=-d_v/c_v\), then \(f_u=0\) fixes \(u\), and \(f_p=0\)
  fixes \(v\).  This is a critical point.
* If \(c_v=d_v=0\), solve \(f_u=0\) for \(u\).  The residual
  \(f_p\) is again a quadratic in \(p\) with leading coefficient \(3\),
  so it has a root and gives a critical point.
* If \(c_v=0\) and \(d_v\ne0\), then
  \(f=d_vv+R(p,u)\).  The map
  \[
  (p,u,v)\longmapsto(p,u,w=f)
  \]
  is an automorphism, with inverse
  \[
  v=\frac{w-R(p,u)}{d_v}.
  \]
  Both directions have degree at most three.

No division by \(d_v\) occurs on its zero boundary.

For the original symmetric matrix

\[
 M=\begin{pmatrix}m_{qq}&m_{qr}\\m_{qr}&m_{rr}\end{pmatrix},
\]

the pivot atlas is complete: if \(m_{qq}\ne0\), use the null vector
\((-m_{qr},m_{qq})\); if \(m_{qq}=0\) and \(\det M=0\), then
\(m_{qr}=0\), and rank one forces \(m_{rr}\ne0\), with null vector
\((1,0)\).  The remaining all-zero boundary is rank zero.  The values
\(c_v,d_v\) are, up to a common nonzero scalar, the pairings of \(c,d\)
with this null vector, so the three cases are invariant and not artifacts
of diagonalization.

### Rank zero

Now

\[
 f=g(p)+p\,c^ty+d^ty,\qquad g(p)=p^3+Ap^2+ap.
\]

* If \(c,d\) are independent, take \(u=c^ty,\ v=d^ty\).  Then
  \(f=g(p)+pu+v\), and
  \((p,u,v)\mapsto(p,u,f)\) has inverse
  \(v=w-g(p)-pu\).
* If \(c=0,d\ne0\), take \(v=d^ty\) and a complementary linear
  coordinate \(u\).  Then \(f=g(p)+v\), with inverse
  \(v=w-g(p)\).
* If \(c\ne0\) and \(d=\delta c\), set \(p=-\delta\).  The two
  transverse derivatives vanish, and \(y\) can be chosen so that
  \(c^ty=-g'(-\delta)\), making \(f_p=0\).
* If \(c=d=0\), a root of the quadratic \(g'\) is a critical point.

The determinant pivot \(\det[c\ d]\), followed by the honest charts
\(c_1\ne0\), \(c_1=0,c_2\ne0\), and \(c=0\), covers every rank-zero
boundary.  Thus the coordinate cases are exactly the nonsingular cases.
Every displayed coordinate map retains \(p\) as a linear coordinate and
has inverse degree at most three.

## 3. Target-linear-combination passage

Let \(F:\mathbf A^3_{\mathbf C}\to\mathbf A^3_{\mathbf C}\) satisfy
\(\det JF=\kappa\in\mathbf C^\times\), and let
\(\alpha\ne0\) be a target row such that

\[
 f=\alpha F=C+\ell^3+Q_2+L_1.
\]

Choose \(T\in\operatorname{GL}_3(\mathbf C)\) with third row \(\alpha\)
and set \(H=TF\).  Then

\[
 H_3=f,\qquad
 \det JH=(\det T)\kappa\in\mathbf C^\times.
\]

Moreover,

\[
 \nabla f=\alpha JF.
\]

Since right multiplication by the invertible matrix \(JF(x)\) cannot
annihilate a nonzero row, \(\nabla f(x)\ne0\) for every \(x\).  The
coordinate theorem therefore gives an automorphism

\[
 \sigma:\ (x_1,x_2,x_3)\longmapsto(u,v,w=f)
\]

with \(\deg\sigma^{-1}\le3\).  Define

\[
 G=H\circ\sigma^{-1}=(G_1(u,v,w),G_2(u,v,w),w).
\]

This is the correct composition; writing \(F\circ\sigma^{-1}\) without
first replacing \(F\) by \(TF\) loses the claim that the third component
is \(w\).  The determinant and degree transfers are

\[
 \det JG=(\det T)\kappa\det J(\sigma^{-1})\in\mathbf C^\times,
 \qquad
 \deg G_i\le 3d.
\]

Expanding the determinant along the last row gives

\[
 \frac{\partial(G_1,G_2)}{\partial(u,v)}
   =\det JG\in\mathbf C^\times.
\]

Finally, \(G\) being an automorphism implies \(H=G\circ\sigma\) is an
automorphism, and then \(F=T^{-1}H\) is an automorphism.  Thus the target
change is completely reversible.

## 4. Exact plane-degree threshold

For every \(w_0\in\mathbf C\), the specialization

\[
 G_{w_0}:(u,v)\longmapsto
   (G_1(u,v,w_0),G_2(u,v,w_0))
\]

is a plane Keller map of maximum component degree at most \(3d\).

The precise statement of Theorem 2.1 of
J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui,
“Increasing the degree of a possible counterexample to the Jacobian
Conjecture from 100 to 108,”
[arXiv:2204.14178](https://arxiv.org/abs/2204.14178), is that a plane
counterexample must either have maximum degree at least \(125\), or have
degree pair \((72,108)\) or \((108,72)\).  Consequently every plane
Keller map of maximum degree **strictly less than \(108\)** is an
automorphism.

Therefore

\[
 d\le35\quad\Longrightarrow\quad
 \deg G_{w_0}\le3d\le105<108,
\]

so all fibres are automorphisms.  At the next integer,

\[
 d=36\quad\Longrightarrow\quad
 \deg G_{w_0}\le108,
\]

and the unresolved degree pair in the cited theorem prevents a uniform
conclusion.  Hence \(d\le35\) is the exact threshold obtainable from
only the bound \(\deg\sigma^{-1}\le3\) and that plane input.

Moh's older range is inclusive: his result is conventionally stated as
excluding maximum plane degree \(\le100\), not merely \(<100\).  It gives
the fallback \(3d\le100\), hence \(d\le33\).  The stricter wording
\(<100\) is conservative and happens to give the same integer threshold,
but it is not the exact citation.

The \(108\) paper currently appears as a 2022 arXiv v1 preprint; this
audit did not locate a journal publication.  Any theorem statement using
\(d\le35\) should identify that dependency.  If only the older published
Moh input is permitted, state \(d\le33\).

## 5. Fibrewise injectivity and the Ax step

If \(G(a)=G(b)\), equality of the third coordinates gives
\(w(a)=w(b)=w_0\).  Since \(G_{w_0}\) is an automorphism, its first two
coordinates then give \((u(a),v(a))=(u(b),v(b))\).  Hence \(a=b\), so
\(G\) is injective on \(\mathbf C\)-points.

James Ax's original theorem gives surjectivity for an injective
endomorphism of a finite-type variety over an algebraically closed field:
J. Ax, “Injective endomorphisms of varieties and schemes,”
*Pacific J. Math.* **31** (1969), 1--7,
[DOI 10.2140/pjm.1969.31.1](https://doi.org/10.2140/pjm.1969.31.1).

To obtain a polynomial inverse with no shorthand gap, use the Keller
condition.  The morphism \(G\) is étale.  If the off-diagonal part of
\(\mathbf A^3\times_G\mathbf A^3\) were nonempty, it would be a nonempty
finite-type \(\mathbf C\)-scheme and would have a closed
\(\mathbf C\)-point, contradicting pointwise injectivity.  Thus the
diagonal is an isomorphism and \(G\) is universally injective.  A
universally injective étale morphism is an open immersion
([Stacks Project, Theorem 41.14.1, Tag 025G](https://stacks.math.columbia.edu/tag/025G)).
Ax supplies surjectivity, so this open immersion is an isomorphism.

An equivalent repair is to use pointwise injectivity to get a
quasi-finite birational morphism, apply Zariski's Main Theorem and
normality of affine space, then use Ax for surjectivity.

## 6. Prior-art collision audit

### No exact collision located

Searches covered the phrases “unimodular gradient cubic coordinate,”
“nonsingular cubic polynomial three variables coordinate,” “polynomial
submersion \(\mathbf C^3\) degree three,” “cube of a linear form plus
quadratic coordinate,” and literature around variables, affine
fibrations, and low-degree automorphisms.  No source located in this
search states the exact implication

\[
 \nabla(C+\ell^3+Q_2+L_1)\ne0
 \Longrightarrow C+\ell^3+Q_2+L_1
 \text{ is a coordinate},
\]

or the accompanying inverse-degree-three conclusion.

This absence of a search hit is not evidence of worldwide novelty.
MathSciNet and zbMATH full-text/classification searches, and specialist
review of the affine-fibration literature, remain necessary.

### Closest hypothesis-distinct literature

1. A. Vistoli, “The Jacobian conjecture in dimension 3 and degree 3,”
   *J. Pure Appl. Algebra* **142** (1999), 79--89,
   [DOI 10.1016/S0022-4049(98)00040-1](https://doi.org/10.1016/S0022-4049(98)00040-1),
   proves the degree-three, dimension-three Jacobian conjecture.  This
   overlaps when an **entire Keller map** has degree at most three.  It
   does not state that one arbitrary nonsingular cubic component is a
   coordinate, and it does not yield the present higher-degree
   target-component corollary.
2. J. Blanc and I. van Santen, “Automorphisms of the affine 3-space of
   degree 3,” *Indiana Univ. Math. J.* **71** (2022), 857--912,
   [DOI 10.1512/iumj.2022.71.8857](https://doi.org/10.1512/iumj.2022.71.8857),
   classify degree-at-most-three automorphisms and study cubic
   hypersurfaces already known to be \(\mathbf A^2\) and families whose
   hyperplane preimages are \(\mathbf A^2\).  “No critical point” is
   weaker than those fibre hypotheses in general, so this is adjacent,
   not an identified source for the rank lemma.
3. S. Kaliman, “Polynomials with general \(\mathbf C^2\)-fibers are
   variables,” *Pacific J. Math.* **203** (2002), 161--190,
   [DOI 10.2140/pjm.2002.203.161](https://doi.org/10.2140/pjm.2002.203.161),
   is strong variable-polynomial prior art under general-fibre
   \(\mathbf C^2\) hypotheses.  The cube-leading rank proof does not
   assume its fibres are \(\mathbf C^2\); it proves a coordinate directly.
4. N. R. Ribeiro, “Classification at infinity of polynomials of degree 3
   in 3 variables,”
   [arXiv:2201.11026](https://arxiv.org/abs/2201.11026), classifies
   singularities at infinity and studies global fibrations in a restricted
   isolated-at-infinity setting.  No cube-leading coordinate criterion was
   found in its stated results.
5. V. Shpilrain and J.-T. Yu, “Polynomial retracts and the Jacobian
   conjecture,” *Trans. Amer. Math. Soc.* **352** (2000), 477--484,
   [arXiv:math/9701210](https://arxiv.org/abs/math/9701210), is a warning
   against broadening the lemma: a unimodular gradient alone does not
   generally force a polynomial to be a coordinate.  The special
   cube-leading shape is essential.

### Collision verdict

There is no identified theorem collision at the exact hypothesis level.
There is genuine overlap with:

* Vistoli on the subcase where the full Keller map has degree at most
  three;
* Blanc--van Santen and Kaliman after imposing substantially stronger
  affine-plane fibre hypotheses.

Accordingly, the safe claim is “elementary theorem independently proved
here; exact prior source not located,” not “new theorem.”

## 7. Reference list for the external implication chain

* Guccione--Guccione--Horruitiner--Valqui:
  [arXiv:2204.14178](https://arxiv.org/abs/2204.14178), especially
  Theorem 2.1.
* T. T. Moh, “On the Jacobian conjecture and the configurations of
  roots,” *J. Reine Angew. Math.* **340** (1983), 140--212,
  [DOI 10.1515/crll.1983.340.140](https://doi.org/10.1515/crll.1983.340.140).
* James Ax:
  [DOI 10.2140/pjm.1969.31.1](https://doi.org/10.2140/pjm.1969.31.1).
* Étale universally injective implies open immersion:
  [Stacks Project Tag 025G](https://stacks.math.columbia.edu/tag/025G).

No external contact or outreach was made.
