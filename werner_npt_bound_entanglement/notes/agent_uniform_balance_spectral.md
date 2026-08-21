# Complement balance and the four-site Pauli-Gram obstruction

## Status

This note gives an exact reduction of the proposed four-site slice
inequality
\[
 A_T=A_{\bar T}\quad(0<|T|<4)
 \quad\Longrightarrow\quad p_{1234}\geq\frac18                 \tag{1}
\]
to a spectral assertion about one real symmetric \(3\times3\) matrix.
It also derives all consequences of the strong three-block inequality
that were tested in this reduction.

The spectral assertion has **not** been proved.  Moreover, the formal
permutation-symmetric point passes all of the resulting quadratic
strong-\(Q_3\) inequalities while violating the spectral assertion.
Thus any successful proof of (1) must use nonlinear compatibility of the
reduced channels belonging to one common code isometry, not merely their
individual Pauli Gram matrices.

All identities below are exact.

## 1. Reduced logical channels

Let
\[
 U:\mathbb C^2\longrightarrow
 (\mathbb C^3)^{\otimes4}
\]
be an isometry and \(P=UU^\dagger\).  Use the Pauli basis
\(\sigma_0=I,\sigma_1,\sigma_2,\sigma_3\), normalized by
\(\operatorname{Tr}(\sigma_\mu\sigma_\nu)=2\delta_{\mu\nu}\), and put
\[
 {\cal N}_T(B)=\operatorname{Tr}_{\bar T}(UBU^\dagger).
\]
Write
\[
 J_T={\cal N}_T(I),\qquad X_{T,a}={\cal N}_T(\sigma_a),
\]
and let
\[
 \Gamma_T=
 \begin{pmatrix}
 A_T&b_T^{\,t}\\
 b_T&G_T
 \end{pmatrix},                                             \tag{2}
\]
where
\[
 A_T=\operatorname{Tr}J_T^2,\quad
 (b_T)_a=\operatorname{Re}\operatorname{Tr}(J_TX_{T,a}),\quad
 (G_T)_{ab}=\operatorname{Re}\operatorname{Tr}(X_{T,a}X_{T,b}).
\]
Thus, for \(B=b_0I+b\cdot\sigma\),
\[
 q_T(B):=\|{\cal N}_T(B)\|_2^2
 =(b_0,b)^t\Gamma_T(b_0,b).                                 \tag{3}
\]

The exact logical Pauli complement identity is
\[
 \Gamma_T-\Gamma_{\bar T}
 =(A_T-A_{\bar T})\operatorname{diag}(1,-1,-1,-1).          \tag{4}
\]
Consequently, under the complement-balance hypothesis in (1),
\[
 \Gamma_T=\Gamma_{\bar T}\qquad(0<|T|<4),                   \tag{5}
\]
and
\[
 \operatorname{tr}G_T
 =2A_{\bar T}-A_T=A_T.                                      \tag{6}
\]

Define
\[
 D=\sum_{|T|=2}G_T-2\sum_{|T|=1}G_T,\qquad
 t=\operatorname{tr}D
   =\sum_{|T|=2}A_T-2\sum_{|T|=1}A_T.                       \tag{7}
\]

## 2. Exact cross-sector formula

Fix a unit Bloch vector \(x\).  Let \(u_x,v_x\) be the two orthonormal
encoded states corresponding to the antipodal logical pure states
\((I\pm x\cdot\sigma)/2\), and set
\[
 g_T(x)=\operatorname{Tr}
 \bigl(\rho_T^{u_x}\rho_T^{v_x}\bigr).
\]
Direct expansion gives
\[
 g_T(x)=\frac14\bigl(A_T-x^tG_Tx\bigr).                     \tag{8}
\]
For an ordered cross tensor define
\[
 c_R(x)=\|\Pi_R(u_x\otimes v_x)\|^2.
\]
Fourier expansion of the local symmetric/antisymmetric projections gives
\[
 c_R(x)=\frac1{16}\sum_{T\subseteq[4]}
 (-1)^{|R\cap T|}g_T(x).                                   \tag{9}
\]
Here \(g_\varnothing=1\), \(g_{[4]}=0\), and complement balance implies
\(g_T=g_{\bar T}\) for every proper nonempty \(T\).  Taking
\(R=[4]\) in (9) and then using (8) yields
\[
 \boxed{\qquad
 16c_{[4]}(x)=1+\frac{t-x^tDx}{4}.
 \qquad}                                                    \tag{10}
\]

This formula explains why the stronger basiswise claim
\(c_{[4]}(x)\geq1/16\) is false: it asks for \(x^tDx\leq t\) for every
\(x\).  Even the repetition code violates that statement after a generic
logical basis rotation.

