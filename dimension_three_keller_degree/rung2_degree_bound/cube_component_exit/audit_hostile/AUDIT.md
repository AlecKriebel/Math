# Hostile audit: cube-leading submersions

**Verdict:** **PASS.**  No blocking defect or missing rank boundary was
found.

This is an independent audit of the following statement over
\(\mathbb C\).

> If \(f\in\mathbb C[x,y,z]\) has degree at most three, its cubic
> homogeneous part is a nonzero cube of a linear form, and \(\nabla f\)
> never vanishes, then \(f\) is a polynomial coordinate.  It can be
> completed to an automorphism whose inverse has degree at most three.

The proof below was derived before `verify_theorem.py` was read.  The exact
audit certificate uses PARI/GP, not the primary verifier's Python
polynomial class.

## 1. Exhaustive normal form

After a linear change, a scalar rescaling, and removal of the constant
term,
\[
 f=x^3+a x^2+x(by+cz)+q(y,z)+dx+ey+gz,              \tag{1}
\]
where \(q\) is a binary quadratic form.  Its transverse Hessian has rank
\(2,1\), or \(0\).  These ranks are invariant under the remaining linear
changes in \(y,z\), and exhaust all boundaries.

### Rank two

The two equations \(f_y=f_z=0\) have a unique solution
\((y(x),z(x))\) affine-linear in \(x\).  Substitution in \(f_x\) gives a
quadratic in \(x\) whose leading coefficient is exactly \(3\): the terms
\(by(x)+cz(x)\) have degree at most one and cannot cancel \(3x^2\).
Over \(\mathbb C\) this quadratic has a root, producing a critical point.
Thus rank two cannot occur for a submersion.

The PARI certificate performs this solve for a fully symbolic nonsingular
symmetric \(2\times2\) Hessian, retaining its determinant as a denominator.

### Rank one

Diagonalize \(q\) to \(y^2/2\), with \(z\) spanning its kernel.  Then
\[
 f_z=cx+g.
\]

- If \(c\ne0\), solve \(f_z=0\) for \(x\), \(f_y=0\) for \(y\), and
  \(f_x=0\) for \(z\).  This is a critical point.
- If \(c=0=g\), solve \(f_y=0\) for \(y(x)\).  The remaining \(f_x=0\)
  equation is again quadratic with leading coefficient \(3\), so a
  critical point exists.
- Hence a submersion requires \(c=0\) and \(g\ne0\).  In that chart
  \[
  f=gz+h(x,y),
  \]
  and \((x,y,z)\mapsto(x,y,f)\) is triangular, with
  \(z=(f-h)/g\).  Its inverse has degree at most three.

No division by \(c\) was used on the \(c=0\) boundary.

### Rank zero

Now
\[
 f_y=bx+e,\qquad f_z=cx+g.                           \tag{2}
\]

If \((b,c)\ne(0,0)\), the two affine polynomials in (2) have a common root
exactly when
\[
\Delta=bg-ce=0.
\]
On that locus, \(f_x=0\) can be solved using whichever of \(b,c\) is
nonzero, so a critical point exists.  Therefore a submersion has
\(\Delta\ne0\).  The invertible linear change
\[
Y=by+cz,\qquad Z=ey+gz
\]
then gives
\[
f=h(x)+xY+Z.
\]
The automorphism \((x,Y,Z)\mapsto(x,Y,f)\) has inverse
\[
Z=f-h(x)-xY,
\]
of degree at most three.

If \(b=c=0\), absence of a critical point forces
\((e,g)\ne(0,0)\), and a linear transverse change makes \(f=h(x)+Z\).
This is the remaining triangular chart.

The two charts \(b\ne0\) and \(b=0,c\ne0\) were checked separately.  Thus
the proof does not silently divide by \(b\) on its zero locus.

## 2. Conditional consequence for Keller maps

Let \(F:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\) be Keller of
degree at most \(d\), and suppose there is a nonzero target covector
\(\alpha\) for which \(f=\alpha\mathbin{\cdot}F\) is as above.  Extend
\(\alpha\) to an element of \(\mathrm{GL}_3(\mathbb C)\) and apply that
linear target change, putting \(f\) in the third component without
increasing degree.  A row of an everywhere-invertible Jacobian cannot
vanish, so \(f\) is a submersion.  Straighten \(f\) using the
degree-\(\le3\) inverse just constructed.  After this target change,
\[
G=(G_1,G_2,w),\qquad \deg G\le3d.                   \tag{3}
\]
The source automorphism has constant nonzero Jacobian, so
\[
\det\frac{\partial(G_1,G_2)}{\partial(X,Y)}
\in\mathbb C^\times.
\]
For every \(w=c\), the first two components give a plane Keller map of
degree at most \(3d\).

