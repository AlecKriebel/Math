# Cube-component exit

## Status

This artifact proves an elementary coordinate lemma and derives a
bounded-degree complex Keller corollary.  It does **not** claim a global
Jacobian theorem, a quartic row, or any denominator family beyond the
five exact entries listed below.

This is an AI-assisted, non-peer-reviewed research note.  Exact
verification checks the algebra encoded in the scripts; it is evidence,
not peer review.

Draft freeze (UTC): `2026-07-26T07:53:50Z`.

First public release (UTC): `2026-07-26T08:13:13Z`.

### Coordinate theorem

Let \(k\) be an algebraically closed field of characteristic zero.  Let
\(\ell\) be a nonzero linear form and
\[
f=C+\ell^3+Q_2+L_1\in k[x,y,z],
\]
where \(Q_2\) and \(L_1\) are homogeneous of degrees two and one.  If
\(\nabla f\) has no zero in \(k^3\), then \(f\) is a coordinate of
\(k[x,y,z]\).  A coordinate automorphism containing \(f\), and its
inverse, can be chosen of degree at most three.

The same statement covers a nonzero scalar multiple of \(\ell^3\):
over \(k\), absorb a cube root of the scalar into \(\ell\).  The
constant \(C\) is removed and restored by a translation.

### Complex Keller corollary

Let \(F:\mathbf C^3\to\mathbf C^3\) be a Keller map of total degree
\(d\), and suppose some nonzero target-linear combination
\(\alpha\!\cdot\!F\) has the displayed cube-leading form.
Extend \(\alpha\) to \(T\in\mathrm{GL}_3(\mathbf C)\); then \(TF\) is
again Keller, with determinant \((\det T)(\det JF)\), and
\(\alpha\!\cdot\!F\) is one of its components.  Its gradient is a row
of an everywhere invertible Jacobian and is therefore nowhere zero.
Using the plane floor proved in the public preprint cited below, \(F\)
is an automorphism whenever
\[
d\le35,\qquad 3d\le105<108.
\]

The degree-\(108\) input is the primary preprint:

