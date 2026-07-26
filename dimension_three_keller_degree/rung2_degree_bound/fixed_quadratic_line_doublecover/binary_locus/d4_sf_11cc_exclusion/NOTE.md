# Exclusion of the isolated squarefree \(\kappa=16\) family

**Status:** candidate theorem with two exact algebraic implementations;
hostile mathematical audit pending.

**First banked (UTC):** 2026-07-26.

This note is not peer reviewed.  The exact checks certify the encoded
algebra; they are not peer review.

## 1. Statement and scope

Consider a degree-four Keller map over \(\mathbb C\), written as
\[
F=L_0X+H_2+H_3+H_4,
\]
with \(H_i\) homogeneous of degree \(i\).  In the binary
fixed-quadratic line-double-cover row, normalize
\[
H_4=(P,Q,0),\qquad
P=hp^2,\quad Q=hq^2.
\]
The canonical incidence family `D4-SF-11CC` is the isolated point
\[
h=p^2-4pq+q^2,\qquad
R:=(H_3)_3=h(p+q).                                  \tag{1}
\]

### Candidate theorem

No Keller counterexample has leading data (1).  More precisely, every
degree-four Keller map whose leading data belongs to the
`D4-SF-11CC` orbit is a polynomial automorphism.

This excludes one of the 26 high-incidence families in the frozen
denominator.  It does not close the parent fixed-quadratic row and does
not improve the universal total-degree floor of four.

To identify (1) with the canonical denominator, write
\[
h=(p-rq)(p-r^{-1}q).
\]
At \(\kappa=(r+r^{-1})^2=16\), choose \(r+r^{-1}=4\).  Then
\[
h=p^2-4pq+q^2,
\]
and the canonical residual line
\((r^2+1)p+4rq\) is \(4r(p+q)\).  Thus its cubic is proportional
to \(h(p+q)\); a nonzero target scaling gives (1).

## 2. Weighted identities

Put
\[
\mathcal J(z)=L_0+zJH_2+z^2JH_3+z^3JH_4,\qquad
E_j=[z^j]\det\mathcal J(z).
\]
For
\[
\alpha=J(Q,R),\qquad
\beta=-J(P,R),\qquad
\gamma=J(P,Q),
\]
one has
\[
\gcd(\alpha,\beta,\gamma)\doteq
pq(p^2-4pq+q^2),                                   \tag{2}
\]
of degree four, and \(\alpha,\beta\) are constant-linearly independent.
The two relevant binary syzygy nullities are two and four, as required
by the \(\{2,2\}\) Hilbert--Burch shape.

The \(r^2\) block of \(E_7\) has nullity zero.  Choose the following
bases for the subsequent degree-one and degree-two syzygies:
\[
\begin{aligned}
S^x_0&=\left(-\frac{3p-q}{3},-\frac{p-3q}{3},0\right),\\
S^x_1&=\left(\frac{15p-4q}{9},\frac p9,1\right),
                                                               \tag{3}\\
S^y_0&=\left(-\frac{p(3p-q)}3,-\frac{p(p-3q)}3,0\right),\\
S^y_1&=\left(-\frac{(p+3q)(3p-q)}9,
             -\frac{(p-3q)(p+3q)}9,0\right),\\
S^y_2&=\left(\frac{p(15p-4q)}9,\frac{p^2}9,p\right),\\
S^y_3&=\left(\frac{3p^2+44pq-12q^2}{27},
             \frac{p^2}{27},q\right).
                                                               \tag{4}
\end{aligned}
\]
Each displayed triple satisfies
\(\alpha A+\beta B+\gamma C=0\), and the exact nullity computation
shows that they are bases.

Let \(x_0,x_1\) be the \(r^1\)-block coordinates in (3), and let
\(y_0,\ldots,y_3\) be the \(r^0\)-block coordinates in (4).  Arbitrary
binary summands in \(H_3\) and \((H_2)_3\) are retained below.

## 3. The complete \(E_6\) contact plane

Write
\[
c_{ijk}=[p^iq^jr^k]E_6.
\]
Direct expansion of the full determinant, with arbitrary binary lower
summands, gives
\[
\begin{aligned}
\frac{27}{4}c_{303}
  &=(3x_0-x_1)^2,\\
27c_{303}+\frac{27}{4}c_{213}
  &=(3x_0-4x_1)^2.                                  \tag{5}
\end{aligned}
\]
Hence \(E_6=0\) forces \(x_0=x_1=0\).

After this substitution, two further coefficient combinations are
\[
\begin{aligned}
\frac{243}{8}c_{501}
  &=(9y_0+3y_1-3y_2-y_3)^2,\\
189c_{501}+\frac{405}{8}c_{411}
 +\frac{27}{2}c_{321}+\frac{27}{8}c_{231}
  &=(3y_1-4y_3)^2.                                  \tag{6}
\end{aligned}
\]
Thus the projected \(E_6\) contact locus is contained in the plane
\[
x_0=x_1=0,\qquad
y_0=\frac{y_2-y_3}{3},\qquad
y_1=\frac43y_3.                                     \tag{7}
\]
Conversely, explicit coefficients
\[
A_{r^2}=-\frac{y_2^2+3y_3^2}{36},\qquad
B_{r^2}=-\frac{3y_2^2+y_3^2}{36}
\]
with the other displayed \(E_6\) lower variables zero solve every
coefficient of \(E_6\).  Hence (7), not merely its containment, is the
complete projected contact locus.

