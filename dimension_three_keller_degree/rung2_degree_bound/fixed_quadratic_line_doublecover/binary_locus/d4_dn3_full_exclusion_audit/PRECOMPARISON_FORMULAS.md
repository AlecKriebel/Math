# Frozen clean-room formulas before comparison

**Frozen UTC:** 2026-07-26T06:03:00Z

At this timestamp no file in `d4_dn3_full_descent` and no lower script or
note in `delta_ge3_survivor_probe` had been read.  The formulas below were
derived from the audited contact atlas and a standalone reconstruction of the
weighted determinant.

## 1. Both transverse contact planes

Put
\[
c_\pm=\frac{-4\pm2\sqrt2}{3}.
\]
The complete seven-pivot \(E_6\) solve uses
\[
(a_{pr},a_{qr},a_{r^2},b_{pr},b_{r^2},u_0,u_1)
\]
and has pivots
\[
373248(7\mp5\sqrt2)k^2.
\]

After this solve, two lower-variable-free \(E_5\) coefficients are
\[
\begin{aligned}
[p^3r^2]E_5
 &=3(\pm\sqrt2-2)\,k(s+c_\pm k)^2,\\
[q^3r^2]E_5
 &=3(\pm\sqrt2-2)\,k(s-4k/3)^2.
\end{aligned}
\]
For \(k\ne0\), they cannot vanish simultaneously because
\(-c_\pm\ne4/3\).  This covers arbitrary \(s\), with no omitted internal
line.

## 2. Punctured intersection

Set \(k=0,\ s\ne0\).  The fresh \(E_6\) pivot is
\[
-279936s,
\]
solving
\[
(a_{pr},a_{qr},a_{r^2},b_{pr},b_{r^2},u_0).
\]

The \(r\)-linear part of \(E_5\) has rank three.  A pivot \(192s^4\)
solves \(b_{qr},L_{33},t_1\):
\[
\begin{aligned}
b_{qr}&=\frac{s}{2}(-v_1+v_2),\\
L_{33}&=s\left(
-\frac{t_0}{2}+\frac{t_2}{2}
+\frac{3u_1}{8}-\frac{3u_2}{4}+\frac{9u_3}{8}
-\frac{3v_1}{8}+\frac{3v_2}{4}-\frac{9v_3}{8}
\right),\\
t_1&=t_0+t_2.
\end{aligned}
\]

The binary part of \(E_5\) has rank three.  A pivot \(216s\) solves
\((a_{pq},L_{13},L_{23})\) in the clean-room indexing
\((a_1,l_2,l_5)\).  Its sole compatibility polynomial is
\[
\begin{aligned}
C={}&8(t_0-t_2)(v_0-v_1+v_2-v_3)
u_1^2-4u_1u_2+6u_1u_3\\
&-15u_1v_0+13u_1v_1-11u_1v_2+9u_1v_3
4u_2^2-12u_2u_3\\
&+30u_2v_0-26u_2v_1+22u_2v_2-18u_2v_3
9u_3^2\\
&-45u_3v_0+39u_3v_1-33u_3v_2+27u_3v_3\\
&+18v_0^2-21v_0v_1+6v_0v_2+9v_0v_3
4v_1^2+5v_1v_2-18v_1v_3\\
&-8v_2^2+27v_2v_3-18v_3^2.
\end{aligned}
\]

Three \(r^2\)-coefficients of \(E_4\) are nonzero scalar multiples of
\[
D=v_0-v_1+v_2-v_3,
\]
one being
\[
[p^2r^2]E_4=-\frac94s^3D.
\]
Thus \(D=0\).  On this hyperplane,
\[
C=W^2,\qquad
W=u_1-2u_2+3u_3-v_1+2v_2-3v_3,
\]
so \(W=0\).

The remaining \(r\)-linear \(E_4\) equations have rank two and a pivot
\[
6s^4
\]
solving \(b_0,L_{31}\):
\[
\begin{aligned}
b_0&=b_1-b_3+\frac14(v_1-2v_2+3v_3)^2,\\
L_{31}&=L_{32}
       +\frac12(t_0-t_2)(v_1-2v_2+3v_3).
\end{aligned}
\]

Put \(V=v_1-2v_2+3v_3\).  The non-\(r\) \(E_4\) system has rank two and
requires two fresh charts:

- If \(V\ne0\), the pivot
  \[
  -\frac94s^2V^2
  \]
  solves \((a_0,b_1)\), all remaining \(E_4\) coefficients vanish, and
  direct substitution gives \(\det L=0\).
- If \(V=0\), recomputation before the \(V\)-division gives the pivot
  \[
  -9s^2
  \]
  solving \((L_{11},L_{21})=(l_0,l_3)\); again every remaining \(E_4\)
  coefficient vanishes and direct substitution gives \(\det L=0\).

Thus the whole punctured intersection is incompatible with the Keller
condition.

## 3. Origin

At \(k=s=0\), a fresh \(E_6\) pivot
\[
31104
\]
solves
\[
(a_{pr},a_{qr},a_{r^2},b_{pr},b_{r^2}).
\]
After this complete solve,
\[
\begin{aligned}
[p^3r]E_4&=3b_{qr}^2,\\
[q^3r]E_4&=\frac13(3b_{qr}-4L_{33})^2.
\end{aligned}
\]
Hence \(b_{qr}=L_{33}=0\), and the five \(E_6\)-pivot variables then also
vanish identically.  All six nonbinary quadratic coefficients are zero.
Since the contact is the origin, the cubic contact terms vanish too, so
every nonlinear homogeneous term is binary.

After subtracting the constant, the invertible linear part permits a target
linear change putting the map in the form
\[
(g_1(p,q),g_2(p,q),r+g_3(p,q)).
\]
The first two coordinates form a plane Keller map of degree at most four.
Moh's unconditional degree-\(<100\) theorem makes it an automorphism, and
the triangular lift is an automorphism.

## Frozen verdict

The four-chart lower descent excludes the complete frozen D4-DN-3 family,
provided the displayed exact calculations survive independent verification
and post-freeze comparison.
