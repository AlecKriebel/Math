# The fixed-support conic-preserving rate family

This directory describes all rate vectors on the final 20-reaction support
whose mass-action field vanishes on the conic

\[
L=z-x-y+1=0,\qquad
Q=7x^2-2xy-16x+7y^2-16y+16=0.
\]

All statements here are over `QQ`.  Run

```sh
.venv/bin/python weakly_reversible_continuum_no_common_factor/family/verify_family.py
```

from the repository root for the exact verification.

## Canonical remainder map

The directed rates occur in the following fixed order, which is also the
column order of `remainder_matrix.csv`:

| column | rate | column | rate |
|---:|:---|---:|:---|
| 0 | \(k_{0,1}\) | 10 | \(k_{2,7}\) |
| 1 | \(k_{1,0}\) | 11 | \(k_{7,2}\) |
| 2 | \(k_{0,4}\) | 12 | \(k_{2,9}\) |
| 3 | \(k_{4,0}\) | 13 | \(k_{9,2}\) |
| 4 | \(k_{0,6}\) | 14 | \(k_{3,4}\) |
| 5 | \(k_{6,0}\) | 15 | \(k_{4,3}\) |
| 6 | \(k_{1,7}\) | 16 | \(k_{5,9}\) |
| 7 | \(k_{7,1}\) | 17 | \(k_{9,5}\) |
| 8 | \(k_{2,4}\) | 18 | \(k_{8,9}\) |
| 9 | \(k_{4,2}\) | 19 | \(k_{9,8}\) |

Use lexicographic order with variable order \(z>y>x\).  The reduced
Groebner basis of \((L,Q)\) is

\[
z-x-y+1,\qquad
y^2-\frac27xy+x^2-\frac{16}{7}(x+y)+\frac{16}{7}.
\]

Every degree-at-most-three normal form therefore has a unique coefficient
vector in the ordered monomial list

\[
(1,x,y,x^2,xy,x^3,x^2y).
\]

For a rate vector \(k\in\mathbb Q^{20}\), stack these seven coefficients
for \(F_1,F_2,F_3\).  This defines the canonical matrix
\(M\in\mathbb Q^{21\times20}\), recorded in
`remainder_matrix.csv`.  By construction,

\[
F_i\in(L,Q)\ \text{for all }i
\quad\Longleftrightarrow\quad Mk=0.
\]

An exact rank certificate uses the zero-based row indices

```text
0,1,2,4,5,6,7,8,9,12,13,14,15,16,18,19
```

and column indices

```text
0,1,2,3,4,5,6,7,8,9,10,11,13,14,16,18.
```

The determinant of this \(16\times16\) submatrix is

\[
\frac{7255941120}{823543}
=\frac{2^{13}3^{11}5}{7^7}\ne0.
\]

The four independent kernel vectors below prove the reverse rank bound, so
\(\operatorname{rank}M=16\) and \(\dim\ker M=4\).

## Exact kernel basis

The columns of the following table are an integer-vector basis of
\(\ker_{\mathbb Q}M\).  This means a basis over `QQ` whose vectors happen
to have primitive integer entries; no assertion about a saturated
integer-lattice basis is needed.

| rate | \(u_a\) | \(u_b\) | \(u_c\) | \(u_d\) |
|:---|---:|---:|---:|---:|
| \(k_{0,1}\) | 0 | 0 | 2940 | 13020 |
| \(k_{1,0}\) | 0 | 0 | 87318 | 120582 |
| \(k_{0,4}\) | 0 | 0 | 0 | 10752 |
| \(k_{4,0}\) | 0 | 1 | -3136 | 0 |
| \(k_{0,6}\) | 0 | 0 | 9282 | 6930 |
| \(k_{6,0}\) | 0 | 0 | 21216 | 67584 |
| \(k_{1,7}\) | 0 | 0 | 29835 | 22275 |
| \(k_{7,1}\) | 0 | 0 | -3360 | 0 |
| \(k_{2,4}\) | 1 | 0 | 0 | 10752 |
| \(k_{4,2}\) | 0 | 1 | 3136 | 13888 |
| \(k_{2,7}\) | -3 | 0 | 32487 | 24255 |
| \(k_{7,2}\) | 0 | 0 | 77616 | 107184 |
| \(k_{2,9}\) | 1 | 0 | 0 | 0 |
| \(k_{9,2}\) | 0 | 0 | 6272 | 13888 |
| \(k_{3,4}\) | 0 | 0 | 0 | 59136 |
| \(k_{4,3}\) | 0 | -3 | 0 | 0 |
| \(k_{5,9}\) | 0 | 0 | 0 | 59136 |
| \(k_{9,5}\) | 0 | 0 | -9408 | 0 |
| \(k_{8,9}\) | 0 | 0 | 0 | 66528 |
| \(k_{9,8}\) | 0 | 0 | 0 | 10080 |

