# An exact one-sided bound and origin-depth consequences

## Scope and result

This note proves, using exact arithmetic,

\[
A(4,1/\sqrt3)\le 33,\qquad B(5)\le 38.
\]

Here \(A(d,s)\) is the largest size of a subset of \(S^{d-1}\) with
distinct inner products at most \(s\), and \(B(5)\) is the largest size of a
five-dimensional kissing code contained in a closed hemisphere.

The initially requested intermediate target \(A(4,1/\sqrt3)\le32\) is **not
proved here**.  The exact degree-11 Delsarte certificate below has objective
approximately \(33.97371538\), so its rigorous integer consequence is 33.
This is nevertheless sufficient to obtain \(B(5)\le38\), because the final
optimization is integral.

For a hypothetical 41-point kissing code \(C\subset S^4\), the one-sided
bound implies:

1. every open hemisphere contains at least three points of \(C\);
2. the origin has Tukey halfspace-depth at least \(3\), or normalized depth
   at least \(3/41\);
3. after deleting any two points, the origin is still in the interior of the
   convex hull of the remaining 39 points;
4. every direction obeys an additional exact belt/cap occupancy inequality;
5. at every code point, contact degree and number of negative inner products
   obey an exact tradeoff.

These are necessary conditions, not a resolution of the kissing-number
problem.

## 1. Exact Delsarte certificate on \(S^3\)

Let \(P_k=P_k^{(4)}\) be the normalized Gegenbauer polynomials for \(S^3\):

\[
P_0(t)=1,\qquad P_1(t)=t,
\]
\[
(k+1)P_k(t)=2ktP_{k-1}(t)-(k-1)P_{k-2}(t)
\quad(k\ge2).
\]

Thus \(P_k(1)=1\).  Put \(s=\sqrt3/3\), and define

\[
\begin{aligned}
q(t)&=t^4+\frac{1001}{500}t^3+\frac{249}{200}t^2
       +\frac{59}{250}t+\frac{13}{5000},\\
r(t)&=t^2-\frac{213}{100}t+\frac{251}{200},\\
f(t)&=(t-s)q(t)^2r(t).
\end{aligned}
\]

The discriminant of \(r\) is

\[
\frac{213^2}{100^2}-4\frac{251}{200}
=-\frac{4831}{10000}<0.
\]

Since \(r\) has positive leading coefficient, \(r(t)>0\) for every real
\(t\).  It follows directly from the factorization that

\[
f(t)\le0\qquad(-1\le t\le s),
\]

including the endpoint \(t=s\).

### Exact Gegenbauer expansion

Let \(L=480000000000\).  Direct recurrence expansion gives

\[
Lf(t)=\sum_{k=0}^{11}c_kP_k(t),\qquad
c_k=A_k+B_k\sqrt3,
\]

with the following integer pairs:

| \(k\) | \(A_k\) | \(B_k\) |
|---:|---:|---:|
| 0 | 65616828309 | -29212891978 |
| 1 | 206150925534 | -87489104412 |
| 2 | 305494320357 | -118512249600 |
| 3 | 292120130280 | -96572298160 |
| 4 | 190277529675 | -45913025900 |
| 5 | 79541678070 | -7363576500 |
| 6 | 17995184550 | 2412486650 |
| 7 | 6922938600 | -3892514800 |
| 8 | 14474556225 | -8293972500 |
| 9 | 16167037500 | -5856250000 |
| 10 | 9662812500 | -1718750000 |
| 11 | 2812500000 | 0 |

Every \(A_k\) is positive.  If \(B_k\ge0\), positivity of \(c_k\) is
immediate.  For every row with \(B_k<0\), exact integer calculation gives

\[
A_k^2-3B_k^2>0.
\]

Indeed the smallest of these displayed norms is

\[
2472064454712840000>0
\]

(the full list is stored in the certificate).  Hence \(A_k>|B_k|\sqrt3\)
and \(c_k>0\) for every \(k\).

At \(t=1\),

