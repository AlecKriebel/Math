# An exact degree-10 cap-SDP bound \(B(5)\leq35\)

## Theorem and status

Let \(B(5)\) be the largest size of a kissing code in \(S^4\) contained
in a closed hemisphere.  Then
\[
\boxed{B(5)\leq35.}                               \tag{1}
\]

The proof is computer-assisted but exact.  Its only computer-certified step
is the evaluation of a fixed rational polynomial on a compact
three-dimensional semialgebraic domain.  The certificate contains rational
Gram factors, and the verifier uses only Python's standard library and
`fractions.Fraction`; it makes no floating-point sign or PSD decision.

This is deliberately **not** a claim that \(B(5)\leq33\).  Bachoc and
Vallentin reported a numerical degree-10 cap-SDP value with integer
consequence \(33\), but their numerical solver output is not an exact
certificate.  The present rational certificate has the weaker exact
objective \(679/19\), which is enough for (1).

## 1. The axisymmetric positive kernels

Fix the north pole \(e\in S^4\).  For two points \(x,y\in S^4\), write
\[
u=\langle e,x\rangle,\qquad
v=\langle e,y\rangle,\qquad
t=\langle x,y\rangle.
\]
Let \(P_i^{(m)}\) be the normalized zonal polynomial on \(S^{m-1}\):
\[
P_0^{(m)}=1,\quad P_1^{(m)}=z,
\]
\[
(i+m-3)P_i^{(m)}(z)
=(2i+m-4)zP_{i-1}^{(m)}(z)-(i-1)P_{i-2}^{(m)}(z).                 \tag{2}
\]
Define polynomialized equatorial kernels \(Q_k\) by
\[
Q_0=1,\qquad Q_1=t-uv,
\]
\[
(k+1)Q_k
=2k(t-uv)Q_{k-1}
-(k-1)(1-u^2)(1-v^2)Q_{k-2}.                    \tag{3}
\]
Equivalently,
\[
Q_k=((1-u^2)(1-v^2))^{k/2}
P_k^{(4)}\!\left(
\frac{t-uv}{\sqrt{(1-u^2)(1-v^2)}}\right),
\]
with (3) providing its polynomial continuation at the boundary.

For \(0\leq k\leq10\), let \(Y_k(u,v,t)\) be the
\((11-k)\)-square matrix
\[
(Y_k)_{ij}
=P_i^{(5+2k)}(u)P_j^{(5+2k)}(v)Q_k(u,v,t),
\qquad 0\leq i,j\leq10-k,                       \tag{4}
\]
and put
\[
\overline Y_k(u,v,t)
=\frac{Y_k(u,v,t)+Y_k(v,u,t)}2.                 \tag{5}
\]

### Positivity lemma

For every finite \(C\subset S^4\),
\[
\sum_{x,y\in C}\overline Y_k(
\langle e,x\rangle,\langle e,y\rangle,\langle x,y\rangle)
\succeq0.                                       \tag{6}
\]

Here is a direct feature-map proof in exactly the normalization (4), with
no omitted constants to track.  Put
\[
r_x=x-\langle e,x\rangle e\in e^\perp\cong\mathbb R^4,\qquad
p_k(u)=\bigl(P_0^{(5+2k)}(u),\ldots,
P_{10-k}^{(5+2k)}(u)\bigr)^{\mathsf T}.
\]
The addition formula for degree-\(k\) homogeneous harmonic polynomials on
\(\mathbb R^4\) gives a basis \(H_{k,a}\) and a constant \(c_k>0\) such
that
\[
Q_k(u,v,t)=c_k\sum_a H_{k,a}(r_x)H_{k,a}(r_y).   \tag{6a}
\]
For nonzero \(r_x,r_y\), this is the usual zonal addition formula after
factoring out \(\|r_x\|^k\|r_y\|^k\); recurrence (3) shows that it extends
polynomially to \(r_x=0\) or \(r_y=0\).  Equations (4) and (6a) now give
\[
\begin{aligned}
\sum_{x,y\in C}Y_k(u_x,u_y,\langle x,y\rangle)
&=c_k\sum_a
\left(\sum_{x\in C}p_k(u_x)H_{k,a}(r_x)\right)
\left(\sum_{x\in C}p_k(u_x)H_{k,a}(r_x)\right)^{\mathsf T}\\
&\succeq0.
\end{aligned}
\]
The ordered-pair sum is symmetric, so replacing \(Y_k\) by (5) leaves it
unchanged.  This proves (6).

