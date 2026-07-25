# An exact degree-11 cap-SDP bound \(B(5)\leq34\)

## Theorem

Let \(B(5)\) be the largest size of a kissing code in \(S^4\) contained in
a closed hemisphere.  Then
\[
\boxed{B(5)\leq34.}                                      \tag{1}
\]

This is a computer-assisted exact theorem.  The certificate consists of
integer Gram factors.  The verifier uses only Python's standard library and
`fractions.Fraction`; all PSD statements, polynomial coefficients,
Bernstein bounds, branch decisions, and objective comparisons are exact.
The numerical SDP that discovered the factors is not part of the proof.

## 1. Positive axisymmetric kernels

Fix \(e\in S^4\), and for \(x,y\in S^4\) put
\[
u=\langle e,x\rangle,\qquad v=\langle e,y\rangle,\qquad
t=\langle x,y\rangle.
\]
Let \(P_i^{(m)}\) be the normalized zonal polynomial on \(S^{m-1}\):
\[
P_0^{(m)}=1,\quad P_1^{(m)}=z,
\]
\[
(i+m-3)P_i^{(m)}(z)
=(2i+m-4)zP_{i-1}^{(m)}(z)-(i-1)P_{i-2}^{(m)}(z).          \tag{2}
\]
Define
\[
Q_0=1,\qquad Q_1=t-uv,
\]
\[
(k+1)Q_k
=2k(t-uv)Q_{k-1}
-(k-1)(1-u^2)(1-v^2)Q_{k-2}.                              \tag{3}
\]
For \(0\leq k\leq11\), set
\[
p_k(u)=\bigl(P_0^{(5+2k)}(u),\ldots,
P_{11-k}^{(5+2k)}(u)\bigr)^{\mathsf T},
\]
\[
Y_k(u,v,t)=p_k(u)p_k(v)^{\mathsf T}Q_k(u,v,t),\qquad
\overline Y_k=\frac{Y_k(u,v,t)+Y_k(v,u,t)}2.                \tag{4}
\]

For every finite \(C\subset S^4\),
\[
M_k(C):=\sum_{x,y\in C}\overline Y_k(u_x,u_y,\langle x,y\rangle)
\succeq0.                                                  \tag{5}
\]
Indeed, write \(r_x=x-u_xe\in e^\perp\cong\mathbb R^4\).
The addition formula for degree-\(k\) homogeneous harmonics gives a basis
\(H_{k,a}\) and \(c_k>0\) such that
\[
Q_k(u_x,u_y,\langle x,y\rangle)
=c_k\sum_aH_{k,a}(r_x)H_{k,a}(r_y).                         \tag{6}
\]
For nonzero \(r_x,r_y\), this is the ordinary zonal addition formula after
factoring their norms; recurrence (3) supplies the polynomial continuation
at the poles.  Therefore the ordered-pair sum of \(Y_k\) equals
\[
c_k\sum_a
\left(\sum_{x\in C}p_k(u_x)H_{k,a}(r_x)\right)
\left(\sum_{x\in C}p_k(u_x)H_{k,a}(r_x)\right)^{\mathsf T},
\]
which is PSD.  Symmetrization does not change the ordered-pair sum, proving
(5).  This direct feature proof uses exactly the normalization implemented
by the certificate; there are no omitted \(\lambda_{ij}\) constants.

## 2. Fixed rational dual polynomial

The certificate
[`../certificates/one_sided_cap_degree11_bound.json`](../certificates/one_sided_cap_degree11_bound.json)
stores an integer matrix \(A_k\) for each \(0\leq k\leq11\).  Define
\[
L_k=10^{-9}A_k,\qquad F_k=L_kL_k^{\mathsf T}\succeq0,       \tag{7}
\]
and
\[
F(u,v,t)=\sum_{k=0}^{11}
\langle F_k,\overline Y_k(u,v,t)\rangle.                    \tag{8}
\]
Expansion of (2)--(8) gives a rational polynomial with 650 nonzero
monomials and multidegree \((11,11,11)\).

