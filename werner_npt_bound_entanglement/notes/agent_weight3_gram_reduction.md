# Exact weight-three Gram reduction for a balanced four-qutrit code

## Status

For a complement-balanced rank-two code, the \(3\times3\) matrix
\[
 D=\sum_{|T|=2}G_T-2\sum_{|T|=1}G_T
\]
from `agent_uniform_balance_spectral.md` has the exact factorization
\[
 \boxed{\qquad D=-\frac92\,W_3\preceq0,\qquad}              \tag{1}
\]
where \(W_3\) is the Gram matrix of the exact operator-weight-three
components of the three encoded logical Pauli matrices.

Thus the four-copy problem on the complement-balanced slice is reduced
to the following explicit rank-two/Pluecker statement:
\[
 \boxed{\qquad \operatorname{rank}W_3\leq2.\qquad}          \tag{2}
\]
Equivalently, there is a nonzero logical Bloch direction \(x\) such that
the encoded traceless operator
\[
 \tau_x=U(x\cdot\sigma)U^\dagger
\]
has no exact-weight-three component.

If (2) holds, then \(p_{[4]}\geq1/8\), and hence the balanced frontier is
settled.  Equation (1) is proved below; equation (2) remains unproved.

## 1. Exact-support decomposition

At each qutrit site choose a Hermitian Hilbert--Schmidt orthonormal
operator basis
\[
 e_0=\frac{I_3}{\sqrt3},\qquad e_1,\ldots,e_8,
\]
where \(e_1,\ldots,e_8\) are traceless.  For the code isometry
\[
 U:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes4},
\]
put
\[
 \tau_a=U\sigma_aU^\dagger,\qquad a=1,2,3.
\]
Expand
\[
 \tau_a
 =\sum_{\boldsymbol\mu}
 c_{a,\boldsymbol\mu}\,
 e_{\mu_1}\otimes e_{\mu_2}\otimes
 e_{\mu_3}\otimes e_{\mu_4}.                              \tag{3}
\]
The coefficients are real because both the basis operators and
\(\tau_a\) are Hermitian.

For a multi-index \(\boldsymbol\mu\), define its exact support by
\[
 \operatorname{supp}\boldsymbol\mu
 =\{i:\mu_i\ne0\}.
\]
For every \(R\subseteq[4]\), define the real positive semidefinite Gram
matrix
\[
 (W_R)_{ab}
 =
 \sum_{\operatorname{supp}\boldsymbol\mu=R}
 c_{a,\boldsymbol\mu}c_{b,\boldsymbol\mu}.                 \tag{4}
\]
Write
\[
 W_k=\sum_{|R|=k}W_R.
\]
Since every \(\tau_a\) is traceless,
\[
 W_\varnothing=0.                                         \tag{5}
\]

## 2. Partial-trace Pauli Grams

Let
\[
 X_{T,a}=\operatorname{Tr}_{\bar T}\tau_a,\qquad
 (G_T)_{ab}=\operatorname{Tr}(X_{T,a}X_{T,b}).
\]
A term in (3) survives the trace over \(\bar T\) exactly when its support
is contained in \(T\).  Every traced \(e_0\) contributes
\(\operatorname{Tr}e_0=\sqrt3\).  Orthonormality of the surviving tensor
basis therefore gives
\[
 \boxed{\qquad
 G_T=3^{\,4-|T|}\sum_{R\subseteq T}W_R.
 \qquad}                                                   \tag{6}
\]
This formula fixes all normalization factors.

In particular,
\[
 G_{\{i\}}=27W_{\{i\}},                                   \tag{7}
\]
and
\[
 G_{\bar i}
 =3\sum_{\varnothing\ne R\subseteq\bar i}W_R.              \tag{8}
\]

## 3. Complement balance

The exact logical Pauli complement identity implies that scalar
complement balance \(A_T=A_{\bar T}\) gives
\[
 G_T=G_{\bar T}
\]
for every proper nonempty \(T\).  Applying this only to the four
singleton/triple pairs and using (7)--(8) yields
\[
 9W_{\{i\}}
 =
 \sum_{\varnothing\ne R\subseteq\bar i}W_R.                \tag{9}
\]
Sum (9) over \(i\).  On its right side:

- every exact-weight-one matrix occurs three times;
- every exact-weight-two matrix occurs twice;
- every exact-weight-three matrix occurs once.

Consequently,
\[
 9W_1=3W_1+2W_2+W_3,
\]
or
\[
 \boxed{\qquad 6W_1=2W_2+W_3.\qquad}                      \tag{10}
\]

On the other hand, (6) gives
\[
\begin{aligned}
 \sum_{|T|=2}G_T
 &=9(3W_1+W_2),\\
 2\sum_{|T|=1}G_T
 &=54W_1.
\end{aligned}
\]
Therefore
\[
\begin{aligned}
 D
 &=9(W_2-3W_1)\\
 &=-\frac92W_3,
\end{aligned}
\]
which proves (1).

## 4. Why singularity would finish the balanced problem

The real symmetric part of the all-antisymmetric logical spin-one
effect is already known exactly:
\[
 \operatorname{Re}E_{[4]}
 =\frac{(4+t)I_3-D}{32},
 \qquad t=\operatorname{Tr}D.                              \tag{11}
\]
Since \(E_{[4]}\succeq0\), its real part is positive semidefinite on real
vectors.

Assume (2), and choose a real unit vector \(x\in\ker W_3=\ker D\).
Equation (11) gives
\[
 0\leq x^t\operatorname{Re}E_{[4]}x
 =\frac{4+t}{32}.
\]
Thus
\[
 t\geq-4.
\]
Using
\[
 p_{[4]}=\frac{6+t}{16}
\]
then gives
\[
 \boxed{\qquad p_{[4]}\geq\frac18.\qquad}                  \tag{12}
\]

The missing statement (2) has several equivalent forms:

1. every \(3\times3\) minor of the stacked exact-weight-three
   coefficient map vanishes;
2. all Bloch coefficient vectors of exact-weight-three physical
   operators lie in one common plane;
3. after one logical \(SU(2)\) basis change, all exact-weight-three
   compressions are simultaneously real, with no \(\sigma_y\)
   component;
4. the partial transpose of \(E_{[4]}\) has a maximally entangled
   eigenvector with eigenvalue \(1/16\).

Any proof must use the common rank-two origin
\(\tau_a=U\sigma_aU^\dagger\); the linear Pauli-Gram constraints alone
allow \(W_3\) to be positive definite.