Set
\[
m=y_2,\qquad n=y_3.
\]
The nonbinary derivatives on this plane are
\[
\begin{aligned}
U_r&=\frac p3(4mp-mq+nq),\\
V_r&=\frac q3(mp-np+4nq),\\
T_r&=mp+nq,                                         \tag{8}
\end{aligned}
\]
where \(U=(H_3)_1,V=(H_3)_2,T=(H_2)_3\).

## 4. The three rank charts below \(E_6\)

Retain arbitrary binary cubic parts of \(U,V\), the arbitrary binary
quadratic part of \(T\), every quadratic coefficient in
\((H_2)_1,(H_2)_2\), and all nine entries of \(L_0\).
The coefficient matrix for the remaining \(E_6\) solve has generic rank
seven.  A nonzero maximal minor is a scalar multiple of
\[
\Delta=m^2-4mn+n^2.                                 \tag{9}
\]
Thus there are exactly three charts:

1. \(\Delta\ne0\), of rank seven;
2. \(\Delta=0\) with \((m,n)\ne(0,0)\), of rank six; and
3. \((m,n)=(0,0)\), of rank five.

On the generic chart, solving the complete \(E_6\) system and reading two
coefficients of \(E_5\) gives
\[
\begin{aligned}
[p^2qr^2]E_5
  &=-\frac49(7m^3-6m^2n+3mn^2-2n^3),\\
[pq^2r^2]E_5
  &= \frac49(2m^3-3m^2n+6mn^2-7n^3).               \tag{10}
\end{aligned}
\]
The two cubics have resultants
\[
\operatorname{Res}_m=-46656n^9,\qquad
\operatorname{Res}_n=46656m^9.                     \tag{11}
\]
Their only common affine zero is therefore the origin, which is not in
this chart.  The generic chart is empty.

For the conic chart, \(n\ne0\), and after scaling
\[
\frac mn=2\pm\sqrt3.
\]
The scaling here is the remaining nonzero transverse source scaling
\(r\mapsto cr\), which preserves the binary leading form.
The two points are exchanged by \(p\leftrightarrow q\), so take
\(n=1,m=2+\sqrt3\).  A fresh rank-six \(E_6\) solve, without division by
\(\Delta\), gives
\[
\begin{aligned}
[p^2qr^2]E_5&=-64-\frac{112}{3}\sqrt3,\\
[pq^2r^2]E_5&= 16+\frac{32}{3}\sqrt3.               \tag{12}
\end{aligned}
\]
Both have nonzero norm \(-256/3\) over \(\mathbb Q\), so this chart is
empty as well.

At the origin, recompute \(E_6\) at rank five.  Let \(b\) be the
coefficient of \(qr\) in \((H_2)_2\), and put
\(\lambda=(L_0)_{33}\).  After the complete fresh solve, two coefficients
of \(E_4\) are
\[
\begin{aligned}
[p^3r]E_4&=\frac8{27}(3b-\lambda)^2,\\
[q^3r]E_4&=\frac8{27}(3b-4\lambda)^2.               \tag{13}
\end{aligned}
\]
Hence \(b=\lambda=0\).  The rank-five \(E_6\) formulas then set every
\(r\)-dependent coefficient in \((H_2)_1,(H_2)_2\) to zero.  Since
\((m,n)=(0,0)\) and \(x_0=x_1=0\), all of \(H_2,H_3,H_4\) are binary:
\[
H_i=H_i(p,q).                                       \tag{14}
\]

## 5. The unconditional plane exit

Because a Keller map has invertible linear part, postcompose by
\(L_0^{-1}\).  Equation (14) gives
\[
(p,q,r)\longmapsto
\bigl(p+A(p,q),\ q+B(p,q),\ r+C(p,q)\bigr).         \tag{15}
\]
Its Jacobian determinant is the Jacobian determinant of the plane map
\[
(p,q)\longmapsto(p+A(p,q),q+B(p,q)).
\]
This plane Keller map has degree at most four.  Moh's unconditional
plane theorem through degree \(100\) makes it a polynomial automorphism;
no assumption of the plane Jacobian Conjecture is used.  The third
component in (15) is then a triangular lift, so the original
three-dimensional map is a polynomial automorphism.  This proves the
candidate theorem, subject to the pending hostile audit.

## 6. Exact verification

Run

```sh
./verify_strict.sh
```

The terminal marker is

```text
D4_SF_11CC_FULL_STRICT_PASS
```

`verify_exclusion_sympy.py` reconstructs the syzygy nullities, the full
weighted determinant with arbitrary binary lower summands, the contact
plane, all three rank charts, the two resultants, and the final collapse
to binary nonlinear terms.  `verify_exclusion_pari.gp` independently reconstructs the
determinants in PARI/GP, including a fresh exact-number-field solve on the
conic chart and a fresh zero-contact solve.  The wrapper rejects optimized
Python and any PARI/GP error transcript.

These checks were produced with substantial AI assistance.  They are
evidence about the encoded identities, not a substitute for human
mathematical review.

## Reference

T.-T. Moh, “On the Jacobian conjecture and the configurations of roots,”
*Journal für die reine und angewandte Mathematik* **340** (1983),
140--212,
[doi:10.1515/crll.1983.340.140](https://doi.org/10.1515/crll.1983.340.140).
