# The coupled two-/three-skew feature as one shifted exterior inequality

## Status

This note gives an exact, lossless reduction of the coupled logical
feature target and an exact obstruction to the most direct matched-Gram
certificate.  It does **not** prove the remaining inequality and does
not give a negative Werner witness.

Let
\[
\begin{aligned}
 {\cal J}_2(C)
 &=\frac34N-\frac12S+\frac14P,\\
 {\cal J}_3(C)
 &=\frac18(N-S+P-T),
\end{aligned}                                             \tag{1}
\]
where
\[
\begin{aligned}
 N&=\|C\|_2^2,&
 S&=\sum_i\|\operatorname{Tr}_iC\|_2^2,\\
 P&=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2,&
 T&=|\operatorname{Tr}C|^2 .
\end{aligned}
\]
For a rank-at-most-two matrix let \(s_1,s_2\) be its two
possibly nonzero singular values.  The complete coupled target is
exactly
\[
\boxed{\qquad
 {\cal J}_2(C)+2{\cal J}_3(C)+s_1s_2\geq0 .
\qquad}                                                   \tag{2}
\]
If \(\Pi_2\) is the orthogonal projection onto the operator sector
having exactly two traceless qutrit factors, then (2) is equivalently
\[
\boxed{\qquad
 \|\Pi_2C\|_2^2
 \leq\frac49\left(\|C\|_2^2+s_1s_2\right).
\qquad}                                                   \tag{3}
\]
Thus the two- and three-skew contributions do not merely satisfy a
joint upper estimate: after their exact cancellation, only one
degree-two mass and the global rank-two exterior norm remain.

The dependency-free exact checker is
`verification/verify_n3_coupled_skew_exterior_target.py`.

## 1. Exact sector collapse

The partial-trace formula for the exact degree-two component is
\[
\boxed{\qquad
 \|\Pi_2C\|_2^2
 =\frac13S-\frac29P+\frac19T .
\qquad}                                                   \tag{4}
\]
Indeed, the three orthogonal summands of \(\Pi_2\) have one scalar
and two traceless local factors.  Applying
\({\cal P}_i(C)=I_i\otimes\operatorname{Tr}_iC/3\) and
\({\cal Q}_i=I-{\cal P}_i\), and then using orthogonality, gives
(4) directly.

Equations (1) and (4) give the identity
\[
\boxed{
\begin{aligned}
 {\cal J}_2(C)+2{\cal J}_3(C)
 &=N-\frac34S+\frac12P-\frac14T\\
 &=N-\frac94\|\Pi_2C\|_2^2 .
\end{aligned}}                                           \tag{5}
\]
For rank two,
\[
 s_1s_2=\|\wedge^2C\|_2,                                 \tag{6}
\]
so (2) is precisely the exterior inequality (3).

There is no separated estimate in (5).  The negative part of
\({\cal J}_2\) and the compensating triple-skew part of
\(2{\cal J}_3\) have collapsed before any inequality is applied.
The exact small counterpencil in
`agent_n3_q2_small_qubit_counterfamily.md` violates the separated
\({\cal J}_2+s_1s_2/2\) inequality but satisfies (2) strictly.

## 2. Equivalence to the coupled feature concurrence