Whenever an established plane Keller theorem covers degree \(3d\), every
fibre is an automorphism.  Equality of two \(G\)-images first gives equal
\(w\), then equality on that plane fibre; hence \(G\) is injective.
Ax--Grothendieck gives surjectivity, and a bijective étale morphism is an
isomorphism.  This is a conditional fibre lemma, not an appeal to the
open plane Jacobian Conjecture.

Equivalently, one may use the plane theorem over
\(\overline{\mathbb C(w)}\), descend generic degree one, and invoke the
birational Keller theorem.  The fibrewise argument above avoids the
field-transfer step entirely.

## 3. Degree-\(35\) corollary and exact threshold

Guccione--Guccione--Horruitiner--Valqui, Theorem 2.1 of
[*Increasing the degree of a possible counterexample to the Jacobian
Conjecture from 100 to 108*](https://arxiv.org/abs/2204.14178), states
that a plane counterexample has maximum component degree at least \(125\),
or degree pair \((72,108)\) or \((108,72)\).  Consequently every complex
plane Keller map of maximum component degree strictly less than \(108\)
is invertible.

Thus (3) also proves:

> If \(d\le35\), a complex Keller map of degree at most \(d\) with a
> nonzero target-linear combination satisfying the cube-leading
> degree-three hypothesis is a polynomial automorphism.

Indeed,
\[
3d\le105<108.
\]
The strict inequality is essential: \(d=36\) gives \(3d=108\), exactly
the unresolved boundary in that source.

The mathematical threshold and complex hypotheses were verified in the
primary public manuscript.  A peer-reviewed publication record for
arXiv:2204.14178 was not located in the audit search, so this report calls
it a primary public preprint rather than silently upgrading its
bibliographic status.  If that preprint is not accepted as an input,
Moh's established plane range \(<100\) still gives the conservative
corollary \(d\le33\), since \(3d\le99<100\); it does not give \(d=34\).

## 4. Frozen denominator scope

The audit binds to the frozen denominator
`audit_delta_ge3_denominator/DENOMINATOR.json`, SHA-256
`440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a`,
with counts \(19+6+1=26\).

Exactly three whole-family points are newly excluded:

- `PF-BRANCH-FOURTH-THIRD`, \(h=p^2,R=p^3\);
- `D3-BB-30`, \(h=pq,R=p^3\);
- `D3-OB-300`, \(h=p(p+q),R=p^3\).

`D4-DN-3`, \(h=L^2,R=L^3\), is also a consequence but was already
excluded elsewhere, so it is redundant rather than a new count.

For `D3-SF-20C`, only the retained pivot \(z=3\) is covered.  At that
pivot the residual line is \(-4X\), so \(R\) is a scalar multiple of
\(X^3\).  At the reciprocal sheet \(z=1/3\), the residual line is
\(4(p+rq)\), which is not proportional to \(X=p-rq\).  The generic
`D3-SF-20C` family and the \(z=1/3\) sheet are not excluded by this
theorem.

## 5. Verification and hostile mutations

Run:

```sh
./verify_strict.sh
```

`verify_cube_hostile.gp` symbolically checks the general rank-two solve,
both rank-one pivots, both dependent rank-zero charts, all inverse
formulas, inverse-degree ceilings, the \(d=35/36\) arithmetic, and the
Moh fallback boundary \(d=33/34\).
`verify_scope.py` hard-binds the frozen SHA, counts, IDs, and the
\(z=3\) boundary.

The strict wrapper requires the terminal marker
`CUBE_COMPONENT_HOSTILE_AUDIT_PASS`.  It also changes the sign in the
rank-one inverse and requires that mutation to fail before the exact
marker.  Optimized Python is rejected so scope assertions cannot be
silently removed.

These scripts verify the encoded algebra and scope.  They do not reprove
the external bounded-degree plane theorem or Ax--Grothendieck.

## 6. Exact limitations

- The coordinate theorem concerns degree-at-most-three polynomials over
  \(\mathbb C\) whose nonzero cubic homogeneous part is one cube.  It
  says nothing about a general cubic form or a degree-four component.
- The Keller corollary requires such a polynomial to occur as a nonzero
  target-linear combination \(\alpha\mathbin{\cdot}F\).  It is not an
  unconditional degree bound for all Keller maps.
- No whole quartic row is excluded here.  The finite denominator claim
  is exactly the three new whole-family entries and the single retained
  \(z=3\) pivot listed above, with `D4-DN-3` counted only as redundant.
- The \(d\le35\) endpoint depends on the cited degree-\(108\) preprint.
  The published Moh fallback stops at \(d\le33\), and this degree
  multiplication argument stops before \(d=36\).
- The exact scripts certify the algebraic rank split, inverse formulas,
  arithmetic thresholds, and frozen-data binding.  They do not
  mechanically certify the external plane theorems, Ax--Grothendieck,
  the literature-priority search, or claims outside the frozen bridge.
