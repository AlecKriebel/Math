# Exclusion of the unmarked finite resonance \(c^2=9\)

**Status:** audited exact theorem. An independent hostile reconstruction
passed on 2026-07-25T09:55:40Z. This has not been peer reviewed. Exact
computer checks verify the encoded algebra; they are not peer review.

**First recorded:** 2026-07-25T07:49:45Z.

## 1. Statement

Let
\[
F=F(0)+LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have degree four, where each \(H_j\) is homogeneous of degree \(j\). Put
\[
p=x^2,\qquad q=y^2+xz
\]
and suppose
\[
H_4=\bigl((p-q)^2,(p+q)^2,0\bigr),\qquad
(H_3)_3=x(p-3q).                                      \tag{1}
\]

### Theorem

No Keller map has the leading data (1).

The two values \(c=3\) and \(c=-3\) are the same joint orbit. Indeed, the
source change
\[
(x,y,z)\longmapsto(x,iy,-z)
\]
sends \(p\) to \(p\) and \(q\) to \(-q\). Composing with the target
transposition of the first two coordinates restores the displayed order of
\(((p-q)^2,(p+q)^2)\) and sends \(x(p-cq)\) to \(x(p+cq)\). Thus the theorem
excludes the full finite resonance \(c^2=9\).

The result is confined to this exact joint orbit in the
rank-one-restriction line-\((2,2)\) pencil. It is not, by itself, a theorem
about every degree-four leading form.

## 2. Weighted Jacobian equations

Write
\[
P=(p-q)^2,\qquad Q=(p+q)^2,\qquad R=x(p-3q),
\]
\[
U=(H_3)_1,\qquad V=(H_3)_2,\qquad W=(H_2)_3.
\]
Introduce a bookkeeping variable \(s\) and set
\[
\det\!\left(L+sJH_2+s^2JH_3+s^3JH_4\right)
  =\sum_{j=0}^8 E_js^j.                               \tag{2}
\]
For a Keller map, \(E_1,\ldots,E_8\) vanish and
\[
E_0=\det L\ne0.                                       \tag{3}
\]
For a polynomial \(E\), the notation \([m]E\) denotes the coefficient of
the monomial \(m\).

## 3. Complete raw \(E_7\) kernel and gauge

Put
\[
\partial=2y\partial_z-x\partial_y.
\]
The top identity \(E_8=\operatorname{Jac}(P,Q,R)=0\) holds. Direct expansion
of the next equation gives the compact identity
\[
\boxed{
E_7=2\left(
8x(p-q)(p+q)\partial W
+3(p+q)(q-3p)\partial U
+3(p-q)(p+q)\partial V
\right).}                                             \tag{4}
\]
Here \(U,V\) range over all cubics and \(W\) over all quadratics. The
resulting \(36\times26\) coefficient matrix has exact rank \(14\). A fixed
maximal minor in the encoded monomial orders is
\[
-1039973956284579840.                                  \tag{5}
\]

Four gauge directions are
\[
(R,0,0),\quad(0,R,0),\quad
\partial_x(P,Q,R),\quad\partial_y(P,Q,R).              \tag{6}
\]
The following eight directions complement them:
\[
\begin{gathered}
(xq,0,0),\quad(0,xq,0),\\
\bigl(y(p-q),y(3p-q),0\bigr),\quad
\bigl(z(p-q),z(3p-q),0\bigr),\\
(0,0,p),\\
(0,8x^2z,3y^2),\quad
(0,-8xyz,3yz),\quad
(0,-8xz^2,3z^2).
\end{gathered}                                         \tag{7}
\]
All twelve vectors lie in the kernel. Their coefficient matrix has rank
\(12\), with fixed minor
\[
49152.                                                  \tag{8}
\]
Since the nullity is \(26-14=12\), (6)--(7) give the complete raw kernel.

On the four gauge directions (6), the coordinate functionals
\[
[x^3]U,\quad[x^3]V,\quad[xy]W,\quad[xz]W
\]
have determinant \(-36\). Hence the gauge is valid over characteristic
zero without dividing by a parameter. Source translations remove the two
translation jets, and target shears by the third component remove the two
\(R\)-directions. Every solution of \(E_7=0\) therefore has the complete
normal form
\[
\begin{aligned}
U={}&A\,xq+C\,y(p-q)+D\,z(p-q),\\
V={}&B\,xq+C\,y(3p-q)+D\,z(3p-q)\\
   &\quad+8e\,x^2z-8f\,xyz-8g\,xz^2,\\
W={}&w\,p+3e\,y^2+3f\,yz+3g\,z^2.
\end{aligned}                                         \tag{9}
\]

## 4. Division-free \(E_6\) compatibility

Write
\[
\begin{aligned}
(H_2)_1={}&u_0p+u_qq+u_1xy+u_2xz+u_3yz+u_4z^2,\\
(H_2)_2={}&v_0p+v_qq+v_1xy+v_2xz+v_3yz+v_4z^2,
\end{aligned}                                         \tag{10}
\]
and write \(L=(\ell_{ij})\).

The compatibility restrictions in \(E_6=0\) can be read from four literal
coefficient combinations. No rank specialization and no division by a
modulus is used:
\[
[xyz^4]E_6=192g^2.                                    \tag{11}
\]
After \(g=0\),
\[
-[x^2yz^3]E_6+[y^5z]E_6=144f^2.                      \tag{12}
\]
After \(g=f=0\),
\[
\begin{aligned}
&[x^4yz]E_6-[x^3y^3]E_6-2[x^3yz^2]E_6\\
&\qquad+[x^2y^3z]E_6+[x^2yz^3]E_6
   =-48(D+2e)^2.                                      \tag{13}
\end{aligned}
\]
After \(g=f=0\) and \(D=-2e\),
\[
[x^5y]E_6-[x^3y^3]E_6-[x^3yz^2]E_6+[x^2y^3z]E_6
  =24C^2.                                             \tag{14}
\]
Equations (11)--(14), successively, force
\[
g=0,\qquad f=0,\qquad D=-2e,\qquad C=0.               \tag{15}
\]

For adversarial redundancy, both exact implementations also reconstruct
cleared polynomial left-kernel vectors for the full \(E_6\) lower-coefficient
matrix. Their pairings reproduce (11)--(14), so the displayed identities
do not arise from silently clearing a denominator.

## 5. Complete surviving \(E_6\) solve

After (15), the degree-three and third degree-two pieces are
\[
\begin{aligned}
U&=A\,xq-2e\,z(p-q),\\
V&=B\,xq+2e\,z(p+q),\\
W&=w\,p+3e\,y^2.                                      \tag{16}
\end{aligned}
\]
Regarding \(E_6\) as a linear system in
\[
(u_0,u_q,u_1,u_2,u_3,u_4,
v_0,v_q,v_1,v_2,v_3,v_4,\ell_{32},\ell_{33}),          \tag{17}
\]
its rank is exactly \(8\). A constant maximal minor is
\[
5159780352.                                            \tag{18}
\]
Exact row reduction gives the complete solution
\[
\begin{aligned}
u_1&=0,&u_2&=Ae,&u_3&=0,&u_4&=e^2,\\
v_1&=-\frac83\ell_{32},&
v_2&=Be+8e^2-\frac83\ell_{33},&
v_3&=0,&v_4&=e^2.
\end{aligned}                                         \tag{19}
\]
The six entries \(u_0,u_q,v_0,v_q,\ell_{32},\ell_{33}\) remain free.
Substitution of (19) makes all of \(E_6\) identically zero, proving the
converse as well as necessity.

## 6. The \(E_5\) resonance split

Three coefficients of \(E_5\), after (19), are
\[
\begin{aligned}
[x^5]E_5={}&
 (12A-4B-32e-\tfrac{32}{3}w)\ell_{32}
+18\ell_{12}-6\ell_{22},\\
[x^4z]E_5={}&
 (2A+2B+32e+\tfrac{32}{3}w)\ell_{32}
+12\ell_{12},\\
[x^3z^2]E_5={}&
-2(A-B)\ell_{32}-6\ell_{12}+6\ell_{22}.
\end{aligned}                                         \tag{20}
\]
Their coefficient matrix in
\((\ell_{12},\ell_{22},\ell_{32})\) has determinant
\[
-96S,\qquad S=-6A+3B+48e+16w.                         \tag{21}
\]
If \(S\ne0\), (20) forces the second column of \(L\) to vanish, contrary
to (3).

If \(S=0\) but \(\ell_{32}=0\), the second equation in (20) gives
\(\ell_{12}=0\), and the third then gives \(\ell_{22}=0\). Again the second
column of \(L\) vanishes. Therefore a Keller map would have to satisfy
\[
B=2A-16e-\frac{16}{3}w,\qquad \ell_{32}\ne0.           \tag{22}
\]

On (22), the complete \(E_5\) system has rank \(4\) in
\((\ell_{12},\ell_{13},\ell_{22},\ell_{23})\), with constant minor
\[
20736.                                                  \tag{23}
\]
Its unique solution is
\[
\begin{aligned}
\ell_{12}&=-\frac A2\ell_{32},\\
\ell_{22}&=\frac{-15A+96e+32w}{18}\ell_{32},\\
\ell_{13}&=\frac A2(3e^2-\ell_{33})+eu_q,\\
\ell_{23}&=\frac{15A-96e-32w}{18}(3e^2-\ell_{33})+ev_q.
\end{aligned}                                         \tag{24}
\]
Direct substitution verifies every coefficient of \(E_5\).

## 7. The \(E_4\) exit

After (22)--(24), two literal coefficients finish the argument:
\[
[x^2z^2]E_4=\frac{16}{3}\ell_{32}(3e^2-\ell_{33}).
                                                               \tag{25}
\]
Because \(\ell_{32}\ne0\), equation (25) forces
\(\ell_{33}=3e^2\). On that locus,
\[
[x^3y]E_4=\frac{16}{3}\ell_{32}^2.                    \tag{26}
\]
Equation (26) contradicts \(\ell_{32}\ne0\). Thus every branch either has
\(\det L=0\) or fails a positive-degree Jacobian equation. No Keller map
has the leading data (1).

## 8. Verification and disclosure

The package contains:

- `verify_resonance_c3_sympy.py`, an exact SymPy reconstruction of the raw
  kernel, gauge, compatibility tree, complete lower solves, and exit;
- `verify_resonance_c3_pari.gp`, an independent exact PARI/GP
  reconstruction from the full determinant (2), including polynomial
  left-syzygy clearing;
- `verify_resonance_c3_pari_strict.sh`, which accepts only the exact PARI
  success transcript; and
- `test_fail_closed.sh`, which rejects optimized Python, forged exact
  constants, and forged PARI diagnostics.

The independent hostile-audit directory additionally contains a clean
PARI/GP reconstruction with reversed monomial and raw-variable orders. It
checks the constant rank floor through every \(E_6\) specialization, the
complete \(E_5\) branch cover, the two final \(E_4\) pivots, and the exact
\(c=3\leftrightarrow-3\) conjugacy. Its strict runner and four targeted
fault injections pass.

Run from this directory:

```text
/usr/bin/python3 -u verify_resonance_c3_sympy.py
./verify_resonance_c3_pari_strict.sh
./test_fail_closed.sh
./audit_hostile/verify_hostile_pari_strict.sh
./audit_hostile/test_fail_closed.sh
```

The two computer-algebra implementations are independent implementations,
but both ultimately expand exact polynomial identities. They are evidence
about the encoded algebra, not peer review and not a replacement for expert
mathematical review.

This theorem and its artifacts were developed with AI assistance. The scope
is the exact \(c^2=9\) orbit stated above; no claim is made here that the
surrounding orbit taxonomy is exhaustive.
