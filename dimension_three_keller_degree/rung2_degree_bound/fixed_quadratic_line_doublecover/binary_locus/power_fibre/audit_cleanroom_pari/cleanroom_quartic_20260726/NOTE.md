# Clean-room audit: the quartic power fibre

## Verdict

**PASS.**  Over \(\mathbf C\), every Keller map
\[
F=L(p,q,r)^t+H_2+H_3+H_4,\qquad
H_4=(p^4,p^2q^2,0),\qquad (H_3)_3=p^3,
\]
with \(L\in\mathrm{GL}_3(\mathbf C)\), is a polynomial automorphism.
No counterexample was found.

The decisive point is stronger than the top-contact calculation:

> Every nonsingular polynomial
> \(f=p^3+Q_2(p,q,r)+L_1(p,q,r)\) is a coordinate of
> \(\mathbf C[p,q,r]\).

For a Keller map, \(f=F_3\) is nonsingular because its gradient is a row
of an everywhere invertible Jacobian matrix.  This lemma covers **every**
solution of every \(E_6\) and lower branch; it is not a generic-chart
argument.

The resulting source-coordinate inverse has degree at most three.
For the requested fixed quartic forms, after making \(F_3\) the third
variable every plane fibre has degree at most \(9\) (the general
composition bound is \(4\cdot3=12\)).  Moh's plane theorem in the safe
range \(<100\) makes every fibre an automorphism, and
Ax--Grothendieck then makes the three-variable map an automorphism.

## Clean-room scope

This directory was created for this audit.  No pre-existing file under
`power_fibre/` was read.  The only inherited material inspected was the
frozen external incidence denominator
`delta_ge3_universal/{denominator.json,FREEZE.json}`, which records the
name of the normalized leaf \(h=p^2,\ R=p^3\).  None of its proof scripts
or conclusions was used.

All symbolic checks here use PARI/GP or the dependency-free exact sparse
engine in `verify_certificate.py`.

## 1. Standalone coordinate lemma

Let \(k\) be any algebraically closed field of characteristic zero, and let
\[
f=C+p^3+Q_2+L_1.
\]
The constant \(C\) is harmless: replace \(f\) by \(f-C\), and translate
the eventual coordinate \(w\) back by \(C\).  Thus take \(C=0\).
Put \(y=(q,r)^t\) and write, uniquely,
\[
 f=p^3+A p^2+p\,c^t y+\frac12y^tMy+a p+d^t y,                 \tag{1}
\]
where \(M=M^t\in M_2(\mathbf C)\) and \(c,d\in\mathbf C^2\).
Thus
\[
\nabla_yf=My+cp+d,\qquad
f_p=3p^2+2Ap+c^ty+a.                                         \tag{2}
\]

The following rank atlas is exhaustive.

### Rank two: \(\det M\ne0\)

For every \(p\), the two equations \(\nabla_yf=0\) have the unique
solution
\[
y=-M^{-1}(cp+d).
\]
After substitution, \(f_p\) is a univariate quadratic in \(p\) whose
leading coefficient is \(3\).  It has a root over \(\mathbf C\), giving
a critical point of \(f\).  Therefore this chart cannot occur for a
Keller map.

### Rank one: \(\det M=0,\ M\ne0\)

After a constant invertible change of \(q,r\), (1) has the form
\[
f=p^3+Ap^2+p(c_u u+c_vv)+\frac m2u^2+ap+d_uu+d_vv,\qquad m\ne0.
\]
There are exactly three subcharts.

1. If \(c_v\ne0\), take
   \[
   p=-d_v/c_v,\qquad
   u=-(c_up+d_u)/m,
   \]
   and choose \(v\) to make \(f_p=0\).  This is a critical point.
2. If \(c_v=0=d_v\), solve \(f_u=0\) for \(u\).  The remaining
   \(f_p\) is again a univariate quadratic with leading coefficient
   \(3\), hence has a root.  This is a critical point.
3. If \(c_v=0,\ d_v\ne0\), then
   \[
   f=d_vv+R(p,u).
   \]
   It is a coordinate, with the explicit inverse
   \[
   (p,u,w)\longmapsto
   \left(p,u,\frac{w-R(p,u)}{d_v}\right).                     \tag{3}
   \]

No division is made on the boundary \(d_v=0\): it is the second,
critical, subchart.

### Rank zero: \(M=0\)

Now
\[
f=g(p)+p\,c^ty+d^ty,\qquad g(p)=p^3+Ap^2+ap.
\]

