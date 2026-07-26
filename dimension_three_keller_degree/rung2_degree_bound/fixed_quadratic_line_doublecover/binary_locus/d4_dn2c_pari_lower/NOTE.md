# Direct PARI full-family certificate for `D4-DN-2C`

**First complete run (UTC):** `2026-07-26T06:34:50Z`

**Full-family run (UTC):** `2026-07-26T07:08:33Z`

**Status:** exact clean-room contact-atlas reconstruction and lower-chart
exclusion; not peer reviewed.

## Scope

Over \(\mathbb C\), for
\[
h=(p+q)^2,\qquad
P=hp^2,\qquad Q=hq^2,\qquad R=h(p-2q),
\]
the programs in this directory rebuild
\[
\det\!\left(L+wJH_2+w^2JH_3+w^3JH_4\right)
\]
directly in PARI/GP.  They independently derive the complete \(E_7\)
kernel, the reduced \(E_6\) contact locus, its exhaustive four-chart
atlas, and then descend all four charts while retaining every nonpivot
lower coefficient.

The calculation excludes this one frozen canonical family without relying
on a separately supplied contact atlas.  It does not close the parent row
or improve a universal degree bound.

## 1. Independent reconstruction of the contact atlas

Direct differentiation of the raw top forms gives
\[
\alpha=-6pq(p+q)^3,\qquad
\beta=6p(p+q)^3(p+2q),\qquad
\gamma=8pq(p+q)^4.
\]
After removing the common factor \(2p(p+q)^3\), the three \(E_7\)
blocks are:

| block | raw variables | rank | nullity |
|---|---:|---:|---:|
| \(r^2\) | 2 | 2 | 0 |
| \(r^1\) | 5 | 3 | 2 |
| \(r^0\) | 8 | 4 | 4 |

The verifier exhibits six independent kernel parameters
\((d,z,a,b,x,y)\), whose dimension equals the total nullity, and checks
the literal \(E_7\) polynomial is zero:
\[
\begin{aligned}
U_2&=\left(d+\frac43z\right)p+
     \left(2d+\frac43z\right)q,&
V_2&=dq,&T_2&=z,\\
U_1&=\left(x+\frac43a\right)p^2+
 \left(y+2x+\frac43(a+b)\right)pq+
 \left(2y+\frac43b\right)q^2,\\
V_1&=xpq+yq^2,&T_1&=ap+bq.
\end{aligned}
\]

Four raw \(E_6\), \(r^3\)-coefficients are
\[
\begin{aligned}
[p^3r^3]E_6&=-6d^2,\\
[p^2qr^3]E_6&=\frac{16}{3}z(3d+z),\\
[pq^2r^3]E_6&=\frac23(3d+4z)(9d+4z),\\
[q^3r^3]E_6&=\frac43(3d+2z)^2.
\end{aligned}
\]
Thus \(d=0\), then \(z=0\), set-theoretically in characteristic zero.

The remaining six \(r\)-linear equations involve only the two lower
unknowns \(a_5,b_5\), with coefficient matrix
\[
\begin{pmatrix}
0&0\\-12&24\\-36&84\\-36&108\\-12&60\\0&12
\end{pmatrix}.
\]
It has constant rank two; rows two and six give pivot \(-144\).
Solving those rows leaves
\[
g=2b+3y,\qquad
f=8a^2-16ab+24ax-24ay-24bx+27x^2-54xy+9y^2.
\]
Precisely, the first residual is \(2g^2/3\).  After \(g=0\), so
\(b=-3y/2\), the three nonzero unsolved residuals are
\[
\frac13f_0,\quad\frac23f_0,\quad\frac13f_0,\qquad
f_0=8a^2+24ax+27x^2-18xy+9y^2.
\]
Consequently the reduced contact locus, equivalently the radical of this
projected compatibility system over an algebraic closure, is
\[
d=z=g=f=0.
\]

Over \(\mathbb Q(\eta)\), \(\eta^2=-2\), the quadratic splits as
\[
\begin{aligned}
\ell_+&=9x+(4+2\eta)a+(-3+3\eta)y,\\
\ell_-&=9x+(4-2\eta)a+(-3-3\eta)y,\\
\ell_+\ell_-&=3f_0.
\end{aligned}
\]
The two factors are distinct.  Hence there are exactly two conjugate
planes.  Writing \(a=k,\ y=s,\ b=-3s/2\), they are
\[
x_+=\frac{-(4+2\eta)k+(3-3\eta)s}{9},\qquad
x_-=\frac{-(4-2\eta)k+(3+3\eta)s}{9}.
\]
Their difference is
\[
x_+-x_-=-\frac{2\eta}{9}(2k+3s),
\]
so they meet exactly on \(2k+3s=0\).  This is the line
\[
(a,b,x,y)=\left(k,k,-\frac23k,-\frac23k\right);
\]
its \(k=0\) point is the origin.  The two plane interiors, the punctured
common line, and the origin are therefore disjoint and exhaustive.

