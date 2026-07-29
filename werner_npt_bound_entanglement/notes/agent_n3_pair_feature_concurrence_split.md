# Symmetric Hodge splitting of the logical feature concurrence

## Status

This note gives an exact reduction and exact obstructions, not a proof
of the remaining feature-concurrence inequality.

Let
\[
 S=\left(\frac49I-\Pi _2\right)^\Gamma\succeq0
\]
be the positive two-replica operator in the shifted pair-sector
reduction, and let \(Q\) be its compression to the two left and two
right singular planes.  There is a canonical positive splitting
\[
 Q=Q_{(2)}+Q_{(3)}
\]
such that
\[
 {\cal C}(Q)\leq{\cal C}(Q_{(2)})+{\cal C}(Q_{(3)}).
\]
Consequently the strictly smaller sufficient target
\[
 \boxed{\quad
 {\cal C}(Q_{(2)})+{\cal C}(Q_{(3)})\leq\frac49
 \quad}                                                   \tag{1}
\]
would prove the sharp shifted pair inequality.

The constant in (1) is sharp.  However, the tempting two separate
budgets
\[
 {\cal C}(Q_{(2)})\leq\frac29,\qquad
 {\cal C}(Q_{(3)})\leq\frac29                              \tag{2}
\]
are false: an exact physical code has
\[
 {\cal C}(Q_{(2)})=0,\qquad {\cal C}(Q_{(3)})=\frac8{27}.
\]
Thus a successful proof must retain compensation between the
two- and three-local-exterior pieces.

The dependency-free exact checker is
`verification/verify_n3_pair_feature_concurrence_split.py`.

## 1. The canonical positive splitting

