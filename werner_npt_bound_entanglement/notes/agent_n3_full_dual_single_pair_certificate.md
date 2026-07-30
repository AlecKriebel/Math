# The full three-copy dual: an exact single-pair residual certificate

## Status

This note proves the full inverse-marginal residual inequality when
only one of its three pair coefficients is nonzero.  This is the
diagonal-block theorem needed for a subsequent three-component Gram
analysis.

For every isometry
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}
\]
and every doubly-traceless \(B_{12}\in M_3\otimes M_3\),
\[
\boxed{
 \left\langle
 (B_{12}\otimes I_3)V,\,
 S_V^{-1}(B_{12}\otimes I_3)V
 \right\rangle
 \leq2\|B_{12}\|_2^2 ,
}                                                        \tag{1}
\]
where
\[
 S_V
 =I-\frac1{12}\sum_{i=1}^3e_i(R_V)+\frac1{24}R_V
 \tag{2}
\]
is the exact low-sector Schur operator from
`notes/agent_n3_full_dual_low_sector_elimination.md`.
The same statement holds for either of the other pair positions.

The proof is an operator certificate.  It uses:

1. an explicit finite product-projector decomposition, proved below;
2. an elementary two-dimensional-ancilla positivity lemma; and
3. one manifestly completely positive remainder.

No classification theorem or external result is used.

The dependency-free exact checker is
`verification/verify_n3_full_dual_single_pair_certificate.py`.

## 1. Pair and low-sector frame operators

Write
\[
 |\boldsymbol V\rangle
 =\sum_{r=0}^1v_r\otimes|r\rangle_K,\qquad
 P=\frac12|\boldsymbol V\rangle\langle\boldsymbol V|.
 \tag{3}
\]
Then \(P\) has trace one and the isometry condition gives
\[
 \operatorname{Tr}_{123}P=\frac12I_K.
 \tag{4}
\]
For a physical site \(i\), let
\[
 e_i(X)=I_i\otimes\operatorname{Tr}_iX,\qquad
 q_i=e_i-\frac13\operatorname{id}.                       \tag{5}
\]
All these maps act trivially on \(K\).

Since \(R_V=2P\), (2) becomes
\[
 S_V=I-\frac16\sum_i e_i(P)+\frac1{12}P.                \tag{6}
\]
The coefficient \(B_{12}\) has domain weight \(2\) in the full
dual.  Completeness of an orthonormal traceless matrix basis on sites
\(1,2\) therefore gives its output frame
\[
\begin{aligned}
 F_{12}
 &=\frac12q_1q_2(R_V)\\
 &=q_1q_2(P)\\
 &=e_1e_2(P)-\frac13(e_1+e_2)(P)+\frac19P.
\end{aligned}                                             \tag{7}
\]
Consequently (1) for every \(B_{12}\) is equivalent, by the elementary
frame/Schur-complement criterion, to
\[
 \boxed{\qquad F_{12}\preceq S_V.\qquad}                 \tag{8}
\]
Explicitly, if
\[
 {\cal M}_{12}(B)=(B\otimes I_3)V,
\]
then \(F_{12}={\cal M}_{12}(2I)^{-1}{\cal M}_{12}^\dagger\).
Thus
\[
\|S_V^{-1/2}{\cal M}_{12}(B)\|_2^2\leq2\|B\|_2^2
\]
for every \(B\) if and only if
\(S_V^{-1/2}F_{12}S_V^{-1/2}\preceq I\), which is (8).

## 2. The exact residual factorization

Equation (4) implies
\[
 2e_1e_2e_3(P)=I                                      \tag{9}
\]
on the full physical-output--logical space.  Subtracting (7) from
(6), and then using (9), gives
\[
\begin{aligned}
 S_V-F_{12}
 =\bigg[
 2e_1e_2e_3-e_1e_2
 +\frac16(e_1+e_2-e_3)-\frac1{36}\operatorname{id}
 \bigg](P).
\end{aligned}                                            \tag{10}
\]
Define maps on sites \(1,2\):
\[
\begin{aligned}
 {\cal A}
 &=2e_1e_2-\frac16\operatorname{id},\\
 {\cal B}
 &=\left(e_1-\frac16\operatorname{id}\right)
   \left(e_2-\frac16\operatorname{id}\right),
\end{aligned}                                             \tag{11}
\]
and on site \(3\):
\[
 \Phi_3=e_3-\frac12\operatorname{id}.                    \tag{12}
\]
Direct expansion of (10) gives the exact residual Gram
\[
\boxed{
 S_V-F_{12}
 ={\cal A}\Phi_3(P)
  +\left(\frac12{\cal A}-{\cal B}\right)(P).
}                                                        \tag{13}
\]
Both summands in (13) are positive.  The rest of the proof establishes
this assertion from first principles.