After \(d=z=0\), literal reconstruction proves that the complete \(E_6\)
system consists of exactly six \(r\)-linear and seven binary
coefficients.  It is a \(13\times18\) linear system in the distinct
lower variables
\[
(a_2,a_4,a_5,b_2,b_4,b_5,L_{33},
u_0,u_1,u_2,u_3,v_0,v_1,v_2,v_3,t_0,t_1,t_2).
\]
Every one of the 18 columns is nonzero on the generic plane chart.  Exact
rank computations, displayed pivots, and full 13-row residual solves give:

| chart | rank | exact pivot |
|---|---:|---:|
| \(\Pi_+\), \(2k+3s\ne0\) | 7 | \(93312(\eta-1)(2k+3s)^2\) |
| \(\Pi_-\), \(2k+3s\ne0\) | 7 | \(-93312(\eta+1)(2k+3s)^2\) |
| common line, \(k\ne0\) | 6 | \(186624k\) |
| origin | 5 | \(-31104\) |

The signs depend on the independently selected row and column order.  The
nonvanishing factors prove the asserted ranks on every point of the
corresponding chart, not merely generically.

## 2. The two transverse plane interiors

Let \(\eta^2=-2\), let \(a=k,\ y=s,\ b=-3s/2\), and on \(\Pi_+\) put
\[
x=\frac{-(4+2\eta)k+(3-3\eta)s}{9}.
\]
The directly reconstructed seven-pivot is
\[
93312(\eta-1)(2k+3s)^2.
\]
After solving it and retaining all eleven free lower variables, the
following three \(E_5\) coefficients are independent of every lower
variable:
\[
\begin{aligned}
[pq^2r^2]E_5={}&
\eta\!\left(\frac{32}{243}k^3+\frac4{27}sk^2+
\frac59s^2k+\frac{17}{18}s^3\right)\\
&+\frac{160}{243}k^3+\frac{20}{27}sk^2
-\frac29s^2k+\frac29s^3,\\
[p^2qr^2]E_5={}&
\eta\!\left(\frac{176}{243}k^3+\frac{28}{27}sk^2+
\frac29s^2k+\frac49s^3\right)\\
&+\frac{232}{243}k^3+\frac{32}{27}sk^2+
\frac{10}{9}s^2k+\frac{20}{9}s^3,\\
[p^3r^2]E_5={}&
\eta\!\left(\frac{40}{81}k^3+\frac49sk^2-s^2k-
\frac56s^3\right)\\
&-\frac{16}{81}k^3-\frac{16}{9}sk^2-2s^2k+
\frac13s^3.
\end{aligned}
\]
On the affine projective chart \(k=1,\ t=s/k\), their exact gcd (with the
normalization returned by PARI, and hence up to a nonzero scalar) is
\[
\frac{t}{162}+\frac1{243}=\frac{3t+2}{486}.
\]
Thus their only common projective zero is \(2k+3s=0\), precisely the
removed common line.  At \(k=0,s=1\), their respective values are
\[
\frac{17}{18}\eta+\frac29,\qquad
\frac49\eta+\frac{20}{9},\qquad
-\frac56\eta+\frac13,
\]
all nonzero.  Hence \(\Pi_+\setminus\{2k+3s=0\}\) is empty at \(E_5\).
Conjugating \(\eta\mapsto-\eta\) gives the same gcd and excludes
\(\Pi_-\).

## 3. The punctured common line

On the common line \(s=-2k/3\), the contact is
\[
U_1=\frac23kp(p+q),\qquad
V_1=-\frac23kq(p+q),\qquad
T_1=k(p+q),
\]
with \(k\ne0\).  Fresh, constant-rank solves use the following pivots:

| stage | rank | pivot |
|---|---:|---:|
| \(E_6\) | 6 | \(186624k\) |
| \(E_5\), \(r\)-linear | 2 | \(-16k^3/3\) |
| \(E_5\), binary | 3 | \(32k^3\) |
| \(E_4\), \(r\)-linear after \(B=0\) | 1 | \(2k\) |
| \(E_4\), binary after \(B=0\) | 2 | \(-4k^2\) |

