# Exclusion of the isolated squarefree \(\kappa=-16/5\) family

**Status:** certified family-level exclusion.  Two exact algebraic
implementations and an independent clean-room hostile reconstruction pass.

**First banked (UTC):** 2026-07-26.

This note is not peer reviewed.  The exact checks certify the encoded
algebra; they are not peer review.

## 1. Statement and scope

Let \(s^2=-5\), and put
\[
X=p-sq,\qquad Y=sp-q,\qquad h=XY.
\]
In the binary fixed-quadratic line-double-cover row, normalize
\[
H_4=(P,Q,0),\qquad P=hp^2,\quad Q=hq^2.
\]
The canonical incidence family `D4-SF-21C` is
\[
R:=(H_3)_3=X^2Y.                                  \tag{1}
\]
The corresponding modulus is
\[
\kappa=-5+2-\frac15=-\frac{16}{5}.
\]

### Theorem

No Keller counterexample over \(\mathbb C\) has leading data in the
`D4-SF-21C` orbit.  More precisely, every degree-four Keller map with
leading data (1), up to the source and target normalizations used in the
frozen denominator, is a polynomial automorphism.

This excludes one of the 26 canonical high-incidence families in the
fine denominator.  It does not close the parent fixed-quadratic row and
does not improve the universal total-degree floor of four.

## 2. Weighted setup and syzygies

Write
\[
F=L_0(p,q,r)^t+H_2+H_3+H_4
\]
and
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
exact computation gives
\[
\gcd(\alpha,\beta,\gamma)\doteq pX^2Y,             \tag{2}
\]
of degree four, and \(\alpha,\beta\) are
constant-linearly independent.  The degree-one syzygy space has basis
\[
\begin{aligned}
S^x_0&=\left(\frac{4s}{5}p-q,\ q,\ 0\right),\\
S^x_1&=\left(\frac43p+\frac{4s}{15}q,\ 0,\ 1\right),
                                                               \tag{3}
\end{aligned}
\]
and the degree-two space has basis
\[
pS^x_0,\quad qS^x_0,\quad pS^x_1,\quad qS^x_1.     \tag{4}
\]
Every displayed triple satisfies
\(\alpha A+\beta B+\gamma C=0\), and the nullity calculation proves
that these are full bases.

Let \(x_0,x_1\) be the \(r^2\)-block coordinates in (3), and let
\(y_0,\ldots,y_3\) be the \(r\)-block coordinates in (4).  The
determinant calculation below retains arbitrary binary cubic parts in
the first two components of \(H_3\), an arbitrary binary quadratic
part in the third component of \(H_2\), all quadratic coefficients in
the first two components of \(H_2\), and all nine entries of \(L_0\).

## 3. The complete \(E_6\) contact plane

Put \(c_{ijk}=[p^iq^jr^k]E_6\).  The two highest-\(r\) equations begin
with
\[
c_{303}=6x_0^2,\qquad
c_{213}\big|_{x_0=0}=\frac{4s}{3}x_1^2.            \tag{5}
\]
Thus \(E_6=0\) forces \(x_0=x_1=0\).

After setting \(x=0\), the 13 nonzero coefficient equations are affine
linear in 18 lower coefficients.  Their coefficient matrix has rank
nine.  Four exact left-kernel vectors give compatibility polynomials
\(C_0,C_1,C_2,C_3\).  The two needed identities are
\[
\begin{aligned}
C_3&=s\left(y_1-\frac{4s}{15}y_3\right)^2,\\
\left.(C_0-C_2)\right|_{y_1=4sy_3/15}
  &=-\frac14\left(y_2-\frac{s}{5}y_3\right)^2.     \tag{6}
\end{aligned}
\]
The four compatibility polynomials vanish identically after these two
relations.  Conversely, the complete \(E_6\) linear system is solvable
there.  Hence the projected contact locus is exactly the plane
\[
x_0=x_1=0,\quad
y_0=m,\quad y_1=\frac{4s}{15}n,\quad
y_2=\frac{s}{5}n,\quad y_3=n.                      \tag{7}
\]

