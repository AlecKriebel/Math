# Exact obstruction to separate quaternion-multiplier bounds

## Status

This note does **not** disprove the coupled four-channel inequality
\[
E_\epsilon\le E_I+E_X+E_Z.
\]
It rules out a natural way of proving it: reconstructing the
\(\epsilon\)-channel from each positive channel separately, estimating the
three reconstruction maps only by their sharp operator norms, and combining
those three scalar norm estimates.

The obstruction already occurs on three qubits, where the coupled inequality
is known to be true.  Thus the missing contraction has to retain coherent
information shared by the three positive quaternion channels.

The dependency-free exact checker is
`verification/verify_n3_quaternion_multiplier_obstruction.py`.

## 1. Three exact multiplier reconstructions

Use the notation of `agent_n3_four_channel_ppt_schur.md`.  Thus
\[
 U:\mathbb C^2\longrightarrow {\cal H}
\]
is an isometry,
\[
 \tau_0=I,\qquad \tau_1=X,\qquad \tau_2=Z,\qquad
 \tau_3=\epsilon=
 \begin{pmatrix}0&1\\-1&0\end{pmatrix},
\]
and
\[
 J_\tau=U\tau U^\dagger .
\]
For an arbitrary test matrix \(V:\mathbb C^2\to{\cal H}\), put
\[
 X_V=VU^{\mathsf T}.
\]
Then \(X_V=X_V\overline U\,U^{\mathsf T}\), and the four Fierz energies
can be written
\[
 E_\tau(V)=\|X_VJ_\tau^{\mathsf T}\|_{\cal W}^2,          \tag{1}
\]
where
\[
 \|Y\|_{\cal W}^2
 =
 \frac18\left\langle
 Y,\prod_{i=1}^3(2I-\mathsf T_i)Y
 \right\rangle_{\rm HS}.                                 \tag{2}
\]

The logical multiplication table gives the three exact identities
\[
\begin{aligned}
 X_VJ_\epsilon^{\mathsf T}
 &=(X_VJ_I^{\mathsf T})J_\epsilon^{\mathsf T},\\
 X_VJ_\epsilon^{\mathsf T}
 &=(X_VJ_X^{\mathsf T})J_Z^{\mathsf T},\\
 X_VJ_\epsilon^{\mathsf T}
 &=-(X_VJ_Z^{\mathsf T})J_X^{\mathsf T}.                 \tag{3}
\end{aligned}
\]
For \(\lambda\in\{\epsilon,Z,X\}\), let
\[
 k_\lambda(U)
 =
 \sup_{\substack{0\ne Y=Y\overline U U^{\mathsf T}}}
 \frac{\|YJ_\lambda^{\mathsf T}\|_{\cal W}^2}
      {\|Y\|_{\cal W}^2}.                                \tag{4}
\]
Equations (1)--(3) imply the three valid separate estimates
\[
 E_\epsilon\le k_\epsilon E_I,\qquad
 E_\epsilon\le k_ZE_X,\qquad
 E_\epsilon\le k_XE_Z.                                  \tag{5}
\]

Suppose one combines (5) with nonnegative scalar weights.  Such a
combination can prove
\[
 E_\epsilon\le E_I+E_X+E_Z
\]
only if
\[
 \frac1{k_\epsilon}+\frac1{k_Z}+\frac1{k_X}\ge1.         \tag{6}
\]
Indeed, weights \(w_\mu\ge0\), \(\sum_\mu w_\mu=1\), would have to
satisfy \(w_\mu k_\mu\le1\) for all three channels.  Such weights exist
exactly when (6) holds.

## 2. A rational three-qubit obstruction

