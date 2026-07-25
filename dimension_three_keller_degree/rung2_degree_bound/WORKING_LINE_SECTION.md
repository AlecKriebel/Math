# Working lemma: generic-line defects of a Keller counterexample

**Status:** proof audited; priority audit remains open.  This is a working
theorem, not yet a completed artifact and not peer reviewed.

**Recorded:** 2026-07-24T23:00:00Z.

This file distinguishes total polynomial degree \(D\), generic field degree
\(\delta\), and degree \(s\) of the reduced nonproperness hypersurface.

## 1. Setup

Let
\[
F:\mathbb A^3_{\mathbb C}\longrightarrow\mathbb A^3_{\mathbb C}
\]
be a Keller counterexample.  Write
\[
D=\max_i\deg F_i,\qquad
\delta=[\mathbb C(x_1,x_2,x_3):\mathbb C(F_1,F_2,F_3)].
\]
Let \(S_F\) be the Jelonek nonproperness hypersurface, with its reduced
structure, and set
\[
s=\deg S_F.
\]

After a generic linear change in the target, all three coordinate
polynomials have degree exactly \(D\).  Choose a target affine line
\(\ell\simeq\mathbb A^1\) in a simultaneous genericity open set so that:

1. its projective closure avoids \(S_F\) at infinity and it meets \(S_F\)
   transversely in \(s\) distinct smooth affine points \(t_1,\ldots,t_s\);
2. it avoids the omitted-value set
   \(\mathbb A^3\setminus F(\mathbb A^3)\), whose codimension is at least two;
3. \(C=F^{-1}(\ell)\) is smooth and irreducible;
4. on a resolution of the compactified graph, the boundary meets the
   base-changed line over each \(t_i\).

Here is the missing genericity justification.  The basepoint-free mobile
system
\[
\Lambda=\mathbb P\langle1,F_1,F_2,F_3\rangle
\]
has three-dimensional image.  Bertini irreducibility gives an irreducible
general first member.  Its restricted system has two-dimensional image,
because it dominates the corresponding target hyperplane, so a second
application gives an irreducible curve \(C\).  This is the mobile-system
form of Bertini; see Jouanolou, *Théorèmes de Bertini et applications*,
Section 6.10, especially 6.10.3.  Since \(F\) is étale, its base change
\(C\to\ell\) is étale, so \(C\) is also smooth.

For item 4, resolve the compactified graph to a smooth threefold
\(\widetilde X\) on which the rational extension of \(F\) is a morphism.
Every irreducible component of \(S_F\) is dominated by a boundary divisor.
Over a dense open of that component the divisor map is finite.  Choose
\(\ell\) so that its transverse intersection points lie in all these dense
opens and avoid the images of lower-dimensional exceptional strata.  The
base-changed curve therefore contains a boundary point over each \(t_i\),
and contains no curve component wholly in the boundary.  Each such point is
a puncture of the completion of the affine curve.

Let
\[
R:C\longrightarrow\ell\simeq\mathbb A^1
\]
be the restriction.  Let \(\bar C\) be the smooth projective completion of
\(C\), let \(g=g(\bar C)\), and let
\[
r=\#(\bar C\setminus C).
\]
For \(t_i\in\ell\cap S_F\), define
\[
n_i=\#F^{-1}(t_i),\qquad
\kappa_i=\delta-n_i,\qquad
K=\sum_{i=1}^s\kappa_i.
\]
Because the line avoids the omitted set, and because a point of \(S_F\) has
strictly fewer than \(\delta\) affine preimages for an étale map,
\[
1\le n_i\le\delta-1,\qquad
1\le\kappa_i\le\delta-1.
\tag{1}
\]

## 2. Exact defect identity

### Candidate Lemma 1

With the genericity conditions above,
\[
\boxed{K=2g-2+\delta+r.}
\tag{2}
\]

There are two independent derivations.

### Euler-characteristic derivation

Over
\[
\ell^\circ=\ell\setminus\{t_1,\ldots,t_s\}
\]
the map is a finite étale cover of degree \(\delta\).  Hence
\[
\chi\!\left(R^{-1}(\ell^\circ)\right)
=\delta\chi(\ell^\circ)=\delta(1-s).
\]
Adding the affine exceptional fibres gives
\[
\chi(C)
=\delta(1-s)+\sum_{i=1}^s n_i
=\delta(1-s)+s\delta-K
=\delta-K.
\]
On the other hand, a smooth irreducible affine curve with projective genus
\(g\) and \(r\) punctures has
\[
\chi(C)=2-2g-r.
\]
Equating the two expressions proves (2).

### Riemann--Hurwitz derivation

Extend \(R\) to
\[
\bar R:\bar C\longrightarrow\mathbb P^1.
\]
There is no ramification on \(C\).  If \(r_f\) boundary points map to finite
values and \(r_\infty\) lie over infinity, then \(r=r_f+r_\infty\).  Exact
fibre accounting gives
\[
\kappa_i
=\sum_{\substack{p\in\bar C\setminus C\\ \bar R(p)=t_i}}e_p.
\]
Thus finite boundary ramification contributes \(K-r_f\), while ramification
over infinity contributes \(\delta-r_\infty\).  Riemann--Hurwitz gives
\[
2g-2=-2\delta+(K-r_f)+(\delta-r_\infty),
\]
which is again (2).

The use of \(\sum e_p\), rather than \(\sum(e_p-1)\), in the definition of
the fibre defect is essential: a finite nonproper puncture can be
unramified.