The exact certificate audit proves
\[
F(u,u,1)\leq\frac{1647}{50}\qquad(0\leq u\leq1),            \tag{9}
\]
and
\[
F(u,v,t)\leq-\frac{969}{1000}                               \tag{10}
\]
on the complete closed pair domain
\[
\mathcal D=\left\{\begin{array}{l}
0\leq u,v\leq1,\quad -1\leq t\leq1/2,\\
\Delta(u,v,t):=1+2uvt-u^2-v^2-t^2\geq0.
\end{array}\right.                                         \tag{11}
\]
The determinant condition in (11) is precisely the determinant of the Gram
matrix of \(e,x,y\).  Together with the displayed interval constraints it
is the complete domain for distinct pairs in a closed hemisphere.

## 3. Exact Bernstein certificate

For a polynomial on \([0,1]^r\), its tensor Bernstein basis functions are
nonnegative and sum to one.  Hence the minimum and maximum Bernstein
coefficients are exact lower and upper bounds on the whole closed box.
The de Casteljau midpoint recursion gives the exact coefficients on two
closed half-boxes whose union is their parent.

For (9), the verifier substitutes \(v=u,t=1\) in
\(1647/50-F\).  Three terminal dyadic intervals have nonnegative minimum
Bernstein coefficient.

For (10), it makes the exact substitution
\[
t=-1+\frac32s,\qquad (u,v,s)\in[0,1]^3,
\]
and sets
\[
H=-\frac{969}{1000}-F.
\]
It converts both \(H\) and \(\Delta\) to degree-11 tensor Bernstein form and
bisects \(u,v,s\) cyclically.  A leaf is accepted only if

1. its maximum Bernstein coefficient for \(\Delta\) is strictly negative,
   making the entire box infeasible; or
2. its minimum Bernstein coefficient for \(H\) is nonnegative.

The rebuilt tree has 5,995 leaves: 2,848 are determinant-infeasible and
3,147 prove \(H\geq0\).  Its maximum depth is 31.  The ordered leaf digest is
```
3ffd08afa66bcd12e52399e392c09fda237f8bab18fc1af9a8090e76f1f81f65
```
and the independent Gram-factor payload digest is
```
723d5521951ce45d236116016a69e7e8e510b8e7ba1f0338f7c1d6fffe507257
```
The verifier reconstructs the tree and both hashes; it does not trust a
stored solver leaf list.

Every computation in this audit is an integer operation or a `Fraction`
operation.  Thus a negative coefficient is never rounded upward, a
near-positive matrix is never treated as PSD, and no tolerance occurs in
the proof.

## 4. Summation and integer bound

Let \(C\) be a kissing code in the closed hemisphere centered at \(e\), and
write \(n=|C|\).  From (5) and (7),
\[
\langle F_k,M_k(C)\rangle
=\operatorname{Tr}(L_k^{\mathsf T}M_k(C)L_k)\geq0.
\]
Summing over \(k\) gives
\[
\sum_{x,y\in C}F(u_x,u_y,\langle x,y\rangle)\geq0.          \tag{12}
\]
The \(n\) diagonal terms satisfy (9), and the \(n(n-1)\) ordered distinct
terms satisfy (10).  Consequently
\[
0\leq\frac{1647}{50}n-\frac{969}{1000}n(n-1).
\]
For \(n>0\),
\[
n\leq1+\frac{1647/50}{969/1000}
=\frac{11303}{323}<35.                                     \tag{13}
\]
Since \(n\) is integral, \(n\leq34\), proving (1).

Equivalently, scaling all blocks by \(1000/969\) gives the standard
off-diagonal normalization \(-1\), diagonal bound \(10980/323\), and exact
dual objective \(11303/323\).

## 5. Consequences for a hypothetical 41-code

If \(C\) were a 41-point kissing code, every closed hemisphere would contain
at most 34 points.  Therefore, for every nonzero direction \(a\),
\[
\#\{x\in C:\langle a,x\rangle<0\}\geq7,
\qquad
\#\{x\in C:\langle a,x\rangle>0\}\geq7.                     \tag{14}
\]
Points on the separating great sphere cause no gap: they lie in both closed
hemispheres and neither open complement.

Every affine closed halfspace containing the origin contains a parallel
closed halfspace through the origin, so (14) gives origin Tukey depth at
least seven.  After deleting any \(D\subset C\) with \(|D|\leq6\), both open
sides of every origin hyperplane still meet \(C\setminus D\).  The separating
hyperplane theorem therefore gives
\[
\boxed{0\in\operatorname{int}\operatorname{conv}(C\setminus D)
\quad\text{whenever }|D|\leq6.}                              \tag{15}
\]

There is also a vertexwise sign-degree consequence.  Fix \(x\in C\), and
among the other 40 points write
\[
p(x)=\#\{y:\langle x,y\rangle>0\},\quad
z(x)=\#\{y:\langle x,y\rangle=0\},\quad
r(x)=\#\{y:\langle x,y\rangle<0\}.
\]
The closed hemisphere centered at \(x\) contains \(x\) itself together with
the \(p(x)+z(x)\) nonnegative neighbors.  The closed hemisphere centered at
\(-x\) contains the \(r(x)+z(x)\) nonpositive neighbors but not \(x\).
Consequently
\[
1+p(x)+z(x)\leq34,\qquad r(x)+z(x)\leq34.                    \tag{16}
\]
Since \(p(x)+z(x)+r(x)=40\), every vertex satisfies
\[
\boxed{r(x)\geq7,\qquad p(x)\geq6,}                           \tag{17}
\]
together with the zero-sensitive inequalities
\(p(x)+z(x)\leq33\) and \(r(x)+z(x)\leq34\).  Here \(p(x)\)
includes all contact neighbors and all shallower strictly positive
neighbors; no symmetry, antipodality, or rigidity is assumed.

## 6. Boundary and failure audit

- Heights \(u,v=0\) and \(u,v=1\) are included.
- Contacts \(t=1/2\), antipodal values when feasible, and all degenerate
  triples with \(\Delta=0\) are included.
- A box is discarded only when the exact strict inequality
  \(\max\Delta<0\) holds.
- Proved leaves allow the non-strict condition \(\min H\geq0\).
- Closed child boxes cover their parent and overlap harmlessly on the split
  face.
- Every \(F_k\) is PSD by the displayed exact Gram product, independently of
  the discovery eigenvalue diagnostics.
- The first numerical degree-11 candidate is not used.  Its proposed target
  failed at the exact feasible dyadic point
  \[
  (u,v,t)=\left(\frac{4791}{65536},\frac5{64},-\frac{113}{128}\right),
  \]
  where exact evaluation gives \(F>-969/1000\).  This failure motivated a
  denser symmetry-plane search but was not hidden or rounded away.
- The successful source matrices were multiplied by the discovery scale
  \(997/1000\) before rational Gram-factor extraction.  The proof uses only
  the resulting integers in (7), not the floating-point source or that
  provenance scale.

## 7. Reproduction and dependency map

Run from the project root:

```sh
python3 verifiers/verify_one_sided_cap_degree11.py
python3 -m unittest tests.test_one_sided_cap_degree11 -v
```

The proof dependencies are
```text
homogeneous-harmonic addition formula
                  |
                  v
       ordered sums of Y_k are PSD
                  |
 exact Gram factors F_k = L_k L_k^T
                  |
                  v
       rational F(u,v,t), 650 terms
          /                         \
 exact diagonal audit          exact domain tree
 F(u,u,1)<=1647/50              F<=-969/1000
          \                         /
             ordered-pair summation
                        |
                        v
             |C| <= 11303/323 < 35
                        |
                        v
                      B(5)<=34
```

The exploratory search and rationalization programs live in `experiments/`;
they are not called by the verifier.
