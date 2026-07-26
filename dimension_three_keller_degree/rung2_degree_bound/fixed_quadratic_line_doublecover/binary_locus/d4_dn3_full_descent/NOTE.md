# Exclusion of the frozen family `D4-DN-3`

**First complete exact proof (UTC):** `2026-07-26T05:34:00Z`  
**Status:** certified family-level exclusion, subject to the scope stated
below.  Independent exact SymPy reconstructions and a direct PARI/GP replay
agree.  The work is not peer reviewed.

## Statement

Over \(\mathbb C\), in the
fixed-quadratic line-double-cover row, consider the frozen exact-delta-four
doubled-nonbranch family
\[
 h=(p+q)^2,\qquad
 P=hp^2,\qquad Q=hq^2,\qquad R=(p+q)^3.
\]
There is no Keller counterexample with these normalized top forms.

Equivalently, every Keller map in this frozen family is a polynomial
automorphism.  This closes one of the 26 canonical high-incidence families
and the fifth of the six isolated exact-delta-four families.  It does
**not** close the parent fixed-quadratic row, change the frozen global
\(4/14\) count, or improve the universal total-degree floor of four.

## Weighted determinant equations

After subtracting the constant term, write
\[
 F=L(p,q,r)^t+H_2+H_3+H_4,
\]
where
\[
 H_4=(P,Q,0),\qquad H_3=(U,V,R),\qquad H_2=(A,B,T).
\]
Introduce
\[
 \Delta(w)=
 \det\!\left(
 L+wJH_2+w^2JH_3+w^3JH_4
 \right)
 =\sum_j E_jw^j .
\]
For a Keller map, \(E_j=0\) for every \(j>0\), while
\(E_0=\det L\ne0\).

Put
\[
 \alpha=J(Q,R),\qquad
 \beta=-J(P,R),\qquad
 \gamma=J(P,Q).
\]
Here
\[
 \alpha=-6q(p+q)^4,\qquad
 \beta=-6p(p+q)^4,\qquad
 \gamma=8pq(p+q)^4.
\]
The complete \(E_7\) equation
\[
 \alpha U_r+\beta V_r+\gamma T_r=0
\]
has successive nullities \(0,2,4\).  Naming its six parameters
\((d,z,a,b,x,y)\), write
\[
U=U_0+rU_1+r^2U_2,\qquad
V=V_0+rV_1+r^2V_2,\qquad
T=T_0+rT_1+r^2T_2.
\]
Every contact is
\[
\begin{aligned}
U_2&=\frac{4z-3d}{3}p,&
V_2&=dq,&T_2&=z,\\
U_1&=\frac{4a-3x}{3}p^2+
      \frac{4b-3y}{3}pq,&
V_1&=xpq+yq^2,&T_1&=ap+bq.
\end{aligned}
\]
Thus no contact branch is omitted by an ansatz.

## Complete \(E_6\) contact locus

The \(r^3\)-part of \(E_6\) is
\[
\begin{aligned}
&\frac23(-3d+4z)^2q^3
+2(9d^2-16dz+8z^2)pq^2\\
&\quad+\frac23(27d^2-24dz+8z^2)p^2q
+6d^2p^3.
\end{aligned}
\]
Its extreme coefficients force \(d=z=0\).

Restoring all 18 lower variables, elimination from the remaining \(E_6\)
system gives the exact set-theoretic contact locus
\[
 a=b,\qquad
 8a^2+24a(x-y)+9(x-y)^2=0.
\]
Over \(\mathbb C\), this is precisely the union of two planes
\[
\Pi_\pm:\quad
(a,b,x,y)=
\left(k,k,s+c_\pm k,s\right),
\qquad
c_\pm=\frac{-4\pm2\sqrt2}{3}.
\]
They meet along \(k=0\).

The elimination is specialization-safe.  The full coefficient and
augmented matrices have equal ranks on the following exhaustive atlas:

| chart | condition | ranks | nonzero pivot |
|---|---:|---:|---:|
| `DN3-P+-KNZ` | \(\Pi_+\), \(k\ne0\) | \(7/7\) | \(373248(7-5\sqrt2)k^2\) |
| `DN3-P--KNZ` | \(\Pi_-\), \(k\ne0\) | \(7/7\) | \(373248(7+5\sqrt2)k^2\) |
| `DN3-INTERSECTION-SNZ` | \(k=0,\ s\ne0\) | \(6/6\) | \(-279936s\) |
| `DN3-ORIGIN` | \(k=s=0\) | \(5/5\) | \(31104\) |

In particular, the apparent denominator
\[
s+\left(-\frac{10}{3}+2\sqrt2\right)k
\]
from an earlier symbolic solve is not a geometric boundary: the displayed
seven-pivot is independent of \(s\).

## The two transverse planes

