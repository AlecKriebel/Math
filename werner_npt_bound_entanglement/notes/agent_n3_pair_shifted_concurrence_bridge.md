# The feature concurrence controls the sharp shifted pair inequality

## Status

This note gives an exact implication, not a proof of the remaining
Hodge inequality.

Let \(\Pi _2\) be the exact degree-two projection on three qutrit
operator factors.  The still-unproved feature-state bound
\[
 {\cal C}(Q)\leq\frac49                                      \tag{1}
\]
from the Takagi--Hodge reduction implies the stronger quantitative
pair-sector conjecture
\[
 \boxed{\qquad
 \|\Pi _2C\|_2^2
 \leq\frac49\left(s_1(C)^2+s_2(C)^2+s_1(C)s_2(C)\right)
 \qquad(\operatorname{rank}C\leq2).
 \qquad}                                                     \tag{2}
\]
Thus (1) does more than imply the unshifted \(2/3\) pair theorem.
It proves the newly observed sharp singular-value interpolation.

The note also proves (2) on the complete exact rank-one-saturation
boundary, using the proved saturation spectral gap.

The dependency-free exact checker is
`verification/verify_n3_pair_shifted_concurrence_bridge.py`.

## 1. The shifted Gram target

Write a singular-value decomposition
\[
 C=s_1E_1+s_2E_2,\qquad
 E_r=|u_r\rangle\langle v_r|,                             \tag{3}
\]
where the two \(u_r\)'s and the two \(v_r\)'s are separately
orthonormal.  A relative phase can be absorbed into \(E_2\), so it
is necessary to control the modulus of the cross term.  Put
\[
 G_{rs}=\langle E_r,\Pi _2E_s\rangle_{\rm HS}.            \tag{4}
\]
The sharp rank-one theorem gives
\[
 0\leq G_{11},G_{22}\leq\frac49.                          \tag{5}
\]
Set
\[
 p=\frac49-G_{11},\qquad q=\frac49-G_{22}.                \tag{6}
\]
The scalar shifted determinant is
\[
 \boxed{\qquad
 |G_{12}|\leq\frac29+\sqrt{pq}.
 \qquad}                                                   \tag{7}
\]

Indeed, (7) implies (2), because
\[
\begin{aligned}
 \|\Pi _2C\|_2^2
 &\leq
 \left(\frac49-p\right)s_1^2
 +\left(\frac49-q\right)s_2^2
 +2s_1s_2\left(\frac29+\sqrt{pq}\right)\\
 &=\frac49(s_1^2+s_2^2+s_1s_2)
   -\left(s_1\sqrt p-s_2\sqrt q\right)^2.
                                                               \tag{8}
\end{aligned}
\]
Conversely, optimizing (2) over the ratio \(s_2/s_1\) gives (7)
whenever \(|G_{12}|>2/9\), so this is the exact \(2\times2\)
form of the strengthened conjecture.

## 2. The positive logical feature state

On the two physical replicas let
\[
 S=\left(\frac49I-\Pi _2\right)^\Gamma
 =\frac49\Pi_{q=2}^-+\frac{20}{9}\Pi_{q=3}^-\succeq0,     \tag{9}
\]
where \(q\) counts antisymmetric local-swap factors.  Compress \(S\)
to the two left and right singular planes.  With the standard
vectorization convention, this gives a positive two-qubit operator
\[
 Q\succeq0.                                               \tag{10}
\]
Only three entries will be needed.  The partial-transpose index
crossing gives
\[
 \boxed{
 Q_{00,00}=p,\qquad
 Q_{11,11}=q,\qquad
 Q_{01,10}=-G_{12}.
 }                                                         \tag{11}
\]
These are exactly the diagonal rank-one slacks and the crossed
pair-sector interference.

For a positive two-qubit operator \(Q\), choose any pure-column
decomposition
\[
 Q=\sum_a|z_a\rangle\langle z_a|,\qquad
 z_a=\operatorname{vec}M_a,\quad M_a\in M_2.              \tag{12}
\]
Let
\[
 J=\epsilon\otimes\epsilon,\qquad
 \epsilon=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
 \tag{13}
\]
Then
\[
 z_a^{\mathsf T}Jz_a=2\det M_a.                          \tag{14}
\]
The established four-column Takagi mixing lemma says that the
minimum of
\[
 \sum_a|z_a^{\mathsf T}Jz_a|                             \tag{15}
\]
over all decompositions (12) is
\[
 {\cal C}(Q)=
 \max\{0,t_1-t_2-t_3-t_4\},                              \tag{16}
\]
where \(t_1\geq\cdots\geq t_4\) are the four Takagi singular
values of the polarized determinant matrix.

