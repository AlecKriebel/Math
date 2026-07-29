# The pair-sector feature state: Takagi mixing and qutrit Hodge polarization

## Status

This note does **not** prove the qutrit pair-sector theorem.  It gives
an exact coherent-Kraus reduction which is strictly stronger than
summing determinant magnitudes channel by channel.

For the positive feature state \(K_{\rm f}\) defined below, put
\[
 {\cal C}(K_{\rm f})
 =
 \max\{0,s_1-s_2-s_3-s_4\},
 \tag{1}
\]
where \(s_1\geq\cdots\geq s_4\geq0\) are the four nonzero Takagi
singular values of its polarized determinant matrix.  The remaining
target is
\[
 \boxed{\qquad {\cal C}(K_{\rm f})\leq\frac49. \qquad}
 \tag{2}
\]
Inequality (2) implies the shifted pair-sector determinant.  It is
sharp on the known product equality code.

The independent checker is
`verification/verify_n3_pair_sector_takagi_hodge.py`.

## 1. The positive feature state

On two replicas of the three-qutrit physical space, let
\({\mathsf A}_i=(I-F_i)/2\) and
\({\mathsf S}_i=(I+F_i)/2\).  The positive feature part of the
partially transposed witness is
\[
 S
 =\frac49E_2+\frac{20}{9}E_3,
 \tag{3}
\]
where
\[
\begin{aligned}
 E_2&={\mathsf A}_1{\mathsf A}_2{\mathsf S}_3
     +{\mathsf A}_1{\mathsf S}_2{\mathsf A}_3
     +{\mathsf S}_1{\mathsf A}_2{\mathsf A}_3,\\
 E_3&={\mathsf A}_1{\mathsf A}_2{\mathsf A}_3.
\end{aligned}
\tag{4}
\]
Equivalently,
\[
 \boxed{\qquad
 S=\frac49\sum_{i<j}{\mathsf A}_i{\mathsf A}_j
   +\frac89{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3.
 \qquad}
 \tag{5}
\]
Thus the antisymmetric component of each of the three double-Hodge
channels is the same triple-Hodge channel.  Formula (5) exposes the
coherence which is lost by four independent determinant estimates.

Choose real Hilbert--Schmidt orthonormal symmetric and skew-symmetric
matrix bases at every qutrit.  Their vectorizations resolve
\({\mathsf S}_i\) and \({\mathsf A}_i\), respectively.  Let \(R\)
run through the resulting tensor Kraus basis of \(E_2\oplus E_3\), and
put
\[
 w_R=
 \begin{cases}
 4/9,&R\text{ has exactly two skew factors},\\
 20/9,&R\text{ has three skew factors}.
 \end{cases}
 \tag{6}
\]

For isometries \(U=(u_1,u_2)\) and \(V=(v_1,v_2)\), define
\[
 M_R=U^{\mathsf T}RV\in M_2,\qquad
 z_R=\sqrt{w_R}\operatorname{vec}M_R.
 \tag{7}
\]
The logical compression of \(S\) is the positive two-qubit operator
\[
 \boxed{\qquad
 K_{\rm f}=\sum_R|z_R\rangle\langle z_R|.
 \qquad}
 \tag{8}
\]
The full compressed witness is
\[
 K=\frac29I_4+K_{\rm f}.
 \tag{9}
\]

## 2. Polarized determinants and coherent mixing

Set
\[
 \epsilon=\begin{pmatrix}0&1\\-1&0\end{pmatrix},
 \qquad J=\epsilon\otimes\epsilon.
 \tag{10}
\]
For column vectorization,
\[
 \operatorname{vec}(M)^{\mathsf T}J\operatorname{vec}(N)
 =2\,\operatorname{pdet}(M,N),
 \tag{11}
\]
where
\[
\begin{aligned}
2\,\operatorname{pdet}(M,N)
={}&M_{11}N_{22}+N_{11}M_{22}\\
&-M_{12}N_{21}-N_{12}M_{21}.
\end{aligned}
\tag{12}
\]
In particular, the value at \(M=N\) is \(2\det M\).

Define the complex symmetric matrix on the Kraus labels
\[
 \boxed{\qquad
 \tau_{RS}=z_R^{\mathsf T}Jz_S
 =2\sqrt{w_Rw_S}\operatorname{pdet}(M_R,M_S).
 \qquad}
 \tag{13}
\]
Although the physical Kraus space has dimension \(189\), the nonzero
rank of \(\tau\) is at most four.  Replacing the Kraus columns by a
unitary mixture sends
\[
 \tau\longmapsto T^{\mathsf T}\tau T.
 \tag{14}
\]

### Lemma 2.1 (exact four-column mixing)

Let \(s_1\geq\cdots\geq s_4\) be the nonzero singular values of
\(\tau\), padded by zeros.  Among all Kraus decompositions of
\(K_{\rm f}\),
\[
 \boxed{\qquad
 \inf\sum_a\left|z_a^{\mathsf T}Jz_a\right|
 =\max\{0,s_1-s_2-s_3-s_4\}.
 \qquad}
 \tag{15}
\]

#### Proof

A unitary congruence first puts \(\tau\) into the diagonal form
\(\operatorname{diag}(s_1,\ldots,s_4)\).  For any subsequent unitary
\(T\), its \(a\)-th diagonal entry is
\[
 q_a=\sum_is_iT_{ia}^2.
 \]
The triangle inequality gives
\[
\sum_a|q_a|
\geq
\sum_a\left(s_1|T_{1a}|^2-\sum_{i>1}s_i|T_{ia}|^2\right)
=s_1-\sum_{i>1}s_i.
\]
The left side is nonnegative, proving the lower bound in (15).

For the reverse bound, let \(H\) be the real \(4\times4\) Hadamard
matrix divided by \(2\).  Choose phases \(\theta_i\) so that
\[
\left|\sum_is_ie^{i\theta_i}\right|
=\max\{0,s_1-s_2-s_3-s_4\};
\]
this is the elementary polygon inequality for four segments.  With
\[
 T=\operatorname{diag}(e^{i\theta_i/2})H,
 \]
all four diagonal entries have the same absolute value,
\[
 |q_a|=\frac14\left|\sum_is_ie^{i\theta_i}\right|.
 \]
Their sum attains the lower bound. \(\square\)

For a pure two-qubit column \(z=\operatorname{vec}M\), direct
diagonalization of the partial transpose gives
\[
 (|z\rangle\langle z|)^\Gamma\succeq-|\det M|I_4
 =-\frac12|z^{\mathsf T}Jz|I_4.
 \tag{16}
\]
Consequently, any decomposition satisfying
\[
 \sum_a|z_a^{\mathsf T}Jz_a|\leq\frac49
 \tag{17}
\]
gives
\[
 K_{\rm f}^{\Gamma}\succeq-\frac29I_4,
 \]
and hence \(K^\Gamma\succeq0\).  Lemma 2.1 proves that (2) is exactly
the coherent determinant bound needed for this argument.

## 3. Intrinsic bivector formula

Put
\[
 u_\wedge
 =\frac{u_1\otimes u_2-u_2\otimes u_1}{\sqrt2},
 \qquad
 v_\wedge
 =\frac{v_1\otimes v_2-v_2\otimes v_1}{\sqrt2}.
 \tag{18}
\]
Expanding the four terms gives
\[
 \operatorname{pdet}(M_R,M_S)
 =
 \frac12
 \left\langle\overline{u_\wedge},
 (R\otimes S+S\otimes R)v_\wedge
 \right\rangle .
 \tag{19}
\]
Therefore
\[
 \boxed{\qquad
 \tau_{RS}
 =
 \sqrt{w_Rw_S}
 \left\langle\overline{u_\wedge},
 (R\otimes S+S\otimes R)v_\wedge
 \right\rangle .
 \qquad}
 \tag{20}
\]
This retains both common singular planes in one polarized tensor.

For a qutrit, choose the normalized skew basis
\[
 (A_k)_{ab}=\frac1{\sqrt2}\epsilon_{kab},
 \qquad k=0,1,2.
 \tag{21}
\]
Equation (21) is the local Hodge isometry
\(\bigwedge^2\mathbb C^3\simeq\overline{\mathbb C^3}\).
Substituting the tensors
\[
 A_p\otimes A_q\otimes S_\mu
 \quad\text{and}\quad
 A_p\otimes A_q\otimes A_r
 \tag{22}
\]
and their site permutations into (20) gives the promised explicit
Hodge polarization: the \(162\) exact-two-skew channels and the \(27\)
triple-skew channels are entries of one common symmetric matrix
\(\tau\), not four independent determinant lists.

The unresolved statement is now:

> For every pair of qutrit three-copy isometries \(U,V\), the Hodge
> tensor (20)--(22) has
> \(2\|\tau\|_\infty-\|\tau\|_1\leq4/9\).

This is an invariant common-origin inequality.  It is immune to the
known factor-two failure of summing \(|\det M_R|\) in the original
Kraus basis because (15) optimizes all coherent channel mixtures
before taking absolute values.

## 4. Exact sharp boundary

For
\[
 U=(|000\rangle,|001\rangle),\qquad
 V=(|110\rangle,|111\rangle),
 \tag{23}
\]
one obtains
\[
 K_{\rm f}=
 \begin{pmatrix}
 1/9&0&0&0\\
 0&4/9&-1/3&0\\
 0&-1/3&4/9&0\\
 0&0&0&1/9
 \end{pmatrix}.
 \tag{24}
\]
Its four Takagi singular values are
\[
 \frac79,\qquad\frac19,\qquad\frac19,\qquad\frac19.
 \tag{25}
\]
Thus
\[
 {\cal C}(K_{\rm f})=\frac79-\frac39=\frac49.
 \tag{26}
\]
The Hadamard construction in Lemma 2.1 gives an explicit optimal
four-column mixing: take the dominant Takagi phase \(+1\), the other
three phases \(-1\), and mix with the normalized real Hadamard matrix.
All four resulting determinant amplitudes have magnitude \(1/9\).
