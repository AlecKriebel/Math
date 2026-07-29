# The normalized one-plane marginal frontier for the qutrit pair sector

## Status

This note gives three exact, lossless forms of the unresolved
pair-sector theorem
\[
 \|\Pi _2C\|_2^2\leq \frac23\|C\|_2^2
 \qquad(\operatorname{rank}C\leq2).                       \tag{1}
\]
They are:

1. one scalar inequality among joint physical/logical swap sectors;
2. one four-party marginal operator inequality;
3. two-positivity of one explicit trace-replacement map.

The note also gives a sparse exact counterexample to the tempting
stronger inequality obtained by deleting two positive compensators.
That stronger inequality fails by exactly \(1/8\), while the complete
target is an equality on the same example.

The complete inequality (1) is **not proved or disproved here**.  The
dependency-free exact checker is
`verification/verify_n3_pair_one_plane_marginal_frontier.py`.

## 1. Normalization

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad K=\mathbb C^2,
\]
and let
\[
 V:K\longrightarrow{\cal H},\qquad V^\dagger V=I_K.
\]
Write \(v_a=V|a\rangle\) and normalize the code purification as
\[
 |\Psi\rangle
 =\frac1{\sqrt2}\sum_{a=0}^1v_a\otimes|a\rangle_K,
 \qquad
 R=|\Psi\rangle\langle\Psi|.
                                                               \tag{2}
\]
Then
\[
 \|\Psi\|=1,\qquad \rho_K^\Psi=I_K/2.                    \tag{3}
\]

For a physical site \(i\), let
\[
 e_i(X)=I_i\otimes\operatorname{Tr}_iX,\qquad
 {\cal R}_i=e_i-\frac13\,\operatorname{id}.              \tag{4}
\]
All unshown factors, including \(K\), are left unchanged.  The
normalized one-plane frame operator is
\[
 {\cal S}(R)=\sum_{1\leq i<j\leq3}{\cal R}_i{\cal R}_j(R).
                                                               \tag{5}
\]
The unnormalized convention
\(\boldsymbol V=\sum_av_a|a\rangle\) used in the earlier one-plane
note has frame operator \(2{\cal S}(R)\).  Consequently (1) is
equivalent to
\[
 \boxed{\qquad {\cal S}(R)\preceq I_{{\cal H}\otimes K}
 \quad\text{for every normalized code purification (2).}\qquad}
                                                               \tag{6}
\]

## 2. Exact joint-swap sector inequality

Let \(x\in{\cal H}\otimes K\) be a unit vector and put
\[
 z=\Psi\otimes x.
\]
On the two replicas let \(F_1,F_2,F_3\) swap corresponding physical
qutrits and let \(F_K\) swap the auxiliary qubits.  Let \(E_r\) be
the joint physical-swap projector with exactly \(r\) antisymmetric
signs, and put
\[
 S_K=\frac{I+F_K}{2},\qquad A_K=\frac{I-F_K}{2}.
\]
Define the nonnegative sector masses
\[
 s_r=\|S_KE_rz\|^2,\qquad
 a_r=\|A_KE_rz\|^2,\qquad d_r=s_r-a_r.                  \tag{7}
\]

The swap trick and (3) give
\[
 \sum_r d_r
 =\langle z,F_Kz\rangle
 =\operatorname{Tr}(\rho_K^\Psi\rho_K^x)=\frac12.
                                                               \tag{8}
\]
Since \(\sum_r(s_r+a_r)=1\), this is equivalently
\[
 \boxed{\qquad \sum_ra_r=\frac14,\qquad
                    \sum_rs_r=\frac34.\qquad}            \tag{9}
\]

The physical swap polynomial associated with the one-plane defect
has eigenvalues
\[
 h_r=2,\ 2,\ 6,\ 22\qquad(r=0,1,2,3).                   \tag{10}
\]
Direct expansion of (4)--(5), or the swap trick term by term, gives
\[
 3\left(1-\langle x,{\cal S}(R)x\rangle\right)
 =\sum_{r=0}^3h_rd_r
 =1+4d_2+20d_3.                                        \tag{11}
\]
Therefore the complete one-plane theorem is exactly
\[
 \boxed{\qquad d_2+5d_3\geq-\frac14.\qquad}              \tag{12}
\]
Using (9), the same assertion becomes the positive-sector comparison
\[
 \boxed{\qquad
 a_0+a_1+s_2+5s_3\geq4a_3.
 \qquad}                                                 \tag{13}
\]
No estimate is used in passing among (6), (12), and (13).

## 3. Exact marginal operator

For \(T\subseteq\{1,2,3\}\), write \(\rho_{KT}^\Psi\) for the
reduction of \(R\) to \(K\) and the physical sites in \(T\), embedded
back into the full space by tensoring the identity on the missing
physical sites.  Expanding (5) gives
\[
\begin{aligned}
 {\cal S}(R)
 ={}&
 \sum_{i=1}^3 \rho_{Ki}^\Psi
 -\frac23\sum_{1\leq i<j\leq3}\rho_{Kij}^\Psi
 {}+\frac13R.                                            \tag{14}
\end{aligned}
\]
Here the first sum arises from \(e_je_k(R)\), and the second from
\(e_k(R)\).