The \(r^2\)-part of \(E_4\) forces
\[
S=v_0-v_1+v_2-v_3=0.
\]
After this substitution, put
\[
\begin{aligned}
T_\Delta&=t_0-t_1+t_2,\\
Y&=u_2-\frac32u_3-2v_2+3v_3-\frac43t_1+\frac43t_2,\\
Z&=v_1-2v_2+3v_3-\frac23t_1+\frac43t_2,\\
B&=kZ+2L_{33}.
\end{aligned}
\]
If \(C_1,C_5,C_6\) denote the three nonzero residual binary \(E_5\)
coefficients, the direct determinant reconstruction gives
\[
C_1=2YB,\qquad
C_5=-5C_1+\frac{16}{9}kT_\Delta^2,\qquad
C_6=-4C_1+\frac{16}{9}kT_\Delta^2.
\]
Consequently \(T_\Delta=0\) and \(YB=0\).

On \(Y=0\), a necessary coefficient is
\[
[q^3r]E_4=\frac23B^2,
\]
so every solution has \(B=0\).  On \(B=0\), the two displayed \(E_4\)
rank solves leave the single compatibility
\[
kYW=0,
\]
where
\[
\begin{aligned}
W={}&-v_1^2+
\left(4v_2-6v_3+\frac23t_1-\frac43t_2\right)v_1
-4v_2^2\\
&+\left(12v_3-\frac43t_1+\frac83t_2\right)v_2
-9v_3^2+(2t_1-4t_2)v_3
-\frac43L_{31}+\frac43L_{32}.
\end{aligned}
\]
The branch \(W=0\) gives \(\det L=0\) identically.

It remains to consider \(Y=0,\ W\ne0\).  The coefficient
\([p^3]E_3\) factors exactly as
\[
[p^3]E_3=kWH,
\]
with
\[
\begin{aligned}
H={}&
\left(v_2-\frac32v_3+t_1-t_2\right)v_1-v_2^2
+(3v_3-t_1+t_2)v_2\\
&-\frac94v_3^2+(t_1-t_2)v_3-b_1+b_3.
\end{aligned}
\]
Since \(W\ne0\), this forces \(H=0\); its coefficient of \(b_1\) is
\(-1\), so this introduces no pivot divisor.  The remaining \(E_3\)
system has rank one.  Its safe pivot is \(3W\), and after that solve its
two residuals are both
\[
-\frac{k}{2}W^2.
\]
This contradicts \(kW\ne0\).  The punctured common line is therefore
excluded with no unexamined pivot boundary.

## 4. The origin

The zero-contact chart is rebuilt before any \(1/k\)-division.  Its
complete \(E_6\) system has rank five and constant pivot \(31104\).
After that solve,
\[
[p^3r]E_4=-3b_{qr}^2,\qquad
[q^3r]E_4=\frac23(3b_{qr}+2L_{33})^2.
\]
Thus \(b_{qr}=L_{33}=0\).  Literal substitution makes every one of the
five \(E_6\)-pivot formulas zero.  Together with \(b_{qr}=0\), this sets
all six nonbinary quadratic coefficients of \(A,B\) to zero.  The contact
is zero, so every nonlinear term is binary.

The verifier constructs the adjugate of \(L\) and checks directly that,
after target normalization, the first two coordinates are binary, the
third has constant \(r\)-slope \(\det L\), and
\[
\det J_{p,q}(G_1,G_2)=\det L\cdot\det(L+JH).
\]
For a Keller map the plane factor is therefore a degree-at-most-four
plane Keller map.  Moh's unconditional degree-\(<100\) theorem makes it
an automorphism, and the third coordinate is a triangular lift.

## Verification

Run:

```sh
./verify_strict.sh
```

The terminal markers are:

```text
D4_DN2C_DIRECT_PARI_LOWER_STRICT_PASS
D4_DN2C_DIRECT_PARI_CONTACT_ATLAS_STRICT_PASS
D4_DN2C_DIRECT_PARI_FULL_FAMILY_STRICT_PASS
```

The wrapper rejects PARI diagnostics, requires every contact and lower
chart marker, and requires three deliberately corrupted decisive
identities to fail: the doubled contact hyperplane, the transverse
projective gcd, and the final \(E_3\) square.

The calculations and exposition were produced with substantial AI
assistance.  Exact computer algebra is evidence about the encoded algebra,
not peer review.
