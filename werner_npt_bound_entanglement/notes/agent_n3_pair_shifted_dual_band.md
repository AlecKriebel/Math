# The strengthened pair-sector frontier has only a balanced two-mode remainder

## Status

This note does **not** prove the qutrit pair-sector theorem.  It gives
an exact dual form of the numerically sharp strengthening
\[
 \|\Pi _2C\|_2^2
 \stackrel{?}{\leq}
 \frac49\left(s_1(C)^2+s_2(C)^2+s_1(C)s_2(C)\right),
 \qquad \operatorname{rank}C\leq2,                       \tag{1}
 \]
and proves that the already established rank-one estimate settles
the entire spectrally imbalanced part of its dual.  The only remaining
case has
\[
 \frac12d_1\leq d_2\leq d_1,                             \tag{2}
 \]
where \(d_1,d_2\) are the two largest singular values of a
pair-sector operator.

The dependency-free exact checker is
`verification/verify_n3_pair_shifted_dual_band.py`.

## 1. A two-singular-value gauge

For a rank-at-most-two matrix \(C\), put
\[
 \phi(C)=\|C\|_2^2+\|\mathop{\bigwedge}\nolimits^2C\|_2
 =s_1^2+s_2^2+s_1s_2.                                   \tag{3}
\]
Let \(D\) be arbitrary, with singular values
\(d_1\geq d_2\geq0\).  Singular-value alignment gives
\[
 \sup_{\substack{\operatorname{rank}C\leq2\\C\ne0}}
 \frac{|\langle D,C\rangle|^2}{\phi(C)}
 =
 \sup_{s_1\geq s_2\geq0}
 \frac{(d_1s_1+d_2s_2)^2}
 {s_1^2+s_2^2+s_1s_2}.                                  \tag{4}
\]

### Lemma 1

The value in (4) is
\[
 \boxed{
 \begin{cases}
 d_1^2,&d_1\geq2d_2,\\[2mm]
 \displaystyle\frac43
 (d_1^2-d_1d_2+d_2^2),&d_1\leq2d_2.
 \end{cases}}                                            \tag{5}
\]

#### Proof

Write
\[
 H=\begin{pmatrix}1&1/2\\1/2&1\end{pmatrix},
 \qquad
 H^{-1}=\frac43
 \begin{pmatrix}1&-1/2\\-1/2&1\end{pmatrix}.             \tag{6}
\]
Without the constraint \(s_2\geq0\), the squared dual norm in
(4) is
\[
 (d_1,d_2)H^{-1}(d_1,d_2)^{\mathsf T}
 =\frac43(d_1^2-d_1d_2+d_2^2).                          \tag{7}
\]
The maximizing ray is
\[
 (s_1,s_2)\ \parallel\
 (d_1-\tfrac12d_2,\ d_2-\tfrac12d_1).                   \tag{8}
\]
It lies in \(s_1\geq s_2\geq0\) exactly when
\(d_1\leq2d_2\).  If \(d_1\geq2d_2\), the maximum over the
positive cone is on its boundary \(s_2=0\), where its value is
\(d_1^2\).  The two formulas agree at \(d_1=2d_2\).
\(\square\)

## 2. Exact duality

Let \({\cal K}=\operatorname{Ran}\Pi _2\).  Inequality (1) is
equivalent to
\[
 \boxed{\qquad
 \sup_{\substack{\operatorname{rank}C\leq2\\C\ne0}}
 \frac{|\langle D,C\rangle|^2}{\phi(C)}
 \leq\frac49\|D\|_2^2
 \quad\text{for every }D\in{\cal K}.
 \qquad}                                                  \tag{9}
\]
Indeed, (1) and Cauchy--Schwarz give (9), because
\[
 \langle D,C\rangle=\langle D,\Pi _2C\rangle.
\]
Conversely, apply (9) with \(D=\Pi _2C\) and cancel one
factor of \(\|\Pi _2C\|_2\).

Combining (5) and (9), the strengthened conjecture is exactly the
following two-branch singular-value theorem:
\[
 \boxed{
 \begin{aligned}
 d_1\geq2d_2&:\quad
 d_1^2\leq\frac49\|D\|_2^2,                              \tag{10}\\
 d_1\leq2d_2&:\quad
 3(d_1^2-d_1d_2+d_2^2)\leq\|D\|_2^2.                    \tag{11}
 \end{aligned}}
\]

## 3. The imbalanced branch is already proved

The established sharp rank-one pair-sector theorem
\[
 \|\Pi _2(|x\rangle\langle y|)\|_2^2
 \leq\frac49\|x\|^2\|y\|^2                              \tag{12}
\]
is, by ordinary Hilbert-space duality, exactly
\[
 \boxed{\qquad
 d_1(D)^2\leq\frac49\|D\|_2^2
 \quad(D\in{\cal K}).\qquad}                             \tag{13}
\]
Thus (10) requires no new argument.  The whole strengthened
conjecture has been reduced to (11) in the balanced band (2).

If
\[
 T=\sum_{j\geq3}d_j^2
 =\|D\|_2^2-d_1^2-d_2^2,                                \tag{14}
\]
then the sole remaining assertion is the explicit tail-mass bound
\[
 \boxed{\qquad
 T\geq2d_1^2+2d_2^2-3d_1d_2,
 \qquad \frac12d_1\leq d_2\leq d_1.
 \qquad}                                                  \tag{15}
\]
The right side is strictly positive throughout this band.  At
\(d_2=d_1/2\), (15) is already exactly the consequence of
(13); beyond that endpoint it is the genuinely new spectral-spreading
claim.

Finally, (10)--(11) imply the original pair-sector Ky--Fan target
\[
 d_1^2+d_2^2\leq\frac23\|D\|_2^2.                       \tag{16}
\]
For (10), use \(d_2^2\leq d_1^2/4\).  For (11), observe
\[
 3(d_1^2-d_1d_2+d_2^2)
 -\frac32(d_1^2+d_2^2)
 =\frac32(d_1-d_2)^2\geq0.                              \tag{17}
\]

## 4. Remaining exact lemma

It is enough to prove (15) for
\[
 D=B_{12}\otimes I_3+B_{13}\otimes I_3+B_{23}\otimes I_3,
 \qquad
 \operatorname{Tr}_iB_{ij}
 =\operatorname{Tr}_jB_{ij}=0.                          \tag{18}
\]
This is a smaller target than either the unrestricted pair-sector
Ky--Fan inequality or (1): the sharp rank-one theorem has removed
every spectrum with \(d_2<d_1/2\), and the endpoint
\(d_2=d_1/2\) is already controlled.  What remains is a quantitative
statement that the common three-pair incidence forces enough singular
mass below the two leading modes.