\[
Lf(1)=1207236441600-402412147200\sqrt3.
\]

The exact margin below objective 34 is

\[
\begin{aligned}
34c_0-Lf(1)
&=1023735720906-590826180052\sqrt3,\\
1023735720906^2-3(590826180052)^2
&=808101154412557292724>0.
\end{aligned}
\]

The rational part of the margin is positive, so the norm inequality proves
that the margin itself is positive.  Therefore

\[
\frac{f(1)}{f_0}=\frac{Lf(1)}{c_0}<34,
\]

where \(f_0=c_0/L>0\) is the constant Gegenbauer coefficient.

### Delsarte conclusion

For completeness, if \(X=\{x_1,\ldots,x_M\}\subset S^3\), positive
definiteness of the Gegenbauer kernels gives

\[
\sum_{i,j=1}^M P_k(\langle x_i,x_j\rangle)\ge0
\quad(k\ge1).
\]

Consequently,

\[
\sum_{i,j=1}^M f(\langle x_i,x_j\rangle)\ge f_0M^2.
\]

If all distinct inner products are at most \(s\), every off-diagonal term
on the left is nonpositive, whereas every diagonal term equals \(f(1)\).
Thus

\[
f_0M^2\le Mf(1),\qquad M<34.
\]

Since \(M\) is an integer,

\[
\boxed{A(4,1/\sqrt3)\le33.}
\]

All coefficients, signs, and the objective comparison are checked from the
factorization by
[`../verifiers/verify_one_sided_tukey.py`](../verifiers/verify_one_sided_tukey.py).
The verifier uses only `fractions.Fraction` and exact arithmetic in
\(\mathbb Q(\sqrt3)\).

## 2. The belt projection and cap reflection

The following version includes all boundary cases explicitly.  It is a
self-contained specialization of the cap-reflection mechanism used by
Musin and by Barg--Musin.

Let \(P\subset S^4\) be a kissing code contained in the closed hemisphere

\[
H_u=\{x\in S^4:\langle u,x\rangle\ge0\},
\]

where \(u\) is a unit vector.  Write \(z_x=\langle u,x\rangle\), and split

\[
\begin{aligned}
P_a&=\{x\in P:0\le z_x<1/2\},&a&=|P_a|,\\
P_b&=\{x\in P:z_x\ge1/2\},&b&=|P_b|.
\end{aligned}
\]

### Reflection inequality

Let \(R_u(x)=x-2z_xu\), reflection in the equatorial hyperplane.  For
\(x\in P_b\) and \(y\in P\),

\[
\langle R_u(x),y\rangle
=\langle x,y\rangle-2z_xz_y
\le\langle x,y\rangle\le\frac12.
\]

The case \(y=x\), which must not be omitted, gives

\[
\langle R_u(x),x\rangle=1-2z_x^2\le\frac12
\]

precisely because \(z_x\ge1/2\).  Reflected-reflected inner products equal
the original ones.  Moreover, \(R_u(P_b)\) lies in the negative hemisphere,
so it is disjoint from \(P\).  Therefore

\[
P\cup R_u(P_b)
\]

is a five-dimensional kissing code of size \(a+2b\).  Using the assumed
rigorous bound \(\tau(5)\le44\),

\[
\boxed{a+2b\le44.}
\]

At the boundary \(z_x=1/2\), the self-reflected inner product is exactly
\(1/2\), so assigning this boundary to \(P_b\) is valid.

### Projection inequality

For \(x\in P_a\), project to the equator and normalize:

\[
\pi_u(x)=\frac{x-z_xu}{\sqrt{1-z_x^2}}\in S^3.
\]

For \(x,y\in P_a\), put \(z=z_x,w=z_y\).  Then

\[
\langle\pi_u(x),\pi_u(y)\rangle
\le
\frac{1/2-zw}{\sqrt{(1-z^2)(1-w^2)}}.
\]

The right side is at most \(1/\sqrt3\).  Since both sides to be squared are
nonnegative, this is equivalent to

