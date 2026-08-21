# The balanced Lorentz determinant as one exact-weight-three Gram determinant

## Status

Let
\[
 U:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes4}
\]
be a code isometry, put \(P=UU^\dagger\), and define the encoded Pauli
operators
\[
 \tau_0=P,\qquad \tau_a=U\sigma_aU^\dagger\quad(1\leq a\leq3).
\]
Assume the four singleton/complement purity balances.  This note proves
the exact identity
\[
 \boxed{\qquad
 18\bigl(\widehat\Gamma+2\eta\bigr)
 =128E_{00}-81Z_3,
 \qquad}                                                    \tag{1}
\]
where

- \(\eta=\operatorname{diag}(1,-1,-1,-1)\);
- \(\widehat\Gamma=\sum_{T\subseteq[4]}(-1)^{|T|}\Gamma_T\)
  is the alternating reduced-channel Pauli Gram;
- \(E_{00}\) is the matrix unit in the \(\tau_0\) direction; and
- \(Z_3\succeq0\) is the Gram matrix of the exact operator-weight-three
  coefficient vectors of \(\tau_0,\tau_1,\tau_2,\tau_3\).

Since left multiplication by \(\eta\) changes a determinant only by a
sign, the conjectural fixed Lorentz eigenvalue \(-2\),
\[
 \det(\eta\widehat\Gamma+2I_4)=0,
                                                               \tag{2}
\]
is therefore equivalent to the single exact-support identity
\[
 \boxed{\qquad
 \det(128E_{00}-81Z_3)=0.
 \qquad}                                                       \tag{3}
\]

Identity (1) is proved below.  The singularity assertion (3) remains
unproved.  It is a strictly smaller nonlinear common-code lemma: all
linear complement-balance algebra and every normalization constant have
already been eliminated.

### Hypothesis audit

Only the four singleton/triple equalities
\[
 A_{\{i\}}=A_{\bar i}\qquad(i=1,2,3,4)                      \tag{H}
\]
are used anywhere in the proof of (1).  In particular, the three
pair/pair equalities
\[
 A_{\{i,j\}}=A_{\overline{\{i,j\}}}
\]
are **not** assumed.

This distinction matters.  On the stronger seven-balance locus the
logical bivector has uniform mass in its eight odd local-swap sectors.
That conclusion from (H) alone is a separate, presently unproved
nonlinear assertion (equivalently, the sharp odd-sector defect
inequality discussed elsewhere in the project).  Neither uniform odd
sectors nor any numerically observed cubic-moment identity is used
below.

## 1. Exact-support Pauli Grams

Choose at every qutrit site a Hermitian Hilbert--Schmidt orthonormal
operator basis
\[
 e_0=\frac{I_3}{\sqrt3},\qquad e_1,\ldots,e_8,
\]
with the last eight elements traceless.  Expand
\[
 \tau_\mu
 =\sum_{\boldsymbol\alpha}
 c_{\mu,\boldsymbol\alpha}\,
 e_{\alpha_1}\otimes e_{\alpha_2}\otimes
 e_{\alpha_3}\otimes e_{\alpha_4}.
                                                               \tag{4}
\]
For \(R\subseteq[4]\), let \(C_R\) be the matrix whose \(\mu\)-th
column consists of the coefficients in (4) having exact support \(R\),
and put
\[
 Z_R=C_R^\dagger C_R,\qquad
 Z_k=\sum_{|R|=k}Z_R.                                        \tag{5}
\]
Thus every \(Z_R\) and \(Z_k\) is a real positive semidefinite
\(4\times4\) Gram matrix.

Pauli orthogonality gives
\[
 \sum_{k=0}^4Z_k
 =\bigl(\operatorname{Tr}\tau_\mu\tau_\nu\bigr)_{\mu,\nu=0}^3
 =2I_4.                                                       \tag{6}
\]
Only \(\tau_0=P\) has a nonzero identity coefficient.  Since
\(\operatorname{Tr}P=2\) and
\(e_0^{\otimes4}=I_{81}/9\),
\[
 c_{0,\boldsymbol0}=\frac29,\qquad
 \boxed{\quad Z_0=\frac4{81}E_{00}.\quad}                    \tag{7}
\]

## 2. Reduced-channel Grams and Möbius weights

For \(T\subseteq[4]\), let
\[
 {\cal N}_T(B)=\operatorname{Tr}_{\bar T}(UBU^\dagger),
\qquad
 (\Gamma_T)_{\mu\nu}
 =\operatorname{Tr}\bigl({\cal N}_T(\sigma_\mu)
                         {\cal N}_T(\sigma_\nu)\bigr).
                                                               \tag{8}
\]
A term of exact support \(R\) survives the trace over \(\bar T\)
exactly when \(R\subseteq T\).  Each traced identity basis element
contributes \(\operatorname{Tr}e_0=\sqrt3\).  Hence
\[
 \boxed{\qquad
 \Gamma_T=3^{\,4-|T|}\sum_{R\subseteq T}Z_R.
 \qquad}                                                       \tag{9}
\]

Alternating (9) over all \(T\) gives
\[
\begin{aligned}
 \widehat\Gamma
 &=\sum_{T\subseteq[4]}(-1)^{|T|}\Gamma_T\\
 &=\sum_{R\subseteq[4]}Z_R
   \sum_{T\supseteq R}(-1)^{|T|}3^{\,4-|T|}\\
 &=\sum_{R\subseteq[4]}(-1)^{|R|}2^{\,4-|R|}Z_R.
\end{aligned}                                                \tag{10}
\]
In level notation,
\[
 \widehat\Gamma
 =16Z_0-8Z_1+4Z_2-2Z_3+Z_4.                                \tag{11}
\]