J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui,
“Increasing the degree of a possible counterexample to the Jacobian
Conjecture from 100 to 108,”
[arXiv:2204.14178](https://arxiv.org/abs/2204.14178).

Its abstract explicitly states that the plane lower floor is raised to
\(108\).  A peer-reviewed journal version was not located in this
audit.  If that preprint is not accepted as an input, Moh's established
safe range \(<100\) gives the conservative fallback
\[
d\le33,\qquad 3d\le99<100.
\]

## Complete rank atlas

After a linear change take \(\ell=x\), write \(y=(y,z)^t\), and express
\[
f=x^3+Ax^2+x\,c^ty+\frac12y^tMy+ax+d^ty+C,
\]
with \(M\) symmetric \(2\times2\).  Remove \(C\) by translation and put
\(g(x)=x^3+Ax^2+ax\).

### Rank two

If \(M\) is invertible, the transverse equations give
\[
y=-M^{-1}(cx+d).
\]
The remaining derivative is exactly
\[
3x^2+(2A-c^tM^{-1}c)x+(a-c^tM^{-1}d).
\]
Choose a root \(x_0\) and set \(y_0=-M^{-1}(cx_0+d)\).  All three
derivatives vanish, so rank two is impossible for a nonsingular \(f\).

### Rank one

After a constant transverse linear change,
\[
f=g(x)+x(\beta u+\gamma v)+\frac m2u^2+\varepsilon u+\eta v,
\qquad m\ne0.
\]

If \(\gamma\ne0\), an explicit critical point is
\[
x_0=-\frac{\eta}{\gamma},\qquad
u_0=-\frac{\beta x_0+\varepsilon}{m},\qquad
v_0=-\frac{g'(x_0)+\beta u_0}{\gamma}.
\]
Indeed \(f_v,f_u,f_x\) vanish in that order.

If \(\gamma=0=\eta\), put
\[
u(x)=-\frac{\beta x+\varepsilon}{m}.
\]
Then \(f_u=f_v=0\), and
\[
f_x=3x^2+\left(2A-\frac{\beta^2}{m}\right)x
       +\left(a-\frac{\beta\varepsilon}{m}\right).
\]
A root \(x_0\), together with \(u_0=u(x_0)\) and \(v_0=0\), is a
critical point.

Thus nonsingularity forces \(\gamma=0,\eta\ne0\), where
\[
f=\eta v+R(x,u),\qquad
R=g(x)+\beta xu+\frac m2u^2+\varepsilon u.
\]
The coordinate map \((x,u,v)\mapsto(x,u,w=f)\) has inverse
\[
v=\frac{w-R(x,u)}{\eta}.
\]

The rank-one normalization has no missing pivot.  If
\[
M=\begin{pmatrix}m_{11}&m_{12}\\m_{12}&m_{22}\end{pmatrix}
\]
and \(m_{11}\ne0,\det M=0\), the quadratic equals
\[
\frac{m_{11}}2
\left(y+\frac{m_{12}}{m_{11}}z\right)^2.
\]
On the boundary \(m_{11}=0=\det M\), necessarily \(m_{12}=0\);
rank one is then exactly \(m_{22}\ne0\).  The remaining boundary is
\(M=0\).

### Rank zero

Write
\[
f=g(x)+x(by+cz)+ey+hz,\qquad \Delta=bh-ce.
\]
If \(\Delta\ne0\), set
\[
u=by+cz,\qquad v=ey+hz.
\]
Then \(f=g(x)+xu+v\), with
\[
v=w-g(x)-xu,\quad
y=\frac{hu-cv}{\Delta},\quad
z=\frac{-eu+bv}{\Delta}.
\]
This is an explicit coordinate inverse of degree at most three.

Suppose \(\Delta=0\) and \((b,c)=(0,0)\).  If \((e,h)\ne(0,0)\), set
\(v=ey+hz\).  On \(e\ne0\), use \(u=z\) and
\(y=(v-hu)/e\).  On the boundary \(e=0,h\ne0\), use \(u=y\) and
\(z=v/h\).  In either chart \(f=g(x)+v\) and \(v=w-g(x)\).  If also
\((e,h)=(0,0)\), any root \(x_0\) of \(g'\), with \(y_0=z_0=0\), is a
critical point.

Finally, suppose \(\Delta=0\) and \((b,c)\ne(0,0)\).  Then
\((e,h)=\delta(b,c)\): use \(\delta=e/b\) on \(b\ne0\), or
\(\delta=h/c\) on \(b=0,c\ne0\).  Set \(x_0=-\delta\).  If \(b\ne0\),
take
\[
y_0=-g'(x_0)/b,\qquad z_0=0;
\]
if \(b=0,c\ne0\), take
\[
y_0=0,\qquad z_0=-g'(x_0)/c.
\]
These are critical points.  This covers every rank-zero pivot and
boundary.

## Keller bridge

After the target change described above, choose a source coordinate
automorphism \(\sigma=(u,v,\alpha\!\cdot\!F)\).  In these source
coordinates,
\[
G=(TF)\circ\sigma^{-1}=(G_1(u,v,w),G_2(u,v,w),w).
\]
The coordinate inverse has degree at most three, so
\(\deg G_i\le3d\).  Each specialization \(w=w_0\) is a plane Keller
map.  Under the cited floor it is an automorphism.  Hence \(G\) is
injective fibre by fibre.  Ax--Grothendieck gives surjectivity.  Since
\(G\) is Keller, it is étale; injectivity makes it a universally
injective étale morphism, hence an open immersion.  A surjective open
immersion is an isomorphism, so \(G\), then \(F\), is a polynomial
automorphism.

## Frozen 26-family bridge

The bridge is recorded in [BRIDGE.json](./BRIDGE.json) and checked
directly against the frozen canonical 26-family denominator.

Newly excluded whole-family points:

* `PF-BRANCH-FOURTH-THIRD`: \(h=p^2,\ R=p^3\);
* `D3-BB-30`: \(h=pq,\ R=p^3\);
* `D3-OB-300`: \(h=p(p+q),\ R=p^3\).

Recorded but already excluded:

* `D4-DN-3`: \(h=L^2,\ R=L^3\).

Newly excluded retained pivot only:

* \(z=3\) in `D3-SF-20C`, where \(R=X^3\).

The generic `D3-SF-20C` family and its reciprocal \(z=1/3\) sheet are
not excluded by this theorem.  No other denominator entry is claimed.
At the fine-family level this changes the frozen count from \(6/26\)
to \(9/26\).  It does not close the containing global row: the global
quartic status remains \(4/14\) certified, \(4/14\) provisional, and
\(6/14\) open, and the universal total-degree floor remains four.

## Verification

Run:

```sh
./verify_strict.sh
```

This is the primary suite.  Its successful final marker is:

`CUBE_COMPONENT_EXIT_STRICT_PASS`

The wrapper also requires four corrupted certificates to fail: the
rank-two leading coefficient, a coordinate inverse sign, the
degree-\(36\) boundary, and an attempted enlargement of the frozen
denominator scope.

To require both the primary suite and the separately implemented
hostile audit, run:

```sh
./verify_all_strict.sh
```

The aggregate wrapper checks for both underlying terminal markers and
prints its own marker only after both pass:

`CUBE_COMPONENT_ALL_STRICT_PASS`

The hostile audit report and its independent research log are in
[`audit_hostile/AUDIT.md`](./audit_hostile/AUDIT.md) and
[`audit_hostile/RESEARCH_LOG.md`](./audit_hostile/RESEARCH_LOG.md).
A separate hypothesis and prior-art audit is in
[`audit_geometry/AUDIT.md`](./audit_geometry/AUDIT.md).

Worldwide novelty and priority are unresolved; see
[PRIORITY_AUDIT.md](./PRIORITY_AUDIT.md) and
[DISCLOSURE.md](./DISCLOSURE.md).