## 3. A finite product decomposition

We first prove the only separability fact needed in the argument.
Let
\[
 |\Phi_n\rangle=\sum_{a=0}^{n-1}|a\,a\rangle,\qquad
 P_{\Phi_n}=\frac1n|\Phi_n\rangle\langle\Phi_n|.
 \tag{14}
\]

### Lemma 3.1

For every \(n\geq2\), \(I-P_{\Phi_n}\) is a finite positive sum of
product-vector projectors.

### Proof

Let \(\Theta=\{1,i,-1,-i\}\).  For \(0\leq a<b<n\) and
\(\theta\in\Theta\), put
\[
 |p_{ab,\theta}\rangle
 =\frac12
 (|a\rangle+\theta|b\rangle)
 \otimes
 (|a\rangle-\overline\theta|b\rangle).                  \tag{15}
\]
Every \(p_{ab,\theta}\) is a product vector.  Averaging the four
phases cancels all nonconstant powers of \(\theta\) and gives
\[
\begin{aligned}
 \frac14\sum_{\theta\in\Theta}
 |p_{ab,\theta}\rangle\langle p_{ab,\theta}|
 ={}&\frac14
 (|aa\rangle-|bb\rangle)
 (\langle aa|-\langle bb|)\\
 &+\frac14|ab\rangle\langle ab|
  +\frac14|ba\rangle\langle ba|.
\end{aligned}                                             \tag{16}
\]
Summing (16) over \(a<b\), and using the complete-graph identity
\[
 \sum_{a<b}
 (|aa\rangle-|bb\rangle)
 (\langle aa|-\langle bb|)
 =n\sum_a|aa\rangle\langle aa|
  -|\Phi_n\rangle\langle\Phi_n|,
 \tag{17}
\]
gives the explicit decomposition
\[
\boxed{
\begin{aligned}
 I-P_{\Phi_n}
 ={}&\frac1n\sum_{a<b}\sum_{\theta\in\Theta}
 |p_{ab,\theta}\rangle\langle p_{ab,\theta}|\\
 &+\frac{n-1}{n}
 \sum_{a\ne b}|ab\rangle\langle ab|.
\end{aligned}}                                           \tag{18}
\]
Every coefficient is positive. \(\square\)

We now apply this with \(n=9\).  Use the Choi convention
\[
 J_{\cal R}
 =\sum_{a,b}{\cal R}(|a\rangle\langle b|)
       \otimes|a\rangle\langle b|.                       \tag{19}
\]
For the trace-replacement map
\({\cal E}(X)=\operatorname{Tr}(X)I_n\), one has
\[
 J_{\cal E}=I_{n^2},\qquad
 J_{\operatorname{id}}=|\Phi_n\rangle\langle\Phi_n|.
 \tag{20}
\]
Thus the first map in (11), regarded as a map on \(M_9\), has
\[
\begin{aligned}
 J_{\cal A}
 &=2I-\frac16|\Phi_9\rangle\langle\Phi_9|\\
 &=\frac12I+\frac32(I-P_{\Phi_9}).                       \tag{21}
\end{aligned}
\]
Equation (18), together with the evident product decomposition of
\(I\), proves directly that \(J_{\cal A}\) is a finite positive sum
\[
 J_{\cal A}=\sum_\mu X_\mu\otimes Y_\mu,\qquad
 X_\mu,Y_\mu\succeq0.                                   \tag{22}
\]

For clarity, (22) implies the precise property used below.  The Choi
formula gives
\[
 {\cal A}(Z)
 =\sum_\mu X_\mu
   \operatorname{Tr}(Y_\mu^{\mathsf T}Z).
 \tag{23}
\]
Therefore, for every positive \(W\) on
\(\mathbb C^9\otimes{\cal R}\),
\[
 ({\cal A}\otimes\operatorname{id}_{\cal R})(W)
 =\sum_\mu X_\mu\otimes
 \operatorname{Tr}_{\mathbb C^9}
 \left[(Y_\mu^{\mathsf T}\otimes I)W\right]              \tag{24}
\]
is a positive sum of product operators across
\(\mathbb C^9:{\cal R}\).  Positivity of the second factors in (24)
follows, for example, by testing against a vector on \({\cal R}\) and
cyclically inserting the positive square root of \(Y_\mu^{\mathsf T}\).

