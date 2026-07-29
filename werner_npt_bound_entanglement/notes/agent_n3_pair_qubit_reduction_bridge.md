# Pair-sector logical reduction and the direct qutrit-projection obstruction

## Status

This note gives an exact qubit reduction identity for the pair-sector
logical Gram.  It then rules out the most direct attempt to invoke the
rank-two qutrit projection inequality.  It does **not** disprove a more
elaborate use of that theorem after a Kraus grouping or dilation, and it
does not prove the pair-sector inequality.

## 1. The logical spin-flip identity

Use column vectorization
\[
 |\operatorname{vec}M\rangle
 =\sum_{a,b=0}^1M_{ab}|a\,b\rangle
\]
and put
\[
 \epsilon=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]
For every \(M\in M_2(\mathbb C)\),
\[
\boxed{\qquad
 \left(
 |\operatorname{vec}M\rangle
 \langle\operatorname{vec}M|
 \right)^{\Gamma_2}
 =
 MM^\dagger\otimes I_2
 -
 |\operatorname{vec}(M\epsilon)\rangle
 \langle\operatorname{vec}(M\epsilon)|.
\qquad}                                                     \tag{1}
\]

Indeed, at row \((a,d)\) and column \((c,b)\), the right side is
\[
 \sum_jM_{aj}\overline{M_{cj}}\delta_{db}
 -
 \sum_{j,k}M_{aj}\epsilon_{jd}
 \overline{M_{ck}}\epsilon_{kb}.
\]
The two-dimensional identity
\[
 \epsilon_{jd}\epsilon_{kb}
 =\delta_{jk}\delta_{db}-\delta_{jb}\delta_{dk}
\]
reduces this to \(M_{ab}\overline{M_{cd}}\), which is exactly the
corresponding entry of the partial transpose on the left.

Now let the positive feature part of a logical compression be
\[
 K_{\rm f}=\sum_Rw_R
 |\operatorname{vec}M_R\rangle
 \langle\operatorname{vec}M_R|,
 \qquad w_R\geq0,
\]
and define
\[
 A=\sum_Rw_RM_RM_R^\dagger,\qquad
 \widetilde K
 =\sum_Rw_R
 |\operatorname{vec}(M_R\epsilon)\rangle
 \langle\operatorname{vec}(M_R\epsilon)|.
\]
Summing (1) gives
\[
\boxed{\qquad
 (mI_4+K_{\rm f})^{\Gamma_2}
 =(mI_2+A)\otimes I_2-\widetilde K .
\qquad}                                                     \tag{2}
\]
For the pair witness, \(m=2/9\).  Thus its pair-only theorem is exactly
the qubit reduction inequality
\[
 \widetilde K\preceq(mI_2+A)\otimes I_2                    \tag{3}
\]
for the special common-code Kraus frame.

## 2. Why the raw Gram is not a rank-two qutrit projection

Consider the sharp code
\[
 U=(|000\rangle,|001\rangle),\qquad
 V=(|110\rangle,|111\rangle).
\]
The full logical compression of \(W^\Gamma\), in the logical product
basis \(00,01,10,11\), is
\[
 K=
 \begin{pmatrix}
 1/3&0&0&0\\
 0&2/3&-1/3&0\\
 0&-1/3&2/3&0\\
 0&0&0&1/3
 \end{pmatrix}.                                           \tag{4}
\]
It has exact spectrum
\[
 \operatorname{spec}K=\{1,1/3,1/3,1/3\}.                 \tag{5}
\]
After removing the universal floor \(mI_4=(2/9)I_4\),
\[
 \operatorname{spec}K_{\rm f}
 =\{7/9,1/9,1/9,1/9\}.                                   \tag{6}
\]
Both matrices are therefore full-rank and non-idempotent.  In
particular, neither can be changed by a unitary or an invertible
congruence into a rank-two orthogonal projection: rank is preserved by
both operations, and unitary equivalence also preserves (5)--(6).

The partial transpose of (4) is nevertheless positive:
\[
 K^{\Gamma_2}
 =
 \begin{pmatrix}
 1/3&0&0&-1/3\\
 0&2/3&0&0\\
 0&0&2/3&0\\
 -1/3&0&0&1/3
 \end{pmatrix},
\qquad
\operatorname{spec}K^{\Gamma_2}=\{0,2/3,2/3,2/3\}.        \tag{7}
\]
Thus this is also an equality case of (3).

The rank-two qutrit theorem
\[
 P\preceq\rho_A\otimes I+I\otimes\rho_B
\]
has the rank-two **projection** hypothesis essentially.  It cannot be
extended termwise to rank-one projectors: for a maximally entangled
qutrit vector, both marginals are \(I/3\), and the proposed right side
is \(2I/3\), which does not dominate the vector projector.  Hence a
spectral decomposition of the full-rank Gram in (4) does not repair the
rank obstruction.

The exact conclusion is limited but useful: Theorem 11.1 cannot be
applied by directly identifying the logical Gram, its feature part, or
an invertible congruence of either with its rank-two projection \(P\).
A successful bridge would have to construct a new qutrit rank-two
projection after a coherent grouping or dilation of the physical
Kraus channels and then show that its reduction is precisely (3).

The dependency-free checker is
`verification/verify_n3_pair_qubit_reduction_bridge.py`.