Take
\[
\begin{aligned}
 u_0&=|000\rangle,\\
 u_1&=\frac35|001\rangle+\frac45|010\rangle,
 \qquad U=(u_0,u_1).
\end{aligned}                                             \tag{7}
\]
The columns are orthonormal.  We identify an \(8\)-by-\(2\) test matrix
\(V\) with its column-interleaved vector
\[
 (V_{0,0},V_{0,1},V_{1,0},V_{1,1},\ldots,V_{7,0},V_{7,1}).
\]
Consider the following three integer test vectors:
\[
\begin{aligned}
v_I&=-4e_1-5e_2-4e_4-5e_7,\\
v_X&= 4e_2+4e_4+5e_7,\\
v_Z&=-4e_1+5e_2+4e_4+5e_7.                              \tag{8}
\end{aligned}
\]
Direct rational contraction of (1)--(2) gives
\[
\begin{array}{c|ccc}
 &E_\epsilon&E_\mu&E_\epsilon/E_\mu\\ \hline
\mu=I&9237/200&143/10&9237/2860\\
\mu=X&1921/50&521/50&1921/521\\
\mu=Z&9237/200&143/10&9237/2860 .
\end{array}                                               \tag{9}
\]
In particular,
\[
\begin{aligned}
E_\epsilon(v_I)-3E_I(v_I)&=\frac{657}{200}>0,\\
E_\epsilon(v_X)-3E_X(v_X)&=\frac{179}{25}>0,\\
E_\epsilon(v_Z)-3E_Z(v_Z)&=\frac{657}{200}>0.             \tag{10}
\end{aligned}
\]
Therefore
\[
 k_\epsilon>3,\qquad k_Z>3,\qquad k_X>3,
\]
and hence
\[
 \frac1{k_\epsilon}+\frac1{k_Z}+\frac1{k_X}<1.           \tag{11}
\]
Condition (6) fails strictly.

The sharp constants for this anchor are algebraic and can also be read
off exactly.  If \(H_\tau\) is the Gram matrix of \(E_\tau\), direct
block elimination gives, up to positive scalar factors,
\[
\begin{aligned}
\det(H_\epsilon-\lambda H_I)
&=\det(H_\epsilon-\lambda H_Z)\\
&\doteq
(\lambda-1)^8
\cdot(1875\lambda^2-6826\lambda+2451)^2
\cdot(2451\lambda^2-6826\lambda+1875)^2,\\
\det(H_\epsilon-\lambda H_X)
&\doteq
(\lambda-3)^2(\lambda-1)^8(3\lambda-1)^2
\cdot(2451\lambda^2-9706\lambda+2451)^2.                 \tag{12}
\end{aligned}
\]
Every \(H_\tau\) is positive definite: the filter in (2) is positive
definite, and \(V\tau^{\mathsf T}U^{\mathsf T}=0\) implies \(V=0\)
because \(U^{\mathsf T}\overline U=I_2\).  Hence the largest generalized
root in each pencil is the sharp multiplier constant.
Consequently
\[
\begin{aligned}
k_\epsilon=k_X
&=\frac{3413+4\sqrt{440809}}{1875},\\
k_Z
&=\frac{4853+4\sqrt{1096513}}{2451}.                    \tag{13}
\end{aligned}
\]
All three are strictly larger than \(3\), consistently with the shorter
rational certificates (9)--(10).

This is not a counterexample to three-copy positivity.  All three local
spaces in (7) are qubits, so the exact common-local-qubit identity gives
\[
 Q_3(C)=
 \left\|\mathcal P_{0,1}\otimes\mathcal P_{0,2}
 \otimes\mathcal P_{0,3}(C)\right\|_2^2\ge0.              \tag{14}
\]
For the anchor (7), the coupled four-channel Gram
\[
 \Gamma_I+\Gamma_X+\Gamma_Z-\Gamma_\epsilon
\]
has rank \(14\) and the following exact two-dimensional kernel:
\[
\begin{aligned}
 &\frac45e_2+\frac35e_4+e_7,\\
 &\frac45e_{10}+\frac35e_{12}+e_{15}.                    \tag{15}
\end{aligned}
\]
Thus the final inequality is saturated in coherent directions even
though every separate quaternion multiplier has squared norm strictly
larger than \(3\).

## 3. Consequence

The state-dependent identities (3) remain useful, but their three sharp
scalar operator norms discard precisely the common-input geometry needed
for the theorem.  A viable quaternion/Koszul certificate must therefore
do at least one of the following:

1. mix the three positive channel vectors before taking norms;
2. use an operator-valued partition of the input space rather than three
   anchor-dependent scalars; or
3. factor the full coupled Gram difference directly.

This is the Fierz-channel analogue of the previously recorded failure of
scalar cube-routing mixtures, but it is logically independent of that
obstruction.