On \(\Pi_+\) with \(k\ne0\), solve the complete seven-pivot \(E_6\)
system while retaining all eleven free lower variables.  Two coefficients
of \(E_5\) are nevertheless independent of every one of them:
\[
\begin{aligned}
[p^3r^2]E_5
 &=3(\sqrt2-2)k(s+c_+k)^2,\\
[q^3r^2]E_5
 &=3(\sqrt2-2)k\left(s-\frac43k\right)^2.
\end{aligned}
\]
The common scalar is nonzero.  If both coefficients vanished, then
\[
s=-c_+k=\frac43k,
\]
contrary to \(c_+\ne-4/3\).  Hence the whole transverse part of
\(\Pi_+\) is empty.  Galois conjugation gives
\[
\begin{aligned}
[p^3r^2]E_5
 &=3(-\sqrt2-2)k(s+c_-k)^2,\\
[q^3r^2]E_5
 &=3(-\sqrt2-2)k\left(s-\frac43k\right)^2,
\end{aligned}
\]
and excludes \(\Pi_-\) in the same way.  No exceptional \(s/k\)-value is
lost.

## The punctured plane intersection

On the common line \(k=0,\ s\ne0\), rename its nonzero coordinate
\(\rho=s\).  The contact becomes
\[
 U_1=-\rho p(p+q),\qquad
 V_1=\rho q(p+q),\qquad T_1=0.
\]
A fresh solve, rather than a specialization of a \(1/k\)-formula, gives
the following nonzero pivot minors:

| stage | rank | pivot |
|---|---:|---:|
| \(E_6\) | 6 | \(-279936\rho\) |
| \(E_5\), \(r\)-linear | 3 | \(192\rho^4\) |
| \(E_5\), binary | 3 | \(108\rho^3\) |
| \(E_4\), \(r\)-linear | 2 | \(3\rho^4\) |
| \(E_4\), binary | 2 | \(9\rho^2\) |

All solution denominators are constants or powers of \(\rho\); the only
removed divisor is the separately recomputed origin.

After the two \(E_5\) stages put
\[
 S=v_0-v_1+v_2-v_3
\]
and
\[
 D=u_1-2u_2+3u_3-v_1+2v_2-3v_3.
\]
The complete \(r^2\)-part of \(E_4\) is
\[
\begin{aligned}
[p^2r^2]E_4&=-\frac94\rho^3S,\\
[pqr^2]E_4&=-\frac92\rho^3S,\\
[q^2r^2]E_4&=-\frac94\rho^3S.
\end{aligned}
\]
Thus \(S=0\).  After this substitution, all six residual binary
\(E_5\) equations are
\[
\left(0,0,0,\frac34,\frac32,\frac34\right)\rho D^2.
\]
Hence \(D=0\).  The complete remaining \(E_4\) systems have no
compatibility polynomial, and exact back-substitution into every
\(E_4\) coefficient gives zero.  Substitution of the same full solution
into the literal determinant of the linear part gives
\[
\det L=0.
\]
This contradicts the Keller condition.  An independent clean-room solve
used a different final pivot and explicitly split its additional
\(V=0\) boundary; both \(V\ne0\) and \(V=0\) again gave
\(\det L=0\).

## The origin

At \(k=s=0\), recompute the rank-five \(E_6\) system.  After its full
solution, two necessary coefficients are
\[
[p^3r]E_4=3b_{qr}^2,\qquad
[q^3r]E_4=\frac13(3b_{qr}-4L_{33})^2.
\]
They force
\[
b_{qr}=L_{33}=0.
\]
The complete \(E_6\) formulas then set all six nonbinary quadratic
coefficients of \(A,B\) to zero.  The contact is zero as well, so every
nonlinear term depends only on \(p,q\).

If \(L\) were singular, the map would not be Keller.  If \(L\) is
invertible, postcompose the already constant-free map by \(L^{-1}\).  The map
has the form
\[
(p,q,r)\longmapsto
\bigl(p+\Phi(p,q),q+\Psi(p,q),r+\Theta(p,q)\bigr).
\]
Because the original constant Jacobian equals \(\det L\), the first two
coordinates form a plane Keller map of Jacobian one and degree at most four.
Moh's unconditional bounded-degree theorem (degree strictly less than
\(100\)) makes it a polynomial automorphism.  The displayed triangular
lift is therefore an automorphism.  This exit does not assume the open
plane Jacobian Conjecture.

The four contact charts are exhaustive, so the theorem follows.

## Verification

The primary SymPy calculations reconstruct the full weighted determinant,
the contact atlas, the transverse \(E_5\) obstruction, and the complete
intersection/origin descents.  The clean-room SymPy audit derives all four
lower charts independently and uses different pivots on the punctured
intersection.  PARI/GP directly reconstructs both the transverse
obstruction over \(\mathbb Q(\sqrt2)\) and the rational boundary descent.

Run the aggregate strict wrapper in this directory.  It rejects disabled
assertions, interpreter diagnostics, missing terminal markers, and
deliberately mutated decisive identities.

```sh
./verify_strict.sh
```

Its terminal marker is

```text
D4_DN3_FULL_FAMILY_EXCLUSION_STRICT_PASS
```

Exact computer algebra is evidence about the algebra encoded by the
scripts.  It is not peer review.

## Scope and disclosure

This result concerns only the frozen canonical family `D4-DN-3`.  It is
not an exclusion of all degree-four Keller counterexamples and proves no
new universal degree bound.  The derivation, code, audits, and exposition
were produced with substantial AI assistance.

## Reference

R. Biggers, T.-T. Moh, and M. Fried, “On the Jacobian conjecture and the
configurations of roots,” *Journal für die reine und angewandte
Mathematik* **340** (1983), 140–213,
[doi:10.1515/crll.1983.340.140](https://doi.org/10.1515/crll.1983.340.140).
