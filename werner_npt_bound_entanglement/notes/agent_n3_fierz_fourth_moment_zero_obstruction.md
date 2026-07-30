# Exact zero obstruction to the scalar Fierz fourth-moment closure

## Result

The scalar fourth-moment estimate proposed in
`agent_n3_normal_residual_fierz_hessian.md` is not a universal
critical-point inequality.  It already fails, by a large exact
margin, at a canonical nonnormal rank-two zero.

Let
\[
\begin{aligned}
 C_0
 &=|000\rangle\langle110|+|001\rangle\langle111|\\
 &=|0\rangle\langle1|\otimes|0\rangle\langle1|
   \otimes\bigl(|0\rangle\langle0|+|1\rangle\langle1|\bigr).
\end{aligned}                                             \tag{1}
\]
Then
\[
 \operatorname{rank}C_0=2,\qquad
 \|C_0\|_2^2=2,\qquad Q_3(C_0)=0.                        \tag{2}
\]
Moreover
\[
 {\cal L}(C_0)
 =-|002\rangle\langle112|=:W_0,\qquad
 \|W_0\|_2^2=1,                                         \tag{3}
\]
so \(C_0\) is norm-critical on the smooth rank-two stratum: its
endpoint gradient is entirely in the normal block.

For the individual-label Fierz quantities \(A_T,B_T,p_T,r_T\)
defined in the earlier note, with the unnormalized singular value
matrix \(\Sigma=I_2\), exact summation gives
\[
\boxed{
 \sum_Tw_TA_T=\sum_Tw_TB_T=\frac{649}{32},\qquad
 \sum_Tw_T|p_T|=0,
}                                                        \tag{4}
\]
whereas
\[
\boxed{
 \sum_Tw_T|r_T|=2,\qquad
 \sum_T\eta_Tw_Tr_T=1=\|W_0\|_2^2.
}                                                        \tag{5}
\]
Consequently the proposed scalar left side is \(649/32\), while its
natural residual target is \(1\).  It misses by
\[
 \frac{649}{32}-1=\frac{617}{32}.                       \tag{6}
\]
For the normalized matrix \(C=C_0/\sqrt2\), the corresponding
numbers are \(649/64\), \(1/2\), and gap \(617/64\).

This does not disprove an estimate augmented by a condition peculiar
to a strictly negative minimizer.  It does prove that the displayed
scalar fourth-moment closure has no boundary-stable universal form,
even after imposing rank two and exact first-order criticality.

The dependency-free exact checker is
`verification/verify_n3_fierz_fourth_moment_zero_obstruction.py`.

## 1. Endpoint and criticality

Put
\[
 P_{01}=|0\rangle\langle0|+|1\rangle\langle1|.
\]
Since both off-diagonal factors in (1) are traceless,
\[
 L(|0\rangle\langle1|)=|0\rangle\langle1|.
\]
On the final factor,
\[
 L(P_{01})
 =P_{01}-\frac12\operatorname{Tr}(P_{01})I_3
 =P_{01}-I_3
 =-|2\rangle\langle2|.
\]
This proves (3).  The supports of \(C_0\) and \(W_0\) are disjoint,
so
\[
 Q_3(C_0)=\langle C_0,{\cal L}(C_0)\rangle=0.
\]
If
\[
 U=\operatorname{span}\{|000\rangle,|001\rangle\},\qquad
 V=\operatorname{span}\{|110\rangle,|111\rangle\},
\]
then the row and column of \(W_0\) lie in \(U^\perp\) and
\(V^\perp\), respectively.  Thus the tangent block of
\({\cal L}(C_0)\) vanishes, which is precisely norm-criticality at
\(q=0\).

## 2. Exact Fierz arithmetic

