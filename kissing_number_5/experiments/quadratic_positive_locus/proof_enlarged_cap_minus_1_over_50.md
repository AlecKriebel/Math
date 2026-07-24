# An exact enlarged-cap bound at height \(-1/50\)

## Theorem

Fix \(e\in S^4\).  Let \(C\subset S^4\) satisfy
\[
\langle x,y\rangle\leq\frac12\qquad(x\ne y,\ x,y\in C)
\]
and
\[
\langle e,x\rangle\geq-\frac1{50}\qquad(x\in C).
\]
Then
\[
\boxed{|C|\leq39.}
\]

This is a computer-assisted theorem with exact rational Gram factors and an
exact Bernstein-domain verifier.  The exploratory solver and its
floating-point matrices are not proof dependencies.

## 1. Polynomial kernel

For \(u=\langle e,x\rangle\), \(v=\langle e,y\rangle\), and
\(t=\langle x,y\rangle\), define normalized Gegenbauer polynomials by
\[
P_0^{(n)}(z)=1,\qquad P_1^{(n)}(z)=z,
\]
\[
P_m^{(n)}(z)=
\frac{(2m+n-4)zP_{m-1}^{(n)}(z)-(m-1)P_{m-2}^{(n)}(z)}
     {m+n-3}.
\tag{1}
\]
Define
\[
Q_0=1,\qquad Q_1=t-uv,
\]
\[
Q_k=
\frac{2k(t-uv)Q_{k-1}-(k-1)(1-u^2)(1-v^2)Q_{k-2}}
     {k+1}.
\tag{2}
\]
For \(0\leq k\leq8\), let \(F_k\) be the exact rational matrix reconstructed
from block \(k\) in
[`enlarged_cap_minus_1_over_50_exact_factors.json`](enlarged_cap_minus_1_over_50_exact_factors.json).
If \(L_k\) is the displayed integer matrix divided by \(10^6\), then
\[
F_k=L_kL_k^{\mathsf T}\succeq0
\tag{3}
\]
exactly.  The final block is the zero matrix, represented by an empty
factor.

For \(0\leq i,j\leq8-k\), put
\[
(Y_k)_{ij}(u,v,t)=
Q_k(u,v,t)
\frac{
P_i^{(5+2k)}(u)P_j^{(5+2k)}(v)+
P_j^{(5+2k)}(u)P_i^{(5+2k)}(v)}
2
\tag{4}
\]
and define
\[
F(u,v,t)=\sum_{k=0}^8\langle F_k,Y_k(u,v,t)\rangle.
\tag{5}
\]
The conventional positive normalization constants in the
Bachoc--Vallentin matrices have been omitted by a positive diagonal
congruence.  The spherical-harmonic addition formula and (3) therefore give
\[
\sum_{x,y\in C}
F(\langle e,x\rangle,\langle e,y\rangle,\langle x,y\rangle)
\geq0
\tag{6}
\]
for every finite \(C\subset S^4\).  This positivity statement does not
require any cap restriction.

## 2. Exact domain inequalities

The verifier reconstructs (5) in the rational power basis and proves
\[
F(u,u,1)\leq35
\qquad\left(-\frac1{50}\leq u\leq1\right)
\tag{7}
\]
and
\[
F(u,v,t)\leq-\frac9{10}
\tag{8}
\]
on the complete closed domain
\[
\mathcal D=\left\{
\begin{array}{l}
-1/50\leq u,v\leq1,\quad -1\leq t\leq1/2,\\
1+2uvt-u^2-v^2-t^2\geq0.
\end{array}
\right.
\tag{9}
\]
The last inequality is the determinant of the Gram matrix of \(e,x,y\).
Thus every geometrically realizable distinct pair from the cap occurs in
\(\mathcal D\).

## 3. Exact Bernstein certificate

The affine substitution
\[
u=-\frac1{50}+\frac{51}{50}a,\qquad
v=-\frac1{50}+\frac{51}{50}b,\qquad
t=-1+\frac32s
\tag{10}
\]
maps the containing box to \([0,1]^3\).  All substitutions and
power-to-Bernstein conversions use `Fraction` arithmetic.

For (7), the verifier converts \(35-F(u,u,1)\), a degree-16 polynomial, to
the univariate Bernstein basis.  Three dyadic leaves, of maximum depth two,
have nonnegative Bernstein coefficients.

For (8), put \(H=-9/10-F\).  Starting with the full cube, the verifier
bisects \(a,b,s\) cyclically at exact midpoints.  A leaf is accepted only
if either:

1. the maximum Bernstein coefficient of the transformed Gram determinant
   is strictly negative, so the entire box is infeasible; or
2. the minimum Bernstein coefficient of \(H\) is nonnegative.

Nonnegativity of every Bernstein coefficient implies nonnegativity of the
polynomial on the whole box.  Closed dyadic children cover their parent,
including their shared boundary.

The exact tree has 1,344 leaves and maximum depth 21:

- 630 determinant-infeasible leaves;
- 714 leaves proving \(H\geq0\).

The ordered leaf digest is

```text
1bf44242737474073736f8ce772e6433bab6fe4ea5d869fb10a660f413069ef1
```

## 4. Summation

Write \(N=|C|>0\).  Combining (6)--(8) gives
\[
0\leq
\sum_{x,y\in C}F(u_x,u_y,\langle x,y\rangle)
\leq35N-\frac9{10}N(N-1).
\]
Consequently
\[
N\leq1+\frac{35}{9/10}=\frac{359}{9}<40.
\]
Since \(N\) is integral, \(N\leq39\).

## 5. Boundary and numerical rigor

- Heights \(u=-1/50\) and \(v=-1/50\) are included.
- Contacts \(t=1/2\), both determinant-zero sheets, feasible pole strata,
  and all intersections of these faces are included.
- An infeasible leaf requires a strict exact upper bound \(<0\) for the
  determinant.  A proved leaf permits the non-strict exact lower bound
  \(H\geq0\).
- Every kernel block is an exact product \(L_kL_k^{\mathsf T}\); no
  near-PSD judgment occurs.
- The targets \(-9/10\), \(35\), and \(359/9<40\) are rational and checked
  without rounding.
- The solver status `optimal_inaccurate`, its tiny negative eigenvalues,
  and all random audits belong only to discovery.  PSD projection was
  followed by exact factor extraction and a fresh full-domain proof.
- Run the verifier without Python's `-O` flag because assertions are proof
  checks.

## 6. Reproduction and dependency map

From the repository root:

```sh
python3 \
  experiments/quadratic_positive_locus/verify_enlarged_cap_minus_1_over_50.py
python3 -m unittest \
  experiments.quadratic_positive_locus.test_enlarged_cap_minus_1_over_50 -v
```

The verifier uses only the Python standard library.

```text
integer Gram factors L_k
          |
          v
exact PSD blocks F_k=L_k L_k^T + harmonic addition formula
          |
          v
positive ordered-pair kernel F
       /                         \
degree-16 diagonal audit     1,344-leaf pair-domain audit
F(u,u,1)<=35                F(u,v,t)<=-9/10
       \                         /
        exact ordered-pair summation
                    |
                    v
             N <= 359/9 < 40
                    |
                    v
                  N <= 39
```