## 3. What the four singleton balances say

The exact logical Pauli complement identity says that scalar
singleton/complement balance upgrades to
\[
 \Gamma_{\{i\}}=\Gamma_{\bar i}.
                                                               \tag{12}
\]
Using (9),
\[
 27(Z_0+Z_{\{i\}})
 =3\sum_{R\subseteq\bar i}Z_R.
                                                               \tag{13}
\]
Sum (13) over the four sites.  A support of size \(r\leq3\) occurs in
exactly \(4-r\) of the complements.  Therefore
\[
 108Z_0+27Z_1
 =12Z_0+9Z_1+6Z_2+3Z_3,
\]
or
\[
 \boxed{\qquad
 32Z_0+6Z_1-2Z_2-Z_3=0.
 \qquad}                                                       \tag{14}
\]

## 4. Elimination of weights zero, one, two, and four

First eliminate \(Z_4\) from (11) using (6):
\[
 \widehat\Gamma
 =2I_4+15Z_0-9Z_1+3Z_2-3Z_3.                              \tag{15}
\]
Equation (14) gives
\[
 -9Z_1=-3Z_2-\frac32Z_3+48Z_0.                             \tag{16}
\]
Substitution into (15) cancels \(Z_1\) and \(Z_2\) completely:
\[
 \boxed{\qquad
 \widehat\Gamma
 =2I_4+63Z_0-\frac92Z_3.
 \qquad}                                                       \tag{17}
\]

Finally,
\[
 2I_4+2\eta=4E_{00},
\]
and (7) gives
\[
\begin{aligned}
 \widehat\Gamma+2\eta
 &=4E_{00}+63\frac4{81}E_{00}-\frac92Z_3\\
 &=\frac{64}{9}E_{00}-\frac92Z_3.
\end{aligned}                                                \tag{18}
\]
Multiplying by \(18\) proves (1).

## 5. Determinant equivalence and the remaining lemma

Because \(\det\eta=-1\),
\[
 \det(\eta\widehat\Gamma+2I_4)
 =-\det(\widehat\Gamma+2\eta).                              \tag{19}
\]
Equation (1) therefore proves the equivalence between (2) and (3).

Writing
\[
 Z_3=
 \begin{pmatrix}
 z_{00}&z_0^t\\
 z_0&W_3
 \end{pmatrix},
                                                               \tag{20}
\]
the spatial block \(W_3\) is precisely the exact-weight-three Gram of
the three encoded traceless Pauli operators.  Thus a stronger sufficient
lemma is
\[
 \operatorname{rank}W_3\leq2
 \quad\text{and}\quad
 z_0\perp\ker W_3.                                          \tag{21}
\]
Numerical balanced frames satisfy the still stronger common-kernel
statement: the same purely spatial vector annihilates every proper
exact-support coefficient map.  That observation is discovery evidence,
not part of this proof.

The remaining exact target can be stated without Pauli coordinates:

> **Residual exact-weight-three Plücker lemma.**  If a rank-two qutrit
> code obeys its four singleton/complement purity balances, then the
> four exact-weight-three coefficient vectors of
> \(P,U\sigma_1U^\dagger,U\sigma_2U^\dagger,U\sigma_3U^\dagger\) have
> Gram matrix \(Z_3\) satisfying
> \[
> \det(128E_{00}-81Z_3)=0.
> \]

Proving this lemma proves the fixed Lorentz eigenvalue and, through the
already established negative-semidefinite spatial block reduction,
the complement-balanced four-copy frontier.

## 6. Discovery observations deliberately excluded from the theorem

Floating-point Newton restoration of (H), including starts obtained
from the stronger seven-balance feasibility search, consistently gave
\[
 \operatorname{rank}W_3\leq2.
\]
On generic-looking seven-balanced frames the two nonzero eigenvalues of
\(D=-\tfrac92W_3\) were distinct and negative, while the third was zero
at the balance-residual scale.  For example, one restored frame gave
\[
 \operatorname{spec}D
 \simeq(-2.13683026,-0.64429898,-1.4\cdot10^{-15}).
\]

The same frames exhibited two stronger phenomena:

1. for each site \(i\), if the two codewords are flattened as
   \(3\times27\) matrices \(U_i,V_i\), then
   \[
   \operatorname{rank}\begin{bmatrix}U_i\\V_i\end{bmatrix}=3;
   \]
2. on the stronger seven-balance locus, the cubic complementary
   difference
   \[
   \operatorname{Tr}(J_i+x\cdot X_i)^3
   -\operatorname{Tr}(J_{\bar i}+x\cdot X_{\bar i})^3
   \]
   vanished at numerical residual scale for every site.

For an arbitrary code the last polynomial vanishes on \(|x|=1\), hence
has the exact form
\[
 (|x|^2-1)(c_i+\ell_i\cdot x).
\]
The numerical statement is that \(c_i=\ell_i=0\) on the tested stronger
balanced frames.  No proof that (H), or even the seven equalities, forces
either phenomenon is known.  They are recorded only as possible
equality-classification targets and are not part of the determinant
reduction.

The exact stopping point of this track is therefore (3), or the
stronger sufficient statement
\[
 \operatorname{rank}W_3\leq2.
\]
No four-copy theorem and no four-copy counterexample follows without
proving one of these residual assertions.
