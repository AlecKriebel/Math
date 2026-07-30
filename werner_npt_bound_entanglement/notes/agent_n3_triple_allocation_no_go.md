# An exact no-go for splitting off the triple-Hodge correction

## Status

This note records an exact obstruction inside the stronger shifted
degree-two program
\[
 \|\Pi _2C\|_2^2
 \leq \frac49\bigl(\|C\|_2^2+s_1(C)s_2(C)\bigr).
 \tag{1}
\]
It does not disprove (1).

Let
\[
 {\mathsf A}_i=\frac{I-F_i}{2}
 \tag{2}
\]
on two physical replicas.  The positive feature operator associated
with the rank-one degree-two slack is
\[
 {\mathsf S}
 =
 \left(\frac49I-\Pi _2\right)^\Gamma
 =
 \frac49\sum_{i<j}{\mathsf A}_i{\mathsf A}_j
 +\frac89{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3.
 \tag{3}
\]
A natural proposed certificate is to allocate a scalar multiple of
the pure triple-Hodge channel as the universal \(2/9\) correction and
prove that the remainder has two-block-positive partial transpose.
The following theorem rules out every such allocation at once.

> **Theorem.**  For every real \(\lambda\), the operator
> \[
>  {\mathsf T}_\lambda
>  =
>  {\mathsf S}
>  -\lambda{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3
>  \tag{4}
> \]
> has a partial transpose which is not two-block-positive.

Thus the exact-two-skew and triple-skew channels must remain
coherently mixed.  No proof can isolate a correction supported only
on the all-antisymmetric physical sector and leave a separately
two-block-positive matched Gram.

The dependency-free exact checker is
`verification/verify_n3_triple_allocation_no_go.py`.

## 1. The two feature forms

For a coefficient matrix \(C\), write
\[
\begin{aligned}
 N&=\|C\|_2^2,\\
 S_1&=\sum_i\|\operatorname{Tr}_iC\|_2^2,\\
 S_2&=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2,\\
 T&=|\operatorname{Tr}C|^2.
\end{aligned}
\tag{5}
\]
The exact two-skew and triple-skew contractions are
\[
\begin{aligned}
 {\cal J}_2(C)
 &=\frac34N-\frac12S_1+\frac14S_2,\\
 {\cal J}_3(C)
 &=\frac18(N-S_1+S_2-T).
\end{aligned}
\tag{6}
\]
Direct partial transposition of (3) gives
\[
 \langle\psi_C|{\mathsf S}^\Gamma|\psi_C\rangle
 =
 \frac49{\cal J}_2(C)+\frac89{\cal J}_3(C).
\tag{7}
\]
Consequently
\[
 \langle\psi_C|{\mathsf T}_\lambda^\Gamma|\psi_C\rangle
 =
 \frac49{\cal J}_2(C)
 +\left(\frac89-\lambda\right){\cal J}_3(C).
\tag{8}
\]

## 2. One rank-two witness for every allocation

On three qutrit operator factors put
\[
 C
 =
 |0\rangle\langle0|
 \otimes |0\rangle\langle1|
 \otimes
 \left(
 |0\rangle\langle0|+|1\rangle\langle1|
 \right).
\tag{9}
\]
The three factors have ranks \(1,1,2\), respectively, so
\[
 \operatorname{rank}C=2.
\tag{10}
\]
All quantities in (5) are integers:
\[
 N=2,\qquad S_1=6,\qquad S_2=4,\qquad T=0.
\tag{11}
\]
Substitution in (6) gives
\[
 \boxed{
 {\cal J}_2(C)=-\frac12,\qquad
 {\cal J}_3(C)=0.
 }
\tag{12}
\]
Equation (8) is therefore independent of \(\lambda\):
\[
 \boxed{
 \langle\psi_C|{\mathsf T}_\lambda^\Gamma|\psi_C\rangle
 =-\frac29<0
 \qquad(\lambda\in\mathbb R).
 }
\tag{13}
\]
The coefficient matrix has rank two, so its vectorization has
Schmidt rank two.  This proves the theorem.

For comparison, the same matrix does not violate the desired shifted
inequality.  Its two nonzero singular values are both \(1\), and its
exact degree-two mass is
\[
 \|\Pi _2C\|_2^2=\frac{10}{9}.
\tag{14}
\]
Hence
\[
 \frac49(N+s_1s_2)-\|\Pi _2C\|_2^2
 =
 \frac43-\frac{10}{9}
 =
 \frac29>0.
\tag{15}
\]
The missing \(4s_1s_2/9\) exterior allowance is therefore genuinely
coherent: it cannot be assigned to a pure triple-Hodge summand before
the pair and triple channels are combined.

## 3. Scope

The obstruction is stronger than the failure of one chosen numerical
coefficient.  Since \({\cal J}_3(C)=0\), the same exact witness defeats
every scalar redistribution along
\({\mathsf A}_1{\mathsf A}_2{\mathsf A}_3\).
It leaves open a code-dependent Hodge/Pluecker correction mixing the
three pair channels with the triple channel, equivalently the Takagi
feature-state bound
\[
 {\cal C}(Q)\leq\frac49.
\tag{16}
\]
