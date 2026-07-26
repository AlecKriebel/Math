# Hostile audit of the D4-SF-11CC exclusion

**Verdict:** pass; promote the family-level exclusion.

**Audit timestamp (UTC):** `2026-07-26T05:26:00Z`.

This audit was reconstructed from the canonical normal form before the
primary `NOTE.md` or either primary verifier was read.  It uses a separate
exact script and a different contact-elimination mechanism.  The work is
not peer reviewed.

## Scope of the verdict

The promoted statement is only:

> Every complex degree-four Keller map in the canonical
> `D4-SF-11CC` leading-data orbit is a polynomial automorphism.

This excludes one isolated high-incidence family.  It does not close L07,
the parent fixed-quadratic row, the quartic frontier, or a program rung.

## Independent reconstruction

Starting with the squarefree-root cover
\[
X=p-\rho q,\quad Y=p-\rho^{-1}q,\quad
z=\rho^2,\quad (z+z^{-1}+2)=16,
\]
choose \(\rho+\rho^{-1}=4\).  Exact reduction modulo
\(\rho^2-4\rho+1\) gives
\[
XY=p^2-4pq+q^2,\qquad
(z+1)p+4\rho q=4\rho(p+q).
\]
Scaling the third target coordinate therefore gives the rational normal
form
\[
h=p^2-4pq+q^2,\qquad R=h(p+q).
\]
The opposite sign is carried to this form by \(q\mapsto-q\), and
\(\rho\mapsto\rho^{-1}\) changes the residual only by a unit.  Thus the
normalization covers the whole canonical point, rather than one
unmentioned square-root presentation.

The independently recomputed \(E_7\) syzygy nullities are \(0,2,4\) in
degrees \(0,1,2\).  In the resulting coordinates
\((x_0,x_1;y_0,\ldots,y_3)\), the hostile verifier retains:

- all eight arbitrary binary cubic coefficients in the first two entries
  of \(H_3\);
- all three arbitrary binary quadratic coefficients in the third entry of
  \(H_2\);
- every quadratic coefficient in the first two entries of \(H_2\); and
- all nine entries of the linear part.

The full \(E_6\) system is \(28\times18\) in the coefficients that occur at
that weight.  A constant \(5\times5\) pivot has determinant
\(-5971968\), so it is safe on every contact chart.  After this
parameter-free elimination, four residuals contain nonzero scalar
multiples of
\[
\begin{aligned}
(3x_0-x_1)^2,\qquad&
(3x_0-2x_1)(3x_0+2x_1),\\
(9y_0+3y_1-3y_2-y_3)^2,\qquad&
(3y_1-4y_3)^2.
\end{aligned}
\]
The first pair forces \(x_0=x_1=0\); the second pair then forces the two
linear \(y\)-relations.  Conversely, an explicit solution of every
\(E_6\) coefficient proves that the projected contact locus is exactly
\[
x_0=x_1=0,\qquad
y_0=(m-n)/3,\quad y_1=4n/3,\quad y_2=m,\quad y_3=n.
\]
This supplies a completeness proof independent of the primary
coefficient combinations.

On this plane, the exact coefficient and augmented ranks agree:

| chart | condition | ranks |
|---|---|---|
| generic | \(\Delta=m^2-4mn+n^2\ne0\) | \(7/7\) |
| conic | \(\Delta=0,\ (m,n)\ne(0,0)\) | \(6/6\) |
| origin | \(m=n=0\) | \(5/5\) |

The generic symbolic ranks are seven, and a maximal minor is a nonzero
constant times \(\Delta\).  The conic consists of the two projective
points \(m/n=2\pm\sqrt3\); both were freshly solved, not identified by
assumption.  The origin was also freshly solved.

For the generic chart, two \(E_5\) coefficients are fixed, independently
of every free lower coefficient, by
\[
-\frac49(7m^3-6m^2n+3mn^2-2n^3),\qquad
\frac49(2m^3-3m^2n+6mn^2-7n^3).
\]
Their two resultants are \(-46656n^9\) and \(46656m^9\), so their common
affine zero is only the origin.  Fresh solves at both conic points give
nonzero values.  Thus every nonzero contact is excluded.

At the origin, two \(E_4\) coefficients become
\[
\frac8{27}(3b-\lambda)^2,\qquad
\frac8{27}(3b-4\lambda)^2.
\]
They force \(b=\lambda=0\), after which the complete \(E_6\) formulas
force all six nonbinary quadratic coefficients to zero.  The \(E_7\)
contact coordinates are already zero, so every nonlinear homogeneous
part depends only on \(p,q\).

## Orbit and Moh exit

After first subtracting the constant term, the Keller condition makes the
linear part \(L_0\) invertible.  Postcomposition by \(L_0^{-1}\) preserves
binary dependence of all nonlinear terms and produces
\[
(p,q,r)\longmapsto
(p+A(p,q),\ q+B(p,q),\ r+C(p,q)).
\]
Its Jacobian determinant is that of the degree-at-most-four plane map
\(\phi=(p+A,q+B)\).  Moh's unconditional plane result for degree
strictly less than \(100\) applies.  If \(\phi^{-1}\) is its polynomial
inverse, the displayed threefold map has inverse
\[
(u,v,w)\longmapsto
\bigl(\phi^{-1}(u,v),\
w-C(\phi^{-1}(u,v))\bigr).
\]
No plane Jacobian-conjecture assumption or BCW reduction is used.

The primary note now uses the historically safer “degree \(<100\)” and
states explicitly that the constant term is removed before the homogeneous
decomposition.  These editorial corrections have no effect at degree four.

## Exact replay

Run:

```sh
./verify_hostile.sh
```

The terminal marker is:

```text
D4_SF_11CC_HOSTILE_AUDIT_STRICT_PASS
```

The hostile script does not import either primary verifier.  Assertions
must remain enabled.  These exact checks certify the encoded algebra; they
are evidence, not peer review.

## Disclosure

The reconstruction, audit, and verifier were produced with substantial AI
assistance.