\[
D(z,w):=\frac14-z^2-w^2+3zw-2z^2w^2\ge0.
\]

For fixed \(z\in[0,1/2]\), \(D\) is a concave quadratic in \(w\), so its
minimum on \([0,1/2]\) is attained at an endpoint.  Exactly,

\[
D(z,0)=\frac14-z^2\ge0,\qquad
D(z,1/2)=\frac32z(1-z)\ge0.
\]

Thus the projected set is a spherical \((4,1/\sqrt3)\)-code.  The same
inequality also proves that the projection is injective: two images cannot
coincide because their inner product would be 1.  Hence

\[
\boxed{a\le A(4,1/\sqrt3)\le33.}
\]

## 3. Exact one-sided kissing bound

The two integer inequalities

\[
a\le33,\qquad a+2b\le44
\]

imply

\[
a+b\le38.
\]

Indeed, if \(a+b\ge39\), then the second inequality gives \(b\le5\), and
hence \(a\ge34\), a contradiction.  Equality \(a+b=38\) permits only

\[
(a,b)=(33,5)\quad\hbox{or}\quad(32,6).
\]

Therefore

\[
\boxed{B(5)\le38.}
\]

Notice that the unproved stronger intermediate estimate
\(A(4,1/\sqrt3)\le32\) would give the same integer one-sided bound 38.

## 4. Consequences for a hypothetical 41-code

Assume now that \(C\subset S^4\) is a 41-point kissing code.

### 4.1 Origin-centered Tukey depth

For any unit vector \(u\), the subset

\[
C\cap H_u,\qquad H_u=\{x:\langle u,x\rangle\ge0\},
\]

is a one-sided kissing code.  Hence it has at most 38 points.  Its
complement is the open hemisphere

\[
\{x:\langle u,x\rangle<0\},
\]

which therefore contains at least three points.  Replacing \(u\) by \(-u\)
shows that both open sides of every hyperplane through the origin contain
at least three code points:

\[
\boxed{
\#\{x\in C:\langle u,x\rangle>0\}\ge3,\qquad
\#\{x\in C:\langle u,x\rangle<0\}\ge3.}
\]

Every closed halfspace containing the origin contains a closed halfspace
through the origin, and hence contains at least three points of \(C\).
Thus the Tukey depth of the origin is at least 3 (normalized depth at least
\(3/41\)).

In particular \(0\) lies in the interior of \(\operatorname{conv}C\).
More strongly, delete any set \(D\subset C\) with \(|D|\le2\).  Every open
side of every origin hyperplane still contains a point of \(C\setminus D\).
The strict separation theorem then gives

\[
\boxed{0\in\operatorname{int}\operatorname{conv}(C\setminus D)
\quad\text{for every }|D|\le2.}
\]

Equivalently, every 39-point subset of \(C\) positively spans
\(\mathbb R^5\).  A standard interior-point argument also yields, for every
such deletion, coefficients

\[
\lambda_x>0,\qquad
\sum_{x\in C\setminus D}\lambda_x=1,\qquad
\sum_{x\in C\setminus D}\lambda_xx=0.
\]

To see strict positivity, let \(v\) be the average of the remaining points.
Because the origin is interior, \(-\varepsilon v\) is in their convex hull
for sufficiently small \(\varepsilon>0\).  Add the uniform weights
\(\varepsilon/|C\setminus D|\) to a convex representation of
\(-\varepsilon v\), then renormalize.

### 4.2 Directional belt/cap tradeoff

For a unit vector \(u\), define

\[
r(u)=\#\{x\in C:\langle u,x\rangle<0\},\qquad
b(u)=\#\{x\in C:\langle u,x\rangle\ge1/2\}.
\]

Applying the belt/cap split to \(C\cap H_u\) gives

\[
a=41-r(u)-b(u).
\]

The reflection inequality and the projected-code inequality become

\[
41-r(u)+b(u)\le44,\qquad
41-r(u)-b(u)\le33.
\]

Therefore every direction satisfies the exact interval

\[
\boxed{\max(0,8-r(u))\le b(u)\le r(u)+3.}
\]

The feasibility of this interval itself forces \(r(u)\ge3\).  If an open
hemisphere contains exactly three points, then the opposite closed
hemisphere has 38 points and necessarily

\[
b(u)\in\{5,6\},
\]

corresponding to the two equality profiles \((a,b)=(33,5),(32,6)\).

### 4.3 Vertexwise contact/sign tradeoff

Take \(u=x\in C\).  Let

\[
d(x)=\#\{y\in C\setminus\{x\}:\langle x,y\rangle=1/2\},
\]
\[
r(x)=\#\{y\in C\setminus\{x\}:\langle x,y\rangle<0\}.
\]

Because distinct code points have inner product at most \(1/2\),

\[
b(x)=1+d(x).
\]

The directional interval yields

\[
\boxed{d(x)+r(x)\ge7,\qquad d(x)\le r(x)+2.}
\]

For example, a contact-free vertex of a hypothetical 41-code would have to
have at least seven strictly negative neighbors.  If \(r(x)=3\), then
\(d(x)\in\{4,5\}\).

## 5. Boundary and rigor audit

- The kissing condition is \(\langle x,y\rangle\le1/2\), not strict.
  Equality is retained throughout.
- Height \(z=1/2\) belongs to the reflected cap.  Its reflection is exactly
  \(60^\circ\) from the original point and is therefore allowed.
- Height \(z=0\) belongs to the projected belt; normalization is harmless.
- The projection proof is on the full closed square
  \([0,1/2]^2\), so limiting belt points are covered.
- The Delsarte sign condition holds on the full interval
  \([-1,1/\sqrt3]\), including both endpoints, by factorization rather than
  grid sampling.
- Every Gegenbauer coefficient and the objective margin is checked in
  \(\mathbb Q(\sqrt3)\).  No floating-point PSD or sign decision occurs.
- The conclusion \(A(4,1/\sqrt3)\le33\) uses the strict exact inequality
  \(f(1)/f_0<34\), followed only by integrality.
- Tukey depth uses closed halfspaces, while the complementary count uses
  open hemispheres.  Both orientations are applied, so points on the
  separating hyperplane cause no gap.

## 6. Dependency map and novelty assessment

```text
exact factorization + exact Gegenbauer expansion
                  |
                  v
          A(4,1/sqrt(3)) <= 33
                  |
       projection |            reflection + tau(5) <= 44
                  +-----------------------+
                                          |
                                          v
                                    B(5) <= 38
                                          |
                         intersections with every hemisphere
                                          |
                   +----------------------+------------------+
                   v                      v                  v
          origin Tukey depth >= 3   deletion-2 robust   directional
                                      convex hull        cap tradeoff
                                                               |
                                                               v
                                                    contact/sign tradeoff
```

The origin-depth, deletion robustness, and the two directional inequalities
are genuinely additional exact constraints on a hypothetical 41-code.  They
use neither symmetry, rigidity, antipodality, nor a prescribed contact
graph.  In particular, the vertex inequality couples ordinary negative
inner products to contacts, whereas the existing negative-tail graph bound
uses only inner products strictly below \(-1/2\).

They do **not** presently give a contradiction.  A Tukey depth of three is
compatible with many full-dimensional point sets, and \(B(5)\le38\) does not
bound a code that is not contained in a hemisphere.  Thus this route should
be recorded as a certified new constraint, not as an upper bound
\(\tau(5)\le40\).

## Source context

The cap-reflection and meridional-projection mechanism appears in Oleg
Musin, [*The one-sided kissing number in four
dimensions*](https://arxiv.org/abs/math/0511071), and the general
one-sided inequality is stated by Alexander Barg and Oleg Musin,
[*Codes in spherical caps*](https://arxiv.org/abs/math/0606734).
The proof above is specialized and self-contained; those papers are not
used as black boxes.