* If \(c,d\) are independent, use the linear coordinates
  \(u=c^ty,\ v=d^ty\).  Then
  \[
  f=g(p)+pu+v,\qquad v=w-g(p)-pu,                             \tag{4}
  \]
  so \(f\) is a coordinate.
* If \(c=0,\ d\ne0\), take \(v=d^ty\) and any complementary linear
  coordinate \(u\).  Then
  \[
  f=g(p)+v,\qquad v=w-g(p),                                  \tag{5}
  \]
  so \(f\) is a coordinate.
* If \(c\ne0\) and \(c,d\) are dependent, write \(d=\delta c\).
  At \(p=-\delta\), \(\nabla_yf=0\), and \(y\) can be chosen so that
  \(f_p=0\).  This gives a critical point.
* If \(c=d=0\), a root of \(g'(p)=3p^2+2Ap+a\) gives a critical
  point.

Thus a nonsingular \(f\) occurs only in the coordinate subcharts
(3)--(5).  Both the coordinate map and its displayed inverse have
degree at most three.

### Exact pivot boundaries

Writing
\[
M=\begin{pmatrix}m_{qq}&m_{qr}\\m_{qr}&m_{rr}\end{pmatrix},
\]
the rank-one normalization uses the following division-safe charts.

* \(m_{qq}\ne0\): a null vector is
  \(n=(-m_{qr},m_{qq})\).
* \(m_{qq}=0\) and \(\det M=0\): necessarily \(m_{qr}=0\).
  Rank one then means \(m_{rr}\ne0\), with null vector \(n=(1,0)\).
* The boundary \(m_{qq}=m_{qr}=m_{rr}=0\) is exactly the rank-zero
  chart.

In rank one, \(c_v\) and \(d_v\) above are, up to a common nonzero
factor, \(n^tc\) and \(n^td\).  Hence the three rank-one subcharts do
not depend on the chosen diagonalization.

In rank zero, the first pivot is \(\det[c\ d]\).  On its zero locus,
the \(c\ne0\) branch is covered by the two honest charts
\(c_1\ne0\) and \(c_1=0,\ c_2\ne0\); the remaining boundary is
\(c=0\), split into \(d\ne0\) and \(d=0\).  This lists every pivot
boundary.

## 2. From the coordinate lemma to an automorphism

For a Keller map, \(\det JF\) is a nonzero constant.  Therefore every
row of \(JF(x)\), in particular \(\nabla F_3(x)\), is nonzero for every
\(x\in\mathbf C^3\).  Since
\[
F_3=p^3+(H_2)_3+(Lx)_3,
\]
the lemma applies without using, dividing, saturating, or specializing
any \(E_6\) parameter.

Let
\[
\sigma:\mathbf A^3\longrightarrow\mathbf A^3,\qquad
(p,q,r)\longmapsto(u,v,w)
\]
be one of the coordinate automorphisms constructed above, with
\(w=F_3\).  The formulas show
\[
\deg\sigma\le3,\qquad\deg\sigma^{-1}\le3.
\]
Set
\[
G=F\circ\sigma^{-1}=(G_1(u,v,w),G_2(u,v,w),w).
\]
The determinant transfer is exact:
\[
\det JG=(\det JF)\,(\det J\sigma^{-1})\in\mathbf C^\times.
\]
Expanding along the last row gives
\[
\frac{\partial(G_1,G_2)}{\partial(u,v)}\in\mathbf C^\times.   \tag{6}
\]
Moreover, the general composition bound is
\[
\deg G_i\le(\deg F)(\deg\sigma^{-1})\le4\cdot3=12.           \tag{7}
\]
For this fixed leading family the exact structural ceiling improves to
\(9\).  Every coordinate construction above retains \(p\) as a linear
coordinate, while \(q,r\) acquire degree at most three.  Hence the two
fixed quartics \(p^4,p^2q^2\) acquire degrees at most \(4,8\);
arbitrary cubic terms acquire degree at most \(9\), quadratics at most
\(6\), and linear terms at most \(3\).

For every \(w_0\in\mathbf C\), (6) specializes to a two-variable
Keller map
\[
(u,v)\longmapsto(G_1(u,v,w_0),G_2(u,v,w_0))
\]
of total degree at most \(9<100\).  Moh's verified plane range
\(<100\) makes this specialized map an automorphism.  This paragraph,
and the Ax--Grothendieck step below, is applied over \(\mathbf C\);
the coordinate lemma itself holds over every algebraically closed
characteristic-zero field.

It follows that \(G\) is injective: equal images have equal third
coordinate \(w\), and then equality in that plane fibre forces equal
\((u,v)\).  By the Ax--Grothendieck theorem, an injective polynomial
self-map of \(\mathbf A^3_{\mathbf C}\) is a polynomial automorphism.
Hence \(G\), and therefore \(F\), is an automorphism.

This avoids a possible function-field descent gap.  One may instead
work over \(\mathbf C(w)\), but a generic-fibre inverse alone requires
an additional argument excluding denominators in \(w\).  The
fibrewise-injectivity route above needs no such argument.

The low-degree input is T. T. Moh, *On the Jacobian conjecture and the
configurations of roots*, J. Reine Angew. Math. **340** (1983),
140--212, DOI `10.1515/crll.1983.340.140`.  Moh's own summary states
the plane low-degree range (we use only the safe \(<100\) formulation):
`https://www.math.purdue.edu/~ttm/jacobian.html`.

## 3. Complete top-contact reconstruction

Although the coordinate proof already covers every lower branch, the
top determinant layers were independently reconstructed.

Put
\[
Z=(H_2)_3,\quad A=(H_3)_1,\quad B=(H_3)_2,\quad X=(H_2)_1,
\quad \ell=(Lx)_3,\quad\lambda=\partial_r\ell.
\]
For polynomials \(f,g,h\), write
\[
[f,g,h]=\det(\nabla f,\nabla g,\nabla h).
\]

Use a scaling parameter \(t\):
\[
\det\!\left(L+tJH_2+t^2JH_3+t^3JH_4\right)=\det L.
\]
The \(t^9\) layer vanishes because the third row of \(JH_4\) is zero.
The \(t^8\) layer is
\([p^4,p^2q^2,p^3]=0\).

### The \(t^7\) layer

Direct expansion gives
\[
E_7=8p^5q\,Z_r-6p^4q\,A_r
    =2p^4q(4pZ_r-3A_r).                                     \tag{8}
\]
Thus, with no parameter division,
\[
A=\frac43pZ+a(p,q),\qquad a\in\mathbf C[p,q]_3.              \tag{9}
\]

### The \(t^6\) layer

After (9), all six trilinear terms give
\[
\begin{aligned}
E_6={}&8\lambda p^5q-6p^4qX_r
       +3p^2a_qB_r\\
    &+2pq(pa_p-qa_q)Z_r+\frac83p^2q\,Z\,Z_r.                 \tag{10}
\end{aligned}
\]

Two cancellations are worth recording:
\[
[p^4,B,Z]+\left[\frac43pZ,B,p^3\right]=0,
\]
and
\[
[p^4,(H_2)_2,p^3]=0.
\]
These are checked symbolically in both independent verifiers.

### Division-free parameterization of every top contact

Let \(V_d=\mathbf C[p,q,r]_d\), and define the right inverse of
\(\partial_r\)
\[
\mathcal I_r\!\left(\sum c_{ijk}p^iq^jr^k\right)
 =\sum\frac{c_{ijk}}{k+1}p^iq^jr^{k+1}.
\]

Choose freely
\[
Z\in V_2,\quad a\in\mathbf C[p,q]_3,\quad
U\in V_2,\quad B_0,X_0\in\mathbf C[p,q],
\]
where \(B_0\) and \(X_0\) have degrees \(3\) and \(2\), respectively,
and choose the linear row \(\ell\).  Set
\[
B=B_0+\mathcal I_r(U)
\]
and
\[
N=8\lambda p^5q+3p^2a_qU
  +2pq(pa_p-qa_q)Z_r+\frac83p^2qZZ_r.                        \tag{11}
\]

The complete \(E_6\) condition is the coefficient-subspace condition
\[
N\in6p^4q\,V_1.                                              \tag{12}
\]
When (12) holds, the quotient \(V=N/(6p^4q)\in V_1\) is unique, and
\[
X=X_0+\mathcal I_r(V).                                       \tag{13}
\]
Conversely, (11)--(13) give \(E_6=0\).  Thus (9) and
(11)--(13) parameterize every top contact.  There is no hidden
nonzero pivot: (12) literally says that all coefficients outside the
three monomials \(p^5q,p^4q^2,p^4qr\) vanish.

The binary part \(B_0\), the binary part \(X_0\), all of
\((H_2)_2\), and the first two rows of \(L\) are free at these two
layers (with the eventual condition \(\det L\ne0\)).  Lower Keller
identities may cut this affine kernel further, but every such cut is
already covered by the coordinate lemma in Section 1.

## 4. Top stabilizer and orbit boundaries

The full linear source stabilizer of the displayed leading family,
paired with the forced diagonal target rescaling, is
\[
(p,q,r)=(aP,bQ,cR+uP+vQ),\qquad abc\ne0,
\]
\[
(F_1,F_2,F_3)\longmapsto
(a^{-4}F_1,\ a^{-2}b^{-2}F_2,\ a^{-3}F_3).
\]
One may additionally shear the first two target components by
multiples of \(F_3\); this changes only lower homogeneous pieces.

There are no missing linear source terms:

* \(p^3\) forces the \(p\)-axis;
* \(p^4,p^2q^2\) then force the \(q\)-axis (a \(q\mapsto q+\mu p\)
  shear would create a forbidden \(p^3q\) quartic);
* \(r\) is invisible to the fixed leading forms and may be scaled and
  sheared by \(p,q\).

For the third linear row \(\ell\), let \(\lambda=\ell_r\).

* If \(\lambda\ne0\), an \(r\)-scale and \(r\)-shear normalize
  \(\ell=r\).
* If \(\lambda=0\), invertibility of \(L\) makes \(\ell\) a nonzero
  binary line.  Under the diagonal \(p,q\) torus its three exact
  zero-pattern orbits are
  \[
  \ell=p,\qquad\ell=q,\qquad\ell=p+q.
  \]
  The boundaries of the mixed orbit are precisely the two axis
  orbits.

No further stabilizer quotient is used in (11)--(13); keeping that
affine-kernel parameterization unquotiented is what prevents a
parameter endpoint from being lost.  The only later normalizations
are the exhaustive rank/pivot normalizations of Section 1, made by
honest polynomial source automorphisms after the full family has
already been retained.

## 5. Lower exits and coverage statement

The logical flow is
\[
\text{full Keller identities}
\Longrightarrow \det JF\in\mathbf C^\times
\Longrightarrow \nabla F_3\ne0
\Longrightarrow F_3\text{ is a degree-}\le3\text{ coordinate}
\Longrightarrow \text{plane fibres of degree }\le9
\Longrightarrow F\text{ is an automorphism}.
\]

Therefore:

* no \(E_6\) branch is assumed generic;
* no lower determinant identity is discarded;
* no coefficient is inverted without separately listing its zero
  boundary;
* the rank-two and critical rank-one/rank-zero charts are impossible
  for a Keller map;
* every surviving chart has an explicit coordinate inverse;
* the plane theorem is applied only after the exact degree ceiling is
  established.

## 6. Frozen denominator corollaries

The coordinate lemma uses only \(\deg F\le4\) and the fact that one
component has cubic leading form equal to the cube of a linear form.
It therefore applies to a few additional *points* in the frozen
canonical denominator.  These mappings were checked directly against
`audit_delta_ge3_denominator/DENOMINATOR.json`, whose SHA-256 at audit
time is

`440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a`.

The exact certified list is:

* `PF-BRANCH-FOURTH-THIRD`: \(h=p^2,\ R=p^3\);
* `D4-DN-3`: \(h=L^2,\ R=L^3\) (already closed elsewhere);
* `D3-BB-30`: \(h=pq,\ R=p^3\);
* `D3-OB-300`: \(h=p(p+q),\ R=p^3\);
* only the retained pivot \(z=3\) inside `D3-SF-20C`, where the
  denominator explicitly says \(R=X^3\).

The generic `D3-SF-20C` normal form is
\[
R=X^2((5-3z)p+4rq),
\]
so this audit **does not** close that whole family.  Its reciprocal
\(z=1/3\) is recorded as a distinct regular sheet, not as the
\(R=X^3\) pivot.  No other denominator family is claimed here.

`verify_frozen_corollaries.py` rechecks exactly these statements.

## 7. Reproduction and hostile mutations

Run

```sh
./verify_strict.sh
```

It requires both markers

* `POWER_FIBRE_PARI_PASS`, and
* `POWER_FIBRE_CLEANROOM_STRICT_PASS`,

then requires four corrupted certificates to fail:

1. \(4/3\) in (9) is changed;
2. the \(\lambda\)-term sign in (10) is changed;
3. the explicit coordinate identity is corrupted;
4. the fixed-family plane ceiling \(9\) is falsely lowered to \(8\).

The final marker is

`POWER_FIBRE_CLEANROOM_VERIFY_STRICT_PASS`.

The computation is tiny on the specified Apple M1 Pro and does not
benefit meaningfully from more hardware.
