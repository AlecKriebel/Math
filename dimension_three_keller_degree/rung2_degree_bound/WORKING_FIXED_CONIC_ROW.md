# Working calculation: the binary fixed-divisor conic row

**Status:** exact exploratory calculation; two split-root tangent branches
are closed, while the zero-tangent and double-root branches remain.  No
claim in this note is promoted pending an independent raw-system audit.
This is not peer reviewed.

**Recorded:** 2026-07-25T02:47:00Z.

## 1. Setup and finite branch reduction

Consider the fixed-divisor conic row
\[
H_4=h(p,q)A(p,q),\qquad A=(p^2,pq,q^2)^T,
\tag{1}
\]
where \(h\) is a binary quadratic and \(r\) is a complementary source
coordinate.  The automorphism group of the Veronese conic reduces \(h\) to
\[
h=pq\quad\text{or}\quad h=p^2.
\tag{2}
\]
Put \(A_p=\partial_pA,A_q=\partial_qA\).  The degree-eight equation and
Hilbert--Burch give
\[
\begin{split}
H_3={}&V(p,q)
+r\bigl((ap+bq)A_p+(cp+dq)A_q\bigr)\\
&+\frac{r^2}{2}(eA_p+fA_q).
\end{split}
\tag{3}
\]

A raw degree-seven solve first forces \(e=f=0\).  In the split-root case it
then forces \(b=c=0\), while in the double-root case it forces \(b=0\).
The coefficient of \(r^2\) in the degree-six identity is respectively
\[
\boxed{12p^2q^2(a-d)^2(a+d)}
\tag{4}
\]
and
\[
\boxed{24dp^2\bigl(cp+(d-a)q\bigr)^2.}
\tag{5}
\]
Thus the nonzero tangent fields reduce to a finite list:

- for \(h=pq\), \(d=a\) or \(d=-a\);
- for \(h=p^2\), either \(d=0\), or \(c=0,d=a\).

Residual source changes preserving (1), followed by scaling \(r\), reduce
the nonzero cases to scalar, semisimple, or nilpotent Jordan
representatives.  The tangent-zero case must be treated separately.

## 2. Split roots and the opposite-weight field

Let \(h=pq\) and normalize
\[
\partial_rH_3=pA_p-qA_q.
\tag{6}
\]
After solving degree seven, the eight degree-six compatibility equations
include
\[
w_{15}=0,\quad v_9=0,\quad
4v_{10}+3w_{16}-2w_9=0,
\]
\[
-12v_{11}+8v_6+6w_{10}-w_3=0,\quad
w_4=v_7=w_2=w_{12}=0.
\tag{7}
\]
With (7) imposed, the degree-five coefficient is linear in the six
remaining entries of \(L_0\).  Its exact left-nullspace contains the
constant compatibility equation
\[
\boxed{64=0.}
\tag{8}
\]
Hence this branch contains no Keller map.

## 3. Split roots and the scalar field

Now normalize
\[
\partial_rH_3=2A.
\tag{9}
\]
Degrees seven through five reduce the cubic and quadratic pieces to the
following compact parametrization:
\[
H_3=
\begin{pmatrix}
(U-X)p^3+(V-Y)p^2q\\
Up^2q+Vpq^2\\
(U+X)pq^2+(V+Y)q^3
\end{pmatrix}
+2rA,
\tag{10}
\]
and
\[
\begin{aligned}
(H_2)_1={}&(18XY+8XT-8YS-4ST-C+2B_1)p^2\\
&+(9Y^2+8YT+2T^2+2B_2)pq+2Tpr,\\
(H_2)_2={}&B_0p^2+B_1pq+B_2q^2+Spr+Tqr,\\
(H_2)_3={}&(9X^2-8XS+2B_0+2S^2)pq+Cq^2+2Sqr.
\end{aligned}
\tag{11}
\]

Four degree-four left-null certificates are exact squares.  Successively
they give
\[
\boxed{
S=2X,\quad T=-2Y,\quad
B_0=UX-X^2,\quad B_2=-VY-Y^2.
}
\tag{12}
\]
The remaining degree-four coefficient gives
\[
\boxed{C=B_1+UY+VX+XY.}
\tag{13}
\]

Write the two still-free entries of the linear part as
\(\ell_4,\ell_7\).  Degrees six through four then force
\[
L_0=
\begin{pmatrix}
-2B_1Y+2CY-UY^2-XY^2+2\ell_4&
Y^2(V+Y)&2Y^2\\
\frac{2B_1X-2CX+VX^2+3X^2Y+\ell_7}{2}&
\ell_4&-2XY\\
X^2(U-X)&\ell_7&2X^2
\end{pmatrix}.
\tag{14}
\]
The complete degree-two coefficient is the square
\[
\boxed{E_2=(Rp-2Qq)^2,}
\tag{15}
\]
where
\[
\begin{aligned}
Q&=B_1Y+UY^2+\ell_4,\\
R&=-2B_1X-2UXY+VX^2+X^2Y+\ell_7.
\end{aligned}
\tag{16}
\]
Hence \(Q=R=0\).  But direct expansion of (14) gives
\[
\det L_0=
\bigl(VX^2Y+X^2Y^2+2X\ell_4+Y\ell_7\bigr)^2.
\tag{17}
\]
Substituting \(Q=R=0\) into (17) makes its squared factor identically zero.
Thus this branch also contains no Keller map.

## 4. Remaining cases

The following cases are still open in this calculation:

1. \(h=pq\) with \(\partial_rH_3=0\);
2. \(h=p^2\) with scalar tangent field;
3. \(h=p^2\) with a semisimple one-zero-eigenvalue tangent field;
4. \(h=p^2\) with a nilpotent tangent field;
5. \(h=p^2\) with zero tangent field.

For the split-root zero-tangent case, degree seven has the exact form
\[
\partial_rH_2=\alpha A_p+\beta A_q.
\]
The residual conic symmetry reduces its nonzero locus to the cases where
one or both of \(\alpha,\beta\) are nonzero.  This is the next finite
elimination target.

## 5. Disclosure and verification boundary

All displayed coefficients were obtained by exact determinant expansion
with a completely general binary cubic vector, a completely general
quadratic vector, and an arbitrary \(3\times3\) linear part.  The compact
parametrization (10)--(14) was substituted back into the raw determinant
before (15)--(17) were factored.

An exact permanent regression and an independent derivation have not yet
been completed.  The present note is therefore a checkpoint, not a banked
theorem.  It was developed with AI assistance.  Exact algebra is evidence
about the encoded calculation, not peer review.