## 3. Concurrence-to-shifted-determinant lemma

### Lemma

If \(Q\succeq0\) obeys
\[
 {\cal C}(Q)\leq\frac49,                                  \tag{17}
\]
then its entries in (11) obey (7).

### Proof

By (15)--(17), there is a decomposition (12) satisfying
\[
 \sum_a|\det M_a|\leq\frac29.                            \tag{18}
\]
Write the entries of \(M_a\) as \(m^a_{ij}\).  Equations
(11)--(12) give
\[
\begin{aligned}
 |G_{12}|
 &=\left|\sum_a\overline{m^a_{01}}m^a_{10}\right|\\
 &\leq\sum_a|m^a_{01}m^a_{10}|\\
 &\leq\sum_a|\det M_a|
      +\sum_a|m^a_{00}m^a_{11}|\\
 &\leq\frac29+
 \sqrt{\left(\sum_a|m^a_{00}|^2\right)
       \left(\sum_a|m^a_{11}|^2\right)}\\
 &=\frac29+\sqrt{pq}.
                                                               \tag{19}
\end{aligned}
\]
The second inequality is just
\[
 m_{01}m_{10}=m_{00}m_{11}-\det M,                       \tag{20}
\]
and the last one is ordinary Cauchy--Schwarz.  This proves
(7), and then (8) proves (2). \(\square\)

The significance is that the constant \(2/9\) is exactly half of
the conjectured Takagi excess \(4/9\).  The remaining common-code
problem can therefore be stated without any singular-value ratio:
\[
 \boxed{\qquad {\cal C}(Q)\leq\frac49
 \quad\text{for every pair of qutrit three-copy planes.}\qquad}
 \tag{21}
\]
This is still unproved.  It is the invariant Hodge tensor inequality
from the earlier Takagi note, not an abstract two-qubit consequence:
arbitrary positive feature states need not satisfy (21).

## 4. The complete exact saturation boundary

There is also a direct proof of (7) on the complete sharp boundary.
Assume
\[
 G_{11}=\frac49                                             \tag{22}
\]
for the equality pair \(E_1=|u_1\rangle\langle v_1|\).  The complete
rank-one-saturation classification and its spectral-gap theorem give,
for
\[
 E=\Pi _2E_1,
\]
the identities
\[
 Ev_1=\frac49u_1,\qquad E^\dagger u_1=\frac49v_1,
 \qquad s_2(E)\leq\frac29.                              \tag{23}
\]
Because \(v_2\perp v_1\) and \(u_2\perp u_1\), the restriction of
\(E\) from \(v_1^\perp\) to \(u_1^\perp\) has operator norm at most
\(s_2(E)\).  Therefore
\[
\begin{aligned}
 |G_{12}|
 &=|\langle E,E_2\rangle_{\rm HS}|\\
 &=|\langle u_2,Ev_2\rangle|
 \leq s_2(E)
 \leq\frac29.                                             \tag{24}
\end{aligned}
\]
Here \(p=0\), so (24) is exactly (7).  Swapping the labels \(1,2\)
handles saturation of \(G_{22}\).

This boundary result is sharp.  For example,
\[
\begin{aligned}
 u_1&=|000\rangle,&u_2&=|011\rangle,\\
 v_1&=|100\rangle,&v_2&=|111\rangle
\end{aligned}                                             \tag{25}
\]
gives
\[
 G=
 \begin{pmatrix}
 4/9&-2/9\\
 -2/9&4/9
 \end{pmatrix}.                                          \tag{26}
\]
Thus both diagonal slacks vanish and (7) is an equality.

## 5. Remaining task

The exact implication chain is now
\[
 \boxed{
 {\cal C}(Q)\leq\frac49
 \Longrightarrow
 (|G_{12}|-\tfrac29)_+^2
 \leq(\tfrac49-G_{11})(\tfrac49-G_{22})
 \Longrightarrow
 \|\Pi _2C\|_2^2
 \leq\frac49(s_1^2+s_2^2+s_1s_2).
 }                                                         \tag{27}
\]
The first premise is the sole unproved step in this note.  Its proof
must use the qutrit Hodge realization of \(Q\); block positivity or
positivity of an arbitrary logical two-qubit feature state is not
enough.