Define the full sector-defect operator \(O_\Psi\) by
\[
 \langle x,O_\Psi x\rangle
 =a_0+a_1+s_2+5s_3-4a_3.                                \tag{15}
\]
Equations (11)--(14) give the exact identity
\[
\boxed{
 4O_\Psi
 =
 3I
{}+2\sum_{i<j}\rho_{Kij}^\Psi
{}-3\sum_i\rho_{Ki}^\Psi
{}-R.
}                                                       \tag{16}
\]
Thus the pair-sector theorem is precisely the four-party marginal
operator inequality
\[
\boxed{
 3I
{}+2\sum_{i<j}\rho_{Kij}^\Psi
\succeq
3\sum_i\rho_{Ki}^\Psi+|\Psi\rangle\langle\Psi|,
\qquad \rho_K^\Psi=I_2/2.
}                                                       \tag{17}
\]

This form contains no alternating scalar sum.  Its sole nonlinear
input is that all six marginals come from one pure state with a
maximally mixed auxiliary qubit.

There is also an exact rank-one Schur-complement target.  Put
\[
 {\cal A}_\Psi
 =3I+2\sum_{i<j}\rho_{Kij}^\Psi
       -3\sum_i\rho_{Ki}^\Psi.                           \tag{18}
\]
Then (17) is \({\cal A}_\Psi-R\succeq0\).  If
\({\cal A}_\Psi\succ0\), this is equivalent to the single scalar
condition
\[
 \boxed{\qquad
 \langle\Psi,{\cal A}_\Psi^{-1}\Psi\rangle\leq1.
 \qquad}                                                 \tag{19}
\]
Without strict positivity, the exact replacement is
\[
 {\cal A}_\Psi\succeq0,\qquad
 \Psi\in\operatorname{Ran}{\cal A}_\Psi,\qquad
 \langle\Psi,{\cal A}_\Psi^+\Psi\rangle\leq1,            \tag{20}
\]
where \(+\) denotes the Moore--Penrose inverse.

## 4. Equivalent two-positive map

Let the \(e_i\)'s now act on \(M_{27}\), without an auxiliary
factor, and define
\[
\boxed{
 \Theta
 =
 2e_1e_2e_3
 -\sum_{i<j}e_ie_j
 +\frac23\sum_ie_i
 -\frac13\,\operatorname{id}.
}                                                       \tag{21}
\]
For the normalized \(R\) in (2), equation (3) gives
\[
 2e_1e_2e_3(R)=I_{{\cal H}}\otimes I_K.
\]
Hence
\[
 \Theta\otimes\operatorname{id}_K(R)
 =I-{\cal S}(R)=\frac43O_\Psi.                           \tag{22}
\]

Every Schmidt-rank-two vector can be written as an invertible
logical filter applied to a normalized code purification; singular
rank-one cases follow by a limit.  Because \(\Theta\) acts only on
the physical system, the logical filter becomes a congruence on the
output.  It follows that
\[
\boxed{
 \text{the pair-sector theorem}
 \quad\Longleftrightarrow\quad
 \Theta\text{ is two-positive}.
}                                                       \tag{23}
\]
This is an exact reformulation, not an independent proof.

## 5. Exact failure of the uncompensated Hodge core

Deleting the two nonnegative terms \(a_0+5s_3\) from (13) gives the
attractive but false proposal
\[
 s_2+a_1\stackrel?{\geq}4a_3.                            \tag{24}
\]
It fails already inside a common local qubit support.

Use binary computational strings inside the qutrit triple and put
\[
\begin{aligned}
 v_0&=\frac{|000\rangle+|111\rangle}{\sqrt2},&
 v_1&=\frac{|001\rangle+|110\rangle}{\sqrt2},\\
 x_0&=\frac{-|001\rangle+|110\rangle}{2},&
 x_1&=\frac{-|000\rangle+|111\rangle}{2}.
\end{aligned}                                           \tag{25}
\]
Then \(v_0,v_1\) are orthonormal and
\[
 \Psi=\frac{v_0|0\rangle+v_1|1\rangle}{\sqrt2},
 \qquad
 x=x_0|0\rangle+x_1|1\rangle
                                                               \tag{26}
\]
are both unit vectors.  Exact swap projection gives
\[
\begin{array}{c|cccc}
r&0&1&2&3\\ \hline
s_r&5/16&3/8&1/16&0\\
a_r&1/8&1/16&0&1/16 .
\end{array}                                             \tag{27}
\]
Consequently
\[
 s_2+a_1-4a_3
 =\frac1{16}+\frac1{16}-\frac4{16}
 =-\frac18,                                             \tag{28}
\]
whereas the two deleted compensators repair the gap exactly:
\[
 a_0+5s_3=\frac18,\qquad
 a_0+a_1+s_2+5s_3-4a_3=0.                               \tag{29}
\]
Thus (24) cannot be used as a lemma in a proof of (13).  The
\(a_0\) channel is indispensable even on the binary-support
boundary.

## 6. Remaining exact problem

The unresolved pair-sector frontier is now any one of the equivalent
statements (6), (12), (13), (17), or (23).  The marginal form (17)
and Schur form (19)--(20) are the smallest operator targets in this
note.  The counterexample (25)--(29) shows that the negative
fully-antisymmetric logical/physical channel cannot be controlled by
the one-antisymmetric and physical-weight-two channels alone.

A successful proof must use all four compensating terms in (13), or
equivalently prove the common-pure-state marginal domination (17).