## 3. Universal numerical consequences

Every \(t_i\) is detected by at least one finite boundary puncture and there
is at least one puncture above infinity.  Therefore
\[
r\ge s+1.
\tag{3}
\]
Combining (1)--(3) yields the sharper sandwich
\[
\boxed{2g+\delta+s-1\le K\le s(\delta-1),}
\]
or
\[
\boxed{2g\le (s-1)\delta-2s+1.}
\tag{4}
\]

In particular, \(s=1\) is impossible.  This conclusion is already covered by
Nollet--Xavier's 2007 theorem: a hyperplane satisfies their normal-crossing
and transversality hypotheses, forcing the cover degree to be one.  No
novelty is claimed for
\[
s\ge2.
\tag{5}
\]

The affine curve \(C\) is cut out by two equations of degree at most \(D\).
Bézout bounds the degree of its projective closure by \(D^2\), and every
normalization branch at infinity contributes positive intersection
multiplicity.  Hence
\[
r\le D^2.
\tag{6}
\]
Equations (3) and (6) imply
\[
s\le D^2-1.
\tag{7}
\]

Jelonek's 1993 degree estimate, after making all component degrees equal to
\(D\), is
\[
s\le\frac{D^3-\delta}{D}.
\tag{8}
\]
Using (5) in (8) gives
\[
\boxed{\delta\le D^3-2D.}
\tag{9}
\]
Campbell--Razar--Wright separately gives \(\delta\ge3\).

## 4. The total-degree-four table

For a hypothetical total-degree-four counterexample, (5), (7), (8), and
(9) give
\[
\boxed{3\le\delta\le56}
\tag{10}
\]
and
\[
\boxed{
2\le s\le
\min\left\{15,\left\lfloor\frac{64-\delta}{4}\right\rfloor\right\}.
}
\tag{11}
\]
The generic-line genus obeys
\[
\boxed{
g\le
\left\lfloor
\frac{s(\delta-2)-\delta+1}{2}
\right\rfloor.
}
\tag{12}
\]

## 5. Singularities at infinity in the complete-intersection case

Let \(H_U,H_V\) be the leading quartics of the two equations defining the
generic line preimage.

If
\[
\gcd(H_U,H_V)\ne1,
\]
the homogenized intersection has a curve component in the plane at infinity;
the affine curve is residual and the \((4,4)\) arithmetic-genus formula
cannot be applied directly.

If
\[
\gcd(H_U,H_V)=1,
\]
the projective intersection has no curve component at infinity.  It is a
Cohen--Macaulay, hence unmixed, complete intersection; its affine open is
the smooth integral curve \(C\), and generic reducedness plus unmixedness
rules out a nilpotent structure supported only at infinity.  Thus it is the
integral projective closure of \(C\), of type \((4,4)\).  Its arithmetic
genus is
\[
p_a
=1+\frac{4\cdot4(4+4-4)}2
=33.
\]
The affine curve is smooth, so every singularity is at infinity.  If
\(\Delta_\infty\) is the total delta invariant there, then
\[
g=33-\Delta_\infty.
\]
Consequently (12) becomes
\[
\boxed{
\Delta_\infty\ge
\max\left\{0,
\left\lceil\frac{65+\delta+2s-s\delta}{2}\right\rceil
\right\}.
}
\tag{13}
\]

Using the largest \(s\) allowed by (11) gives:

| \(\delta\) | \(s_{\max}\) | \(g_{\max}\) | \(\Delta_{\infty,\min}\) |
|---:|---:|---:|---:|
| 3 | 15 | 6 | 27 |
| 4 | 15 | 13 | 20 |
| 5 | 14 | 19 | 14 |
| 6 | 14 | 25 | 8 |
| 7 | 14 | 32 | 1 |

Thus a total-degree-four, generic-degree-three counterexample must either
have a common leading-form curve at infinity or lose at least \(27\) units
of arithmetic genus through singularities at infinity.

## 6. Extremal branch data

If
\[
(s,\delta)=(2,3),
\]
then every inequality above is an equality:
\[
g=0,\qquad r=3,\qquad K=4.
\]
There is one boundary puncture over each of the two finite nonproper values,
each of local degree \(2\), and one puncture over infinity, of local degree
\(3\).  Each finite exceptional fibre contains one affine point.  The
branch-cycle types are
\[
(2),\quad(2),\quad(3),
\]
and generate \(S_3\).

## 7. Priority and audit status

- Z. Jelonek, *The set of points at which a polynomial map is not proper*,
  Ann. Polon. Math. 58 (1993), 259--266, gives (8).
- S. Nollet and F. Xavier, *On Kulikov's problem*, Arch. Math. 89 (2007),
  385--389, DOI 10.1007/s00013-007-2244-x, already excludes the hyperplane
  case underlying (5).
- The withdrawn arXiv:2011.03472 must not be used as a theorem source.
- Searches through 2026-07-24T23:00:00Z did not locate (2), (4), or the
  quartic infinity table in the Keller-map literature.  This is
  source-specific evidence, not a guarantee of worldwide priority.
- Independent adversarial review checked connectedness, the two Bertini
  steps, boundary detection on a resolved graph, and complete-intersection
  integrality.  It also rejected a false proposed estimate
  \(K\le64-\delta\): cancellation between sections can make finite boundary
  ramification arbitrarily larger than their common base order.
- The proof is now internally complete.  Promotion to a release still
  requires a broader literature audit and a second independent source-level
  check of every cited theorem.