## 3. The all-antisymmetric sector effect

Let
\[
 E_{[4]}=
 (U^\dagger\otimes U^\dagger)\Pi_{[4]}(U\otimes U)
 \big|_{\operatorname{Sym}^2(\mathbb C^2)}.
\]
The vector
\[
 s_x=\frac{u_x\otimes v_x+v_x\otimes u_x}{\sqrt2}
\]
is the spin-one \(m=0\) state in direction \(x\).  Because the fourfold
antisymmetric local sector has positive global replica parity,
\[
 \langle s_x,E_{[4]}s_x\rangle=2c_{[4]}(x).                 \tag{11}
\]
Under the standard real-vector model of the spin-one representation,
(10)--(11) determine the real symmetric part of the effect:
\[
 \boxed{\qquad
 \operatorname{Re}E_{[4]}
 =\left(\frac18+\frac{t}{32}\right)I_3-\frac1{32}D.
 \qquad}                                                    \tag{12}
\]
Taking the trace gives the particularly simple identity
\[
 \boxed{\qquad
 p_{[4]}=\operatorname{Tr}E_{[4]}=\frac{6+t}{16}.
 \qquad}                                                    \tag{13}
\]
Thus (1) is exactly the scalar claim
\[
 t\geq-4.                                                   \tag{14}
\]

### A sufficient spectral lemma

If
\[
 \lambda_{\min}(D)\leq\operatorname{tr}D=t,                 \tag{15}
\]
choose a unit eigenvector \(x\) for \(\lambda_{\min}(D)\).  Equation
(10) gives \(c_{[4]}(x)\geq1/16\).  Since \(E_{[4]}\succeq0\),
\[
 p_{[4]}=\operatorname{Tr}E_{[4]}
 \geq\langle s_x,E_{[4]}s_x\rangle
 =2c_{[4]}(x)\geq\frac18.                                  \tag{16}
\]
In particular, (1) follows if \(D\) has at most one negative eigenvalue.
The weaker exact condition in (15) is
\[
 \lambda_2(D)+\lambda_3(D)\geq0
\]
for increasingly ordered eigenvalues.

This is the current finite-dimensional target.

## 4. An exact boundary case

Suppose complement balance holds and, for some logical basis \(u,v\) and
some physical site \(i\),
\[
 g_{\{i\}}=\operatorname{Tr}(\rho_i^u\rho_i^v)=0.           \tag{17}
\]
For positive semidefinite matrices, zero Hilbert--Schmidt product implies
orthogonal supports.  Hence \(g_T=0\) for every \(T\) containing \(i\).
If \(T\) does not contain \(i\) and is nonempty and proper, then
\(\bar T\) contains \(i\), so complement balance gives
\(g_T=g_{\bar T}=0\).  Together with
\(g_\varnothing=1,g_{[4]}=0\), equation (9) gives
\[
 c_{[4]}=\frac1{16}.
\]
Therefore
\[
 p_{[4]}\geq2c_{[4]}=\frac18.                               \tag{18}
\]
This proves (1) on the entire stratum where one antipodal logical basis
has orthogonal one-site reductions.

## 5. Strong \(Q_3\) for every positive logical filter

Let
\[
 B=b_0I+b\cdot\sigma\succeq0,\qquad b_0\geq|b|.
\]
Then
\[
 \operatorname{Tr}(UBU^\dagger)=2b_0,\qquad
 \operatorname{Tr}(UBU^\dagger)^2=2(b_0^2+|b|^2).
\]
The strong three-block inequality applied to the positive operator
\(UBU^\dagger\) says
\[
 Q_3(UBU^\dagger)
 \geq\frac18\left(
 2\operatorname{Tr}(UBU^\dagger)^2
 -(\operatorname{Tr}UBU^\dagger)^2\right)
 =\frac12|b|^2.                                             \tag{19}
\]

Group the four sites as the three blocks
\(\{i\},\{j\},\{k,l\}\).  Using (5), direct expansion of the left side is
\[
 Q_3(UBU^\dagger)
 =\frac32b_0^2+2|b|^2
 -\frac14\bigl(q_i(B)+q_j(B)+q_{ij}(B)\bigr).
\]
Thus every unordered pair \(\{i,j\}\) obeys the exact Lorentz-cone
quadratic inequality
\[
 \boxed{\qquad
 q_i(B)+q_j(B)+q_{ij}(B)
 \leq6(b_0^2+|b|^2)=3q_{[4]}(B).
 \qquad}                                                    \tag{20}
\]