Use the real normalized qutrit basis consisting of
\[
 E_{ii},\qquad
 \frac{E_{ij}+E_{ji}}{\sqrt2},\qquad
 \frac{E_{ij}-E_{ji}}{\sqrt2}
 \quad(i<j).
\]
For a threefold tensor label \(T\), let \(k(T)\) be its number of
skew factors and use
\[
 w_T=\frac{3^{k(T)}}8,\qquad \eta_T=(-1)^{k(T)}.
\]
Grouping the 729 labels only after evaluating each individual
quantity gives the following exact audit.  A parity word records
symmetric/skew as \(0/1\).

| parity | \(\sum wA\) | \(\sum wB\) | \(\sum w|p|\) | \(\sum w|r|\) | \(\sum\eta wr\) |
|---|---:|---:|---:|---:|---:|
| 000 | \(25/32\) | \(25/32\) | \(0\) | \(1/32\) | \(-1/32\) |
| 001 | \(51/32\) | \(51/32\) | \(0\) | \(3/32\) | \(3/32\) |
| 010 | \(3/2\) | \(3/2\) | \(0\) | \(3/32\) | \(-3/32\) |
| 011 | \(99/32\) | \(99/32\) | \(0\) | \(9/32\) | \(9/32\) |
| 100 | \(3/2\) | \(3/2\) | \(0\) | \(3/32\) | \(-3/32\) |
| 101 | \(99/32\) | \(99/32\) | \(0\) | \(9/32\) | \(9/32\) |
| 110 | \(45/16\) | \(45/16\) | \(0\) | \(9/32\) | \(-9/32\) |
| 111 | \(189/32\) | \(189/32\) | \(0\) | \(27/32\) | \(27/32\) |

The checker also reconstructs the signed colligation entrywise:
\[
 W_0=\sum_T\eta_Tw_TN_T.
\]
Thus (4)--(5) do not depend on a floating-point normalization or a
collapsed parity approximation.

## 3. Where the loss occurs

There are two separate losses.

First, taking absolute values label by label already replaces
\[
 \sum_T\eta_Tw_Tr_T=1
\]
by
\[
 \sum_Tw_T|r_T|=2.
\]
Second, the labelwise Hessian estimates followed by weighted
Cauchy--Schwarz replace \(2\) by
\[
 \sqrt{\left(\sum_Tw_TA_T\right)
       \left(\sum_Tw_TB_T\right)}
 =\frac{649}{32}.
\]
The main failure is therefore not a small constant mismatch; the
diagonal label budgets have discarded the coherent cancellation
that synthesizes one rank-one normal residual.

This is visible without any Fierz frame.  Take the coherent leakage
channel
\[
\begin{aligned}
 D_X&=|002\rangle\langle110|,\\
 D_Z&=|000\rangle\langle112|,\\
 N&=|002\rangle\langle112|.
\end{aligned}
\]
Then
\[
 Q_3(D_X)=Q_3(D_Z)=1,\qquad
 \langle D_X,{\cal L}(D_Z)\rangle=0,\qquad
 |\langle W_0,N\rangle|=1.                              \tag{7}
\]
Hence the exact \(2\times2\) Hessian bound is saturated:
\[
 (0+1)^2=1\cdot1.
\]
The sharp information survives at the level of a coherent leakage
direction and is lost only when that direction is expanded into
individual Fierz labels and bounded diagonally.

## 4. Sharper remaining object

The next candidate cannot be another scalar estimate of
\(\sum_Tw_TA_T\) and \(\sum_Tw_TB_T\).  It must retain cross-label
interference.  Two equivalent formulations are natural:

1. optimize the normal bilinear pairing
   \[
   (X,Z)\longmapsto\langle W,X\Sigma Z\rangle
   \]
   directly under the full one-sided Hessian quadratic forms; or
2. regard the Fierz synthesis map
   \[
   (N_T)_T\longmapsto\sum_T\eta_Tw_TN_T
   \]
   as one operator between the two Hessian Hilbert spaces and bound
   its operator norm, retaining the off-diagonal Gram entries between
   different labels.

At \(C_0\), either formulation selects the single coherent channel in
(7) and is sharp.  Any successful global inequality must reproduce
that behavior on the zero manifold while still contradicting the
strict residual lower bound at a hypothetical negative minimizer.