Normalize by taking the four free rates

\[
a=k_{2,9},\quad b=k_{4,3},\quad c=k_{9,5},\quad d=k_{9,8}.
\]

Then every conic-preserving rate vector, and no other one, is

\[
k=a u_a-\frac b3u_b-\frac{c}{9408}u_c+\frac d{10080}u_d.
\]

Equivalently, its twenty entries in the displayed rate order are

\[
\begin{array}{rclcrcl}
k_{0,1}&=&(62d-15c)/48,&&k_{1,0}&=&33(58d-45c)/160,\\
k_{0,4}&=&16d/15,&&k_{4,0}&=&(c-b)/3,\\
k_{0,6}&=&(154d-221c)/224,&&k_{6,0}&=&(9856d-3315c)/1470,\\
k_{1,7}&=&45(154d-221c)/3136,&&k_{7,1}&=&5c/14,\\
k_{2,4}&=&(15a+16d)/15,&&k_{4,2}&=&(62d-15b-15c)/45,\\
k_{2,7}&=&(154d-192a-221c)/64,&&k_{7,2}&=&11(58d-45c)/60,\\
k_{2,9}&=&a,&&k_{9,2}&=&2(31d-15c)/45,\\
k_{3,4}&=&88d/15,&&k_{4,3}&=&b,\\
k_{5,9}&=&88d/15,&&k_{9,5}&=&c,\\
k_{8,9}&=&33d/5,&&k_{9,8}&=&d.
\end{array}
\]

## The positive cone

All twenty directed rates are strictly positive exactly when

\[
a>0,\quad b>0,\quad c>0,\quad d>0,\quad b<c,\quad
192a+221c<154d.
\]

Necessity follows from the four free rates together with
\(k_{4,0}=(c-b)/3\) and
\(k_{2,7}=(154d-192a-221c)/64\).  For a manifest sufficiency certificate,
write

\[
c=b+h,\qquad
d=\frac{192a+221(b+h)+s}{154},qquad a,b,h,s>0.
\]

After this substitution every displayed rate is a linear form in
\(a,b,h,s\) with nonnegative rational coefficients and at least one strictly
positive coefficient.  The verifier checks all eighty coefficients exactly.
This gives a rational bijection from the open positive orthant to the entire
positive rate cone.

Every point of this cone assigns a positive rate to every directed edge of
the same fixed support.  Hence the network remains reversible and connected,
and its vector field continues to vanish identically on the same positive
conic.

The rate vector in `network.csv` has

\[
(a,b,c,d)=(3920,3920,15680,658560)
=3920(1,1,4,168).
\]

Its orthant coordinates are

\[
(a,b,h,s)=(3920,3920,11760,97200320),
\]

so it is a strict interior point, not a boundary specialization.

## Generic absence of a common factor

There is also a rigorous generic statement.  Homogenize each coordinate
polynomial to degree three.  In the projective space of triples of cubic
forms, the locus having a common homogeneous factor of a fixed degree
\(e=1,2,3\) is the image of the projective multiplication morphism

\[
\mathbb P(V_e)\times
\mathbb P(V_{3-e}^{\oplus3})
\longrightarrow
\mathbb P(V_3^{\oplus3}).
\]

Here the \(V_j\) are spaces of forms in the homogenizing variables
\(x,y,z,w\).  Denote the projective image by \(\Sigma_e\).  It is closed
because the source is projective.  Its affine cone
\(\widehat\Sigma_e\subset V_3^{\oplus3}\), including the zero triple, is
closed as well.  Thus the finite union of these affine cones pulls back along
the linear four-parameter rate map to a closed subset of affine parameter
space.  This explicitly includes the parameter-space origin, where all three
coordinates vanish and projectivization itself would be undefined.

Every affine common factor homogenizes to a homogeneous common factor, so
the complement of this closed locus consists entirely of affine-coprime
fields.  The closed homogeneous locus may also include degree-drop limits
with a factor \(w\), which causes no problem for this implication.

The same argument works geometrically, not merely over `QQ`.  If rational
forms had a common irreducible factor over \(\mathbb C\), rationality would
force every Galois conjugate of that factor to divide every coordinate.  The
product of the distinct conjugates (equivalently, its norm up to repeated
associates and a scalar) is then a nonconstant polynomial over \(\mathbb Q\)
dividing every coordinate.  Therefore gcd one over \(\mathbb Q\) rules out
common factors after extension to \(\mathbb R\) or \(\mathbb C\).

The verifier reconstructs the original integer specialization and checks
both its affine and homogenized coordinate gcds over \(\mathbb Q\) are
exactly one.  By the scalar-extension observation it lies outside the
geometric common-factor cones.  Therefore the family contains a nonempty
Zariski-open subset of geometrically coprime fields.  In this precise sense,
coprimality is generic in the fixed-support family.