There is a second family obtained by conditioning a site.  Fix \(l\),
condition \(UBU^\dagger\) on a Haar-random qutrit line at \(l\), and
apply (19) to the remaining three sites.  The elementary identity
\[
 \int |x\rangle\langle x|^{\otimes2}\,dx
 =\frac{I+F_l}{12}                                         \tag{21}
\]
shows, before complement simplification, that the averaged inequality is
\[
 \sum_{T\subseteq\bar l}
 \left(-\frac12\right)^{3-|T|}
 \bigl(q_T(B)+q_{T\cup\{l\}}(B)\bigr)
 \geq\frac18\left[
 2(q_{\bar l}(B)+q_{[4]}(B))
 -(q_\varnothing(B)+q_l(B))\right].
 \]
Using (5) reduces this exactly to
\[
 \boxed{\qquad
 \sum_{i\ne l}q_i(B)
 +\sum_{\{i,j\}\subseteq\bar l}q_{ij}(B)
 \leq3\bigl(q_l(B)+q_{[4]}(B)\bigr).
 \qquad}                                                    \tag{22}
\]

Put
\[
 S_1=\sum_iq_i(B),\qquad S_2=\sum_{i<j}q_{ij}(B).
\]
Summing (20) over the six pairs and (22) over the four choices of \(l\)
gives respectively
\[
 3S_1+S_2\leq18q_{[4]},\qquad
 S_2\leq6q_{[4]}.                                          \tag{23}
\]
If the two nonnegative defects are
\[
 {\cal A}=18q_{[4]}-3S_1-S_2,\qquad
 {\cal C}=12q_{[4]}-2S_2,
\]
then the quadratic form associated with the full \(4\times4\) Gram
combination satisfies
\[
 S_2-2S_1
 =-2q_{[4]}+\frac23{\cal A}-\frac56{\cal C}.                \tag{24}
\]
The opposite signs of the two defects are the obstruction: these
strong-\(Q_3\) consequences do not control the sign or inertia of \(D\).

## 6. Exact formal obstruction to every quadratic Gram-only proof

At the permutation-symmetric formal target, put
\[
 A_1=\frac{77}{40},\qquad A_2=\frac{17}{10},
\]
and take the isotropic proper-subset Gram matrices
\[
 \Gamma_i=
 \operatorname{diag}\left(\frac{77}{40},
 \frac{77}{120}I_3\right),\qquad
 \Gamma_{ij}=
 \operatorname{diag}\left(\frac{17}{10},
 \frac{17}{30}I_3\right).                                  \tag{25}
\]
They obey complement balance and \(\operatorname{tr}G_T=A_T\).  In (20)
the scalar and spatial slacks are, exactly,
\[
 6-\left(2\frac{77}{40}+\frac{17}{10}\right)=\frac9{20},
\qquad
 6-\left(2\frac{77}{120}+\frac{17}{30}\right)=\frac{83}{20}.
\]
In (22) the scalar and spatial slacks are
\[
 6-3\frac{17}{10}=\frac9{10},\qquad
 6-\frac{17}{10}=\frac{43}{10}.
\]
Thus all grouped and conditioned strong-\(Q_3\) inequalities hold
strictly for every positive logical \(B\).

Nevertheless,
\[
 D=6\left(\frac{17}{30}I_3\right)
 -8\left(\frac{77}{120}I_3\right)
 =-\frac{26}{15}I_3,\qquad
 t=-\frac{26}{5}.                                          \tag{26}
\]
So \(D\) has three negative eigenvalues, (15) fails, and (13) gives
\[
 p_{[4]}=\frac1{20}<\frac18.
\]

This is not a physical-code counterexample; it is a sharp obstruction to
the proof method.  A proof of (1) must exclude the simultaneous
realizability of (25) using a nonlinear identity or inequality coupling
the channels \({\cal N}_T\) that arise from the same tensor \(U\).

## Research log

- **2026-07-28 17:50--18:26 PDT.** Derived the cross-sector formula
  (10), the spin-one effect formula (12), and the exact identity
  \(p_{[4]}=(6+\operatorname{tr}D)/16\).  Isolated
  \(\lambda_{\min}(D)\leq\operatorname{tr}D\) as a sufficient
  three-dimensional spectral target.
- **2026-07-28 18:05--18:26 PDT.** Applied strong \(Q_3\) both to every
  positive logical filter and to every one-site Haar conditioning.
  The formal isotropic point (25) passes all resulting inequalities
  strictly, proving that the missing obstruction is nonlinear
  common-isometry compatibility rather than quadratic Pauli-Gram data.