This normalization is important: the certificate and verifier use (2)--(5)
with every \(\lambda_{ij}\) omitted.

## 2. The fixed rational dual polynomial

The certificate
[`../certificates/one_sided_cap_degree10_bound.json`](../certificates/one_sided_cap_degree10_bound.json)
stores, for every \(0\leq k\leq10\), an integer matrix \(A_k\) and the
common denominator \(10^8\).  Define
\[
L_k=10^{-8}A_k,\qquad F_k=L_kL_k^{\mathsf T}.     \tag{7}
\]
Thus every \(F_k\succeq0\) by an exact displayed Gram factorization; no
principal-minor calculation and no near-PSD tolerance is involved.

Set
\[
F(u,v,t)=\sum_{k=0}^{10}
\langle F_k,\overline Y_k(u,v,t)\rangle,          \tag{8}
\]
where \(\langle A,B\rangle=\operatorname{Tr}(AB^{\mathsf T})\).
Expanding (2)--(8) gives a rational polynomial with 506 nonzero monomials
and multidegree exactly \((10,10,10)\).

The exact domain audit proves
\[
F(u,u,1)\leq33\qquad(0\leq u\leq1),              \tag{9}
\]
and
\[
F(u,v,t)\leq-\frac{19}{20}                       \tag{10}
\]
throughout
\[
\mathcal D=
\left\{\begin{array}{l}
0\leq u\leq1,\quad0\leq v\leq1,\quad-1\leq t\leq1/2,\\
1+2uvt-u^2-v^2-t^2\geq0.
\end{array}\right.                               \tag{11}
\]
The last inequality is the determinant of the \(3\times3\) Gram matrix of
\(e,x,y\).  Hence (11) is the full compact pair domain needed for distinct
points of a code in the closed hemisphere.  We do not impose \(u\leq v\);
the audit covers both orders.

## 3. Exact Bernstein verification of (9)--(10)

For completeness, here is the entire certification mechanism.

### Bernstein enclosure lemma

On \([0,1]^r\), write a polynomial in tensor Bernstein form
\[
p(z)=\sum_{\alpha}b_\alpha
\prod_{\ell=1}^r
\binom{d_\ell}{\alpha_\ell}
z_\ell^{\alpha_\ell}(1-z_\ell)^{d_\ell-\alpha_\ell}.
\]
Every basis function is nonnegative and their sum is \(1\).  Therefore
\[
\min_\alpha b_\alpha\leq p(z)\leq\max_\alpha b_\alpha             \tag{12}
\]
on the entire closed box.

The de Casteljau midpoint recursion produces the exact Bernstein
coefficients on the two half-boxes.  The two closed children have union
equal to their closed parent and meet on the bisecting face, so no point,
including a boundary point, is lost.  Repeating this independently in
each coordinate proves that all terminal boxes cover the initial box.

The verifier computes every coefficient as a `Fraction`.  Thus (12) uses
neither nearest rounding nor an unrecorded tolerance.  In interval language,
the bounds are already exact outward bounds: the lower endpoint is the exact
minimum of rational coefficients and the upper endpoint is their exact
maximum.

### Diagonal audit

Substitute \(v=u,t=1\) in \(33-F\), convert the resulting univariate
rational polynomial to Bernstein form on \([0,1]\), and bisect at exact
midpoints.  Three terminal intervals suffice, and each has nonnegative
minimum Bernstein coefficient.  This proves (9), including \(u=0,1\).

### Full pair-domain audit

Apply the exact affine substitution
\[
t=-1+\frac32s,\qquad 0\leq s\leq1,
\]
so the initial compact box is exactly
\[
[0,1]_u\times[0,1]_v\times[0,1]_s.               \tag{13}
\]
Let
\[
H=-\frac{19}{20}-F,\qquad
\Delta=1+2uvt-u^2-v^2-t^2.
\]
Both are converted exactly to tensor Bernstein form of degree 10 in each
variable.  Starting from (13), the verifier bisects \(u,v,s\) cyclically
at exact midpoints.  A box is terminal in exactly one of two ways:

1. `infeasible`: the maximum Bernstein coefficient of \(\Delta\) is
   negative, so every point in the box lies outside (11);
2. `proved`: the minimum Bernstein coefficient of \(H\) is nonnegative,
   so (10) holds throughout the box.

The deterministic tree has 2,483 leaves: 1,090 infeasible leaves and 1,393
proved leaves.  Its maximum leaf depth is 26.  The ordered terminal
manifest has SHA-256
\[
\texttt{c4de17e5b741b824ed0b45d2af74a3927165db13c2ee717d8461efc78a028743}.
\]
The root box, branch rule, terminal rules, counts, depth, and digest are
stored in the certificate.  The verifier rebuilds the full tree rather than
trusting a solver-generated leaf list.  Since every nonterminal parent is
replaced by its two exact half-boxes, the terminal leaves cover (13);
since every feasible leaf is of type `proved`, (10) follows on all of
\(\mathcal D\).

The factor payload has a separate SHA-256 digest
\[
\texttt{d2c2bf6959c0d5be7c3ee182d4ddc8ae891c5e6df2d74632fb631623bc3585cc}.
\]
The tests alter a factor entry and the tree digest separately and check that
both changes are rejected before the expensive domain traversal.

## 4. Cap-SDP summation and the integer conclusion

Let \(C\subset S^4\) lie in the closed hemisphere centered at \(e\), and
write \(n=|C|\).  For each \(k\), let \(M_k\) be the PSD matrix in (6).
Because \(F_k=L_kL_k^{\mathsf T}\),
\[
\langle F_k,M_k\rangle
=\operatorname{Tr}(L_k^{\mathsf T}M_kL_k)\geq0.
\]
Summing this identity and using (8) gives
\[
\sum_{x,y\in C}F(
\langle e,x\rangle,\langle e,y\rangle,\langle x,y\rangle)\geq0.   \tag{14}
\]
Every diagonal ordered pair satisfies (9).  Every distinct ordered pair
lies in (11), including all height, contact, and determinant boundaries,
and satisfies (10).  Hence
\[
0\leq 33n-\frac{19}{20}n(n-1).
\]
For \(n>0\),
\[
n\leq1+\frac{33}{19/20}
=\frac{679}{19}<36.
\]
Since \(n\) is integral, \(n\leq35\).  This proves (1).

Equivalently, scaling every \(F_k\) by \(20/19\) gives the standard dual
normalization
\[
F_{\rm scaled}\leq-1\quad\hbox{off diagonal},\qquad
F_{\rm scaled}(u,u,1)\leq\frac{660}{19},
\]
with dual objective
\[
1+\frac{660}{19}=\frac{679}{19}<36.              \tag{15}
\]
Thus any strict exact cap-dual objective below \(34\) would indeed prove
\(B(5)\leq33\), but (15), not such a stronger unverified value, is what the
present certificate proves.

## 5. Consequences for a hypothetical 41-code

Assume \(C\subset S^4\) is a 41-point kissing code.  For every unit vector
\(u\), the closed hemisphere
\[
H_u=\{x:\langle u,x\rangle\geq0\}
\]
contains at most 35 code points.  Its complement is the open hemisphere
\(\{x:\langle u,x\rangle<0\}\), so
\[
\#\{x\in C:\langle u,x\rangle<0\}\geq6.          \tag{16}
\]
Applying the same statement to \(-u\) gives at least six points in the
opposite open hemisphere as well.  Points on the separating great sphere
belong to both closed hemispheres but to neither open complement; the
closed/open convention in (16) therefore has no boundary gap.

Thus every closed halfspace through the origin contains at least six points
of \(C\).  More generally, a closed affine halfspace containing the origin
contains its parallel closed halfspace whose boundary passes through the
origin, so the origin has Tukey depth at least six.  After deleting any set
\(D\subset C\) of at most five points, each
open side of every hyperplane through the origin still contains a point of
\(C\setminus D\).  If the origin were not in the interior of
\(\operatorname{conv}(C\setminus D)\), a supporting or strict separating
hyperplane through the origin would place all remaining points in one
closed side, leaving the opposite open side empty.  Therefore
\[
\boxed{0\in\operatorname{int}\operatorname{conv}(C\setminus D)
\quad\text{for every }|D|\leq5.}                 \tag{17}
\]

The independent tangent-neighborhood lemma in
[`tangent_nonnegative_neighborhood.md`](tangent_nonnegative_neighborhood.md)
is stronger in vertex directions: every code point has at least seven
strictly negative neighbors.  The cap-SDP result is stronger for arbitrary
directions and is what yields Tukey depth six.

## 6. Boundary and numerical-rigor audit

- Hemisphere heights \(u=0\) and \(v=0\) are included.
- The north-pole heights \(u=1\) and \(v=1\) are included.
- Contact pairs \(t=1/2\) are included; the inequality is not made strict.
- Antipodal inner product \(t=-1\) is included whenever the Gram determinant
  permits it.
- Degenerate triples with \(\Delta=0\) remain in the feasible domain.
  Only boxes with the **strict** exact bound \(\max\Delta<0\) are discarded.
- A proved leaf accepts the non-strict exact condition \(\min H\geq0\), so
  zeros on a face are retained.
- Child boxes are closed and cover their parent exactly.  Overlap on a
  bisecting face is harmless.
- Every matrix is PSD because it is reconstructed as the exact product
  \(L_kL_k^{\mathsf T}\).
- The floating-point source eigenvalues and entry-change diagnostics stored
  with the certificate are discovery metadata only.  The verifier ignores
  them.
- All polynomial recurrences, substitutions, Gram products, Bernstein
  conversions, signs, comparisons, branch decisions, and hashes are
  recomputed from exact integers and rational arithmetic.

## 7. Reproduction and dependency map

From the project directory run

```sh
python3 verifiers/verify_one_sided_cap_degree10.py
python3 -m unittest tests.test_one_sided_cap_degree10 -v
```

On the reference machine the verifier uses about 30 MB of memory and takes
under one minute.  The discovery scripts are separate:

- `experiments/search_one_sided_cap_sdp.py` searches sampled duals and is
  not trusted;
- `experiments/rationalize_one_sided_cap_candidate.py` converts a numerical
  matrix candidate into rational Gram factors and is not trusted;
- the verifier reconstructs all proof obligations from the final fixed
  certificate.

```text
axisymmetric harmonic addition formula
                  |
                  v
       sum of modified Y_k kernels is PSD
                  |
 exact Gram factors F_k = L_k L_k^T
                  |
                  v
   fixed rational polynomial F(u,v,t)
          /                         \
 exact diagonal Bernstein audit   exact full-domain tree
       F(u,u,1)<=33                 F<=-19/20
          \                         /
           cap-SDP ordered-pair sum
                      |
                      v
               |C| <= 679/19 < 36
                      |
                      v
                    B(5)<=35
                      |
                      v
       open-hemisphere count >=6, Tukey depth >=6,
       deletion-five robust interior convex hull
```

## Source context

The kernel and cap-SDP formulation is the one in Christine Bachoc and Frank
Vallentin, *Semidefinite programming, multivariate orthogonal polynomials,
and codes in spherical caps*, European Journal of Combinatorics 30 (2009),
625--637.  Their theorem supplies the harmonic kernel framework; the rational
matrices, exact \(679/19\) objective, and complete Bernstein verification here
are independent artifacts in this repository.