## 4. The two-dimensional-ancilla lemma

### Lemma 4.1

For every positive \(Z\) on \(\mathbb C^3\otimes\mathbb C^2\),
\[
 (\Phi\otimes\operatorname{id}_2)(Z)\succeq0,\qquad
 \Phi(X)=\operatorname{Tr}(X)I_3-\frac12X.               \tag{25}
\]

### Proof

By a spectral decomposition it suffices to take
\(Z=|z\rangle\langle z|\).  The Schmidt rank of \(z\) is at most two,
so write
\[
 |z\rangle
 =\sum_{r=1}^m\sqrt{\lambda_r}
 |a_r\rangle|b_r\rangle,\qquad m\leq2.                  \tag{26}
\]
Put
\[
 \rho=\operatorname{Tr}_{\mathbb C^3}|z\rangle\langle z|
 =\sum_r\lambda_r|b_r\rangle\langle b_r|.
 \tag{27}
\]
For an arbitrary \(w\), Cauchy--Schwarz applied to the \(m\) Schmidt
terms gives
\[
 |\langle z,w\rangle|^2
 \leq m\,\langle w|I_3\otimes\rho|w\rangle
 \leq2\,\langle w|I_3\otimes\rho|w\rangle.               \tag{28}
\]
Consequently
\[
 I_3\otimes\rho-\frac12|z\rangle\langle z|\succeq0,
 \tag{29}
\]
which is (25). \(\square\)

Apply (24) to \(P\), with
\({\cal R}=\mathbb C^3\otimes K\).  It gives
\[
 {\cal A}(P)=\sum_\mu X_\mu^{12}\otimes Z_\mu^{3K},
 \qquad X_\mu,Z_\mu\succeq0.                            \tag{30}
\]
The logical space \(K\) has dimension two.  Since \({\cal A}\) and
\(\Phi_3\) commute, Lemma 4.1 applied termwise to (30) proves
\[
 {\cal A}\Phi_3(P)\succeq0.                              \tag{31}
\]

## 5. The completely positive remainder

It remains to treat the second term in (13).  On each local qutrit
input--output pair, let
\[
 P_i=\frac13|\Phi_3\rangle\langle\Phi_3|,\qquad
 Q_i=I-P_i.                                               \tag{32}
\]
The Choi matrices of the maps in (11) are
\[
\begin{aligned}
 J_{\cal A}
 &=2I-\frac32P_1P_2,\\
 J_{\cal B}
 &=\left(I-\frac12P_1\right)
   \left(I-\frac12P_2\right).
\end{aligned}                                             \tag{33}
\]
Therefore
\[
\boxed{
 J_{\frac12{\cal A}-{\cal B}}
 =\frac12(P_1Q_2+Q_1P_2)\succeq0.
}                                                        \tag{34}
\]
The map \(\frac12{\cal A}-{\cal B}\) is consequently completely
positive, directly from a spectral decomposition of its positive
Choi matrix.  Hence
\[
 \left(\frac12{\cal A}-{\cal B}\right)(P)\succeq0.       \tag{35}
\]

Equations (13), (31), and (35) prove
\(S_V-F_{12}\succeq0\).  By the lossless frame equivalence in
Section 1, this proves (1).

## 6. Equality and the next Gram problem

If equality holds in (1), its Schur-transformed output
\[
 w=S_V^{-1}(B_{12}\otimes I_3)V
\]
satisfies \((S_V-F_{12})w=0\), and hence lies simultaneously in the
kernels of the two positive operators in (13).  The second positive
map is especially explicit from (34): its Choi support consists
exactly of the sectors with one local maximally entangled Choi
direction and one orthogonal direction.

For the unrestricted three-component residual, define the three
coefficient-to-output maps \({\cal M}_{12},{\cal M}_{13},
{\cal M}_{23}\).  This note proves positivity of every diagonal block
\[
 2I-{\cal M}_{ij}^\dagger S_V^{-1}{\cal M}_{ij}\succeq0.
 \tag{36}
\]
The remaining issue is not another one-component estimate: it is the
common off-diagonal polarization
\[
 -{\cal M}_{ij}^\dagger S_V^{-1}{\cal M}_{ik}.
 \tag{37}
\]
The factorization (13) supplies an exact positive residual Gram for
each diagonal.  A two-component proof must determine whether these
three residual Grams admit compatible cross terms whose \(2\times2\)
block matrices remain positive.