On this plane the nonbinary derivatives are
\[
\begin{aligned}
U_r&=p\left[\left(\frac{4s}{5}m+\frac{4s}{15}n\right)p-mq\right],\\
V_r&=q\left[mp+\frac{4s}{15}nq\right],\\
T_r&=\frac n5(sp+5q),                              \tag{8}
\end{aligned}
\]
where \(U=(H_3)_1,V=(H_3)_2,T=(H_2)_3\).

## 4. The three lower rank charts

The remaining \(E_6\) coefficient matrix has generic rank seven.  A
maximal minor is a nonzero scalar multiple of
\[
\Delta=\left(m-\frac n3\right)\left(m+\frac n6\right). \tag{9}
\]
The complete contact plane therefore has three kinds of points:

1. \(\Delta\ne0\), of rank seven;
2. the two nonzero directions \((m,n)\sim(1,3),(-1,6)\), of rank six;
3. the origin, of rank five.

On the generic chart, a seven-pivot solution of every coefficient of
\(E_6\) gives
\[
\begin{aligned}
[p^2qr^2]E_5
 &=\frac{8s}{225}
   (135m^3+135m^2n-9mn^2+n^3),\\
[pq^2r^2]E_5
 &=-\frac4{45}
   (135m^3+18mn^2-2n^3).                           \tag{10}
\end{aligned}
\]
The two cubics have resultants
\[
\operatorname{Res}_m=-1793613375\,n^9,\qquad
\operatorname{Res}_n= 1793613375\,m^9.             \tag{11}
\]
Their only common affine zero is the origin, outside this chart.

At each nonzero rank-six direction, a fresh six-pivot solve—without
division by \(\Delta\)—gives
\[
[p^3r^2]E_5=-\frac{108}{5}.                        \tag{12}
\]
Both boundary directions are therefore empty.

At the origin, a fresh rank-five solve gives, with \(b\) the coefficient
of \(qr\) in \((H_2)_2\) and
\(\lambda=(L_0)_{33}\),
\[
[p^3r]E_4=12b^2,\qquad
\left.[p^2qr]E_4\right|_{b=0}=\frac{8s}{3}\lambda^2.
                                                               \tag{13}
\]
Thus \(b=\lambda=0\).  The rank-five formulas then make every
\(r\)-dependent coefficient of the first two components of \(H_2\)
zero.  Together with \(m=n=x_0=x_1=0\), all nonlinear terms are binary:
\[
H_i=H_i(p,q).                                      \tag{14}
\]

## 5. The unconditional plane exit

First subtract the constant value \(F(0)\).  The Keller condition makes
\(L_0\) invertible.  After postcomposing by \(L_0^{-1}\), equation (14)
has triangular-lift form
\[
(p,q,r)\longmapsto
\bigl(p+A(p,q),\ q+B(p,q),\ r+C(p,q)\bigr).         \tag{15}
\]
The first two coordinates form a plane Keller map of degree at most
four.  Moh's unconditional plane theorem for degree strictly less than
\(100\) makes that plane map a polynomial automorphism; this does not
assume the plane Jacobian Conjecture.  Equation (15) is then a triangular
lift of an automorphism, hence is itself a polynomial automorphism.

This proves the theorem.

## 6. Exact verification

Run

```sh
./verify_strict.sh
```

The terminal marker is

```text
D4_SF_21C_FULL_STRICT_PASS
```

`verify_exclusion_sympy.py` reconstructs the incidence gcd, both
syzygy spaces, the determinant with all lower coefficients present,
the complete contact plane, the generic and boundary rank charts, the
two resultants, and the zero-contact collapse.  The independent
`verify_exclusion_pari.gp` reconstructs the determinant over
\(\mathbb Q(s)/(s^2+5)\), certifies four explicit left-kernel
compatibilities, and performs fresh pivot solves in every chart.  The
strict wrapper rejects optimized Python, PARI/GP error transcripts, and
a deliberately mutated boundary obstruction.

These checks were produced with substantial AI assistance.  They are
evidence about the encoded identities, not a substitute for human
mathematical review.

## Reference

R. Biggers, T.-T. Moh, and M. Fried, “On the Jacobian conjecture and the
configurations of roots,”
*Journal für die reine und angewandte Mathematik* **340** (1983),
140--213,
[doi:10.1515/crll.1983.340.140](https://doi.org/10.1515/crll.1983.340.140).
