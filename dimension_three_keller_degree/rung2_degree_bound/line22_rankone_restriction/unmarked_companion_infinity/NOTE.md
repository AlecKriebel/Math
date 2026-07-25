# Exclusion of the unmarked companion-at-infinity orbit

**Status:** audited exact theorem. A dependency-free hostile reconstruction
passed on 2026-07-25T10:00:00Z. This has not been peer reviewed. Exact
computer checks verify the encoded algebra; they are not peer review.

**Recorded:** 2026-07-25T07:18:00Z.

## 1. Statement

Let
\[
 F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
 \mathbb A^3_{\mathbb C}
\]
have degree four, with each \(H_i\) homogeneous of degree \(i\). Put
\[
 p=x^2,\qquad q=y^2+xz
\]
and suppose
\[
 H_4=\bigl((p-q)^2,(p+q)^2,0\bigr),\qquad (H_3)_3=xq.       \tag{1}
\]
This is the companion-at-infinity orbit in the unmarked-critical family of
the rank-one-restriction line-\((2,2)\) pencil.

There is no loss in omitting a constant term: postcomposing with the target
translation \(Y\mapsto Y-F(0)\) leaves the Jacobian and every positive-degree
homogeneous part unchanged.

### Theorem

No Keller map has the leading data (1).

The result is only about this exact joint orbit. It does not assert that all
line-\((2,2)\) leading forms have been excluded.

## 2. The complete degree-seven kernel

Write
\[
 P=(p-q)^2,\qquad Q=(p+q)^2,\qquad R=xq,
\]
\[
 U=(H_3)_1,\qquad V=(H_3)_2,\qquad W=(H_2)_3,
\]
and
\[
 \partial=2y\partial_z-x\partial_y.
\]
The degree-eight identity is
\[
 E_8=\operatorname{Jac}(P,Q,R)=0.
\]
Direct expansion of the next identity gives
\[
\boxed{
E_7=2\left(
8x(p-q)(p+q)\partial W
+(p+q)(2p-q)\partial U
-(p-q)(2p+q)\partial V
\right)}                                                   \tag{2}
\]
Here \(U,V\) range over all cubics and \(W\) over all quadratics, so (2) is a
linear map with \(26\) unknown coefficients. Its exact rank is \(18\). In
the monomial orders encoded in the verifier, a constant maximal minor is
\[
 1709960483517235200.                                      \tag{3}
\]

Six evident kernel directions are
\[
\begin{gathered}
(x^3,0,0),\quad(xq,0,0),\quad(0,x^3,0),\quad(0,xq,0),\\
(0,0,p),\quad(0,0,q).
\end{gathered}                                              \tag{4}
\]
There are also the source-translation jets
\[
 \tau_x=(P_x,Q_x,R_x),\qquad
 \tau_y=(P_y,Q_y,R_y),\qquad
 \tau_z=(P_z,Q_z,R_z).                                     \tag{5}
\]
The eight directions consisting of (4), \(\tau_x\), and \(\tau_y\) have a
coefficient minor equal to \(-8\). The third jet is not an omitted kernel
direction: it satisfies the exact relation
\[
 \tau_z+2(x^3,0,0)-2(xq,0,0)-2(0,x^3,0)-2(0,xq,0)
 -(0,0,p)=0.                                               \tag{6}
\]
Equations (3)--(6), together with nullity \(26-18=8\), prove that this is the
complete raw kernel.

Affine source translations in \(x,y\) remove the coefficients of
\(\tau_x,\tau_y\). Target shears adding the third component to either of the
first two remove the two \(xq=R\) directions. These operations only relabel
lower homogeneous coefficients. Thus every solution of \(E_7=0\) has the
complete gauge
\[
 H_3=(A x^3,B x^3,xq),\qquad
 W=w_0p+w_1q.                                              \tag{7}
\]
No generic-rank inference or division by a modulus occurs.

## 3. Constant degree-six forcing

Use the adapted basis for the first two entries of \(H_2\):
\[
\begin{aligned}
(H_2)_1={}&u_0p+u_qq+\widehat u_1xy+\widehat u_2xz
                    +\widehat u_3yz+\widehat u_4z^2,\\
(H_2)_2={}&v_0p+v_qq+\widehat v_1xy+\widehat v_2xz
                    +\widehat v_3yz+\widehat v_4z^2.
\end{aligned}                                              \tag{8}
\]
Write \(L=(\ell_{ij})\). After (7), \(E_6\) is a homogeneous linear system
in exactly the ten variables
\[
\ell_{32},\ell_{33},
\widehat u_1,\widehat u_2,\widehat u_3,\widehat u_4,
\widehat v_1,\widehat v_2,\widehat v_3,\widehat v_4.        \tag{9}
\]
It is independent of \(A,B,w_0,w_1,u_0,u_q,v_0,v_q\) and the other seven
entries of \(L\). A \(10\times10\) minor is the nonzero integer
\[
 4831838208.                                               \tag{10}
\]
Exact row reduction therefore forces every variable in (9) to vanish:
\[
\ell_{32}=\ell_{33}=0,\qquad
(H_2)_1,(H_2)_2\in\langle p,q\rangle.                      \tag{11}
\]
Substitution of (11) makes every coefficient of \(E_6\) identically zero.
Thus (11) is the full solution, not a selection of necessary equations.

## 4. Degree-five determinant exit

After (11), four literal coefficients of \(E_5\) are
\[
\begin{aligned}
[x^5]E_5&=-4(\ell_{12}-\ell_{22}),\\
[x^4z]E_5&=-2(\ell_{12}+\ell_{22}),\\
[x^4y]E_5&=8(\ell_{13}-\ell_{23}),\\
[x^3yz]E_5&=4(\ell_{13}+\ell_{23}).
\end{aligned}                                              \tag{12}
\]
There is no parameter in a denominator. The first two equations give
\(\ell_{12}=\ell_{22}=0\), and the last two give
\(\ell_{13}=\ell_{23}=0\). Together with (11), the second and third columns
of \(L\) vanish. Hence
\[
 \det L=0.
\]
For a Keller map the constant term of the Jacobian determinant is
\(\det L\in\mathbb C^\times\), a contradiction. This proves the theorem.

## 5. Exact verification and disclosure

The package contains:

- `verify_unmarked_infinity_sympy.py`, which reconstructs the full raw
  \(E_7\) matrix, kernel and gauges, the constant \(E_6\) forcing minor and
  converse, and the \(E_5\) determinant exit;
- `verify_unmarked_infinity_pari.gp`, an independent PARI/GP reconstruction;
- `verify_unmarked_infinity_pari_strict.sh`, which requires the exact PARI
  transcript; and
- `test_fail_closed.sh`, which rejects optimized Python, forged exact minors,
  and forged PARI diagnostics.

Run from this directory:

```text
/usr/bin/python3 -u verify_unmarked_infinity_sympy.py
./verify_unmarked_infinity_pari_strict.sh
./test_fail_closed.sh
```

The two implementations use the same coefficient-matrix method in different
computer algebra systems; this is independent implementation evidence, not
methodologically independent mathematics.

The hostile verifier in `audit_hostile/` instead implements sparse
multivariate arithmetic directly over \(\mathbb Q\), reconstructs the full
Jacobian, proves the raw rank by a rank sandwich, and independently checks
the gauge quotient, \(E_6\) converse, and \(E_5\) determinant exit. Its
strict transcript and four fault injections pass.

This theorem and its artifacts were developed with AI assistance. The work
has not been peer reviewed. The exact checks establish facts about the
encoded polynomial identities and do not replace expert review.