Let \(F_i\) swap the \(i\)-th physical factor between two replicas and
put
\[
 {\mathsf A}_i=\frac{I-F_i}{2}.                            \tag{3}
\]
If \(q\) is the number of locally antisymmetric swap sectors, then
\(S\) has eigenvalue \(4/9\) at \(q=2\), eigenvalue \(20/9\) at
\(q=3\), and zero otherwise.  Therefore
\[
\boxed{
\begin{aligned}
 S&=S_{(2)}+S_{(3)},\\
 S_{(2)}&=\frac49\sum_{1\leq i<j\leq3}
                    {\mathsf A}_i{\mathsf A}_j,\\
 S_{(3)}&=\frac89{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3.
\end{aligned}}                                           \tag{4}
\]
Indeed, on \(q=2\) exactly one pair in the sum contributes.  On
\(q=3\) all three pairs contribute \(4/3\), and the last term adds
\(8/9\), giving \(20/9\).

Let \(u_0,u_1\) and \(v_0,v_1\) be orthonormal frames for the left and
right planes, and define the isometry
\[
 W(|a\rangle|c\rangle)=u_a\otimes v_c.
\]
The two positive logical feature operators are
\[
 Q_{(r)}=W^\dagger S_{(r)}W,\qquad r=2,3.                 \tag{5}
\]

For a positive two-qubit operator \(R\), use the homogeneous
concurrence
\[
 {\cal C}(R)=\inf_{R=\sum_\mu|z_\mu\rangle\langle z_\mu|}
 \sum_\mu |z_\mu^{\mathsf T}
   (\epsilon\otimes\epsilon)z_\mu|,
 \qquad
 \epsilon=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.          \tag{6}
\]
Taking the union of decompositions of two positive operators proves
directly that
\[
 {\cal C}(R_1+R_2)\leq{\cal C}(R_1)+{\cal C}(R_2).         \tag{7}
\]
Equations (4)--(7) prove the reduction to (1).

## 2. Exact sharpness of the split target

In the logical basis \(00,01,10,11\), take
\[
\begin{aligned}
 (u_0,u_1)&=(|000\rangle,|001\rangle),\\
 (v_0,v_1)&=(|110\rangle,|111\rangle).
\end{aligned}                                             \tag{8}
\]
Direct swap contraction gives
\[
 Q_{(3)}=
 \begin{pmatrix}
 0&0&0&0\\
 0&1/9&-1/9&0\\
 0&-1/9&1/9&0\\
 0&0&0&0
 \end{pmatrix},                                          \tag{9}
\]
and
\[
 Q_{(2)}=
 \begin{pmatrix}
 1/9&0&0&0\\
 0&1/3&-2/9&0\\
 0&-2/9&1/3&0\\
 0&0&0&1/9
 \end{pmatrix}.                                          \tag{10}
\]
Both matrices are invariant under the spin flip.  Their ordered
Takagi spectra are respectively
\[
 (2/9,0,0,0),\qquad (5/9,1/9,1/9,1/9).                  \tag{11}
\]
Hence
\[
 {\cal C}(Q_{(3)})=\frac29,\qquad
 {\cal C}(Q_{(2)})=\frac29.                              \tag{12}
\]
The sufficient target (1), if true, is therefore sharp.

## 3. Exact failure of the separate component budgets

Let
\[
 |\Phi\rangle=\frac{|00\rangle+|11\rangle+|22\rangle}{\sqrt3}
\]
on the first two physical sites, and take the orthonormal frames
\[
\begin{aligned}
 (u_0,u_1)&=(-|\Phi\rangle|0\rangle,-|\Phi\rangle|2\rangle),\\
 (v_0,v_1)&=( |\Phi\rangle|2\rangle,-|\Phi\rangle|0\rangle).
\end{aligned}                                             \tag{13}
\]
Exact contraction now gives
\[
 Q_{(3)}=\frac4{27}
 \begin{pmatrix}
 1&0&0&1\\
 0&0&0&0\\
 0&0&0&0\\
 1&0&0&1
 \end{pmatrix},                                          \tag{14}
\]
and
\[
 Q_{(2)}=\frac4{27}
 \begin{pmatrix}
 2&0&0&1\\
 0&1&0&0\\
 0&0&1&0\\
 1&0&0&2
 \end{pmatrix}.                                          \tag{15}
\]
Again both are spin-flip invariant.  Their ordered Takagi spectra are
\[
 (8/27,0,0,0),\qquad
 (4/9,4/27,4/27,4/27).                                   \tag{16}
\]
It follows that
\[
 \boxed{
 {\cal C}(Q_{(3)})=\frac8{27}>\frac29,\qquad
 {\cal C}(Q_{(2)})=0.
 }                                                        \tag{17}
\]
This is an exact physical obstruction to (2), not numerical evidence.
It does not violate either (1) or the original target
\({\cal C}(Q)\leq4/9\).

## 4. Two exact no-go certificates for naive triple-Hodge estimates

Let
\[
 (A_p)_{jk}=\frac1{\sqrt2}\varepsilon_{pjk},
 \qquad p,j,k\in\{0,1,2\}.                               \tag{18}
\]
The \(A_p\)'s are a Hilbert--Schmidt orthonormal basis of real
skew-symmetric qutrit matrices, and
\[
 \sum_{p=0}^2A_p\otimes A_p=\frac{3P_\Phi-F}{2}.          \tag{19}
\]

For the code (13), the natural triple-Hodge pure-column decomposition
uses the \(2\times2\) compressions
\[
 M_{pqr}=U^{\mathsf T}(A_p\otimes A_q\otimes A_r)V.
\]
An exact calculation gives
\[
 \boxed{\quad
 \sum_{p,q,r}|\det M_{pqr}|=\frac16>\frac18.
 \quad}                                                   \tag{20}
\]
Only \((p,q,r)=(0,0,1),(1,1,1),(2,2,1)\) contribute.  After
clearing the \(\sqrt2\) and \(\sqrt3\) normalizations, each compression
is \(2I_2\); the total determinant numerator is \(12\) and the common
denominator is \(72\).

Because the columns of the feature decomposition carry the factor
\(\sqrt{8/9}\), the concurrence cost produced by this unmixed
decomposition is
\[
 \frac{16}{9}\sum_{p,q,r}|\det M_{pqr}|=\frac8{27}.
\]
Thus the raw Kraus triangle estimate cannot prove a \(2/9\) budget.

There is also an exact operator-norm obstruction.  Put
\[
 D=\left(\sum_{p=0}^2A_p\otimes A_p\right)\otimes A_1.
\]
Equation (19) gives
\[
 \|D\|_{\rm op}^2=\frac12,\qquad
 \|D\|_2^2=3,\qquad
 \boxed{\frac{\|D\|_{\rm op}^2}{\|D\|_2^2}=\frac16>\frac18.}
                                                               \tag{21}
\]
Hence the stronger triple-skew estimate
\(\|D\|_{\rm op}^2\leq\|D\|_2^2/8\) is false.

## 5. What remains

The surviving exact implication is
\[
\boxed{
 {\cal C}(Q_{(2)})+{\cal C}(Q_{(3)})\leq\frac49
 \ \Longrightarrow\
 {\cal C}(Q)\leq\frac49
 \ \Longrightarrow\
 \|\Pi _2C\|_2^2
 \leq\frac49(s_1^2+s_2^2+s_1s_2).
}                                                         \tag{22}
\]
The first inequality is unproved.  The countercode (13) shows why its
two terms cannot be assigned independent \(2/9\) budgets.

Discovery-only optimization has approached \(4/9\) from below near
the sharp code (8) and has not produced a violation of (1) or of the
original \({\cal C}(Q)\leq4/9\) target.  This absence of a numerical
violation is not used as mathematical evidence.  The exact results of
this note are only the decomposition, the sharp code, and the
obstructions (13)--(21).