Let \(U,V:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) be the two
physical code frames, and let \(Q_{(2)},Q_{(3)}\) be the positive
two-qubit feature operators
\[
\begin{aligned}
 Q_{(2)}
 &=\operatorname{comp}\left[
 \frac49\sum_{i<j}{\mathsf A}_i{\mathsf A}_j\right],\\
 Q_{(3)}
 &=\operatorname{comp}\left[
 \frac89{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3\right],
 \qquad {\mathsf A}_i=\frac{I-F_i}{2}.
\end{aligned}                                             \tag{7}
\]
Put \(Q=Q_{(2)}+Q_{(3)}\).  The determinant-one filter formula for
homogeneous two-qubit concurrence says
\[
 {\cal C}(Q)
 =
 \sup_{A,B\in SL(2,\mathbb C)}
 \left\{-\operatorname{Tr}\left[
 F_{\rm L}(A\otimes B)Q(A\otimes B)^\dagger
 \right]\right\}_+ .                                     \tag{8}
\]
After applying \(A,B\), write the two filtered physical frames as
\(X,Y\), and put \(C=XY^\dagger\).  They obey
\[
 s_1(C)s_2(C)
 =\sqrt{\det(X^\dagger X)\det(Y^\dagger Y)}=1.           \tag{9}
\]
The swap/partial-transpose contraction gives, without an estimate,
\[
 \operatorname{Tr}\left[F_{\rm L}Q\right]
 =\frac49\left({\cal J}_2(C)+2{\cal J}_3(C)\right).
                                                               \tag{10}
\]
Consequently
\[
\boxed{\qquad
 {\cal C}(Q)\leq\frac49\ \hbox{for all code planes}
 \quad\Longleftrightarrow\quad
 \text{(2) for all rank-at-most-two }C .
\qquad}                                                   \tag{11}
\]
The converse follows by dividing an arbitrary rank-two \(C\) by
\(\sqrt{s_1s_2}\), taking its singular-value decomposition, and
viewing the two factors as determinant-one filters of isometries.
Rank one follows by continuity.  Thus (3) is a lossless common-plane
exterior formulation of the coupled feature theorem, not a numerical
relaxation.

## 3. The shifted two-by-two determinant

Write
\[
 C=s_1E_1+e^{i\theta}s_2E_2,\qquad
 E_r=|u_r\rangle\langle v_r|,
                                                               \tag{12}
\]
where both displayed pairs are orthonormal.  Define
\[
 G_{rs}=\langle E_r,\Pi_2E_s\rangle_{\rm HS},\qquad
 \mu=\frac49,
                                                               \tag{13}
\]
and the two rank-one slacks
\[
 p=\mu-G_{11},\qquad q=\mu-G_{22}.                       \tag{14}
\]
The sharp rank-one theorem gives \(p,q\geq0\).  Substitution of
(12) into (3), followed by minimization over the relative phase and
the ratio \(s_2/s_1\), gives the exact scalar determinant
\[
\boxed{\qquad
 |G_{12}|
 \leq\frac29+\sqrt{pq}.
\qquad}                                                   \tag{15}
\]
Indeed, after choosing the adverse phase, the defect in (3) is
\[
 ps_1^2+qs_2^2+
 2s_1s_2\left(\frac29-|G_{12}|\right).                  \tag{16}
\]
Copositivity of this binary quadratic for all \(s_1,s_2\geq0\) is
exactly (15).  At equality in (15), inserting the bound in (16)
leaves
\[
 \left(s_1\sqrt p-s_2\sqrt q\right)^2.                  \tag{17}
\]

## 4. Exact obstruction to an ordinary matched-slack correction

Let
\[
 {\mathsf S}=\left(\frac49I-\Pi_2\right)^\Gamma\succeq0
                                                               \tag{18}
\]
and compress it to the four product columns
\(u_a\otimes v_b\), ordered as \(00,01,10,11\).  Call the resulting
positive matrix \(Q\).  Partial-transpose index crossing gives
\[
 Q_{00,00}=p,\qquad Q_{11,11}=q,\qquad
 Q_{01,10}=-G_{12}.                                     \tag{19}
\]
Positivity supplies the ordinary matched Gram entry
\[
 m=Q_{00,11},\qquad |m|\leq\sqrt{pq}.                   \tag{20}
\]
It is therefore tempting to prove (15) from the phase-covariant
triangle
\[
 |Q_{01,10}-m|\stackrel{?}{\leq}\frac29.                \tag{21}
\]
This fails at the sharpest possible elementary code.

Take
\[
\begin{aligned}
 (u_0,u_1)&=(|000\rangle,|001\rangle),\\
 (v_0,v_1)&=(|110\rangle,|111\rangle).
\end{aligned}                                             \tag{22}
\]
Exact contraction gives
\[
 G=\frac13
 \begin{pmatrix}1&1\\1&1\end{pmatrix},                  \tag{23}
\]
so \(p=q=1/9\) and (15) is an equality.  On the complete four-column
compression one instead has
\[
\boxed{
 Q=
 \begin{pmatrix}
 1/9&0&0&0\\
 0&4/9&-1/3&0\\
 0&-1/3&4/9&0\\
 0&0&0&1/9
 \end{pmatrix}.}                                         \tag{24}
\]
Thus
\[
 m=0,\qquad |Q_{01,10}-m|=\frac13>\frac29.              \tag{25}
\]
The ordinary matched slack contributes none of the universal
\(2/9\) correction at this equality point.  Any successful Gram
certificate must instead construct a genuinely Hodge/Pluecker
correction that transforms with the phase of \(G_{12}\) and equals
\(2/9\) on (22).  Replacing it by a matched positive-Gram entry
cannot work.

## 5. Remaining exact lemma

The coupled two-/three-skew program is now the single statement
\[
\boxed{\qquad
 \|\Pi_2C\|_2^2
 \leq\frac49\left(\|C\|_2^2+\|\wedge^2C\|_2\right)
 \quad(\operatorname{rank}C\leq2).
\qquad}                                                   \tag{26}
\]
Equivalently, prove the shifted determinant (15) for every pair of
common qutrit three-copy planes.

The obstruction (24)--(25) shows that the needed \(2/9\) term is not
an arbitrary scalar allowance and is not the ordinary matched
Cauchy--Schwarz correction.  It must arise from a coherent
second-compound contraction of the two common decomposable code
bivectors.  Establishing that contraction, or finding a physical
violation of (15), is the remaining task.
